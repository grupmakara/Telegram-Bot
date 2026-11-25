import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import type { Episode, Line } from '../story/schema';
import { voicesFor, type Provider, type VoiceCfg } from './voices';

export type Word = { text: string; startMs: number; endMs: number };
export type AudioMeta = { file: string; durationMs: number; words: Word[] };

export const cacheKey = (text: string, cfg: VoiceCfg): string =>
  createHash('sha1').update(`${cfg.provider}|${cfg.voice}|${cfg.pitch}|${cfg.rate}|${JSON.stringify(cfg.settings ?? {})}|${text}`).digest('hex').slice(0, 16);

export function allLines(ep: Episode): Line[] {
  return [ep.kanca, ...ep.sahneler.flatMap((s) => s.satirlar), ep.son];
}

const ROOT = resolve(import.meta.dirname, '../..');

/** Tüm replikleri seslendirir (önbellekli). ElevenLabs yetkisizse Edge'e düşer ve uyarır. */
export function synthEpisode(ep: Episode, cacheDir: string, provider: Provider = (process.env.TTS_PROVIDER as Provider) || 'elevenlabs'): { audio: Map<Line, AudioMeta>; provider: Provider } {
  const lines = allLines(ep);
  const voices = voicesFor(provider);
  const keys = lines.map((l) => cacheKey(l.metin, voices[l.kim]));
  mkdirSync(cacheDir, { recursive: true });
  const job = join(cacheDir, `job-${ep.bolum}-${provider}.json`);
  writeFileSync(job, JSON.stringify({
    outDir: cacheDir,
    items: lines.map((l, i) => ({ key: keys[i], text: l.metin, ...voices[l.kim] })),
  }));
  try {
    execFileSync(join(ROOT, '.venv/bin/python'), [join(ROOT, 'tts/synth.py'), job], { stdio: 'inherit' });
  } catch (e) {
    if (provider === 'elevenlabs' && (e as { status?: number }).status === 3) {
      console.warn('⚠ ElevenLabs anahtarı yok ya da geçersiz — geçici olarak Edge sesleri kullanılıyor.');
      return synthEpisode(ep, cacheDir, 'edge');
    }
    throw e;
  }
  const out = new Map<Line, AudioMeta>();
  lines.forEach((l, i) => {
    const meta = JSON.parse(readFileSync(join(cacheDir, `${keys[i]}.json`), 'utf8'));
    out.set(l, { file: join(cacheDir, `${keys[i]}.mp3`), ...meta });
  });
  return { audio: out, provider };
}
