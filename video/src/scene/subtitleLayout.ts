import type { Word } from '../audio/synth';

export function wrapWords(words: string[], maxChars = 24): string[][] {
  const rows: string[][] = [];
  let cur: string[] = [];
  for (const w of words) {
    const next = [...cur, w].join(' ');
    if (cur.length && next.length > maxChars) {
      rows.push(cur);
      cur = [w];
    } else cur.push(w);
  }
  if (cur.length) rows.push(cur);
  return rows;
}

export function pagesOf<T>(rows: T[], perPage = 2): T[][] {
  const out: T[][] = [];
  for (let i = 0; i < rows.length; i += perPage) out.push(rows.slice(i, i + perPage));
  return out;
}

/** Orijinal metnin kelimelerini (noktalama dahil) TTS kelime zamanlarına eşler. */
export function alignWords(metin: string, words: Word[], durationMs: number): Word[] {
  const tokens = metin.split(/\s+/).filter(Boolean);
  if (tokens.length === words.length) return tokens.map((text, i) => ({ ...words[i], text }));
  const step = durationMs / tokens.length;
  return tokens.map((text, i) => ({ text, startMs: Math.round(i * step), endMs: Math.round((i + 1) * step) }));
}
