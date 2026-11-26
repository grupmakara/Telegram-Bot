"""Render one episode JSON into a 1080x1920 Shorts video.

Usage: python3 engine/render.py diziler/<dizi>/bolumler/bolum01.json [--preview]
"""
import argparse
import asyncio
import hashlib
import json
import math
import random
import ssl
import subprocess
import sys
import wave
from pathlib import Path

import cairo
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from rig import draw_character, hexc, rrect  # noqa: E402
from sets import FONT, PROPS, W, H, make_background  # noqa: E402

FPS = 30
SR = 48000
ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "tts"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


# ------------------------------------------------------------------ TTS ----
async def _tts(text, voice, out):
    import edge_tts
    import edge_tts.communicate as comm
    if Path(CA_BUNDLE).exists():
        comm._SSL_CTX = ssl.create_default_context(cafile=CA_BUNDLE)
    await edge_tts.Communicate(text, voice["id"], rate=voice.get("rate", "+0%"),
                               pitch=voice.get("pitch", "+0Hz")).save(str(out))


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(path), "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def speak(text, voice):
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(json.dumps([text, voice], sort_keys=True).encode()).hexdigest()[:16]
    out = CACHE / f"{key}.mp3"
    if not out.exists():
        for attempt in range(4):
            try:
                asyncio.run(_tts(text, voice, out))
                break
            except Exception:  # network hiccup: retry with backoff
                if attempt == 3:
                    raise
                import time
                time.sleep(2 ** attempt)
    a = decode(out)
    # trim leading/trailing near-silence
    idx = np.where(np.abs(a) > 0.01)[0]
    if len(idx):
        a = a[max(0, idx[0] - 800): idx[-1] + 2400]
    return a


# ---------------------------------------------------------------- audio ----
def synth_sfx(kind, dur=1.0):
    t = np.arange(int(SR * dur)) / SR
    rnd = np.random.default_rng(7)
    if kind == "thud":
        return (np.sin(2 * np.pi * 55 * t) * np.exp(-t * 6) * 0.9
                + rnd.normal(0, 0.3, len(t)) * np.exp(-t * 25))
    if kind == "sting":  # dramatic cliffhanger hit
        base = sum(np.sin(2 * np.pi * f * t) for f in (55, 110, 131, 165)) / 3
        return base * np.exp(-t * 1.6) * 0.8 + rnd.normal(0, 0.25, len(t)) * np.exp(-t * 18)
    if kind == "ding":
        return (np.sin(2 * np.pi * 1320 * t) + 0.5 * np.sin(2 * np.pi * 1980 * t)) * np.exp(-t * 4) * 0.35
    if kind == "phone":
        tone = np.sin(2 * np.pi * 880 * t) * 0.5 + np.sin(2 * np.pi * 1100 * t) * 0.3
        gate = ((t * 4) % 1 < 0.5).astype(float)
        return tone * gate * 0.3
    if kind == "alarm":
        f = 700 + 300 * np.sign(np.sin(2 * np.pi * 2 * t))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    if kind == "elevator":  # clunk + grinding stop
        g = rnd.normal(0, 0.2, len(t)) * np.exp(-t * 3) * (np.sin(2 * np.pi * 30 * t) > 0)
        return g + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 8) * 0.8
    if kind == "whoosh":
        n = rnd.normal(0, 1, len(t))
        env = np.sin(np.pi * t / dur) ** 2
        return np.convolve(n, np.ones(40) / 40, "same") * env * 0.5
    if kind == "door":
        return np.sin(2 * np.pi * 90 * t) * np.exp(-t * 14) + rnd.normal(0, 0.4, len(t)) * np.exp(-t * 40)
    return np.zeros_like(t)


def music_bed(total, seed=1):
    """Soft minor pad with a slow pulse; the channel-style tension bed."""
    t = np.arange(int(SR * total)) / SR
    chords = [(110, 130.8, 164.8), (87.3, 110, 130.8), (98, 123.5, 146.8), (82.4, 103.8, 123.5)]
    out = np.zeros_like(t)
    seg = 4.0
    for i in range(int(total / seg) + 1):
        a, b = int(i * seg * SR), int(min(total, (i + 1) * seg + 0.6) * SR)
        if a >= len(t):
            break
        tt = t[a:b] - t[a]
        env = np.minimum(1, tt / 1.2) * np.minimum(1, np.maximum(0, (seg + 0.6 - tt) / 0.8))
        sig = sum(np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)
                  for f in chords[i % len(chords)])
        out[a:b] += sig[: b - a] * env[: b - a]
    pulse = 0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t)
    out = out * pulse
    return out / (np.max(np.abs(out)) + 1e-9) * 0.07


