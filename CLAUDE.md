# Proje notları

## Seslendirme kuralı

- **Tüm hikâyeler ve yeni bölümler VoxCPM2 ile seslendirilir** (`openbmb/VoxCPM2`, Apache-2.0, Türkçe + duygu talimatı).
- Araç: `tts/hikaye_seslendir.py`. Senaryo biçimi dosyanın başında ve `tts/ornek_hikaye.txt` içinde.
  ```bash
  /opt/voxcpm/bin/python tts/hikaye_seslendir.py senaryo.txt -o bolum.mp3
  ```
- Karakter sesleri `tts/sesler/<ad>.wav` içinde saklanır ve her bölümde aynen kullanılır; karakterin sesi değişmesin diye bu dosyaları silmeyin/değiştirmeyin (yeni ses isteniyorsa silin).
- Her replik Whisper ile kontrol edilir ve birebir tutana kadar yeniden üretilir. "KONTROL ET" çıkan replikleri kullanıcıya bildirin.
- Fısıltı için `[fısıltı]` kullanın (net telaffuzlu tarif içerir); çıplak "whispering" tarifi kelimeleri yutabiliyor.
- Botun `/ses` komutu (hızlı, kısa yanıtlar) OmniVoice ile çalışır: `plugin/OmniVoiceTTS.js`.
