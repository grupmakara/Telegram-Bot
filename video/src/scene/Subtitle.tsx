import React from 'react';
import type { Word } from '../audio/synth';
import { pagesOf, wrapWords } from './subtitleLayout';

const ROWS_PER_PAGE = 2;
const MAX_CHARS = 22;

/** Kelime kelime vurgulu altyazı. currentMs: replik başından itibaren geçen süre. */
export const Subtitle: React.FC<{ words: Word[]; currentMs: number; speaker?: string; top?: number }> = ({ words, currentMs, speaker, top = 1420 }) => {
  const rows = wrapWords(words.map((w) => w.text), MAX_CHARS);
  // her satırı kelime nesnelerine geri eşle
  let idx = 0;
  const wordRows = rows.map((r) => r.map(() => words[idx++]));
  const pages = pagesOf(wordRows, ROWS_PER_PAGE);
  const pageIdx = Math.max(0, pages.findIndex((p) => p[p.length - 1][p[p.length - 1].length - 1].endMs >= currentMs));
  const page = pages[pageIdx === -1 ? pages.length - 1 : pageIdx];
  return (
    <div style={{ position: 'absolute', left: 60, right: 60, top, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      {speaker ? (
        <div style={{ fontFamily: 'Nunito, sans-serif', fontWeight: 800, fontSize: 34, color: '#2b1d14', background: '#e9c46a', borderRadius: 14, padding: '2px 18px', marginBottom: 10, border: '3px solid #2b1d14' }}>
          {speaker}
        </div>
      ) : null}
      {page.map((row, ri) => (
        <div key={ri} style={{ display: 'flex', gap: 18, justifyContent: 'center', flexWrap: 'wrap' }}>
          {row.map((w, wi) => {
            const active = currentMs >= w.startMs && currentMs < w.endMs + 80;
            return (
              <span key={wi} style={{ fontFamily: 'Nunito, sans-serif', fontWeight: 800, fontSize: 70, lineHeight: 1.15, color: active ? '#FFD54A' : '#fff', WebkitTextStroke: '14px #111', paintOrder: 'stroke fill', transform: active ? 'scale(1.08)' : undefined, display: 'inline-block' }}>
                {w.text}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};
