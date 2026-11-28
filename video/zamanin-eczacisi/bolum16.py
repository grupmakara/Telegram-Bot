"""Bölüm 16 - Eve Dönüş (2. sezon finali)"""
OUT = 'proje16'
TITLE = ('BÖLÜM 16', 'Eve Dönüş', '2. SEZON FİNALİ')
HOOK = ('Yüzüncü can...', 'Ve havan <b>son kez</b> açılıyor!')
END = ('2. Sezon Finali', '3. sezonda görüşmek üzere...')
HOOK_CUT = ('l13', 'Yüz', 'h0', 'until')
CTA = True  # bitişte takip/beğeni animasyonu
LINES = {
    'h0': ('b16_h0.wav', 'ayse', 'Yüz can. Havan açılıyor!', 2.2),
    'l1': ('b16_l1.wav', 'ayse', 'Baba, yat. Kıpırdama. Yusuf, söğüt kabuğunu getir, ezip çiğneyecek.', 4.6, 0.6, 'urgent, calm, focused'),
    'l2': ('b16_l2.wav', 'hekim', 'Söğüt kabuğu mu? Ateş için değil miydi o?', 2.8, 0.6, 'confused, worried'),
    'l3': ('b16_l3.wav', 'ayse', 'Kanı inceltir, Ahmet Efendi. Kalbe giden yolu açmaya yardım eder. Benim zamanımda bunun hapı var.', 6.0, 0.6, 'explaining, urgent'),
    'l4': ('b16_l4.wav', 'ayse', 'Baba, yavaş nefes al. Benimle. İçeri... dışarı...', 3.8, 0.5, 'soft, calm, gentle'),
    'l5': ('b16_l5.wav', 'huseyin', 'Ağrı... azalıyor, kızım. Taş kalkıyor gibi...', 3.4, 0.5, 'weak, relieved, slow'),
    'l6': ('b16_l6.wav', 'hekim', 'Nabzı düzeldi. Allah\'ım... Kurtuldu.', 3.0, 0.6, 'amazed, relieved'),
    'l7': ('b16_l7.wav', 'huseyin', 'Kızım... Sen benim kızım değilsin, değil mi? Ama kızımı bana sen geri getireceksin.', 5.6, 0.5, 'emotional, gentle, slow'),
    'l8': ('b16_l8.wav', 'ayse', 'Evet, baba. Bu gece. Ve o, seni çok seviyor.', 3.6, 0.5, 'emotional, crying softly'),
    'l9': ('b16_l9.wav', 'ayse', 'Yüz can. Havan hiç bu kadar parlak olmamıştı.', 3.2, 0.6, 'whispering, amazed'),
    'l10': ('b16_l10.wav', 'kemal', 'Kızım, git. Babana kavuş. Ama bunu al, dedemden kalan son mektup.', 4.6, 0.5, 'emotional, warm'),
    'l11': ('b16_l11.wav', 'ayseg', 'Elif! Lokman Efendi\'nin son mektubunu okuyorum!', 3.0, 0.7, 'excited, urgent'),
    'l12': ('b16_l12.wav', 'ayseg', 'Ben de bir zamanlar senin gibiydim. Uzak bir yüzyılın eczacısı. Havan beni getirdi. Ben dönmedim; kaldım ve bu şehre şifa oldum.', 8.4, 0.5, 'reading slowly, amazed'),
    'l13': ('b16_l13.wav', 'ayse', 'Yüz can. Havan açılıyor! Ayşe, şimdi! İki el, aynı anda!', 3.8, 0.8, 'urgent, emotional'),
    'l14': ('b16_l14.wav', 'ayseg', 'Hoşça kal, Elif! Babama iyi baktığın için... teşekkür ederim!', 3.8, 0.7, 'emotional, crying with joy'),
    'l15': ('b16_l15.wav', 'ayse', 'Baba! Benim, Ayşe! Gerçekten benim!', 2.8, 0.8, 'crying with joy'),
    'l16': ('b16_l16.wav', 'huseyin', 'Kızım! Gözlerinden tanıdım. Hoş geldin, kızım.', 3.6, 0.6, 'emotional, joyful, crying'),
    'l17': ('b16_l17.wav', 'kemal', 'Elif? Kızım... sen misin?', 2.2, 0.6, 'hesitant, hopeful'),
    'l18': ('b16_l18.wav', 'ayseg', 'Benim, Kemal Bey. Elif. Eve döndüm.', 3.0, 0.6, 'emotional, smiling, tired'),
    'l19': ('b16_l19.wav', 'kemal', 'Kitabın son sayfası değişti, bak. Yeni bir resim var. Beyaz önlüklü bir çocuk...', 5.0, 0.5, 'mysterious, slow, surprised'),
    'l20': ('b16_l20.wav', 'ayseg', 'Ben Elif. Bir eczacıyım. Ve havan... yeni birini bekliyor.', 4.4, 0.5, 'calm, mysterious, narration'),
}
SPLITS = {'l3': ('Benim', 0.7), 'l12': ('Ben', 0.5), 'l13': ('Ayşe', 0.42)}


