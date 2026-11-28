# Zamanın Eczacısı · 2. Sezon: İki Dünya, Tek Havan

1. sezon sonunda: Elif (1665'te Ayşe'nin bedeninde) 42 can kurtardı, 58 kaldı. Havan üzerinden gerçek
Ayşe'yle (2026'da Elif'in bedeninde) gece aynı saatte konuşabiliyorlar. Kadı Efendi şifahane açmaya izin verdi;
Hekim Ahmet Efendi ve çırağı Yusuf artık Elif'in yanında.

**Sezonun yeni kuralı:** Ayşe'nin 2026'da kurtardığı canlar da sayılıyor. Yüze ikisi birlikte ulaşacak.
**Sezonun sırrı:** Havanı 1665'e kim bıraktı? Her bölümde bir ipucu; finalde cevap.

| Bölüm | Başlık | Dünya | Özet |
|---|---|---|---|
| 9 | Şifahane | 1665 | Şifahane açılıyor. Denizci reisinin diş etleri kanıyor, Hekim kan almak istiyor; Elif turunç ve limonla iskorbütü tedavi ediyor. Gece havandan Ayşe'nin sesi: "Burada biri benden şüpheleniyor." |
| 10 | Kemal Bey'in Şüphesi | 2026 | Eczane sahibi Kemal Bey "Elif"in değiştiğini fark ediyor. Kemal Bey şeker düşmesiyle yere yığılınca Ayşe 1665'te öğrendiği bilgiyle bal veriyor. Havan bunu da sayıyor: iki dünya aynı sayaçta. |
| 11 | Mühürlü Mektup | 1665 | Havanın dibinde bir mühür: hilal ve yılan. Kadı Efendi tanıyor: yüz yıl önce kaybolan Attar Lokman Efendi. Mektubu: "Yüz can, iki el, tek havan." Elif, subaşının iltihaplı yarasını temizliyor (51). |
| 12 | Eski Kitap | 2026 | Kemal Bey dedesinin Lokman mühürlü kitabını getiriyor; Ayşe eski yazıyı okuyabiliyor ve gerçeği anlatıyor. Kitapta veba uyarısı ve Elif'in yüzünün resmi var. |
| 13 | Veba Söylentisi | 1665 | Limana veba taşıyan bir gemi geliyor. Elif fare-pire bağlantısını anlatıyor; Kadı kırk günlük karantina emrediyor. On iki can kurtuluyor, şehir korunuyor (63). Ama öfkeli bir tüccarın taşı havanı çatlatıyor. |
| 14 | Kırık Havan | iki dünya | Ses kesiliyor. Kemal Bey'in kitabı ve Kadı'nın mektubu aynı sırrı söylüyor: dolunay gecesi iki el aynı anda. Elif Yusuf'un çıkan kolunu yerine oturtuyor (64). Havan onarılıyor ama kırmızı parlıyor. |
| 15 | Doksan Dokuz | iki dünya | Sayaç doksan dokuzda. Son can kimin olacak? |
| 16 | Eve Dönüş (2. Sezon Finali) | iki dünya | Yüzüncü can ve büyük seçim: dönmek mi, kalmak mı? |

Ses: VoxCPM2 + duzen.py (hız ve seviye düzeni). Yeni karakter: Kemal Bey (`kemal`, VoxCPM2 ile tasarlanmış ses).

Sezon finali kuralı: finalin `TITLE` üçlüsüne rozet eklenir (ör. `('BÖLÜM 16', 'Eve Dönüş', '2. SEZON FİNALİ')`);
başlık kartında kırmızı rozet çıkar. `END[0]` ve kapanış kartında da "N. Sezon Finali" yazılır.

Bitiş animasyonu: Bölüm 13'ten itibaren her bölümde `CTA = True` ve `add('son', 'end', dur=5.2)`; bitiş kartında
Beğen (kalp kırmızıya döner) ve Takip Et (✓ Takip Ediliyor) düğmelerine dokunma animasyonu ve "pop" sesi.
