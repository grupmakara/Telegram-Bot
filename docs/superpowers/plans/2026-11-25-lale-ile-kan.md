# Lale ile Kan — Üretim Hattı Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Episode YAML → one command → 1080×1920 MP4 (voiced, subtitled, animated SVG puppets) + cover PNG + caption text.

**Architecture:** `video/` is a standalone Node project. A Python helper synthesizes each line with edge-tts (word timings cached on disk). A pure TS function turns episode + audio metadata into a frame-accurate timeline. Remotion renders the timeline with React/SVG puppet and background components using the pre-installed Chromium.

**Tech Stack:** Node 22, TypeScript, Remotion 4, zod, yaml, vitest; Python 3 + edge-tts; ffmpeg/ffprobe; @fontsource fonts (local, no network).

**Spec:** `docs/superpowers/specs/2026-11-25-lale-ile-kan-design.md`

## Global Constraints

- Output: 1080×1920, 30 fps, H.264 MP4; episode length target 60–90 s (warn outside, do not fail).
- Voices: only `tr-TR-AhmetNeural`, `tr-TR-EmelNeural`; characters differ by pitch/rate.
- edge-tts must run with `--proxy $HTTPS_PROXY` semantics (`proxy=` arg) and `SSL_CERT_FILE=/root/.ccr/ca-bundle.crt`.
- Chromium: `browserExecutable: '/opt/pw-browsers/chromium'` (do not download Chrome).
- No music in the video. No copying reference series' names/characters/looks.
- Turkish text everywhere: upper-casing uses `toLocaleUpperCase('tr-TR')`; fonts must cover latin-ext (ı İ ğ ş ç ö ü).
- `video/out/` and `video/cache/` are gitignored; story files and code are committed.
- The existing bot files (`index.js`, `plugin/`, `handlers/`, root `package.json`) are not touched.

## Review Focus

1. Turkish glyphs/casing (`i→İ`, `ı→I`) in band, subtitles, cover — test in Task 2/6.
2. Long lines (>60 chars) must wrap within 960 px and never overflow — test in Task 6.
3. Unknown character/location id or missing field in YAML → error naming the file and path — test in Task 2.
4. TTS network failure → retried 3×, then a clear error; already-cached lines are not re-synthesized — test in Task 3.
5. Same text spoken by two characters must not share a cache entry (key includes voice/pitch/rate) — test in Task 3.

---

### Task 1: Scaffold + render smoke test

**Files:** Create `video/package.json`, `video/tsconfig.json`, `video/remotion.config.ts`, `video/src/index.ts`, `video/src/Root.tsx`, `video/.gitignore`, `video/scripts/smoke.sh`

**Produces:** `npm run render -- <compId> <out>` working; `registerRoot` in `src/index.ts`.

- [ ] Install `remotion @remotion/cli @remotion/renderer react react-dom zod yaml typescript tsx vitest @fontsource/cinzel @fontsource/nunito`.
- [ ] `Root.tsx` registers composition `Smoke` (1080×1920, 30 fps, 60 frames, solid bg + "LALE İLE KAN" text).
- [ ] `remotion.config.ts`: `Config.setBrowserExecutable('/opt/pw-browsers/chromium')`, `Config.setChromiumOpenGlRenderer('swangle')`.
- [ ] Run `bash scripts/smoke.sh` → renders `out/smoke.mp4`; `ffprobe` shows `1080x1920`, 2.0 s. Expected: PASS.
- [ ] Commit.

### Task 2: Episode schema + loader

**Files:** Create `video/src/story/schema.ts`, `video/src/story/load.ts`, `video/src/story/registry.ts`; Test `video/test/schema.test.ts`

