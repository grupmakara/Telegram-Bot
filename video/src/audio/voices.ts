import type { SpeakerId } from '../story/registry';

export type VoiceCfg = { voice: string; pitch: string; rate: string };
const A = 'tr-TR-AhmetNeural';
const E = 'tr-TR-EmelNeural';
const v = (voice: string, pitch: string, rate: string): VoiceCfg => ({ voice, pitch, rate });

export const VOICES: Record<SpeakerId, VoiceCfg> = {
  emir: v(A, '+0Hz', '+10%'),
  murad: v(A, '+0Hz', '+10%'),
  bekir: v(A, '-15Hz', '+0%'),
  saffet: v(A, '-8Hz', '+12%'),
  lutfi: v(A, '-5Hz', '-2%'),
  hizir: v(A, '-10Hz', '+0%'),
  yusuf: v(A, '-12Hz', '+2%'),
  nilufer: v(E, '+0Hz', '+10%'),
  zeynep: v(E, '+10Hz', '+15%'),
  anlatici: v(A, '-4Hz', '+8%'),
};
