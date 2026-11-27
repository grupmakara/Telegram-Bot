#!/bin/bash
# Chatterbox ile seslendir -> Whisper ile doğrula -> hatalıları yeniden üret (en fazla 3 tur) -> render + miks
# Kullanım: ./uret.sh 3 4 5 6
cd "$(dirname "$0")"; export HF_HUB_DISABLE_XET=1
B=""; for e in "$@"; do B="$B bolum$e"; done
./hazirla.sh
for tur in 0 1 2 3; do
  SEED_EK=$((tur * 101)) /opt/tts/bin/python -u cb_uret.py $B
  python3 -u dogrula.py $B 2>/dev/null > dogrula_tur$tur.log
  kotu=$(grep "YENİDEN ÜRETİLECEK" dogrula_tur$tur.log | sed 's/.*: //')
  echo "tur $tur: $kotu"
  [ "$kotu" = "yok" ] && break
  [ $tur -lt 3 ] && for f in $kotu; do rm -f ses5/$f; done
done
for e in "$@"; do
  python3 motor.py bolum$e 2>&1 | grep -v -i warn
  (cd proje$e && rm -rf .hyperframes/artifacts && npx --yes hyperframes render -o ../sessiz$e.mp4 2>&1 | grep -E 'rendered in|rror')
  python3 miks.py proje$e sessiz$e.mp4 cikti/zamanin-eczacisi-bolum$e.mp4 && echo "HAZIR: cikti/zamanin-eczacisi-bolum$e.mp4"
done
echo BITTI
