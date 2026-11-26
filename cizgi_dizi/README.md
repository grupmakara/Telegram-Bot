# Çizgi Dizi Stüdyosu

Günde 3 bölüm yayınlanacak, merak uyandıran Türkçe animasyon dizi Shorts'ları.
Her bölüm bir JSON senaryodan otomatik olarak 1080×1920 videoya dönüşür
(düz vektör karakterler, ağız senkronu, altyazı, müzik ve efekt).

## 1. Referans kanal analizi: Çizgi Seri (@cizgiseri)

| Özellik | Kanalda gözlenen |
|---|---|
| Format | Her gün yeni bölüm; dizi halinde Shorts, sezonlar ayrıca tek parça uzun video |
| Diziler | O Köyün Delisi (24+ bölüm), Saklı Şansım (22 bölüm, sezon finali), Odadaki Kız (12 bölüm), Hurdacı Sabri (yeni) |
| Ana kalıp | **Küçümsenen kahraman** (deli, sıvacı, hurdacı) gizli bir bilgi/kimlikle haklı çıkar |
| Başlık kalıbı | `"Alıntı" dedi, ters köşe olay | Dizi Adı N. Bölüm` |
| Başlık örnekleri | *"Bu da sahtedir" deyip yırttığı tablo altı milyar dolar çıktı* / *"Deliye sormam" dedi, yamaçta oğlu vardı* |
| Görsel stil | Düz 2D vektör, önden bakan karakterler, kalın kontur, sade mekânlar (karlı köy, köşk, Boğaz manzarası) |
| Ekran öğeleri | Altta siyah kutuda beyaz diyalog altyazısı, telefon "Gelen arama" ekranı, sarı "SEZON FİNALİ" etiketi |
| Hedef | Yetişkin izleyici; aile, para, kayınvalide, gizli varis, haksızlığa uğrayıp haklı çıkma |
| En çok izlenenler | Para/değer ters köşesi (sahte sanılan tablo, pazardan alınan saray porseleni) ve aile içi gerilim (kayınvalide) |

**Bizim uyguladığımız kurallar**
1. İlk cümle kavga, hakaret ya da şok içerir (ilk 2 saniyede merak).
2. Her bölüm küçük bir olayı çözer ve büyük sırra bir ipucu ekler.
3. Son sahne her zaman yarım kalır, ekranda *"… N. Bölüm'de"* kartı ve gerilim efekti çıkar.
4. Bölüm süresi 60–80 saniye, 12–18 replik.
5. Başlıkta önce alıntı, sonra sonuç gelir; sonucu tam söylemeyiz.

## 2. Dizi: Bodrum Kattaki Adam (özgün)

> Nişantaşı'ndaki Sedef Apartmanı'nın kapıcısı Rıza Usta'yı herkes küçümser.
> Yönetici onu kovmak ister, zengin komşular hor görür, bir müteahhit binayı
> "çürük" raporuyla yıktırmaya çalışır. Ama Rıza Usta bu binanın her kolonunu
> bilir, çünkü binayı 1979'da o çizmiştir.

### Karakterler
| Kod | Karakter | Rol | Ses |
|---|---|---|---|
| `riza` | **Rıza Usta**, 58 | Kapıcı. Aslında binanın proje mühendisi Rıza Karaca | Ahmet (kalın) |
| `zeynep` | **Zeynep**, 21 | Kızı, mimarlık öğrencisi, sırrı ilk o çözer | Emel (genç) |
| `selma` | **Selma Hanım**, 50 | 5. kat, kibirli zengin komşu, Can'ın annesi | Emel (olgun) |
| `kenan` | **Kenan Bey**, 55 | Apartman yöneticisi, Rıza'yı kovmak istiyor | Ahmet (hızlı) |
| `can` | **Can**, 23 | Selma'nın oğlu, Zeynep'e âşık | Ahmet (genç) |
| `ferit` | **Ferit**, 40 | Müteahhit temsilcisi, sahte rapor hazırlıyor | Ahmet (yavaş) |
| `anlatici` | Anlatıcı | Sahne geçişleri | Ahmet |

