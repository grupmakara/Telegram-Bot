import { describe, it, expect } from 'vitest';
import { loadEpisode } from '../src/story/load';
import { allLines, type AudioMeta } from '../src/audio/synth';
import { buildTimeline, RULES } from '../src/timeline/build';
import type { Line } from '../src/story/schema';

const ep = loadEpisode(__dirname + '/fixtures/ep99.yaml');
const audio = new Map<Line, AudioMeta>(allLines(ep).map((l) => [l, { file: 'x.mp3', durationMs: 1000, words: [] }]));
const f = (ms: number) => Math.ceil((ms / 1000) * 30);

describe('buildTimeline', () => {
  const tl = buildTimeline(ep, audio, 30);
  it('total frames follow the rules', () => {
    const line = f(1000);
    const kanca = line + RULES.kancaTail;
    const scene1 = 3 * line + 2 * RULES.lineGap + RULES.sceneFade;
    const scene2 = 1 * line + RULES.sceneFade;
    const son = line + RULES.sonTail;
    expect(tl.durationInFrames).toBe(kanca + RULES.titleFlash + scene1 + scene2 + son + RULES.devam);
  });
  it('segments are ordered kanca, sahne, sahne, son, devam', () => {
    expect(tl.segments.map((s) => s.kind)).toEqual(['kanca', 'sahne', 'sahne', 'son', 'devam']);
  });
  it('lines never overlap and frames are integers', () => {
    const lines = tl.segments.flatMap((s) => s.lines);
    for (let i = 1; i < lines.length; i++) expect(lines[i].from).toBeGreaterThanOrEqual(lines[i - 1].from + lines[i - 1].dur);
    for (const l of lines) { expect(Number.isInteger(l.from)).toBe(true); expect(Number.isInteger(l.dur)).toBe(true); }
  });
});
