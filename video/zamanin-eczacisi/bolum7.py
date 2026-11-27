"""Bölüm 7 - Hekim'in Kızı"""
OUT = 'proje7'
TITLE = ('BÖLÜM 7', "Hekim'in Kızı")
HOOK = ('Düşmanı ondan yardım istiyor...', 'Ya <b>geç</b> kalırsa?')
END = ('İki kız, iki yüzyıl...', 'Bölüm 8 yakında...')
HOOK_CUT = ('l5', 'Ne', 'h0', 'from')
LINES = {
    'h0': ('b7_h0.wav', 'hekim', 'Ne olur... Kızımı kurtar!', 2.4),
    'l1': ('b7_l1.wav', 'ayse', 'Havanın içinde bir yüz var... Bu... benim yüzüm!', 4.0, 0.6, 'whispering, shocked'),
    'l2': ('b7_l2.wav', 'ayse', 'Ama ben buradayım... O zaman o kim?', 3.0, 0.5, 'confused, quiet'),
    'l3': ('b7_l3.wav', 'hekim', 'Ayşe! Kapıyı aç, ne olur!', 2.4, 0.9, 'desperate, shouting'),
    'l4': ('b7_l4.wav', 'huseyin', 'Hekim Ahmet Efendi? Bu saatte?', 2.6, 0.6, 'surprised, sleepy'),
    'l5': ('b7_l5.wav', 'hekim', 'Kızım Leyla... Nefes alamıyor. Ne olur... Kızımı kurtar!', 4.6, 0.9, 'desperate, crying'),
    'l6': ('b7_l6.wav', 'leyla', 'Baba... göğsüm... sıkışıyor...', 2.8, 0.7, 'weak, breathless, wheezing'),
    'l7': ('b7_l7.wav', 'ayse', 'Hırıltı var... Bu astım krizi olabilir. Pencereleri açın, hemen!', 4.6, 0.8, 'urgent, commanding'),
    'l8': ('b7_l8.wav', 'ayse', 'Leyla, bana bak. Benimle nefes al. Yavaşça... içine... dışarı...', 6.0, 0.4, 'very calm, soothing, slow'),
    'l9': ('b7_l9.wav', 'hekim', 'Ne yapabilirim? Söyle, ne gerekiyorsa yaparım!', 3.4, 0.8, 'panicked'),
    'l10': ('b7_l10.wav', 'ayse', 'Kaynar su ve nane getirin. Buharını ona soluttaracağız.', 4.0, 0.6, 'quick, focused'),
    'l11': ('b7_l11.wav', 'yusuf', 'Nane bende var, hocam!', 1.8, 0.7, 'eager, quick'),
    'l12': ('b7_l12.wav', 'leyla', 'Baba... nefes alabiliyorum...', 2.6, 0.5, 'weak, relieved'),
    'l13': ('b7_l13.wav', 'hekim', "Leyla'm... Allah'ım, şükürler olsun.", 2.8, 0.8, 'crying with relief'),
    'l14': ('b7_l14.wav', 'hekim', 'Sana cadı dedim... Seni mahkemeye sürükledim... Ve sen kızımı kurtardın.', 6.0, 0.6, 'ashamed, emotional, slow'),
    'l15': ('b7_l15.wav', 'ayse', 'Hepimiz yanılırız, efendim. Önemli olan, şimdi aynı taraftayız.', 4.6, 0.5, 'warm, kind'),
    'l16': ('b7_l16.wav', 'hekim', 'Bundan sonra yanındayım, Ayşe. Ne gerekirse.', 3.4, 0.5, 'sincere'),
    'l17': ('b7_l17.wav', 'hekim', 'Bir şey daha... O havan. Benim dedem de anlatırdı onu.', 4.4, 0.4, 'mysterious, slow'),
    'l18': ('b7_l18.wav', 'hekim', 'Derdi ki, havanı ilk kullanan da zamanın ötesinden gelmiş bir şifacıymış.', 5.5, 0.4, 'storytelling, mysterious'),
    'l19': ('b7_l19.wav', 'ayse', 'Benden önce de biri mi geldi?', 2.4, 0.7, 'shocked whisper'),
    'l20': ('b7_l20.wav', 'ayse', 'Kırk iki can... Elli sekiz kaldı.', 3.0, 0.5, 'whispering, counting'),
    'l21': ('b7_l21.wav', 'ayseg', 'Kimse var mı? Burası neresi? Bu ışıklar ne?', 3.6, 0.8, 'scared, echoing, lost'),
    'l22': ('b7_l22.wav', 'ayse', 'Bu ses... Bu gerçek Ayşe! Benim bedenimde!', 3.6, 0.8, 'shocked, whispering'),
}
SPLITS = {'l14': ('Ve', 0.6), 'l8': ('Yavaşça', 0.45)}


