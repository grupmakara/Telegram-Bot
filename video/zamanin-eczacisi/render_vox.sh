#!/bin/bash
# Sesler hazırken yalnızca render + miks (VoxCPM2 sesleri, ses6/). Kullanım: ./render_vox.sh 5 6 7 8
cd "$(dirname "$0")"
for e in "$@"; do
  # 2 dakikanın altında kalırsa replik sonrası nefes payını artır
  for pad in 0.6 0.75 0.9 1.05 1.2; do
    SES_DIR=ses6 PAD_OUT=$pad python3 motor.py bolum$e 2>&1 | grep -v -i warn
    python3 -c "import json,sys; sys.exit(json.load(open('proje$e/zamanlama.json'))['total'] < 121)" && break
  done
  (cd proje$e && rm -rf .hyperframes/artifacts && npx --yes hyperframes render -o ../sessiz$e.mp4 2>&1 | grep -E 'rendered in|rror')
  python3 miks.py proje$e sessiz$e.mp4 cikti/zamanin-eczacisi-bolum$e.mp4 && echo "HAZIR: cikti/zamanin-eczacisi-bolum$e.mp4"
done
echo BITTI
