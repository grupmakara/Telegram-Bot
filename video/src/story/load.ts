import { readFileSync } from 'node:fs';
import { parse } from 'yaml';
import { EpisodeSchema, type Episode } from './schema';

export function loadEpisode(path: string): Episode {
  let raw: unknown;
  try {
    raw = parse(readFileSync(path, 'utf8'));
  } catch (e) {
    throw new Error(`${path}: YAML hatası: ${(e as Error).message}`);
  }
  const res = EpisodeSchema.safeParse(raw);
  if (!res.success) {
    const issues = res.error.issues.map((i) => `  ${i.path.join('.') || '(kök)'}: ${i.message}${'keys' in i ? ' ' + (i as { keys: string[] }).keys.join(', ') : ''}`).join('\n');
    throw new Error(`${path} geçersiz:\n${issues}`);
  }
  return res.data;
}
