"""Bölüm 11 - Mühürlü Mektup"""
OUT = 'proje11'
TITLE = ('BÖLÜM 11', 'Mühürlü Mektup')
HOOK = ('Havanın dibinde bir mühür...', 'Ve onu <b>Kadı Efendi</b> tanıyor!')
END = ('Lokman Efendi kimdi?', 'Bölüm 12 yakında...')
HOOK_CUT = ('l9', 'Attar', 'h0', 'until')
LINES = {
    'h0': ('b11_h0.wav', 'kadi', 'Bu mührü tanıyorum!', 1.8),
    'l1': ('b11_l1.wav', 'ayse', 'Elli can... Havanın parıltısı her gece biraz daha güçleniyor.', 4.2, 0.4, 'quiet, thoughtful'),
    'l2': ('b11_l2.wav', 'huseyin', 'Kızım, o havanı dedemden beri kimse yerinden oynatmadı. Dikkat et.', 4.4, 0.5, 'warning, gentle'),
    'l3': ('b11_l3.wav', 'ayse', 'Baba, bak! Dibinde bir şey var. Bir mühür... Hilal ve bir yılan.', 4.6, 0.6, 'surprised, curious'),
    'l4': ('b11_l4.wav', 'huseyin', 'Ömrümde görmedim bunu. Kadı Efendi eski mühürleri bilir.', 3.8, 0.5, 'puzzled'),
    'l5': ('b11_l5.wav', 'subasi', 'Kadı Efendi meşgul! Hem... Ah, kolum...', 3.2, 0.6, 'stern, then in pain'),
    'l6': ('b11_l6.wav', 'ayse', 'Kolunuz şişmiş, kızarmış. Ne zaman yaralandınız?', 3.4, 0.5, 'concerned, careful'),
    'l7': ('b11_l7.wav', 'subasi', 'Üç gün önce bir hırsız bıçakladı. Üstüne kül bastım, geçer sandım.', 4.4, 0.5, 'tired, proud'),
    'l8': ('b11_l8.wav', 'ayse', 'Yara iltihaplanmış. Kaynamış suyla yıkayıp temiz bezle saracağız. Bal da sürelim.', 5.2, 0.5, 'calm, confident, explaining'),
    'l9': ('b11_l9.wav', 'kadi', 'Bu mührü tanıyorum! Attar Lokman Efendi\'nin mührü bu.', 3.6, 0.6, 'shocked, slow'),
    'l10': ('b11_l10.wav', 'kadi', 'Yüz yıl önce bu şehirde yaşamış. Ölüme çare bulduğu söylenirdi.', 4.6, 0.4, 'solemn, slow, storytelling'),
    'l11': ('b11_l11.wav', 'kadi', 'Bir gece dükkânıyla birlikte kayboldu. Geriye sadece bir mektup kaldı.', 4.6, 0.5, 'mysterious, slow'),
    'l12': ('b11_l12.wav', 'ayse', 'Bir mektup mu? Ne yazıyordu?', 2.2, 0.6, 'eager, curious'),
    'l13': ('b11_l13.wav', 'kadi', 'Yüz can, iki el, tek havan. Kimse anlamadı. Mahkeme sandığında saklanıyor.', 5.2, 0.5, 'quiet, mysterious'),
    'l14': ('b11_l14.wav', 'ayse', 'Yüz can... İki el... Ben ve Ayşe!', 3.0, 0.6, 'whispering, realization'),
    'l15': ('b11_l15.wav', 'subasi', 'Kızım, kolumun ateşi düştü. Sana bir özrüm var. Seni cadı sanmıştım.', 4.8, 0.5, 'embarrassed, grateful'),
    'l16': ('b11_l16.wav', 'ayse', 'Elli bir can. Ve ilk ipucu.', 2.6, 0.5, 'quiet, determined, speaking slowly and clearly'),
    'l17': ('b11_l17.wav', 'ayse', 'Ayşe! Havanı yapan kişinin adı Lokman Efendi. Bir attarmış.', 4.0, 0.6, 'excited, whispering'),
    'l18': ('b11_l18.wav', 'ayseg', 'Lokman mı? Elif... Kemal Bey\'in dedesinin eczanesinin adı Lokman Eczanesi!', 4.8, 0.7, 'shocked, whispering'),
}
SPLITS = {'l9': ('Attar', 0.4), 'l8': ('Kaynamış', 0.3)}


