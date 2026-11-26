"""Backgrounds and props in the same flat vector style (1080x1920 canvas)."""
import math
import random

import cairo

from rig import OUTLINE, ellipse, fill_stroke, hexc, rrect, shade

W, H = 1080, 1920
FONT = "DejaVu Sans"


def _grad(ctx, y0, y1, c0, c1):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, *hexc(c0))
    g.add_color_stop_rgb(1, *hexc(c1))
    ctx.rectangle(0, y0, W, y1 - y0)
    ctx.set_source(g)
    ctx.fill()


def _text(ctx, txt, x, y, size, color=(1, 1, 1), bold=True, center=True, maxw=460):
    ctx.select_font_face(FONT, 0, 1 if bold else 0)
    ctx.set_font_size(size)
    ext = ctx.text_extents(txt)
    while ext.width > maxw and size > 12:
        size *= 0.92
        ctx.set_font_size(size)
        ext = ctx.text_extents(txt)
    ctx.move_to(x - (ext.width / 2 + ext.x_bearing if center else 0), y)
    ctx.set_source_rgb(*color)
    ctx.show_text(txt)


def _window(ctx, x, y, w, h, lit=False, night=False):
    rrect(ctx, x, y, w, h, 6)
    glass = "#f2d27a" if lit else ("#2b3c5c" if night else "#bcd8ea")
    fill_stroke(ctx, hexc(glass), 4)
    ctx.move_to(x + w / 2, y)
    ctx.line_to(x + w / 2, y + h)
    ctx.move_to(x, y + h * 0.4)
    ctx.line_to(x + w, y + h * 0.4)
    ctx.set_source_rgb(*OUTLINE)
    ctx.set_line_width(4)
    ctx.stroke()


def bg_lobby(ctx, night=False):
    _grad(ctx, 0, 1300, "#efe3c8", "#e2d1ad")
    ctx.rectangle(0, 0, W, 90)
    fill_stroke(ctx, hexc("#d8c59c"), 4)
    # wainscot
    ctx.rectangle(0, 1050, W, 250)
    fill_stroke(ctx, hexc("#9c6b43"), 4)
    for x in range(30, W, 170):
        rrect(ctx, x, 1080, 130, 190, 8)
        fill_stroke(ctx, hexc("#8a5d39"), 3)
    # marble floor
    for r in range(6):
        for c in range(9):
            col = "#ddd6ca" if (r + c) % 2 == 0 else "#b9b0a2"
            ctx.rectangle(c * 125 - (r % 2) * 60, 1300 + r * 110, 125, 110)
            ctx.set_source_rgb(*hexc(col))
            ctx.fill()
    # elevator
    ctx.rectangle(690, 520, 330, 530)
    fill_stroke(ctx, hexc("#7d8188"))
    ctx.rectangle(715, 545, 140, 505)
    fill_stroke(ctx, hexc("#c7ccd3"))
    ctx.rectangle(855, 545, 140, 505)
    fill_stroke(ctx, hexc("#bfc4cb"))
    rrect(ctx, 790, 440, 130, 60, 10)
    fill_stroke(ctx, hexc("#222222"))
    _text(ctx, "4", 855, 486, 44, hexc("#ff5a3c"))
    # mailboxes
    for r in range(3):
        for c in range(3):
            ctx.rectangle(60 + c * 95, 600 + r * 80, 85, 70)
            fill_stroke(ctx, hexc("#b8893c"), 4)
            ctx.rectangle(80 + c * 95, 620 + r * 80, 45, 10)
            ctx.set_source_rgb(*OUTLINE)
            ctx.fill()
    # wall lamp
    for lx in (520,):
        ellipse(ctx, lx, 380, 40, 55)
        fill_stroke(ctx, hexc("#ffe9a8"), 4)
    # plant
    rrect(ctx, 400, 920, 110, 130, 12)
    fill_stroke(ctx, hexc("#a35a3a"))
    for a in range(-3, 4):
        ellipse(ctx, 455 + a * 28, 860 - abs(a) * -10, 26, 70)
        fill_stroke(ctx, hexc("#4f8a4b"), 3)
    _text(ctx, "SEDEF APT.", 540, 300, 56, hexc("#7a5a2f"), maxw=900)
    if night:
        ctx.rectangle(0, 0, W, H)
        ctx.set_source_rgba(0.05, 0.08, 0.2, 0.35)
        ctx.fill()