def plan(add, S):
    shopm = ('shop', {'mortar': True})
    night = ('room', {'time': 'night'})
    H = lambda **o: S.C('huseyin', 300, 1700, **o)
    As = lambda **o: S.C('ayse', 800, 1400, **o)
    Hd = lambda **o: S.C('hekim', 540, 1600, 0.95, **o)
    L = lambda **o: S.C('leyla', 600, 1540, 0.85, **o)
    A = lambda **o: S.C('ayse', 930, 1560, 0.95, **o)
    Hk = lambda **o: S.C('hekim', 230, 1880, **o)
    Y = lambda **o: S.C('yusuf', 760, 1920, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=night, hook=True, cam=S.close(Hk(), 2.6, 3.0), chars=[L(eyes='half', brow='worried', mouth='o'), A(), Hk(brow='worried', point=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub='Çeşme kapatıldı, salgın durdu. Havan ilk kez kendi kendine parladı.')
    add('gece', 'black', dur=1.8, text='Gece yarısı...')
    add('m0', 'mortar', dur=2.6, zoom=(1.0, 1.2), old=True)
    add('b1', 'bowl', 'l1', extra=0.3)
    add('w0', 'window', dur=2.8)
    add('b2', 'stage', 'l2', bg=shopm, cam=S.close(As(), 2.5, 2.8), chars=[H(), As(brow='confused', mouth='flat')])
    add('d3', 'stage', 'l3', bg=('door', {'crowd': False}), knock=[0.0, 0.25, 0.5], cam=S.close(Hd(), 2.0, 2.4), chars=[Hd(brow='worried', point=True)])
    add('d4', 'stage', 'l4', bg=shopm, cam=S.close(H(), 2.3, 2.5), chars=[H(brow='surprised', eyes='half'), As()])
    add('d5', 'stage', 'l5', extra=0.3, bg=('door', {'crowd': False}), cam=S.close(Hd(), 2.3, 2.8), chars=[Hd(brow='worried')])
    add('ro', 'stage', dur=2.4, bg=night, cam=((1.0, 540, 960), (1.08, 540, 1040)), chars=[L(eyes='half', brow='worried', mouth='o'), A(), Hk(brow='worried')])
    add('r6', 'stage', 'l6', bg=night, cam=S.close(L(), 2.6, 2.9), chars=[L(eyes='half', brow='worried', mouth='o'), A(), Hk()])
    add('r7', 'stage', 'l7', bg=night, cam=S.close(A(), 2.4, 2.6), chars=[L(), A(brow='determined', mouth='flat'), Hk()])
    add('r8a', 'stage', 'l8', 'a', bg=night, cam=((1.6, 760, 1250), (1.8, 760, 1250)), chars=[L(eyes='half', brow='worried'), A()])
    add('r8b', 'stage', 'l8', 'b', bg=night, cam=S.close(L(), 2.5, 2.7), chars=[L(eyes='half', brow='worried'), A()])
    add('r9', 'stage', 'l9', bg=night, cam=S.close(Hk(), 2.4, 2.6), chars=[L(), A(), Hk(brow='worried')])
    add('r10', 'stage', 'l10', bg=night, cam=S.close(A(), 2.4, 2.6), chars=[L(), A(brow='determined', mouth='flat'), Hk()])
    add('r11', 'stage', 'l11', bg=night, cam=S.close(Y(), 2.2, 2.4), chars=[L(), Y(wave=True)])
    add('saat', 'black', dur=1.8, text='Bir saat sonra...')
    add('rw', 'stage', dur=2.8, bg=night, cam=((1.0, 540, 960), (1.08, 540, 1040)), chars=[L(eyes='closed', brow='asleep'), A(eyes='half')])
    add('r12', 'stage', 'l12', bg=night, cam=S.close(L(), 2.6, 2.8), chars=[L(brow='happy', mouth='smirk'), A(), Hk()])
    add('r13', 'stage', 'l13', bg=night, cam=S.close(Hk(), 2.4, 2.7), chars=[L(), A(), Hk(brow='happy')])
    add('r14a', 'stage', 'l14', 'a', bg=night, cam=S.close(Hk(), 2.5, 2.7), chars=[L(), A(), Hk(brow='worried')])
    add('r14b', 'stage', 'l14', 'b', bg=night, cam=((1.4, 560, 1250), (1.5, 560, 1250)), chars=[L(brow='happy'), A(brow='happy'), Hk(brow='worried')])
    add('r15', 'stage', 'l15', bg=night, cam=S.close(A(), 2.5, 2.7), chars=[L(), A(brow='happy', mouth='smirk'), Hk()])
    add('r16', 'stage', 'l16', bg=night, cam=S.close(Hk(), 2.4, 2.6), chars=[L(), A(), Hk(brow='happy')])
    add('r17', 'stage', 'l17', bg=night, cam=S.close(Hk(), 2.6, 2.8), chars=[L(), A(), Hk(brow='confused')])
    add('m18', 'mortar', 'l18', zoom=(1.0, 1.25), old=True)
    add('r19', 'stage', 'l19', extra=0.3, bg=night, cam=S.close(A(), 2.7, 3.2), chars=[L(), A(eyes='wide', brow='surprised', mouth='o', shock=True), Hk()])
    add('m20', 'mortar', 'l20', extra=0.3, zoom=(1.1, 1.3), old=True)
    add('b21', 'bowl', 'l21', extra=0.3)
    add('b22', 'stage', 'l22', extra=0.8, bg=shopm, cam=S.close(As(), 2.8, 3.4), chars=[H(), As(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('sonraki', 'black', dur=4.5, text='Sonraki bölümde...', sub="İki kız, iki yüzyıl... Elif, gerçek Ayşe'yle ilk kez konuşacak.")
    add('son', 'end', dur=3.5)
