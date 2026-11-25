import { describe, it, expect } from 'vitest';
import { wrapWords, alignWords, pagesOf } from '../src/scene/subtitleLayout';

describe('wrapWords', () => {
  it('keeps rows within maxChars', () => {
    const words = 'Babamın kanını yerde bırakanlar bu şehirde rahat uyuyor ama artık uyuyamayacaklar efendim'.split(' ');
    const rows = wrapWords(words, 24);
    for (const r of rows) expect(r.join(' ').length).toBeLessThanOrEqual(24);
    expect(rows.flat()).toEqual(words);
  });
  it('allows a single over-long word on its own row', () => {
    expect(wrapWords(['Kısa', 'Çekoslovakyalılaştıramadıklarımızdan', 'mı'], 24)).toEqual([['Kısa'], ['Çekoslovakyalılaştıramadıklarımızdan'], ['mı']]);
  });
  it('pages are two rows each and keep order', () => {
    const rows = [['a'], ['b'], ['c'], ['d'], ['e']];
    expect(pagesOf(rows, 2)).toEqual([[['a'], ['b']], [['c'], ['d']], [['e']]]);
  });
});

describe('alignWords', () => {
  it('maps original tokens (with punctuation) onto boundary timings', () => {
    const t = alignWords('Zeynep?.. Sen yaşıyor musun?', [
      { text: 'Zeynep', startMs: 100, endMs: 600 }, { text: 'Sen', startMs: 900, endMs: 1100 },
      { text: 'yaşıyor', startMs: 1100, endMs: 1600 }, { text: 'musun', startMs: 1600, endMs: 2000 },
    ], 2200);
    expect(t.map((w) => w.text)).toEqual(['Zeynep?..', 'Sen', 'yaşıyor', 'musun?']);
    expect(t[1].startMs).toBe(900);
  });
  it('falls back to even spread when counts differ', () => {
    const t = alignWords('İstanbul, 1720 yılı.', [{ text: 'İstanbul', startMs: 0, endMs: 500 }], 3000);
    expect(t).toHaveLength(3);
    expect(t[2].startMs).toBe(2000);
  });
});