def plan(add, S):
    shopm = ('shop', {'mortar': True})
    court = ('court', {})
    H = lambda **o: S.C('huseyin', 280, 1720, **o)
    A = lambda **o: S.C('ayse', 800, 1650, **o)
    Ac = lambda **o: S.C('ayse', 830, 1690, **o)
    K = lambda **o: S.C('kadi', 540, 1330, 0.92, **o)
    Sb = lambda **o: S.C('subasi', 230, 1830, **o)
    G = lambda **o: S.C('ayseg', 560, 1420, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=court, hook=True, cam=S.close(K(), 2.4, 2.9), chars=[K(brow='surprised'), Ac(eyes='wide', brow='surprised', mouth='o')])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub="Ayşe 2026'da Kemal Bey'i kurtardı. Kemal Bey havanı tanıdı: dedesinin dükkânında görmüştü.")
    add('w0', 'window', dur=2.6)
    add('m1', 'mortar', 'l1', zoom=(1.0, 1.15), old=True)
    add('s2', 'stage', 'l2', bg=shopm, cam=S.close(H(), 2.3, 2.5), chars=[H(brow='worried'), A()])
    add('s3a', 'stage', 'l3', bg=shopm, cam=S.close(A(), 2.5, 2.8), chars=[H(), A(eyes='wide', brow='surprised', mouth='o')])
    add('m3', 'mortar', dur=2.4, zoom=(1.3, 1.6), old=True)
    add('s4', 'stage', 'l4', bg=shopm, cam=S.close(H(), 2.3, 2.5), chars=[H(brow='confused'), A()])
    add('mah', 'black', dur=2.0, text='Mahkeme')
    add('c5', 'stage', 'l5', bg=court, cam=S.close(Sb(), 2.2, 2.5), chars=[K(), Sb(brow='worried', arm=-20), Ac()])
    add('c6', 'stage', 'l6', bg=court, cam=S.close(Ac(), 2.4, 2.6), chars=[K(), Sb(), Ac(brow='worried', mouth='flat')])
    add('c7', 'stage', 'l7', bg=court, cam=S.close(Sb(), 2.2, 2.4), chars=[K(), Sb(brow='smug'), Ac()])
    add('c8a', 'stage', 'l8', 'a', bg=court, cam=S.close(Ac(), 2.4, 2.6), chars=[K(), Sb(), Ac(brow='determined', mouth='flat')])
    add('c8b', 'jars', 'l8', 'b')
    add('c9a', 'stage', 'l9', 'a', bg=court, cam=S.close(K(), 2.3, 2.7), chars=[K(brow='surprised', point=True), Sb(), Ac()])
    add('c9b', 'mortar', 'l9', 'b', zoom=(1.2, 1.4), old=True)
    add('c10', 'stage', 'l10', bg=court, cam=((1.2, 540, 1150), (1.35, 540, 1100)), chars=[K(), Ac(brow='surprised')])
    add('c11', 'stage', 'l11', bg=court, cam=S.close(K(), 2.2, 2.5), chars=[K(brow='worried'), Ac()])
    add('c12', 'stage', 'l12', bg=court, cam=S.close(Ac(), 2.4, 2.6), chars=[K(), Ac(eyes='wide', brow='surprised', mouth='o')])
    add('c13', 'stage', 'l13', extra=0.4, bg=court, cam=S.close(K(), 2.4, 2.8), chars=[K(brow='worried'), Ac()])
    add('c14', 'stage', 'l14', extra=0.4, bg=court, cam=S.close(Ac(), 2.7, 3.1), chars=[K(), Ac(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('gun', 'black', dur=1.8, text='Üç gün sonra...')
    add('c15', 'stage', 'l15', bg=court, cam=S.close(Sb(), 2.2, 2.4), chars=[K(), Sb(brow='happy'), Ac(brow='happy')])
    add('c16', 'stage', 'l16', bg=court, cam=S.close(Ac(), 2.5, 2.8), chars=[K(), Sb(), Ac(brow='determined', mouth='smirk')])
    add('gece', 'black', dur=1.8, text='O gece...')
    add('m17', 'mortar', 'l17', zoom=(1.0, 1.25), old=True)
    add('e18', 'stage', 'l18', extra=0.8, bg=('pharmacy', {}), cam=((2.2, 560, 1080), (2.7, 560, 1080)), chars=[G(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('sonraki', 'black', dur=4.5, text='Sonraki bölümde...', sub="Kemal Bey dedesinin eski kitabını getiriyor. Son sayfada tanıdık bir yüz...")
    add('son', 'end', dur=4.0)
