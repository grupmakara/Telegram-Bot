#!/bin/bash
# Bölüm klasörlerini (HyperFrames projeleri) şablondan oluşturur, fon müziğini üretir.
cd "$(dirname "$0")"
for e in $(seq 1 16); do [ -d proje$e ] || cp -r sablon proje$e; done
[ -f muzik.wav ] || python3 muzik.py
mkdir -p cikti teslim