**Produces:**
- `type Episode = { bolum: number; baslik: string; kanca: Line; sahneler: Scene[]; son: Line; aciklama: string; etiketler: string[] }`
- `type Line = { kim: string; metin: string; ifade?: Ifade; poz?: Poz }` (kanca/son use `kim`, not `karakter`)
- `type Scene = { mekan: MekanId; gecmis?: boolean; gece?: boolean; karakterler: { id: CharId; x: number; ifade?: Ifade; yon?: 'sol'|'sag' }[]; satirlar: Line[] }`
- `Ifade = 'normal'|'ofkeli'|'uzgun'|'saskin'|'gulumseyen'|'sinsi'`; `Poz = 'durus'|'isaret'|'kol_kaldir'|'el_gogus'`
- `CHAR_IDS = ['emir','murad','bekir','nilufer','saffet','lutfi','hizir','zeynep','yusuf']` (+ `'anlatici'` valid only as `kim`); `murad` = Emir in merchant costume.
- `MEKAN_IDS = ['divan','konak_salon','lale_bahcesi','halic_liman','carsi','zindan','idam_meydani']`
- `loadEpisode(path: string): Episode` — throws `Error` whose message includes the file path and the zod issue path.
- `trUpper(s: string): string`

- [ ] Tests: valid ep parses; `kim: 'ahmet'` throws message containing `sahneler.0.satirlar.0.kim` and file name; a line spoken by a char not in scene's `karakterler` (and not anlatici) throws; `trUpper('lale ile kan')==='LALE İLE KAN'`, `trUpper('ışık')==='IŞIK'`.
- [ ] Run vitest → FAIL; implement; → PASS. Commit.

### Task 3: TTS stage

**Files:** Create `video/tts/synth.py`, `video/src/audio/voices.ts`, `video/src/audio/synth.ts`; Test `video/test/voices.test.ts`, `video/tts/test_synth.py`

**Produces:**
- `VOICES: Record<CharId|'anlatici', { voice: string; pitch: string; rate: string }>` — emir `Ahmet,+0Hz,+0%`; murad same as emir; bekir `Ahmet,-15Hz,-10%`; saffet `Ahmet,-8Hz,+5%`; lutfi `Ahmet,-5Hz,-15%`; hizir `Ahmet,-10Hz,-12%`; yusuf `Ahmet,-12Hz,-8%`; nilufer `Emel,+0Hz,+0%`; zeynep `Emel,+10Hz,+8%`; anlatici `Ahmet,-4Hz,-5%`.
- `synth.py <job.json>`: job `{items:[{key,text,voice,pitch,rate}], outDir}` → for each missing `outDir/<key>.mp3` writes mp3 + `<key>.json` `{durationMs, words:[{text,startMs,endMs}]}` using `edge_tts.Communicate(..., boundary='WordBoundary', proxy=os.environ.get('HTTPS_PROXY'))`; 3 retries with 2 s backoff; exit 1 with the failing text on final failure. Duration via ffprobe.
- `synthEpisode(ep: Episode, cacheDir: string): Promise<Map<Line, AudioMeta>>`, `AudioMeta = { file: string; durationMs: number; words: Word[] }`; `cacheKey(text, voiceCfg): string` = sha1 of `voice|pitch|rate|text`.

- [ ] Tests: every CHAR_ID + anlatici has a voice; `cacheKey` differs for same text with emir vs bekir; python test: existing key file is skipped (mock Communicate not called); failing Communicate 3× → exit 1.
- [ ] FAIL → implement → PASS. Real run on one line produces mp3 + json with ≥1 word. Commit.

### Task 4: Timeline

**Files:** Create `video/src/timeline/build.ts`; Test `video/test/timeline.test.ts`

**Produces:** `buildTimeline(ep: Episode, audio: Map<Line, AudioMeta>, fps=30): Timeline`
- `Timeline = { durationInFrames: number; segments: Segment[] }`, `Segment = { kind: 'kanca'|'sahne'|'son'|'devam'; from: number; dur: number; sceneIndex?: number; lines: TimedLine[] }`, `TimedLine = { line: Line; from: number; dur: number; audio: AudioMeta }` (frames, absolute).
- Rules: kanca first (its audio + 15 frame tail); title flash 30 frames; scenes back-to-back with 8-frame gaps between lines and 12-frame fade between scenes; `son` line then `devam` card 60 frames.

- [ ] Tests: total frames = sum of rules for a 2-scene fixture (compute expected explicitly); lines never overlap; every `from` is integer.
- [ ] FAIL → implement → PASS. Commit.

### Task 5: Puppets + character sheet

