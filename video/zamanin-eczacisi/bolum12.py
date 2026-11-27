"""Bölüm 12 - Eski Kitap"""
OUT = 'proje12'
TITLE = ('BÖLÜM 12', 'Eski Kitap')
HOOK = ('Yüz yıllık bir kitap...', 'Son sayfada <b>Elif\'in yüzü</b> var!')
END = ('Lokman Efendi Elif\'i nereden biliyordu?', 'Bölüm 13 yakında...')
HOOK_CUT = ('l18', 'Yani', 'h0', 'until')
LINES = {
    'h0': ('b12_h0.wav', 'ayseg', 'Bu resimdeki benim yüzüm!', 2.0),
    'l1': ('b12_l1.wav', 'kemal', 'Elif, dedemin sandığından bunu çıkardım. Yüzlerce yıllık bir kitap.', 4.4, 0.5, 'curious, calm'),
    'l2': ('b12_l2.wav', 'kemal', 'Kapağında bir hilal ve bir yılan var. Senin havanın üstündeki gibi.', 4.4, 0.5, 'puzzled, slow'),
    'l3': ('b12_l3.wav', 'ayseg', 'Lokman Efendi\'nin mührü...', 2.2, 0.5, 'whispering, amazed'),
    'l4': ('b12_l4.wav', 'kemal', 'Lokman mı? Dedemin dedesinin dedesi... Nereden biliyorsun bu adı?', 4.2, 0.6, 'surprised, suspicious'),
    'l5': ('b12_l5.wav', 'kemal', 'Neyse. Kimse okuyamadı zaten. Eski yazı, Arap harfleri.', 3.8, 0.5, 'tired, dismissive'),
    'l6': ('b12_l6.wav', 'ayseg', 'Ben okuyabilirim.', 1.6, 0.5, 'quiet, confident'),
    'l7': ('b12_l7.wav', 'ayseg', 'Bu kitap, Attar Lokman\'ın şifa defteri. Her sayfada bir bitki, bir hastalık.', 5.0, 0.5, 'reading slowly, focused'),
    'l8': ('b12_l8.wav', 'kemal', 'Elif... Sen bu yazıyı nasıl okuyorsun? Ben yıllardır çözemedim!', 4.0, 0.6, 'shocked'),
    'l9': ('b12_l9.wav', 'ayseg', 'Kemal Bey, size bir şey söylemem lazım. Ama önce bana inanacağınıza söz verin.', 5.0, 0.5, 'serious, hesitant'),
    'l10': ('b12_l10.wav', 'kemal', 'Söz veriyorum, kızım. Seni tanırım; sen yalan söylemezsin.', 3.8, 0.5, 'gentle, warm'),
    'l11': ('b12_l11.wav', 'ayseg', 'Ben Elif değilim. Adım Ayşe. Bin altı yüz altmış beşten geliyorum.', 4.6, 0.6, 'emotional, trembling'),
    'l12': ('b12_l12.wav', 'kemal', 'Bu... Bu imkânsız.', 2.0, 0.5, 'stunned, slow, quiet'),
    'l13': ('b12_l13.wav', 'kemal', 'Ama dedem hep derdi: Bir gün havan geri döner, yanında da bir kız gelir.', 5.2, 0.5, 'slow, remembering, mysterious'),
    'l14': ('b12_l14.wav', 'ayseg', 'Bakın, kitabın sonunda bir not var. Veba gelecek. Kapıları kapatın, suyu kaynatın.', 5.6, 0.6, 'reading, worried'),
    'l15': ('b12_l15.wav', 'ayseg', 'Elif! Elif! Lokman Efendi vebayı yazmış! Size geliyor!', 3.6, 0.7, 'urgent, whispering'),
    'l16': ('b12_l16.wav', 'ayse', 'Veba mı? Eğer doğruysa... yüzlerce insan tehlikede.', 3.6, 0.6, 'alarmed, quiet'),
    'l17': ('b12_l17.wav', 'ayseg', 'Bir sayfa daha var. Bir resim... Beyaz önlüklü bir kız.', 4.0, 0.5, 'whispering, slow, nervous'),
    'l18': ('b12_l18.wav', 'ayseg', 'Bu resimdeki benim yüzüm! Yani... Elif\'in yüzü!', 3.4, 0.7, 'shocked, scared'),
}
SPLITS = {'l14': ('Veba', 0.42), 'l7': ('Her', 0.62)}


