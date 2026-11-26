#!/bin/bash
# Günlük üretim: Gemini ücretsiz kotasıyla eksik replikleri seslendirir, doğrular,
# sesleri tamamlanan ve henüz teslim edilmemiş bölümleri render edip cikti/ klasörüne yazar.
# Yeni hazırlanan bölümler "YENI: cikti/....mp4" satırıyla bildirilir.
cd "$(dirname "$0")"
BOLUMLER="bolum3 bolum4 bolum5 bolum6 bolum7 bolum8"
./hazirla.sh
python3 -u gem_uret.py $BOLUMLER
python3 -u dogrula.py $BOLUMLER 2>/dev/null > dogrula.log
kotu=$(grep "YENİDEN ÜRETİLECEK" dogrula.log | sed 's/.*: //')
if [ -n "$kotu" ] && [ "$kotu" != "yok" ]; then
  for f in $kotu; do echo "$f" >> yeniden.log; c=$(grep -c "^$f$" yeniden.log); [ "$c" -le 2 ] && rm -f ses4/$f; done
  python3 -u gem_uret.py $BOLUMLER
fi
for e in 3 4 5 6 7 8; do
  [ -f teslim/bolum$e ] && continue
  python3 - <<PY || continue
import importlib, os, sys
m = importlib.import_module('bolum$e')
sys.exit(0 if all(os.path.exists(os.path.join('ses4', v[0])) for v in m.LINES.values() if len(v) >= 5) else 1)
PY
  python3 motor.py bolum$e 2>&1 | grep -v -i warn
  (cd proje$e && rm -rf .hyperframes/artifacts && npx --yes hyperframes render -o ../sessiz$e.mp4 2>&1 | grep -E 'rendered in|rror')
  python3 miks.py proje$e sessiz$e.mp4 cikti/zamanin-eczacisi-bolum$e.mp4 && touch teslim/bolum$e && echo "YENI: cikti/zamanin-eczacisi-bolum$e.mp4"
done
echo "GUNLUK BITTI"
