"""Bölüm 10 - Kemal Bey'in Şüphesi"""
OUT = 'proje10'
TITLE = ('BÖLÜM 10', "Kemal Bey'in Şüphesi")
HOOK = ('Eczanede kimse yok...', 'Ve Kemal Bey <b>yere yığıldı!</b>')
END = ('Havanı kim bıraktı?', 'Bölüm 11 yakında...')
HOOK_CUT = ('l9', 'Kemal', 'h0', 'until')
LINES = {
    'h0': ('b10_h0.wav', 'ayseg', 'Kemal Bey! Beni duyuyor musunuz?', 2.4),
    'l1': ('b10_l1.wav', 'kemal', 'Elif, kızım... Son günlerde sen hiç sen değilsin.', 3.8, 0.5, 'suspicious, gentle'),
    'l2': ('b10_l2.wav', 'kemal', 'Dün bilgisayarı açamadın. Bugün de reçeteleri tek tek elle yazıyorsun.', 5.0, 0.5, 'puzzled, calm'),
    'l3': ('b10_l3.wav', 'ayseg', 'Yorgunum, Kemal Bey. Biraz... başım dönüyor sadece.', 3.6, 0.5, 'nervous, hesitant'),
    'l4': ('b10_l4.wav', 'kemal', 'Peki. Ben öğlen yemeğini sonra yerim, önce şu kutuları dizelim.', 4.4, 0.4, 'calm, tired'),
    'l5': ('b10_l5.wav', 'ayseg', 'Elif bana çok anlattı... Ama bu kutuların hepsi birbirine benziyor.', 4.4, 0.5, 'whispering, to herself, worried'),
    'l6': ('b10_l6.wav', 'kemal', 'Elif... Başım... Ellerim titriyor...', 3.2, 0.6, 'weak, confused, trembling'),
    'l7': ('b10_l7.wav', 'ayseg', 'Kemal Bey? Terlemişsiniz! Yüzünüz bembeyaz!', 3.2, 0.7, 'alarmed, worried'),
    'l8': ('b10_l8.wav', 'kemal', 'Sabah iğnemi yaptım... Yemek yemedim...', 2.8, 0.5, 'weak, slurring, slow'),
    'l9': ('b10_l9.wav', 'ayseg', 'Kemal Bey! Beni duyuyor musunuz? İğne... şeker hastalığı!', 4.0, 0.7, 'urgent, scared'),
    'l10': ('b10_l10.wav', 'ayseg', 'Elif anlatmıştı. Kandaki şeker düşerse, hemen tatlı bir şey vermek gerek!', 4.6, 0.6, 'fast, determined'),
    'l11': ('b10_l11.wav', 'ayseg', 'Bal! Rafta bal var. Kemal Bey, yutun, yavaşça...', 3.6, 0.6, 'urgent, gentle'),
    'l12': ('b10_l12.wav', 'ayseg', 'Bir de... şu telefon. Yüz on iki. Ambulans çağıracağım.', 3.8, 0.6, 'determined, careful'),
    'l13': ('b10_l13.wav', 'kemal', 'Geçiyor... Gözlerim açılıyor. Elif, sen beni kurtardın.', 4.0, 0.5, 'weak, relieved, grateful'),
    'l14': ('b10_l14.wav', 'kemal', 'Ama dün telefonu bile tanımıyordun. Bunu nereden bildin?', 3.8, 0.5, 'curious, suspicious'),
    'l15': ('b10_l15.wav', 'ayseg', 'Bir... arkadaşım öğretti. Çok uzaklarda yaşayan bir arkadaşım.', 4.0, 0.5, 'hesitant, smiling'),
    'l16': ('b10_l16.wav', 'ayse', 'Ayşe! Havan bugün parladı. Sayı birden elli oldu!', 3.8, 0.7, 'excited, amazed'),
    'l17': ('b10_l17.wav', 'ayseg', 'Kemal Bey! Şeker hastası, bayılmıştı. Ona bal verdim!', 3.8, 0.7, 'proud, excited, whispering'),
    'l18': ('b10_l18.wav', 'ayse', 'Demek senin kurtardıkların da sayılıyor... Yüze birlikte ulaşacağız!', 4.4, 0.6, 'emotional, hopeful'),
    'l19': ('b10_l19.wav', 'kemal', 'Elif... Kiminle konuşuyorsun?', 2.4, 0.5, 'quiet, suspicious'),
    'l20': ('b10_l20.wav', 'kemal', 'Bu havan... Ben bu havanı daha önce gördüm. Dedemin dükkânında.', 4.8, 0.5, 'shocked, slow, quiet'),
}
SPLITS = {'l9': ('İğne', 0.6), 'l20': ('Ben', 0.3)}


