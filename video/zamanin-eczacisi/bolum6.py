"""Bölüm 6 - Çeşmenin Sırrı"""
OUT = 'proje6'
TITLE = ('BÖLÜM 6', 'Çeşmenin Sırrı')
HOOK = ('Mahalle susuz kalacak...', 'Ya da <b>hasta</b> kalacak!')
END = ('Havan ne gösterecek?', 'Bölüm 7 yakında...')
HOOK_CUT = ('l7', '', 'h0', 'all')
LINES = {
    'h0': ('b6_h0.wav', 'ayse', 'Bu çeşmeyi kapatmamız lazım!', 2.4),
    'l1': ('b6_l1.wav', 'yusuf', 'İşte bu çeşme. Mahallenin yarısı buradan su içer.', 3.8, 0.5, 'explaining'),
    'l2': ('b6_l2.wav', 'ayse', 'Hasta olanlar nerede oturuyor, Yusuf? Hepsini say bana.', 4.0, 0.5, 'focused'),
    'l3': ('b6_l3.wav', 'yusuf', "Fırıncı, bakkal, Zehra Teyze'nin komşuları... Hepsi bu sokakta.", 4.5, 0.5, 'thinking, listing'),
    'l4': ('b6_l4.wav', 'ayse', 'Hepsi bu çeşmenin etrafında. Hastalık buradan yayılıyor!', 4.0, 0.7, 'excited realization'),
    'l5': ('b6_l5.wav', 'zehra', 'Kızım, bu çeşme yüz yıllık! Hiç kimse hastalanmadı bugüne kadar.', 4.8, 0.6, 'protesting, old'),
    'l6': ('b6_l6.wav', 'ayse', 'Zehra Teyze, bak, çeşmenin taşları çatlamış. Pis su sızıyor içine.', 4.8, 0.5, 'gentle, explaining'),
    'l7': ('b6_l7.wav', 'ayse', 'Bu çeşmeyi kapatmamız lazım!', 2.4, 0.9, 'loud, determined'),
    'l8': ('b6_l8.wav', 'riza', 'Kapatırsak nereden su içeceğiz?', 2.6, 0.6, 'worried, objecting'),
    'l9': ('b6_l9.wav', 'ayse', 'Yukarı mahallenin çeşmesinden. Ve her suyu kaynatarak.', 3.8, 0.5, 'calm'),
    'l10': ('b6_l10.wav', 'hekim', "Bir çeşmeyi kapatmak için Kadı'nın izni gerekir, kızım.", 4.0, 0.5, 'cold, formal'),
    'l11': ('b6_l11.wav', 'ayse', "O zaman Kadı Efendi'ye gidelim, efendim. Siz de gelin.", 3.8, 0.5, 'polite, bold'),
    'l12': ('b6_l12.wav', 'hekim', 'Ben mi? Neden?', 1.8, 0.6, 'surprised'),
    'l13': ('b6_l13.wav', 'ayse', 'Çünkü siz de gördünüz. Limanda kaynatılmış su adamları kurtardı.', 4.6, 0.5, 'firm, respectful'),
    'l14': ('b6_l14.wav', 'hekim', '...Gördüm. Haklıydın.', 2.4, 0.4, 'reluctant, quiet, sighing'),
    'l15': ('b6_l15.wav', 'kadi', 'Hekim Ahmet Efendi de mi aynı fikirde?', 3.0, 0.5, 'surprised, slow'),
    'l16': ('b6_l16.wav', 'hekim', 'Evet, Kadı Efendi. Çeşme kapatılsın.', 2.8, 0.5, 'formal'),
    'l17': ('b6_l17.wav', 'kadi', 'Öyleyse kapatılsın! Ve kızım... Perhize uydum. Ellerim artık titremiyor.', 5.5, 0.5, 'warm, pleased'),
    'l18': ('b6_l18.wav', 'ayse', 'Sevindim, Kadı Efendi. Yürüyüşü de bırakmayın!', 3.2, 0.6, 'happy, playful'),
    'l19': ('b6_l19.wav', 'yusuf', 'Ayşe Hanım, bir haftadır kimse hastalanmadı!', 3.2, 0.8, 'excited, joyful'),
    'l20': ('b6_l20.wav', 'ayse', 'Kırk bir can... Elli dokuz kaldı.', 3.0, 0.5, 'whispering, counting'),
    'l21': ('b6_l21.wav', 'huseyin', 'Kızım, havan... Havan parlıyor!', 2.6, 0.8, 'shocked, afraid'),
    'l22': ('b6_l22.wav', 'ayse', 'Bu ilk defa oluyor... Bir şey göstermek istiyor!', 3.6, 0.7, 'amazed, whispering'),
}
SPLITS = {'l17': ('Ve', 0.4)}


