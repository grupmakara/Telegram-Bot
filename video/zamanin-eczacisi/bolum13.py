"""Bölüm 13 - Veba Söylentisi"""
OUT = 'proje13'
TITLE = ('BÖLÜM 13', 'Veba Söylentisi')
HOOK = ('İstanbul\'a veba geliyor...', 'Ve kalabalık <b>Elif\'i</b> suçluyor!')
END = ('Havan kırıldı mı?', 'Bölüm 14 yakında...')
HOOK_CUT = ('l17', 'Vebayı', 'h0', 'until')
LINES = {
    'h0': ('b13_h0.wav', 'riza', 'Cadı bu! Vebayı o getirdi!', 2.2),
    'l1': ('b13_l1.wav', 'ayse', 'Lokman Efendi\'nin kitabı haklıysa, veba kapımızda.', 3.6, 0.5, 'worried, quiet'),
    'l2': ('b13_l2.wav', 'denizci', 'Kızım! Limana Mısır\'dan bir gemi geldi. İçinde hastalar var, kasıklarında şişlikler...', 5.4, 0.7, 'scared, urgent'),
    'l3': ('b13_l3.wav', 'ayse', 'Şişlik, ateş, titreme... Bu veba. Gemiden kimse inmemeli!', 4.2, 0.7, 'alarmed, firm'),
    'l4': ('b13_l4.wav', 'hekim', 'Veba Allah\'ın takdiridir, kızım. Kimse önüne geçemez.', 3.8, 0.5, 'resigned, slow'),
    'l5': ('b13_l5.wav', 'ayse', 'Önüne geçebiliriz, Ahmet Efendi. Vebayı farelerin pireleri taşır. Gemideki fareler limana inerse, şehre yayılır.', 6.4, 0.6, 'urgent, explaining'),
    'l6': ('b13_l6.wav', 'ayse', 'Gemi kırk gün limanın dışında beklemeli. Hastalar ayrı yerde bakılmalı.', 4.8, 0.6, 'determined'),
    'l7': ('b13_l7.wav', 'kadi', 'Kırk gün mü? Tüccarlar ayaklanır, kızım. Mallar çürür.', 3.8, 0.6, 'doubtful, stern'),
    'l8': ('b13_l8.wav', 'ayse', 'Mallar çürür, Kadı Efendi. Ama insanlar yaşar. Bir kez yayılırsa, binlerce can gider.', 5.4, 0.6, 'pleading, firm'),
    'l9': ('b13_l9.wav', 'kadi', 'Bu kız bir kez beni haklı çıkardı. Gemi kırk gün bekleyecek! Subaşı, emri duyur!', 5.2, 0.7, 'commanding'),
    'l10': ('b13_l10.wav', 'subasi', 'Emredersiniz! Kimse gemiden inmeyecek!', 2.6, 0.7, 'firm, loud'),
    'l11': ('b13_l11.wav', 'ayse', 'Yusuf, evleri dolaş. Yatakları güneşe sersinler, fare deliklerini kapatsınlar.', 4.8, 0.5, 'calm, instructing'),
    'l12': ('b13_l12.wav', 'yusuf', 'Ellerini de yıkasınlar, değil mi abla? Her zaman dediğin gibi!', 3.6, 0.6, 'eager, proud'),
    'l13': ('b13_l13.wav', 'ayse', 'Aferin Yusuf. Her zaman.', 1.8, 0.5, 'warm, smiling'),
    'l14': ('b13_l14.wav', 'denizci', 'Kızım, gemiden ses geliyor. Kırk günün sonunda on iki kişi sağ çıktı. Şehre tek bir hasta girmedi!', 6.2, 0.6, 'relieved, amazed'),
    'l15': ('b13_l15.wav', 'ayse', 'On iki can, ve şehir kurtuldu. Altmış üç.', 3.0, 0.5, 'quiet, emotional, counting'),
    'l16': ('b13_l16.wav', 'huseyin', 'Kızım, kapıda kalabalık var. Biri onları kışkırtıyor...', 3.6, 0.6, 'worried, urgent'),
    'l17': ('b13_l17.wav', 'riza', 'Cadı bu! Vebayı o getirdi! Malımız limanda çürüdü!', 3.6, 0.9, 'angry, accusing'),
    'l18': ('b13_l18.wav', 'ayse', 'Durun! Ben kimseye zarar vermedim! Taş atmayın, havan...!', 3.6, 0.8, 'scared, urgent'),
}
SPLITS = {'l5': ('Vebayı', 0.35), 'l17': ('Malımız', 0.55)}


