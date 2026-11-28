"""Commercial-safe voice-over with Chatterbox Multilingual (Resemble AI, MIT licence).

Each character speaks with its own designed voice (diziler/<dizi>/sesler/<character>.wav, made
with VoxCPM2 voice design, no real person cloned). Chatterbox clones that reference clip and
reads the line in Turkish; emotion strength comes from the line's mood. Every clip is checked
with Whisper and regenerated (up to 3 tries) if it does not match the script.

Runs in its own virtualenv (/root/cb) so it does not disturb the VoxCPM2 install:

  /root/cb/bin/python engine/cb.py voice diziler/<dizi>/bolumler/bolumNN.json [...] [--force|--fix]

Clips go to seslendirme/<dizi>/cb/<bolumNN>/s<scene>_l<line>.wav (+ .txt with score and what
Whisper heard); render.py prefers them over VoxCPM2 and ElevenLabs clips.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from clone import check  # noqa: E402  (Whisper word-level check)
from voices import clip_name, spoken_lines  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = Path("/root/.cache/huggingface/hub/models--ResembleAI--chatterbox/snapshots")
# Emotion strength per mood (Chatterbox "exaggeration"; 0.5 is neutral). Higher values also
# speed speech up, so cfg_weight is lowered a little for them.
EXAGGERATION = {"angry": 0.8, "surprised": 0.75, "smug": 0.7, "worried": 0.65, "sad": 0.6,
                "smile": 0.55, "neutral": 0.5}
NARRATOR_EXAGGERATION = 0.6
ACCEPT = 0.9

_model = None


def model():
    """Chatterbox Multilingual with the newer v3 text model (t3_mtl23ls_v3) and the v2 decoder."""
    global _model
    if _model is None:
        import torch
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        torch.set_num_threads(os.cpu_count() or 4)
        snap = sorted(SNAPSHOT.iterdir())[-1]
        ckpt = ROOT / ".cache" / "chatterbox_v3"
        ckpt.mkdir(parents=True, exist_ok=True)
        links = {f: f for f in ["ve.pt", "grapheme_mtl_merged_expanded_v1.json", "conds.pt",
                                "Cangjie5_TC.json", "s3gen.pt"]}
        links["t3_mtl23ls_v2.safetensors"] = "t3_mtl23ls_v3.safetensors"
        for dst, src in links.items():
            if not (ckpt / dst).exists() and (snap / src).exists():
                os.symlink(snap / src, ckpt / dst)
        _model = ChatterboxMultilingualTTS.from_local(ckpt, "cpu")
    return _model


def save(wav, out):
    """Write 48 kHz mono with a short lead-in and trailing silence trimmed to 0.15 s."""
    a = np.asarray(wav.squeeze().cpu().numpy() if hasattr(wav, "cpu") else wav, dtype=np.float32)
    sr = model().sr
    loud = np.where(np.abs(a) > 0.02 * (np.abs(a).max() + 1e-9))[0]
    if len(loud):
        a = a[: min(len(a), loud[-1] + int(0.15 * sr))]
    a = np.concatenate([np.zeros(int(sr * 0.12), np.float32), a])
    subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-",
                    "-ar", "48000", str(out)], input=a.tobytes(), check=True)


def voice_episode(ep_path, force=False, fix=False):
    ep_path = Path(ep_path)
    dizi = ep_path.parent.parent.name
    ep = json.loads(ep_path.read_text(encoding="utf-8"))
    out_dir = ROOT / "seslendirme" / dizi / "cb" / ep_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    for si, li, ln in spoken_lines(ep):
        out = out_dir / clip_name(si, li)
        meta = out_dir / f"{clip_name(si, li)}.txt"
        if out.exists() and not force:
            if not (fix and meta.exists() and float(meta.read_text().split()[0]) < ACCEPT):
                continue
        ref = ROOT / "diziler" / dizi / "sesler" / f"{ln['who']}.wav"
        text = ln.get("say", ln["text"])
        ex = NARRATOR_EXAGGERATION if ln["who"] == "anlatici" else EXAGGERATION.get(ln.get("mood", "neutral"), 0.5)
        cfg = 0.4 if ex >= 0.7 else 0.5
        best = None
        for attempt in range(3):
            tmp = out_dir / f".try{attempt}.wav"
            save(model().generate(text, language_id="tr", audio_prompt_path=str(ref), exaggeration=ex,
                                  cfg_weight=cfg), tmp)
            score, heard, _ = check(tmp, text)
            if best is None or score > best[0]:
                best = (score, tmp, heard)
            if score >= ACCEPT:
                break
        score, tmp, heard = best
        tmp.replace(out)
        for f in out_dir.glob(".try*.wav"):
            f.unlink()
        meta.write_text(f"{score:.3f} {heard}\n")
        flag = "  " if score >= ACCEPT else "!!"
        print(f"{flag} {ep_path.stem}/{out.name} {ln['who']:8} {score:.2f} | {heard}", flush=True)


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:]
    paths = [a for a in rest if not a.startswith("--")]
    if cmd == "voice":
        for p in paths:
            voice_episode(p, "--force" in rest, "--fix" in rest)
