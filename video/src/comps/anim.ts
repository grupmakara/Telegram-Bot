import type { SpeakerId } from '../story/registry';
import type { TimedLine } from '../timeline/build';

/** Konuşan karakterin ağız açıklığı (0..1). */
export function mouthFor(id: SpeakerId, active: TimedLine | undefined, absFrame: number, fps: number): number {
  if (!active || active.line.kim !== id) return 0;
  const ms = ((absFrame - active.from) / fps) * 1000;
  const words = active.audio.words;
  const speaking = words.length ? words.some((w) => ms >= w.startMs - 30 && ms <= w.endMs + 30) : ms < active.audio.durationMs;
  if (!speaking) return 0;
  return (absFrame >> 2) % 2 ? 1 : 0.4;
}

export const activeLine = (lines: TimedLine[], abs: number) => lines.find((l) => abs >= l.from && abs < l.from + l.dur);

