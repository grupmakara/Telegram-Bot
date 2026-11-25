import React from 'react';
import type { MekanId } from '../story/registry';

const INK = '#2b1d14';
const W = 1080;
const H = 1920;
export const FLOOR_Y = 1880;

const range = (n: number) => Array.from({ length: n }, (_, i) => i);

const Arch: React.FC<{ x: number; y: number; w: number; h: number; fill: string; stroke?: string }> = ({ x, y, w, h, fill, stroke = INK }) => (
  <path d={`M${x},${y + h} L${x},${y + w * 0.5} Q${x},${y} ${x + w / 2},${y - w * 0.25} Q${x + w},${y} ${x + w},${y + w * 0.5} L${x + w},${y + h} Z`} fill={fill} stroke={stroke} strokeWidth={6} />
);

const Tulip: React.FC<{ x: number; y: number; s?: number; c: string }> = ({ x, y, s = 1, c }) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <path d="M0,0 L0,70" stroke="#3f7a3a" strokeWidth={6} />
    <path d="M0,50 Q-26,30 -22,6 Q-6,26 0,44" fill="#4f8f45" />
    <path d="M-18,-30 Q-20,6 0,8 Q20,6 18,-30 L9,-14 L0,-34 L-9,-14 Z" fill={c} stroke={INK} strokeWidth={4} />
  </g>
);

const Divan = () => (
  <g>
    <rect width={W} height={H} fill="#7a1f24" />
    <rect y={0} width={W} height={160} fill="#5a141a" />
    {range(3).map((i) => <Arch key={i} x={70 + i * 330} y={420} w={280} h={820} fill="#4a1016" stroke="#d4a73c" />)}
    {range(3).map((i) => <Arch key={i} x={110 + i * 330} y={500} w={200} h={600} fill="#a8c4d6" stroke="#d4a73c" />)}
    <rect y={1160} width={W} height={90} fill="#1f5f8a" />
    {range(14).map((i) => <circle key={i} cx={40 + i * 78} cy={1205} r={22} fill="#e9e2cf" stroke="#d4a73c" strokeWidth={4} />)}
    <rect y={1250} width={W} height={200} fill="#8c2a2a" stroke={INK} strokeWidth={6} />
    {range(8).map((i) => <rect key={i} x={20 + i * 135} y={1270} width={110} height={110} rx={20} fill="#c9a55a" stroke={INK} strokeWidth={5} />)}
    <rect y={1450} width={W} height={H - 1450} fill="#a3322f" />
    <rect x={80} y={1520} width={920} height={360} fill="none" stroke="#d4a73c" strokeWidth={10} />
    {range(5).map((i) => <path key={i} d={`M${180 + i * 180},1640 l40,-50 l40,50 l-40,50 Z`} fill="#d4a73c" opacity={0.8} />)}
    <path d="M540,0 L540,250" stroke="#d4a73c" strokeWidth={6} />
    <path d="M480,250 L600,250 L570,330 L510,330 Z" fill="#d4a73c" stroke={INK} strokeWidth={5} />
  </g>
);

const KonakSalon: React.FC<{ gece?: boolean }> = ({ gece }) => (
  <g>
    <rect width={W} height={H} fill="#d9b98c" />
    {range(9).map((i) => <rect key={i} x={i * 120} y={0} width={120} height={1300} fill={i % 2 ? '#cfae80' : '#d9b98c'} />)}
    <rect y={1100} width={W} height={200} fill="#8a5a33" stroke={INK} strokeWidth={6} />
    <rect x={300} y={300} width={480} height={640} rx={18} fill={gece ? '#1d2747' : '#bfe0f2'} stroke={INK} strokeWidth={8} />
    {gece && <circle cx={650} cy={430} r={60} fill="#f3edd0" />}
    {range(7).map((i) => <line key={'v' + i} x1={300 + (i + 1) * 60} y1={300} x2={300 + (i + 1) * 60} y2={940} stroke="#6b4223" strokeWidth={10} />)}
    {range(10).map((i) => <line key={'h' + i} x1={300} y1={300 + (i + 1) * 58} x2={780} y2={300 + (i + 1) * 58} stroke="#6b4223" strokeWidth={10} />)}
    <rect x={280} y={940} width={520} height={30} fill="#6b4223" stroke={INK} strokeWidth={6} />
    <rect y={1300} width={W} height={180} fill="#7a1f2b" stroke={INK} strokeWidth={6} />
    {range(6).map((i) => <rect key={i} x={30 + i * 175} y={1225} width={150} height={110} rx={26} fill={i % 2 ? '#d4a73c' : '#2e5e9e'} stroke={INK} strokeWidth={5} />)}
    <rect y={1480} width={W} height={H - 1480} fill="#7b4b2a" />
    <ellipse cx={540} cy={1760} rx={500} ry={130} fill="#9e2f2a" stroke="#d4a73c" strokeWidth={8} />
    <ellipse cx={540} cy={1760} rx={380} ry={90} fill="none" stroke="#d4a73c" strokeWidth={5} />
    <path d="M60,0 L60,120 M1020,0 L1020,120" stroke="#5a3a1e" strokeWidth={5} />
    <path d="M30,120 L90,120 L78,190 L42,190 Z M990,120 L1050,120 L1038,190 L1002,190 Z" fill="#d4a73c" stroke={INK} strokeWidth={4} />
  </g>
);

