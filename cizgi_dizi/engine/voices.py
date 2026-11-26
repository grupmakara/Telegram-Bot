"""Expressive voice-over via ElevenLabs (eleven_v4 audio tags), per character.

Workflow
  1. python3 engine/voices.py prompts <bolum.json>
       -> prints one prompt per character (all their lines, with emotion tags).
  2. Generate each prompt with that character's ElevenLabs voice and save it as
       seslendirme/<dizi>/takes/<who>__<bolumNN>[+<bolumMM>...].mp3
       (one take may hold a character's lines from several episodes, in order)
  3. python3 engine/voices.py split seslendirme/<dizi>/takes/*.mp3
       -> aligns each take with Whisper and cuts it into per-line files
          seslendirme/<dizi>/<bolumNN>/s<scene>_l<line>.wav, which render.py uses
          instead of the edge-tts fallback.
"""
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR = 48000

MOOD_TAG = {
    "angry": "[angrily]", "smug": "[sarcastically]", "surprised": "[shocked]",
    "sad": "[sadly]", "worried": "[nervously]", "smile": "[warmly]", "neutral": "[calmly]",
}


def take_dir(ep_path):
    ep_path = Path(ep_path)
    return ROOT / "seslendirme" / ep_path.parent.parent.name / ep_path.stem


def spoken_lines(ep):
    for si, sc in enumerate(ep["scenes"]):
        for li, ln in enumerate(sc["lines"]):
            if ln.get("who") and ln.get("text"):
                yield si, li, ln


def tagged(ln):
    tag = ln.get("tag") or MOOD_TAG.get(ln.get("mood", "neutral"), "")
    if ln.get("who") == "anlatici" and not ln.get("tag"):
        tag = "[mysteriously]"
    return f"{tag} {ln['text']}".strip()


def prompts(ep):
    by = {}
    for si, li, ln in spoken_lines(ep):
        by.setdefault(ln["who"], []).append(tagged(ln))
    return {who: "\n\n".join(lines) for who, lines in by.items()}


# --------------------------------------------------------------- split ----
def norm(w):
    w = w.replace("I", "ı").replace("İ", "i").lower()
    w = unicodedata.normalize("NFKD", w)
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9ı]", "", w)


def decode(path, sr):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(path), "-ac", "1", "-ar", str(sr),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def split_take(take, model):
    """take file name: <who>__<bolumA>+<bolumB>.mp3 inside seslendirme/<dizi>/takes/."""
    take = Path(take)
    who, eps = take.stem.split("__")
    dizi = take.parent.parent.name
    items = []  # (out_path, text)
    for stem in eps.split("+"):
        ep_path = ROOT / "diziler" / dizi / "bolumler" / f"{stem}.json"
        ep = json.loads(ep_path.read_text(encoding="utf-8"))
        d = take_dir(ep_path)
        d.mkdir(parents=True, exist_ok=True)
        for si, li, ln in spoken_lines(ep):
            if ln["who"] == who:
                items.append((d / f"s{si}_l{li}.wav", ln["text"]))
    audio = decode(take, SR)
    a16 = decode(take, 16000)
    segs, _ = model.transcribe(a16, language="tr", word_timestamps=True)
    words = [(norm(w.word), w.start, w.end) for s in segs for w in s.words if norm(w.word)]
    script = []
    for k, (_, text) in enumerate(items):
        script += [(norm(t), k) for t in text.split() if norm(t)]
    sm = difflib.SequenceMatcher(a=[t for t, _ in script], b=[w for w, _, _ in words], autojunk=False)
    first, last = {}, {}
    for blk in sm.get_matching_blocks():
        for j in range(blk.size):
            k = script[blk.a + j][1]
            first.setdefault(k, blk.b + j)
            last[k] = blk.b + j
    n, total = len(items), len(audio) / SR
    bounds = [0.0]
    for k in range(n - 1):
        if k in last and (k + 1) in first and first[k + 1] > last[k]:
            # lines are separated by a pause: cut in the longest silence between
            # the last recognised word of this line and the first of the next.
            # (Words Whisper hears differently, e.g. "imza alıyorum", may sit on
            # either side of the matched ones, so the longest gap is the safe cut.)
            lo, hi = last[k], first[k + 1]
            gi = max(range(lo, hi), key=lambda i: words[i + 1][1] - words[i][2])
            cut = (words[gi][2] + words[gi + 1][1]) / 2
        else:
            cut = total * (k + 1) / n
            print(f"  UYARI: {take.name} replik {k + 1}/{k + 2} sınırı tahmini")
        bounds.append(max(cut, bounds[-1] + 0.2))
    bounds.append(total)
    print(f"{take.name}: {n} replik, eşleşme %{100 * sm.ratio():.0f}")
    for k, (out, text) in enumerate(items):
        seg = audio[int(bounds[k] * SR): int(bounds[k + 1] * SR)]
        idx = np.where(np.abs(seg) > 0.012)[0]
        if len(idx):
            seg = seg[max(0, idx[0] - 1200): idx[-1] + 3600]
        subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1",
                        "-i", "-", str(out)], input=seg.astype(np.float32).tobytes(), check=True)
        print(f"  {out.parent.name}/{out.name}: {len(seg) / SR:4.1f}s  {text[:60]}")


def split(takes):
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    for t in takes:
        split_take(t, model)


if __name__ == "__main__":
    cmd, ep_path = sys.argv[1], sys.argv[2]
    if cmd == "prompts":
        ep = json.loads(Path(ep_path).read_text(encoding="utf-8"))
        take_dir(ep_path).mkdir(parents=True, exist_ok=True)
        print(json.dumps(prompts(ep), ensure_ascii=False, indent=1))
    elif cmd == "split":
        split(sys.argv[2:])
