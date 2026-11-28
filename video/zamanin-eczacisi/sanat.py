"""Zamanın Eczacısı - karakter ve mekân çizimleri (SVG)."""
import math

# ---------------------------------------------------------------- yardımcılar
OUTLINE = '#3A2618'
INIT = []  # gsap.set satırları (dönme merkezleri, başlangıç pozları)


def ell(cx, cy, rx, ry, fill, extra=''):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'


def path(d, fill='none', stroke=None, sw=0, extra=''):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ''
    return f'<path d="{d}" fill="{fill}"{s} {extra}/>'


def limb(points, color, width, outline=OUTLINE):
    d = 'M ' + ' L '.join(f'{x},{y}' for x, y in points)
    return (path(d, stroke=outline, sw=width + 6) + path(d, stroke=color, sw=width))


def eye(p, side, cx, cy, rx, ry, iris, state):
    """Göz: beyaz, iris, kirpik çizgisi ve kırpma için göz kapağı."""
    cid = f'{p}-clip{side}'
    lid0 = {'closed': 1, 'half': 0.45}.get(state, 0)
    INIT.append(f'gsap.set("#{p}-lid{side}", {{svgOrigin: "0 {-(ry + 3)}", scaleY: {lid0}}});')
    lid_scale = 1 if state == 'closed' else 0
    s = 1.18 if state == 'wide' else 1
    return f'''
    <g transform="translate({cx},{cy}) scale({s})">
      <clipPath id="{cid}"><ellipse cx="0" cy="0" rx="{rx}" ry="{ry}"/></clipPath>
      <ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="#FBF7F0"/>
      <g clip-path="url(#{cid})">
        <circle cx="1" cy="1" r="{ry * 0.92:.1f}" fill="{iris}"/>
        <circle cx="1" cy="1" r="{ry * 0.45:.1f}" fill="#1E140E"/>
        <circle cx="{ry * 0.35:.1f}" cy="{-ry * 0.35:.1f}" r="{ry * 0.25:.1f}" fill="#fff"/>
      </g>
      {path(f'M {-rx - 2},{2} Q 0,{-ry * 1.9:.1f} {rx + 2},{2}', stroke='#2A1A12', sw=4.5)}
      <g id="{p}-lid{side}">
        <ellipse cx="0" cy="0" rx="{rx + 3}" ry="{ry + 3}" fill="{{SKIN}}"/>
        {path(f'M {-rx - 3},{0} Q 0,{ry * 1.2:.1f} {rx + 3},{0}', stroke='#2A1A12', sw=4.5)}
      </g>
    </g>'''


# ---------------------------------------------------------------- karakterler
BROWS = {
    # (sol açı, sağ açı, dikey kayma)
    'neutral': (0, 0, 0),
    'confused': (-8, 14, -4),
    'worried': (-14, 14, -2),
    'determined': (12, -12, 3),
    'tired': (-5, 5, 6),
    'smug': (-2, 10, -4),
    'happy': (-6, 6, -6),
    'surprised': (-4, 4, -16),
    'asleep': (4, -4, 2),
}


def ayse(p, eyes='open', brow='neutral', mouth='closed', tilt=0, modern=False, variant='ayse'):
    """Ayşe (içinde Elif): sedirde oturan genç kadın. Orijin: oturduğu nokta."""
    skin, shade = '#F2C9A4', '#E0AF8A'
    teal, teal_d = '#3F7F7A', '#2F6662'
    fatma = variant in ('fatma', 'zehra')
    if variant == 'fatma':
        teal, teal_d = '#7A2E3A', '#5E2430'
        skin, shade = '#E9BC96', '#D6A47E'
    elif variant == 'zehra':
        teal, teal_d = '#5E4A7A', '#4A3A62'
        skin, shade = '#E2B48E', '#CFA07C'
    elif variant == 'leyla':
        teal, teal_d = '#C96B7A', '#A85462'
        skin, shade = '#F0C8A6', '#DDB08E'
    body_c, sleeve_c, skirt_c, cuff_c = (('#F3F6F6', '#F3F6F6', '#E3E9E9', '#3F7F7A') if modern
                                         else (teal, teal, teal_d, '#C99A3A'))
    bl, br, by = BROWS[brow]
    o_open = 'M -12,-282 Q 0,-300 12,-282 Q 0,-266 -12,-282 Z' if mouth != 'o' else ''
    mouth_closed = {'o': path('M -10,-276 Q 0,-280 10,-276', stroke='#8B3A3A', sw=4),
                    'flat': path('M -13,-279 Q 0,-281 13,-279', stroke='#8B3A3A', sw=4),
                    'smirk': path('M -15,-281 Q 3,-273 17,-289', stroke='#8B3A3A', sw=4)}.get(
                        mouth, path('M -15,-282 Q 0,-275 15,-282', stroke='#8B3A3A', sw=4))
    o_shape = (f'<ellipse cx="0" cy="-280" rx="11" ry="15" fill="#6A2222"/>'
               f'<ellipse cx="0" cy="-271" rx="7" ry="4" fill="#C9575A"/>')
    open_shape = (f'<ellipse cx="0" cy="-280" rx="14" ry="10" fill="#6A2222"/>'
                  f'<ellipse cx="0" cy="-274" rx="8" ry="4" fill="#C9575A"/>')
    eye_state = eyes
    INIT.append(f'gsap.set("#{p}-head", {{svgOrigin: "0 -255", rotation: {tilt}}});')
    svg = f'''
<g id="{p}">
  <!-- örtü arkası -->
  {path('M -84,-330 C -92,-420 -44,-452 0,-452 C 44,-452 92,-420 84,-330 L 92,-250 Q 0,-236 -92,-250 Z', fill='#4A2C1D', stroke=OUTLINE, sw=3) + ''.join(ell(92 + i * 4, -380 + i * 34, 20, 26, '#4A2C1D', f'stroke="{OUTLINE}" stroke-width="2.5"') for i in range(4)) if modern else
    path('M -102,-330 C -108,-430 -50,-470 0,-470 C 50,-470 108,-430 102,-330 L 128,-200 Q 0,-180 -128,-200 Z', fill='#EFE4CC', stroke=OUTLINE, sw=3)}
  <!-- etek -->
  {path('M -92,-60 L 92,-60 Q 150,40 165,190 L -165,190 Q -150,40 -92,-60 Z', fill=skirt_c, stroke=OUTLINE, sw=3)}
  {path('M -40,-50 Q -45,80 -60,185 M 40,-50 Q 48,80 62,185', stroke='#285955', sw=4)}
  {ell(-70, 196, 34, 13, '#C99A3A', f'stroke="{OUTLINE}" stroke-width="3"')}
  {ell(70, 196, 34, 13, '#C99A3A', f'stroke="{OUTLINE}" stroke-width="3"')}
  <!-- boyun ve gövde -->
  <rect x="-22" y="-268" width="44" height="45" fill="{shade}"/>
  {path('M -96,-212 Q -100,-232 -66,-236 L 66,-236 Q 100,-232 96,-212 L 90,-52 L -90,-52 Z', fill=body_c, stroke=OUTLINE, sw=3)}
  {path('M -30,-236 L 0,-180 L 30,-236 Z', fill=teal, stroke=OUTLINE, sw=2.5) + path('M -30,-236 L -6,-120 M 30,-236 L 6,-120', stroke='#B9C4C4', sw=4) + '<rect x="34" y="-190" width="38" height="22" rx="3" fill="#3F7F7A"/>' if modern else path('M -26,-236 L 0,-196 L 26,-236 Z', fill='#F4EBD9', stroke=OUTLINE, sw=2.5)}
  {'' if modern else path('M -60,-180 Q -40,-120 -62,-70 M 60,-180 Q 40,-120 62,-70', stroke=teal_d, sw=4)}
  {'' if modern else '<rect x="-92" y="-86" width="184" height="34" rx="6" fill="#C99A3A" stroke="' + OUTLINE + '" stroke-width="3"/>' + path('M -92,-75 L 92,-75 M -92,-63 L 92,-63', stroke='#A87A26', sw=3)}
  {'' if (modern or fatma) else ''.join(ell(-58 + i * -1.5, -232 + i * 33, 15, 19, '#4A2C1D', f'stroke="{OUTLINE}" stroke-width="2.5"') for i in range(5)) + ell(-64, -62, 10, 8, '#B8432F', f'stroke="{OUTLINE}" stroke-width="2"')}
  <!-- kollar -->
  {limb([(-90, -215), (-104, -130), (-40, -78)], sleeve_c, 40)}
  {limb([(90, -215), (104, -130), (40, -78)], sleeve_c, 40)}
  <rect x="-58" y="-98" width="22" height="40" rx="6" fill="{cuff_c}" stroke="{OUTLINE}" stroke-width="2.5" transform="rotate(-60 -47 -78)"/>
  <rect x="36" y="-98" width="22" height="40" rx="6" fill="{cuff_c}" stroke="{OUTLINE}" stroke-width="2.5" transform="rotate(60 47 -78)"/>
  {ell(-18, -74, 22, 17, skin, f'stroke="{OUTLINE}" stroke-width="3"')}
  {ell(18, -72, 22, 17, skin, f'stroke="{OUTLINE}" stroke-width="3"')}
  <!-- baş -->
  <g id="{p}-head">
    {path('M -72,-345 C -72,-402 -40,-428 0,-428 C 40,-428 72,-402 72,-345 C 72,-293 40,-254 0,-251 C -40,-254 -72,-293 -72,-345 Z', fill=skin, stroke=OUTLINE, sw=3)}
    {(path('M -76,-340 C -80,-424 -40,-446 0,-446 C 40,-446 80,-424 76,-340 C 64,-390 32,-400 4,-384 C -26,-402 -60,-390 -76,-340 Z', fill='#4A2C1D', stroke=OUTLINE, sw=2.5) + ell(-74, -312, 11, 34, '#4A2C1D', f'stroke="{OUTLINE}" stroke-width="2"')) if modern else
     path('M -72,-356 C -70,-410 -30,-430 0,-428 C 30,-430 70,-410 72,-356 C 58,-386 32,-394 6,-380 C -24,-396 -56,-388 -72,-356 Z', fill='#4A2C1D', stroke=OUTLINE, sw=2.5)
     + path('M -84,-352 C -88,-432 -42,-466 0,-466 C 42,-466 88,-432 84,-352 C 76,-404 42,-436 0,-436 C -42,-436 -76,-404 -84,-352 Z', fill='#F4EBD8', stroke=OUTLINE, sw=3)
     + ('' if fatma else ''.join(f'<circle cx="{78 * math.cos(math.radians(a)):.1f}" cy="{-352 - 80 * math.sin(math.radians(a)):.1f}" r="4" fill="#B8432F"/>' for a in range(18, 170, 13)))}
    {path('M -44,-322 q 12,6 24,0 M 20,-322 q 12,6 24,0 M -30,-290 q -6,8 -2,16 M 30,-290 q 6,8 2,16', stroke='#B98564', sw=2.5) if variant == 'zehra' else ''}
    {ell(-46, -303, 14, 8, '#E8958A', 'opacity=".45"')}
    {ell(46, -303, 14, 8, '#E8958A', 'opacity=".45"')}
    {eye(p, 'L', -31, -338, 17, 12, '#6B4A2A', eye_state)}
    {eye(p, 'R', 31, -338, 17, 12, '#6B4A2A', eye_state)}
    <g id="{p}-browL" transform="translate(-31,{-366 + by}) rotate({bl})">{path('M -17,2 Q 0,-7 17,0', stroke='#4A2C1D', sw=6)}</g>
    <g id="{p}-browR" transform="translate(31,{-366 + by}) rotate({br})">{path('M -17,0 Q 0,-7 17,2', stroke='#4A2C1D', sw=6)}</g>
    {path('M -2,-326 Q 5,-312 -5,-305', stroke='#C28A68', sw=3.5)}
    <g id="{p}-mouthC">{mouth_closed}</g>
    <g id="{p}-mouthO" opacity="0">{o_shape if mouth == 'o' else open_shape}</g>
  </g>
</g>'''
    return svg.replace('{SKIN}', skin)


