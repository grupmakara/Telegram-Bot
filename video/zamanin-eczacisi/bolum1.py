"""Bölüm 1 - Yanlış Yüzyıl"""
OUT = 'proje1'
TITLE = ('BÖLÜM 1', 'Yanlış Yüzyıl')
HOOK = ('Bir eczacı', '<b>360 yıl</b> geriye düştü...')
END = ("Mehmet'i kurtarabilecek mi?", 'Bölüm 2 yakında...')
HOOK_CUT = ('l7', 'daha', 'h0', 'until')
# anahtar: (dosya, konuşan, altyazı, tahmini süre, duygu yoğunluğu)
LINES = {
    'h0': ('b1_h0.wav', 'ayse', '1665 mi?!', 1.5),
    'p1': ('b1_p1.wav', 'ayse', 'Gece nöbetinin son reçetesi de bitti...', 3.5, 0.35),
    'p1b': ('b1_p1b.wav', 'ayse', 'Saat üç... Bir kahve daha içersem ayakta uyuyacağım.', 4.0, 0.4),
    'p2': ('b1_p2.wav', 'ayse', 'Bu eski havan da nereden çıktı? Üstünde bir yazı var...', 4.6, 0.5),
    'p3': ('b1_p3.wav', 'ayse', '"Şifa arayan... zamanı bulur..."', 3.2, 0.3),
    'l1': ('b1_l1.wav', 'huseyin', 'Ayşe! Kalk kızım, dükkânı açacağız!', 2.8, 0.6),
    'l2': ('b1_l2.wav', 'ayse', "Ayşe mi? Ben... Elif'im.", 3.0, 0.5),
    'l2b': ('b1_l2b.wav', 'ayse', 'Bu eller... benim değil. Bu elbise de...', 3.5, 0.6),
    'l3': ('b1_l3.wav', 'ayse', 'Bu kavanozlar... bu kokular...', 3.0, 0.35),
    'l4': ('b1_l4.wav', 'huseyin', "Ne Elif'i kızım? Ateşin mi çıktı yoksa?", 2.9, 0.5),
    'l5': ('b1_l5.wav', 'ayse', 'Burası neresi? Hangi yıldayız?', 2.7, 0.6),
    'l6': ('b1_l6.wav', 'huseyin', "1665, kızım! İstanbul'dayız. Haydi, kalk artık!", 5.4, 0.55),
    'l7': ('b1_l7.wav', 'ayse', '1665 mi?! Daha penisilin bile yok!', 4.1, 0.9),
    'l8': ('b1_l8.wav', 'huseyin', 'Yüzün kireç gibi olmuş kızım. Otur, sana bir ıhlamur yapayım.', 4.5, 0.45),
    'l9': ('b1_l9.wav', 'ayse', 'Ihlamur... Ateşi düşürür, terletir... Bunu biliyorum!', 4.0, 0.6),
    'c1': ('b1_c1.wav', 'huseyin', 'Kızım, komşunun oğlu Mehmet üç gündür ateşler içinde. Hekim bile umudu kesti.', 6.0, 0.45),
    'c2': ('b1_c2.wav', 'ayse', 'Antibiyotik yok... serum yok... Ama bu raflarda başka şeyler var.', 5.5, 0.45),
    'c3': ('b1_c3.wav', 'ayse', "Söğüt kabuğu, kekik, bal... Baba, beni Mehmet'e götür!", 5.0, 0.7),
    'c4': ('b1_c4.wav', 'huseyin', 'Sen mi? Ayşe, sen ne zamandan beri şifacısın?', 3.6, 0.6),
    'c5': ('b1_c5.wav', 'ayse', 'Ne zamandan beri mi? Yaklaşık 360 yıl sonrasından beri.', 4.5, 0.55),
    'c5b': ('b1_c5b.wav', 'huseyin', 'Hah! Ateşin hâlâ geçmemiş galiba kızım!', 3.0, 0.7),
    'c6': ('b1_c6.wav', 'huseyin', 'Peki kızım... Ama Hekim Ahmet Efendi bunu duyarsa, başımız belaya girer.', 5.0, 0.45),
    'c7': ('b1_c7.wav', 'ayse', "Bırak duysun. Bu gece Mehmet'in ateşi düşecek.", 3.6, 0.6),
    'c8': ('b1_c8.wav', 'huseyin', "Haydi o zaman. Mehmet'in evi iki sokak ötede.", 3.5, 0.5),
    'c9': ('b1_c9.wav', 'ayse', 'Dün gece bir eczanedeydim... Bu gece, bir çocuğun hayatı ellerimde.', 5.0, 0.5),
}
SPLITS = {'p2': ('Üstünde', 0.5), 'l6': ('İstanbul', 0.45), 'c2': ('Ama', 0.55), 'c3': ('Baba', 0.55), 'c9': ('Bu', 0.45)}


