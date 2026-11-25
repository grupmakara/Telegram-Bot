import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import type { Episode, Line } from '../story/schema';
import { VOICES, type VoiceCfg } from './voices';

export type Word = { text: string; startMs: number; endMs: number };
export type AudioMeta = { file: string; durationMs: number; words: Word[] };

export const cacheKey = (text: string, cfg: VoiceCfg): string =>
  createHash('sha1').update(`${cfg.voice}|${cfg.pitch}|${cfg.rate}|${text}`).digest('hex').slice(0, 16);

export function allLines(ep: Episode): Line[] {
  return [ep.kanca, ...ep.sahneler.flatMap((s) => s.satirlar), ep.son];
}

const ROOT = resolve(import.meta.dirname, '../..');

/** Tüm replikleri seslendirir (önbellekli). Dosya yolları cacheDir'e göre mutlak döner. */
export function synthEpisode(ep: Episode, cacheDir: string): Map<Line, AudioMeta> {
  const lines = allLines(ep);
  const keys = lines.map((l) => cacheKey(l.metin, VOICES[l.kim]));
  mkdirSync(cacheDir, { recursive: true });
  const job = join(cacheDir, `job-${ep.bolum}.json`);
  writeFileSync(job, JSON.stringify({
    outDir: cacheDir,
    items: lines.map((l, i) => ({ key: keys[i], text: l.metin, ...VOICES[l.kim] })),
  }));
  execFileSync(join(ROOT, '.venv/bin/python'), [join(ROOT, 'tts/synth.py'), job], { stdio: 'inherit' });
  const out = new Map<Line, AudioMeta>();
  lines.forEach((l, i) => {
    const meta = JSON.parse(readFileSync(join(cacheDir, `${keys[i]}.json`), 'utf8'));
    out.set(l, { file: join(cacheDir, `${keys[i]}.mp3`), ...meta });
  });
  return out;
}
