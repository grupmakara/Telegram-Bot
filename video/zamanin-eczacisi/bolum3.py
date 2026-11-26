"""Bölüm 3 - Havanın Sırrı"""
OUT = 'proje3'
TITLE = ('BÖLÜM 3', 'Havanın Sırrı')
HOOK = ('Bir canı kurtardı...', 'Şimdi <b>kendi canı</b> tehlikede!')
END = ("Kadı Efendi'nin karşısında ne olacak?", 'Bölüm 4 yakında...')
HOOK_CUT = ('l8', 'Kadı', 'h0', 'until')
LINES = {
    'h0': ('b3_h0.wav', 'subasi', 'Attar Hüseyin! Kapıyı aç!', 2.0),
    'l1': ('b3_l1.wav', 'huseyin', 'Kızım, bak! Kapının önü hasta dolmuş!', 3.2, 0.7),
    'l2': ('b3_l2.wav', 'ayse', 'Haber çabuk yayılmış. Sırayla, herkese bakacağız!', 3.6, 0.6),
    'z1': ('b3_z1.wav', 'zehra', 'Kızım, dizlerim sızlıyor. Geceleri uyuyamıyorum.', 3.6, 0.5),
    'z2': ('b3_z2.wav', 'ayse', 'Zencefil ve biberiye, Zehra Teyze. Ilık sararsınız, geçecek.', 4.2, 0.45),
    'z3': ('b3_z3.wav', 'zehra', 'Allah razı olsun kızım, ellerine sağlık!', 2.8, 0.6),
    'r1': ('b3_r1.wav', 'riza', 'Üç gündür öksürüyorum, kızım. Göğsüm yanıyor.', 3.4, 0.5),
    'r2': ('b3_r2.wav', 'ayse', 'Kekik ve bal, Rıza Amca. Sabah akşam, sıcak suyla.', 3.8, 0.45),
    'r3': ('b3_r3.wav', 'riza', 'Bu kız gerçekten bir mucize!', 2.4, 0.6),
    'hk1': ('b3_hk1.wav', 'hekim', "Gülün bakalım... Kadı Efendi'nin karşısında da gülecek misiniz?", 4.2, 0.6),
    'l3': ('b3_l3.wav', 'ayse', 'Baba... bu havan! Bu havan nereden geldi?', 3.4, 0.8),
    'l4': ('b3_l4.wav', 'huseyin', 'O mu? Dedemden kalma. Üstündeki yazıyı bugüne kadar kimse okuyamadı.', 5.0, 0.45),
    'l4b': ('b3_l4b.wav', 'huseyin', 'Dedem derdi ki, bu havan kimi seçerse, o şifacı olurmuş.', 4.2, 0.5),
    'l5': ('b3_l5.wav', 'ayse', 'Ben okuyabiliyorum... "Şifa arayan, zamanı bulur..."', 4.0, 0.4),
    'l6': ('b3_l6.wav', 'ayse', '"...ve zamanı bulan, geri dönmek için yüz canı kurtarmalı."', 4.5, 0.5),
    'l7': ('b3_l7.wav', 'ayse', 'Yüz can mı? Yani... eve dönmenin bir yolu var!', 3.8, 0.8),
    'l7b': ('b3_l7b.wav', 'ayse', 'Mehmet bir... Zehra Teyze iki... Rıza Amca üç. Doksan yedi kaldı.', 5.0, 0.5),
    'l8': ('b3_l8.wav', 'subasi', "Attar Hüseyin! Kapıyı aç! Kadı Efendi'nin emri var!", 4.0, 1.0),
    'l9': ('b3_l9.wav', 'huseyin', 'Subaşı... Hekim Ahmet şikâyet etmiş olmalı.', 3.2, 0.6),
    'l10': ('b3_l10.wav', 'subasi', 'Kızını götüreceğiz. Büyücülükle suçlanıyor!', 3.5, 0.8),
    'l10b': ('b3_l10b.wav', 'huseyin', 'Kızım, kaç! Arka kapıdan kaç!', 2.6, 0.9),
    'l10c': ('b3_l10c.wav', 'ayse', 'Kaçarsam suçlu olurum, baba. Gideceğim.', 3.2, 0.55),
    'l11': ('b3_l11.wav', 'ayse', 'Bir kişiyi kurtardım. Daha doksan dokuz kişi var... Ve kimse beni durduramayacak.', 6.0, 0.7),
}
SPLITS = {'l3': ('Bu', 0.4), 'l11': ('Ve', 0.62)}