MEN = {
    # cübbe, iç entari, kuşak, kuşak çizgisi, ten, sakal
    'huseyin': ('#6E4B2F', '#717D3E', '#B2452E', '#E3B65A', '#DDA57C', 'full'),
    'hekim': ('#2E3F5E', '#9A9A86', '#5E2E5E', '#C9A55A', '#D9A47E', 'goatee'),
    'subasi': ('#8E2B22', '#D7B25A', '#3B3431', '#C9A55A', '#C98E64', 'mustache'),
    'riza': ('#7A6A4F', '#C9B48A', '#4E5C3A', '#D7B25A', '#C98E64', 'full'),
    'kadi': ('#E8E2D0', '#3F6B3F', '#C9A55A', '#8E6A2A', '#E2B48E', 'white'),
    'denizci': ('#2E4A6B', '#F2ECDD', '#B2452E', '#E3B65A', '#B9805A', 'mustache'),
    'yusuf': ('#5E7A3A', '#E3D9C0', '#6E4B2F', '#C9A55A', '#E0AE88', 'none'),
    # 2026: eczane sahibi Kemal Bey (beyaz önlük, mavi gömlek, gözlük)
    'kemal': ('#F3F6F6', '#8FB3C9', '#3F7F7A', '#2E5F5A', '#D9A47E', 'mustache_gray'),
}


