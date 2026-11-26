# **Telegram Botu**

## Kurulum

1. `.env.example` dosyasını `.env` adıyla kopyalayın ve @BotFather'dan aldığınız tokeni `BOT_API` satırına yazın.
2. `URL` boş bırakılırsa bot **polling** modunda çalışır; domain veya HTTPS gerekmez. Webhook kullanmak için `URL`'e botun herkese açık `https://` adresini yazın.

> `.env` dosyası token içerdiği için depoya eklenmez (`.gitignore`).

### Docker ile (önerilen; video komutları için gerekli)

Video komutları FFmpeg, yt-dlp ve Whisper gerektirir. Bunların hepsi Docker imajında kuruludur:

```bash
docker compose up -d --build
docker compose logs -f
```

Sunucuda en az 2 GB RAM ve yaklaşık 5 GB disk olmalıdır. Daha doğru altyazı için imajı `docker compose build --build-arg WHISPER_MODEL=small` ile derleyip `.env` içinde `WHISPER_MODEL=small` yazın.

### Docker olmadan

```bash
npm install
pip install yt-dlp openai-whisper   # ffmpeg ayrıca kurulmalı (ör. apt install ffmpeg)
npm start
```

> Heroku'da video komutları çalışmaz: Whisper, Heroku'nun 500 MB'lık uygulama boyutu sınırını aşar.

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
