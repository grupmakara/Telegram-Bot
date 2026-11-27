#!/usr/bin/env python3
"""Instagram/Facebook story görselleri (1080x1920): bölüm başına bir story + her gün için 'bugün 2 yeni bölüm'.
Kareler story/kare/bolumN.png (altyazısız, bölüm animasyonundan). Çıktı: story/*.png
'python3 story.py aksam 5' yalnızca 'Bölüm 5 bu akşam yayında' afişini üretir (story/story-bolum5-aksam.png).
"""
import os, subprocess, json, sys
R = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(R, 'story')
BOLUM = {
    3: ('Havanın Sırrı', 'Yüz can kurtarırsa eve dönebilecek... Ama kapıda subaşı var!'),
    4: ("Kadı'nın Huzurunda", 'Cadılıkla suçlanan bir eczacı. Tek silahı: bilgisi.'),
    5: ('Limandaki Salgın', 'Gemiciler bir bir düşüyor. Suçlu içtikleri su mu?'),
    6: ('Çeşmenin Sırrı', 'Yüz yıllık çeşme mahalleyi hasta ediyor olabilir mi?'),
    7: ("Hekim'in Kızı", 'En büyük düşmanı, gece yarısı kapısını çalıyor.'),
    8: ('İki Dünya', "Havandan gelen ses... Gerçek Ayşe 2026'da!"),
}
GUNLER = [(2, 3, 4), (3, 5, 6), (4, 7, 8)]  # 1. gün: Bölüm 1-2 (yayınlandı)


def tr_buyuk(t):
    return t.replace('i', 'İ').replace('ı', 'I').upper()
FONT = f'file://{R}/sablon/fonts'
CSS = f'''
@font-face {{ font-family: Cinzel; font-weight: 700; src: url({FONT}/cinzel-latin.woff2); unicode-range: U+0000-00FF, U+2010-2027; }}
@font-face {{ font-family: Cinzel; font-weight: 700; src: url({FONT}/cinzel-latinext.woff2); unicode-range: U+0100-024F; }}
@font-face {{ font-family: Nunito; font-style: italic; font-weight: 800; src: url({FONT}/nunito-latin.woff2); unicode-range: U+0000-00FF, U+2010-2027; }}
@font-face {{ font-family: Nunito; font-style: italic; font-weight: 800; src: url({FONT}/nunito-latinext.woff2); unicode-range: U+0100-024F; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1920px; overflow: hidden; background: #120B07; color: #fff; }}
.bg {{ position: absolute; inset: 0; background-size: cover; background-position: center; }}
.shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(18,11,7,.85) 0%, rgba(18,11,7,.15) 22%, rgba(18,11,7,0) 45%, rgba(18,11,7,.55) 62%, rgba(18,11,7,.95) 82%); }}
.logo {{ position: absolute; top: 120px; left: 0; right: 0; text-align: center; font-family: Cinzel; font-size: 70px; color: #E8C987; letter-spacing: .05em; text-shadow: 0 4px 20px rgba(0,0,0,.7); }}
.logo small {{ display: block; font-size: 30px; letter-spacing: .3em; margin-top: 10px; color: #CDB894; }}
.rozet {{ display: inline-block; background: #B2452E; color: #fff; font-family: Nunito; font-style: italic; font-weight: 800; font-size: 40px; padding: 12px 34px; border-radius: 40px; box-shadow: 0 6px 20px rgba(0,0,0,.5); }}
.alt {{ position: absolute; left: 70px; right: 70px; bottom: 210px; text-align: center; }}
.no {{ font-family: Cinzel; font-size: 56px; color: #E8C987; letter-spacing: .15em; margin-top: 34px; }}
.baslik {{ font-family: Cinzel; font-size: 92px; line-height: 1.05; margin-top: 10px; text-shadow: 0 6px 24px rgba(0,0,0,.8); }}
.cizgi {{ width: 300px; height: 4px; margin: 34px auto; background: linear-gradient(90deg, transparent, #C9A55A, transparent); }}
.merak {{ font-family: Nunito; font-style: italic; font-weight: 800; font-size: 46px; line-height: 1.3; color: #F4EBD8; text-shadow: 0 3px 10px rgba(0,0,0,.8); }}
.cta {{ position: absolute; bottom: 90px; left: 0; right: 0; text-align: center; font-family: Nunito; font-style: italic; font-weight: 800; font-size: 38px; color: #E8C987; }}
.aksam {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,14,40,.95) 0%, rgba(10,14,40,.82) 30%, rgba(10,14,40,.45) 40%, rgba(40,20,30,.05) 50%, rgba(60,25,15,.55) 64%, rgba(18,11,7,.97) 84%); }}
.ay {{ position: absolute; top: 330px; right: 120px; width: 110px; height: 110px; border-radius: 50%; box-shadow: -26px 14px 0 0 #F3E3B5; filter: drop-shadow(0 0 30px rgba(243,227,181,.6)); }}
.yildiz {{ position: absolute; width: 6px; height: 6px; border-radius: 50%; background: #FFF6DC; box-shadow: 0 0 10px #FFF6DC; }}
.buaksam {{ position: absolute; top: 360px; left: 0; right: 0; text-align: center; }}
.buaksam h1 {{ font-family: Cinzel; font-size: 120px; line-height: 1; color: #F3E3B5; text-shadow: 0 0 40px rgba(243,227,181,.45), 0 6px 24px rgba(0,0,0,.8); margin-top: 26px; }}
.buaksam h2 {{ font-family: Cinzel; font-size: 72px; letter-spacing: .12em; color: #fff; margin-top: 8px; text-shadow: 0 6px 24px rgba(0,0,0,.8); }}
.gun {{ position: absolute; top: 330px; left: 0; right: 0; text-align: center; }}
.gun h1 {{ font-family: Cinzel; font-size: 84px; line-height: 1.1; color: #fff; margin-top: 30px; text-shadow: 0 6px 24px rgba(0,0,0,.8); }}
.kartlar {{ position: absolute; top: 700px; left: 70px; right: 70px; display: flex; gap: 40px; }}
.kart {{ flex: 1; border-radius: 28px; overflow: hidden; border: 5px solid #C9A55A; background: #2A1A10; box-shadow: 0 12px 40px rgba(0,0,0,.6); }}
.kart .resim {{ height: 700px; background-size: cover; background-position: center 35%; }}
.kart .yazi {{ padding: 26px 18px 30px; text-align: center; }}
.kart .yazi b {{ display: block; font-family: Cinzel; font-size: 34px; color: #E8C987; letter-spacing: .1em; }}
.kart .yazi span {{ display: block; font-family: Cinzel; font-size: 40px; line-height: 1.15; margin-top: 10px; }}
'''


