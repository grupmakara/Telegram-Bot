"""Bölüm 2 - İlk Reçete"""
OUT = 'proje2'
TITLE = ('BÖLÜM 2', 'İlk Reçete')
HOOK = ('Sabaha kadar vakti var...', 'Çocuk ölürse <b>suçlu o!</b>')
END = ('Hekim Ahmet Efendi susacak mı?', 'Bölüm 3 yakında...')
HOOK_CUT = ('l9', 'Sabaha', 'h0', 'from')
LINES = {
    'h0': ('b2_h0.wav', 'hekim', 'Sabaha kadar. Ölürse, vebali senin boynuna.', 3.2),
    'l1': ('b2_l1.wav', 'fatma', 'Attar Efendi, ne olur... Oğlum üç gündür gözünü açmıyor.', 4.5, 0.8),
    'l2': ('b2_l2.wav', 'ayse', 'Korkmayın Fatma Hanım. Önce ateşini düşürmemiz lazım.', 4.0, 0.45),
    'l2b': ('b2_l2b.wav', 'fatma', 'Hekim Efendi sabah gelip kan aldıracakmış... Ama oğlum zaten çok zayıf.', 5.0, 0.7),
    'l2c': ('b2_l2c.wav', 'ayse', 'Alnı yanıyor... Ateşi en az kırk derece.', 3.2, 0.5),
    'l3': ('b2_l3.wav', 'ayse', 'Söğüt kabuğunu kaynatın. İçindeki madde ateşi düşürür, ağrıyı keser.', 5.0, 0.45),
    'l4': ('b2_l4.wav', 'huseyin', 'Kızım, bunları nereden biliyorsun?', 2.6, 0.35),
    'l5': ('b2_l5.wav', 'ayse', 'Sonra anlatırım, baba.', 1.8, 0.35),
    'l6': ('b2_l6.wav', 'ayse', 'Bir kâse su, bir tutam tuz, biraz bal. Kaşık kaşık içirin, vücudu kurumasın.', 5.5, 0.45),
    'l6b': ('b2_l6b.wav', 'fatma', 'Tuz mu? Bal mı? Bu nasıl ilaç böyle kızım?', 3.2, 0.6),
    'l6c': ('b2_l6c.wav', 'ayse', 'Vücudu su kaybediyor. Tuz ve bal, onu ayakta tutacak.', 4.0, 0.5),
    'l7': ('b2_l7.wav', 'hekim', 'Ne oluyor burada? Bu çocuğa kan aldırılacak, ben söyledim!', 4.0, 0.9),
    'l8': ('b2_l8.wav', 'ayse', 'Kan almak onu daha da zayıflatır, efendim. Bu gece bana izin verin.', 4.6, 0.6),
    'l9': ('b2_l9.wav', 'hekim', 'Bir attarın kızı mı bana hekimlik öğretecek? Sabaha kadar. Ölürse, vebali senin boynuna.', 6.0, 0.7),
    'l9b': ('b2_l9b.wav', 'huseyin', 'Kızım, ya ölürse? Bizi de yakarlar!', 3.0, 0.8),
    'l9c': ('b2_l9c.wav', 'ayse', 'Ölmeyecek baba. Buna izin vermeyeceğim.', 3.0, 0.6),
    'l10': ('b2_l10.wav', 'ayse', 'Hadi Mehmet... Hadi, savaş...', 3.0, 0.4),
    'l10b': ('b2_l10b.wav', 'ayse', 'Bez ısındı... Bir daha. Soğuk su... bir kaşık daha...', 4.0, 0.35),
    'l10c': ('b2_l10c.wav', 'fatma', 'Ya Rabbi... Oğlumu bana bağışla...', 3.0, 0.45),
    'l11': ('b2_l11.wav', 'mehmet', 'Anne... acıktım...', 2.4, 0.4),
    'l12': ('b2_l12.wav', 'fatma', "Oğlum! Ateşi düşmüş... Allah'ım, şükürler olsun!", 4.0, 0.9),
    'l12b': ('b2_l12b.wav', 'ayse', 'Hoş geldin, Mehmet.', 1.8, 0.4),
    'l13': ('b2_l13.wav', 'hekim', 'Bu kız... Ya bir cadı, ya da benim hiç tanımadığım türden bir hekim.', 5.0, 0.55),
}
SPLITS = {'l3': ('İçindeki', 0.45), 'l6': ('Kaşık', 0.5), 'l9': ('Sabaha', 0.5)}


