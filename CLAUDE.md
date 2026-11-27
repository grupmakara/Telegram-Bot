# Proje notları

## Seslendirme kuralı

- **Tüm hikâyeler ve yeni bölümler `--motor ikisi` (varsayılan) ile seslendirilir:** her replik hem Gemini 3.1 Flash TTS (`gemini-3.1-flash-tts-preview`) hem VoxCPM2 (VoiceStudio motoru, `openbmb/VoxCPM2`, Apache-2.0) ile üretilir; Whisper'ın daha doğru bulduğu kalır, eşitlikte Gemini.
- Gemini ücretsiz kotası **günde 10 istek**; dolunca araç kalan replikleri kendiliğinden VoxCPM2 ile bitirir. Bunu kullanıcıya bildirin.
- Araç: `tts/hikaye_seslendir.py`. Senaryo biçimi dosyanın başında ve `tts/ornek_hikaye.txt` içinde.
  ```bash
  /opt/voxcpm/bin/python tts/hikaye_seslendir.py senaryo.txt -o bolum.mp3
  ```
- Karakter sesleri `tts/sesler/` içinde saklanır (Gemini eşlemesi `gemini_sesler.json`, VoxCPM2 sesleri `<ad>.wav`) ve her bölümde aynen kullanılır; karakterin sesi değişmesin diye bu dosyaları silmeyin/değiştirmeyin (yeni ses isteniyorsa silin).
- Her replik Whisper ile kontrol edilir ve birebir tutana kadar yeniden üretilir. "KONTROL ET" çıkan replikleri kullanıcıya bildirin.
- Fısıltı için `[fısıltı]` kullanın (net telaffuzlu tarif içerir); çıplak "whispering" tarifi kelimeleri yutabiliyor.
- Botun `/ses` komutu (hızlı, kısa yanıtlar) OmniVoice ile çalışır: `plugin/OmniVoiceTTS.js`.