def plan(add, S):
    st, stb = ('street', {}), ('street', {'broken': True})
    Y = lambda **o: S.C('yusuf', 260, 1820, **o)
    A = lambda **o: S.C('ayse', 820, 1640, 0.95, **o)
    Z = lambda **o: S.C('zehra', 250, 1700, 0.95, **o)
    R = lambda **o: S.C('riza', 260, 1820, **o)
    Hk = lambda **o: S.C('hekim', 240, 1820, **o)
    K = lambda **o: S.C('kadi', 540, 1330, 0.92, **o)
    Ac = lambda **o: S.C('ayse', 830, 1690, **o)
    Hkc = lambda **o: S.C('hekim', 210, 1860, **o)
    H = lambda **o: S.C('huseyin', 300, 1700, **o)
    As = lambda **o: S.C('ayse', 800, 1400, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=stb, hook=True, cam=S.close(A(), 2.5, 3.0), chars=[A(brow='determined', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub='Elif limandaki salgını durdurdu. Ama hastalık mahalleye sıçradı.')
    add('so', 'stage', dur=3.0, bg=st, cam=((1.0, 540, 960), (1.1, 540, 1050)), chars=[])
    add('s1', 'stage', 'l1', bg=st, cam=((1.1, 450, 1200), (1.2, 400, 1250)), chars=[Y(point=True), A()])
    add('s2', 'stage', 'l2', bg=st, cam=S.close(A(), 2.4, 2.6), chars=[Y(), A(brow='determined', mouth='flat')])
    add('s3', 'stage', 'l3', bg=st, cam=S.close(Y(), 2.3, 2.5), chars=[Y(brow='confused'), A()])
    add('s4', 'stage', 'l4', bg=st, cam=S.close(A(), 2.5, 2.8), chars=[Y(), A(brow='surprised', mouth='o', eyes='wide')])
    add('k0', 'jars', dur=2.4)
    add('s5', 'stage', 'l5', bg=st, cam=S.close(Z(), 2.3, 2.5), chars=[Z(brow='worried', mouth='flat'), A()])
    add('s6a', 'stage', 'l6', bg=stb, cam=((1.6, 540, 1050), (1.9, 540, 1060)), chars=[])
    add('s7', 'stage', 'l7', bg=stb, cam=((1.1, 600, 1250), (1.3, 700, 1250)), chars=[Z(brow='surprised'), A(brow='determined', mouth='o', shock=True)])
    add('s8', 'stage', 'l8', bg=st, cam=S.close(R(), 2.3, 2.5), chars=[R(brow='worried'), A()])
    add('s9', 'stage', 'l9', bg=st, cam=S.close(A(), 2.4, 2.6), chars=[R(), A()])
    add('s10', 'stage', 'l10', bg=st, cam=S.close(Hk(), 2.3, 2.5), chars=[Hk(brow='determined'), A()])
    add('s11', 'stage', 'l11', bg=st, cam=S.close(A(), 2.4, 2.6), chars=[Hk(), A(brow='smug', mouth='smirk')])
    add('s12', 'stage', 'l12', bg=st, cam=S.close(Hk(), 2.5, 2.7), chars=[Hk(brow='surprised'), A()])
    add('s13', 'stage', 'l13', bg=st, cam=S.close(A(), 2.4, 2.6), chars=[Hk(), A(brow='determined', mouth='flat')])
    add('s14', 'stage', 'l14', extra=0.5, bg=st, cam=S.close(Hk(), 2.4, 2.9), chars=[Hk(brow='worried'), A()])
    add('co', 'stage', dur=2.4, bg=('court', {}), cam=((1.0, 540, 960), (1.08, 540, 1000)), chars=[K(), Hkc(), Ac()])
    add('c15', 'stage', 'l15', bg=('court', {}), cam=S.close(K(), 2.2, 2.4), chars=[K(brow='surprised'), Hkc(), Ac()])
    add('c16', 'stage', 'l16', bg=('court', {}), cam=S.close(Hkc(), 2.3, 2.5), chars=[K(), Hkc(brow='neutral'), Ac()])
    add('c17a', 'stage', 'l17', 'a', bg=('court', {}), cam=S.close(K(), 2.2, 2.4), chars=[K(brow='determined', point=True), Hkc(), Ac()])
    add('c17b', 'stage', 'l17', 'b', bg=('court', {}), cam=S.close(K(), 2.4, 2.6), chars=[K(brow='happy'), Hkc(), Ac()])
    add('c18', 'stage', 'l18', bg=('court', {}), cam=S.close(Ac(), 2.5, 2.7), chars=[K(), Hkc(), Ac(brow='happy', mouth='smirk')])
    add('hafta', 'black', dur=2.0, text='Bir hafta sonra...')
    add('w0', 'window', dur=2.8)
    add('s19', 'stage', 'l19', bg=st, cam=S.close(Y(), 2.3, 2.5), chars=[Y(brow='happy', wave=True), A()])
    add('m20', 'mortar', 'l20', extra=0.3, zoom=(1.0, 1.15), old=True)
    add('d21', 'stage', 'l21', bg=('shop', {'mortar': True}), cam=S.close(H(), 2.3, 2.6), chars=[H(brow='surprised', point=True), As()])
    add('m22', 'mortar', 'l22', extra=0.8, zoom=(1.2, 1.6), old=True, flash=True)
    add('son', 'end', dur=3.5)