def bg_basement(ctx, night=False):
    _grad(ctx, 0, 1350, "#b8a789", "#a39373")
    ctx.rectangle(0, 1350, W, H - 1350)
    ctx.set_source_rgb(*hexc("#6e5a44"))
    ctx.fill()
    for y in range(1380, H, 70):
        ctx.move_to(0, y)
        ctx.line_to(W, y)
    ctx.set_source_rgba(0, 0, 0, 0.25)
    ctx.set_line_width(3)
    ctx.stroke()
    # pipes
    ctx.rectangle(0, 120, W, 34)
    fill_stroke(ctx, hexc("#8b8f93"), 4)
    # high window (street level)
    ctx.rectangle(330, 200, 420, 190)
    fill_stroke(ctx, hexc("#1f2d4a" if night else "#9fc3de"))
    for x in range(360, 750, 55):
        ctx.move_to(x, 200)
        ctx.line_to(x, 390)
    ctx.set_source_rgb(*OUTLINE)
    ctx.set_line_width(7)
    ctx.stroke()
    # shelf with jars
    ctx.rectangle(40, 640, 300, 22)
    fill_stroke(ctx, hexc("#7a5132"), 4)
    for i, col in enumerate(["#c9772f", "#d9c04a", "#8bb04a", "#b34b3b"]):
        rrect(ctx, 55 + i * 72, 560, 55, 80, 10)
        fill_stroke(ctx, hexc(col), 3)
    # stove + teapot (çaydanlık)
    ctx.rectangle(780, 860, 260, 190)
    fill_stroke(ctx, hexc("#e6e2da"))
    ellipse(ctx, 880, 800, 70, 60)
    fill_stroke(ctx, hexc("#c8402f"))
    ellipse(ctx, 880, 715, 45, 38)
    fill_stroke(ctx, hexc("#c8402f"))
    ctx.move_to(945, 800)
    ctx.line_to(1000, 760)
    ctx.set_source_rgb(*OUTLINE)
    ctx.set_line_width(10)
    ctx.stroke()
    # hanging bulb
    ctx.move_to(540, 0)
    ctx.line_to(540, 470)
    ctx.set_line_width(4)
    ctx.stroke()
    g = cairo.RadialGradient(540, 500, 10, 540, 500, 380)
    g.add_color_stop_rgba(0, 1, 0.95, 0.7, 0.55)
    g.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
    ctx.set_source(g)
    ctx.arc(540, 500, 380, 0, 2 * math.pi)
    ctx.fill()
    ellipse(ctx, 540, 500, 26, 34)
    fill_stroke(ctx, hexc("#fff2b8"), 4)
    # framed family photo
    rrect(ctx, 80, 300, 170, 210, 6)
    fill_stroke(ctx, hexc("#7a5132"))
    ctx.rectangle(100, 320, 130, 170)
    fill_stroke(ctx, hexc("#e9dcc0"), 3)