def huseyin(p, brow='neutral', arm=0, variant='huseyin'):
    """Ayakta duran erkek karakter (Hüseyin, Hekim, Subaşı). Orijin: ayakların ortası."""
    coat, inner, sash, sash2, skin, beard = MEN[variant]
    bl, br, by = BROWS[brow]
    INIT.append(f'gsap.set("#{p}-arm", {{svgOrigin: "98 -628", rotation: {arm}}});')
    INIT.append(f'gsap.set("#{p}-head", {{svgOrigin: "0 -680"}});')
    if beard == 'full':
        beard_svg = (path('M -68,-778 C -72,-702 -46,-648 0,-640 C 46,-648 72,-702 68,-778 C 58,-738 38,-722 0,-722 C -38,-722 -58,-738 -68,-778 Z', fill='#3B3431', stroke=OUTLINE, sw=3)
                     + path('M -40,-700 Q -34,-680 -26,-666 M 30,-702 Q 26,-684 20,-668 M -6,-690 L -4,-660', stroke='#8A8580', sw=3))
        stache = path('M -32,-728 Q -14,-744 0,-734 Q 14,-744 32,-728 Q 16,-720 0,-726 Q -16,-720 -32,-728 Z', fill='#3B3431', stroke=OUTLINE, sw=2.5)
    elif beard == 'white':
        beard_svg = (path('M -68,-778 C -74,-680 -40,-590 0,-570 C 40,-590 74,-680 68,-778 C 58,-738 38,-722 0,-722 C -38,-722 -58,-738 -68,-778 Z', fill='#EEEBE4', stroke=OUTLINE, sw=3)
                     + path('M -36,-690 Q -30,-640 -18,-600 M 26,-692 Q 22,-650 14,-610 M -4,-680 L -2,-590', stroke='#C9C4BA', sw=3))
        stache = path('M -32,-728 Q -14,-744 0,-734 Q 14,-744 32,-728 Q 16,-720 0,-726 Q -16,-720 -32,-728 Z', fill='#EEEBE4', stroke=OUTLINE, sw=2.5)
    elif beard == 'mustache_gray':
        beard_svg = ''
        stache = path('M -40,-726 Q -18,-746 0,-734 Q 18,-746 40,-726 Q 22,-718 0,-728 Q -22,-718 -40,-726 Z', fill='#8C8682', stroke=OUTLINE, sw=2.5)
    elif beard == 'none':
        beard_svg = ''
        stache = ''
    elif beard == 'goatee':
        beard_svg = path('M -34,-716 C -34,-690 -14,-640 0,-622 C 14,-640 34,-690 34,-716 C 20,-706 -20,-706 -34,-716 Z', fill='#2A2422', stroke=OUTLINE, sw=3)
        stache = path('M -30,-728 Q -14,-740 0,-733 Q 14,-740 30,-728 Q 14,-723 0,-728 Q -14,-723 -30,-728 Z', fill='#2A2422', stroke=OUTLINE, sw=2.5)
    else:
        beard_svg = ''
        stache = path('M -56,-724 Q -30,-752 0,-736 Q 30,-752 56,-724 Q 44,-716 30,-726 Q 14,-722 0,-728 Q -14,-722 -30,-726 Q -44,-716 -56,-724 Z', fill='#1E1A18', stroke=OUTLINE, sw=2.5)
    if variant == 'hekim':
        hat = (path('M -78,-842 C -82,-960 -40,-990 0,-990 C 40,-990 82,-960 78,-842 C 60,-826 -60,-826 -78,-842 Z', fill='#F4F0E6', stroke=OUTLINE, sw=3)
               + path('M -80,-870 Q 0,-892 80,-870 L 80,-846 Q 0,-866 -80,-846 Z', fill='#3F6B3F', stroke=OUTLINE, sw=2.5)
               + path('M -60,-930 Q 0,-950 60,-930 M -70,-900 Q 0,-920 70,-900', stroke='#D8D0BE', sw=3))
    elif variant == 'kadi':
        hat = (path('M -92,-836 C -100,-990 -50,-1040 0,-1040 C 50,-1040 100,-990 92,-836 C 70,-816 -70,-816 -92,-836 Z', fill='#F7F4EC', stroke=OUTLINE, sw=3)
               + path('M -94,-870 Q 0,-896 94,-870 L 94,-844 Q 0,-868 -94,-844 Z', fill='#C9A55A', stroke=OUTLINE, sw=2.5)
               + path('M -70,-940 Q 0,-962 70,-940 M -80,-905 Q 0,-928 80,-905 M -55,-985 Q 0,-1000 55,-985', stroke='#DCD5C4', sw=3.5))
    elif variant == 'yusuf':
        hat = (path('M -66,-830 C -66,-900 66,-900 66,-830 Z', fill='#F4F0E6', stroke=OUTLINE, sw=3)
               + path('M -60,-812 Q 0,-852 60,-812 Q 0,-828 -60,-812 Z', fill='#2E2018', stroke=OUTLINE, sw=2))
    elif variant in ('riza', 'denizci'):
        hat = (path('M -52,-850 L -46,-905 Q 0,-918 46,-905 L 52,-850 Z', fill='#A33A2E', stroke=OUTLINE, sw=3)
               + path('M 0,-912 Q 30,-920 40,-880', stroke='#1E1A18', sw=4))
    elif variant == 'kemal':
        # kısa kır saç + gözlük
        hat = (path('M -70,-790 C -76,-860 -40,-884 0,-884 C 40,-884 76,-860 70,-790 C 62,-830 40,-846 0,-844 C -40,-846 -62,-830 -70,-790 Z', fill='#8C8682', stroke=OUTLINE, sw=3)
               + '<g fill="rgba(220,235,240,.25)" stroke="#2A2422" stroke-width="4">'
               + '<rect x="-52" y="-798" width="42" height="32" rx="10"/><rect x="10" y="-798" width="42" height="32" rx="10"/></g>'
               + path('M -10,-784 L 10,-784', stroke='#2A2422', sw=4))
    elif variant == 'subasi':
        hat = (path('M -66,-836 C -70,-940 -30,-1010 20,-1000 C 60,-990 72,-930 66,-836 Z', fill='#A33A2E', stroke=OUTLINE, sw=3)
               + '<rect x="-74" y="-860" width="148" height="34" rx="6" fill="#D7B25A" stroke="' + OUTLINE + '" stroke-width="3"/>'
               + path('M -60,-843 L 60,-843', stroke='#A87A26', sw=3))
    else:
        hat = (path('M -40,-892 C -40,-930 40,-930 40,-892 Z', fill='#A33A2E', stroke=OUTLINE, sw=3)
               + path('M -96,-838 C -100,-900 -40,-908 0,-904 C 40,-908 100,-900 96,-838 C 90,-812 50,-806 0,-808 C -50,-806 -90,-812 -96,-838 Z', fill='#F2ECDD', stroke=OUTLINE, sw=3)
               + path('M -88,-858 Q -20,-890 60,-892 M -92,-838 Q 0,-866 92,-850 M -70,-818 Q 10,-842 90,-826', stroke='#CFC3A8', sw=3.5))
    mouth_y = -712 if beard == 'mustache' else -718
    svg = f"""
<g id="{p}">
  {ell(0, 0, 120, 16, 'rgba(40,20,10,.25)')}
  {ell(-38, -12, 34, 14, '#C8952E', f'stroke="{OUTLINE}" stroke-width="3"')}
  {ell(38, -12, 34, 14, '#C8952E', f'stroke="{OUTLINE}" stroke-width="3"')}
  {path('M -102,-640 Q -60,-664 0,-662 Q 60,-664 102,-640 L 138,-22 L -138,-22 Z', fill=coat, stroke=OUTLINE, sw=3)}
  {path('M -38,-656 L 38,-656 L 52,-22 L -52,-22 Z', fill=inner, stroke=OUTLINE, sw=3)}
  {''.join(f'<circle cx="0" cy="{-600 + i * 38}" r="5" fill="#D7B25A" stroke="{OUTLINE}" stroke-width="1.5"/>' for i in range(5))}
  {path('M -70,-380 L -88,-30 M 70,-380 L 88,-30', stroke='rgba(0,0,0,.25)', sw=4)}
  <rect x="-112" y="-440" width="224" height="40" rx="8" fill="{sash}" stroke="{OUTLINE}" stroke-width="3"/>
  {path('M -112,-428 L 112,-428 M -112,-413 L 112,-413', stroke=sash2, sw=3)}
  {limb([(-98, -628), (-122, -480), (-112, -380)], coat, 46)}
  {ell(-112, -366, 20, 22, skin, f'stroke="{OUTLINE}" stroke-width="3"')}
  <g id="{p}-arm">
    {limb([(98, -628), (122, -480), (112, -380)], coat, 46)}
    {ell(112, -366, 20, 22, skin, f'stroke="{OUTLINE}" stroke-width="3"')}
  </g>
  <g id="{p}-head">
    {ell(-70, -762, 13, 20, skin, f'stroke="{OUTLINE}" stroke-width="3"')}
    {ell(70, -762, 13, 20, skin, f'stroke="{OUTLINE}" stroke-width="3"')}
    {path('M -68,-772 C -68,-830 -36,-852 0,-852 C 36,-852 68,-830 68,-772 C 68,-712 40,-668 0,-664 C -40,-668 -68,-712 -68,-772 Z', fill=skin, stroke=OUTLINE, sw=3)}
    {beard_svg}
    <g id="{p}-mouthC">{path(f'M -11,{mouth_y} Q 0,{mouth_y + 4} 11,{mouth_y}', stroke='#2A1A18', sw=3.5)}</g>
    <g id="{p}-mouthO" opacity="0"><ellipse cx="0" cy="{mouth_y + 4}" rx="12" ry="9" fill="#5A1E1E"/></g>
    {stache}
    {path('M -4,-778 Q 12,-748 -2,-744', stroke='rgba(120,70,40,.6)', sw=4)}
    {eye(p, 'L', -28, -782, 14, 10, '#4B3420', 'open')}
    {eye(p, 'R', 28, -782, 14, 10, '#4B3420', 'open')}
    <g id="{p}-browL" transform="translate(-29,{-806 + by}) rotate({bl})">{path('M -17,3 Q 0,-7 17,0', stroke='#2A2422', sw=9)}</g>
    <g id="{p}-browR" transform="translate(29,{-806 + by}) rotate({br})">{path('M -17,0 Q 0,-7 17,3', stroke='#2A2422', sw=9)}</g>
    {hat}
  </g>
</g>"""
    return svg.replace('{SKIN}', skin)


def mehmet(p, eyes='closed', mouth='flat', sick=True, cloth=False):
    """Yatakta yastığa yaslanmış hasta çocuk. Orijin: göğüs (yorgan buradan başlar)."""
    skin = '#EBC09A'
    INIT.append(f'gsap.set("#{p}-head", {{svgOrigin: "0 -95"}});')
    cheeks = '#E0605A' if sick else '#E8958A'
    drops = ''.join(f'<path id="{p}-ter{i}" d="M {x},{y} q 7,12 0,17 q -7,-5 0,-17 Z" fill="#8FC9E6" stroke="#4E8FB0" stroke-width="1.5"/>'
                    for i, (x, y) in enumerate(((-52, -214), (50, -200)))) if sick else ''
    mouths = {'flat': path('M -10,-112 Q 0,-114 10,-112', stroke='#8B3A3A', sw=3.5),
              'smile': path('M -13,-115 Q 0,-104 13,-115', stroke='#8B3A3A', sw=3.5)}
    svg = f"""
<g id="{p}">
  {path('M -70,-80 Q -74,-96 -50,-100 L 50,-100 Q 74,-96 70,-80 L 66,40 L -66,40 Z', fill='#F4EFE4', stroke=OUTLINE, sw=3)}
  {path('M -18,-100 L 0,-70 L 18,-100', stroke=OUTLINE, sw=2.5)}
  <g id="{p}-head">
    {path('M -56,-160 C -56,-206 -30,-226 0,-226 C 30,-226 56,-206 56,-160 C 56,-118 32,-92 0,-90 C -32,-92 -56,-118 -56,-160 Z', fill=skin, stroke=OUTLINE, sw=3)}
    {path('M -58,-168 C -62,-220 -30,-240 0,-240 C 32,-240 62,-222 58,-168 C 48,-196 30,-204 12,-196 C 0,-206 -20,-206 -30,-196 C -40,-204 -52,-192 -58,-168 Z', fill='#2E2018', stroke=OUTLINE, sw=2.5)}
    {ell(-34, -128, 12, 7, cheeks, 'opacity=".6"')}{ell(34, -128, 12, 7, cheeks, 'opacity=".6"')}
    {eye(p, 'L', -22, -160, 13, 9, '#4B3420', eyes)}
    {eye(p, 'R', 22, -160, 13, 9, '#4B3420', eyes)}
    <g id="{p}-browL" transform="translate(-22,-182) rotate(-10)">{path('M -12,2 Q 0,-5 12,0', stroke='#2E2018', sw=5)}</g>
    <g id="{p}-browR" transform="translate(22,-182) rotate(10)">{path('M -12,0 Q 0,-5 12,2', stroke='#2E2018', sw=5)}</g>
    {path('M -1,-150 Q 4,-140 -3,-136', stroke='#C28A68', sw=3)}
    <g id="{p}-mouthC">{mouths.get(mouth, mouths['flat'])}</g>
    <g id="{p}-mouthO" opacity="0"><ellipse cx="0" cy="-112" rx="8" ry="6" fill="#6A2222"/></g>
    {drops}
    {('<g id="' + p + '-bez"><rect x="-46" y="-214" width="92" height="30" rx="8" fill="#FFFFFF" stroke="' + OUTLINE + '" stroke-width="3"/>' + path('M -40,-202 L 40,-202', stroke='#C9D3D3', sw=3) + '</g>') if cloth else ''}
  </g>
</g>"""
    return svg.replace('{SKIN}', skin)