def plan(add, S):
    ph = ('pharmacy', {})
    shopm = ('shop', {'mortar': True})
    G = lambda **o: S.C('ayseg', 780, 1420, **o)
    K = lambda **o: S.C('kemal', 300, 1760, 0.95, **o)
    A = lambda **o: S.C('ayse', 800, 1400, **o)
    add('kanca', 'stage', 'h0', extra=0.4, bg=ph, hook=True, cam=S.close(G(), 2.4, 2.9), chars=[K(brow='tired'), G(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('baslik', 'title', dur=1.9)
    add('ozet', 'black', dur=3.8, text='Önceki bölümde...', sub="Elif yedi denizciyi kurtardı. 2026'da Ayşe, Kemal Bey'in şüphelendiğini söyledi.")
    add('yer', 'black', dur=2.0, text='İstanbul, 2026')
    add('eo', 'stage', dur=2.8, bg=ph, cam=((1.0, 540, 960), (1.06, 540, 1000)), chars=[])
    add('e1', 'stage', 'l1', bg=ph, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='confused'), G()])
    add('e2', 'stage', 'l2', bg=ph, cam=((1.2, 520, 1250), (1.3, 520, 1200)), chars=[K(brow='confused', point=True), G(brow='worried', mouth='flat')])
    add('e3', 'stage', 'l3', bg=ph, cam=S.close(G(), 2.4, 2.6), chars=[K(), G(brow='worried', mouth='flat')])
    add('e4', 'stage', 'l4', bg=ph, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='tired'), G()])
    add('e5', 'stage', 'l5', bg=ph, cam=((2.3, 760, 1100), (2.6, 760, 1100)), chars=[G(brow='confused', mouth='flat')])
    add('sonra', 'black', dur=1.8, text='Bir saat sonra...')
    add('e6', 'stage', 'l6', bg=ph, cam=S.close(K(), 2.2, 2.6), chars=[K(brow='tired', arm=-25), G()])
    add('e7', 'stage', 'l7', bg=ph, cam=S.close(G(), 2.4, 2.7), chars=[K(brow='tired'), G(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('e8', 'stage', 'l8', bg=ph, cam=S.close(K(), 2.4, 2.8), chars=[K(brow='asleep'), G(brow='worried')])
    add('e9a', 'stage', 'l9', 'a', bg=ph, cam=((1.2, 540, 1250), (1.3, 560, 1250)), chars=[K(brow='asleep'), G(brow='worried', mouth='o', shock=True)])
    add('e9b', 'stage', 'l9', 'b', bg=ph, cam=S.close(G(), 2.4, 2.8), chars=[K(), G(eyes='wide', brow='determined', mouth='o')])
    add('e10', 'stage', 'l10', bg=ph, cam=S.close(G(), 2.4, 2.6), chars=[K(), G(brow='determined', mouth='flat')])
    add('e11', 'stage', 'l11', bg=ph, cam=((1.3, 520, 1250), (1.45, 480, 1250)), chars=[K(brow='asleep'), G(brow='determined', point=True)])
    add('e12', 'stage', 'l12', bg=ph, cam=S.close(G(), 2.4, 2.6), chars=[K(), G(brow='determined', mouth='flat')])
    add('dk', 'black', dur=1.8, text='Birkaç dakika sonra...')
    add('e13', 'stage', 'l13', bg=ph, cam=S.close(K(), 2.2, 2.4), chars=[K(brow='happy'), G(brow='happy')])
    add('e14', 'stage', 'l14', bg=ph, cam=S.close(K(), 2.3, 2.5), chars=[K(brow='confused'), G()])
    add('e15', 'stage', 'l15', bg=ph, cam=S.close(G(), 2.4, 2.6), chars=[K(), G(brow='happy', mouth='smirk')])
    add('gece', 'black', dur=1.8, text='O gece...')
    add('m16', 'mortar', 'l16', zoom=(1.0, 1.2), old=True)
    add('e17', 'stage', 'l17', bg=ph, cam=((2.3, 780, 1100), (2.6, 780, 1100)), chars=[G(brow='happy', mouth='smirk')])
    add('b18', 'stage', 'l18', bg=shopm, cam=S.close(A(), 2.5, 2.8), chars=[A(brow='happy', mouth='smirk')])
    add('e19', 'stage', 'l19', extra=0.4, bg=ph, cam=((1.2, 400, 1250), (1.35, 360, 1250)), chars=[K(brow='confused'), G(eyes='wide', brow='surprised', mouth='o', shock=True)])
    add('e20a', 'stage', 'l20', 'a', bg=ph, cam=S.close(K(), 2.3, 2.6), chars=[K(brow='surprised'), G()])
    add('m20', 'mortar', 'l20', 'b', extra=0.8, zoom=(1.1, 1.4))
    add('sonraki', 'black', dur=4.5, text='Sonraki bölümde...', sub='Havanın dibinde gizli bir mühür. Kadı Efendi onu tanıyor.')
    add('son', 'end', dur=4.0)
