# "Lale ile Kan" — Animasyon Dizi Üretim Hattı · Tasarım

Tarih: 2026-11-25 · Durum: onay bekliyor (ses: Edge TTS; günlük üretim: istek üzerine)

## 1. Amaç ve neden

Kullanıcı, Instagram'da (ve Reels/TikTok formatında) her gün **3 bölüm** yayınlayabileceği,
izleyicide merak uyandırıp izlenme ve takipçi artıran **2D çizgi film tarzında, bölümlü bir dram dizisi**
istiyor. Örnek aldığı hesaplar: `gelecektengecmisime` ("1453 Yeniden Doğuş"), `saklisansim`,
`oadambendegilim`. Ortak format:

- Düz renkli, eklemli "kukla" karakterler (cut-out animasyon).
- Diyaloglar karakter sesleriyle seslendirilir, altyazı ekranda.
- Üstte dizi adı + "X. Bölüm"; kapakta/ilk saniyede tek bir çarpıcı replik.
- Her bölüm bir merak noktasında (cliffhanger) biter.

Kullanıcı üç hesabın profil ekran görüntülerini paylaştı (görsel referans): ten rengi düz yüzler,
kalın kontur, büyük gözler, eklemli kollar; kapak karesinde alt bantta tırnak içinde replik
("O Adam Ben Değilim" stili: krem bant, el yazısı benzeri yazı) veya üstte koyu bant + "X. BÖLÜM"
("Saklı Şansım" stili). Hedef cilalılık seviyesi bu ekran görüntüleri kadar; birebir kopya değil.

Senaryo, seslendirme, altyazı ve montajın tamamını Claude üretecek. Kullanıcı yalnızca
hazır MP4'ü paylaşacak (otomatik yayın sonraki aşama).

## 2. Hedefler / Hedef dışı / Anti-hedefler

**Hedefler**
- Bölüm senaryosu (metin dosyası) → tek komutla hazır 1080×1920 MP4.
- Karakterler ve mekânlar tüm bölümlerde birebir aynı görünür.
- Bölüm başı 60–90 sn; günde 3 bölüm üretilebilir hız.
- Kelime kelime senkron, büyük, okunaklı Türkçe altyazı.
- İlk teslim: Bölüm 1–3 hazır videolar + sezonun 30 bölümlük akışı.

**Hedef dışı (v1)**
- Instagram/TikTok'a otomatik yükleme (Meta işletme hesabı + token gerektiriyor; sonra).
- Telegram'a otomatik gönderim (mevcut bot sonra bağlanabilir; şu an `api.telegram.org` erişimi denenmedi).
- Videoya gömülü müzik (aşağıya bkz.).
- Tam kare-kare animasyon, yürüme döngüsü gibi karmaşık hareketler.

**Anti-hedefler** (çalışsa bile başarısızlık sayılır)
- Örnek dizilerin hikâyesini, karakterlerini, adlarını veya görünümünü kopyalamak.
- Bölümden bölüme değişen karakter görünümü.
- Dinlenmesi rahatsız edici, robotik ses.
- Merak sonu olmayan, "kapanmış" bölümler.

## 3. Kısıtlar

- Bulut konteyner; ağ kısıtlı. `instagram.com`, `graph.facebook.com`, `speech.platform.bing.com`
  şu an engelli. npm/PyPI erişimi var.
- Chromium + Playwright kurulu (`/opt/pw-browsers/chromium`), ffmpeg kurulu, Node 22, Python 3.
- Konteyner geçicidir: kod ve senaryolar repoya commit edilir; videolar çıktı olarak kullanıcıya gönderilir.
- Repo mevcut bir Telegram botu (Node 12 / telegraf 3). Dizi hattı ondan **ayrı bir alt klasörde** yaşar,
  botu bozmaz.

## 4. Yaklaşımlar (değerlendirilen)

1. **Kodla çizilmiş SVG kukla karakterler + otomatik montaj (Remotion).** ✅ **Seçilen.**
   Tutarlı karakter, ücretsiz, ölçeklenebilir. Bedeli: sade çizim tarzı ve ilk kurulum emeği.
2. **Her sahne için yapay zekâ ile üretilen resim + Ken Burns efekti.** Reddedildi: karakter tutarlılığı
   bozulur, ücretli API + ek ağ izni gerekir.