def plan(add, S):
    night, dawn = ('room', {'time': 'night'}), ('room', {'time': 'dawn'})
    F = lambda **o: S.C('fatma', 190, 1560, 0.95, **o)
    M = lambda **o: S.C('mehmet', 640, 1420, **o)
    A = lambda **o: S.C('ayse', 930, 1560, 0.95, **o)
    Hk = lambda **o: S.C('hekim', 260, 1880, **o)
    Hs = lambda **o: S.C('huseyin', 760, 1900, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=night, hook=True, cam=S.close(Hk(), 2.6, 3.0),
        chars=[M(), A(), Hk(brow='determined', point=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub="Eczacı Elif, 1665 İstanbul'unda bir attarın kızı olarak uyandı ve hasta Mehmet'e yardım etmeye karar verdi.")
    add('r0', 'stage', dur=2.8, bg=night, cam=((1.0, 540, 960), (1.06, 540, 1000)), chars=[S.C('fatma', 190, 1560, 0.95, brow='worried', mouth='flat'), S.C('mehmet', 640, 1420)])
    add('r1', 'stage', 'l1', bg=night, cam=((1.0, 540, 960), (1.08, 540, 1060)), chars=[F(brow='worried', mouth='flat'), M(), A(brow='worried', mouth='flat')])
    add('r2', 'stage', 'l2', bg=night, cam=S.close(A(), 2.4, 2.6), chars=[F(), M(), A()])
    add('r2b', 'stage', 'l2b', bg=night, cam=S.close(F(), 2.4, 2.6), chars=[F(brow='worried', mouth='flat'), M(), A()])
    add('r2c', 'stage', 'l2c', bg=night, cam=S.close(M(), 2.7, 3.0), chars=[F(), M(), A()])
    add('r3a', 'stage', 'l3', 'a', bg=night, cam=S.close(A(), 2.6, 2.7), chars=[F(), M(), A(brow='determined', mouth='flat')])
    add('r3b', 'jars', 'l3', 'b', labels=True)
    add('r4', 'stage', 'l4', bg=night, cam=S.close(Hs(), 2.3, 2.5), chars=[M(), Hs(brow='worried')])
    add('r5', 'stage', 'l5', bg=night, cam=S.close(A(), 2.6, 2.7), chars=[F(), M(), A(brow='smug', mouth='smirk')])
    add('r6a', 'stage', 'l6', 'a', bg=night, cam=S.close(A(), 2.4, 2.5), chars=[F(), M(), A()])
    add('r6b', 'stage', 'l6', 'b', bg=night, cam=S.close(M(), 2.6, 2.9), chars=[F(), M(cloth=True), A()])
    add('r6c', 'stage', 'l6b', bg=night, cam=S.close(F(), 2.3, 2.5), chars=[F(brow='confused', mouth='flat'), M(cloth=True), A()])
    add('r6d', 'stage', 'l6c', bg=night, cam=S.close(A(), 2.4, 2.6), chars=[F(), M(cloth=True), A()])
    add('r7', 'stage', 'l7', bg=night, knock=[0.0, 0.25], cam=((1.0, 540, 960), (1.5, 300, 1180)),
        chars=[M(cloth=True), A(brow='surprised'), Hk(brow='determined', point=True)])
    add('r8', 'stage', 'l8', bg=night, cam=S.close(A(), 2.5, 2.7), chars=[M(cloth=True), A(brow='determined', mouth='flat')])
    add('r9a', 'stage', 'l9', 'a', bg=night, cam=S.close(Hk(), 2.4, 2.5), chars=[M(cloth=True), Hk(brow='smug')])
    add('r9b', 'stage', 'l9', 'b', bg=night, cam=S.close(Hk(), 2.6, 3.1), chars=[M(cloth=True), Hk(brow='determined', point=True)])
    add('r9c', 'stage', 'l9b', bg=night, cam=S.close(Hs(), 2.3, 2.6), chars=[M(cloth=True), Hs(brow='worried')])
    add('r9d', 'stage', 'l9c', extra=0.3, bg=night, cam=S.close(A(), 2.5, 2.9), chars=[F(), M(cloth=True), A(brow='determined', mouth='flat')])
    add('gece', 'black', dur=1.8, text='Gece yarısı...')
    add('r10', 'stage', 'l10', extra=0.4, bg=night, cam=((1.6, 800, 1230), (1.75, 800, 1230)),
        chars=[M(cloth=True), A(eyes='half', brow='worried', mouth='flat')])
    add('r10b', 'stage', 'l10b', extra=0.4, bg=night, cam=((2.2, 720, 1250), (2.4, 700, 1250)),
        chars=[M(cloth=True), A(eyes='half', brow='tired', mouth='flat')])
    add('r10c', 'stage', 'l10c', extra=0.4, bg=night, cam=S.close(F(), 2.4, 2.7), chars=[F(eyes='half', brow='worried', mouth='flat'), M(cloth=True), A(eyes='half')])
    add('safak', 'black', dur=1.8, text='Sabaha karşı...')
    add('r10d', 'stage', dur=2.6, bg=dawn, cam=((1.0, 540, 960), (1.08, 540, 1040)), chars=[F(eyes='closed', brow='asleep'), M(sick=False, eyes='closed'), A(eyes='closed', brow='asleep', tilt=9)])
    add('r11', 'stage', 'l11', extra=0.4, bg=dawn, cam=S.close(M(), 2.6, 2.9), chars=[F(), M(sick=False, eyes='closed', wake=0.3), A()])
    add('r12', 'stage', 'l12', bg=dawn, cam=((1.0, 540, 960), (1.15, 400, 1150)), chars=[F(brow='happy'), M(sick=False, eyes='open', mouth='smile'), A(brow='happy')])
    add('r12b', 'stage', 'l12b', extra=0.5, bg=dawn, cam=S.close(A(), 2.5, 2.8), chars=[F(), M(sick=False, eyes='open', mouth='smile'), A(brow='happy', mouth='smirk')])
    add('r13', 'stage', 'l13', extra=0.6, bg=dawn, cam=S.close(Hk(), 2.4, 2.9), chars=[M(sick=False, eyes='open', mouth='smile'), Hk(brow='confused')])
    add('son', 'end', dur=3.5)