def plan(add, S):
    shopm = ('shop', {'mortar': True})
    ph = ('pharmacy', {})
    H = lambda **o: S.C('huseyin', 280, 1720, **o)
    A = lambda **o: S.C('ayse', 800, 1650, **o)
    G = lambda **o: S.C('ayseg', 780, 1420, **o)
    K = lambda **o: S.C('kemal', 300, 1760, 0.95, **o)
    Hk = lambda **o: S.C('hekim', 250, 1820, 0.95, **o)
    Hs = lambda **o: S.C('huseyin', 300, 1720, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=shopm, hook=True, cam=S.close(A(), 2.6, 3.1), chars=[H(), A(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub='Sayaç doksan dokuza ulaştı. Ve Hüseyin göğsünü tutarak yere yığıldı.')
    add('s1', 'stage', 'l1', bg=shopm, cam=((1.3, 520, 1250), (1.45, 560, 1250)), chars=[H(brow='tired', arm=-30), A(brow='determined', point=True)])
    add('s2', 'stage', 'l2', bg=shopm, cam=S.close(Hk(), 2.3, 2.5), chars=[Hk(brow='confused'), A()])
    add('s3a', 'stage', 'l3', 'a', bg=shopm, cam=S.close(A(), 2.4, 2.6), chars=[Hk(), A(brow='determined', mouth='flat')])
    add('s3b', 'jars', 'l3', 'b')
    add('s4', 'stage', 'l4', bg=shopm, cam=((1.3, 520, 1250), (1.4, 520, 1220)), chars=[H(brow='tired'), A(brow='worried', mouth='flat')])
    add('s5', 'stage', 'l5', bg=shopm, cam=S.close(H(), 2.3, 2.5), chars=[H(brow='tired'), A()])
    add('s6', 'stage', 'l6', bg=shopm, cam=S.close(Hk(), 2.3, 2.5), chars=[Hk(brow='happy'), A(brow='happy')])
    add('aksam', 'black', dur=1.8, text='Dolunay gecesi...')
    add('s7', 'stage', 'l7', extra=0.4, bg=shopm, cam=S.close(H(), 2.4, 2.7), chars=[H(brow='worried'), A()])
    add('s8', 'stage', 'l8', extra=0.4, bg=shopm, cam=S.close(A(), 2.6, 2.9), chars=[H(), A(brow='worried', mouth='smirk')])
    add('m9', 'mortar', 'l9', zoom=(1.0, 1.25), old=True)
    add('yer', 'black', dur=1.8, text='İstanbul, 2026')
    add('e10', 'stage', 'l10', bg=ph, cam=S.close(K(), 2.2, 2.5), chars=[K(brow='worried'), G(brow='worried')])
    add('e11', 'stage', 'l11', bg=ph, cam=S.close(G(), 2.4, 2.7), chars=[K(), G(eyes='wide', brow='surprised', mouth='o')])
    add('e12a', 'stage', 'l12', 'a', bg=ph, cam=((2.2, 760, 1100), (2.4, 760, 1100)), chars=[G(brow='confused', mouth='flat')])
    add('e12b', 'stage', 'l12', 'b', bg=ph, cam=S.close(G(), 2.5, 2.9), chars=[K(), G(eyes='wide', brow='surprised', mouth='o')])
    add('m13a', 'mortar', 'l13', 'a', zoom=(1.0, 1.2), old=True, touch=True)
    add('m13b', 'mortar', 'l13', 'b', zoom=(1.2, 1.4), touch=True, flash=True)
    add('e14', 'stage', 'l14', extra=0.6, bg=ph, cam=S.close(G(), 2.5, 2.8), chars=[K(), G(brow='happy', mouth='o')])
    add('beyaz', 'black', dur=1.6, text='...')
    add('s15', 'stage', 'l15', bg=shopm, cam=((1.2, 540, 1250), (1.35, 560, 1250)), chars=[Hs(brow='happy', wave=True), A(eyes='wide', brow='happy', mouth='o')])
    add('s16', 'stage', 'l16', extra=0.5, bg=shopm, cam=S.close(Hs(), 2.3, 2.6), chars=[Hs(brow='happy'), A(brow='happy', mouth='smirk')])
    add('e17', 'stage', 'l17', bg=ph, cam=S.close(K(), 2.2, 2.5), chars=[K(brow='worried'), G(eyes='half', brow='tired')])
    add('e18', 'stage', 'l18', extra=0.5, bg=ph, cam=S.close(G(), 2.4, 2.7), chars=[K(), G(brow='happy', mouth='smirk')])
    add('e19', 'stage', 'l19', bg=ph, cam=((1.2, 400, 1250), (1.4, 360, 1250)), chars=[K(brow='surprised', point=True), G(brow='surprised')])
    add('m20', 'mortar', 'l20', extra=1.0, zoom=(1.0, 1.3))
    add('sonraki', 'black', dur=4.5, text='2. Sezon Finali', sub='Havan yeni birini bekliyor... 3. sezonda görüşmek üzere.')
    add('son', 'end', dur=5.2)
