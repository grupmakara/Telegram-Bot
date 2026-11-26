"""Bölüm 5 - Limandaki Salgın"""
OUT = 'proje5'
TITLE = ('BÖLÜM 5', 'Limandaki Salgın')
HOOK = ('Bir salgın başlıyor...', 'Ve <b>herkes</b> aynı sudan içiyor!')
END = ('Çeşmenin sırrı ne?', 'Bölüm 6 yakında...')
HOOK_CUT = ('l9', 'Herkes', 'h0', 'until')
LINES = {
    'h0': ('b5_h0.wav', 'ayse', 'Bu sudan kimse içmeyecek!', 2.2),
    'l1': ('b5_l1.wav', 'denizci', 'Kimsin sen? Burası kadın işi değil, git buradan!', 3.6, 0.7, 'gruff, dismissive'),
    'l2': ('b5_l2.wav', 'ayse', "Ben attar Hüseyin'in kızıyım. Adamların ölüyor reis, bana izin ver!", 5.0, 0.7, 'urgent, firm'),
    'l3': ('b5_l3.wav', 'riza', "Reis, bu kız Mehmet'i kurtaran kız!", 2.8, 0.6, 'insistent'),
    'l4': ('b5_l4.wav', 'denizci', 'Peki. Ama bir şey olursa, hesabını sen verirsin.', 3.6, 0.5, 'reluctant, gruff'),
    'l5': ('b5_l5.wav', 'ayse', 'Ateş yok ama vücutları kuruyor... Su kaybediyorlar.', 4.0, 0.5, 'focused, worried'),
    'l6': ('b5_l6.wav', 'ayse', 'Reis, adamların suyu nereden içiyor?', 2.8, 0.5, 'quick, serious'),
    'l7': ('b5_l7.wav', 'denizci', 'Şu fıçılardan. Limandaki kuyudan doldurduk.', 3.2, 0.5, 'matter of fact'),
    'l8': ('b5_l8.wav', 'ayse', 'Kuyu... Hastalık sudan geliyor!', 2.8, 0.7, 'realization, whispering then louder'),
    'l9': ('b5_l9.wav', 'ayse', 'Bu sudan kimse içmeyecek! Herkes suyu kaynatsın!', 3.5, 0.9, 'shouting, commanding'),
    'l10': ('b5_l10.wav', 'denizci', 'Kaynatmak mı? Su su işte!', 2.4, 0.6, 'confused, skeptical'),
    'l11': ('b5_l11.wav', 'ayse', 'Suda gözle görülmeyen canlılar var reis. Ateş onları öldürür.', 4.5, 0.5, 'patient, explaining'),
    'l12': ('b5_l12.wav', 'hekim', 'Görülmeyen canlılar mı? Şimdi de cin mi var suda?', 3.8, 0.7, 'sarcastic, mocking'),
    'l13': ('b5_l13.wav', 'ayse', 'Cin değil, efendim. Ama inanmıyorsanız, bekleyin ve görün.', 4.2, 0.5, 'calm, confident'),
    'l14': ('b5_l14.wav', 'ayse', 'Rıza Amca, tuz ve bal getir. Her hastaya kaşık kaşık içireceğiz.', 4.6, 0.5, 'quick, organizing'),
    'l15': ('b5_l15.wav', 'denizci', 'Kızım... Adamlarımın hiçbiri ölmedi. Hiçbiri!', 3.8, 0.8, 'amazed, emotional'),
    'l16': ('b5_l16.wav', 'ayse', 'Suyu kaynatmaya devam edin reis. Hastalık bitmedi.', 3.6, 0.5, 'tired, serious'),
    'l17': ('b5_l17.wav', 'hekim', 'Kaynatılmış su... Nasıl düşünemedim bunu?', 3.2, 0.5, 'quiet, thoughtful, to himself'),
    'l18': ('b5_l18.wav', 'ayse', 'Yirmi üç can... Yetmiş yedi kaldı.', 3.0, 0.5, 'whispering, counting'),
    'l19': ('b5_l19.wav', 'yusuf', "Ayşe Hanım... Ben Hekim Ahmet Efendi'nin çırağıyım. Yusuf.", 4.2, 0.5, 'shy, polite'),
    'l20': ('b5_l20.wav', 'yusuf', 'Size bir şey söylemem lazım. Limandaki kuyu... Hastalık sadece orada değil.', 5.0, 0.6, 'nervous, urgent whisper'),
    'l21': ('b5_l21.wav', 'ayse', 'Ne demek istiyorsun?', 1.8, 0.6, 'alarmed'),
    'l22': ('b5_l22.wav', 'yusuf', 'Bizim mahallenin çeşmesinden içenler de hastalanmaya başladı.', 4.2, 0.6, 'worried'),
}
SPLITS = {'l9': ('Herkes', 0.5), 'l20': ('Limandaki', 0.45)}