3. **Yapay zekâ ile karakter bir kez çizilip parçalanır, kukla gibi oynatılır.** Reddedildi: parçalama
   kırılgan ve zahmetli; iki yolun zayıflıklarını birleştirir.

Kullanıcı 1. yolu seçti.

## 5. Hikâye: "Lale ile Kan" (kullanıcı A seçeneğini seçti)

**Dönem/mekân:** 1720'ler, İstanbul, Lale Devri. Saray, konaklar, lale bahçeleri, Haliç, çarşı.

**Öncül:** Saray kâtibi Yusuf Efendi, Vezir Kara Bekir Paşa'nın gizli hazine yolsuzluğunu fark eder.
Bekir onu sahte belgelerle ihanetle suçlatıp idam ettirir; konağı yakılır, oğlu Emir'in öldüğü sanılır.
10 yıl sonra Emir, **"Tüccar Murad"** adıyla zengin bir yabancı olarak İstanbul'a döner; babasını
mahvedenleri tek tek düşürür. Ama Bekir'in kızı **Nilüfer**'e âşık olur.

**Karakterler** (hepsi özgün; görünüm notları çizim için bağlayıcı):

| Karakter | Rol | Görünüm |
|---|---|---|
| Emir / "Tüccar Murad" (27) | Kahraman | Siyah kısa sakal, kalın kaşlar, koyu lacivert kaftan, beyaz sarık (Murad kimliğinde zengin bordo kaftan + altın kuşak) |
| Kara Bekir Paşa (55) | Kötü adam, vezir | Gür kır sakal, çatık kaşlar, yüksek beyaz kavuk, siyah-altın kürklü kaftan |
| Nilüfer (22) | Bekir'in kızı, aşk | Uzun kızıl-kahve örgülü saç, açık yeşil entari, ince altın taç/hotoz |
| Saffet Ağa (45) | Bekir'in sağ kolu, ilk hedef | Yanağında yara izi, kalın bıyık, kırmızı yelek, belde hançer |
| Kadı Lütfi Efendi (60) | Sahte hükmü veren kadı | Ak sakal, gözlük, büyük kavuk, koyu yeşil cübbe |
| Hızır Reis (65) | Emir'i kurtaran kaptan, akıl hocası | Beyaz kısa sakal, göz bandı, mavi denizci yeleği |
| Zeynep (19) | Emir'in öldü sanılan kız kardeşi; Bekir'in konağında hizmetçi | Siyah saç, beyaz başörtü, sade gri entari |
| Yusuf Efendi | Baba (yalnız geçmiş sahneleri) | Kır sakal, kâtip kavuğu, kahverengi cübbe |

**Sezon 1 akışı (30 bölüm, ~10 gün):**
- 1–3: Açılış. 1. bölüm: Emir'in idam günü anısı + "Murad" olarak İstanbul'a iniş. Sonu: Bekir'in
  konağında hizmet eden kızın Zeynep olduğunu görür.
- 4–10: Saffet Ağa'nın düşüşü; Nilüfer ile tanışma; Zeynep'in Emir'i tanımaması.
- 11–20: Kadı Lütfi'nin itirafı; Bekir "Murad"dan şüphelenir; Nilüfer gerçeği sezer.
- 21–30: Bekir'in karşı hamlesi, Emir'in yakalanması, Zeynep'in kardeşini tanıması, sezon finali:
  Bekir'in arkasında daha büyük birinin (saraydan) olduğunun ortaya çıkması.

Ayrıntılı bölüm dökümü ilk 10 bölüm için `video/story/season1.md`'ye yazılacak; sonrakiler üretim
sırasında, izleyici yorumlarına göre ayarlanabilecek şekilde açık bırakılır.

**Bölüm yapısı (her bölüm):**
1. 0–3 sn **kanca**: bölümün en çarpıcı repliği/anı önce gösterilir (kapak karesi de budur).
2. Üst bant: "LALE İLE KAN" logosu + "X. BÖLÜM" (tüm bölüm boyunca).
3. 3–5 sahne, 8–14 replik; arada kısa anlatıcı cümleleri.
4. Son 2 sn: merak sonu repliği + "Devamı X+1. Bölümde" kartı.
5. Açıklama metni + hashtag önerisi her bölümle birlikte üretilir.

