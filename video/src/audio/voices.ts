import type { SpeakerId } from '../story/registry';

export type Provider = 'elevenlabs' | 'edge';
export type VoiceCfg = { provider: Provider; voice: string; pitch: string; rate: string; settings?: { stability: number; similarity_boost: number; style: number } };

const A = 'tr-TR-AhmetNeural';
const E = 'tr-TR-EmelNeural';
const e = (voice: string, pitch: string, rate: string): VoiceCfg => ({ provider: 'edge', voice, pitch, rate });

/** Yedek: ücretsiz Edge sesleri (yalnız 2 Türkçe ses). */
export const EDGE_VOICES: Record<SpeakerId, VoiceCfg> = {
  emir: e(A, '+0Hz', '+10%'),
  murad: e(A, '+0Hz', '+10%'),
  bekir: e(A, '-15Hz', '+0%'),
  saffet: e(A, '-8Hz', '+12%'),
  lutfi: e(A, '-5Hz', '-2%'),
  hizir: e(A, '-10Hz', '+0%'),
  yusuf: e(A, '-12Hz', '+2%'),
  nilufer: e(E, '+0Hz', '+10%'),
  zeynep: e(E, '+10Hz', '+15%'),
  anlatici: e(A, '-4Hz', '+8%'),
};

const el = (voice: string, stability = 0.45, style = 0.35): VoiceCfg => ({ provider: 'elevenlabs', voice, pitch: '', rate: '', settings: { stability, similarity_boost: 0.8, style } });

/**
 * ElevenLabs hazır sesleri (eleven_multilingual_v2 ile Türkçe konuşur).
 * Kimlikler ElevenLabs'in herkese açık hazır sesleridir; anahtar gelince dinlenip gerekirse değiştirilecek.
 */
export const EL_VOICES: Record<SpeakerId, VoiceCfg> = {
  emir: el('TxGEqnHWrfWFTfGW9XjX'), // Josh — genç, derin erkek
  murad: el('TxGEqnHWrfWFTfGW9XjX'),
  bekir: el('2EiwWnXFnvU5JabPnv8n', 0.35, 0.5), // Clyde — sert, kalın, yaşlı
  saffet: el('N2lVS1w4EtoT3dr4eOWO', 0.4, 0.45), // Callum — boğuk, tehditkâr
  lutfi: el('onwK4e9ZLuTAKqWW03F9', 0.55, 0.2), // Daniel — ağır, yaşlı
  hizir: el('VR6AewLTigWG4xSOukaG', 0.5, 0.3), // Arnold — kalın, yaşlı kaptan
  yusuf: el('pNInz6obpgDQGcFmaJgB', 0.5, 0.4), // Adam — derin, olgun
  nilufer: el('21m00Tcm4TlvDq8ikWAM', 0.45, 0.35), // Rachel — genç kadın
  zeynep: el('EXAVITQu4vr4xnJDKyoq', 0.45, 0.35), // Bella — yumuşak, genç kız
  anlatici: el('nPczCjzI2devNBz1zQrb', 0.6, 0.2), // Brian — derin anlatıcı
};

export const voicesFor = (p: Provider) => (p === 'elevenlabs' ? EL_VOICES : EDGE_VOICES);
/** Geriye dönük: Edge eşlemesi. */
export const VOICES = EDGE_VOICES;
