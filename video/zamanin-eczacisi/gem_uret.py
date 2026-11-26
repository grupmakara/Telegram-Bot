#!/usr/bin/env python3
"""Gemini TTS ile seslendirme (ücretsiz katman, günlük kota). Eksik replikleri sırayla üretir;
bir modelin günlük kotası dolunca sıradakine geçer, hepsi dolunca durur.
Kullanım: gem_uret.py bolum3 bolum4 ...   Çıkış kodu: 0 = hepsi tamam, 3 = kota bitti (yarın devam)
"""
import importlib, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemini_tts import synth, KotaDoldu

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'ses4')
MODELLER = ['gemini-3.8-flash-lite-tts', 'gemini-3.8-flash-tts', 'gemini-3.1-flash-tts-preview', 'gemini-2.5-flash-preview-tts']
SES = {'ayse': 'Leda', 'huseyin': 'Achird', 'fatma': 'Sulafat', 'mehmet': 'Laomedeia', 'leyla': 'Zephyr',
       'hekim': 'Alnilam', 'subasi': 'Orus', 'zehra': 'Gacrux', 'riza': 'Algenib', 'kadi': 'Rasalgethi',
       'denizci': 'Fenrir', 'yusuf': 'Puck', 'ayseg': 'Despina'}
KIM = {'ayse': 'a young woman in her twenties', 'huseyin': 'a warm middle-aged father', 'fatma': 'a mother in her forties',
       'mehmet': 'a sick eight-year-old boy', 'leyla': 'a twelve-year-old girl', 'hekim': 'a proud, stern physician in his fifties',
       'subasi': 'a stern guard officer', 'zehra': 'a kind elderly grandmother', 'riza': 'a tired working man with a hoarse voice',
       'kadi': 'an old, wise judge', 'denizci': 'a rough sea captain', 'yusuf': 'a shy young apprentice', 'ayseg': 'a shy young woman'}


def yumusat(style):
    s = style or 'natural, conversational'
    s = re.sub(r'\bshouting\b|\bloud\b|\bvery emotional\b', 'raised voice, intense but not screaming', s)
    return s


def hedef_lufs(style):
    s = (style or '').lower()
    if any(w in s for w in ('whisper', 'quiet', 'soft', 'weak', 'sleepy', 'praying', 'to himself')):
        return -25
    if any(w in s for w in ('angry', 'raised', 'commanding', 'panick', 'urgent', 'shock')):
        return -18
    return -20


kota = set()
eksik = 0
for ep in sys.argv[1:]:
    mod = importlib.import_module(ep)
    stil_tablo = getattr(importlib.import_module('vox_uret_stil'), 'STYLE', {}) if os.path.exists(os.path.join(ROOT, 'vox_uret_stil.py')) else {}
    for key, spec in mod.LINES.items():
        if len(spec) < 5:
            continue
        fname, who, text = spec[0], spec[1], spec[2]
        dst = os.path.join(OUT, fname)
        if os.path.exists(dst):
            continue
        style = yumusat((spec[5] if len(spec) > 5 else None) or stil_tablo.get(fname))
        direction = f'{KIM[who]}, speaking Turkish naturally; {style}'
        raw = dst + '.raw.wav'
        os.makedirs(OUT, exist_ok=True)
        ok = False
        for m in MODELLER:
            if m in kota:
                continue
            try:
                synth(text.replace('"', ''), SES[who], direction, raw, model=m)
                ok = True
                print(f'{fname} {who} {m}', flush=True)
                break
            except KotaDoldu:
                kota.add(m); print(f'  kota doldu: {m}', flush=True)
            except Exception as e:
                print(f'  {fname} {m} hata: {str(e)[:160]}', flush=True)
        if not ok:
            eksik += 1
            if len(kota) == len(MODELLER):
                print('TÜM KOTALAR DOLDU', flush=True)
                sys.exit(3)
            continue
        flt = ('silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
               f'loudnorm=I={hedef_lufs(style)}:TP=-2:LRA=11,aresample=24000')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', flt, '-ac', '1', dst], check=True)
        os.remove(raw)
        time.sleep(12)
print('TAMAM' if not eksik else f'EKSİK {eksik}', flush=True)
sys.exit(0 if not eksik else 3)