## 6. Nasıl yapılacak (kararlar)

**Klasör:** `video/` (repo kökünde, bottan bağımsız kendi `package.json`'ı ile).

**Render:** Remotion (React) + Chromium, 1080×1920, 30 fps, H.264 MP4. *(Claude'un kararı:
Remotion animasyon zamanlaması, katmanlar ve kamera hareketi için en uygun; Chromium kurulu.
Lisans: bireysel/küçük ekip için ücretsiz.)*

**Karakterler:** Her karakter React/SVG bileşeni; ortak bir "kukla iskeleti" (baş, gövde, üst kol,
ön kol, el, bacaklar) + karaktere özel kıyafet/saç/sakal katmanları. Parametreler:
- `ifade`: normal, öfkeli, üzgün (gözyaşı), şaşkın, gülümseyen, sinsi
- `ağız`: konuşurken sesin genliğine göre açılıp kapanır
- otomatik göz kırpma, hafif nefes/salınım
- `poz`: duruş, kol kaldırma, işaret etme, el göğüste
- `yön`: sola/sağa bakış (aynalama)

**Mekânlar:** SVG arka planlar: Divan-ı Hümayun, Bekir'in konak salonu, lale bahçesi, Haliç limanı
(gemi), çarşı, zindan, idam meydanı (geçmiş — sepya filtre). Gece/gündüz varyantı.

**Kamera:** sahne içi yavaş yakınlaşma/kaydırma; konuşana yakın plan geçişi; kesme ve kararma.

**Seslendirme:** Microsoft Edge TTS (`edge-tts`), Türkçe nöral sesler `tr-TR-AhmetNeural` (erkek) ve
`tr-TR-EmelNeural` (kadın). Sadece iki ses olduğundan karakterler perde (pitch) ve hız ile ayrılır
(ör. Bekir: Ahmet −15 Hz, yavaş; Emir: Ahmet normal; Hızır: Ahmet −8 Hz, yavaş; Nilüfer: Emel normal;
Zeynep: Emel +10 Hz, hızlı). Anlatıcı: Ahmet, sakin.
- **Ön koşul:** `speech.platform.bing.com` için ağ izni — kullanıcıya onay kartıyla sorulacak.
- Kullanıcı kararı: ücretsiz Edge sesi (ElevenLabs reddedildi). Deneme klibinde dinleyip onaylayacak;
  beğenmezse ücretli servise geçiş yeniden konuşulur. espeak-ng yalnızca ağ izni gelene kadar geliştirme
  sırasında yer tutucu olarak kullanılabilir, asla teslim edilmez.

**Altyazı:** edge-tts kelime zaman damgalarından (WordBoundary) üretilir. Ekranın alt üçte birinde,
beyaz kalın yazı + siyah kontur, o an söylenen kelime sarı vurgulu; konuşan karakterin adı küçük
etikette. Kanca repliği kapakta tırnak içinde büyük yazı.

**Müzik:** Videoya gömülmez. *(Claude'un kararı:)* Kullanıcı Instagram'da paylaşırken uygulama
içinden popüler/trend bir müzik ekler — hem telif sorunu çıkmaz hem de algoritma trend sesleri
öne çıkarır. Basit ses efektleri (kapı, kılıç, gök gürültüsü) v2'de.

**Senaryo formatı:** Her bölüm bir YAML dosyası: `video/story/episodes/ep01.yaml`:

```yaml
bolum: 1
baslik: "Ölü Adamın Dönüşü"
kanca: { karakter: emir, replik: "On yıl önce beni öldürdüler… Bugün geri döndüm." }
sahneler:
  - mekan: idam_meydani
    gecmis: true            # sepya
    karakterler: [{ id: yusuf, x: 0.5, ifade: uzgun }, { id: bekir, x: 0.8, ifade: sinsi }]
    satirlar:
      - { kim: anlatici, metin: "İstanbul, 1710…" }
      - { kim: yusuf, metin: "Oğlum… kaç!", ifade: uzgun }
  - mekan: halic_liman
    ...
son: { karakter: emir, replik: "Zeynep?.. Sen yaşıyor musun?" }
aciklama: "…"
etiketler: ["#laleilekan", "#dizi", "#animasyon", ...]
```

**Üretim komutu:** `npm run bolum -- 1` → (1) her replik için TTS + kelime zamanları
(`video/cache/`) → (2) zaman çizelgesi hesaplanır → (3) Remotion render → `video/out/ep01.mp4`
+ `ep01_kapak.png` + `ep01_aciklama.txt`.

**Günlük akış (kullanıcı kararı):** Zamanlanmış görev yok. Kullanıcı her gün "sıradaki 3 bölüm"
der; Claude bir sonraki bölümleri `season1.md` akışına ve önceki bölümlere bakarak yazar, üretir,
gönderir. Hangi bölümde kalındığı repodaki `video/story/episodes/` dosyalarından anlaşılır; hikâye
özeti `video/story/ozet.md`'de her bölümden sonra güncellenir (yeni oturum bağlamı için).

**Teslim:** Videolar kullanıcıya dosya olarak gönderilir; senaryolar ve kod `claude/instagram-video-production-hfb69m`
dalına commit edilir.

**Üretim sırası (Claude'un kararı):** Önce kullanıcıya bir **karakter kartı** (8 karakter tek
görselde) + **10 sn'lik deneme klibi** (ses + altyazı + ağız hareketi) gösterilir; onaydan sonra
kalan mekânlar ve 1–3. bölümlerin tam render'ı yapılır. Bölüm 1–3 senaryoları render'dan önce
metin olarak kullanıcıya sunulur.

**Lisans (Claude'un kararı):** Kullanıcı bireysel içerik üreticisi varsayıldı → Remotion ücretsiz.
3 kişiden büyük bir şirketse Remotion lisansı gerekir; o durumda render katmanı
Playwright kare yakalama + ffmpeg'e taşınabilir (bileşenler aynı kalır).

## 7. Builder'a bırakılanlar

- SVG çizim ayrıntıları (renk paleti, oranlar) — görünüm tablosuna sadık kalarak.
- Ağız animasyonunun genlikten mi, kelime zamanlarından mı sürüleceği.
- Sahne geçiş türleri, kamera hareketlerinin tam değerleri.
- Repliklerin arasındaki boşluk süreleri, tempo.
- Kod yapısı, test kapsamı (zaman çizelgesi hesaplaması ve YAML doğrulaması test edilmeli).

## 8. Değişiklikler (2026-11-25, kullanıcı kararları — önceki bölümlerin önüne geçer)

Kullanıcı üç örnek video gönderdi (2,5–3 dk; karakter başına ayrı, geniş aralıklı doğal sesler;
konuşmanın ~8 dB altında sürekli müzik/ortam sesi; küçük, sakin, tek satırlık altyazılar) ve şunlara karar verdi:

- **Render: Remotion → HyperFrames.** Her bölüm `video/projects/epNN/` altında düzenlenebilir bir HyperFrames
  projesi olarak üretilir (`index.html` + `compositions/` sahne başına bir dosya, GSAP zaman çizelgeleri).
  Kuklalar ve mekânlar aynı React/SVG bileşenlerinden statik SVG olarak üretilir; göz kırpma, ağız, nefes,
  ifade değişimi ve kamera GSAP ile canlandırılır. Remotion lisans kısıtı ortadan kalkar.
- **Ses: ElevenLabs** (`eleven_multilingual_v2`, karakter başına ayrı hazır ses; `src/audio/voices.ts`).
  Anahtar ağ vekilinden `xi-api-key` olarak eklenir. Anahtar yokken Edge sesleri yedek olarak kullanılır ve uyarı basılır.
- **Süre: ~3 dakika** (150–200 sn). Her yayın bölümü sezon akışından ~2 hikâye adımı kapsar.
- **Müzik: evet.** Fon müziği `assets/bgm/tema.mp3` (ElevenLabs Music ile `npm run muzik`), ses 0.14.
  Sahne geçişlerinde whoosh, sonda riser + darbe (Pixabay lisanslı efektler, `assets/sfx/CREDITS.md`).
- **Altyazı:** örnekler gibi küçük ve sakin; 5 kelime / 30 karakterlik gruplar, anlatıcı italik ve sarımsı,
  konuşan adı yok; Reels güvenli alanında (alt kenar y ≤ 1248).
