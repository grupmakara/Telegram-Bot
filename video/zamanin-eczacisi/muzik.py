#!/usr/bin/env python3
"""Özgün fon müziği: Hicaz makamında ud benzeri telli + dem (drone) + ney benzeri üfleme + def.
Tamamen sentez (Karplus-Strong ve sinüs), telifsiz. Çıktı: ses2/muzik.wav (döngüye uygun, 64 sn).
"""
import os
import subprocess

import numpy as np

SR = 44100
BPM = 76
BEAT = 60 / BPM
BARS = 20                       # 4/4, ~63 sn
L = int(SR * BEAT * 4 * BARS)
rng = np.random.default_rng(1665)

# Re Hicaz: Re Mi♭ Fa# Sol La Si♭ Do Re (yaklaşık, 12-TET)
SCALE = [0, 1, 4, 5, 7, 8, 10, 12]
BASE = 146.83                    # D3


def hz(step, octave=0):
    o, i = divmod(step, len(SCALE))
    return BASE * 2 ** ((SCALE[i] + 12 * (o + octave)) / 12)


def pluck(freq, dur, bright=0.5):
    n = int(SR * dur)
    period = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, period) * 0.8
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % period]
        nxt = buf[(i + 1) % period]
        buf[i % period] = (0.5 + bright * 0.004) * (out[i] + nxt) * 0.996
    env = np.minimum(1, np.arange(n) / (0.004 * SR))
    return out * env


def add(track, sig, t):
    i = int(t * SR)
    j = min(len(track), i + len(sig))
    track[i:j] += sig[:j - i]


music = np.zeros(L)
t_axis = np.arange(L) / SR

# dem: Re + La, yavaş titreşimli
drone = (np.sin(2 * np.pi * 73.42 * t_axis) * 0.5 + np.sin(2 * np.pi * 110.0 * t_axis) * 0.3
         + np.sin(2 * np.pi * 146.83 * t_axis) * 0.15)
drone *= 0.18 * (1 + 0.15 * np.sin(2 * np.pi * 0.11 * t_axis))
music += drone

# ud: makam içinde dolaşan ezgi, 2 ölçülük cümleler, cümle sonunda duraklama
step = 4
for bar in range(BARS):
    phrase_end = bar % 4 == 3
    for k in range(8):
        if phrase_end and k >= 4:
            break
        if rng.random() < 0.22:
            continue
        step = int(np.clip(step + rng.choice([-2, -1, -1, 0, 1, 1, 2]), 0, 10))
        if phrase_end and k == 3:
            step = 0 if bar % 8 == 7 else 4  # karar sesi (Re) / güçlü (La)
        dur = BEAT / 2 * (3 if phrase_end and k == 3 else 1.6)
        t0 = (bar * 4 + k / 2) * BEAT
        add(music, pluck(hz(step), dur + 0.6) * (0.55 if k % 2 == 0 else 0.4), t0)

# ney benzeri uzun üfleme notaları (4 ölçüde bir)
for bar in range(2, BARS, 4):
    f = hz([7, 4, 5, 2][(bar // 4) % 4], 0)
    n = int(SR * BEAT * 6)
    tt = np.arange(n) / SR
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.2 * tt)
    tone = np.sin(2 * np.pi * f * 2 * np.cumsum(vib) / SR) * 0.5 + np.sin(4 * np.pi * f * 2 * np.cumsum(vib) / SR) * 0.08
    breath = np.convolve(rng.normal(0, 1, n), np.ones(30) / 30, 'same') * 0.05
    env = np.sin(np.pi * np.minimum(1, tt / tt[-1])) ** 1.5
    add(music, (tone + breath) * env * 0.16, bar * 4 * BEAT)

# def: düm (1, 3) ve tek (2.5, 4)
for bar in range(BARS):
    for beat, kind in ((0, 'dum'), (1.5, 'tek'), (2, 'dum'), (3, 'tek'), (3.5, 'tek')):
        n = int(SR * 0.35)
        tt = np.arange(n) / SR
        if kind == 'dum':
            s = np.sin(2 * np.pi * (60 + 50 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9) * 0.35
        else:
            s = np.convolve(rng.normal(0, 1, n), [1, -1], 'same') * np.exp(-tt * 40) * 0.05
        add(music, s, (bar * 4 + beat) * BEAT)

# döngü için uçları yumuşat, normalize et
fade = int(SR * 1.0)
music[:fade] *= np.linspace(0, 1, fade)
music[-fade:] *= np.linspace(1, 0, fade)
music = music / np.max(np.abs(music)) * 0.8

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'muzik.wav')
raw = out + '.raw.wav'
pcm = (music * 32767).astype(np.int16)
import wave
with wave.open(raw, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
# hafif oda yankısı ve stereo genişlik
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af',
                'aecho=0.8:0.6:60|130:0.25|0.15,highpass=f=50,lowpass=f=9000,loudnorm=I=-20:TP=-2,aformat=channel_layouts=stereo',
                out], check=True)
os.remove(raw)
print(out, round(L / SR, 1), 's')
