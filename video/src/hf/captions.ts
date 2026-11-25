import type { Word } from '../audio/synth';

export type CaptionGroup = { text: string; startMs: number; endMs: number };

/** Sakin altyazı grupları: en çok 5 kelime / 30 karakter; cümle sonu ya da 150 ms+ duraksamada böl. */
export function captionGroups(words: Word[], maxWords = 5, maxChars = 30): CaptionGroup[] {
  const out: CaptionGroup[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) out.push({ text: cur.map((x) => x.text).join(' '), startMs: cur[0].startMs, endMs: cur[cur.length - 1].endMs });
    cur = [];
  };
  words.forEach((wd, i) => {
    const prev = cur[cur.length - 1];
    if (prev && (wd.startMs - prev.endMs >= 150 || cur.length >= maxWords || [...cur, wd].map((x) => x.text).join(' ').length > maxChars)) flush();
    cur.push(wd);
    if (/[.!?…]$/.test(wd.text)) flush();
    if (i === words.length - 1) flush();
  });
  return out;
}
