"""Bölüm 15 - Doksan Dokuz"""
OUT = 'proje15'
TITLE = ('BÖLÜM 15', 'Doksan Dokuz')
HOOK = ('Sayaç doksan dokuzda...', 'Ve yüzüncü can <b>babası</b> olabilir!')
END = ('Yüzüncü can...', 'Bölüm 16, 2. Sezon Finali yakında...')
HOOK_CUT = ('l18', 'Baba', 'h0', 'until')
CTA = True  # bitişte takip/beğeni animasyonu
LINES = {
    'h0': ('b15_h0.wav', 'ayse', 'Baba! Baba, beni duyuyor musun?', 2.4),
    'l1': ('b15_l1.wav', 'kadi', 'Kızım, mektubun arkasında son bir satır var. Kırmızı ışık, son geçittir.', 4.8, 0.5, 'serious, slow'),
    'l2': ('b15_l2.wav', 'kadi', 'Yüzüncü can kurtulduğunda, dolunayda havan son bir kez açılır. Sonra sonsuza dek kapanır.', 5.8, 0.5, 'solemn, slow, mysterious'),
    'l3': ('b15_l3.wav', 'ayse', 'Son bir kez... Yani ya şimdi döneceğiz, ya hiç.', 3.6, 0.5, 'quiet, emotional'),
    'l4': ('b15_l4.wav', 'ayse', 'Ayşe, otuz altı can kaldı. Ama artık iki kişi değiliz.', 3.8, 0.6, 'determined, whispering'),
    'l5': ('b15_l5.wav', 'ayseg', 'Kemal Bey bana her gün yeni bir ilaç öğretiyor. Ben de ona bitkilerimi!', 4.2, 0.6, 'happy, proud'),
    'l6': ('b15_l6.wav', 'hekim', 'Ayşe kızım, bugün altı hastayı Yusuf ile ben iyileştirdik. Senin usulünle.', 4.6, 0.6, 'proud, warm'),
    'l7': ('b15_l7.wav', 'yusuf', 'Önce eller yıkanır, sonra su kaynatılır, sonra hasta dinlenir!', 3.8, 0.7, 'excited, reciting'),
    'l8': ('b15_l8.wav', 'ayse', 'Yetmiş beş... Seksen iki... Doksan...', 3.4, 0.5, 'quiet, counting slowly'),
    'l9': ('b15_l9.wav', 'kemal', 'Kızım, bir anne ağlayarak geldi. Bebeğinin ateşi çok yüksek.', 4.0, 0.6, 'worried, urgent'),
    'l10': ('b15_l10.wav', 'ayseg', 'Elbiselerini gevşetelim, ılık suyla silelim. Kemal Bey, doktoru arayın, dozunu o versin.', 5.6, 0.6, 'calm, focused, careful'),
    'l11': ('b15_l11.wav', 'kemal', 'Ateş düşüyor... Aferin, kızım. Artık gerçek bir eczacı oldun.', 4.0, 0.6, 'relieved, proud'),
    'l12': ('b15_l12.wav', 'ayse', 'Doksan dokuz. Havan hiç bu kadar parlak olmamıştı.', 3.6, 0.5, 'whispering, amazed'),
    'l13': ('b15_l13.wav', 'ayseg', 'Elif... Bir can kaldı. Sonra eve dönüyoruz, değil mi?', 3.8, 0.6, 'emotional, hopeful, whispering'),
    'l14': ('b15_l14.wav', 'ayse', 'Evet. Ama burayı... babanı... çok özleyeceğim.', 3.6, 0.5, 'sad, quiet, emotional'),
    'l15': ('b15_l15.wav', 'ayseg', 'Ben de seni özleyeceğim. Kemal Bey\'i de.', 3.0, 0.5, 'sad, smiling softly'),
    'l16': ('b15_l16.wav', 'huseyin', 'Kızım... Göğsüm... Bir taş oturmuş gibi... Kolum uyuşuyor...', 4.4, 0.6, 'weak, in pain, slow'),
    'l17': ('b15_l17.wav', 'ayse', 'Göğüs ağrısı, kola yayılıyor... Bu kalp krizi olabilir!', 3.8, 0.7, 'alarmed, urgent'),
    'l18': ('b15_l18.wav', 'ayse', 'Baba! Baba, beni duyuyor musun? Yusuf, Ahmet Efendi\'yi çağır, çabuk!', 4.4, 0.8, 'panicked, urgent'),
}
SPLITS = {'l2': ('Sonra', 0.72), 'l10': ('Kemal', 0.55)}