def bg_salon(ctx, night=True):
    _grad(ctx, 0, 1350, "#f3e7d3", "#e6d5b8")
    ctx.rectangle(0, 1350, W, H - 1350)
    ctx.set_source_rgb(*hexc("#8d5b3c"))
    ctx.fill()
    # bosphorus window
    wx, wy, ww, wh = 140, 230, 800, 760
    rrect(ctx, wx - 25, wy - 25, ww + 50, wh + 50, 10)
    fill_stroke(ctx, hexc("#7a4e2e"))
    ctx.save()
    ctx.rectangle(wx, wy, ww, wh)
    ctx.clip()
    _grad(ctx, wy, wy + wh, "#1d2546" if night else "#7fb6e0", "#c46a4f" if night else "#cfe6f5")
    ctx.move_to(wx, wy + 560)
    for i in range(9):
        ctx.line_to(wx + i * 100, wy + 520 + (i % 3) * 25)
    ctx.line_to(wx + ww, wy + wh)
    ctx.line_to(wx, wy + wh)
    ctx.close_path()
    ctx.set_source_rgb(*hexc("#2a2c3e" if night else "#5d7a5a"))
    ctx.fill()
    ctx.rectangle(wx, wy + 640, ww, 200)
    ctx.set_source_rgb(*hexc("#1a2a4a" if night else "#3d7fb3"))
    ctx.fill()
    # bridge
    ctx.set_source_rgb(*hexc("#d9d9e6"))
    ctx.set_line_width(5)
    for tx in (wx + 180, wx + 620):
        ctx.rectangle(tx, wy + 380, 16, 260)
        ctx.fill()
    ctx.move_to(wx - 20, wy + 600)
    ctx.curve_to(wx + 200, wy + 380, wx + 600, wy + 380, wx + ww + 20, wy + 600)
    ctx.stroke()
    ctx.rectangle(wx, wy + 600, ww, 10)
    ctx.fill()
    rnd = random.Random(3)
    for _ in range(70):
        ctx.arc(wx + rnd.random() * ww, wy + 470 + rnd.random() * 160, 3, 0, 6.3)
        ctx.set_source_rgb(1, 0.85, 0.4)
        ctx.fill()
    ctx.restore()
    for x in (wx + ww / 2,):
        ctx.move_to(x, wy)
        ctx.line_to(x, wy + wh)
    ctx.set_source_rgb(*hexc("#7a4e2e"))
    ctx.set_line_width(16)
    ctx.stroke()
    # curtains
    for sgn, x in ((1, 40), (-1, 1040)):
        ctx.move_to(x, 150)
        ctx.curve_to(x + sgn * 120, 500, x + sgn * 40, 900, x + sgn * 150, 1100)
        ctx.line_to(x, 1100)
        ctx.close_path()
        fill_stroke(ctx, hexc("#8d1f3a"))
    # chandelier
    ctx.move_to(540, 0)
    ctx.line_to(540, 90)
    ctx.set_source_rgb(*OUTLINE)
    ctx.set_line_width(4)
    ctx.stroke()
    ellipse(ctx, 540, 120, 120, 30)
    fill_stroke(ctx, hexc("#e0b84a"), 4)
    for i in range(-2, 3):
        ellipse(ctx, 540 + i * 50, 160, 12, 22)
        fill_stroke(ctx, hexc("#fff3c4"), 3)


def bg_street(ctx, night=False):
    _grad(ctx, 0, 900, "#26345e" if night else "#f2a76a", "#e58a6b" if night else "#f7d7a6")
    # facade
    ctx.rectangle(60, 140, 960, 1250)
    fill_stroke(ctx, hexc("#e8d9bb"))
    for r in range(4):
        for c in range(4):
            _window(ctx, 120 + c * 230, 210 + r * 230, 150, 170, lit=(r * 4 + c) % 3 == 0 or night)
            ctx.rectangle(110 + c * 230, 385 + r * 230, 170, 16)
            fill_stroke(ctx, hexc("#cdb88f"), 3)
    # door
    rrect(ctx, 400, 1100, 280, 290, 20)
    fill_stroke(ctx, hexc("#5b3a26"))
    ctx.rectangle(420, 1010, 240, 70)
    fill_stroke(ctx, hexc("#24344f"), 4)
    _text(ctx, "SEDEF APT.", 540, 1060, 36, hexc("#f3d27a"))
    # sidewalk + road
    ctx.rectangle(0, 1390, W, 140)
    fill_stroke(ctx, hexc("#b6aea2"), 4)
    ctx.rectangle(0, 1530, W, 390)
    ctx.set_source_rgb(*hexc("#4a4a50"))
    ctx.fill()
    # tree + lamp
    ctx.rectangle(905, 1050, 30, 340)
    fill_stroke(ctx, hexc("#6b4a2e"))
    for dx, dy in ((-60, 0), (60, 0), (0, -70), (-20, 40)):
        ellipse(ctx, 920 + dx, 980 + dy, 110, 90)
        fill_stroke(ctx, hexc("#4f8a4b"), 4)
    ctx.rectangle(140, 900, 18, 490)
    fill_stroke(ctx, hexc("#2d2d33"), 3)
    ellipse(ctx, 149, 890, 40, 30)
    fill_stroke(ctx, hexc("#ffe28a" if night else "#f3f0e0"), 4)


