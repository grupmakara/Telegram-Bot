import React from 'react';
import type { Look } from './characters';
import type { Ifade } from '../story/registry';

export const INK = '#2b1d14';
const S = { stroke: INK, strokeWidth: 5, strokeLinejoin: 'round' as const, strokeLinecap: 'round' as const };

const EYE_Y = 200;
const EYES = [162, 238];

/** Kaşlar: [iç y, dış y] her göz için (sol, sağ). */
const BROWS: Record<Ifade, [[number, number], [number, number]]> = {
  normal: [[158, 152], [158, 152]],
  ofkeli: [[170, 146], [170, 146]],
  uzgun: [[144, 160], [144, 160]],
  saskin: [[136, 138], [136, 138]],
  gulumseyen: [[150, 148], [150, 148]],
  sinsi: [[164, 150], [140, 136]],
};

const MOUTH_CLOSED: Record<Ifade, string> = {
  normal: 'M180,272 Q200,278 220,272',
  gulumseyen: 'M174,266 Q200,292 226,266',
  ofkeli: 'M178,280 Q200,266 222,280',
  uzgun: 'M180,282 Q200,270 220,282',
  saskin: '',
  sinsi: 'M180,274 Q206,282 226,262',
};

export const BackHair: React.FC<{ look: Look }> = ({ look }) => {
  if (look.hair === 'braid') {
    const beads = Array.from({ length: 9 }, (_, i) => i);
    return (
      <g>
        <path d="M88,200 Q80,60 200,62 Q320,60 312,200 L318,330 Q200,360 82,330 Z" fill={look.hairColor} {...S} />
        {beads.map((i) => (
          <ellipse key={i} cx={292 - i * 2} cy={360 + i * 34} rx={22 - i * 0.8} ry={20} fill={look.hairColor} {...S} />
        ))}
      </g>
    );
  }
  if (look.headwear === 'basortu') {
    return <path d="M70,210 Q60,40 200,40 Q340,40 330,210 L360,420 Q200,470 40,420 Z" fill={look.headwearColor} {...S} />;
  }
  return null;
};

