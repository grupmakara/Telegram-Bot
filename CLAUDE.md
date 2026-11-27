# Proje notları (Claude için)

## Video üretimi: "Zamanın Eczacısı" animasyon dizisi

Hat `video/zamanin-eczacisi/` klasöründedir (ayrıntı: oradaki README.md).

### Seslendirme kuralı
- Bölüm 4'ten itibaren Türkçe seslendirme **VoxCPM2** (openbmb/VoxCPM2, Apache-2.0, ücretsiz, ticari kullanıma
  uygun) ile yapılır: `video/zamanin-eczacisi/vox_uret.py` ve `uret_vox.sh` (çıktı `ses6/`).
  Kurulum (CPU): `python3 -m venv /opt/voxcpm && /opt/voxcpm/bin/pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cpu && /opt/voxcpm/bin/pip install voxcpm==2.0.3 "torchcodec==0.7.*" num2words`
- Yedek: **Chatterbox Multilingual** (MIT): `cb_uret.py` ve `uret.sh` (çıktı `ses5/`).
- Chatterbox kurulumu: ortamın kurulum betiği Chatterbox'ı `/opt/tts` sanal ortamına kurar. Eksikse:
  `python3 -m venv /opt/tts && /opt/tts/bin/pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu && /opt/tts/bin/pip install chatterbox-tts==0.1.7 num2words`
  Model indirirken `HF_HUB_DISABLE_XET=1` gerekir.
- Karakter sesleri `video/zamanin-eczacisi/referans/<karakter>.wav` dosyalarıdır (VoxCPM2 ile tasarlanmış
  yapay Türkçe sesler). Aynı karakter her bölümde aynı referansla seslendirilir.
- Duygu yoğunluğu ölçülü tutulur (exaggeration 0.35–0.7); bağırma yok. Fısıltı/sakin replikler daha alçak
  seviyede miksajlanır.
- Her replik `dogrula.py` (Whisper) ile senaryoya karşı kontrol edilir; hatalılar farklı tohumla yeniden üretilir.
- Gerçek kişilere ait sesler (örn. ElevenLabs kütüphanesindeki sanatçı sesleri) klonlanmaz.
- Ticari kullanıma kapalı modeller (XTTS-v2/CPML, OmniVoice/CC-BY-NC vb.) kullanılmaz.

### Bölüm üretmek
```bash
cd video/zamanin-eczacisi
./uret_vox.sh 7 8    # bölüm 7 ve 8 (VoxCPM2): seslendir, doğrula, render, miksaj -> cikti/
```