def write_wav(path, mono):
    st = np.clip(np.stack([mono, mono], 1), -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


# ------------------------------------------------------------- timeline ----
def build_timeline(ep, cast, voice_dir):
    beats, t = [], 0.35
    for si, scene in enumerate(ep["scenes"]):
        for li, line in enumerate(scene["lines"]):
            b = dict(line, scene=si, index=li)
            if "who" in line:
                pre = voice_dir / f"s{si}_l{li}.wav"
                if pre.exists():  # expressive ElevenLabs take (engine/voices.py)
                    b["audio"] = decode(pre)
                else:
                    b["audio"] = speak(line["text"], cast[line["who"]]["voice"])
                dur = len(b["audio"]) / SR
            else:
                dur = line.get("dur", 1.2)
            b["start"], b["end"] = t, t + dur
            t += dur + line.get("pause", 0.28)
            beats.append(b)
        t += 0.25
    return beats, t


def envelope(audio):
    hop = SR // FPS
    n = len(audio) // hop + 1
    pad = np.pad(audio, (0, n * hop - len(audio)))
    rms = np.sqrt((pad.reshape(n, hop) ** 2).mean(1))
    rms = rms / (np.percentile(rms, 95) + 1e-6)
    # quantise to a few mouth shapes like cut-out animation
    return np.clip(np.round(rms * 3) / 3, 0, 1)


# --------------------------------------------------------------- drawing ----
def wrap(ctx, text, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if ctx.text_extents(test).x_advance > maxw and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def draw_subtitle(ctx, text, narrator=False, y=1520):
    ctx.select_font_face(FONT, 1 if narrator else 0, 1)
    size = 50
    ctx.set_font_size(size)
    lines = wrap(ctx, text, 900)
    lh = size * 1.28
    boxh = lh * len(lines) + 40
    maxw = max(ctx.text_extents(l).x_advance for l in lines)
    rrect(ctx, 540 - maxw / 2 - 32, y - boxh / 2, maxw + 64, boxh, 18)
    ctx.set_source_rgba(0, 0, 0, 0.78)
    ctx.fill()
    for i, l in enumerate(lines):
        e = ctx.text_extents(l)
        ctx.move_to(540 - e.x_advance / 2, y - boxh / 2 + 20 + lh * (i + 0.78))
        ctx.set_source_rgb(*((1, 0.86, 0.35) if narrator else (1, 1, 1)))
        ctx.show_text(l)


def draw_pill(ctx, text, y=150, size=38, bg="#f5c542", fg="#1a1a1a"):
    ctx.select_font_face(FONT, 0, 1)
    ctx.set_font_size(size)
    e = ctx.text_extents(text)
    w, h = e.x_advance + 60, size * 1.7
    rrect(ctx, 540 - w / 2, y - h / 2, w, h, h / 2)
    ctx.set_source_rgb(*hexc(bg))
    ctx.fill_preserve()
    ctx.set_source_rgb(0.1, 0.1, 0.1)
    ctx.set_line_width(4)
    ctx.stroke()
    ctx.move_to(540 - e.x_advance / 2, y + size * 0.36)
    ctx.set_source_rgb(*hexc(fg))
    ctx.show_text(text)


LAYOUT = {1: [(540, 1.05)], 2: [(285, 0.95), (795, 0.95)], 3: [(195, 0.8), (540, 0.84), (885, 0.8)],
          4: [(150, 0.66), (405, 0.66), (675, 0.66), (930, 0.66)]}


def plan_shot(beat, scene):
    cast = scene["cast"]
    if beat.get("shot"):
        return beat["shot"]
    if "who" not in beat or beat["who"] not in cast:
        return "wide"
    i = beat["index"]
    if i == 0 or len(cast) == 1 or i % 3 == 2:
        return "wide"
    return "close"


class Renderer:
    def __init__(self, ep, cast, beats, total):
        self.ep, self.cast, self.beats, self.total = ep, cast, beats, total
        self.bgs = {}
        self.moods = {}
        self.blinks = {c: sorted(random.Random(sum(map(ord, c))).uniform(0, total) for _ in range(int(total / 3.2)))
                       for c in cast}
        for b in beats:
            b["shot_kind"] = plan_shot(b, ep["scenes"][b["scene"]])
            if "audio" in b:
                b["env"] = envelope(b["audio"])

    def bg(self, name):
        if name not in self.bgs:
            self.bgs[name] = make_background(name)
        return self.bgs[name]

    def beat_at(self, t):
        cur = self.beats[0]
        for b in self.beats:
            if b["start"] <= t:
                cur = b
        return cur

    def blink(self, c, t):
        for bt in self.blinks.get(c, []):
            if 0 <= t - bt < 0.16:
                return 1.0
        return 0.0

    def mood_state(self, upto):
        moods = {}
        for b in self.beats:
            if b is upto:
                break
            if b.get("who"):
                moods[b["who"]] = b.get("mood", moods.get(b["who"], "neutral"))
            for k, v in b.get("react", {}).items():
                moods[k] = v
        if upto.get("who"):
            moods[upto["who"]] = upto.get("mood", "neutral")
        for k, v in upto.get("react", {}).items():
            moods[k] = v
        return moods

    def frame(self, ctx, t):
        b = self.beat_at(t)
        scene = self.ep["scenes"][b["scene"]]
        local = t - b["start"]
        moods = self.mood_state(b)
        shake = b.get("shake") and local < 0.6
        ctx.save()
        if shake:
            ctx.translate(math.sin(t * 90) * 14 * (1 - local / 0.6), math.cos(t * 70) * 10 * (1 - local / 0.6))
        z = 1.0 + 0.045 * min(1, local / max(0.5, b["end"] - b["start"] + 0.3))
        ctx.translate(540, 900)
        ctx.scale(z, z)
        ctx.translate(-540, -900)
        ctx.set_source_surface(self.bg(scene["bg"]), 0, 0)
        ctx.paint()

        speaker = b.get("who")
        castlist = scene["cast"]
        if b["shot_kind"] == "close" and speaker in castlist:
            placements = [(speaker, 540, 1.32, 2230)]
        elif isinstance(b["shot_kind"], str) and b["shot_kind"].startswith("two:"):
            pair = b["shot_kind"][4:].split(",")
            placements = [(c, x, s, 1920) for c, (x, s) in zip(pair, LAYOUT[2])]
        else:
            placements = [(c, x, s, 1920) for c, (x, s) in zip(castlist, LAYOUT[len(castlist)])]
        xs = {c: x for c, x, _, _ in placements}
        for c, x, s, base in placements:
            mouth = 0.0
            if c == speaker and "env" in b:
                fi = int(local * FPS)
                if 0 <= fi < len(b["env"]):
                    mouth = float(b["env"][fi])
            look = 0.0
            if speaker in xs and c != speaker:
                look = 1.0 if xs[speaker] > x else -1.0
            bob = math.sin(t * 2.2 + (sum(map(ord, c)) % 7)) * 4 + (mouth * -6)
            tilt = math.sin(t * 1.3 + (sum(map(ord, c)) % 5)) * 0.015
            draw_character(ctx, self.cast[c], x, base, s, mood=moods.get(c, "neutral"),
                           mouth_open=mouth, blink=self.blink(c, t), look=look, bob=bob, tilt=tilt)
        ctx.restore()

        if b.get("prop"):
            ctx.rectangle(0, 0, W, H)
            ctx.set_source_rgba(0, 0, 0, 0.35)
            ctx.fill()
            pop = min(1, local / 0.25)
            ctx.save()
            ctx.translate(540, 800)
            ctx.scale(0.6 + 0.4 * pop, 0.6 + 0.4 * pop)
            ctx.translate(-540, -800)
            PROPS[b["prop"]](ctx, t, b.get("prop_caption", ""))
            ctx.restore()

        draw_pill(ctx, f"{self.ep['series']} • {self.ep['episode']}. Bölüm", y=140, size=34)
        if b.get("caption"):
            draw_subtitle(ctx, b["caption"], narrator=True)
        elif b.get("text"):
            draw_subtitle(ctx, b["text"], narrator=(speaker == "anlatici"))

    def end_card(self, ctx, t):
        k = min(1, t / 0.4)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source_rgba(0.02, 0.02, 0.05, 0.72 * k)
        ctx.fill()
        nxt = self.ep.get("next_text", f"Devamı {self.ep['episode'] + 1}. Bölüm'de...")
        ctx.select_font_face(FONT, 0, 1)
        ctx.set_font_size(64)
        lines = wrap(ctx, nxt, 900)
        for i, l in enumerate(lines):
            e = ctx.text_extents(l)
            ctx.move_to(540 - e.x_advance / 2, 860 + i * 84)
            ctx.set_source_rgba(1, 1, 1, k)
            ctx.show_text(l)
        draw_pill(ctx, "Takip et, kaçırma!", y=1120, size=44, bg="#e23b3b", fg="#ffffff")


def render(ep_path, preview=False):
    ep_path = Path(ep_path)
    ep = json.loads(ep_path.read_text(encoding="utf-8"))
    cast = json.loads((ep_path.parent.parent / "cast.json").read_text(encoding="utf-8"))
    beats, story_end = build_timeline(ep, cast, ROOT / "seslendirme" / ep_path.parent.parent.name / ep_path.stem)
    end_len = 2.6
    total = story_end + end_len
    r = Renderer(ep, cast, beats, total)

    # ---- audio mix
    mix = np.zeros(int(SR * (total + 0.5)), dtype=np.float32)
    bed = music_bed(total)
    mix[: len(bed)] += bed
    for b in beats:
        a0 = int(b["start"] * SR)
        if "audio" in b:
            seg = b["audio"] * 0.95
            mix[a0: a0 + len(seg)] += seg[: len(mix) - a0]
        if b.get("sfx"):
            s = synth_sfx(b["sfx"], b.get("sfx_dur", 1.4)) * b.get("sfx_gain", 1.0)
            mix[a0: a0 + len(s)] += s[: len(mix) - a0]
    sting = synth_sfx("sting", 2.4)
    s0 = int(story_end * SR)
    mix[s0: s0 + len(sting)] += sting[: len(mix) - s0]
    mix = mix / max(1.0, float(np.max(np.abs(mix))) / 0.95)

    out_dir = ROOT / "cikti" / ep_path.parent.parent.name
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = ep_path.stem
    wav = out_dir / f"{stem}.wav"
    write_wav(wav, mix[: int(SR * total)])
    out = out_dir / f"{stem}.mp4"

    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    ctx.set_line_join(1)
    if preview:  # contact sheet of a few frames instead of a video
        ts = [b["start"] + 0.4 for b in beats][::max(1, len(beats) // 8)][:8] + [story_end + 1.5]
        sheet = cairo.ImageSurface(cairo.FORMAT_RGB24, 270 * len(ts), 480)
        sc = cairo.Context(sheet)
        for i, tt in enumerate(ts):
            r.frame(ctx, tt) if tt < story_end else (r.frame(ctx, story_end - 0.01), r.end_card(ctx, 1))
            sc.save()
            sc.translate(270 * i, 0)
            sc.scale(0.25, 0.25)
            sc.set_source_surface(surf, 0, 0)
            sc.paint()
            sc.restore()
        p = out_dir / f"{stem}_preview.png"
        sheet.write_to_png(str(p))
        print(p, f"{total:.1f}s")
        return p

    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium",
         "-crf", "21", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k", "-shortest",
         "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    nframes = int(total * FPS)
    for f in range(nframes):
        t = f / FPS
        if t < story_end:
            r.frame(ctx, t)
        else:
            r.frame(ctx, story_end - 0.01)
            r.end_card(ctx, t - story_end)
        surf.flush()
        enc.stdin.write(surf.get_data())
    enc.stdin.close()
    enc.wait()
    wav.unlink()
    print(out, f"{total:.1f}s")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="+")
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    for e in a.episodes:
        render(e, a.preview)