export const Face: React.FC<{ look: Look; ifade: Ifade; mouthOpen: number; blink: boolean; look_dx: number; all?: boolean }> = ({ look, ifade, mouthOpen, blink, look_dx, all }) => {
  const brows = BROWS[ifade];
  const lidCover = ifade === 'sinsi' ? 0.45 : ifade === 'ofkeli' ? 0.3 : 0;
  const renderEyes = (blink: boolean) =>
    EYES.map((x, i) => {
          if (look.eyepatch && i === 1) return null;
          if (blink) return <path key={x} d={`M${x - 20},${EYE_Y + 2} Q${x},${EYE_Y + 12} ${x + 20},${EYE_Y + 2}`} fill="none" {...S} />;
          return (
            <g key={x}>
              <ellipse cx={x} cy={EYE_Y} rx={20} ry={24} fill="#fff" {...S} />
              <circle cx={x + look_dx} cy={EYE_Y + 3} r={10} fill="#3b2516" />
              <circle cx={x + look_dx + 3} cy={EYE_Y - 1} r={3} fill="#fff" />
              {lidCover > 0 && (
                <path d={`M${x - 22},${EYE_Y - 24 + 48 * lidCover} L${x - 22},${EYE_Y - 30} L${x + 22},${EYE_Y - 30} L${x + 22},${EYE_Y - 24 + 48 * lidCover} Z`} fill={look.skin} stroke="none" />
              )}
              {lidCover > 0 && <line x1={x - 20} x2={x + 20} y1={EYE_Y - 24 + 48 * lidCover} y2={EYE_Y - 24 + 48 * lidCover} {...S} />}
              {look.female && <path d={`M${x + (i ? 16 : -16)},${EYE_Y - 18} l${i ? 8 : -8},-8`} {...S} />}
            </g>
          );
        });
  const renderMouth = (mouthOpen: number) =>
    mouthOpen > 0.05 ? (
          <ellipse cx={200} cy={278} rx={17} ry={4 + mouthOpen * 13} fill="#5a1e1e" {...S} strokeWidth={4} />
        ) : ifade === 'saskin' ? (
          <ellipse cx={200} cy={280} rx={9} ry={11} fill="#5a1e1e" {...S} strokeWidth={4} />
        ) : (
          <path d={MOUTH_CLOSED[ifade]} fill="none" stroke={look.female ? '#b8433f' : INK} strokeWidth={look.female ? 7 : 5} strokeLinecap="round" />
        );
  return (
    <g>
      {/* kulaklar */}
      {look.headwear !== 'basortu' && (
        <>
          <ellipse cx={100} cy={210} rx={16} ry={26} fill={look.skin} {...S} />
          <ellipse cx={300} cy={210} rx={16} ry={26} fill={look.skin} {...S} />
        </>
      )}
      <ellipse cx={200} cy={200} rx={100} ry={115} fill={look.skin} {...S} />
      {look.hair === 'short' && look.headwear === 'none' && (
        <path d="M98,200 Q92,78 200,76 Q308,78 302,200 Q290,128 200,122 Q110,128 98,200 Z" fill={look.hairColor} {...S} />
      )}
      {look.hair === 'braid' && <path d="M100,190 Q105,82 200,80 Q295,82 300,190 Q270,120 200,118 Q160,118 130,150 Q112,168 100,190 Z" fill={look.hairColor} {...S} />}
      {look.old && (
        <g fill="none" stroke={INK} strokeWidth={3} opacity={0.55}>
          <path d="M122,196 l-10,6 M122,206 l-12,2" />
          <path d="M278,196 l10,6 M278,206 l12,2" />
          <path d="M150,244 Q140,262 150,280 M250,244 Q260,262 250,280" />
        </g>
      )}
      {look.female && (
        <>
          <circle cx={138} cy={246} r={17} fill="#f29a9a" opacity={0.55} />
          <circle cx={262} cy={246} r={17} fill="#f29a9a" opacity={0.55} />
        </>
      )}
      {/* sakal */}
      {look.beard === 'short' && <path d="M104,212 Q108,336 200,350 Q292,336 296,212 Q280,300 200,302 Q120,300 104,212 Z" fill={look.beardColor} {...S} />}
      {look.beard === 'full' && <path d="M100,205 Q92,392 200,420 Q308,392 300,205 Q284,304 200,306 Q116,304 100,205 Z" fill={look.beardColor} {...S} />}
      {/* gözler */}
      {all ? (
        <>
          <g className="eo">{renderEyes(false)}</g>
          <g className="ec" opacity={0}>{renderEyes(true)}</g>
        </>
      ) : (
        renderEyes(blink)
      )}
      {look.eyepatch && (
        <g>
          <path d="M214,178 L98,150 M262,182 L302,166" stroke={INK} strokeWidth={5} />
          <ellipse cx={238} cy={200} rx={27} ry={25} fill="#1b1512" {...S} />
        </g>
      )}
      {look.glasses && (
        <g fill="none" stroke="#7a5a2a" strokeWidth={5}>
          <circle cx={162} cy={EYE_Y} r={30} />
          <circle cx={238} cy={EYE_Y} r={30} />
          <path d="M192,198 Q200,190 208,198" />
        </g>
      )}
      {/* kaşlar */}
      {brows.map(([inner, outer], i) => {
        const x = EYES[i];
        const dir = i === 0 ? -1 : 1;
        return <line key={i} x1={x - dir * 6} y1={inner} x2={x + dir * 24} y2={outer} stroke={look.browColor} strokeWidth={look.browWidth} strokeLinecap="round" />;
      })}
      {ifade === 'uzgun' && (
        <g fill="#7cc8f2" stroke="#3d8fc0" strokeWidth={3}>
          <path d="M150,226 Q144,252 150,262 Q158,252 150,226 Z" />
          <path d="M250,226 Q244,252 250,262 Q258,252 250,226 Z" />
        </g>
      )}
      {look.scar && (
        <g stroke="#8f3b2e" strokeWidth={5} strokeLinecap="round">
          <line x1={124} y1={182} x2={150} y2={248} />
          <line x1={128} y1={206} x2={142} y2={200} />
          <line x1={136} y1={226} x2={150} y2={220} />
        </g>
      )}
      {/* burun */}
      <path d="M202,214 Q190,240 204,246" fill="none" {...S} strokeWidth={4} />
      {/* bıyık */}
      {look.mustache && (
        <path d="M200,252 Q170,244 150,268 Q176,262 200,262 Q224,262 250,268 Q230,244 200,252 Z" fill={look.beard === 'none' ? look.hairColor : look.beardColor} {...S} strokeWidth={4} />
      )}
      {/* ağız */}
      {all ? (
        <>
          <g className="mc">{renderMouth(0)}</g>
          <g className="mo" opacity={0}>{renderMouth(0.8)}</g>
        </>
      ) : (
        renderMouth(mouthOpen)
      )}
    </g>
  );
};

