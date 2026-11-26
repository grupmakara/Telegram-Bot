"""Flat 2D vector character rig (frontal bust) drawn with cairo.

Local coordinates: (0, 0) is the bottom-centre of the character, head centre
sits at (0, -1010). One unit = one pixel at scale 1 on a 1080x1920 canvas.
"""
import math

OUTLINE = (0.17, 0.15, 0.15)
LW = 5


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def shade(c, f):
    return tuple(max(0, min(1, x * f)) for x in c)


def ellipse(ctx, cx, cy, rx, ry):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def fill_stroke(ctx, color, lw=LW, stroke=True):
    ctx.set_source_rgb(*color)
    if stroke:
        ctx.fill_preserve()
        ctx.set_source_rgb(*OUTLINE)
        ctx.set_line_width(lw)
        ctx.stroke()
    else:
        ctx.fill()


def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


# ---------------------------------------------------------------- body ----
def draw_body(ctx, s):
    top = hexc(s["outfit"])
    inner = hexc(s.get("inner", "#f4f1ea"))
    kind = s.get("outfit_type", "sweater")

    def torso():
        ctx.move_to(-255, 10)
        ctx.line_to(-255, -660)
        ctx.curve_to(-255, -760, -200, -790, -120, -800)
        ctx.line_to(120, -800)
        ctx.curve_to(200, -790, 255, -760, 255, -660)
        ctx.line_to(255, 10)
        ctx.close_path()

    # neck
    skin = hexc(s["skin"])
    ctx.rectangle(-52, -880, 104, 110)
    fill_stroke(ctx, shade(skin, 0.9))

    torso()
    fill_stroke(ctx, inner if kind in ("vest", "denim") else top)

    if kind == "vest":  # shirt underneath, vest panels on top
        for sgn in (-1, 1):
            ctx.move_to(sgn * 255, 10)
            ctx.line_to(sgn * 255, -660)
            ctx.curve_to(sgn * 255, -760, sgn * 200, -790, sgn * 120, -800)
            ctx.line_to(sgn * 70, -800)
            ctx.line_to(sgn * 18, -560)
            ctx.line_to(sgn * 18, 10)
            ctx.close_path()
            fill_stroke(ctx, top)
        for y in (-480, -360, -240):
            ellipse(ctx, 34, y, 9, 9)
            fill_stroke(ctx, shade(top, 0.6), 3)
        # collar
        for sgn in (-1, 1):
            ctx.move_to(sgn * 8, -800)
            ctx.line_to(sgn * 70, -805)
            ctx.line_to(sgn * 40, -735)
            ctx.close_path()
            fill_stroke(ctx, inner, 4)
    elif kind in ("suit", "blazer"):
        # shirt V
        ctx.move_to(-75, -800)
        ctx.line_to(0, -620)
        ctx.line_to(75, -800)
        ctx.close_path()
        fill_stroke(ctx, inner, 4)
        if kind == "suit":
            tie = hexc(s.get("tie", "#b3262e"))
            ctx.move_to(-18, -790)
            ctx.line_to(18, -790)
            ctx.line_to(26, -640)
            ctx.line_to(0, -600)
            ctx.line_to(-26, -640)
            ctx.close_path()
            fill_stroke(ctx, tie, 4)
        for sgn in (-1, 1):  # lapels
            ctx.move_to(sgn * 75, -800)
            ctx.line_to(sgn * 125, -790)
            ctx.line_to(sgn * 95, -660)
            ctx.line_to(sgn * 135, -640)
            ctx.line_to(sgn * 0, -560)
            ctx.close_path()
            fill_stroke(ctx, shade(top, 0.82), 4)
        ellipse(ctx, 0, -420, 10, 10)
        fill_stroke(ctx, shade(top, 0.6), 3)
        if s.get("pearls"):
            for i in range(11):
                a = math.pi * (0.15 + 0.7 * i / 10)
                ellipse(ctx, -math.cos(a) * 70, -805 + math.sin(a) * 70, 11, 11)
                fill_stroke(ctx, (0.97, 0.95, 0.9), 2.5)
    elif kind == "denim":
        for sgn in (-1, 1):
            ctx.move_to(sgn * 255, 10)
            ctx.line_to(sgn * 255, -660)
            ctx.curve_to(sgn * 255, -760, sgn * 200, -790, sgn * 120, -800)
            ctx.line_to(sgn * 80, -800)
            ctx.line_to(sgn * 60, 10)
            ctx.close_path()
            fill_stroke(ctx, top)
            ctx.rectangle(sgn * 150 - 40, -560, 80, 60)
            fill_stroke(ctx, shade(top, 0.85), 3)
        ctx.arc(0, -800, 70, 0, math.pi)
        ctx.set_source_rgb(*OUTLINE)
        ctx.set_line_width(4)
        ctx.stroke()
    else:  # sweater / round collar
        ctx.arc(0, -800, 72, 0, math.pi)
        ctx.close_path()
        fill_stroke(ctx, shade(top, 0.85), 4)
        if s.get("scarf"):
            sc = hexc(s["scarf"])
            rrect(ctx, -110, -830, 220, 70, 30)
            fill_stroke(ctx, sc)
            rrect(ctx, 30, -790, 55, 200, 20)
            fill_stroke(ctx, sc)


