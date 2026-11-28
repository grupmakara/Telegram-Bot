"""Bölüm 14 - Kırık Havan"""
OUT = 'proje14'
TITLE = ('BÖLÜM 14', 'Kırık Havan')
HOOK = ('Havan çatladı...', 'Ve iki dünya arasındaki <b>ses kesiliyor!</b>')
END = ('Yüz cana ulaşabilecekler mi?', 'Bölüm 15 yakında...')
CTA = True  # bitişte takip/beğeni animasyonu
HOOK_CUT = ('l3', 'Elif', 'h0', 'until')
LINES = {
    'h0': ('b14_h0.wav', 'ayse', 'Ayşe! Beni duyuyor musun?', 2.2),
    'l1': ('b14_l1.wav', 'huseyin', 'Taşı atan kaçtı, kızım. Ama havan... Ortadan çatlamış.', 3.8, 0.5, 'sad, worried'),
    'l2': ('b14_l2.wav', 'ayse', 'Işığı çok sönük. Bu gece Ayşe\'yle konuşabilecek miyim?', 3.8, 0.5, 'worried, quiet'),
    'l3': ('b14_l3.wav', 'ayse', 'Ayşe! Beni duyuyor musun? Elif ben!', 2.8, 0.7, 'urgent, calling out'),
    'l4': ('b14_l4.wav', 'ayseg', 'Elif... ses... kesik... Duyamıyorum...', 3.2, 0.6, 'faint, whispering, worried'),
    'l5': ('b14_l5.wav', 'ayseg', 'Kemal Bey! Havanın ışığı titriyor. Elif\'i zor duyuyorum!', 3.8, 0.7, 'panicked, scared'),
    'l6': ('b14_l6.wav', 'kemal', 'Sakin ol, kızım. Dedemin kitabında havanla ilgili bir sayfa vardı. Bakalım.', 4.6, 0.5, 'calm, reassuring'),
    'l7': ('b14_l7.wav', 'ayseg', 'Burada yazıyor: Havan kırılırsa, iki el aynı anda tutmalı. Dolunay gecesi.', 5.0, 0.6, 'reading slowly, hopeful'),
    'l8': ('b14_l8.wav', 'kemal', 'Dolunay... Yarın gece dolunay var!', 2.6, 0.6, 'excited'),
    'l9': ('b14_l9.wav', 'ayseg', 'Ama Elif\'e nasıl haber vereceğim? Ses gitti!', 3.2, 0.6, 'worried, desperate'),
    'l10': ('b14_l10.wav', 'kemal', 'Kitabın kenarına bir not düşmüşler. Elif\'in de aynı kitabı bulması gerek.', 4.6, 0.5, 'thoughtful'),
    'l11': ('b14_l11.wav', 'kadi', 'Kızım, Lokman Efendi\'nin mektubunu sandıktan çıkardım. Arkasında bir şey daha yazıyor.', 5.2, 0.5, 'serious, slow'),
    'l12': ('b14_l12.wav', 'ayse', 'Dolunay gecesi, iki el aynı anda... Ayşe de bunu okumuş olmalı!', 4.2, 0.7, 'excited, realization'),
    'l13': ('b14_l13.wav', 'yusuf', 'Ayşe abla! Merdivenden düştüm, kolum...', 2.8, 0.7, 'crying, in pain'),
    'l14': ('b14_l14.wav', 'ayse', 'Kıpırdama Yusuf. Kemik kırılmamış, çıkmış. Babam tutsun, ben yerine oturtacağım.', 5.2, 0.5, 'calm, focused'),
    'l15': ('b14_l15.wav', 'yusuf', 'Ah! Geçti... Kolumu oynatabiliyorum!', 2.8, 0.7, 'relieved, laughing'),
    'l16': ('b14_l16.wav', 'ayse', 'Altmış dört. Hadi dolunay, gel artık.', 2.8, 0.5, 'quiet, hopeful, counting'),
    'l17': ('b14_l17.wav', 'ayse', 'Ayşe, şimdi! İki el, aynı anda!', 2.6, 0.7, 'urgent, determined'),
    'l18': ('b14_l18.wav', 'ayseg', 'Tutuyorum! Elif, seni duyuyorum! Çatlak kapanıyor!', 3.6, 0.8, 'joyful, amazed'),
    'l19': ('b14_l19.wav', 'ayse', 'Ama havan bu kez kırmızı parlıyor. Lokman Efendi... bunu yazmamıştı.', 4.6, 0.5, 'whispering, worried, slow'),
}
SPLITS = {'l7': ('Dolunay', 0.7), 'l14': ('Babam', 0.6)}


