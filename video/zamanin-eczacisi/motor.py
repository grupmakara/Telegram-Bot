#!/usr/bin/env python3
"""Zamanın Eczacısı - bölüm derleme motoru.

Kullanım:  python3 motor.py bolum1      (bolum1.py senaryosunu derler)

Senaryo modülü şunları tanımlar: OUT (proje klasörü), LINES, SPLITS, HOOK_CUT,
HOOK (kanca yazısı), TITLE, END ve plan(add, S) fonksiyonu. Motor; seslerden
ağız hareketlerini ve kelime zamanlarını çıkarır, çekimleri zamanlar,
HyperFrames kompozisyonunu (OUT/index.html) ve miksaj için zamanlama.json yazar.
Eksik ses dosyaları için tahmini süre kullanılır.
"""
import importlib
import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import sanat  # noqa: E402
from sanat import (ayse, huseyin, mehmet, shop_bg, window_view, jars_closeup, pharmacy_bg,  # noqa: E402
                   pharmacy_front, mortar_closeup, room_bg, room_front, door_view, bowl_closeup,
                   court_bg, port_bg, street_bg)

SES = os.path.join(ROOT, os.environ.get('SES_DIR', 'ses5'))
KONTROL = os.path.join(ROOT, 'kontrol')
W, H = 1080, 1920
PAD_IN, PAD_OUT = 0.25, float(os.environ.get('PAD_OUT', '0.6'))


# ---------------------------------------------------------------- ses analizi
def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def audio_duration(path):
    return float(_run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]).strip())


