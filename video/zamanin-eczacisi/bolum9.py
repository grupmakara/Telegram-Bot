"""Bölüm 9 - Şifahane (2. sezon açılışı)"""
OUT = 'proje9'
TITLE = ('BÖLÜM 9', 'Şifahane')
HOOK = ('Hekim kan almak istiyor...', 'Ama Elif <b>başka bir yol</b> biliyor!')
END = ('Ayşe 2026\'da tehlikede mi?', 'Bölüm 10 yakında...')
HOOK_CUT = ('l9', 'Durun', 'h0', 'until')
LINES = {
    'h0': ('b9_h0.wav', 'ayse', 'Durun, Ahmet Efendi!', 2.0),
    'l1': ('b9_l1.wav', 'huseyin', 'Kızım, bak! Kapının önü sabahtan beri dolu.', 3.6, 0.6, 'amazed, proud'),
    'l2': ('b9_l2.wav', 'ayse', 'Baba, artık burası bir şifahane. Herkese bakacağız.', 4.0, 0.5, 'warm, determined'),
    'l3': ('b9_l3.wav', 'yusuf', 'Ayşe abla, limandan bir reis geldi. Çok kötü görünüyor.', 4.0, 0.6, 'worried'),
    'l4': ('b9_l4.wav', 'denizci', 'Kızım, dişlerim sallanıyor, diş etlerim kanıyor. Bacaklarım morardı.', 5.0, 0.5, 'tired, weak'),
    'l5': ('b9_l5.wav', 'denizci', 'Gemide altı adamım daha aynı hâlde.', 3.0, 0.5, 'worried, tired'),
    'l6': ('b9_l6.wav', 'hekim', 'Kanı bozulmuş. Hemen kan alalım, bozuk kan aksın.', 3.8, 0.6, 'confident, stern'),
    'l7': ('b9_l7.wav', 'ayse', 'Reis, kaç aydır denizdesiniz? Ne yiyorsunuz?', 3.4, 0.5, 'curious, calm'),
    'l8': ('b9_l8.wav', 'denizci', 'Dört ay oldu. Peksimet, tuzlu et... Başka bir şey yok.', 4.2, 0.5, 'tired'),
    'l9': ('b9_l9.wav', 'ayse', 'Durun, Ahmet Efendi! Bu adamın kanı bozuk değil. Vücudu taze meyveye aç.', 5.0, 0.6, 'firm, urgent'),
    'l10': ('b9_l10.wav', 'hekim', 'Meyveye mi? Koca reisi limonla mı iyileştireceksin?', 3.6, 0.6, 'mocking, doubtful'),
    'l11': ('b9_l11.wav', 'ayse', 'Evet. Turunç, limon, lahana turşusu. Her gün. Kan almak onu daha da zayıflatır.', 5.4, 0.5, 'confident, explaining'),
    'l12': ('b9_l12.wav', 'hekim', 'Peki. Bir hafta. Ama iyileşmezse, benim usulüm.', 3.6, 0.5, 'reluctant, testing'),
    'l13': ('b9_l13.wav', 'yusuf', 'Ben limana gider, adamlara da turunç götürürüm!', 3.0, 0.7, 'eager, excited'),
    'l14': ('b9_l14.wav', 'denizci', 'Kızım, dişlerim artık sallanmıyor! Adamlarım da ayağa kalktı!', 4.4, 0.7, 'joyful, amazed'),
    'l15': ('b9_l15.wav', 'hekim', 'Kitaplarda böyle bir şey yazmıyordu...', 2.8, 0.4, 'quiet, thoughtful, to himself'),
    'l16': ('b9_l16.wav', 'ayse', 'Kitapları yazmaya devam edeceğiz, Ahmet Efendi. Birlikte.', 3.8, 0.5, 'kind, smiling'),
    'l17': ('b9_l17.wav', 'ayse', 'Yedi can daha... Kırk dokuz oldu.', 3.0, 0.5, 'whispering, counting'),
    'l18': ('b9_l18.wav', 'ayseg', 'Elif! Elif, beni duyuyor musun?', 2.6, 0.7, 'urgent, worried, whispering'),
    'l19': ('b9_l19.wav', 'ayse', 'Ayşe! Buradayım. Ne oldu?', 2.4, 0.6, 'alarmed, quiet'),
    'l20': ('b9_l20.wav', 'ayseg', 'Eczanenin sahibi Kemal Bey... Bugün bana çok garip baktı. Galiba bir şeylerden şüpheleniyor.', 5.6, 0.6, 'scared, whispering'),
}
SPLITS = {'l9': ('Bu', 0.4), 'l11': ('Kan', 0.62)}