def plan(add, S):
    port = ('port', {})
    D = lambda **o: S.C('denizci', 290, 1800, **o)
    A = lambda **o: S.C('ayse', 800, 1600, 0.95, **o)
    R = lambda **o: S.C('riza', 520, 1840, 0.9, **o)
    Hk = lambda **o: S.C('hekim', 260, 1820, **o)
    Y = lambda **o: S.C('yusuf', 290, 1820, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=port, hook=True, cam=S.close(A(), 2.5, 3.0), chars=[D(), A(brow='determined', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub="Kadı, Elif'e yedi gün süre verdi. Limanda gizemli bir hastalık başladı.")
    add('po', 'stage', dur=3.0, bg=port, cam=((1.0, 540, 960), (1.08, 540, 900)), chars=[])
    add('p1', 'stage', 'l1', bg=port, cam=S.close(D(), 2.2, 2.4), chars=[D(brow='determined', point=True), A()])
    add('p2', 'stage', 'l2', bg=port, cam=S.close(A(), 2.4, 2.6), chars=[D(), A(brow='determined', mouth='flat')])
    add('p3', 'stage', 'l3', bg=port, cam=S.close(R(), 2.3, 2.5), chars=[D(), R(brow='worried', point=True), A()])
    add('p4', 'stage', 'l4', bg=port, cam=S.close(D(), 2.2, 2.5), chars=[D(brow='smug'), A()])
    add('p5', 'stage', 'l5', bg=port, cam=S.close(A(), 2.5, 2.7), chars=[D(), A(brow='worried', mouth='flat')])
    add('p6', 'stage', 'l6', bg=port, cam=((1.2, 540, 1300), (1.3, 600, 1300)), chars=[D(), A(brow='confused', mouth='flat')])
    add('p7', 'stage', 'l7', bg=port, cam=((1.4, 220, 1350), (1.6, 180, 1400)), chars=[D(point=True), A()])
    add('p8', 'stage', 'l8', bg=port, cam=S.close(A(), 2.6, 3.0), chars=[D(), A(eyes='wide', brow='surprised', mouth='o')])
    add('p9', 'stage', 'l9', bg=port, cam=((1.2, 600, 1250), (1.4, 700, 1200)), chars=[D(brow='surprised'), A(brow='determined', mouth='o', shock=True)])
    add('p10', 'stage', 'l10', bg=port, cam=S.close(D(), 2.2, 2.4), chars=[D(brow='confused'), A()])
    add('p11', 'stage', 'l11', bg=port, cam=S.close(A(), 2.4, 2.6), chars=[D(), A(brow='neutral')])
    add('p12', 'stage', 'l12', bg=port, cam=S.close(Hk(), 2.3, 2.6), chars=[Hk(brow='smug', point=True), A()])
    add('p13', 'stage', 'l13', bg=port, cam=S.close(A(), 2.5, 2.7), chars=[Hk(), A(brow='smug', mouth='smirk')])
    add('p14', 'stage', 'l14', bg=port, cam=((1.2, 600, 1300), (1.3, 600, 1250)), chars=[R(), A(brow='determined', mouth='flat')])
    add('gun', 'black', dur=2.0, text='Üç gün sonra...')
    add('pw', 'stage', dur=3.0, bg=port, cam=((1.0, 540, 900), (1.1, 560, 960)), chars=[])
    add('p15', 'stage', 'l15', bg=port, cam=S.close(D(), 2.2, 2.5), chars=[D(brow='happy', wave=True), A()])
    add('p16', 'stage', 'l16', bg=port, cam=S.close(A(), 2.4, 2.6), chars=[D(), A(eyes='half', brow='tired', mouth='flat')])
    add('p17', 'stage', 'l17', extra=0.3, bg=port, cam=S.close(Hk(), 2.4, 2.8), chars=[Hk(brow='confused'), A()])
    add('p18', 'bowl', 'l18', extra=0.4)
    add('k0', 'jars', dur=2.4)
    add('p19', 'stage', 'l19', bg=port, cam=((1.2, 520, 1300), (1.3, 480, 1300)), chars=[Y(), A(brow='surprised')])
    add('p20a', 'stage', 'l20', 'a', bg=port, cam=S.close(Y(), 2.3, 2.5), chars=[Y(brow='worried'), A()])
    add('p20b', 'stage', 'l20', 'b', bg=port, cam=S.close(Y(), 2.5, 2.7), chars=[Y(brow='worried'), A()])
    add('p21', 'stage', 'l21', bg=port, cam=S.close(A(), 2.5, 2.7), chars=[Y(), A(brow='surprised', mouth='flat')])
    add('p22', 'stage', 'l22', extra=0.6, bg=port, cam=S.close(Y(), 2.4, 2.9), chars=[Y(brow='worried'), A()])
    add('son', 'end', dur=3.5)