# ---------------------------------------------------------------- mekânlar
def jar(x, y, w, h, content, lid='#9B6B3F'):
    body = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w * 0.18:.0f}" fill="#CFE0DA" fill-opacity=".55" stroke="{OUTLINE}" stroke-width="3"/>'
            f'<rect x="{x + 5}" y="{y + h * 0.35:.0f}" width="{w - 10}" height="{h * 0.62:.0f}" rx="{w * 0.14:.0f}" fill="{content}"/>'
            f'<rect x="{x + w * 0.15:.0f}" y="{y + 10}" width="{w * 0.12:.0f}" height="{h * 0.7:.0f}" rx="4" fill="#fff" opacity=".45"/>'
            f'<rect x="{x - 4}" y="{y - 16}" width="{w + 8}" height="22" rx="6" fill="{lid}" stroke="{OUTLINE}" stroke-width="3"/>')
    return body


def herb_bundle(x, y, length, color):
    leaves = ''.join(ell(x + (i % 3 - 1) * 12, y + 40 + i * (length / 9), 13, 24, color,
                         f'transform="rotate({(i % 2) * 30 - 15} {x} {y + 40 + i * (length / 9):.0f})" stroke="{OUTLINE}" stroke-width="2"')
                     for i in range(8))
    return (path(f'M {x},{y - 60} L {x},{y + 30}', stroke='#7A5A3A', sw=3) + leaves +
            f'<rect x="{x - 14}" y="{y + 20}" width="28" height="14" rx="4" fill="#B2452E" stroke="{OUTLINE}" stroke-width="2"/>')


def shop_bg(p='dk', mortar=False):
    jars_top = ''.join(jar(60 + i * 96, 430, 70, 90, c) for i, c in enumerate(['#D9822B', '#7B4A2A', '#C96B7A', '#6F8F3E']))
    jars_mid = ''.join(jar(70 + i * 120, 620, 84, 76, c) for i, c in enumerate(['#E3C35A', '#8E5A3A', '#F1ECE0']))
    jars_low = ''.join(jar(60 + i * 96, 800, 70, 94, c) for i, c in enumerate(['#A0442F', '#5E7A3A', '#D9822B', '#9A7AA8']))
    planks = ''.join(f'<rect x="0" y="{y}" width="1080" height="{(1920 - y) / 7:.0f}" fill="{c}"/>'
                     for y, c in zip(range(1460, 1920, 66), ['#8B5E3B', '#835838', '#8B5E3B', '#7E5535', '#8B5E3B', '#835838', '#8B5E3B']))
    kilim = ''.join(f'<polygon points="{x},1700 {x + 30},1670 {x + 60},1700 {x + 30},1730" fill="#E3B65A" stroke="{OUTLINE}" stroke-width="2"/>'
                    for x in range(560, 1060, 80))
    return f'''
  <rect width="1080" height="1920" fill="#E6D2AE"/>
  <path d="M 0,1460 L 1080,1460 L 1080,1920 L 0,1920 Z" fill="#8B5E3B"/>{planks}
  <rect x="0" y="1440" width="1080" height="26" fill="#6B4528"/>
  <!-- duvar lekeleri, çatlaklar -->
  {ell(250, 330, 90, 50, '#DCC59E', 'opacity=".6"')}{ell(880, 1080, 120, 60, '#DCC59E', 'opacity=".5"')}
  {path('M 520,300 l 20,40 l -14,34 l 22,30', stroke='#B79A72', sw=3)}
  {path('M 600,1250 l -18,30 l 12,26', stroke='#B79A72', sw=3)}
  <!-- tavan kirişleri -->
  <rect x="0" y="0" width="1080" height="150" fill="#5A3A24"/>
  {''.join(f'<rect x="{x}" y="140" width="58" height="46" fill="#4A2E1C" stroke="{OUTLINE}" stroke-width="3"/>' for x in range(30, 1080, 200))}
  <rect x="0" y="150" width="1080" height="18" fill="#6B4528"/>
  {herb_bundle(150, 230, 120, '#7C9A4A')}{herb_bundle(330, 220, 100, '#B9A04A')}{herb_bundle(950, 230, 110, '#7C9A4A')}
  <!-- raflar -->
  {''.join(f'<rect x="30" y="{y}" width="460" height="22" fill="#7A5132" stroke="{OUTLINE}" stroke-width="3"/>' for y in (520, 696, 894))}
  {jars_top}{jars_mid}{jars_low}
  {stone_mortar(440, 660, 0.3, p) if mortar else ''}
  <!-- pencere -->
  <path d="M 640,880 L 640,560 Q 640,420 810,410 Q 980,420 980,560 L 980,880 Z" fill="#6B4528" stroke="{OUTLINE}" stroke-width="4"/>
  <path d="M 668,860 L 668,566 Q 668,446 810,438 Q 952,446 952,566 L 952,860 Z" fill="#BFDDEB"/>
  {ell(810, 860, 160, 40, '#6FA3B8')}
  <path d="M 700,800 Q 760,760 810,780 Q 870,750 940,790 L 940,860 L 700,860 Z" fill="#A9B7A0"/>
  <path d="M 770,770 Q 770,720 810,716 Q 850,720 850,770 Z" fill="#D9CDB5" stroke="#B9AC90" stroke-width="2"/>
  <rect x="752" y="700" width="8" height="72" fill="#D9CDB5"/><rect x="860" y="700" width="8" height="72" fill="#D9CDB5"/>
  <path d="M 810,438 L 810,860 M 668,650 L 952,650" stroke="#6B4528" stroke-width="12"/>
  <rect x="620" y="872" width="380" height="28" rx="4" fill="#7A5132" stroke="{OUTLINE}" stroke-width="3"/>
  <!-- tezgâh -->
  <rect x="20" y="1210" width="460" height="250" fill="#7A5132" stroke="{OUTLINE}" stroke-width="4"/>
  <rect x="10" y="1190" width="480" height="34" fill="#8E623E" stroke="{OUTLINE}" stroke-width="4"/>
  {path('M 60,1260 L 440,1260 M 60,1340 L 440,1340', stroke='#5E3E25', sw=4)}
  <!-- terazi -->
  {path('M 120,1190 L 120,1060 M 60,1070 L 180,1070', stroke='#B08A3C', sw=6)}
  {path('M 60,1070 L 45,1120 L 75,1120 Z M 180,1070 L 165,1120 L 195,1120 Z', fill='#D7B25A', stroke=OUTLINE, sw=2.5)}
  <!-- havan -->
  {path('M 330,1190 L 312,1130 L 408,1130 L 390,1190 Z', fill='#8C8C8C', stroke=OUTLINE, sw=3)}
  {path('M 380,1140 L 420,1070', stroke='#9E9E9E', sw=16)}
  <!-- sedir -->
  <rect x="560" y="1150" width="520" height="190" rx="24" fill="#B2452E" stroke="{OUTLINE}" stroke-width="4"/>
  {''.join(f'<rect x="{x}" y="1160" width="110" height="170" rx="20" fill="#C99A3A" stroke="{OUTLINE}" stroke-width="3"/>' for x in (590, 960))}
  <rect x="540" y="1330" width="540" height="110" rx="10" fill="#8C3B2E" stroke="{OUTLINE}" stroke-width="4"/>
  {path('M 540,1360 L 1080,1360 M 540,1410 L 1080,1410', stroke='#E3B65A', sw=4)}
  <!-- kilim -->
  <rect x="520" y="1640" width="560" height="130" fill="#A33A2E" stroke="{OUTLINE}" stroke-width="3"/>{kilim}'''


