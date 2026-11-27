#!/usr/bin/env python3
"""Seslendirme düzenleyici: replikleri birbirine benzer hız ve seviyeye getirir.

1. Baştaki/sondaki sessizliği atar, cümle içindeki uzun boşlukları ~0.45 sn'ye kısaltır.
2. Konuşma hızını (hece/sn) karakterin olağan hızının makul bandına çeker
   (perdeyi değiştirmeden atempo ile, en fazla %15 yavaşlatma / %20 hızlandırma).
3. Aynı tını: highpass/lowpass + hafif kompresör + duyguya göre hedef seviye (loudnorm).

Kullanım (tek dosya): duzen.py giris.wav cikis.wav "metin" karakter "stil"
"""
import json
import re
import subprocess
import sys

# 1. sezon VoxCPM2 ölçümlerinden karakterlerin olağan hızı (hece/sn)
HIZ = {'ayse': 5.2, 'ayseg': 4.9, 'hekim': 5.1, 'huseyin': 4.9, 'kadi': 4.6, 'yusuf': 5.3,
       'riza': 5.2, 'denizci': 4.7, 'fatma': 5.0, 'zehra': 5.0, 'leyla': 4.4, 'mehmet': 4.6, 'subasi': 4.8, 'kemal': 4.8}
UNLU = set('aeıioöuüâîû')
SESSIZLIK = ('silenceremove=start_periods=1:start_threshold=-45dB,'
             'silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-42dB:stop_silence=0.45,'
             'areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse')


def hece(metin):
    return max(1, sum(c in UNLU for c in metin.lower()))


def sure(f):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                         capture_output=True, text=True).stdout
    return float(out)


def hedef_lufs(stil):
    s = (stil or '').lower()
    if any(w in s for w in ('whisper', 'quiet', 'soft', 'weak', 'sleepy', 'praying', 'to himself')):
        return -22.5
    if any(w in s for w in ('angry', 'shout', 'loud', 'commanding', 'panick', 'urgent', 'calling')):
        return -19
    return -20


def hiz_bandi(kim, stil):
    h = HIZ.get(kim, 5.0)
    s = (stil or '').lower()
    if any(w in s for w in ('slow', 'whisper', 'tired', 'weak', 'solemn', 'narration', 'crying', 'tears')):
        h *= 0.88
    elif any(w in s for w in ('fast', 'panick', 'urgent', 'excited', 'out of breath')):
        h *= 1.1
    return h * 0.85, h * 1.15


def duzenle(giris, cikis, metin, kim, stil, sr=24000):
    ara = cikis + '.ara.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', giris, '-af', SESSIZLIK, '-ac', '1', ara], check=True)
    hiz = hece(metin) / max(0.3, sure(ara))
    alt, ust = hiz_bandi(kim, stil)
    tempo = 1.0
    if hiz < alt:
        tempo = min(1.2, alt / hiz)
    elif hiz > ust:
        tempo = max(0.85, ust / hiz)
    zincir = (f'atempo={tempo:.3f},' if abs(tempo - 1) > 0.02 else '') + \
        'highpass=f=80,lowpass=f=11000,acompressor=threshold=-24dB:ratio=2.5:attack=5:release=90:makeup=2,' \
        f'loudnorm=I={hedef_lufs(stil)}:TP=-2:LRA=7,aresample={sr}'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', ara, '-af', zincir, '-ac', '1', cikis], check=True)
    subprocess.run(['rm', '-f', ara])
    return round(hiz, 1), round(tempo, 2)


if __name__ == '__main__':
    g, c, metin, kim = sys.argv[1:5]
    print(duzenle(g, c, metin, kim, sys.argv[5] if len(sys.argv) > 5 else ''))