def mouth_keys(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    hop = 16000 // 15
    rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    if rms.size == 0:
        return []
    thr = max(rms.max() * 0.22, 0.01)
    keys, state = [], False
    for i, v in enumerate(rms):
        want = bool(v > thr) and (i % 3 != 2)
        if want != state:
            keys.append((round(i / 15, 3), want))
            state = want
    if state:
        keys.append((round(len(rms) / 15, 3), False))
    return keys


def word_times(path):
    os.makedirs(KONTROL, exist_ok=True)
    name = os.path.basename(path)[:-4]
    js = os.path.join(KONTROL, name + '.json')
    if not os.path.exists(js):
        subprocess.run(['whisper', path, '--model', 'small', '--language', 'tr', '--fp16', 'False',
                        '--word_timestamps', 'True', '--output_format', 'json', '--output_dir', KONTROL],
                       capture_output=True)
    if not os.path.exists(js):
        return []
    d = json.load(open(js))
    return [(w['word'].strip(' ,.!?"\''), w['start']) for s in d['segments'] for w in s.get('words', [])]


def find_word(path, word):
    return next((t for w, t in word_times(path) if w.lower().startswith(word.lower())), None)


# ---------------------------------------------------------------- yardımcılar (senaryolar için)
class S:
    """Senaryolarda kullanılan kısayollar."""

    @staticmethod
    def C(role, x, y, s=1.0, **opts):
        return dict(role=role, x=x, y=y, s=s, **opts)

    @staticmethod
    def face(c):
        if c['role'] in ('ayse', 'fatma', 'zehra', 'leyla', 'ayseg'):
            return c['x'] - 10 * c['s'], c['y'] - 310 * c['s']
        if c['role'] == 'mehmet':
            return c['x'], c['y'] - 140 * c['s']
        return c['x'], c['y'] - 720 * c['s']

    @staticmethod
    def close(c, z0=2.5, z1=2.7):
        fx, fy = S.face(c)
        return ((z0, fx, fy), (z1, fx, fy))


# ---------------------------------------------------------------- derleme
def build(ep_name):
    ep = importlib.import_module(ep_name)
    sanat.INIT.clear()
    out_dir = os.path.join(ROOT, ep.OUT)
    lines = ep.LINES

    # Kanca sesi: bir repliğin başından belirli kelimeye kadar
    if getattr(ep, 'HOOK_CUT', None):
        src_key, word, hook_key, mode = ep.HOOK_CUT
        src = os.path.join(SES, lines[src_key][0])
        dst = os.path.join(SES, lines[hook_key][0])
        if os.path.exists(src) and not os.path.exists(dst):
            cut = find_word(src, word)
            if mode == 'all':
                args = []
            elif mode == 'until':
                if not cut:
                    print(f'UYARI: kanca kelimesi bulunamadı ({src_key}: {word}); 1.6 sn kullanılıyor', flush=True)
                cut = cut or 1.6
                args = ['-t', f'{cut - 0.05:.2f}', '-af', f'afade=t=out:st={max(cut - 0.2, 0):.2f}:d=0.15']
            else:
                args = ['-ss', f'{max((cut or 0) - 0.08, 0):.2f}', '-af', 'afade=t=in:d=0.05']
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, *args, dst], check=True)

    info = {}
    for key, (fname, who, text, est, *_) in lines.items():
        p = os.path.join(SES, fname)
        if os.path.exists(p):
            info[key] = dict(file=p, who=who, text=text, dur=audio_duration(p), keys=mouth_keys(p))
        else:
            info[key] = dict(file=None, who=who, text=text, dur=est, keys=[])
    missing = [k for k, v in info.items() if v['file'] is None]

    split_at = {}
    for key, (word, ratio) in ep.SPLITS.items():
        li = info[key]
        t = find_word(li['file'], word) if li['file'] else None
        split_at[key] = round(t if t is not None else li['dur'] * ratio, 3)

    shots = []

    def add(sid, kind, line=None, part=None, dur=None, extra=0.0, **kw):
        if dur is None:
            li = info[line]
            sp = split_at.get(line)
            if part == 'a':
                dur = PAD_IN + sp
            elif part == 'b':
                dur = li['dur'] - sp + PAD_OUT
            else:
                dur = PAD_IN + li['dur'] + PAD_OUT
            dur += extra
        shots.append(dict(id=sid, kind=kind, line=line, part=part, dur=round(dur, 3), **kw))

    ep.plan(add, S)

    t = 0.0
    for s in shots:
        s['start'] = round(t, 3)
        t += s['dur']
    total = round(t, 3)
    line_start = {}
    for s in shots:
        if s['line'] and s['line'] not in line_start:
            line_start[s['line']] = round(s['start'] + PAD_IN, 3)

    anim, body, sfx = [], [], []

    def cam_anim(sid, cam, dur, start):
        (z0, x0, y0), (z1, x1, y1) = cam
        f = lambda z, x, y: dict(x=round(W / 2 - z * x, 1), y=round(H / 2 - z * y, 1), scale=z)
        anim.append(f'tl.fromTo("#{sid}-w", {json.dumps(f(z0, x0, y0))}, {{...{json.dumps(f(z1, x1, y1))}, duration: {dur}, ease: "sine.inOut"}}, {start});')

    def lip(prefix, role, s):
        lk = s['line']
        if not lk or info[lk]['who'] != role:
            return
        t0 = line_start[lk]
        for kt, opened in info[lk]['keys']:
            at = round(t0 + kt, 3)
            if s['start'] <= at < s['start'] + s['dur']:
                anim.append(f'tl.set("#{prefix}-mouthO", {{opacity: {1 if opened else 0}}}, {at});')
                anim.append(f'tl.set("#{prefix}-mouthC", {{opacity: {0 if opened else 1}}}, {at});')

    def blinks(prefix, start, dur, offset=0.9, every=2.7):
        t = start + offset
        while t < start + dur - 0.2:
            for side in 'LR':
                anim.append(f'tl.to("#{prefix}-lid{side}", {{scaleY: 1, duration: 0.07}}, {t:.3f});')
                anim.append(f'tl.to("#{prefix}-lid{side}", {{scaleY: 0, duration: 0.09}}, {t + 0.1:.3f});')
            t += every

    def shake(target, at, n=6, amp=10):
        for i in range(n):
            anim.append(f'tl.to("{target}", {{x: "+={(-1) ** i * amp}", duration: 0.04}}, {at + 0.05 + i * 0.045:.3f});')

    def shot_div(sid, st, du, inner, width=W, extra=''):
        body.append(f'''
<div id="{sid}" class="clip shot" data-start="{st}" data-duration="{du}">
  <div class="world" id="{sid}-w" style="width:{width}px"><svg width="{width}" height="1920" viewBox="0 0 {width} 1920">{inner}</svg></div>
  {extra}<div class="vignette"></div>
</div>''')

    def card(sid, st, du, html, fade_in=0.5, fade_out=0.35, scale_from=1.06):
        body.append(f'<div id="{sid}" class="clip card" data-start="{st}" data-duration="{du}"><div class="card-in" id="{sid}-in">{html}</div></div>')
        anim.append(f'tl.fromTo("#{sid}-in", {{opacity: 0, scale: {scale_from}}}, {{opacity: 1, scale: 1, duration: {fade_in}, ease: "power2.out"}}, {st});')
        if fade_out:
            anim.append(f'tl.to("#{sid}-in", {{opacity: 0, duration: {fade_out}}}, {round(st + du - fade_out, 3)});')

    def draw_char(prefix, c):
        r = c['role']
        if r in ('ayse', 'fatma', 'zehra', 'leyla', 'ayseg'):
            return ayse(prefix, eyes=c.get('eyes', 'open'), brow=c.get('brow', 'neutral'), mouth=c.get('mouth', 'closed'),
                        tilt=c.get('tilt', 0), modern=c.get('modern', r == 'ayseg'), variant='ayse' if r == 'ayseg' else r)
        if r == 'mehmet':
            return mehmet(prefix, eyes=c.get('eyes', 'closed'), mouth=c.get('mouth', 'flat'),
                          sick=c.get('sick', True), cloth=c.get('cloth', False))
        return huseyin(prefix, brow=c.get('brow', 'neutral'), arm=c.get('arm', 0), variant=r)

    for s in shots:
        sid, st, du, kind = s['id'], s['start'], s['dur'], s['kind']
        speaker = info[s['line']]['who'] if s['line'] else None

        if kind == 'title':
            card(sid, st, du, f'<div class="ornament">✦</div><div class="title">ZAMANIN<br>ECZACISI</div><div class="rule"></div>'
                              f'<div class="subtitle">{ep.TITLE[0]}</div><div class="small">{ep.TITLE[1]}</div>'
                              + (f'<div style="display:inline-block;margin-top:44px;padding:16px 40px;border-radius:44px;background:#B2452E;'
                                 f'color:#fff;font-family:Nunito,sans-serif;font-style:italic;font-weight:800;font-size:46px;'
                                 f'letter-spacing:.04em;box-shadow:0 8px 24px rgba(0,0,0,.5)">{ep.TITLE[2]}</div>' if len(ep.TITLE) > 2 else ''),
                 scale_from=1.08)
            continue
        if kind == 'end':
            card(sid, st, du, f'<div class="small">{ep.END[0]}</div><div class="title sm">ZAMANIN ECZACISI</div><div class="small">{ep.END[1]}</div>',
                 fade_in=0.8, fade_out=0)
            continue
        if kind == 'black':
            card(sid, st, du, f'<div class="small big">{s["text"]}</div>' + (f'<div class="small">{s["sub"]}</div>' if s.get('sub') else ''), fade_in=0.4, fade_out=0.3, scale_from=1.0)
            continue

        if kind == 'stage':
            bg, bgkw = s['bg']
            back = {'shop': lambda: shop_bg(sid, **bgkw), 'pharmacy': lambda: pharmacy_bg(sid),
                    'room': lambda: room_bg(sid, **bgkw), 'door': lambda: door_view(sid, **bgkw),
                    'court': lambda: court_bg(sid), 'port': lambda: port_bg(sid), 'street': lambda: street_bg(sid, **bgkw)}[bg]()
            front = {'pharmacy': lambda: pharmacy_front(sid), 'room': lambda: room_front(sid, **bgkw)}.get(bg, lambda: '')()
            chars_svg = ''
            behind_front = ''
            for c in sorted(s['chars'], key=lambda c: c['role'] != 'mehmet'):
                g = f'<g transform="translate({c["x"]},{c["y"]}) scale({c["s"]})">{draw_char(f"{sid}-{c["role"]}", c)}</g>'
                if bg == 'room' and c['role'] != 'mehmet':
                    behind_front += g
                else:
                    chars_svg += g
            hook = ''
            if s.get('hook'):
                rozet = (f'<div style="display:inline-block;margin-bottom:22px;padding:12px 34px;border-radius:40px;background:#B2452E;'
                         f'color:#fff;font-family:Nunito,sans-serif;font-style:italic;font-weight:800;font-size:42px;'
                         f'box-shadow:0 6px 20px rgba(0,0,0,.5)">{ep.TITLE[2]}</div><br>' if len(ep.TITLE) > 2 else '')
                hook = (f'<div class="hook" id="{sid}-kanca">{rozet}<div class="h1">{ep.HOOK[0]}</div><div class="h2">{ep.HOOK[1]}</div></div>'
                        f'<div class="flashred" id="{sid}-kirmizi"></div>')
            shot_div(sid, st, du, back + chars_svg + front + behind_front, extra=hook)
            cam_anim(sid, s['cam'], du, st)
            for c in s['chars']:
                pr = f'{sid}-{c["role"]}'
                lip(pr, c['role'], s)
                if c.get('eyes', 'closed' if c['role'] == 'mehmet' else 'open') == 'open':
                    blinks(pr, st, du, 0.7 + (sum(map(ord, c['role'])) % 5) * 0.15)
                if c.get('wake') is not None:
                    w = st + c['wake']
                    for side in 'LR':
                        anim.append(f'tl.to("#{pr}-lid{side}", {{scaleY: 0, duration: 0.45, ease: "power1.out"}}, {w:.3f});')
                    if c['role'] != 'mehmet':
                        anim.append(f'tl.to("#{pr}-head", {{rotation: 0, duration: 0.8, ease: "sine.out"}}, {w:.3f});')
                    blinks(pr, w + 1.0, du - c['wake'] - 1.0, 0.0, 2.0)
                if c.get('shock'):
                    anim.append(f'tl.fromTo("#{pr}-head", {{y: 6}}, {{y: -10, duration: 0.18, ease: "power2.out"}}, {st + 0.12:.3f});')
                    shake(f'#{sid}-w', st + 0.12)
                    sfx.append(('boom', st + 0.12))
                if c.get('wave'):
                    anim.append(f'tl.to("#{pr}-arm", {{rotation: -38, duration: 0.35, ease: "back.out(2)"}}, {st + 0.2:.3f});')
                    anim.append(f'tl.to("#{pr}-arm", {{rotation: -24, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {st + 0.6:.3f});')
                if c.get('point'):
                    anim.append(f'tl.to("#{pr}-arm", {{rotation: -55, duration: 0.3, ease: "back.out(2)"}}, {st + 0.15:.3f});')
                if c['role'] == 'mehmet' and c.get('sick', True):
                    for i in range(2):
                        anim.append(f'tl.fromTo("#{pr}-ter{i}", {{y: 0, opacity: 1}}, {{y: 26, opacity: 0.2, duration: 1.6, repeat: {max(1, int(du / 1.6))}, ease: "power1.in"}}, {st + i * 0.7:.3f});')
                if speaker == c['role'] and c['role'] != 'mehmet':
                    anim.append(f'tl.to("#{pr}-head", {{rotation: "+=2", duration: 0.5, yoyo: true, repeat: {max(1, int(du / 0.5) - 1)}, ease: "sine.inOut"}}, {st + 0.1:.3f});')
            if bg == 'room':
                anim.append(f'tl.to("#{sid}-alev", {{scaleY: 1.15, svgOrigin: "260 722", duration: 0.25, yoyo: true, repeat: {int(du / 0.25)}, ease: "sine.inOut"}}, {st});')
                anim.append(f'tl.to("#{sid}-isik", {{opacity: "-=0.15", duration: 0.4, yoyo: true, repeat: {int(du / 0.4)}, ease: "sine.inOut"}}, {st});')
            if bg == 'port':
                anim.append(f'tl.to("#{sid}-gemi", {{y: 10, duration: 1.2, yoyo: true, repeat: {max(1, int(du / 1.2))}, ease: "sine.inOut"}}, {st});')
            if bg == 'pharmacy':
                anim.append(f'tl.to("#{sid}-hale", {{opacity: 0.8, duration: 0.9, yoyo: true, repeat: {max(1, int(du / 0.9))}, ease: "sine.inOut"}}, {st});')
            if bg == 'shop' and bgkw.get('mortar'):
                anim.append(f'tl.fromTo("#{sid}-hale", {{opacity: 0.2}}, {{opacity: 0.9, duration: 0.8, yoyo: true, repeat: {max(1, int(du / 0.8))}, ease: "sine.inOut"}}, {st});')
            if s.get('knock'):
                for i, k in enumerate(s['knock']):
                    shake(f'#{sid}-w', st + k, n=4, amp=7)
                    sfx.append(('knock', st + k))
            if s.get('hook'):
                anim.append(f'tl.fromTo("#{sid}-kanca", {{opacity: 0, scale: 1.5}}, {{opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2)"}}, {st});')
                anim.append(f'tl.fromTo("#{sid}-kanca b", {{color: "#FFFFFF"}}, {{color: "#FFC94A", duration: 0.3}}, {st + 0.4});')
                anim.append(f'tl.fromTo("#{sid}-kirmizi", {{opacity: 0.55}}, {{opacity: 0, duration: 0.6, ease: "power2.out"}}, {st});')
                if not any(c.get('shock') for c in s['chars']):
                    sfx.append(('boom', st))
        elif kind == 'mortar':
            shot_div(sid, st, du, mortar_closeup(sid, old=s.get('old', False)))
            z0, z1 = s['zoom']
            anim.append(f'tl.fromTo("#{sid}-w", {{scale: {z0}, x: {-(z0 - 1) * 540:.0f}, y: {-(z0 - 1) * 1170:.0f}}}, '
                        f'{{scale: {z1}, x: {-(z1 - 1) * 540:.0f}, y: {-(z1 - 1) * 1170:.0f}, duration: {du}, ease: "sine.inOut"}}, {st});')
            anim.append(f'tl.fromTo("#{sid}-yazi", {{opacity: 0.35}}, {{opacity: 1, duration: {du * 0.8:.2f}, ease: "power1.in"}}, {st});')
            anim.append(f'tl.fromTo("#{sid}-hale", {{opacity: 0.3, scale: 0.9, svgOrigin: "540 1170"}}, {{opacity: 1, scale: 1.25, duration: {du}, ease: "power1.in"}}, {st});')
            if s.get('touch'):
                anim.append(f'tl.fromTo("#{sid}-el", {{x: 420, y: 260}}, {{x: 0, y: 0, duration: {du - 0.6:.2f}, ease: "power2.out"}}, {st});')
                for i in range(12):
                    anim.append(f'tl.fromTo("#{sid}-k{i}", {{opacity: 0, y: 0}}, {{opacity: 1, y: {-120 - (i % 4) * 40}, duration: 1.0, ease: "power1.out"}}, {st + 0.3 + i * 0.12:.3f});')
            else:
                anim.append(f'tl.set("#{sid}-el", {{x: 700, y: 400}}, {st});')
            if s.get('flash'):
                fl = round(st + du - 0.45, 3)
                body.append(f'<div id="{sid}-parlama" class="clip flash" data-start="{fl}" data-duration="1.2"></div>')
                anim.append(f'tl.fromTo("#{sid}-parlama", {{opacity: 0}}, {{opacity: 1, duration: 0.4, ease: "power2.in"}}, {fl});')
                anim.append(f'tl.to("#{sid}-parlama", {{opacity: 0, duration: 0.8, ease: "power2.out"}}, {fl + 0.4:.3f});')
                sfx.append(('whoosh', fl - 0.6))
        elif kind == 'jars':
            shot_div(sid, st, du, jars_closeup(sid, labels=s.get('labels', False)), width=1400, extra='<div class="glow"></div>')
            if s.get('labels'):
                anim.append(f'tl.fromTo("#{sid}-w", {{x: -320, scale: 1.0}}, {{x: -340, scale: 1.04, duration: {du}, ease: "sine.inOut"}}, {st});')
            else:
                anim.append(f'tl.fromTo("#{sid}-w", {{x: 0, scale: 1.05}}, {{x: -320, scale: 1.12, duration: {du}, ease: "sine.inOut"}}, {st});')
            if s.get('glow'):
                li = info[s['line']]
                for gi, wname in zip((2, 0, 1), ('Söğüt', 'kekik', 'bal')):
                    at = find_word(li['file'], wname) if li['file'] else None
                    at = line_start[s['line']] + (at if at is not None else ('Söğüt', 'kekik', 'bal').index(wname) * 1.0)
                    anim.append(f'tl.fromTo("#{sid}-glow{gi}", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {at:.3f});')
            for i in range(14):
                anim.append(f'tl.to("#{sid}-toz{i}", {{y: {-60 - (i % 4) * 20}, x: {(i % 3 - 1) * 30}, duration: {du}, ease: "none"}}, {st});')
        elif kind == 'window':
            shot_div(sid, st, du, window_view(sid))
            anim.append(f'tl.fromTo("#{sid}-w", {{scale: 1.0, x: 0, y: 0}}, {{scale: 1.08, x: -43, y: -60, duration: {du}, ease: "sine.inOut"}}, {st});')
            anim.append(f'tl.to("#{sid}-kayik", {{x: 140, duration: {du}, ease: "none"}}, {st});')
            for i in range(3):
                anim.append(f'tl.to("#{sid}-kus{i}", {{x: {120 + i * 30}, y: {-40 - i * 10}, duration: {du}, ease: "none"}}, {st});')
        elif kind == 'bowl':
            shot_div(sid, st, du, bowl_closeup(sid))
            anim.append(f'tl.fromTo("#{sid}-w", {{scale: 1.0, x: 0, y: 0}}, {{scale: 1.15, x: -81, y: -144, duration: {du}, ease: "sine.inOut"}}, {st});')
            anim.append(f'tl.fromTo("#{sid}-yansima", {{opacity: 0}}, {{opacity: 0.8, duration: 1.2}}, {st + 0.3:.3f});')
            for i in range(4):
                anim.append(f'tl.fromTo("#{sid}-hal{i}", {{opacity: 0.7, scale: 0.6, svgOrigin: "540 960"}}, {{opacity: 0, scale: 1.4, duration: 1.6, repeat: {max(1, int(du / 1.6))}}}, {st + i * 0.4:.3f});')

    subs = []
    for k, ts in line_start.items():
        li = info[k]
        subs.append(f'<div class="clip sub" data-start="{ts}" data-duration="{round(li["dur"] + 0.15, 3)}"><span>{li["text"]}</span></div>')

    html = TEMPLATE.format(TOTAL=total, BODY=''.join(body), SUBS=''.join(subs), INIT='\n'.join(sanat.INIT), ANIM='\n'.join(anim))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'index.html'), 'w') as f:
        f.write(html)
    timing = dict(total=total, sfx=sfx,
                  lines={k: dict(start=line_start[k], file=info[k]['file'], dur=info[k]['dur']) for k in line_start},
                  shots=[dict(id=s['id'], start=s['start'], dur=s['dur']) for s in shots])
    with open(os.path.join(out_dir, 'zamanlama.json'), 'w') as f:
        json.dump(timing, f, indent=1, ensure_ascii=False)
    print(f'{ep_name}: {total}s, {len(shots)} çekim, {len(anim)} animasyon satırı')
    if missing:
        print('  eksik ses (tahmini süre):', ', '.join(missing))
    return timing