def window_view(p='w'):
    houses = ''
    for i in range(14):
        x = 40 + i * 74
        y = 1180 + (i * 37 % 60)
        houses += (f'<rect x="{x}" y="{y}" width="64" height="90" fill="#EADBC0" stroke="#B9A889" stroke-width="2"/>'
                   f'<polygon points="{x - 6},{y} {x + 32},{y - 30} {x + 70},{y}" fill="#A9553A"/>'
                   f'<rect x="{x + 22}" y="{y + 30}" width="18" height="26" fill="#7A5132"/>')
    return f'''
  <defs><linearGradient id="{p}-gok" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#9CCBE0"/><stop offset=".7" stop-color="#E9E2CC"/></linearGradient></defs>
  <rect width="1080" height="1920" fill="url(#{p}-gok)"/>
  <circle cx="820" cy="520" r="60" fill="#FFF3C4"/>
  <path d="M 0,1000 Q 200,900 420,960 Q 640,880 820,950 Q 960,900 1080,940 L 1080,1100 L 0,1100 Z" fill="#A9B7A0"/>
  <!-- cami silueti -->
  <g fill="#D9CDB5" stroke="#B3A685" stroke-width="3">
    <path d="M 420,960 Q 420,830 540,820 Q 660,830 660,960 Z"/>
    <path d="M 360,960 Q 360,900 410,896 Q 460,900 460,960 Z"/><path d="M 620,960 Q 620,900 670,896 Q 720,900 720,960 Z"/>
    <rect x="300" y="720" width="18" height="240"/><rect x="762" y="720" width="18" height="240"/>
    <rect x="380" y="780" width="14" height="180"/><rect x="686" y="780" width="14" height="180"/>
    <polygon points="300,720 309,670 318,720"/><polygon points="762,720 771,670 780,720"/>
    <polygon points="380,780 387,742 394,780"/><polygon points="686,780 693,742 700,780"/>
    <rect x="340" y="950" width="400" height="40"/>
  </g>
  <rect x="0" y="1090" width="1080" height="120" fill="#6FA3B8"/>
  {''.join(f'<rect x="{x}" y="{y}" width="{w}" height="4" fill="#fff" opacity=".5"/>' for x, y, w in ((120, 1120, 90), (520, 1150, 140), (840, 1130, 70)))}
  <g id="{p}-kayik">
    <path d="M 160,1150 Q 220,1172 290,1150 L 280,1166 Q 220,1180 170,1166 Z" fill="#7A5132"/>
    <polygon points="222,1150 222,1080 268,1146" fill="#F4EBD8" stroke="#B9A889" stroke-width="2"/>
  </g>
  {houses}
  <rect x="0" y="1270" width="1080" height="650" fill="#EADBC0"/>
  {''.join(f'<path id="{p}-kus{i}" d="M {x},{y} q 12,-10 24,0 q 12,-10 24,0" stroke="#4A3A30" stroke-width="4" fill="none"/>' for i, (x, y) in enumerate(((260, 640), (330, 600), (400, 660))))}
  <!-- pencere çerçevesi -->
  <path fill="#6B4528" fill-rule="evenodd" stroke="{OUTLINE}" stroke-width="5"
        d="M 0,0 L 1080,0 L 1080,1920 L 0,1920 Z M 120,1500 L 120,560 Q 120,300 540,280 Q 960,300 960,560 L 960,1500 Z"/>
  <path d="M 540,280 L 540,1500 M 120,900 L 960,900" stroke="#6B4528" stroke-width="22"/>
  <rect x="60" y="1480" width="960" height="70" rx="6" fill="#7A5132" stroke="{OUTLINE}" stroke-width="4"/>
  {path('M 760,1480 L 740,1380 L 840,1380 L 820,1480 Z', fill='#A9553A', stroke=OUTLINE, sw=3)}
  {''.join(ell(790 + dx, 1360 + dy, 22, 34, '#6F8F3E', f'stroke="{OUTLINE}" stroke-width="2" transform="rotate({r} {790 + dx} {1360 + dy})"') for dx, dy, r in ((-30, -10, -30), (0, -40, 0), (30, -10, 30)))}'''


def jars_closeup(p='k', labels=False):
    jars = ''.join(jar(60 + i * 250, 520, 190, 300, c) for i, c in enumerate(['#D9822B', '#C96B7A', '#6F8F3E', '#E3C35A', '#7B4A2A']))
    jars2 = ''.join(jar(130 + i * 260, 1080, 200, 280, c) for i, c in enumerate(['#8E5A3A', '#F1ECE0', '#9A7AA8', '#A0442F']))
    tags = ''.join(f'<rect x="{x}" y="{y}" width="70" height="44" rx="4" fill="#F4EBD8" stroke="{OUTLINE}" stroke-width="2.5" transform="rotate(-8 {x} {y})"/>'
                   f'{path(f"M {x + 10},{y + 18} l 40,-4 M {x + 12},{y + 30} l 30,-3", stroke="#8B6B4A", sw=3)}'
                   for x, y in ((100, 700), (620, 690), (1130, 700), (440, 1250), (960, 1250)))
    glows = ''
    if labels:
        tags = ''
        for i, (name, cx) in enumerate((('Kekik', 655), ('Bal', 905), ('Söğüt kabuğu', 1155))):
            glows += f'<circle id="{p}-glow{i}" cx="{cx}" cy="670" r="190" fill="url(#{p}-g)" opacity="0"/>'
            tags += (f'<g transform="rotate(-5 {cx} 760)"><rect x="{cx - 95}" y="720" width="190" height="74" rx="8" fill="#F4EBD8" stroke="{OUTLINE}" stroke-width="3"/>'
                     f'<text x="{cx}" y="770" text-anchor="middle" font-family="Nunito" font-style="italic" font-weight="800" font-size="{34 if len(name) < 8 else 26}" fill="#5A3A24">{name}</text></g>')
    dust = ''.join(f'<circle id="{p}-toz{i}" cx="{(i * 137) % 1300}" cy="{300 + (i * 211) % 1300}" r="{3 + i % 3}" fill="#FFF3C4" opacity=".7"/>' for i in range(14))
    return f'''
  <defs><radialGradient id="{p}-g"><stop offset="0" stop-color="#FFE9A8" stop-opacity=".95"/><stop offset="1" stop-color="#FFE9A8" stop-opacity="0"/></radialGradient></defs>
  <rect width="1400" height="1920" fill="#E1CBA4"/>
  {glows}
  <rect x="0" y="820" width="1400" height="40" fill="#7A5132" stroke="{OUTLINE}" stroke-width="4"/>
  <rect x="0" y="1360" width="1400" height="40" fill="#7A5132" stroke="{OUTLINE}" stroke-width="4"/>
  {jars}{jars2}{tags}
  {herb_bundle(200, 140, 200, '#7C9A4A')}{herb_bundle(620, 120, 180, '#B9A04A')}{herb_bundle(1100, 150, 200, '#7C9A4A')}
  {dust}'''