def sayfa(govde):
    return f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{govde}</body></html>'


isler = []
for e, (baslik, merak) in BOLUM.items():
    govde = (f'<div class="bg" style="background-image:url(file://{S}/kare/bolum{e}.png)"></div><div class="shade"></div>'
             f'<div class="logo">ZAMANIN ECZACISI<small>1665 · İSTANBUL</small></div>'
             f'<div class="alt"><span class="rozet">YENİ BÖLÜM</span><div class="no">BÖLÜM {e}</div>'
             f'<div class="baslik">{tr_buyuk(baslik)}</div><div class="cizgi"></div><div class="merak">{merak}</div></div>'
             f'<div class="cta">▲ İzlemek için profile git</div>')
    isler.append((f'{S}/story-bolum{e}.html', f'{S}/story-bolum{e}.png', sayfa(govde)))
for g, a, b in GUNLER:
    kart = lambda e: (f'<div class="kart"><div class="resim" style="background-image:url(file://{S}/kare/bolum{e}.png)"></div>'
                      f'<div class="yazi"><b>BÖLÜM {e}</b><span>{tr_buyuk(BOLUM[e][0])}</span></div></div>')
    govde = (f'<div class="bg" style="background-image:url(file://{S}/kare/bolum{a}.png);filter:blur(18px) brightness(.45);transform:scale(1.1)"></div>'
             f'<div class="logo">ZAMANIN ECZACISI<small>1665 · İSTANBUL</small></div>'
             f'<div class="gun"><span class="rozet">{g}. GÜN</span><h1>Bugün<br>2 yeni bölüm!</h1></div>'
             f'<div class="kartlar">{kart(a)}{kart(b)}</div><div class="cta">▲ İzlemek için profile git</div>')
    isler.append((f'{S}/story-gun{g}.html', f'{S}/story-gun{g}.png', sayfa(govde)))
if len(sys.argv) > 2 and sys.argv[1] == 'aksam':
    e = int(sys.argv[2])
    baslik, merak = BOLUM[e]
    merak = merak.replace('. ', '.<br>', 1)
    yildizlar = ''.join(f'<div class="yildiz" style="left:{x}px;top:{y}px;opacity:{o}"></div>'
                        for x, y, o in [(110, 300, .9), (260, 420, .6), (420, 330, .8), (700, 290, .7), (860, 470, .5), (190, 560, .5), (980, 260, .8), (560, 520, .4)])
    govde = (f'<div class="bg" style="background-image:url(file://{S}/kare/bolum{e}.png)"></div><div class="aksam"></div>{yildizlar}<div class="ay"></div>'
             f'<div class="logo">ZAMANIN ECZACISI<small>1665 · İSTANBUL</small></div>'
             f'<div class="buaksam"><span class="rozet">🌙 BÖLÜM {e}</span><h1>BU AKŞAM</h1><h2>YAYINDA</h2></div>'
             f'<div class="alt"><div class="baslik">{tr_buyuk(baslik)}</div><div class="cizgi"></div><div class="merak">{merak}</div></div>'
             f'<div class="cta">🔔 Bildirimleri aç, kaçırma!</div>')
    isler = [(f'{S}/story-bolum{e}-aksam.html', f'{S}/story-bolum{e}-aksam.png', sayfa(govde))]
for html, _, icerik in isler:
    open(html, 'w').write(icerik)
js = f'''const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1080, height: 1920 }}, deviceScaleFactor: 1 }});
for (const [h, o] of {json.dumps([(h, o) for h, o, _ in isler])}) {{ await p.goto('file://' + h); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300); await p.screenshot({{ path: o }}); }}
await b.close(); }})();'''
open(f'{S}/cek.js', 'w').write(js)
subprocess.run(['node', f'{S}/cek.js'], check=True)
for h, _, _ in isler:
    os.remove(h)
os.remove(f'{S}/cek.js')
print('\n'.join(o for _, o, _ in isler))
