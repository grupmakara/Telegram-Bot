import { describe, it, expect } from 'vitest';
import { captionGroups } from '../src/hf/captions';

const w = (text: string, s: number, e: number) => ({ text, startMs: s, endMs: e });

describe('captionGroups', () => {
  it('breaks at sentence end', () => {
    const g = captionGroups([w('Hazır', 0, 300), w('mısın?', 300, 600), w('Evet.', 700, 900)]);
    expect(g.map((x) => x.text)).toEqual(['Hazır mısın?', 'Evet.']);
    expect(g[1].startMs).toBe(700);
  });
  it('caps at 5 words and 30 chars', () => {
    const words = 'bir iki üç dört beş altı yedi'.split(' ').map((t, i) => w(t, i * 100, i * 100 + 90));
    const g = captionGroups(words);
    expect(g[0].text).toBe('bir iki üç dört beş');
    for (const x of g) expect(x.text.length).toBeLessThanOrEqual(30);
  });
  it('breaks at a pause of 150 ms or more', () => {
    const g = captionGroups([w('Sen', 0, 200), w('mi', 400, 500)]);
    expect(g).toHaveLength(2);
  });
});