def stone_mortar(cx, cy, s, p, glow=True, color='#FFD36A'):
    """Gizemli taş havan. Kabartma yazı şeridi parlar (id: {p}-yazi, {p}-hale)."""
    glyphs = ''.join(path(f'M {cx + (i - 3.5) * 26 * s:.0f},{cy + 10 * s:.0f} q {6 * s:.0f},{-14 * s:.0f} {12 * s:.0f},0 t {12 * s:.0f},0',
                          stroke=color, sw=4 * s) for i in range(8))
    hale = (f'<circle id="{p}-hale" cx="{cx}" cy="{cy}" r="{200 * s:.0f}" fill="url(#{p}-hg)" opacity=".35"/>' if glow else '')
    return f'''
  <defs><radialGradient id="{p}-hg"><stop offset="0" stop-color="{color}" stop-opacity=".9"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>
  {hale}
  {path(f'M {cx - 130 * s:.0f},{cy - 60 * s:.0f} L {cx + 130 * s:.0f},{cy - 60 * s:.0f} L {cx + 100 * s:.0f},{cy + 90 * s:.0f} Q {cx},{cy + 110 * s:.0f} {cx - 100 * s:.0f},{cy + 90 * s:.0f} Z', fill='#8E8A84', stroke=OUTLINE, sw=4 * s)}
  {ell(cx, cy - 60 * s, 130 * s, 26 * s, '#6E6A65', f'stroke="{OUTLINE}" stroke-width="{4 * s:.1f}"')}
  {ell(cx, cy - 56 * s, 104 * s, 16 * s, '#3E3A36')}
  <rect x="{cx - 112 * s:.0f}" y="{cy - 8 * s:.0f}" width="{224 * s:.0f}" height="{34 * s:.0f}" fill="#7A766F"/>
  <g id="{p}-yazi" opacity=".35">{glyphs}</g>
  {path(f'M {cx + 30 * s:.0f},{cy - 60 * s:.0f} L {cx + 120 * s:.0f},{cy - 190 * s:.0f}', stroke=OUTLINE, sw=34 * s)}
  {path(f'M {cx + 30 * s:.0f},{cy - 60 * s:.0f} L {cx + 120 * s:.0f},{cy - 190 * s:.0f}', stroke='#9E9A94', sw=27 * s)}'''


def pharmacy_bg(p):
    """2026, gece nöbetindeki eczane."""
    cols = ['#E8F1F8', '#F4C7C3', '#BFE3C0', '#FFE7A8', '#C9D7F2', '#FFFFFF', '#F2D3E8']
    boxes = ''
    for r, y in enumerate((330, 520, 710, 900)):
        x = 60
        i = r * 3
        while x < 1000:
            w = 60 + (i * 37 % 50)
            h = 90 + (i * 23 % 60)
            c = cols[i % len(cols)]
            boxes += (f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" rx="4" fill="{c}" stroke="#7D8A8A" stroke-width="2.5"/>'
                      f'<rect x="{x + 6}" y="{y - h + 14}" width="{w - 12}" height="10" fill="{cols[(i + 3) % len(cols)]}"/>')
            x += w + 8
            i += 1
    tiles = ''.join(f'<rect x="{x}" y="{y}" width="134" height="64" fill="{"#C9D3D3" if (x // 135 + y // 65) % 2 else "#D4DDDD"}"/>'
                    for x in range(0, 1080, 135) for y in range(1700, 1920, 65))
    return f'''
  <defs><filter id="{p}-blur"><feGaussianBlur stdDeviation="14"/></filter></defs>
  <rect width="1080" height="1920" fill="#D7E4E2"/>
  <rect x="0" y="0" width="1080" height="120" fill="#EEF3F3"/>
  <rect x="140" y="40" width="300" height="26" rx="10" fill="#FFFFFF"/><rect x="640" y="40" width="300" height="26" rx="10" fill="#FFFFFF"/>
  <rect x="140" y="40" width="300" height="26" rx="10" fill="#FFFFFF" filter="url(#{p}-blur)" opacity=".8"/>
  <!-- raflar -->
  {''.join(f'<rect x="40" y="{y}" width="1000" height="18" fill="#F7FAFA" stroke="#7D8A8A" stroke-width="3"/>' for y in (330, 520, 710, 900))}
  {boxes}
  <!-- neon haç -->
  <g transform="translate(900,170)">
    <path d="M -22,-60 L 22,-60 L 22,-22 L 60,-22 L 60,22 L 22,22 L 22,60 L -22,60 L -22,22 L -60,22 L -60,-22 L -22,-22 Z" fill="#2BB673" filter="url(#{p}-blur)"/>
    <path id="{p}-hac" d="M -22,-60 L 22,-60 L 22,-22 L 60,-22 L 60,22 L 22,22 L 22,60 L -22,60 L -22,22 L -60,22 L -60,-22 L -22,-22 Z" fill="#5BE39A" stroke="#1E8F57" stroke-width="4"/>
  </g>
  <!-- saat: 03.12 -->
  <g transform="translate(160,190)">
    <circle r="56" fill="#FFFFFF" stroke="#4E5C5C" stroke-width="6"/>
    {path('M 0,0 L 18,-4', stroke='#2E3A3A', sw=7)}{path('M 0,0 L 22,30', stroke='#2E3A3A', sw=4)}
  </g>
  <rect x="0" y="1000" width="1080" height="700" fill="#C6D8D5"/>
  {tiles}'''


def pharmacy_front(p):
    """Elif'in önündeki tezgâh (karakterin üstüne çizilir)."""
    return f'''
  <rect x="0" y="1300" width="1080" height="420" fill="#2F6F6B" stroke="{OUTLINE}" stroke-width="4"/>
  <rect x="-10" y="1270" width="1100" height="40" fill="#F4F7F7" stroke="{OUTLINE}" stroke-width="4"/>
  <text x="540" y="1530" text-anchor="middle" font-family="Nunito" font-style="italic" font-weight="800" font-size="110" fill="#E9F4F2" letter-spacing="8">ECZANE</text>
  <!-- monitör -->
  <rect x="120" y="1080" width="280" height="180" rx="10" fill="#1F2B2E" stroke="{OUTLINE}" stroke-width="4"/>
  <rect x="136" y="1096" width="248" height="148" rx="4" fill="#3A8FB0"/>
  {path('M 156,1130 L 330,1130 M 156,1160 L 300,1160 M 156,1190 L 340,1190', stroke='#BFE6F2', sw=8)}
  <rect x="236" y="1258" width="48" height="14" fill="#1F2B2E"/>
  <!-- reçeteler -->
  <rect x="430" y="1232" width="120" height="44" fill="#FFFFFF" stroke="#7D8A8A" stroke-width="2" transform="rotate(-6 490 1254)"/>
  {stone_mortar(840, 1200, 0.42, p)}'''


def mortar_closeup(p, old=False, crack=False, color='#FFD36A'):
    hand = f'''
  <g id="{p}-el">
    {path('M 1250,1500 L 1010,1330', stroke=OUTLINE, sw=96)}{path('M 1250,1500 L 1010,1330', stroke='#F3F6F6', sw=88)}
    <rect x="985" y="1290" width="60" height="80" rx="10" fill="#3F7F7A" stroke="{OUTLINE}" stroke-width="3" transform="rotate(35 1015 1330)"/>
    {ell(930, 1270, 70, 48, '#F2C9A4', f'stroke="{OUTLINE}" stroke-width="4" transform="rotate(35 930 1270)"')}
    {path('M 880,1215 L 830,1180 M 868,1240 L 812,1215 M 870,1270 L 818,1262', stroke=OUTLINE, sw=30)}
    {path('M 880,1215 L 830,1180 M 868,1240 L 812,1215 M 870,1270 L 818,1262', stroke='#F2C9A4', sw=24)}
  </g>'''
    sparks = ''.join(f'<circle id="{p}-k{i}" cx="{400 + (i * 97) % 300}" cy="{1000 + (i * 53) % 160}" r="{4 + i % 4}" fill="#FFE9A8" opacity="0"/>' for i in range(12))
    return f'''
  <defs><radialGradient id="{p}-bg" cx=".5" cy=".55"><stop offset="0" stop-color="#3C4A4A"/><stop offset="1" stop-color="#101818"/></radialGradient></defs>
  {('<rect width="1080" height="1920" fill="#D9C29A"/>' + ''.join(jar(40 + i * 260, 420, 180, 300, c) for i, c in enumerate(['#D9822B', '#6F8F3E', '#E3C35A', '#7B4A2A']))
     + '<rect x="0" y="720" width="1080" height="34" fill="#7A5132"/><rect width="1080" height="1290" fill="#3A2416" opacity=".45"/>'
     + '<rect x="0" y="1270" width="1080" height="650" fill="#7A5132"/><rect x="0" y="1260" width="1080" height="30" fill="#8E623E"/>') if old else
    ('<rect width="1080" height="1920" fill="url(#' + p + '-bg)"/><rect x="0" y="1290" width="1080" height="630" fill="#E9EFEF"/><rect x="0" y="1270" width="1080" height="30" fill="#C9D3D3"/>')}
  {stone_mortar(540, 1170, 1.9, p, color=color)}
  {('<g id="' + p + '-catlak">' + path('M 568,1000 L 548,1070 L 584,1120 L 550,1190 L 590,1250 L 566,1320', stroke='#1A1210', sw=12)
     + path('M 584,1120 L 640,1150 M 550,1190 L 500,1215', stroke='#1A1210', sw=7) + '</g>') if crack else ''}
  {sparks}
  {hand}'''