def plan(add, S):
    shopm = ('shop', {'mortar': True})
    port = ('port', {})
    H = lambda **o: S.C('huseyin', 280, 1720, **o)
    A = lambda **o: S.C('ayse', 800, 1650, **o)
    Y = lambda **o: S.C('yusuf', 520, 1800, 0.9, **o)
    D = lambda **o: S.C('denizci', 300, 1780, **o)
    Hk = lambda **o: S.C('hekim', 250, 1800, 0.95, **o)
    G = lambda **o: S.C('ayseg', 560, 1420, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=shopm, hook=True, cam=S.close(A(), 2.6, 3.1), chars=[Hk(arm=-20), A(brow='determined', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki sezonda...', sub="Elif 1665'te kırk iki can kurtardı. Kadı Efendi bir şifahane açmasına izin verdi.")
    add('s2', 'black', dur=2.2, text='2. Sezon', sub='İki dünya, tek havan.')
    add('w0', 'window', dur=3.0)
    add('d1', 'stage', 'l1', bg=('door', {}), cam=((1.0, 540, 1000), (1.15, 540, 1080)), chars=[])
    add('s2a', 'stage', 'l2', bg=shopm, cam=S.close(A(), 2.4, 2.6), chars=[H(), A(brow='happy', mouth='smirk')])
    add('s3', 'stage', 'l3', bg=shopm, cam=S.close(Y(), 2.3, 2.5), chars=[Y(brow='worried', point=True), A()])
    add('s4', 'stage', 'l4', bg=shopm, cam=S.close(D(), 2.2, 2.4), chars=[D(brow='worried'), A(brow='worried', mouth='flat')])
    add('s5', 'stage', 'l5', bg=shopm, cam=((1.2, 520, 1300), (1.35, 520, 1250)), chars=[D(brow='worried'), A()])
    add('s6', 'stage', 'l6', bg=shopm, cam=S.close(Hk(), 2.3, 2.5), chars=[Hk(brow='smug', point=True), A()])
    add('s7', 'stage', 'l7', bg=shopm, cam=S.close(A(), 2.4, 2.6), chars=[D(), A(brow='confused', mouth='flat')])
    add('s8', 'stage', 'l8', bg=shopm, cam=S.close(D(), 2.2, 2.4), chars=[D(brow='tired'), A()])
    add('s9a', 'stage', 'l9', 'a', bg=shopm, cam=((1.3, 540, 1250), (1.4, 560, 1250)), chars=[Hk(arm=-30), A(brow='determined', mouth='o', shock=True)])
    add('s9b', 'jars', 'l9', 'b')
    add('s10', 'stage', 'l10', bg=shopm, cam=S.close(Hk(), 2.3, 2.6), chars=[Hk(brow='smug'), A()])
    add('s11a', 'stage', 'l11', 'a', bg=shopm, cam=S.close(A(), 2.4, 2.6), chars=[Hk(), A(brow='determined', mouth='flat')])
    add('s11b', 'stage', 'l11', 'b', bg=shopm, cam=((1.2, 520, 1300), (1.3, 500, 1250)), chars=[Hk(brow='confused'), A(brow='determined')])
    add('s12', 'stage', 'l12', bg=shopm, cam=S.close(Hk(), 2.3, 2.5), chars=[Hk(brow='worried'), A()])
    add('s13', 'stage', 'l13', bg=shopm, cam=S.close(Y(), 2.3, 2.6), chars=[Y(brow='happy', wave=True), A(brow='happy')])
    add('hafta', 'black', dur=2.0, text='Bir hafta sonra...')
    add('po', 'stage', dur=2.8, bg=port, cam=((1.0, 540, 960), (1.08, 540, 900)), chars=[])
    add('p14', 'stage', 'l14', bg=port, cam=S.close(D(), 2.2, 2.5), chars=[D(brow='happy', wave=True), A(brow='happy')])
    add('p15', 'stage', 'l15', bg=port, cam=((1.4, 300, 1300), (1.6, 260, 1250)), chars=[Hk(brow='confused'), A()])
    add('p16', 'stage', 'l16', bg=port, cam=S.close(A(), 2.4, 2.6), chars=[Hk(), A(brow='happy', mouth='smirk')])
    add('gece', 'black', dur=1.8, text='O gece...')
    add('m17', 'mortar', 'l17', extra=0.4, zoom=(1.0, 1.2), old=True)
    add('m18', 'mortar', 'l18', zoom=(1.2, 1.4), old=True)
    add('b19', 'stage', 'l19', bg=shopm, cam=S.close(A(), 2.6, 3.0), chars=[A(eyes='wide', brow='surprised', mouth='o')])
    add('yer', 'black', dur=1.8, text='İstanbul, 2026')
    add('e20', 'stage', 'l20', extra=0.6, bg=('pharmacy', {}), cam=((2.2, 560, 1080), (2.6, 560, 1080)), chars=[G(eyes='wide', brow='worried', mouth='flat')])
    add('sonraki', 'black', dur=4.5, text='Sonraki bölümde...', sub="Kemal Bey'in şüphesi büyüyor. Ayşe 2026'da yalnız kalacak mı?")
    add('son', 'end', dur=4.0)
