# Zamanın Eczacısı — animasyon dizisi üretim hattı

2D kukla tarzı, dikey (1080×1920) Türkçe animasyon bölümleri. Görseller SVG olarak koddan çizilir,
HyperFrames ile render edilir; seslendirme Gemini TTS ile yapılır.

| Dosya | Görev |
|---|---|
| `sanat.py` | Karakterler (Elif/Ayşe, Hüseyin, Hekim, Kadı…) ve mekânlar (dükkân, oda, mahkeme, liman, sokak…) |
| `motor.py` | Senaryoyu çekimlere çevirir: kamera, ağız senkronu, göz kırpma, altyazı, kanca → `projeN/index.html` |
| `bolumN.py` | Bölüm senaryosu: replikler, duygu yönlendirmeleri, çekim listesi |
| `gem_uret.py` | Gemini TTS ile eksik replikleri üretir (kota dolunca sonraki modele geçer) |
| `dogrula.py` | Replikleri Whisper ile senaryoya karşı kontrol eder |
| `miks.py` / `muzik.py` | Ses miksajı / özgün telifsiz fon müziği |
| `gunluk.sh` | Günlük otomatik üretim (seslendir → doğrula → render → `cikti/`) |

Gereken: ffmpeg, hyperframes (npm), openai-whisper, numpy ve `generativelanguage.googleapis.com`
için `x-goog-api-key` başlığıyla tanımlı bir ağ gizli anahtarı.

```bash
./gunluk.sh            # bugünkü kota kadar üret, hazır bölümleri cikti/ içine yaz
python3 motor.py bolum4  # tek bölümü derle
```

`ses_elevenlabs/` Bölüm 1–2'nin yayınlanan ElevenLabs seslerini, `ses4/` Gemini seslerini içerir.
