"""Bölüm 8 - İki Dünya (1. sezon finali)"""
OUT = 'proje8'
TITLE = ('BÖLÜM 8', 'İki Dünya')
HOOK = ('İki kız yer değiştirdi...', 'Ve <b>sadece biri</b> geri dönebilir mi?')
END = ('1. Sezon Sonu', '2. sezonda görüşmek üzere...')
HOOK_CUT = ('l5', 'Korkma', 'h0', 'until')
LINES = {
    'h0': ('b8_h0.wav', 'ayse', 'Sen benim bedenimdesin, ben de seninkinde!', 3.0),
    'l1': ('b8_l1.wav', 'ayseg', 'Burası çok garip... Duvarlarda kutular, tavanda güneş gibi lambalar...', 5.0, 0.6, 'scared, amazed, whispering'),
    'l2': ('b8_l2.wav', 'ayseg', "Herkes bana Elif diyor. Ama ben Ayşe'yim! Attar Hüseyin'in kızı!", 4.6, 0.8, 'upset, insistent'),
    'l3': ('b8_l3.wav', 'ayse', 'Ayşe! Beni duyabiliyor musun? Ben Elif!', 3.0, 0.8, 'urgent, calling out'),
    'l4': ('b8_l4.wav', 'ayseg', 'Bir ses... Havandan geliyor! Kimsin sen?', 3.2, 0.7, 'startled, scared'),
    'l5': ('b8_l5.wav', 'ayse', 'Sen benim bedenimdesin, ben de seninkinde! Korkma, birlikte çözeceğiz.', 5.0, 0.7, 'emotional, reassuring'),
    'l6': ('b8_l6.wav', 'ayseg', 'Babam... Babam nasıl? İyi mi?', 2.6, 0.7, 'worried, close to tears'),
    'l7': ('b8_l7.wav', 'ayse', 'Baban iyi. Seni çok seviyor. Ben ona iyi bakıyorum, söz.', 4.2, 0.5, 'warm, gentle'),
    'l8': ('b8_l8.wav', 'ayseg', 'Burada bir eczane var... İlaçlar... Ama hiçbirini bilmiyorum!', 4.4, 0.6, 'helpless, worried'),
    'l9': ('b8_l9.wav', 'ayse', 'Ben sana öğretirim. Yüz can kurtarınca ikimiz de evimize döneceğiz.', 4.8, 0.6, 'hopeful, encouraging'),
    'l10': ('b8_l10.wav', 'ayseg', 'Yüz can mı? Ben burada kimi kurtarabilirim ki?', 3.4, 0.6, 'doubtful'),
    'l11': ('b8_l11.wav', 'ayse', 'Sen de bir attarın kızısın Ayşe. Bitkileri benden iyi bilirsin!', 4.4, 0.6, 'encouraging, smiling'),
    'l12': ('b8_l12.wav', 'ayseg', 'Bitkiler... Evet! Onları bilirim!', 2.8, 0.8, 'happy, excited'),
    'l13': ('b8_l13.wav', 'ayse', 'Işık sönüyor... Ayşe! Yarın gece, aynı saatte!', 3.6, 0.8, 'urgent, calling out'),
    'l14': ('b8_l14.wav', 'huseyin', 'Kızım, gece kiminle konuşuyordun?', 2.6, 0.5, 'suspicious, gentle'),
    'l15': ('b8_l15.wav', 'ayse', 'Baba... Sana anlatmam gereken bir şey var. Otur.', 3.6, 0.4, 'serious, hesitant'),
    'l16': ('b8_l16.wav', 'hekim', "Ayşe, Kadı Efendi'den haber var. Bir şifahane açmamıza izin verdi!", 4.6, 0.8, 'excited, proud'),
    'l17': ('b8_l17.wav', 'yusuf', 'Hocam da ben de sizinle çalışacağız!', 2.6, 0.8, 'joyful'),
    'l18': ('b8_l18.wav', 'huseyin', 'Kızım... Kim olursan ol, sen bu ailenin gururusun.', 4.0, 0.6, 'emotional, proud'),
    'l19': ('b8_l19.wav', 'ayse', 'Elli sekiz can daha... Ama artık yalnız değilim.', 3.6, 0.5, 'emotional, hopeful'),
    'l20': ('b8_l20.wav', 'ayse', "Ben Elif. Bir eczacıyım. Ve 1665'te... zamanın eczacısıyım.", 5.0, 0.5, 'calm, proud narration'),
}
SPLITS = {'l5': ('Korkma', 0.55), 'l9': ('Yüz', 0.4), 'l20': ('Ve', 0.5)}