def plan(add, S):
    shop, shopm = ('shop', {}), ('shop', {'mortar': True})
    H = lambda **o: S.C('huseyin', 300, 1700, **o)
    A = lambda **o: S.C('ayse', 800, 1400, **o)
    Z = lambda **o: S.C('zehra', 330, 1560, 0.95, **o)
    R = lambda **o: S.C('riza', 300, 1720, **o)
    Sb = lambda **o: S.C('subasi', 540, 1600, 0.95, **o)
    Hkd = lambda **o: S.C('hekim', 540, 1600, 0.95, **o)
    Hd = lambda **o: S.C('huseyin', 880, 2000, 1.1, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=('door', {'crowd': False}), hook=True, knock=[0.05, 0.3, 0.55],
        cam=S.close(Sb(), 2.0, 2.4), chars=[Sb(brow='determined', point=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub="Elif, Hekim Ahmet Efendi'ye rağmen ateşler içindeki Mehmet'i bir gecede iyileştirdi.")
    add('sabah', 'black', dur=2.0, text='Ertesi sabah...')
    add('w0', 'window', dur=3.0)
    add('d1', 'stage', 'l1', bg=('door', {}), cam=((1.0, 540, 960), (1.12, 540, 1000)), chars=[Hd(brow='surprised', point=True)])
    add('d2', 'stage', 'l2', bg=shopm, cam=S.close(A(), 2.4, 2.6), chars=[H(), A(brow='happy')])
    add('kq', 'stage', dur=3.0, bg=('door', {}), cam=((1.0, 540, 1000), (1.2, 540, 1080)), chars=[])
    add('z1', 'stage', 'z1', bg=shop, cam=((1.2, 560, 1080), (1.4, 360, 1150)), chars=[Z(brow='worried', mouth='flat'), A()])
    add('z2', 'stage', 'z2', bg=shop, cam=S.close(A(), 2.4, 2.6), chars=[Z(), A(brow='happy')])
    add('z3', 'stage', 'z3', bg=shop, cam=S.close(Z(), 2.3, 2.5), chars=[Z(brow='happy'), A()])
    add('k0', 'jars', dur=2.6)
    add('r1', 'stage', 'r1', bg=shop, cam=S.close(R(), 2.2, 2.4), chars=[R(brow='worried'), A()])
    add('r2', 'stage', 'r2', bg=shop, cam=S.close(A(), 2.5, 2.7), chars=[R(), A(brow='happy', mouth='smirk')])
    add('r3', 'stage', 'r3', bg=shop, cam=((1.2, 500, 1080), (1.3, 450, 1080)), chars=[R(brow='happy', wave=True), A(brow='happy')])
    add('hk1', 'stage', 'hk1', extra=0.3, bg=('door', {}), cam=S.close(Hkd(), 2.0, 2.5), chars=[Hkd(brow='smug')])
    add('d3a', 'stage', 'l3', 'a', bg=shopm, cam=((1.1, 560, 1000), (1.25, 500, 900)), chars=[H(), A(brow='surprised', mouth='o', eyes='wide', shock=True)])
    add('d3b', 'mortar', 'l3', 'b', zoom=(1.0, 1.1), old=True)
    add('d4', 'stage', 'l4', bg=shopm, cam=S.close(H(), 2.3, 2.5), chars=[H(), A()])
    add('d4b', 'stage', 'l4b', bg=shopm, cam=((1.2, 420, 960), (1.35, 420, 900)), chars=[H(brow='happy'), A(brow='surprised')])
    add('d5', 'mortar', 'l5', zoom=(1.1, 1.3), old=True)
    add('d6', 'mortar', 'l6', extra=0.3, zoom=(1.3, 1.6), old=True)
    add('d7', 'bowl', 'l7', extra=0.5)
    add('d7b', 'stage', 'l7b', extra=0.4, bg=shopm, cam=S.close(A(), 2.5, 2.9), chars=[H(), A(brow='determined', mouth='smirk')])
    add('m0', 'mortar', dur=2.8, zoom=(1.0, 1.2), old=True)
    add('d8', 'stage', 'l8', bg=('door', {'crowd': False}), knock=[0.0, 0.25, 0.5], cam=((1.0, 540, 960), (1.3, 540, 980)), chars=[Sb(brow='determined')])
    add('d9', 'stage', 'l9', bg=shopm, cam=S.close(H(), 2.3, 2.6), chars=[H(brow='worried'), A()])
    add('d10', 'stage', 'l10', bg=('door', {'crowd': False}), cam=S.close(Sb(), 2.2, 2.6), chars=[Sb(brow='determined', point=True)])
    add('d10b', 'stage', 'l10b', bg=shopm, cam=S.close(H(), 2.4, 2.7), chars=[H(brow='worried', wave=True), A()])
    add('d10c', 'stage', 'l10c', bg=shopm, cam=S.close(A(), 2.5, 2.7), chars=[H(), A(brow='determined', mouth='flat')])
    add('d11a', 'stage', 'l11', 'a', bg=shopm, cam=S.close(A(), 2.5, 2.7), chars=[H(), A(brow='determined', mouth='flat')])
    add('d11b', 'stage', 'l11', 'b', extra=0.6, bg=shopm, cam=S.close(A(), 2.9, 3.5), chars=[H(), A(brow='determined', mouth='flat')])
    add('son', 'end', dur=3.5)
