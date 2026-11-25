import type { SpeakerId } from '../story/registry';

export type VoiceCfg = { voice: string; pitch: string; rate: string };
const A = 'tr-TR-AhmetNeural';
const E = 'tr-TR-EmelNeural';
const v = (voice: string, pitch: string, rate: string): VoiceCfg => ({ voice, pitch, rate });

export const VOICES: Record<SpeakerId, VoiceCfg> = {
  emir: v(A, '+0Hz', '+0%'),
  murad: v(A, '+0Hz', '+0%'),
  bekir: v(A, '-15Hz', '-10%'),
  saffet: v(A, '-8Hz', '+5%'),
  lutfi: v(A, '-5Hz', '-15%'),
  hizir: v(A, '-10Hz', '-12%'),
  yusuf: v(A, '-12Hz', '-8%'),
  nilufer: v(E, '+0Hz', '+0%'),
  zeynep: v(E, '+10Hz', '+8%'),
  anlatici: v(A, '-4Hz', '-5%'),
};