def plan(add, S):
    shopm = ('shop', {'mortar': True})
    court = ('court', {})
    port = ('port', {})
    street = ('street', {'fountain': True})
    H = lambda **o: S.C('huseyin', 280, 1720, **o)
    A = lambda **o: S.C('ayse', 800, 1650, **o)
    Ap = lambda **o: S.C('ayse', 800, 1600, 0.95, **o)
    Ac = lambda **o: S.C('ayse', 830, 1690, **o)
    As = lambda **o: S.C('ayse', 760, 1640, **o)
    D = lambda **o: S.C('denizci', 290, 1800, **o)
    Hk = lambda **o: S.C('hekim', 250, 1820, 0.95, **o)
    K = lambda **o: S.C('kadi', 540, 1330, 0.92, **o)
    Sb = lambda **o: S.C('subasi', 230, 1830, **o)
    Y = lambda **o: S.C('yusuf', 300, 1800, 0.9, **o)
    R = lambda **o: S.C('riza', 300, 1820, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=('door', {}), hook=True, cam=((1.1, 400, 1100), (1.3, 360, 1080)), chars=[R(brow='determined', point=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub="Lokman Efendi'nin kitabı uyardı: Veba gelecek. Kapıları kapatın, suyu kaynatın.")
    add('m1', 'mortar', 'l1', zoom=(1.0, 1.15), old=True)
    add('po', 'stage', dur=2.6, bg=port, cam=((1.0, 540, 960), (1.08, 540, 900)), chars=[])
    add('p2', 'stage', 'l2', bg=port, cam=S.close(D(), 2.2, 2.5), chars=[D(brow='worried', point=True), Ap()])
    add('p3', 'stage', 'l3', bg=port, cam=S.close(Ap(), 2.5, 2.8), chars=[D(), Ap(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('p4', 'stage', 'l4', bg=port, cam=S.close(Hk(), 2.3, 2.5), chars=[Hk(brow='worried'), Ap()])
    add('p5a', 'stage', 'l5', 'a', bg=port, cam=S.close(Ap(), 2.4, 2.6), chars=[Hk(), Ap(brow='determined', mouth='flat')])
    add('p5b', 'stage', 'l5', 'b', bg=port, cam=((1.2, 540, 1250), (1.35, 560, 1250)), chars=[Hk(brow='confused'), Ap(brow='determined', point=True)])
    add('p6', 'stage', 'l6', bg=port, cam=S.close(Ap(), 2.4, 2.6), chars=[Hk(), Ap(brow='determined', mouth='flat')])
    add('mah', 'black', dur=1.8, text='Mahkeme')
    add('c7', 'stage', 'l7', bg=court, cam=S.close(K(), 2.2, 2.5), chars=[K(brow='worried'), Ac()])
    add('c8', 'stage', 'l8', bg=court, cam=S.close(Ac(), 2.4, 2.7), chars=[K(), Ac(brow='determined', mouth='flat')])
    add('c9', 'stage', 'l9', bg=court, cam=S.close(K(), 2.3, 2.6), chars=[K(brow='determined', point=True), Sb(), Ac()])
    add('c10', 'stage', 'l10', bg=court, cam=S.close(Sb(), 2.2, 2.4), chars=[K(), Sb(brow='determined', wave=True), Ac()])
    add('s11', 'stage', 'l11', bg=street, cam=S.close(As(), 2.4, 2.6), chars=[Y(), As(brow='determined', point=True)])
    add('s12', 'stage', 'l12', bg=street, cam=S.close(Y(), 2.3, 2.5), chars=[Y(brow='happy', wave=True), As()])
    add('s13', 'stage', 'l13', bg=street, cam=S.close(As(), 2.5, 2.7), chars=[Y(), As(brow='happy', mouth='smirk')])
    add('kirk', 'black', dur=2.0, text='Kırk gün sonra...')
    add('p14', 'stage', 'l14', bg=port, cam=S.close(D(), 2.2, 2.5), chars=[D(brow='happy', wave=True), Ap(brow='happy')])
    add('p15', 'stage', 'l15', extra=0.4, bg=port, cam=S.close(Ap(), 2.6, 2.9), chars=[D(), Ap(brow='happy', mouth='smirk')])
    add('s16', 'stage', 'l16', bg=shopm, cam=S.close(H(), 2.3, 2.6), chars=[H(brow='worried', point=True), A(brow='worried')])
    add('d17a', 'stage', 'l17', 'a', bg=('door', {}), cam=((1.1, 400, 1100), (1.3, 360, 1080)), chars=[R(brow='determined', point=True)])
    add('d17b', 'stage', 'l17', 'b', bg=('door', {}), cam=((1.0, 540, 1000), (1.1, 540, 1050)), chars=[R(brow='determined', wave=True)])
    add('s18', 'stage', 'l18', bg=shopm, cam=S.close(A(), 2.6, 3.0), chars=[H(brow='worried'), A(eyes='wide', brow='worried', mouth='o', shock=True)])
    add('m19', 'mortar', dur=2.6, zoom=(1.2, 1.5), old=True, crack='anim')
    add('sonraki', 'black', dur=4.5, text='Sonraki bölümde...', sub='Havan çatladı. Ayşe\'nin sesi kesik kesik geliyor...')
    add('son', 'end', dur=4.0)