# ---------------------------------------------------------------- hair ----
def hair_back(ctx, s):
    st = s.get("hair_style", "short")
    hc = hexc(s.get("hair", "#2b2522"))
    if st == "long":
        ctx.move_to(-190, -760)
        ctx.line_to(-190, -1040)
        ctx.curve_to(-190, -1250, 190, -1250, 190, -1040)
        ctx.line_to(190, -760)
        ctx.curve_to(120, -740, -120, -740, -190, -760)
        ctx.close_path()
        fill_stroke(ctx, hc)
    elif st == "bob":
        ctx.move_to(-195, -890)
        ctx.line_to(-195, -1040)
        ctx.curve_to(-195, -1250, 195, -1250, 195, -1040)
        ctx.line_to(195, -890)
        ctx.curve_to(120, -870, -120, -870, -195, -890)
        ctx.close_path()
        fill_stroke(ctx, hc)
    elif st == "headscarf":
        ellipse(ctx, 0, -1020, 215, 235)
        fill_stroke(ctx, hexc(s.get("scarf_color", "#7b4fa0")))


def hair_front(ctx, s):
    st = s.get("hair_style", "short")
    hc = hexc(s.get("hair", "#2b2522"))
    if st == "bald":
        for sgn in (-1, 1):
            ellipse(ctx, sgn * 140, -1045, 26, 60)
            fill_stroke(ctx, hc)
        return
    if st == "headscarf":
        sc = hexc(s.get("scarf_color", "#7b4fa0"))
        ctx.move_to(-190, -900)
        ctx.curve_to(-215, -1250, 215, -1250, 190, -900)
        ctx.line_to(150, -930)
        ctx.curve_to(150, -1170, -150, -1170, -150, -930)
        ctx.close_path()
        fill_stroke(ctx, sc)
        return
    # cap of hair over the top of head
    ctx.save()
    if st in ("short", "spiky", "slick", "long", "bob"):
        ctx.move_to(-162, -1000)
        ctx.curve_to(-178, -1272, 178, -1272, 162, -1000)
        if st == "spiky":
            pts = [(130, -1100), (100, -1080), (70, -1115), (35, -1085), (0, -1120),
                   (-35, -1088), (-70, -1118), (-100, -1082), (-135, -1105)]
            for p in pts:
                ctx.line_to(*p)
        elif st == "slick":
            ctx.curve_to(120, -1130, -40, -1150, -150, -1080)
        elif st in ("long", "bob"):
            ctx.curve_to(150, -1130, 40, -1160, -10, -1150)  # side parting
            ctx.curve_to(-60, -1120, -130, -1100, -165, -1000)
        else:
            ctx.curve_to(110, -1110, 60, -1095, 0, -1100)
            ctx.curve_to(-60, -1095, -120, -1110, -160, -1010)
        ctx.close_path()
        fill_stroke(ctx, hc)
        if s.get("gray_temples"):
            for sgn in (-1, 1):
                ellipse(ctx, sgn * 150, -1040, 16, 45)
                fill_stroke(ctx, (0.75, 0.75, 0.75), 3)
        if st == "slick":
            ctx.move_to(-60, -1170)
            ctx.curve_to(0, -1185, 60, -1175, 100, -1150)
            ctx.set_source_rgba(1, 1, 1, 0.35)
            ctx.set_line_width(10)
            ctx.stroke()
    ctx.restore()