def bg_classroom(ctx, night=False):
    _grad(ctx, 0, 1350, "#e4e9e1", "#d3dacf")
    ctx.rectangle(0, 1350, W, H - 1350)
    ctx.set_source_rgb(*hexc("#9b7653"))
    ctx.fill()
    # chalkboard with a structural sketch
    rrect(ctx, 70, 250, 940, 560, 10)
    fill_stroke(ctx, hexc("#7a5132"))
    ctx.rectangle(95, 275, 890, 510)
    fill_stroke(ctx, hexc("#2f5d48"), 4)
    ctx.set_source_rgba(1, 1, 1, 0.85)
    ctx.set_line_width(5)
    for x in (200, 360, 520):  # frame: columns + beams
        ctx.move_to(x, 720)
        ctx.line_to(x, 380)
    for y in (380, 500, 620):
        ctx.move_to(200, y)
        ctx.line_to(520, y)
    ctx.stroke()
    ctx.move_to(170, 720)
    ctx.line_to(550, 720)
    ctx.stroke()
    _text(ctx, "F = m · a", 780, 420, 52, (1, 1, 1), maxw=360)
    _text(ctx, "Deprem yükü", 780, 520, 40, (1, 1, 1), maxw=360)
    # window + desk
    _window(ctx, 820, 880, 170, 300)
    ctx.rectangle(60, 1150, 520, 60)
    fill_stroke(ctx, hexc("#a8784c"))
    for i, col in enumerate(["#c94c3c", "#3c6fc9", "#e0b84a"]):
        ctx.rectangle(110 + i * 70, 1080 - i * 8, 55, 70 + i * 8)
        fill_stroke(ctx, hexc(col), 3)


BACKGROUNDS = {"classroom": bg_classroom, "lobby": bg_lobby, "basement": bg_basement, "salon": bg_salon, "street": bg_street}


def make_background(name):
    night = name.endswith("_night")
    base = name.replace("_night", "")
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    ctx.set_line_join(1)
    BACKGROUNDS[base](ctx, night=night)
    return surf


# ---------------------------------------------------------------- props ----
def prop_phone(ctx, t, caller="Bilinmeyen"):
    shake = math.sin(t * 60) * 8
    ctx.save()
    ctx.translate(540 + shake, 820)
    ctx.rotate(math.radians(-8))
    rrect(ctx, -150, -290, 300, 580, 40)
    fill_stroke(ctx, hexc("#1d1f2b"), 6)
    rrect(ctx, -130, -260, 260, 520, 24)
    fill_stroke(ctx, hexc("#2f6fe0"), 3)
    _text(ctx, "Gelen arama", 0, -170, 28, (0.9, 0.95, 1), bold=False)
    _text(ctx, caller, 0, -100, 46 if len(caller) < 10 else 34)
    ellipse(ctx, -65, 170, 42, 42)
    fill_stroke(ctx, hexc("#e23b3b"), 4)
    ellipse(ctx, 65, 170, 42, 42)
    fill_stroke(ctx, hexc("#2fbf5a"), 4)
    for sgn in (-1, 1):
        for k in (0, 1):
            ctx.arc(sgn * (185 + k * 30), -150, 30 + k * 10, -0.6 + (0 if sgn > 0 else math.pi),
                    0.6 + (0 if sgn > 0 else math.pi))
            ctx.set_source_rgb(*hexc("#f5c542"))
            ctx.set_line_width(6)
            ctx.stroke()
    ctx.restore()


