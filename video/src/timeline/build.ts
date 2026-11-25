import type { Episode, Line } from '../story/schema';
import type { AudioMeta } from '../audio/synth';

/** Son kelimeden sonra bırakılan sessizlik (edge-tts ~1.2 sn boşluk ekliyor). */
export const TAIL_MS = 300;

export const RULES = { kancaTail: 15, titleFlash: 30, lineGap: 8, sceneFade: 12, sonTail: 15, devam: 60 } as const;

export type TimedLine = { line: Line; from: number; dur: number; audio: AudioMeta };
export type Segment = { kind: 'kanca' | 'sahne' | 'son' | 'devam'; from: number; dur: number; sceneIndex?: number; lines: TimedLine[] };
export type Timeline = { durationInFrames: number; fps: number; segments: Segment[] };

export function buildTimeline(ep: Episode, audio: Map<Line, AudioMeta>, fps = 30): Timeline {
  const frames = (l: Line) => {
    const a = audio.get(l);
    if (!a) throw new Error(`Ses yok: ${l.kim}: ${l.metin}`);
    const last = a.words.length ? a.words[a.words.length - 1].endMs + TAIL_MS : a.durationMs;
    return Math.ceil((Math.min(a.durationMs, last) / 1000) * fps);
  };
  const timed = (l: Line, from: number): TimedLine => ({ line: l, from, dur: frames(l), audio: audio.get(l)! });
  const segments: Segment[] = [];
  let t = 0;

  const k = timed(ep.kanca, 0);
  segments.push({ kind: 'kanca', from: 0, dur: k.dur + RULES.kancaTail, lines: [k] });
  t += k.dur + RULES.kancaTail;

  ep.sahneler.forEach((s, i) => {
    const start = t;
    let c = t + (i === 0 ? RULES.titleFlash : 0);
    const lines = s.satirlar.map((l, li) => {
      if (li > 0) c += RULES.lineGap;
      const tl = timed(l, c);
      c += tl.dur;
      return tl;
    });
    c += RULES.sceneFade;
    segments.push({ kind: 'sahne', from: start, dur: c - start, sceneIndex: i, lines });
    t = c;
  });

  const son = timed(ep.son, t);
  segments.push({ kind: 'son', from: t, dur: son.dur + RULES.sonTail, sceneIndex: ep.sahneler.length - 1, lines: [son] });
  t += son.dur + RULES.sonTail;
  segments.push({ kind: 'devam', from: t, dur: RULES.devam, lines: [] });
  t += RULES.devam;

  return { durationInFrames: t, fps, segments };
}