def plan(add, S):
    shopm = ('shop', {'mortar': True})
    court = ('court', {})
    ph = ('pharmacy', {})
    H = lambda **o: S.C('huseyin', 280, 1720, **o)
    A = lambda **o: S.C('ayse', 800, 1650, **o)
    Ac = lambda **o: S.C('ayse', 830, 1690, **o)
    Kd = lambda **o: S.C('kadi', 540, 1330, 0.92, **o)
    G = lambda **o: S.C('ayseg', 780, 1420, **o)
    K = lambda **o: S.C('kemal', 300, 1760, 0.95, **o)
    Hk = lambda **o: S.C('hekim', 250, 1820, 0.95, **o)
    Y = lambda **o: S.C('yusuf', 520, 1800, 0.9, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=shopm, hook=True, cam=((1.2, 520, 1250), (1.35, 540, 1250)), chars=[H(brow='tired', arm=-25), A(eyes='wide', brow='worried', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub='Dolunayda havan onarıldı. Ama bu kez kırmızı parlıyordu.')
    add('m0', 'mortar', dur=2.4, zoom=(1.0, 1.2), old=True, color='#FF4A3D')
    add('c1', 'stage', 'l1', bg=court, cam=S.close(Kd(), 2.2, 2.5), chars=[Kd(brow='worried'), Ac()])
    add('c2', 'stage', 'l2', bg=court, cam=((1.2, 540, 1150), (1.35, 540, 1100)), chars=[Kd(brow='worried'), Ac(brow='surprised')])
    add('c3', 'stage', 'l3', extra=0.4, bg=court, cam=S.close(Ac(), 2.5, 2.8), chars=[Kd(), Ac(brow='worried', mouth='flat')])
    add('gece', 'black', dur=1.8, text='O gece...')
    add('m4', 'mortar', 'l4', zoom=(1.0, 1.2), old=True, color='#FF4A3D')
    add('e5', 'stage', 'l5', bg=ph, cam=S.close(G(), 2.4, 2.6), chars=[K(brow='happy'), G(brow='happy', mouth='smirk')])
    add('ay', 'black', dur=2.0, text='Bir ay boyunca...')
    add('s6', 'stage', 'l6', bg=shopm, cam=S.close(Hk(), 2.3, 2.5), chars=[Hk(brow='happy'), Y(), A(brow='happy')])
    add('s7', 'stage', 'l7', bg=shopm, cam=S.close(Y(), 2.3, 2.6), chars=[Hk(), Y(brow='happy', wave=True), A(brow='happy')])
    add('m8', 'mortar', 'l8', zoom=(1.0, 1.35), old=True, color='#FF4A3D')
    add('e9', 'stage', 'l9', bg=ph, cam=S.close(K(), 2.2, 2.5), chars=[K(brow='worried', point=True), G()])
    add('e10a', 'stage', 'l10', 'a', bg=ph, cam=S.close(G(), 2.4, 2.6), chars=[K(), G(brow='determined', mouth='flat')])
    add('e10b', 'stage', 'l10', 'b', bg=ph, cam=((1.2, 540, 1250), (1.3, 540, 1250)), chars=[K(brow='worried'), G(brow='determined', point=True)])
    add('e11', 'stage', 'l11', bg=ph, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='happy'), G(brow='happy')])
    add('gece2', 'black', dur=1.8, text='Dolunaydan bir gece önce...')
    add('m12', 'mortar', 'l12', extra=0.3, zoom=(1.0, 1.25), old=True, color='#FF4A3D')
    add('e13', 'stage', 'l13', bg=ph, cam=((2.3, 780, 1100), (2.6, 780, 1100)), chars=[G(brow='worried', mouth='flat')])
    add('b14', 'stage', 'l14', bg=shopm, cam=S.close(A(), 2.6, 2.9), chars=[A(brow='worried', mouth='flat')])
    add('e15', 'stage', 'l15', bg=ph, cam=((2.3, 780, 1100), (2.5, 780, 1100)), chars=[G(brow='worried', mouth='smirk')])
    add('sabah', 'black', dur=1.8, text='Ertesi sabah...')
    add('s16', 'stage', 'l16', bg=shopm, cam=S.close(H(), 2.3, 2.7), chars=[H(brow='tired', arm=-30), A()])
    add('s17', 'stage', 'l17', bg=shopm, cam=S.close(A(), 2.5, 2.8), chars=[H(brow='tired'), A(eyes='wide', brow='worried', mouth='o', shock=True)])
    add('s18', 'stage', 'l18', extra=0.6, bg=shopm, cam=((1.3, 520, 1250), (1.5, 560, 1300)), chars=[H(brow='asleep', arm=-30), A(eyes='wide', brow='worried', mouth='o', shock=True)])
    add('sonraki', 'black', dur=4.5, text='2. Sezon Finali', sub='Yüzüncü can... Ve havanın son geçidi.')
    add('son', 'end', dur=5.2)
