import { describe, it, expect } from 'vitest';
import { EDGE_VOICES, EL_VOICES } from '../src/audio/voices';
import { cacheKey } from '../src/audio/synth';
import { SPEAKER_IDS } from '../src/story/registry';

describe('voices', () => {
  it('every speaker has an edge and an ElevenLabs voice', () => {
    for (const id of SPEAKER_IDS) {
      expect(EDGE_VOICES[id].voice).toMatch(/^tr-TR-(Ahmet|Emel)Neural$/);
      expect(EL_VOICES[id].voice).toMatch(/^[A-Za-z0-9]{20}$/);
    }
  });
  it('main characters have distinct ElevenLabs voices', () => {
    const ids = ['emir', 'bekir', 'saffet', 'lutfi', 'hizir', 'yusuf', 'nilufer', 'zeynep', 'anlatici'] as const;
    expect(new Set(ids.map((i) => EL_VOICES[i].voice)).size).toBe(ids.length);
  });
  it('cache key depends on provider and voice settings', () => {
    expect(cacheKey('Evet.', EDGE_VOICES.emir)).not.toBe(cacheKey('Evet.', EDGE_VOICES.bekir));
    expect(cacheKey('Evet.', EDGE_VOICES.emir)).not.toBe(cacheKey('Evet.', EL_VOICES.emir));
    expect(cacheKey('Evet.', EL_VOICES.emir)).toBe(cacheKey('Evet.', EL_VOICES.murad));
  });
});