export const Headwear: React.FC<{ look: Look }> = ({ look }) => {
  const c = look.headwearColor;
  switch (look.headwear) {
    case 'sarik':
    case 'sarik_sorguc':
      return (
        <g>
          <ellipse cx={200} cy={92} rx={122} ry={62} fill={c} {...S} />
          <path d="M92,104 Q200,60 308,104 M98,122 Q200,84 302,122 M110,80 Q200,44 292,80" fill="none" stroke="#cfc8b8" strokeWidth={4} />
          {look.headwear === 'sarik_sorguc' && (
            <g>
              <path d="M200,70 Q186,10 212,-30 Q218,20 206,70 Z" fill="#f3efe4" {...S} strokeWidth={4} />
              <circle cx={202} cy={80} r={16} fill="#c0283a" stroke="#e2b84a" strokeWidth={6} />
            </g>
          )}
        </g>
      );
    case 'kavuk_tall':
      return (
        <g>
          <path d="M126,112 L104,-56 Q200,-118 296,-56 L274,112 Z" fill={c} {...S} />
          <path d="M112,6 L290,-40" stroke="#d4a73c" strokeWidth={16} />
          <ellipse cx={200} cy={118} rx={118} ry={40} fill={c} {...S} />
          <path d="M90,118 Q200,90 310,118" fill="none" stroke="#cfc8b8" strokeWidth={4} />
        </g>
      );
    case 'kavuk_big':
      return (
        <g>
          <ellipse cx={200} cy={58} rx={140} ry={96} fill={c} {...S} />
          <path d="M70,70 Q200,20 330,70 M66,100 Q200,52 334,100" fill="none" stroke="#cfc8b8" strokeWidth={4} />
          <ellipse cx={200} cy={130} rx={110} ry={26} fill={look.coat} {...S} />
        </g>
      );
    case 'katip':
      return (
        <g>
          <rect x={136} y={-10} width={128} height={140} rx={16} fill="#7a5034" {...S} />
          <ellipse cx={200} cy={124} rx={116} ry={34} fill={c} {...S} />
        </g>
      );
    case 'hotoz':
      return (
        <g fill={c} {...S} strokeWidth={4}>
          <path d="M150,96 L160,58 L178,88 L200,48 L222,88 L240,58 L250,96 Z" />
          <circle cx={200} cy={78} r={7} fill="#c0283a" />
        </g>
      );
    case 'basortu':
      return <path d="M96,206 Q92,70 200,70 Q308,70 304,206 Q298,108 200,104 Q102,108 96,206 Z" fill={c} {...S} />;
    case 'kece':
      return (
        <g>
          <path d="M100,130 Q104,30 200,28 Q296,30 300,130 Z" fill={c} {...S} />
          <rect x={96} y={118} width={208} height={24} rx={10} fill="#efe4cc" {...S} />
        </g>
      );
    default:
      return null;
  }
};