TEMPLATE = '''<!doctype html>
<html lang="tr" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family: "Cinzel"; font-weight: 700; src: url(fonts/cinzel-latin.woff2) format("woff2"); unicode-range: U+0000-00FF, U+2010-2027; }}
@font-face {{ font-family: "Cinzel"; font-weight: 700; src: url(fonts/cinzel-latinext.woff2) format("woff2"); unicode-range: U+0100-024F, U+1E00-1EFF; }}
@font-face {{ font-family: "Nunito"; font-style: italic; font-weight: 800; src: url(fonts/nunito-latin.woff2) format("woff2"); unicode-range: U+0000-00FF, U+2010-2027; }}
@font-face {{ font-family: "Nunito"; font-style: italic; font-weight: 800; src: url(fonts/nunito-latinext.woff2) format("woff2"); unicode-range: U+0100-024F, U+1E00-1EFF; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #120B07; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
.clip {{ position: absolute; inset: 0; }}
.shot {{ overflow: hidden; background: #E6D2AE; }}
.world {{ position: absolute; left: 0; top: 0; height: 1920px; transform-origin: 0 0; }}
.world svg {{ display: block; }}
.vignette {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(40,20,8,.45) 100%); }}
.glow {{ position: absolute; inset: 0; background: radial-gradient(circle at 70% 25%, rgba(255,226,160,.35), transparent 60%); }}
.flash {{ background: radial-gradient(circle at 50% 60%, #FFFFFF 0%, #FFF4D6 60%, #FFE3A0 100%); z-index: 20; opacity: 0; }}
.flashred {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 50%, transparent 30%, rgba(160,20,10,.9) 100%); }}
.card {{ background: radial-gradient(ellipse at 50% 45%, #3A2416 0%, #120B07 75%); display: flex; align-items: center; justify-content: center; }}
.card-in {{ text-align: center; color: #E8C987; font-family: "Cinzel", serif; padding: 0 80px; }}
.title {{ font-size: 120px; line-height: 1.05; letter-spacing: .04em; text-shadow: 0 4px 30px rgba(0,0,0,.6); }}
.title.sm {{ font-size: 64px; margin-top: 24px; }}
.ornament {{ font-size: 48px; margin-bottom: 24px; opacity: .8; }}
.rule {{ width: 360px; height: 3px; margin: 40px auto 28px; background: linear-gradient(90deg, transparent, #C9A55A, transparent); }}
.subtitle {{ font-size: 44px; letter-spacing: .18em; }}
.small {{ font-family: "Nunito", sans-serif; font-style: italic; font-weight: 800; font-size: 38px; margin-top: 26px; color: #CDB894; }}
.small.big {{ font-size: 60px; color: #E8C987; }}
.hook {{ position: absolute; left: 0; right: 0; top: 190px; text-align: center; font-family: "Nunito", sans-serif; font-style: italic;
  font-weight: 800; color: #fff; z-index: 12; transform-origin: 50% 50%; padding: 0 40px;
  text-shadow: 0 0 3px #000, 0 4px 0 rgba(0,0,0,.7), 0 0 30px rgba(0,0,0,.8); }}
.hook .h1 {{ font-size: 84px; line-height: 1.1; }}
.hook .h2 {{ font-size: 76px; line-height: 1.15; }}
.hook b {{ font-weight: 800; }}
.sub {{ display: flex; justify-content: center; align-items: flex-start; padding: 0 70px; top: 1390px; height: 300px; bottom: auto; z-index: 10; }}
.sub span {{ font-family: "Nunito", sans-serif; font-style: italic; font-weight: 800; font-size: 50px; line-height: 1.25;
  color: #FFFFFF; text-align: center; text-shadow: 0 3px 0 rgba(0,0,0,.55), 0 0 18px rgba(0,0,0,.6), 0 0 4px rgba(0,0,0,.9); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{BODY}
{SUBS}
</div>
<script>
{INIT}
const tl = gsap.timeline({{ paused: true }});
{ANIM}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
'''

if __name__ == '__main__':
    for name in sys.argv[1:] or ['bolum1']:
        build(name)
