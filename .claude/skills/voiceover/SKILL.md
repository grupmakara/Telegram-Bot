---
name: voiceover
description: Voice the animated Shorts series in cizgi_dizi/ with commercial-safe open-source TTS (Chatterbox Multilingual, MIT). Use when the user asks to voice, re-voice, dub or fix the voices of episodes ("seslendir", "seslendirme", "sesleri yenile", "bölümleri seslendir", "ses kesiliyor"), to give a new character a voice, or when a rendered episode still uses an older engine.
---

# Voice-over for the animated series (cizgi_dizi)

Episodes are JSON scripts in `cizgi_dizi/diziler/<dizi>/bolumler/bolumNN.json`. Every spoken line
becomes one clip; `engine/render.py` picks clips up automatically, preferring
`seslendirme/<dizi>/cb/` (Chatterbox) → `vox/` (VoxCPM2, old) → `bolumNN/` (ElevenLabs, eps 1-6)
→ edge-tts (drafts only). Work from `cizgi_dizi/`. Talk to the user in Turkish.

## Ground rules

- **Commercial-safe only.** The channel may be monetized. Use Chatterbox Multilingual (MIT,
  Turkish supported) for speech and VoxCPM2 (Apache-2.0) only to *design* new character voices.
  Do not use XTTS-v2 (non-commercial), F5-TTS Turkish (CC-BY-NC), OmniVoice, Fish/Drama, or
  Breeze-TTS (licence unclear). Never clone a real person's voice, including ElevenLabs library
  voices or videos the user sends from other channels. ElevenLabs free tier has no commercial
  rights (paid Starter/Creator does).
- **One voice per character for the whole series.** Reference voices live in
  `diziler/<dizi>/sesler/<character>.wav`. Changing one changes the character mid-season: only
  when the user asks (keep the old file as `<character>_<note>.wav`).
- **Never trust a clip you have not checked.** Lines are checked with Whisper (`check` in
  `engine/clone.py`) plus `judge` in `engine/cb.py`, which also penalises made-up words after the
  line ("tail babble") and a missing first word.

## Setup (once per machine)

Chatterbox lives in its own venv so it does not break the VoxCPM2 install:
```bash
python3 -m venv /root/cb
/root/cb/bin/pip install --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple torch torchaudio
/root/cb/bin/pip install chatterbox-tts faster-whisper "setuptools<81"   # setuptools: watermarker needs pkg_resources
```
`engine/cb.py` loads the newer `t3_mtl23ls_v3` text model with the v2 decoder (`s3gen.pt`;
`s3gen_v3.pt` does not load in chatterbox-tts 0.1.7). Run with `HF_HUB_OFFLINE=1` once weights
are cached.

## Pipeline

1. **New character?** Design a voice with VoxCPM2 (`VOICE_DESIGN` in `engine/vox.py`, then
   `HF_HUB_DISABLE_XET=1 python3 engine/vox.py design diziler/<dizi>`), listen/measure pitch
   (librosa `pyin`), add to `cast.json`.
2. **Voice episodes** (skips existing clips, resumable):
   ```bash
   HF_HUB_OFFLINE=1 /root/cb/bin/python engine/cb.py voice diziler/<dizi>/bolumler/bolumNN.json [...] [--fix|--force]
   ```
   Clips: `seslendirme/<dizi>/cb/bolumNN/s<scene>_l<line>.wav` + `.txt` (score, what Whisper
   heard). Emotion = `EXAGGERATION` per mood. ~15–25 s per line on CPU.
3. **Review** each episode: list clips scoring < 0.85 and compare script vs heard text. Many low
   scores are Whisper only (numbers written as digits "99", merged words "Yatarık", suffix
   spelling "Zeynep ile"). Real problems: a wrong word ("çökün"→"çekin"), missing first word,
   babble after the line. Regenerate only those (up to 4 tries, keep the new clip only if its
   judged score is higher), then re-render.
4. **Render** and check: `python3 engine/render.py diziler/<dizi>/bolumler/bolumNN.json`
   (system python, not the venv); loudness ~-14/-15 LUFS.
5. `python3 engine/hazir_liste.py` updates `HAZIR_VIDEOLAR.md`; commit and push clips + videos.

## Writing lines that voice well

- Numbers must be spelled out in `say` (`"text": "1999"`, `"say": "bin dokuz yüz doksan dokuz"`),
  recaps included. Scan for digits before voicing.
- Very short fragments ("Gece üçte lobide bir matkap sesi...") come out garbled; write full
  sentences.
- A word at the very start followed by `...` can be dropped; if retries fail, rephrase
  (e.g. `Anne...` → `Anneciğim...`) in both `text` and `say`.

## Running long jobs

- Run one detached worker that loops over episodes, voices, then renders only if the video is
  older than its clips: `setsid nohup /root/cb/bin/python -u worker.py > log 2>&1 < /dev/null & disown`.
- **Never delete `.try*.wav` / `.fix*.wav` while a worker runs**: they are its in-progress takes
  (it crashed once). They are git-ignored; just commit around them.
- Commit a video only after its render finished (a half-written mp4 is otherwise pushed).
- After a container restart, start the worker again; finished clips are skipped.

## Troubleshooting

- `CERTIFICATE_VERIFY_FAILED`: point the tool at `/root/.ccr/ca-bundle.crt`.
- `PerthImplicitWatermarker` is `None`: install `setuptools<81` in the venv.
- Hugging Face downloads stall on xet: set `HF_HUB_DISABLE_XET=1`.
- Relative reference paths fail when the worker runs from another directory: use absolute paths.
