# **Heroku'da Webhook İle Çalışan Deneysel Bir Bot**

**Nasıl Çalışır ?**

_.env.example dosyasını .env adıyla kopyalayıp @BotFather'dan aldığınız tokeni BOT_API yerine yapıştırın ve Heroku'dan aldığınız bağlantıyı URL yerine yapıştırın._

Detaylı Bilgi İçin: https://telegra.ph/KENDİ-TELEGRAM-BOTUNUZU-YAPIN-09-11

## Sesli Yanıt (OmniVoice)

`/ses <metin>` yazınca bot metni Türkçe seslendirip sesli mesaj olarak gönderir. Bir mesaja yanıt olarak `/ses` yazılırsa o mesajı okur.

Seslendirme [OmniVoice](https://huggingface.co/k2-fsa/OmniVoice) (Apache-2.0, ücretsiz) ile botun çalıştığı makinede yapılır; dış API veya anahtar gerekmez.

**Kurulum** (ayrı bir Python sanal ortamı; model ~3 GB, ilk açılışta iner, ~4 GB RAM ister):

```bash
python3 -m venv /opt/omnivoice
/opt/omnivoice/bin/pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu
/opt/omnivoice/bin/pip install omnivoice
# ffmpeg de kurulu olmalı (sesli mesaj için OGG/Opus dönüşümü)
```

**Ayarlar** (`.env`):

| Değişken | Varsayılan | Açıklama |
|---|---|---|
| `OMNIVOICE_PYTHON` | `/opt/omnivoice/bin/python` | OmniVoice kurulu Python |
| `OMNIVOICE_INSTRUCT` | `female` | Ses tarifi, ör. `male`, `female, elderly`; boş bırakılırsa model seçer |
| `TTS_MAX_CHARS` | `300` | Tek istekte en fazla karakter |

Not: Heroku'nun standart dyno'ları (512 MB RAM) bu model için yetersizdir; botu en az 4 GB RAM'li bir sunucuda çalıştırın.