def plan(add, S):
    shop = ('shop', {})
    H = lambda **o: S.C('huseyin', 300, 1700, **o)
    A = lambda **o: S.C('ayse', 800, 1400, **o)
    E = lambda **o: S.C('ayse', 560, 1420, modern=True, **o)
    Hd = lambda **o: S.C('huseyin', 880, 2000, 1.1, **o)
    ha, aa = S.close(H()), S.close(A())
    add('kanca', 'stage', 'h0', extra=0.35, bg=shop, hook=True, cam=((3.2, 790, 1095), (3.6, 790, 1100)),
        chars=[H(), A(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('e1', 'stage', 'p1', bg=('pharmacy', {}), cam=((1.0, 540, 960), (1.1, 560, 1050)), chars=[E(eyes='half', brow='tired', mouth='flat')])
    add('e1b', 'stage', 'p1b', bg=('pharmacy', {}), cam=((1.9, 560, 1080), (2.1, 560, 1080)), chars=[E(eyes='half', brow='tired', mouth='flat')])
    add('e2', 'stage', 'p2', 'a', bg=('pharmacy', {}), cam=((2.4, 560, 1060), (2.55, 590, 1070)), chars=[E(brow='confused', mouth='flat')])
    add('e3', 'mortar', 'p2', 'b', zoom=(1.0, 1.08))
    add('e4', 'mortar', 'p3', extra=0.4, zoom=(1.1, 1.35), touch=True, flash=True)
    add('yer', 'black', dur=2.2, text='İstanbul, 1665')
    add('w0', 'window', dur=3.0)
    add('s1', 'stage', 'l1', bg=shop, cam=((1.0, 540, 960), (1.08, 540, 1000)), chars=[H(wave=True), A(eyes='closed', brow='asleep', tilt=9)])
    add('s2', 'stage', 'l2', bg=shop, cam=((2.55, 790, 1090), (2.75, 790, 1080)),
        chars=[H(), A(eyes='closed', brow='confused', mouth='flat', tilt=9, wake=0.35)])
    add('s2b', 'stage', 'l2b', bg=shop, cam=((2.2, 800, 1250), (2.6, 800, 1320)), chars=[H(), A(eyes='wide', brow='worried', mouth='flat')])
    add('s3', 'jars', 'l3', extra=0.2)
    add('s4', 'stage', 'l4', bg=shop, cam=ha, chars=[H(brow='worried'), A()])
    add('s5', 'window', 'l5')
    add('s6a', 'stage', 'l6', 'a', bg=shop, cam=ha, chars=[H(brow='happy', wave=True), A()])
    add('s6b', 'stage', 'l6', 'b', bg=shop, cam=((1.25, 560, 1080), (1.3, 560, 1080)), chars=[H(brow='happy'), A(brow='confused', mouth='flat')])
    add('s7', 'stage', 'l7', extra=0.3, bg=shop, cam=((2.9, 790, 1100), (3.3, 790, 1100)),
        chars=[H(), A(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('s8', 'stage', 'l8', bg=shop, cam=((1.3, 560, 1080), (1.45, 420, 1040)), chars=[H(brow='worried'), A(brow='worried', mouth='flat')])
    add('s9', 'stage', 'l9', bg=shop, cam=S.close(A(), 2.5, 2.8), chars=[H(), A(brow='surprised', mouth='smirk')])
    add('k0', 'jars', dur=2.6)
    add('c1', 'stage', 'c1', bg=shop, cam=S.close(H(), 2.3, 2.5), chars=[H(brow='worried'), A()])
    add('c2a', 'stage', 'c2', 'a', bg=shop, cam=aa, chars=[H(), A(brow='worried', mouth='flat')])
    add('c2b', 'jars', 'c2', 'b', labels=True)
    add('c3a', 'jars', 'c3', 'a', labels=True, glow=True)
    add('c3b', 'stage', 'c3', 'b', bg=shop, cam=S.close(A(), 2.5, 2.8), chars=[H(), A(brow='determined', mouth='flat')])
    add('c4', 'stage', 'c4', bg=shop, cam=S.close(H(), 2.3, 2.6), chars=[H(brow='surprised'), A()])
    add('c5', 'stage', 'c5', extra=0.3, bg=shop, cam=S.close(A(), 2.6, 3.1), chars=[H(), A(brow='smug', mouth='smirk')])
    add('c5b', 'stage', 'c5b', bg=shop, cam=S.close(H(), 2.4, 2.6), chars=[H(brow='happy', wave=True), A()])
    add('c6', 'stage', 'c6', bg=shop, cam=((1.25, 560, 1080), (1.35, 480, 1040)), chars=[H(brow='worried'), A(brow='smug', mouth='smirk')])
    add('c7', 'stage', 'c7', extra=0.3, bg=shop, cam=S.close(A(), 2.7, 3.3), chars=[H(), A(brow='determined', mouth='flat')])
    add('w1', 'window', dur=2.8)
    add('c8', 'stage', 'c8', bg=('door', {'crowd': False}), cam=((1.0, 540, 960), (1.12, 540, 1000)), chars=[Hd(point=True)])
    add('c9a', 'stage', 'c9', 'a', bg=('pharmacy', {}), cam=((1.9, 560, 1080), (2.0, 560, 1080)), chars=[E(eyes='half', brow='tired', mouth='flat')])
    add('c9b', 'stage', 'c9', 'b', extra=0.6, bg=shop, cam=S.close(A(), 2.8, 3.4), chars=[H(), A(brow='determined', mouth='flat')])
    add('son', 'end', dur=3.5)
