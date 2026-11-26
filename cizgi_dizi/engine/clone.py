"""Open-source voice-over: XTTS-v2 cloning each character from earlier expressive takes.

Every character's reference audio comes from the ElevenLabs lines already in
seslendirme/<dizi>/bolumNN/*.wav (episodes 1-6). For each new line we pick
reference clips of the same character in the same mood, so XTTS copies both
the timbre and the delivery. Characters with no takes of their own get a voice
derived from another character (pitch/tempo shifted), see DERIVED.

Usage:
  python3 engine/clone.py diziler/<dizi>/bolumler/bolumNN.json [...] [--force]
Writes seslendirme/<dizi>/bolumNN/s<scene>_l<line>.wav for every spoken line
that has no clip yet (or all lines with --force); render.py picks them up.
"""
import json
import random
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from voices import clip_name, spoken_lines  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SR = 24000  # XTTS output rate

# character -> (source character, semitones, tempo)
DERIVED = {"usta": ("riza", -2.0, 0.92), "hakan": ("kenan", -1.5, 0.97), "murat": ("can", -2.5, 1.0),
           "tarik": ("ferit", -3.0, 0.94), "hirsiz": ("can", -1.0, 1.06)}
MOOD_NEIGHBOURS = {"angry": ["angry", "worried", "smug"], "sad": ["sad", "worried", "neutral"],
                   "surprised": ["surprised", "worried", "angry"], "worried": ["worried", "surprised", "sad"],
                   "smug": ["smug", "smile", "neutral"], "smile": ["smile", "smug", "neutral"],
                   "neutral": ["neutral", "smile", "sad"]}
_model = None


def model():
    global _model
    if _model is None:
        import os
        os.environ.setdefault("COQUI_TOS_AGREED", "1")
        from TTS.api import TTS
        _model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    return _model


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def reference_bank(dizi):
    """{character: {mood: [clip paths]}} from the ElevenLabs-voiced episodes."""
    bank = {}
    base = ROOT / "seslendirme" / dizi
    for ep_path in sorted((ROOT / "diziler" / dizi / "bolumler").glob("bolum*.json")):
        ep = json.loads(ep_path.read_text(encoding="utf-8"))
        d = base / ep_path.stem
        for si, li, ln in spoken_lines(ep):
            f = d / clip_name(si, li)
            if f.exists() and not (d / f"{clip_name(si, li)}.xtts").exists() and dur(f) >= 1.8:
                bank.setdefault(ln["who"], {}).setdefault(ln.get("mood", "neutral"), []).append(f)
    return bank


def shifted(src, semitones, tempo, out):
    if out.exists():
        return out
    f = 2 ** (semitones / 12)
    af = f"asetrate={int(48000 * f)},aresample=48000,atempo={tempo / f:.4f}"
    subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-i", str(src), "-af", af, str(out)], check=True)
    return out


def pick_refs(bank, who, mood, dizi, rnd):
    src_who, semis, tempo = DERIVED.get(who, (who, 0, 1.0))
    moods = bank.get(src_who, {})
    if not moods:
        raise SystemExit(f"{who}: referans ses yok")
    chosen, total = [], 0.0
    for m in MOOD_NEIGHBOURS.get(mood, [mood]) + list(moods):
        clips = list(moods.get(m, []))
        rnd.shuffle(clips)
        for c in clips:
            if c in chosen:
                continue
            chosen.append(c)
            total += dur(c)
            if total >= 9 or len(chosen) >= 3:
                break
        if total >= 9 or len(chosen) >= 3:
            break
    if src_who != who:
        cache = ROOT / ".cache" / "refs" / who
        cache.mkdir(parents=True, exist_ok=True)
        chosen = [shifted(c, semis, tempo, cache / f"{c.parent.name}_{c.name}") for c in chosen]
    return [str(c) for c in chosen]


def synth(text, refs, out):
    wav = model().tts(text=text, speaker_wav=refs, language="tr", temperature=0.55, top_p=0.8,
                      repetition_penalty=6.0, speed=1.0, split_sentences=True)
    a = np.asarray(wav, dtype=np.float32)
    subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-ar", "48000", str(out)], input=a.tobytes(), check=True)