def prop_photo(ctx, t, caption="1979"):
    ctx.save()
    ctx.translate(540, 760)
    ctx.rotate(math.radians(4))
    ctx.rectangle(-260, -300, 520, 600)
    fill_stroke(ctx, hexc("#f6f1e4"), 6)
    ctx.rectangle(-225, -265, 450, 420)
    fill_stroke(ctx, hexc("#c9b48a"), 4)
    # sepia building under construction + young man in hard hat
    ctx.rectangle(-170, -200, 220, 340)
    ctx.set_source_rgb(*hexc("#a88c5e"))
    ctx.fill()
    for y in range(-190, 140, 50):
        ctx.move_to(-180, y)
        ctx.line_to(60, y)
    for x in range(-170, 60, 55):
        ctx.move_to(x, -200)
        ctx.line_to(x, 140)
    ctx.set_source_rgb(*hexc("#6e5634"))
    ctx.set_line_width(4)
    ctx.stroke()
    ellipse(ctx, 130, 20, 38, 44)
    fill_stroke(ctx, hexc("#d7b88a"), 4)
    ctx.arc(130, 0, 44, math.pi, 2 * math.pi)
    fill_stroke(ctx, hexc("#e8d26a"), 4)
    ctx.rectangle(90, 65, 80, 90)
    fill_stroke(ctx, hexc("#8a7350"), 4)
    _text(ctx, caption, 0, 230, 44, hexc("#3a2f25"))
    ctx.restore()


def prop_document(ctx, t, caption="RAPOR"):
    ctx.save()
    ctx.translate(540, 780)
    ctx.rotate(math.radians(-3))
    ctx.rectangle(-270, -340, 540, 680)
    fill_stroke(ctx, hexc("#fbfaf5"), 6)
    title, *rows = caption.split("|")
    _text(ctx, title, 0, -250, 46, hexc("#24344f"))
    ctx.set_source_rgb(*hexc("#9aa0a8"))
    for i in range(9 - 2 * len(rows)):
        ctx.rectangle(-210, -180 + i * 50, 420 - (i % 3) * 60, 14)
        ctx.fill()
    for j, row in enumerate(rows):  # highlighted lines, e.g. the author's name
        y = -180 + (9 - 2 * len(rows)) * 50 + 30 + j * 70
        ctx.rectangle(-230, y - 42, 460, 58)
        ctx.set_source_rgba(1, 0.9, 0.3, 0.55)
        ctx.fill()
        _text(ctx, row, 0, y, 34, hexc("#1a1a1a"), maxw=440)
    ellipse(ctx, 175, 285, 58, 58)
    ctx.set_source_rgba(0.75, 0.1, 0.12, 0.8)
    ctx.set_line_width(7)
    ctx.stroke()
    _text(ctx, "MÜHÜR", 175, 295, 22, (0.75, 0.1, 0.12))
    ctx.restore()


def prop_money(ctx, t, caption=""):
    ctx.save()
    ctx.translate(540, 820)
    for i in range(6):
        rrect(ctx, -230, -40 - i * 34, 460, 120, 10)
        fill_stroke(ctx, hexc("#6fae6a"), 4)
        ellipse(ctx, 0, 20 - i * 34, 40, 40)
        ctx.set_source_rgb(*hexc("#4c8a48"))
        ctx.fill()
    if caption:
        _text(ctx, caption, 0, 200, 64, hexc("#fff2a8"), maxw=900)
    ctx.restore()


def prop_crack(ctx, t, caption=""):
    ctx.save()
    ctx.translate(540, 760)
    ctx.rectangle(-300, -330, 600, 660)
    fill_stroke(ctx, hexc("#e9dcc0"), 6)
    ctx.move_to(-200, -300)
    for x, y in ((-140, -200), (-170, -110), (-60, -20), (-90, 60), (20, 140), (0, 220), (110, 300)):
        ctx.line_to(x, y)
    ctx.set_source_rgb(*OUTLINE)
    ctx.set_line_width(7)
    ctx.stroke()
    ellipse(ctx, -60, -20, 120, 120)
    ctx.set_source_rgb(*hexc("#e23b3b"))
    ctx.set_line_width(8)
    ctx.stroke()
    if caption:
        _text(ctx, caption, 0, 300, 40, hexc("#3a2f25"), maxw=560)
    ctx.restore()


PROPS = {"phone": prop_phone, "photo": prop_photo, "document": prop_document,
         "money": prop_money, "crack": prop_crack}
