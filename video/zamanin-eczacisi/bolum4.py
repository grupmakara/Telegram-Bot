"""Bölüm 4 - Kadı'nın Huzurunda"""
OUT = 'proje4'
TITLE = ('BÖLÜM 4', "Kadı'nın Huzurunda")
HOOK = ('Mahkemede tek başına...', 'Ya <b>suçlu</b> çıkarsa?')
END = ('Limandaki salgını durdurabilecek mi?', 'Bölüm 5 yakında...')
HOOK_CUT = ('l3', 'Ölüleri', 'h0', 'until')
LINES = {
    'h0': ('b4_h0.wav', 'hekim', 'Bu kız bir cadıdır, Kadı Efendi!', 2.5),
    'l1': ('b4_l1.wav', 'huseyin', 'Kızım, Kadı Efendi sert biridir. Ne olur, dikkatli konuş.', 4.2, 0.5, 'worried, quiet'),
    'l2': ('b4_l2.wav', 'ayse', 'Merak etme baba. Gerçeği söyleyeceğim, o kadar.', 3.5, 0.5, 'calm, confident'),
    'l3': ('b4_l3.wav', 'hekim', 'Bu kız bir cadıdır, Kadı Efendi! Ölüleri diriltiyor!', 4.0, 0.9, 'angry, accusing, loud'),
    'l4': ('b4_l4.wav', 'kadi', 'Sessiz olun! Kızım, söyle bakalım... Bu çocuğu nasıl iyileştirdin?', 5.0, 0.6, 'stern, slow, authoritative'),
    'l5': ('b4_l5.wav', 'ayse', 'Büyüyle değil, Kadı Efendi. Söğüt kabuğu, tuz, bal ve sabırla.', 4.5, 0.5, 'calm, respectful'),
    'l6': ('b4_l6.wav', 'hekim', 'Yalan! Hiçbir hekim bunu bilmez!', 2.5, 0.8, 'angry, shouting'),
    'l7': ('b4_l7.wav', 'fatma', 'Kadı Efendi, oğlum ölüyordu. Bu kız onu geri getirdi. Ben şahidim!', 5.0, 0.7, 'emotional, pleading'),
    'l9': ('b4_l9.wav', 'kadi', 'Hmm... Madem bu kadar biliyorsun, bana bir bak bakalım.', 4.0, 0.5, 'curious, testing, slow'),
    'l10': ('b4_l10.wav', 'ayse', 'Elleriniz titriyor... Dudaklarınız kuru... Çok su içiyor, sık sık kalkıyorsunuz, değil mi?', 6.5, 0.5, 'observant, careful, slow'),
    'l11': ('b4_l11.wav', 'kadi', 'Bunu... bunu nereden bildin?', 2.5, 0.6, 'shocked, quiet'),
    'l12': ('b4_l12.wav', 'ayse', 'Kanınızda şeker çok, Kadı Efendi. Tatlıyı ve beyaz ekmeği bırakın. Her gün yürüyün.', 6.0, 0.5, 'confident, kind'),
    'l13': ('b4_l13.wav', 'hekim', "Saçmalık! Kadı Efendi'ye perhiz mi öğretecek?", 3.2, 0.8, 'mocking, angry'),
    'l14': ('b4_l14.wav', 'kadi', 'Susun, Ahmet Efendi! Bu kızın gözü keskin.', 3.2, 0.7, 'commanding'),
    'l15': ('b4_l15.wav', 'kadi', 'Sana yedi gün veriyorum. Yedi gün içinde sözlerin doğru çıkarsa, serbestsin.', 5.5, 0.5, 'slow, solemn'),
    'l16': ('b4_l16.wav', 'ayse', 'Yedi gün yeter, Kadı Efendi.', 2.2, 0.5, 'determined'),
    'l17': ('b4_l17.wav', 'hekim', 'Yedi gün... Bakalım yedi gün dayanabilecek misin?', 3.6, 0.6, 'whispering, threatening'),
    'l18': ('b4_l18.wav', 'huseyin', 'Kızım, yüreğim ağzıma geldi!', 2.4, 0.7, 'relieved, laughing nervously'),
    'l19': ('b4_l19.wav', 'ayse', "Daha bitmedi baba. Şimdi Kadı Efendi'yi iyileştirmemiz lazım.", 4.0, 0.5, 'serious'),
    'l20': ('b4_l20.wav', 'riza', 'Ayşe kızım! Limanda gemiciler bir bir düşüyor!', 3.5, 0.9, 'panicked, out of breath'),
    'l21': ('b4_l21.wav', 'ayse', 'Ne? Nasıl bir hastalık bu?', 2.2, 0.7, 'alarmed'),
    'l22': ('b4_l22.wav', 'riza', 'Bilmiyorum... Kusuyorlar, kuruyup gidiyorlar!', 3.2, 0.8, 'scared'),
    'l23': ('b4_l23.wav', 'ayse', 'Kusma... ishal... Bu kolera olabilir!', 3.0, 0.6, 'whispering, shocked realization'),
}
SPLITS = {'l10': ('Çok', 0.6), 'l12': ('Tatlıyı', 0.45)}