def plan(add, S):
    ph = ('pharmacy', {})
    shopm = ('shop', {'mortar': True})
    G = lambda **o: S.C('ayseg', 780, 1420, **o)
    K = lambda **o: S.C('kemal', 300, 1760, 0.95, **o)
    A = lambda **o: S.C('ayse', 800, 1400, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=ph, hook=True, cam=S.close(G(), 2.4, 2.9), chars=[K(), G(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub="Havanın mührü Attar Lokman Efendi'ye aitti. Kemal Bey'in dedesinin eczanesinin adı: Lokman Eczanesi.")
    add('yer', 'black', dur=2.0, text='İstanbul, 2026')
    add('eo', 'stage', dur=2.6, bg=ph, cam=((1.0, 540, 960), (1.06, 540, 1000)), chars=[])
    add('e1', 'stage', 'l1', bg=ph, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='happy'), G()])
    add('e2', 'stage', 'l2', bg=ph, cam=((1.2, 520, 1250), (1.3, 520, 1200)), chars=[K(brow='confused', point=True), G()])
    add('e3', 'stage', 'l3', bg=ph, cam=S.close(G(), 2.5, 2.8), chars=[K(), G(eyes='wide', brow='surprised', mouth='o')])
    add('e4', 'stage', 'l4', bg=ph, cam=S.close(K(), 2.2, 2.5), chars=[K(brow='surprised'), G()])
    add('e5', 'stage', 'l5', bg=ph, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='tired'), G()])
    add('e6', 'stage', 'l6', extra=0.4, bg=ph, cam=S.close(G(), 2.5, 2.8), chars=[K(), G(brow='determined', mouth='smirk')])
    add('e7', 'stage', 'l7', bg=ph, cam=((2.2, 760, 1100), (2.4, 760, 1100)), chars=[G(brow='determined', mouth='flat')])
    add('e8', 'stage', 'l8', bg=ph, cam=S.close(K(), 2.2, 2.5), chars=[K(brow='surprised', point=True), G()])
    add('e9', 'stage', 'l9', bg=ph, cam=S.close(G(), 2.4, 2.6), chars=[K(), G(brow='worried', mouth='flat')])
    add('e10', 'stage', 'l10', bg=ph, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='happy'), G()])
    add('e11', 'stage', 'l11', extra=0.5, bg=ph, cam=S.close(G(), 2.5, 2.9), chars=[K(), G(brow='worried', mouth='flat')])
    add('e12', 'stage', 'l12', extra=0.4, bg=ph, cam=S.close(K(), 2.3, 2.7), chars=[K(brow='surprised'), G()])
    add('e13', 'stage', 'l13', bg=ph, cam=((1.2, 400, 1250), (1.4, 340, 1250)), chars=[K(brow='worried'), G(brow='surprised')])
    add('e14a', 'stage', 'l14', 'a', bg=ph, cam=S.close(G(), 2.4, 2.6), chars=[K(), G(brow='worried', mouth='flat')])
    add('e14b', 'stage', 'l14', 'b', bg=ph, cam=((1.2, 540, 1250), (1.3, 540, 1250)), chars=[K(brow='worried'), G(brow='worried', mouth='o')])
    add('gece', 'black', dur=1.8, text='O gece...')
    add('e15', 'stage', 'l15', bg=ph, cam=((2.3, 780, 1100), (2.6, 780, 1100)), chars=[G(eyes='wide', brow='worried', mouth='o')])
    add('m16', 'mortar', 'l16', zoom=(1.0, 1.2), old=True)
    add('b16', 'stage', dur=2.4, bg=shopm, cam=S.close(A(), 2.5, 2.8), chars=[A(brow='worried', mouth='flat')])
    add('e17', 'stage', 'l17', bg=ph, cam=((2.3, 780, 1100), (2.5, 780, 1100)), chars=[G(brow='confused', mouth='flat')])
    add('e18', 'stage', 'l18', extra=0.8, bg=ph, cam=S.close(G(), 2.6, 3.2), chars=[G(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('sonraki', 'black', dur=4.5, text='Sonraki bölümde...', sub='İstanbul\'da veba söylentisi. Elif şehri uyarabilecek mi?')
    add('son', 'end', dur=4.0)