def plan(add, S):
    ph = ('pharmacy', {})
    shopm = ('shop', {'mortar': True})
    court = ('court', {})
    H = lambda **o: S.C('huseyin', 280, 1720, **o)
    A = lambda **o: S.C('ayse', 800, 1650, **o)
    Ac = lambda **o: S.C('ayse', 830, 1690, **o)
    G = lambda **o: S.C('ayseg', 780, 1420, **o)
    K = lambda **o: S.C('kemal', 300, 1760, 0.95, **o)
    Kd = lambda **o: S.C('kadi', 540, 1330, 0.92, **o)
    Y = lambda **o: S.C('yusuf', 520, 1800, 0.9, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=shopm, hook=True, cam=S.close(A(), 2.6, 3.1), chars=[H(), A(brow='worried', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub='Elif kırk günlük karantinayla şehri vebadan korudu. Ama öfkeli kalabalığın taşı havanı çatlattı.')
    add('m0', 'mortar', dur=2.6, zoom=(1.0, 1.2), old=True, crack=True)
    add('s1', 'stage', 'l1', bg=shopm, cam=S.close(H(), 2.3, 2.5), chars=[H(brow='worried'), A(brow='worried')])
    add('s2', 'stage', 'l2', bg=shopm, cam=S.close(A(), 2.4, 2.6), chars=[H(), A(brow='worried', mouth='flat')])
    add('gece', 'black', dur=1.8, text='O gece...')
    add('m3', 'mortar', 'l3', zoom=(1.1, 1.3), old=True, crack=True)
    add('e4', 'stage', 'l4', bg=ph, cam=((2.3, 780, 1100), (2.6, 780, 1100)), chars=[G(brow='worried', mouth='flat')])
    add('yer', 'black', dur=1.8, text='İstanbul, 2026')
    add('e5', 'stage', 'l5', bg=ph, cam=S.close(G(), 2.4, 2.7), chars=[K(), G(eyes='wide', brow='worried', mouth='o', shock=True)])
    add('e6', 'stage', 'l6', bg=ph, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='neutral'), G(brow='worried')])
    add('e7a', 'stage', 'l7', 'a', bg=ph, cam=((2.2, 760, 1100), (2.4, 760, 1100)), chars=[G(brow='confused', mouth='flat')])
    add('e7b', 'stage', 'l7', 'b', bg=ph, cam=S.close(G(), 2.5, 2.8), chars=[K(), G(eyes='wide', brow='surprised', mouth='o')])
    add('e8', 'stage', 'l8', bg=ph, cam=S.close(K(), 2.2, 2.5), chars=[K(brow='happy', point=True), G()])
    add('e9', 'stage', 'l9', bg=ph, cam=S.close(G(), 2.4, 2.6), chars=[K(), G(brow='worried', mouth='flat')])
    add('e10', 'stage', 'l10', bg=ph, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='confused'), G()])
    add('yer2', 'black', dur=1.8, text='İstanbul, 1665')
    add('c11', 'stage', 'l11', bg=court, cam=S.close(Kd(), 2.2, 2.5), chars=[Kd(brow='worried'), Ac()])
    add('c12', 'stage', 'l12', bg=court, cam=S.close(Ac(), 2.5, 2.8), chars=[Kd(), Ac(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('s13', 'stage', 'l13', bg=shopm, cam=S.close(Y(), 2.3, 2.6), chars=[H(), Y(brow='worried'), A(brow='worried')])
    add('s14a', 'stage', 'l14', 'a', bg=shopm, cam=S.close(A(), 2.4, 2.6), chars=[H(), Y(brow='worried'), A(brow='determined', mouth='flat')])
    add('s14b', 'stage', 'l14', 'b', bg=shopm, cam=((1.2, 520, 1300), (1.3, 520, 1250)), chars=[H(brow='worried'), Y(brow='worried'), A(brow='determined')])
    add('s15', 'stage', 'l15', bg=shopm, cam=S.close(Y(), 2.3, 2.6), chars=[H(), Y(brow='happy', wave=True), A(brow='happy')])
    add('s16', 'stage', 'l16', bg=shopm, cam=S.close(A(), 2.5, 2.8), chars=[H(), A(brow='happy', mouth='smirk')])
    add('dolunay', 'black', dur=2.0, text='Dolunay gecesi...')
    add('m17', 'mortar', 'l17', zoom=(1.0, 1.3), old=True, crack=True, touch=True)
    add('e18', 'stage', 'l18', bg=ph, cam=S.close(G(), 2.5, 2.8), chars=[K(brow='happy'), G(brow='happy', mouth='o')])
    add('m18', 'mortar', dur=2.4, zoom=(1.3, 1.1), touch=True, flash=True)
    add('m19', 'mortar', 'l19', extra=0.8, zoom=(1.1, 1.4), old=True, color='#FF4A3D')
    add('sonraki', 'black', dur=4.5, text='Sonraki bölümde...', sub='Kırmızı ışık ne anlama geliyor? Sayaç doksan dokuza yaklaşıyor...')
    add('son', 'end', dur=5.2)
