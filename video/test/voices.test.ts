import { describe, it, expect } from 'vitest';
import { VOICES } from '../src/audio/voices';
import { cacheKey } from '../src/audio/synth';
import { SPEAKER_IDS } from '../src/story/registry';

describe('voices', () => {
  it('every speaker has a voice', () => {
    for (const id of SPEAKER_IDS) expect(VOICES[id]?.voice).toMatch(/^tr-TR-(Ahmet|Emel)Neural$/);
  });
  it('bekir is deeper and slower than emir', () => {
    expect(VOICES.bekir).toEqual({ voice: 'tr-TR-AhmetNeural', pitch: '-15Hz', rate: '-10%' });
  });
  it('cache key depends on voice settings', () => {
    expect(cacheKey('Evet.', VOICES.emir)).not.toBe(cacheKey('Evet.', VOICES.bekir));
    expect(cacheKey('Evet.', VOICES.emir)).toBe(cacheKey('Evet.', VOICES.murad));
  });
});
