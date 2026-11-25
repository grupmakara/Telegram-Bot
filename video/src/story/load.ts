import { readFileSync } from 'node:fs';
import { parse } from 'yaml';
import { EpisodeSchema, type Episode } from './schema';

export function loadEpisode(path: string): Episode {
  const res = EpisodeSchema.safeParse(parse(readFileSync(path, 'utf8')));
  if (!res.success) {
    const issues = res.error.issues.map((i) => `  ${i.path.join('.')}: ${i.message}`).join('\n');
    throw new Error(`${path} geçersiz:\n${issues}`);
  }
  return res.data;
}
