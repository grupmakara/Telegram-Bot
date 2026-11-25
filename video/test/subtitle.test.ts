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

import { pageIndexAt, fontSizeFor } from '../src/scene/subtitleLayout';
describe('pageIndexAt', () => {
  const w = (s: number, e: number) => ({ text: 'x', startMs: s, endMs: e });
  const pages = [[[w(0, 100)], [w(100, 200)]], [[w(200, 300)], [w(300, 400)]]];
  it('stays on the last page after the last word ends', () => expect(pageIndexAt(pages, 900)).toBe(1));
  it('shows the page of the current word', () => { expect(pageIndexAt(pages, 50)).toBe(0); expect(pageIndexAt(pages, 250)).toBe(1); });
});
describe('fontSizeFor', () => {
  it('keeps base size for normal rows', () => expect(fontSizeFor(['Hazır mısın evlat?'])).toBe(82));
  it('shrinks so a long single word fits in 900px', () => {
    const s = fontSizeFor(['Anlayamadıklarımızdanmışsınız']);
    expect(s).toBeLessThan(82);
    expect(s * 0.55 * 29).toBeLessThanOrEqual(900);
  });
});
