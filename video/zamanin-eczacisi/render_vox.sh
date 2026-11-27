#!/bin/bash
# Sesler hazırken yalnızca render + miks (VoxCPM2 sesleri, ses6/). Kullanım: ./render_vox.sh 5 6 7 8
cd "$(dirname "$0")"
for e in "$@"; do
  SES_DIR=ses6 python3 motor.py bolum$e 2>&1 | grep -v -i warn
  (cd proje$e && rm -rf .hyperframes/artifacts && npx --yes hyperframes render -o ../sessiz$e.mp4 2>&1 | grep -E 'rendered in|rror')
  python3 miks.py proje$e sessiz$e.mp4 cikti/zamanin-eczacisi-bolum$e.mp4 && echo "HAZIR: cikti/zamanin-eczacisi-bolum$e.mp4"
done
echo BITTI