const LaleBahcesi = () => (
  <g>
    <defs>
      <linearGradient id="skyL" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#8ec9ef" /><stop offset="1" stopColor="#f6e7c8" /></linearGradient>
    </defs>
    <rect width={W} height={H} fill="url(#skyL)" />
    <circle cx={850} cy={300} r={90} fill="#fff3c4" />
    <rect y={1000} width={W} height={H - 1000} fill="#8cbf6a" />
    {range(6).map((i) => <path key={i} d={`M${60 + i * 190},1010 Q${40 + i * 190},780 ${60 + i * 190},560 Q${80 + i * 190},780 ${60 + i * 190},1010 Z`} fill="#2f5f3a" stroke={INK} strokeWidth={5} />)}
    <g>
      <rect x={380} y={720} width={320} height={300} fill="#f2ead8" stroke={INK} strokeWidth={6} />
      <path d="M350,720 Q540,560 730,720 Z" fill="#b5523b" stroke={INK} strokeWidth={6} />
      <Arch x={480} y={830} w={120} h={190} fill="#6b4223" />
    </g>
    <path d="M0,1250 Q540,1180 1080,1250 L1080,1920 L0,1920 Z" fill="#7fb35d" />
    <path d="M420,1920 L480,1250 L600,1250 L660,1920 Z" fill="#e3d2a8" />
    {range(9).map((i) => <Tulip key={'a' + i} x={30 + i * 45} y={1290 + (i % 2) * 30} s={0.9} c={i % 3 ? '#d8343c' : '#f2c230'} />)}
    {range(9).map((i) => <Tulip key={'b' + i} x={690 + i * 45} y={1290 + (i % 2) * 30} s={0.9} c={i % 3 ? '#c0283a' : '#f29b2f'} />)}
    {range(6).map((i) => <Tulip key={'c' + i} x={20 + i * 70} y={1800 + (i % 2) * 20} s={1.6} c={i % 2 ? '#d8343c' : '#f2c230'} />)}
    {range(6).map((i) => <Tulip key={'d' + i} x={720 + i * 70} y={1800 + (i % 2) * 20} s={1.6} c={i % 2 ? '#b62a5a' : '#d8343c'} />)}
  </g>
);

const HalicLiman: React.FC<{ gece?: boolean }> = ({ gece }) => (
  <g>
    <defs>
      <linearGradient id="skyH" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor={gece ? '#0f1a38' : '#f2b880'} /><stop offset="1" stopColor={gece ? '#2c3a66' : '#f8dcb0'} />
      </linearGradient>
    </defs>
    <rect width={W} height={H} fill="url(#skyH)" />
    {gece ? <circle cx={820} cy={260} r={70} fill="#f3edd0" /> : <circle cx={540} cy={820} r={130} fill="#f7d27a" opacity={0.9} />}
    <g fill={gece ? '#1a2240' : '#7a5a6e'}>
      <rect x={0} y={860} width={W} height={120} />
      <path d="M180,860 Q260,740 340,860 Z M600,860 Q700,700 800,860 Z M420,860 Q470,790 520,860 Z" />
      {[150, 370, 560, 840, 920].map((x) => <path key={x} d={`M${x},860 L${x},640 L${x + 8},610 L${x + 16},640 L${x + 16},860 Z`} />)}
    </g>
    <rect y={980} width={W} height={500} fill={gece ? '#1d2f57' : '#4f8fb5'} />
    {range(10).map((i) => <path key={i} d={`M${(i * 137) % 1000},${1020 + i * 40} q30,-14 60,0`} stroke="#d9eef7" strokeWidth={5} fill="none" opacity={0.6} />)}
    <g transform="translate(640,860)">
      <path d="M0,240 L420,240 L370,330 L40,330 Z" fill="#6b4223" stroke={INK} strokeWidth={6} />
      <path d="M200,240 L200,-60 M330,240 L330,10" stroke="#4a2e18" strokeWidth={12} />
      <path d="M210,-50 Q300,60 210,200 Z" fill="#f2ead8" stroke={INK} strokeWidth={5} />
      <path d="M340,20 Q410,100 340,210 Z" fill="#f2ead8" stroke={INK} strokeWidth={5} />
      <path d="M200,-60 l50,14 l-50,14 Z" fill="#c0283a" />
    </g>
    <rect y={1480} width={W} height={H - 1480} fill="#8a5a33" />
    {range(10).map((i) => <line key={i} x1={i * 110} y1={1480} x2={i * 110} y2={1920} stroke="#6b4223" strokeWidth={6} />)}
    <g transform="translate(80,1380)">
      <rect width={110} height={140} rx={30} fill="#9a6a3a" stroke={INK} strokeWidth={6} />
      <path d="M0,40 H110 M0,100 H110" stroke="#4a2e18" strokeWidth={8} />
    </g>
  </g>
);

