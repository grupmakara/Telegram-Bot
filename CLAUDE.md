# Proje notları

## Seslendirme kuralı

- **Bütün oturumlarda ve bütün dizilerde (Bodrum Kattaki Adam, Zamanın Eczacısı ve sonrakiler) seslendirme `tts/hikaye_seslendir.py` aracıyla yapılır.** Kendi ayrı seslendirme betiğinizi yazmayın; aracın eksik bir özelliği varsa araca ekleyin.
- Dizinin daha önce tasarlanmış karakter sesleri varsa (ör. `video/zamanin-eczacisi/referans/<karakter>.wav`), seslerin değişmemesi için bunları aynı karakter adıyla `tts/sesler/` altına kopyalayın; araç yoksa yeni ses tasarlar.
- Senaryo başka biçimdeyse (`bolumN.py`, `.json`) önce aracın düz metin biçimine çevirin: `@karakter: ses tarifi` ve `karakter [duygu]: metin`.
- **Tüm hikâyeler ve yeni bölümler VoxCPM2 ile seslendirilir** (VoiceStudio motoru, `openbmb/VoxCPM2`, Apache-2.0, yerel ve tamamen ücretsiz). Kullanıcı tamamen ücretsiz olanı istedi; bu aracın varsayılan motorudur (`--motor voxcpm`).
- Gemini 3.1 Flash TTS (`--motor gemini` / `ikisi`) sadece kullanıcı açıkça isterse kullanılır; ücretsiz kotası günde 10 istektir.
- Araç: `tts/hikaye_seslendir.py`. Senaryo biçimi dosyanın başında ve `tts/ornek_hikaye.txt` içinde.
  ```bash
  /opt/voxcpm/bin/python tts/hikaye_seslendir.py senaryo.txt -o bolum.mp3
  ```
- Karakter sesleri `tts/sesler/` içinde saklanır (Gemini eşlemesi `gemini_sesler.json`, VoxCPM2 sesleri `<ad>.wav`) ve her bölümde aynen kullanılır; karakterin sesi değişmesin diye bu dosyaları silmeyin/değiştirmeyin (yeni ses isteniyorsa silin).
- Her replik Whisper ile kontrol edilir ve birebir tutana kadar yeniden üretilir. "KONTROL ET" çıkan replikleri kullanıcıya bildirin.
- Fısıltı için `[fısıltı]` kullanın (net telaffuzlu tarif içerir); çıplak "whispering" tarifi kelimeleri yutabiliyor.
- Botun `/ses` komutu (hızlı, kısa yanıtlar) OmniVoice ile çalışır: `plugin/OmniVoiceTTS.js`.
