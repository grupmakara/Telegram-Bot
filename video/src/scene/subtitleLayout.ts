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

/** O an gösterilecek altyazı sayfası: içinde bulunulan kelimenin sayfası; son kelimeden sonra son sayfa. */
export function pageIndexAt(pages: Word[][][], currentMs: number): number {
  const i = pages.findIndex((p) => {
    const last = p[p.length - 1];
    return last[last.length - 1].endMs >= currentMs;
  });
  return i === -1 ? pages.length - 1 : i;
}

const EM_PER_CHAR = 0.55; // Nunito 800 için temkinli ortalama karakter genişliği
/** Satırların 900 px'e sığması için yazı boyutu (gerekirse küçültür). */
export function fontSizeFor(rows: string[], base = 82, maxPx = 900): number {
  const longest = Math.max(...rows.map((r) => r.length));
  return Math.min(base, Math.floor(maxPx / (longest * EM_PER_CHAR)));
}