const Carsi = () => (
  <g>
    <rect width={W} height={H} fill="#c9a77a" />
    {range(4).map((i) => <path key={i} d={`M${i * 270},0 Q${i * 270 + 135},-60 ${i * 270 + 270},0 L${i * 270 + 270},300 Q${i * 270 + 135},180 ${i * 270},300 Z`} fill={i % 2 ? '#b38a5c' : '#e7d3b2'} stroke={INK} strokeWidth={5} />)}
    {range(3).map((i) => (
      <g key={i} transform={`translate(${40 + i * 350},420)`}>
        <Arch x={0} y={0} w={300} h={900} fill="#5a3a22" />
        <rect x={30} y={250} width={240} height={60} fill="#c0283a" />
        <rect x={30} y={330} width={240} height={60} fill="#2e5e9e" />
        <rect x={30} y={410} width={240} height={60} fill="#d4a73c" />
        {range(3).map((j) => <circle key={j} cx={80 + j * 70} cy={160} r={26} fill={['#e2b84a', '#5fa0d8', '#d8343c'][j]} stroke={INK} strokeWidth={4} />)}
        <rect x={20} y={620} width={260} height={60} fill="#8a5a33" stroke={INK} strokeWidth={5} />
      </g>
    ))}
    <rect y={1400} width={W} height={H - 1400} fill="#9c8a74" />
    {range(40).map((i) => <rect key={i} x={(i % 8) * 140 - ((Math.floor(i / 8) % 2) * 70)} y={1400 + Math.floor(i / 8) * 104} width={140} height={104} fill="none" stroke="#7a6a56" strokeWidth={5} />)}
  </g>
);

const Zindan = () => (
  <g>
    <rect width={W} height={H} fill="#3b3a40" />
    {range(120).map((i) => {
      const row = Math.floor(i / 8);
      return <rect key={i} x={(i % 8) * 150 - (row % 2) * 75} y={row * 90} width={150} height={90} fill={i % 3 ? '#45444b' : '#4d4c54'} stroke="#2a292e" strokeWidth={6} />;
    })}
    <rect x={420} y={300} width={240} height={220} fill="#9fb6c9" stroke={INK} strokeWidth={8} />
    {range(4).map((i) => <line key={i} x1={450 + i * 60} y1={300} x2={450 + i * 60} y2={520} stroke="#222" strokeWidth={14} />)}
    <path d="M420,520 L660,520 L900,1700 L180,1700 Z" fill="#cfe0ea" opacity={0.12} />
    <path d="M120,700 q20,40 0,80 q-20,40 0,80 q20,40 0,80" stroke="#777" strokeWidth={10} fill="none" />
    <rect y={1500} width={W} height={H - 1500} fill="#2a292e" />
    {range(14).map((i) => <path key={i} d={`M${60 + i * 70},1780 l30,-40`} stroke="#b59a55" strokeWidth={5} />)}
  </g>
);

const IdamMeydani = () => (
  <g>
    <rect width={W} height={H} fill="#7d8590" />
    {range(5).map((i) => <ellipse key={i} cx={120 + i * 230} cy={200 + (i % 2) * 60} rx={220} ry={70} fill="#5d646e" />)}
    <path d="M0,1000 L200,880 L380,960 L560,820 L760,940 L1080,860 L1080,1100 L0,1100 Z" fill="#4c5259" />
    <rect y={1100} width={W} height={H - 1100} fill="#8b8276" />
    <path d="M780,1100 Q770,700 840,480 Q700,420 760,300 Q900,180 1020,320 Q1100,420 980,500 Q900,700 900,1100 Z" fill="#3d4a3a" stroke={INK} strokeWidth={6} />
    {range(12).map((i) => <ellipse key={i} cx={40 + i * 90} cy={1240 + (i % 2) * 20} rx={40} ry={70} fill="#3a3a3f" />)}
    {range(12).map((i) => <circle key={'h' + i} cx={40 + i * 90} cy={1160 + (i % 2) * 20} r={30} fill="#3a3a3f" />)}
    <rect x={160} y={1300} width={760} height={120} fill="#5a3a22" stroke={INK} strokeWidth={6} />
    <rect y={1420} width={W} height={H - 1420} fill="#a09482" />
  </g>
);

export const Background: React.FC<{ mekan: MekanId; gece?: boolean }> = ({ mekan, gece }) => {
  const inner = (() => {
    switch (mekan) {
      case 'divan': return <Divan />;
      case 'konak_salon': return <KonakSalon gece={gece} />;
      case 'lale_bahcesi': return <LaleBahcesi />;
      case 'halic_liman': return <HalicLiman gece={gece} />;
      case 'carsi': return <Carsi />;
      case 'zindan': return <Zindan />;
      case 'idam_meydani': return <IdamMeydani />;
    }
  })();
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: 'absolute', inset: 0 }}>
      {inner}
      {gece && mekan !== 'konak_salon' && mekan !== 'halic_liman' && <rect width={W} height={H} fill="#0b1433" opacity={0.45} />}
      {gece && mekan === 'konak_salon' && <rect width={W} height={H} fill="#0b1433" opacity={0.25} />}
    </svg>
  );
};