/** Gövde: kaftan / entari / yelek. */
export const Body: React.FC<{ look: Look }> = ({ look }) => {
  const slim = look.female ? 18 : 0;
  const legs = (
    <g>
      <rect x={150} y={820} width={44} height={140} rx={16} fill={look.pants} {...S} />
      <rect x={206} y={820} width={44} height={140} rx={16} fill={look.pants} {...S} />
      <ellipse cx={164} cy={968} rx={40} ry={18} fill={look.shoes} {...S} />
      <ellipse cx={236} cy={968} rx={40} ry={18} fill={look.shoes} {...S} />
    </g>
  );
  if (look.outfit === 'vest') {
    return (
      <g>
        <path d="M150,760 Q140,900 160,950 L196,950 L200,780 L204,950 L240,950 Q260,900 250,760 Z" fill={look.pants} {...S} />
        <ellipse cx={170} cy={966} rx={40} ry={18} fill={look.shoes} {...S} />
        <ellipse cx={230} cy={966} rx={40} ry={18} fill={look.shoes} {...S} />
        <rect x={182} y={300} width={36} height={50} fill={look.skin} {...S} />
        <path d="M122,348 Q200,326 278,348 L292,790 Q200,810 108,790 Z" fill={look.shirt} {...S} />
        <path d="M122,348 Q160,334 180,340 L190,600 L114,600 Z" fill={look.coat} {...S} />
        <path d="M278,348 Q240,334 220,340 L210,600 L286,600 Z" fill={look.coat} {...S} />
        <path d="M114,600 L190,600 M210,600 L286,600" stroke={look.trim} strokeWidth={8} />
        <path d="M110,610 Q200,630 290,610 L292,666 Q200,684 108,666 Z" fill={look.belt} {...S} />
        {look.dagger && (
          <g>
            <path d="M232,620 L250,620 L246,700 Q241,730 236,700 Z" fill="#cfd3d8" {...S} strokeWidth={4} />
            <rect x={226} y={600} width={30} height={26} rx={6} fill="#d9b25c" {...S} strokeWidth={4} />
          </g>
        )}
      </g>
    );
  }
  return (
    <g>
      {legs}
      <rect x={182} y={300} width={36} height={50} fill={look.skin} {...S} />
      <path d={`M${122 + slim},348 Q200,326 ${278 - slim},348 L${318 - slim},900 Q200,928 ${82 + slim},900 Z`} fill={look.coat} {...S} />
      <path d="M170,340 L200,450 L230,340 Z" fill={look.shirt} {...S} />
      {look.outfit === 'kaftan' && (
        <g>
          <path d="M200,450 L200,912" stroke={look.shirt} strokeWidth={30} />
          <path d="M184,450 L180,910 M216,450 L220,910" stroke={look.trim} strokeWidth={10} />
        </g>
      )}
      {look.outfit === 'entari' && <path d={`M${92 + slim},880 Q200,900 ${308 - slim},880`} fill="none" stroke={look.trim} strokeWidth={10} />}
      {look.fur && (
        <g fill="#3a2a1e" {...S}>
          <path d="M120,350 Q200,320 280,350 Q262,400 238,410 L216,346 L184,346 L162,410 Q138,400 120,350 Z" />
          <path d="M162,410 L150,912 L184,912 L190,450 Z" />
          <path d="M238,410 L250,912 L216,912 L210,450 Z" />
        </g>
      )}
      <path d={`M${108 + slim / 2},560 Q200,582 ${292 - slim / 2},560 L${294 - slim / 2},606 Q200,628 ${106 + slim / 2},606 Z`} fill={look.belt} {...S} />
      {look.outfit === 'kaftan' && <circle cx={200} cy={594} r={14} fill={look.trim} {...S} strokeWidth={4} />}
    </g>
  );
};

/** Kol: omuzdan aşağı; açı (derece) dışa doğru pozitif. Sol kol koordinatlarında çizilir. */
export const Arm: React.FC<{ look: Look; upper: number; lower: number }> = ({ look, upper, lower }) => {
  const sleeve = look.outfit === 'vest' ? look.shirt : look.coat;
  return (
    <g transform={`rotate(${upper})`}>
      <line x1={0} y1={0} x2={0} y2={170} stroke={INK} strokeWidth={56} strokeLinecap="round" />
      <line x1={0} y1={0} x2={0} y2={170} stroke={sleeve} strokeWidth={46} strokeLinecap="round" />
      <g transform={`translate(0,170) rotate(${lower})`}>
        <line x1={0} y1={0} x2={0} y2={140} stroke={INK} strokeWidth={50} strokeLinecap="round" />
        <line x1={0} y1={0} x2={0} y2={140} stroke={sleeve} strokeWidth={40} strokeLinecap="round" />
        <line x1={-20} y1={132} x2={20} y2={132} stroke={look.trim} strokeWidth={10} />
        <circle cx={0} cy={166} r={24} fill={look.skin} stroke={INK} strokeWidth={5} />
      </g>
    </g>
  );
};
