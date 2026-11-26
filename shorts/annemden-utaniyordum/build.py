"""Build the 9:16 Short: Ken Burns shots + word-highlight subtitles + narration."""
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
FPS = 30
W, H = 1080, 1920
END = 44.0  # total length (narration ends ~42.0s, then moral card)

# (start, end, image, crop x, crop y, crop w, zoom_from, zoom_to, focus_x, focus_y)
# crop w is in source pixels (1280x720); crop h = w * 16/9.
SHOTS = [
    (0.0, 5.2, "img_cart.png", 760, 0, 405, 1.00, 1.18, 0.5, 0.15),    # Elif sneaks / looks away
    (5.2, 11.4, "img_cart.png", 60, 0, 405, 1.18, 1.00, 0.5, 0.25),    # mother at simit cart
    (11.4, 16.6, "img_cart.png", 110, 30, 300, 1.00, 1.15, 0.5, 0.2),  # "Sonra verirsin kızım"
    (16.6, 21.6, "img_cart.png", 810, 50, 300, 1.00, 1.20, 0.5, 0.15), # Elif stays silent
    (21.6, 28.2, "img_fall.png", 228, 0, 405, 1.00, 1.22, 0.5, 0.45),  # fire alarm, Defne falls
    (28.2, 33.3, "img_rescue.png", 560, 0, 405, 1.15, 1.00, 0.5, 0.3), # mother carries Defne out
    (33.3, 37.5, "img_rescue.png", 690, 30, 270, 1.00, 1.15, 0.5, 0.2),# "Elif'in annesi" (hero)
    (37.5, 40.3, "img_cart.png", 845, 50, 240, 1.00, 1.15, 0.5, 0.2),  # Elif cries with pride
    (40.3, END, "img_cart.png", 470, 0, 405, 1.20, 1.00, 0.5, 0.4),    # front entrance (loop)
]

FIXES = {"tezgahını": "tezgâhını", "Annem,": "Annem", "sonra": "“Sonra", "kızım": "kızım”",
         "Zavallı": "“Zavallı", "kadın.": "kadın.”", "Ben": "Ben...", "Elif'in": "“Elif'in",
         "annesi.": "annesi.”", "çaldı.": "çaldı!", "gitti.": "gitti...", "Biri": "biri",
         "kez": "kez..."}


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def render_shot(i, shot):
    start, end, img, cx, cy, cw, z0, z1, fx, fy = shot
    ch = round(cw * 16 / 9)
    frames = round((end - start) * FPS)
    out = HERE / f"shot_{i:02d}.mp4"
    zoom = f"{z0}+({z1}-{z0})*on/{max(frames - 1, 1)}"
    vf = (
        f"crop={cw}:{ch}:{cx}:{cy},scale=2160:3840:flags=lanczos,"
        f"zoompan=z='{zoom}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}'"
        f":d={frames}:s={W}x{H}:fps={FPS},format=yuv420p"
    )
    run(["ffmpeg", "-y", "-i", str(HERE / img), "-vf", vf, "-frames:v", str(frames),
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(out)])
    return out


def ass_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def build_subs():
    raw = json.loads((HERE / "words.json").read_text())
    words = []
    for w in raw:  # merge Whisper's split suffixes ("Defne" + "'nin")
        if w["w"].startswith("'") and words:
            words[-1]["w"] += w["w"]
            words[-1]["e"] = w["e"]
        else:
            words.append(dict(w))
    for w in words:
        w["w"] = FIXES.get(w["w"], w["w"])

    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["w"][-1] in ".!?:”":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)

    events = []
    for c in chunks:
        for j, w in enumerate(c):
            s = w["s"]
            e = c[j + 1]["s"] if j + 1 < len(c) else w["e"] + 0.15
            text = " ".join(
                ("{\\c&H00D7FF&\\fscx110\\fscy110}" + x["w"] + "{\\r}") if k == j else x["w"]
                for k, x in enumerate(c)
            )
            events.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Sub,,0,0,0,,{text}")

    moral = "{\\fad(400,0)}Ailenin işi değil,\\Nkalbi önemlidir ♥"
    events.append(f"Dialogue: 1,{ass_time(42.1)},{ass_time(END)},Moral,,0,0,0,,{moral}")

    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,2,70,70,560,1
Style: Moral,DejaVu Sans,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,3,24,0,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(events) + "\n"
    path = HERE / "subs.ass"
    path.write_text(ass, encoding="utf-8")
    return path


def main():
    shots = [render_shot(i, s) for i, s in enumerate(SHOTS)]
    lst = HERE / "shots.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in shots))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
         str(HERE / "video_raw.mp4")])
    subs = build_subs()
    out = HERE / "annemden_utaniyordum_short.mp4"
    run(["ffmpeg", "-y", "-i", str(HERE / "video_raw.mp4"), "-i", str(HERE / "voice.mp3"),
         "-filter_complex",
         f"[0:v]ass={subs.name},fade=t=out:st={END - 0.6}:d=0.6[v];"
         f"[1:a]apad,atrim=0:{END},afade=t=out:st={END - 0.6}:d=0.6[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(END), str(out)])
    print(out)


if __name__ == "__main__":
    import os
    os.chdir(HERE)
    main()