### Sezon 1 planı (24 bölüm = 8 gün)
| Gün | Bölüm | Başlık (YouTube) |
|---|---|---|
| 1 | 1 ✅ | "Asansörü de kapıcıya mı soracağız?" dedi, beş dakika sonra iki kat arasında kaldı |
| 1 | 2 ✅ | "Bu bina çürük, yıkılacak" dediler, kapıcı kolonları tek tek saydı |
| 1 | 3 ✅ | "Kapıcının kızıyla ne işin var?" dedi, oğlu kızın elini bırakmadı |
| 2 | 4 | Kapıya tahliye kâğıdı astılar, kapıcı mühürdeki tarihe bakıp güldü |
| 2 | 5 | Bodruma gizlice girdiler, sandık yerinde yoktu |
| 2 | 6 | "Babam mühendis değil, kapıcı" dedi, hoca projeyi görünce ayağa kalktı |
| 3 | 7 | Selma imzayı attı, sonra sözleşmenin arka sayfasını okudu |
| 3 | 8 | Yeni güvenlik şirketi ilk gece kapıyı açık bıraktı, hırsızı kapıcı yakaladı |
| 3 | 9 | Asansör tamircisi kapıcıyı görünce şapkasını çıkardı: "Karaca Bey?" |
| 4 | 10 | Can annesine "Ben de bodruma taşınıyorum" dedi |
| 4 | 11 | Ferit çatlağı büyütmek için gece matkapla geldi, kamera çaydanlığın içindeydi |
| 4 | 12 | "Kapıcı oy kullanamaz" dediler, tapu kaydı okununca salon sustu |
| 5 | 13 | Selma'nın kocası yıllar sonra eve döndü, ilk sarıldığı kişi kapıcıydı |
| 5 | 14 | 1999'da enkazdan çıkardığı çocuk şimdi belediyede müdür |
| 5 | 15 | Ferit'in patronu ilk kez göründü: Kenan'ın ağabeyi |
| 6 | 16 | Apartman kasası boşaltılmış, kayıp defter bodrumda çıktı |
| 6 | 17 | Zeynep bursu kaybetti, harç parasını gizlice Selma yatırdı |
| 6 | 18 | Tatbikatta herkes merdivene koştu, kapıcı "Kolonun yanına!" dedi |
| 7 | 19 | Belediye binayı mühürledi, kapıcı mührün üstüne 1979 projesini koydu |
| 7 | 20 | Ferit havalimanında kaçıyordu, telefon çaldı: arayan kapıcıydı |
| 7 | 21 | "Bina yıkılmayacak" kararı çıktı, Kenan istifasını kapıcıya verdi |
| 8 | 22 | Selma, Zeynep'in parmağına annesinin yüzüğünü taktı |
| 8 | 23 | Apartman toplantısında sordular: "Yeni yönetici kapıcı mı olsun?" |
| 8 | 24 | SEZON FİNALİ: Rıza Karaca neden 22 yıl kapıcı oldu? |

**Büyük sır (finalde açılır):** Rıza Karaca, 1999 depreminde eşini başka bir
müteahhidin çürük binasında kaybetti. Kendi çizdiği tek sağlam binanın başında
durmaya yemin etti. Ferit'in patronu o müteahhidin oğludur. Bu, Sezon 2'nin kancası.

## 3. Yayın takvimi (günde 3 video)

| Saat (TSİ) | Bölüm | Neden |
|---|---|---|
| 12:30 | Günün 1. bölümü | Öğle arası kaydırma |
| 18:00 | Günün 2. bölümü | İş çıkışı |
| 21:00 | Günün 3. bölümü (gerilimli son) | Akşam zirvesi; sonraki güne bekleme yaratır |

- Her sezon bitince bölümleri birleştirip "tek parça" uzun video olarak yükle (kanal da böyle yapıyor).
- Açıklama şablonu: `Bodrum Kattaki Adam N. Bölüm 🎬 Her gün 3 yeni bölüm! Takip et, kaçırma. #animasyon #dizi #shorts #hikaye #bodrumkattakiadam`
- Bölüm başlıkları her senaryo dosyasının `title` alanında hazır.

## 4. Üretim

```bash
pip install edge-tts pycairo numpy        # bir kez
python3 engine/render.py diziler/bodrum_kattaki_adam/bolumler/bolum04.json     # video
python3 engine/render.py diziler/bodrum_kattaki_adam/bolumler/bolum04.json --preview   # hızlı kare önizleme
```

Videolar `cikti/<dizi>/bolumNN.mp4` olarak çıkar (her biri yaklaşık 50 saniyede render edilir).

### Senaryo formatı
```json
{"series": "...", "episode": 4, "title": "...", "next_text": "... 5. Bölüm'de...",
 "scenes": [{"bg": "lobby", "cast": ["riza", "kenan"], "lines": [
   {"who": "kenan", "mood": "angry", "text": "Replik", "react": {"riza": "sad"}},
   {"caption": "GÜM!", "sfx": "thud", "shake": true, "dur": 1.2},
   {"who": "riza", "mood": "smile", "text": "...", "prop": "document", "prop_caption": "TAPU", "shot": "close"}
 ]}]}
```
- **Mekânlar (`bg`):** `lobby`, `basement`, `salon`, `street`; gece için sonuna `_night` eklenir.
- **Duygular (`mood`):** `neutral`, `smile`, `angry`, `surprised`, `sad`, `smug`, `worried`.
- **Objeler (`prop`):** `phone` (yazı = arayan), `photo`, `document`, `money`, `crack`.
- **Efektler (`sfx`):** `thud`, `sting`, `ding`, `phone`, `alarm`, `elevator`, `whoosh`, `door`.
- **Çekim (`shot`):** `wide`, `close` ya da `two:a,b`; boş bırakılırsa otomatik seçilir.
- **Ses:** Microsoft Edge'in ücretsiz Türkçe neural sesleri (`edge-tts`), karakter başına farklı ton ve hız.
