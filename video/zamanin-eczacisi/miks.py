#!/usr/bin/env python3
"""Sessiz render + seslendirmeler + ses efektleri (+ varsa müzik) -> son video.

Kullanım: python3 miks.py proje1 sessiz1.mp4 cikti.mp4
"""
import json
import os
import subprocess
import sys

R = os.path.dirname(os.path.abspath(__file__))
proje, sessiz, out = sys.argv[1], sys.argv[2], sys.argv[3]
t = json.load(open(os.path.join(R, proje, 'zamanlama.json')))
music = os.path.join(R, 'muzik.wav')
total = t['total']

inputs, filters, labels = ['-i', os.path.join(R, sessiz)], [], []
n = 1
for k, li in t['lines'].items():
    if not li['file']:
        continue
    inputs += ['-i', li['file']]
    ms = int(li['start'] * 1000)
    filters.append(f'[{n}:a]aresample=48000,adelay={ms}|{ms},volume=1.6[v{n}]')
    labels.append(f'[v{n}]')
    n += 1

if os.path.exists(music):
    inputs += ['-stream_loop', '-1', '-i', music]
    # konuşma sırasında müziği kıs (sidechain yerine sabit düşük seviye + giriş/çıkış)
    filters.append(f'[{n}:a]aresample=48000,volume=0.18,afade=t=in:d=1.5,afade=t=out:st={total - 2.5}:d=2.5[m]')
else:
    inputs += ['-f', 'lavfi', '-i', f'anoisesrc=color=brown:amplitude=0.02:d={total}']
    filters.append(f'[{n}:a]lowpass=f=400,aresample=48000,afade=t=in:d=1,afade=t=out:st={total - 2}:d=2[m]')
labels.append('[m]')
n += 1

SRC = {
    'boom': ("aevalsrc='0.9*sin(2*PI*(38+60*exp(-t*6))*t)*exp(-t*3.2)+0.25*(random(0)*2-1)*exp(-t*18)':d=1.8:s=48000", 'volume=0.9'),
    'whoosh': ('anoisesrc=color=pink:amplitude=0.7:d=1.6:r=48000',
               'bandpass=f=1200:w=900,afade=t=in:d=1.0:curve=exp,afade=t=out:st=1.0:d=0.6,volume=0.9'),
    'knock': ("aevalsrc='0.8*sin(2*PI*90*t)*exp(-t*40)+0.5*(random(0)*2-1)*exp(-t*60)':d=0.4:s=48000", 'lowpass=f=900,volume=1.4'),
}
for kind, at in t.get('sfx', []):
    src, flt = SRC[kind]
    ms = max(0, int(at * 1000))
    inputs += ['-f', 'lavfi', '-i', src]
    filters.append(f'[{n}:a]{flt},adelay={ms}|{ms}[x{n}]')
    labels.append(f'[x{n}]')
    n += 1

filters.append(f'{"".join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,'
               f'atrim=0:{total},alimiter=limit=0.9[a]')
cmd = ['ffmpeg', '-y', '-v', 'error', *inputs, '-filter_complex', ';'.join(filters),
       '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
       '-movflags', '+faststart', '-shortest', os.path.join(R, out)]
subprocess.run(cmd, check=True)
print(out)