_whisper = None


ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def tr_number(n):
    """Spaced Turkish number words: 1999 -> 'bin dokuz yüz doksan dokuz'."""
    if n == 0:
        return "sıfır"
    words = []
    for value, name in ((1_000_000, "milyon"), (1000, "bin")):
        if n >= value:
            q, n = divmod(n, value)
            if not (value == 1000 and q == 1):
                words.append(tr_number(q))
            words.append(name)
    if n >= 100:
        q, n = divmod(n, 100)
        if q > 1:
            words.append(ONES[q])
        words.append("yüz")
    if n >= 10:
        words.append(TENS[n // 10])
        n %= 10
    if n:
        words.append(ONES[n])
    return " ".join(words)


def _words(text):
    """Normalised words; digits spelled out in Turkish so 22 == 'yirmi iki'."""
    import re
    from voices import norm
    out = []
    for w in text.split():
        for part in re.findall(r"\d+|[^\d]+", w):
            if part.isdigit():
                out += [norm(x) for x in tr_number(int(part)).split()]
            elif norm(part):
                out.append(norm(part))
    return [w for w in out if w]


def check(path, text):
    """Strict word-level match between script and what Whisper hears.

    Returns (score 0..1, heard text, cut time): audio after `cut` holds only words
    beyond the script's last word (XTTS tail babble) and can be trimmed.
    """
    import difflib
    from voices import decode
    global _whisper
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel("small", device="cpu", compute_type="int8")
    a = decode(path, 16000)
    segs, _ = _whisper.transcribe(a, language="tr", word_timestamps=True)
    heard_words = []
    for sg in segs:
        for w in sg.words:  # Whisper splits suffixes: "Zeynep" + "'in" -> "Zeynep'in"
            if heard_words and w.word.strip()[:1] in "'’":
                heard_words[-1] = (heard_words[-1][0] + w.word.strip(), w.end)
            else:
                heard_words.append((w.word, w.end))
    want = _words(text)
    got, ends = [], []
    for raw, end in heard_words:
        for w in _words(raw):
            got.append(w)
            ends.append(end)
    sm = difflib.SequenceMatcher(a=want, b=got, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size]
    matched = sum(b.size for b in blocks)
    cut = None
    kept = len(got)
    if blocks:
        last = blocks[-1].b + blocks[-1].size  # words after this are extra tail
        if last < len(got):
            cut = ends[last - 1] + 0.18
            kept = last
    score = matched / max(len(want), kept, 1)
    heard = " ".join(r for r, _ in heard_words)
    return score, heard, cut




def voice_episode(ep_path, force=False, bank=None, fix=False):
    ep_path = Path(ep_path)
    dizi = ep_path.parent.parent.name
    ep = json.loads(ep_path.read_text(encoding="utf-8"))
    bank = bank or reference_bank(dizi)
    d = ROOT / "seslendirme" / dizi / ep_path.stem
    d.mkdir(parents=True, exist_ok=True)
    rnd = random.Random(ep["episode"])
    for si, li, ln in spoken_lines(ep):
        out = d / clip_name(si, li)
        marker = d / f"{clip_name(si, li)}.xtts"
        if out.exists() and not force:
            if not (fix and marker.exists() and float(marker.read_text().split("\n")[0] or 0) < 0.9):
                continue
        text = ln.get("say", ln["text"])
        best = None
        for attempt in range(5):  # regenerate with other references if Whisper disagrees
            refs = pick_refs(bank, ln["who"], ln.get("mood", "neutral"), dizi, rnd)
            tmp = d / f".try{attempt}.wav"
            synth(text, refs, tmp)
            score, heard, cut = check(tmp, text)
            if best is None or score > best[0]:
                best = (score, tmp, refs, heard, cut)
            if score >= 0.9:
                break
        score, tmp, refs, heard, cut = best
        if cut:  # drop XTTS tail babble after the last scripted word
            subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-i", str(tmp), "-t", f"{cut:.2f}",
                            "-af", "afade=t=out:st=%.2f:d=0.12" % max(0, cut - 0.12), str(out)], check=True)
        else:
            tmp.replace(out)
        for f in d.glob(".try*.wav"):
            f.unlink()
        marker.write_text("\n".join([f"{score:.3f}"] + refs))  # cloned clip: score + references
        flag = "  " if score >= 0.9 else "!!"
        print(f"{flag} {ep_path.stem}/{out.name} {ln['who']:8} {dur(out):4.1f}s {score:.2f} | {heard}", flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    fix = "--fix" in sys.argv  # only redo cloned lines that scored below 0.9
    bank = None
    for a in args:
        bank = bank or reference_bank(Path(a).parent.parent.name)
        voice_episode(a, force, bank, fix)
