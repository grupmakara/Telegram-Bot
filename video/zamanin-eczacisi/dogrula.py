#!/usr/bin/env python3
"""Üretilen replikleri Whisper ile yazıya döker ve senaryo metniyle karşılaştırır.
Kullanım: python3 dogrula.py bolum1 [bolum2 ...]   -> benzerliği düşük olanları listeler
"""
import difflib
import importlib
import json
import os
import re
import sys

import whisper

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
SES = os.path.join(ROOT, os.environ.get('SES_DIR', 'ses5'))
CACHE = os.path.join(ROOT, 'kontrol5', 'dogrulama.json')
os.makedirs(os.path.dirname(CACHE), exist_ok=True)
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
model = whisper.load_model('small')


def norm(s):
    s = s.lower().replace('â', 'a').replace('î', 'i').replace('û', 'u')
    s = re.sub(r'[^a-zçğıöşü0-9 ]', ' ', s)
    return ' '.join(s.split())


bad = []
for ep in sys.argv[1:]:
    mod = importlib.import_module(ep)
    for key, spec in mod.LINES.items():
        f = os.path.join(SES, spec[0])
        if not os.path.exists(f):
            continue
        st = os.stat(f)
        ck = f'{spec[0]}:{st.st_mtime}'
        if ck not in cache:
            cache[ck] = model.transcribe(f, language='tr', fp16=False)['text'].strip()
            json.dump(cache, open(CACHE, 'w'), ensure_ascii=False, indent=0)
        got = cache[ck]
        ratio = difflib.SequenceMatcher(None, norm(spec[2]), norm(got)).ratio()
        flag = 'TAMAM' if ratio >= 0.8 else 'KÖTÜ'
        if ratio < 0.8:
            bad.append(spec[0])
        print(f'{flag} {ratio:.2f} {spec[0]}: {got}', flush=True)
print('YENİDEN ÜRETİLECEK:', ' '.join(bad) if bad else 'yok')
