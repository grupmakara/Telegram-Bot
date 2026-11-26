# **Heroku'da Webhook İle Çalışan Deneysel Bir Bot**

**Nasıl Çalışır ?**

_.env dosyasını açıp @BotFather'dan aldığınız tokeni BOT_API yerine yapıştırın ve Heroku'dan aldığınız bağlantıyı URL yerine yapıştırın._

Detaylı Bilgi İçin: https://telegra.ph/KENDİ-TELEGRAM-BOTUNUZU-YAPIN-09-11

## Video Komutları

| Komut | Açıklama |
|---|---|
| `/indir <bağlantı>` | Videoyu yt-dlp ile indirip sohbete gönderir (en fazla 50 MB). |
| `/altyazi` | Bir video veya ses mesajına yanıt olarak yazılır; Whisper ile `.srt` altyazı çıkarır ve altyazısı gömülü videoyu gönderir. |
| `/altyazi <bağlantı>` | Bağlantıdaki videonun altyazısını çıkarır. |
| `/altyazi tr` | Dili belirtir (belirtilmezse otomatik algılanır). |

İşler sırayla çalıştırılır. Telegram, botların en fazla 20 MB dosya indirmesine izin verir; daha büyük videolar için bağlantı kullanın.

**Sunucuda kurulu olması gerekenler:** `ffmpeg`, `yt-dlp` ve `whisper` (`pip install yt-dlp openai-whisper`).

**İsteğe bağlı ayarlar (.env):**

- `WHISPER_MODEL`: Whisper modeli (varsayılan `base`; `small` daha doğru ama daha yavaş).
- `MAX_SUBTITLE_MINUTES`: Altyazı çıkarılacak en uzun kayıt süresi (varsayılan 10).
- `MAX_UPLOAD_MB`: Gönderilecek en büyük dosya boyutu (varsayılan 50).
- `MAX_MEDIA_QUEUE`: Sırada bekleyebilecek en fazla iş (varsayılan 5).
