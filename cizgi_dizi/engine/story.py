"""Instagram Story (1080x1920) announcing an episode before it goes live.

Usage: python3 engine/story.py diziler/<dizi>/bolumler/bolumNN.json [...]
Output: cikti/<dizi>/story/storyNN.png
Instagram covers roughly the top 250 px and bottom 250 px with its own UI, so
everything important sits between y=260 and y=1670.
"""
import json
import math
import sys
from pathlib import Path

import cairo

sys.path.insert(0, str(Path(__file__).parent))
import render  # noqa: E402
from rig import hexc, rrect  # noqa: E402
from sets import FONT, H, W  # noqa: E402

SLOTS = ["12:30", "18:00", "21:00"]  # 3 episodes a day


def key_frame(ep_path, ep, cast):
    beats, end = render.build_timeline(ep, cast, render.ROOT / "seslendirme" / ep_path.parent.parent.name / ep_path.stem)
    r = render.Renderer(ep, cast, beats, end + 2.6)
    r.clean = True
    first = next((b for b in beats if b.get("teaser")), beats[0])
    src = first.get("orig", first)
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    ctx.set_line_join(1)
    r.frame(ctx, src["start"] + min(0.8, src["dur"] * 0.5))
    return surf


def text_center(ctx, txt, y, size, color, bold=True, maxw=940):
    ctx.select_font_face(FONT, 0, 1 if bold else 0)
    ctx.set_font_size(size)
    lines = render.wrap(ctx, txt, maxw)
    for i, l in enumerate(lines):
        e = ctx.text_extents(l)
        ctx.move_to(540 - e.x_advance / 2, y + i * size * 1.2)
        ctx.set_source_rgb(*color)
        ctx.show_text(l)
    return len(lines)


def make_story(ep_path):
    ep_path = Path(ep_path)
    ep = json.loads(ep_path.read_text(encoding="utf-8"))
    cast = json.loads((ep_path.parent.parent / "cast.json").read_text(encoding="utf-8"))
    n = ep["episode"]
    still = key_frame(ep_path, ep, cast)

    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    ctx.set_line_join(1)
    g = cairo.RadialGradient(540, 900, 100, 540, 960, 1250)
    g.add_color_stop_rgb(0, *hexc("#4a3cc4"))
    g.add_color_stop_rgb(1, *hexc("#120f2a"))
    ctx.set_source(g)
    ctx.paint()
    ctx.save()
    ctx.translate(540, 900)
    for i in range(20):  # light rays
        ctx.rotate(math.pi * 2 / 20)
        ctx.move_to(0, 0)
        ctx.line_to(-80, -1400)
        ctx.line_to(80, -1400)
        ctx.close_path()
        ctx.set_source_rgba(1, 1, 1, 0.04)
        ctx.fill()
    ctx.restore()

    # header
    render.draw_pill(ctx, render.tr_upper(ep["series"]), y=300, size=46, bg="#f5c542", fg="#15132e")

    # tilted card with the key moment
    cw, chh = 600, 1066
    ctx.save()
    ctx.translate(540, 900)
    ctx.rotate(math.radians(-3))
    rrect(ctx, -cw / 2 - 12, -chh / 2 - 12, cw + 24, chh + 24, 36)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()
    rrect(ctx, -cw / 2, -chh / 2, cw, chh, 28)
    ctx.clip()
    ctx.scale(cw / W, chh / H)
    ctx.translate(-W / 2, -H / 2)
    ctx.set_source_surface(still, 0, 0)
    ctx.paint()
    ctx.restore()

    # "NEW EPISODE" sticker
    ctx.save()
    ctx.translate(820, 430)
    ctx.rotate(math.radians(12))
    ctx.translate(-540, 0)  # draw_pill centres on x=540
    render.draw_pill(ctx, "YENİ BÖLÜM", y=0, size=40, bg="#e23b3b", fg="#ffffff")
    ctx.restore()

    # hook bubble over the bottom of the card
    hook = ep.get("story_hook") or ep["title"].split("|")[0].strip()
    ctx.select_font_face(FONT, 0, 1)
    ctx.set_font_size(58)
    lines = render.wrap(ctx, hook, 860)
    bh = 58 * 1.25 * len(lines) + 50
    top = 1420 - bh / 2
    rrect(ctx, 70, top, 940, bh, 30)
    ctx.set_source_rgb(*hexc("#ffffff"))
    ctx.fill_preserve()
    ctx.set_source_rgb(0.08, 0.08, 0.1)
    ctx.set_line_width(6)
    ctx.stroke()
    text_center(ctx, hook, top + 25 + 58 * 0.95, 58, hexc("#15132e"), maxw=860)

    # episode + time
    slot = SLOTS[(n - 1) % 3]
    label = "SEZON FİNALİ" if ep.get("finale") else f"{n}. BÖLÜM"
    render.draw_pill(ctx, f"{label} • BUGÜN {slot}", y=1610, size=46, bg="#e23b3b", fg="#ffffff")

    out = render.ROOT / "cikti" / ep_path.parent.parent.name / "story" / f"story{n:02d}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    surf.write_to_png(str(out))
    print(out)
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        make_story(p)
