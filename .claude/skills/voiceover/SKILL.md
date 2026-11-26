---
name: voiceover
description: Voice the animated Shorts series in cizgi_dizi/ with commercial-safe open-source TTS (VoxCPM2, Apache-2.0). Use when the user asks to voice, re-voice, dub or fix the voices of episodes ("seslendir", "seslendirme", "sesleri yenile", "bölümleri seslendir"), to give a new character a voice, or when a rendered episode still uses the flat edge-tts fallback.
---

# Voice-over for the animated series (cizgi_dizi)

Episodes are JSON scripts in `cizgi_dizi/diziler/<dizi>/bolumler/bolumNN.json`. Every spoken line
becomes one clip; `engine/render.py` picks clips up automatically. Work from `cizgi_dizi/`.

## Ground rules

- **Commercial-safe only.** The channel may be monetized. Use VoxCPM2 (Apache-2.0) with *designed*
  voices. Do not use XTTS-v2 (Coqui licence is non-commercial), OmniVoice or Fish/Drama weights
  (non-commercial), and never clone a real person's voice, including ElevenLabs library voices.
  ElevenLabs free-tier audio is not licensed for commercial use either.
- **One voice per character for the whole series.** Designed voices live in
  `diziler/<dizi>/sesler/<character>.wav` (+ `.txt` transcript). Never regenerate an existing one:
  that changes the character's voice mid-season.
- **Never trust a clip you have not checked.** Every line is verified with Whisper (`check` in
  `engine/clone.py`): word-level match, Turkish number words, tail babble cut off.

## Pipeline

1. **New character?** Add a description to `VOICE_DESIGN` in `engine/vox.py` (age, gender, timbre,
   attitude, in English), add the character to `diziler/<dizi>/cast.json`, then:
   ```bash
   HF_HUB_DISABLE_XET=1 python3 engine/vox.py design diziler/<dizi>
   ```
   Only missing voices are designed. Check the printed score (should be ~1.00).
2. **Voice episodes** (skips lines that already have a clip, so it is resumable):
   ```bash
   HF_HUB_DISABLE_XET=1 python3 engine/vox.py voice diziler/<dizi>/bolumler/bolumNN.json [...]
   ```
   - `--fix` regenerates only lines that scored below 0.8; `--force` regenerates everything.
   - Clips: `seslendirme/<dizi>/vox/bolumNN/s<scene>_l<line>.wav`, score + what Whisper heard in
     `<clip>.txt`. Recap lines use scene key `r` (`sr_l0.wav`).
   - Emotion comes from the line's `mood` (`MOOD_CUE` in `vox.py`, an English cue in parentheses,
     which VoxCPM2 does not read aloud in reference-cloning mode). Numbers must be written out in
     the line's `say` field (`"text": "1979"`, `"say": "bin dokuz yüz yetmiş dokuz"`).
3. **Render** the episodes, then sample frames and check loudness (~-14 LUFS):
   ```bash
   python3 engine/render.py diziler/<dizi>/bolumler/bolumNN.json
   ffmpeg -i cikti/<dizi>/bolumNN.mp4 -af ebur128 -f null - 2>&1 | grep " I:"
   ```
4. **Commit and push** clips (`seslendirme/*/vox/` and `sesler/*.wav` are un-ignored in
   `cizgi_dizi/.gitignore`) together with the rendered videos.

## Running long jobs

VoxCPM2 runs on CPU at roughly 45–60 s per line; a whole season takes hours.
- Run it detached so it outlives tool timeouts and can be resumed after a restart:
  `setsid nohup python3 -u -I worker.py > log 2>&1 < /dev/null & disown`
- Run **one** worker (all 4 threads) that loops over the episodes. Two workers do not fit: loading
  the model peaks at ~7 GB RSS each and the cgroup OOM-kills the second one. Model load takes
  ~3 minutes.
- After a session restart, check `pgrep -fa vox` and simply start the workers again; finished
  clips are skipped.
- Watch progress by counting `seslendirme/<dizi>/vox/*/*.wav`; look for `!!` lines (score < 0.8)
  in the logs and rerun those episodes with `--fix`.

## Troubleshooting

- `CERTIFICATE_VERIFY_FAILED` from a Python tool: point it at `/root/.ccr/ca-bundle.crt`.
- Hugging Face downloads fail on `cas-server.xethub.hf.co`: set `HF_HUB_DISABLE_XET=1`.
- Whisper often mishears correct speech (split suffixes like `Zeynep 'in`, `gıcır diyor`); a score
  of 0.8+ is fine. Read the heard text in `<clip>.txt` before regenerating.
- A line that keeps failing: simplify punctuation, spell out numbers/abbreviations in `say`
  (e.g. `R. Karaca` → `Re Karaca`), then `--fix`.
- Without VoxCPM2 clips, `render.py` falls back to ElevenLabs clips in
  `seslendirme/<dizi>/bolumNN/`, then to edge-tts (flat; drafts only).