**Files:** Create `video/src/puppet/Puppet.tsx`, `video/src/puppet/parts.tsx`, `video/src/puppet/characters.ts`, `video/src/comps/CharacterSheet.tsx`

**Produces:** `<Puppet id: CharId; ifade: Ifade; poz: Poz; yon: 'sol'|'sag'; mouthOpen: number /*0..1*/; frame: number; height: number />` drawn in a 400×1000 viewBox, feet at bottom; auto blink every ~3.5 s (deterministic from id), subtle breathing sway. `CHARACTERS: Record<CharId, Look>` encoding the spec's look table (colors, beard, headwear, scar, eyepatch, glasses, tear for `uzgun`).
- [ ] Register `CharacterSheet` still (1080×1920, all 9 looks in a grid, name labels).
- [ ] `npx remotion still CharacterSheet out/karakterler.png` renders; visual check against spec table. Commit. **Checkpoint: show to user.**

### Task 6: Backgrounds, band, subtitles

**Files:** Create `video/src/scene/Backgrounds.tsx`, `video/src/scene/TopBand.tsx`, `video/src/scene/Subtitle.tsx`, `video/src/scene/fonts.ts`; Test `video/test/subtitle.test.ts`

**Produces:** `<Background mekan gecmis gece />` (sepia filter when `gecmis`, dark-blue overlay when `gece`); `<TopBand bolum />` ("LALE İLE KAN" Cinzel + "N. BÖLÜM"); `<Subtitle words currentMs speaker />` Nunito 800, 64 px, white + 8 px black stroke, current word `#FFD54A`, speaker name chip; `wrapWords(words: string[], maxChars=24): string[][]` (max 2 rows visible, paging).
- [ ] Tests: `wrapWords` on 70-char sentence → no row > 24 chars unless a single word is longer; page splitting keeps word order.
- [ ] FAIL → implement → PASS. Commit.

### Task 7: Episode composition + sample clip

**Files:** Create `video/src/comps/Episode.tsx`, `video/src/comps/Hook.tsx`, `video/src/comps/EndCard.tsx`; Modify `video/src/Root.tsx`

**Consumes:** Timeline (Task 4), Puppet (5), scene parts (6).
**Produces:** composition `Episode` with `inputProps: { timeline: Timeline; episode: Episode }`, `calculateMetadata` sets duration from timeline. Mouth open = 1 while inside a word window of the current line ±40 ms jitter-free alternation (open/half every 4 frames). Camera: slow zoom 1.0→1.06 per scene; speaker gets 1.15 zoom centered on their x for lines >2.5 s. `<Audio>` per TimedLine. Hook segment: speaker close-up + quote in cream band. EndCard: "Devamı N+1. Bölümde".
- [ ] Render 10 s sample from a 3-line fixture → `out/deneme.mp4`; check sound sync and subtitles by eye. **Checkpoint: show to user with character sheet.** Commit.

### Task 8: CLI

**Files:** Create `video/scripts/bolum.ts`; Modify `video/package.json` (`"bolum": "tsx scripts/bolum.ts"`)

**Produces:** `npm run bolum -- <N>` → loads `story/episodes/epNN.yaml`, synthesizes, builds timeline, renders `out/epNN.mp4`, still of frame 10 → `out/epNN_kapak.png`, writes `out/epNN_aciklama.txt` (aciklama + blank line + etiketler joined by space). Prints duration and warns outside 60–90 s.
- [ ] Run on fixture episode → three files exist. Commit.

### Task 9: Story files

**Files:** Create `video/story/season1.md` (30-episode arc, eps 1–10 detailed), `video/story/ozet.md`, `video/story/episodes/ep01.yaml`, `ep02.yaml`, `ep03.yaml`

- [ ] Each episode: hook ≠ ending line, 3–5 scenes, 8–14 lines, ends on unanswered question; ep01 ends with Emir recognizing Zeynep in Bekir's konak.
- [ ] `loadEpisode` passes for all three. Commit. Show scripts to user before rendering.

### Task 10: Render episodes 1–3 and deliver

- [ ] `npm run bolum -- 1..3`; ffprobe each (1080×1920, 60–90 s); send mp4/png/txt to user; update `ozet.md`; commit and push.