def plan(add, S):
    shopm = ('shop', {'mortar': True})
    G = lambda **o: S.C('ayseg', 560, 1420, **o)
    H = lambda **o: S.C('huseyin', 300, 1700, **o)
    As = lambda **o: S.C('ayse', 800, 1400, **o)
    Hk = lambda **o: S.C('hekim', 230, 1760, 0.95, **o)
    Y = lambda **o: S.C('yusuf', 520, 1800, 0.9, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=shopm, hook=True, cam=S.close(As(), 2.7, 3.2), chars=[H(), As(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub="Elif, Hekim'in kızını kurtardı. Havanda gerçek Ayşe'nin sesini duydu.")
    add('yer', 'black', dur=2.0, text='İstanbul, 2026')
    add('eo', 'stage', dur=2.6, bg=('pharmacy', {}), cam=((1.0, 540, 960), (1.06, 540, 1000)), chars=[])
    add('e1', 'stage', 'l1', bg=('pharmacy', {}), cam=((1.0, 540, 960), (1.12, 560, 1060)), chars=[G(eyes='wide', brow='worried', mouth='flat')])
    add('e2', 'stage', 'l2', bg=('pharmacy', {}), cam=((2.3, 560, 1080), (2.5, 560, 1080)), chars=[G(brow='worried', mouth='flat')])
    add('yer2', 'black', dur=2.0, text='İstanbul, 1665')
    add('m3', 'mortar', 'l3', zoom=(1.0, 1.2), old=True)
    add('e4', 'stage', 'l4', bg=('pharmacy', {}), cam=((2.3, 600, 1100), (2.6, 640, 1150)), chars=[G(eyes='wide', brow='surprised', mouth='o')])
    add('b5a', 'stage', 'l5', 'a', bg=shopm, cam=S.close(As(), 2.5, 2.8), chars=[H(), As(brow='worried', mouth='flat')])
    add('b5b', 'bowl', 'l5', 'b')
    add('e6', 'stage', 'l6', bg=('pharmacy', {}), cam=((2.4, 560, 1080), (2.6, 560, 1080)), chars=[G(brow='worried', mouth='flat')])
    add('b7', 'stage', 'l7', bg=shopm, cam=S.close(As(), 2.5, 2.7), chars=[H(), As(brow='happy', mouth='smirk')])
    add('e8', 'stage', 'l8', bg=('pharmacy', {}), cam=((1.3, 560, 1000), (1.5, 560, 1050)), chars=[G(brow='confused', mouth='flat')])
    add('b9a', 'stage', 'l9', 'a', bg=shopm, cam=S.close(As(), 2.4, 2.6), chars=[H(), As(brow='happy')])
    add('b9b', 'mortar', 'l9', 'b', zoom=(1.1, 1.3), old=True)
    add('e10', 'stage', 'l10', bg=('pharmacy', {}), cam=((2.4, 560, 1080), (2.6, 560, 1080)), chars=[G(brow='confused', mouth='flat')])
    add('b11', 'stage', 'l11', bg=shopm, cam=S.close(As(), 2.5, 2.7), chars=[H(), As(brow='smug', mouth='smirk')])
    add('e12', 'stage', 'l12', bg=('pharmacy', {}), cam=((2.4, 560, 1080), (2.8, 560, 1080)), chars=[G(brow='happy', mouth='smirk')])
    add('m13', 'mortar', 'l13', extra=0.5, zoom=(1.3, 1.0), old=True)
    add('sabah', 'black', dur=1.8, text='Sabah...')
    add('d14', 'stage', 'l14', bg=shopm, cam=S.close(H(), 2.3, 2.5), chars=[H(brow='confused'), As()])
    add('d15', 'stage', 'l15', extra=0.6, bg=shopm, cam=((1.3, 560, 1080), (1.45, 560, 1050)), chars=[H(brow='worried'), As(brow='worried', mouth='flat')])
    add('gun', 'black', dur=1.8, text='Ertesi gün...')
    add('w0', 'window', dur=3.0)
    add('d16', 'stage', 'l16', bg=('door', {}), cam=((1.1, 400, 1150), (1.25, 350, 1100)), chars=[Hk(brow='happy', wave=True), Y()])
    add('d17', 'stage', 'l17', bg=('door', {}), cam=S.close(Y(), 2.3, 2.5), chars=[Hk(), Y(brow='happy', wave=True)])
    add('d18', 'stage', 'l18', bg=shopm, cam=S.close(H(), 2.4, 2.6), chars=[H(brow='happy'), As()])
    add('d19', 'stage', 'l19', extra=0.4, bg=shopm, cam=S.close(As(), 2.6, 3.0), chars=[H(), As(brow='happy', mouth='smirk')])
    add('w20', 'window', 'l20', extra=1.0)
    add('sonraki', 'black', dur=4.5, text='Sezon finali', sub='Elli sekiz can daha... Elif eve dönebilecek mi?')
    add('son', 'end', dur=4.0)