def room_bg(p, time='night'):
    """Mehmet'in odası. time: 'night' (kandil ışığı) veya 'dawn' (şafak)."""
    sky = ('#1E2A4A', '#3A4A72') if time == 'night' else ('#F6C89A', '#BFDDEB')
    stars = ''.join(f'<circle cx="{770 + (i * 53) % 170}" cy="{470 + (i * 37) % 200}" r="3" fill="#FFF3C4"/>' for i in range(7)) if time == 'night' else ''
    return f'''
  <defs>
    <linearGradient id="{p}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky[0]}"/><stop offset="1" stop-color="{sky[1]}"/></linearGradient>
    <radialGradient id="{p}-lamp"><stop offset="0" stop-color="#FFD98A" stop-opacity=".85"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="1080" height="1920" fill="#DCC29A"/>
  <rect x="0" y="0" width="1080" height="150" fill="#5A3A24"/>
  {''.join(f'<rect x="{x}" y="140" width="58" height="46" fill="#4A2E1C" stroke="{OUTLINE}" stroke-width="3"/>' for x in range(80, 1080, 220))}
  {ell(300, 520, 120, 70, '#CDB18A', 'opacity=".6"')}
  <!-- pencere -->
  <rect x="740" y="430" width="230" height="300" rx="8" fill="#6B4528" stroke="{OUTLINE}" stroke-width="4"/>
  <rect x="760" y="450" width="190" height="260" fill="url(#{p}-sky)"/>{stars}
  {path('M 855,450 L 855,710 M 760,580 L 950,580', stroke='#6B4528', sw=10)}
  <!-- kandil nişi -->
  <path d="M 200,760 L 200,640 Q 200,580 260,576 Q 320,580 320,640 L 320,760 Z" fill="#B99A70" stroke="{OUTLINE}" stroke-width="3"/>
  <circle id="{p}-isik" cx="260" cy="700" r="230" fill="url(#{p}-lamp)" opacity="{.9 if time == 'night' else .3}"/>
  {path('M 230,740 Q 260,760 290,740 L 280,722 L 240,722 Z', fill='#A9553A', stroke=OUTLINE, sw=3)}
  <path id="{p}-alev" d="M 260,722 Q 248,700 260,680 Q 272,700 260,722 Z" fill="#FFB347" stroke="#E07B22" stroke-width="2"/>
  <!-- testi -->
  {path('M 120,1390 Q 90,1300 130,1260 L 126,1230 L 154,1230 L 150,1260 Q 190,1300 160,1390 Z', fill='#B5643A', stroke=OUTLINE, sw=3)}
  <rect x="0" y="1440" width="1080" height="480" fill="#8B5E3B"/>
  <rect x="0" y="1430" width="1080" height="22" fill="#6B4528"/>
  <!-- döşek ve yastık -->
  <rect x="390" y="1330" width="640" height="190" rx="30" fill="#E8DCC4" stroke="{OUTLINE}" stroke-width="4"/>
  <rect x="510" y="1255" width="260" height="95" rx="40" fill="#F4EFE4" stroke="{OUTLINE}" stroke-width="4"/>
  <rect x="0" y="1720" width="1080" height="200" fill="#A33A2E"/>
  {''.join(f'<polygon points="{x},1820 {x + 30},1790 {x + 60},1820 {x + 30},1850" fill="#E3B65A" stroke="{OUTLINE}" stroke-width="2"/>' for x in range(20, 1080, 90))}'''


def room_front(p, time='night'):
    """Yorgan (çocuğun üstüne çizilir) ve gece/şafak ışık katmanı."""
    patches = ''.join(f'<rect x="{x}" y="{y}" width="110" height="80" fill="{c}" opacity=".9"/>'
                      for (x, y), c in zip(((420, 1420), (560, 1450), (700, 1420), (840, 1450), (480, 1530), (760, 1540)),
                                           ('#C99A3A', '#3F7F7A', '#B2452E', '#C99A3A', '#B2452E', '#3F7F7A')))
    tint = 'rgba(30,40,90,.22)' if time == 'night' else 'rgba(255,190,120,.12)'
    return f'''
  <path d="M 380,1410 Q 640,1360 1050,1400 L 1060,1600 Q 640,1640 370,1600 Z" fill="#D9C7A4" stroke="{OUTLINE}" stroke-width="4"/>
  <clipPath id="{p}-yc"><path d="M 380,1410 Q 640,1360 1050,1400 L 1060,1600 Q 640,1640 370,1600 Z"/></clipPath>
  <g clip-path="url(#{p}-yc)">{patches}</g>
  <rect width="1080" height="1920" fill="{tint}"/>'''


def door_view(p, crowd=True):
    """Dükkânın kapısı içeriden; dışarıda sokak ve kuyruk."""
    people = ''
    if crowd:
        cols = ['#7A2E3A', '#3F7F7A', '#6E4B2F', '#2E3F5E', '#B2452E', '#717D3E', '#9A7AA8']
        for i in range(9):
            x = 300 + (i * 61) % 480
            y = 1140 + (i * 29) % 90
            sc = 0.75 + (i % 3) * 0.08
            c = cols[i % len(cols)]
            people += (f'<g transform="translate({x},{y}) scale({sc})">'
                       f'{path("M -40,0 L -50,170 L 50,170 L 40,0 Q 0,-14 -40,0 Z", fill=c, stroke=OUTLINE, sw=3)}'
                       f'{ell(0, -40, 30, 36, "#DDA57C", f"stroke=\"{OUTLINE}\" stroke-width=\"3\"")}'
                       f'{path("M -32,-52 Q 0,-96 32,-52 Q 0,-66 -32,-52 Z", fill="#F2ECDD" if i % 2 else "#4A2C1D", stroke=OUTLINE, sw=2.5)}</g>')
    return f'''
  <rect width="1080" height="1920" fill="#E6D2AE"/>
  <rect x="0" y="0" width="1080" height="150" fill="#5A3A24"/>
  <!-- kapı boşluğu ve sokak -->
  <path d="M 230,1460 L 230,620 Q 230,420 540,410 Q 850,420 850,620 L 850,1460 Z" fill="#BFDDEB"/>
  <path d="M 230,1000 L 850,1000 L 850,1460 L 230,1460 Z" fill="#D9C7A4"/>
  {''.join(f'<rect x="{x}" y="{780 + (x * 7) % 90}" width="110" height="{260 - (x * 7) % 90}" fill="#EADBC0" stroke="#B9A889" stroke-width="2"/><polygon points="{x - 8},{780 + (x * 7) % 90} {x + 55},{740 + (x * 7) % 90} {x + 118},{780 + (x * 7) % 90}" fill="#A9553A"/>' for x in range(240, 840, 130))}
  {people}
  <!-- kapı kanatları ve çerçeve -->
  <path fill="#6B4528" fill-rule="evenodd" stroke="{OUTLINE}" stroke-width="5"
        d="M 180,1470 L 180,610 Q 180,370 540,360 Q 900,370 900,610 L 900,1470 Z M 230,1460 L 230,620 Q 230,420 540,410 Q 850,420 850,620 L 850,1460 Z"/>
  <path d="M 230,1460 L 230,620 L 120,660 L 120,1500 Z" fill="#7A5132" stroke="{OUTLINE}" stroke-width="4"/>
  <path d="M 850,1460 L 850,620 L 960,660 L 960,1500 Z" fill="#7A5132" stroke="{OUTLINE}" stroke-width="4"/>
  <rect x="0" y="1460" width="1080" height="460" fill="#8B5E3B"/>
  <rect x="0" y="1450" width="1080" height="24" fill="#6B4528"/>'''


def bowl_closeup(p):
    """Su dolu bakır tas; yüzeyde modern Elif'in yansıması."""
    face = ayse(f'{p}-yan', brow='surprised', mouth='o', modern=True)
    rings = ''.join(f'<ellipse id="{p}-hal{i}" cx="540" cy="960" rx="{60 + i * 90}" ry="{60 + i * 90}" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0"/>' for i in range(4))
    return f'''
  <rect width="1080" height="1920" fill="#5A3A24"/>
  {''.join(f'<rect x="0" y="{y}" width="1080" height="10" fill="#4E321F"/>' for y in range(0, 1920, 90))}
  <circle cx="540" cy="960" r="470" fill="#B8733A" stroke="{OUTLINE}" stroke-width="6"/>
  <circle cx="540" cy="960" r="430" fill="#9A5A2A"/>
  <clipPath id="{p}-su"><circle cx="540" cy="960" r="420"/></clipPath>
  <g clip-path="url(#{p}-su)">
    <rect x="100" y="520" width="880" height="880" fill="#5F8FA6"/>
    <g id="{p}-yansima" opacity=".75" transform="translate(540,1290) scale(1.75)">{face}</g>
    <rect x="100" y="520" width="880" height="880" fill="#6FA3B8" opacity=".35"/>
    {rings}
    {ell(400, 760, 120, 40, '#FFFFFF', 'opacity=".25" transform="rotate(-30 400 760)"')}
  </g>'''