def plan(add, S):
    court, street = ('court', {}), ('street', {'fountain': False})
    K = lambda **o: S.C('kadi', 540, 1330, 0.92, **o)
    Hk = lambda **o: S.C('hekim', 210, 1860, **o)
    A = lambda **o: S.C('ayse', 830, 1690, **o)
    F = lambda **o: S.C('fatma', 240, 1700, 0.95, **o)
    Hs = lambda **o: S.C('huseyin', 300, 1820, **o)
    As = lambda **o: S.C('ayse', 800, 1650, **o)
    R = lambda **o: S.C('riza', 280, 1820, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=court, hook=True, cam=S.close(Hk(), 2.3, 2.8), chars=[K(), Hk(brow='determined', point=True), A()])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub="Subaşı, Elif'i büyücülükle suçlayıp Kadı'nın huzuruna götürmek için geldi.")
    add('so', 'stage', dur=2.6, bg=street, cam=((1.0, 540, 960), (1.1, 540, 1040)), chars=[Hs(), As()])
    add('s1', 'stage', 'l1', bg=street, cam=S.close(Hs(), 2.2, 2.4), chars=[Hs(brow='worried'), As()])
    add('s2', 'stage', 'l2', bg=street, cam=S.close(As(), 2.4, 2.6), chars=[Hs(), As(brow='determined', mouth='flat')])
    add('co', 'stage', dur=3.0, bg=court, cam=((1.0, 540, 960), (1.08, 540, 1000)), chars=[K(), Hk(), A()])
    add('c3', 'stage', 'l3', bg=court, cam=((1.2, 400, 1250), (1.5, 260, 1150)), chars=[K(brow='worried'), Hk(brow='determined', point=True), A(brow='worried', mouth='flat')])
    add('c4', 'stage', 'l4', bg=court, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='determined'), Hk(), A()])
    add('c5', 'stage', 'l5', bg=court, cam=S.close(A(), 2.4, 2.6), chars=[K(), Hk(), A(brow='determined', mouth='flat')])
    add('c6', 'stage', 'l6', bg=court, cam=S.close(Hk(), 2.3, 2.6), chars=[K(), Hk(brow='determined', point=True), A()])
    add('c7', 'stage', 'l7', bg=court, cam=S.close(F(), 2.2, 2.4), chars=[K(), F(brow='worried', mouth='flat'), A()])
    add('c9', 'stage', 'l9', bg=court, cam=S.close(K(), 2.2, 2.5), chars=[K(brow='smug'), Hk(), A()])
    add('c10a', 'stage', 'l10', 'a', bg=court, cam=S.close(A(), 2.5, 2.7), chars=[K(), Hk(), A(brow='confused', mouth='flat')])
    add('c10b', 'stage', 'l10', 'b', bg=court, cam=S.close(K(), 2.4, 2.6), chars=[K(brow='surprised'), Hk(), A()])
    add('c11', 'stage', 'l11', bg=court, cam=S.close(K(), 2.6, 2.9), chars=[K(brow='surprised'), Hk(), A()])
    add('c12a', 'stage', 'l12', 'a', bg=court, cam=S.close(A(), 2.5, 2.6), chars=[K(), Hk(), A(brow='determined', mouth='flat')])
    add('c12b', 'stage', 'l12', 'b', bg=court, cam=((1.2, 600, 1300), (1.3, 640, 1300)), chars=[K(brow='surprised'), Hk(brow='surprised'), A(brow='happy')])
    add('c13', 'stage', 'l13', bg=court, cam=S.close(Hk(), 2.3, 2.5), chars=[K(), Hk(brow='smug', point=True), A()])
    add('c14', 'stage', 'l14', bg=court, cam=S.close(K(), 2.3, 2.6), chars=[K(brow='determined', point=True), Hk(), A()])
    add('c15', 'stage', 'l15', extra=0.3, bg=court, cam=((1.0, 540, 1100), (1.3, 540, 1000)), chars=[K(), Hk(brow='worried'), A(brow='worried', mouth='flat')])
    add('c16', 'stage', 'l16', extra=0.3, bg=court, cam=S.close(A(), 2.6, 3.0), chars=[K(), Hk(), A(brow='determined', mouth='smirk')])
    add('c17', 'stage', 'l17', extra=0.3, bg=('door', {'crowd': False}), cam=S.close(S.C('hekim', 540, 1600, 0.95), 2.1, 2.5), chars=[S.C('hekim', 540, 1600, 0.95, brow='determined')])
    add('w0', 'window', dur=2.6)
    add('s18', 'stage', 'l18', bg=street, cam=S.close(Hs(), 2.2, 2.4), chars=[Hs(brow='happy'), As()])
    add('s19', 'stage', 'l19', bg=street, cam=S.close(As(), 2.4, 2.6), chars=[Hs(), As(brow='determined', mouth='flat')])
    add('st0', 'stage', dur=2.4, bg=street, cam=((1.0, 540, 960), (1.1, 540, 1000)), chars=[])
    add('s20', 'stage', 'l20', bg=street, cam=((1.0, 540, 960), (1.4, 300, 1200)), chars=[R(brow='worried', wave=True), As(brow='surprised')])
    add('s21', 'stage', 'l21', bg=street, cam=S.close(As(), 2.5, 2.7), chars=[R(), As(brow='surprised', mouth='o', eyes='wide')])
    add('s22', 'stage', 'l22', bg=street, cam=S.close(R(), 2.3, 2.5), chars=[R(brow='worried'), As()])
    add('s23', 'stage', 'l23', extra=0.6, bg=street, cam=S.close(As(), 2.7, 3.3), chars=[R(), As(brow='worried', mouth='flat', shock=True)])
    add('sonraki', 'black', dur=4.5, text='Sonraki bölümde...', sub='Limanda gemiciler bir bir düşüyor. Elif salgının kaynağını bulabilecek mi?')
    add('son', 'end', dur=3.5)