# ---------------------------------------------------------------- face ----
BROWS = {  # (inner dy, outer dy) relative offsets: + is down
    "neutral": (0, 0), "smile": (-4, 0), "angry": (16, -10), "surprised": (-22, -18),
    "sad": (-16, 8), "smug": (-6, 6), "worried": (-14, 6),
}


def draw_face(ctx, s, mood, mouth_open, blink, look):
    skin = hexc(s["skin"])
    female = s.get("female", False)
    # ears + head
    for sgn in (-1, 1):
        ellipse(ctx, sgn * 150, -1000, 28, 42)
        fill_stroke(ctx, skin)
    ellipse(ctx, 0, -1010, 152, 178)
    fill_stroke(ctx, skin)
    if s.get("beard_shadow"):
        ctx.save()
        ellipse(ctx, 0, -1010, 150, 176)
        ctx.clip()
        ellipse(ctx, 0, -900, 120, 70)
        ctx.set_source_rgba(0.35, 0.3, 0.3, 0.18)
        ctx.fill()
        ctx.restore()
    # blush
    for sgn in (-1, 1):
        ellipse(ctx, sgn * 90, -960, 32, 18)
        ctx.set_source_rgba(0.95, 0.45, 0.45, 0.30 if female else 0.18)
        ctx.fill()
    # eyes
    lx = look * 6
    for sgn in (-1, 1):
        ex, ey = sgn * 58, -1015
        ellipse(ctx, ex, ey, 30, 24 if mood != "surprised" else 30)
        fill_stroke(ctx, (1, 1, 1), 4)
        ctx.save()
        ellipse(ctx, ex, ey, 30, 30)
        ctx.clip()
        ellipse(ctx, ex + lx, ey + 2, 17, 17)
        ctx.set_source_rgb(*hexc(s.get("eyes", "#5a3a22")))
        ctx.fill()
        ellipse(ctx, ex + lx, ey + 2, 8, 8)
        ctx.set_source_rgb(0.08, 0.06, 0.06)
        ctx.fill()
        ellipse(ctx, ex + lx + 5, ey - 4, 4, 4)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()
        # lids
        lid = 0.0
        if mood in ("smug",):
            lid = 0.45
        elif mood == "angry":
            lid = 0.3
        elif mood == "sad":
            lid = 0.25
        lid = max(lid, blink)
        if lid > 0:
            ctx.rectangle(ex - 34, ey - 32, 68, 8 + 56 * lid)
            ctx.set_source_rgb(*skin)
            ctx.fill()
            ctx.move_to(ex - 31, ey - 24 + 56 * lid)
            ctx.line_to(ex + 31, ey - 24 + 56 * lid)
            ctx.set_source_rgb(*OUTLINE)
            ctx.set_line_width(4)
            ctx.stroke()
        ctx.restore()
        if female:
            ctx.move_to(ex + sgn * 26, ey - 14)
            ctx.line_to(ex + sgn * 40, ey - 24)
            ctx.set_source_rgb(*OUTLINE)
            ctx.set_line_width(4)
            ctx.stroke()
    # brows
    bi, bo = BROWS.get(mood, (0, 0))
    bw = s.get("brow_w", 9)
    for sgn in (-1, 1):
        ctx.move_to(sgn * 25, -1062 + bi)
        ctx.line_to(sgn * 88, -1062 + bo)
        ctx.set_source_rgb(*hexc(s.get("brows", s.get("hair", "#2b2522"))))
        ctx.set_line_width(bw)
        ctx.set_line_cap(1)
        ctx.stroke()
    # nose
    ctx.move_to(-6, -1000)
    ctx.curve_to(-14, -975, -10, -965, 8, -965)
    ctx.set_source_rgb(*shade(skin, 0.7))
    ctx.set_line_width(4)
    ctx.stroke()
    if s.get("wrinkles"):
        ctx.set_source_rgba(*shade(skin, 0.7), 1)
        ctx.set_line_width(3)
        for y in (-1105, -1092):
            ctx.move_to(-45, y)
            ctx.curve_to(-15, y - 6, 15, y - 6, 45, y)
            ctx.stroke()
        for sgn in (-1, 1):
            ctx.move_to(sgn * 50, -965)
            ctx.curve_to(sgn * 62, -945, sgn * 60, -930, sgn * 52, -915)
            ctx.stroke()
    # mustache
    if s.get("mustache"):
        ctx.move_to(-62, -930)
        ctx.curve_to(-50, -965, 50, -965, 62, -930)
        ctx.curve_to(30, -945, -30, -945, -62, -930)
        fill_stroke(ctx, hexc(s.get("mustache_color", s.get("hair", "#2b2522"))), 3)
    # mouth
    my = -918
    lip = hexc(s.get("lips", "#8e3b3b"))
    if mouth_open > 0.08:
        h = 8 + 38 * mouth_open
        w = 34 + 8 * mouth_open
        ellipse(ctx, 0, my, w, h)
        fill_stroke(ctx, (0.42, 0.11, 0.12), 4)
        ctx.save()
        ellipse(ctx, 0, my, w, h)
        ctx.clip()
        ctx.rectangle(-w, my - h, 2 * w, h * 0.45)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()
        ellipse(ctx, 0, my + h * 0.8, w * 0.6, h * 0.5)
        ctx.set_source_rgb(0.85, 0.4, 0.42)
        ctx.fill()
        ctx.restore()
    elif mood == "surprised":
        ellipse(ctx, 0, my, 16, 20)
        fill_stroke(ctx, (0.42, 0.11, 0.12), 4)
    else:
        curve = {"smile": 22, "smug": 10, "sad": -16, "angry": -10, "worried": -8}.get(mood, 4)
        x0 = 38 if mood != "smug" else 30
        ctx.move_to(-x0, my)
        ctx.curve_to(-x0 / 2, my + curve, x0 / 2, my + curve, x0 + (12 if mood == "smug" else 0), my - (8 if mood == "smug" else 0))
        ctx.set_source_rgb(*(lip if female else OUTLINE))
        ctx.set_line_width(7 if female else 5)
        ctx.set_line_cap(1)
        ctx.stroke()
    # glasses
    if s.get("glasses"):
        for sgn in (-1, 1):
            rrect(ctx, sgn * 58 - 44, -1048, 88, 66, 18)
            ctx.set_source_rgba(0.8, 0.9, 1, 0.18)
            ctx.fill_preserve()
            ctx.set_source_rgb(*OUTLINE)
            ctx.set_line_width(6)
            ctx.stroke()
        ctx.move_to(-14, -1022)
        ctx.line_to(14, -1022)
        ctx.stroke()


def draw_character(ctx, spec, x, y, scale, mood="neutral", mouth_open=0.0,
                   blink=0.0, look=0.0, bob=0.0, tilt=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)
    ctx.set_line_join(1)
    draw_body(ctx, spec)
    ctx.translate(0, bob)
    ctx.translate(0, -880)
    ctx.rotate(tilt)
    ctx.translate(0, 880)
    hair_back(ctx, spec)
    draw_face(ctx, spec, mood, mouth_open, blink, look)
    hair_front(ctx, spec)
    ctx.restore()