def court_bg(p):
    """Kadı'nın divanhanesi: kemerler, çini, yüksek sedir, halı."""
    arches = ''
    for x in (90, 390, 690):
        arches += (f'<path d="M {x},1150 L {x},620 Q {x},470 {x + 150},450 Q {x + 300},470 {x + 300},620 L {x + 300},1150 Z" fill="#2F5A7A" stroke="{OUTLINE}" stroke-width="4"/>'
                   f'<path d="M {x + 30},1150 L {x + 30},640 Q {x + 30},510 {x + 150},494 Q {x + 270},510 {x + 270},640 L {x + 270},1150 Z" fill="#E9E3D2"/>'
                   + ''.join(f'<circle cx="{x + 60 + (i % 4) * 60}" cy="{700 + (i // 4) * 110}" r="16" fill="#3F7FA8" opacity=".55"/>' for i in range(16)))
    lamps = ''.join(f'{path(f"M {x},150 L {x},330", stroke="#8E6A2A", sw=3)}<path d="M {x - 30},330 L {x + 30},330 L {x + 18},380 L {x - 18},380 Z" fill="#C9A55A" stroke="{OUTLINE}" stroke-width="3"/>'
                    f'<circle cx="{x}" cy="395" r="40" fill="#FFE3A0" opacity=".35"/>' for x in (240, 540, 840))
    return f'''
  <rect width="1080" height="1920" fill="#E8DCC0"/>
  <rect x="0" y="0" width="1080" height="150" fill="#5A3A24"/>
  {lamps}{arches}
  <rect x="0" y="1150" width="1080" height="70" fill="#C9B48A" stroke="{OUTLINE}" stroke-width="3"/>
  <rect x="0" y="1220" width="1080" height="700" fill="#8B5E3B"/>
  <rect x="80" y="1300" width="920" height="560" fill="#8C2E26" stroke="{OUTLINE}" stroke-width="4"/>
  <rect x="120" y="1340" width="840" height="480" fill="none" stroke="#E3B65A" stroke-width="8"/>
  {''.join(f'<polygon points="{x},1580 {x + 40},1540 {x + 80},1580 {x + 40},1620" fill="#E3B65A" stroke="{OUTLINE}" stroke-width="2"/>' for x in range(200, 880, 120))}'''


def port_bg(p):
    """Liman: deniz, gemi, iskele, fıçılar."""
    return f'''
  <defs><linearGradient id="{p}-sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9CCBE0"/><stop offset="1" stop-color="#EBE2CC"/></linearGradient></defs>
  <rect width="1080" height="1920" fill="url(#{p}-sk)"/>
  <circle cx="200" cy="360" r="55" fill="#FFF3C4"/>
  <path d="M 0,900 Q 300,860 560,890 Q 800,850 1080,880 L 1080,960 L 0,960 Z" fill="#A9B7A0"/>
  <rect x="820" y="700" width="70" height="200" fill="#D9CDB5" stroke="#B3A685" stroke-width="3"/>
  <path d="M 810,700 L 855,610 L 900,700 Z" fill="#8E5A3A"/>
  <rect x="0" y="950" width="1080" height="420" fill="#5F93AC"/>
  {''.join(f'<rect x="{x}" y="{y}" width="{w}" height="5" fill="#fff" opacity=".45"/>' for x, y, w in ((80, 1010, 120), (420, 1060, 160), (760, 1000, 90), (300, 1150, 140)))}
  <!-- gemi -->
  <g id="{p}-gemi">
    <path d="M 380,1120 L 1000,1120 L 940,1260 L 440,1260 Z" fill="#6B4528" stroke="{OUTLINE}" stroke-width="4"/>
    {path('M 400,1150 L 980,1150 M 420,1200 L 960,1200', stroke='#5A3A24', sw=5)}
    {path('M 560,1120 L 560,520 M 800,1120 L 800,580', stroke='#5A3A24', sw=12)}
    <path d="M 500,600 Q 560,640 620,600 L 620,860 Q 560,900 500,860 Z" fill="#F4EBD8" stroke="{OUTLINE}" stroke-width="3"/>
    <path d="M 745,650 Q 800,690 855,650 L 855,880 Q 800,915 745,880 Z" fill="#F4EBD8" stroke="{OUTLINE}" stroke-width="3"/>
    <path d="M 560,520 L 640,545 L 560,570 Z" fill="#B2452E"/>
  </g>
  {''.join(f'<path id="{p}-marti{i}" d="M {x},{y} q 14,-12 28,0 q 14,-12 28,0" stroke="#4A3A30" stroke-width="4" fill="none"/>' for i, (x, y) in enumerate(((180, 560), (260, 520), (980, 470))))}
  <!-- iskele -->
  <rect x="0" y="1340" width="1080" height="580" fill="#8B5E3B"/>
  {''.join(f'<rect x="0" y="{y}" width="1080" height="10" fill="#6B4528"/>' for y in range(1380, 1920, 80))}
  {''.join(f'<rect x="{x}" y="1300" width="40" height="120" fill="#5A3A24" stroke="{OUTLINE}" stroke-width="3"/>' for x in (60, 980))}
  <!-- fıçılar, sandıklar -->
  {''.join(f'<ellipse cx="{x}" cy="1440" rx="60" ry="80" fill="#9E6B3F" stroke="{OUTLINE}" stroke-width="4"/>{path(f"M {x - 58},1410 L {x + 58},1410 M {x - 58},1470 L {x + 58},1470", stroke="#5A3A24", sw=6)}' for x in (90, 210))}
  <rect x="860" y="1360" width="170" height="140" fill="#B08A5A" stroke="{OUTLINE}" stroke-width="4"/>
  {path('M 860,1360 L 1030,1500 M 1030,1360 L 860,1500', stroke='#8E6A3A', sw=6)}'''


def street_bg(p, fountain=True, broken=False):
    """Çeşmeli Osmanlı sokağı: cumbalı evler, Arnavut kaldırımı."""
    houses = ''
    for i, x in enumerate((-40, 300, 640, 900)):
        c = ['#E9D9BC', '#E3C9A8', '#EADBC0', '#DCC7A6'][i]
        houses += (f'<rect x="{x}" y="420" width="300" height="760" fill="{c}" stroke="{OUTLINE}" stroke-width="4"/>'
                   f'<rect x="{x - 20}" y="420" width="340" height="230" fill="{c}" stroke="{OUTLINE}" stroke-width="4"/>'
                   f'<polygon points="{x - 40},420 {x + 150},300 {x + 340},420" fill="#A9553A" stroke="{OUTLINE}" stroke-width="4"/>'
                   + ''.join(f'<rect x="{x + 30 + k * 90}" y="470" width="60" height="120" fill="#6B4528" stroke="{OUTLINE}" stroke-width="3"/>' for k in range(3))
                   + f'<rect x="{x + 110}" y="980" width="80" height="200" fill="#5A3A24" stroke="{OUTLINE}" stroke-width="3"/>')
    stones = ''.join(f'<ellipse cx="{(i * 97) % 1100}" cy="{1220 + (i * 53) % 690}" rx="44" ry="24" fill="#9E9384" stroke="#7E7466" stroke-width="2"/>' for i in range(60))
    crack = path('M 490,1010 l 18,40 l -14,30 l 20,36 M 600,1030 l -12,30 l 16,28', stroke='#3A2A20', sw=5) if broken else ''
    fnt = f'''
  <path d="M 380,1200 L 380,900 Q 380,800 540,790 Q 700,800 700,900 L 700,1200 Z" fill="#D9CDB5" stroke="{OUTLINE}" stroke-width="5"/>
  <path d="M 420,1200 L 420,920 Q 420,850 540,842 Q 660,850 660,920 L 660,1200 Z" fill="#C2B497"/>
  <rect x="510" y="1010" width="60" height="22" fill="#B08A3C" stroke="{OUTLINE}" stroke-width="3"/>
  <path id="{p}-su" d="M 540,1032 L 540,1150" stroke="#8FC9E6" stroke-width="10" stroke-linecap="round"/>
  <rect x="400" y="1150" width="280" height="60" fill="#B9AC90" stroke="{OUTLINE}" stroke-width="4"/>
  {crack}''' if fountain else ''
    return f'''
  <rect width="1080" height="1920" fill="#BFDDEB"/>
  {houses}
  <rect x="0" y="1180" width="1080" height="740" fill="#B8AD9C"/>
  {stones}
  {fnt}'''
