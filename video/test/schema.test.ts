import { describe, it, expect } from 'vitest';
import { writeFileSync, mkdtempSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { loadEpisode } from '../src/story/load';
import { trUpper } from '../src/story/registry';

const fixture = join(__dirname, 'fixtures/ep99.yaml');
const tmp = (name: string, body: string) => { const p = join(mkdtempSync(join(tmpdir(), 'ep')), name); writeFileSync(p, body); return p; };

describe('loadEpisode', () => {
  it('parses a valid episode', () => {
    const ep = loadEpisode(fixture);
    expect(ep.bolum).toBe(99);
    expect(ep.sahneler).toHaveLength(2);
    expect(ep.sahneler[0].satirlar[2].ifade).toBe('ofkeli');
  });
  it('rejects unknown speaker with file name and path', () => {
    const bad = readFileSync(fixture, 'utf8').replace('{ kim: anlatici,', '{ kim: ahmet,');
    const p = tmp('kotu.yaml', bad);
    expect(() => loadEpisode(p)).toThrow(/kotu\.yaml[\s\S]*sahneler\.0\.satirlar\.0\.kim/);
  });
  it('rejects a speaker not present in the scene', () => {
    const bad = readFileSync(fixture, 'utf8').replace('{ kim: zeynep, metin', '{ kim: bekir, metin');
    expect(() => loadEpisode(tmp('yok.yaml', bad))).toThrow(/bekir/);
  });
  it('rejects unknown location', () => {
    const bad = readFileSync(fixture, 'utf8').replace('mekan: konak_salon', 'mekan: uzay');
    expect(() => loadEpisode(tmp('mekan.yaml', bad))).toThrow(/sahneler\.1\.mekan/);
  });
});

describe('trUpper', () => {
  it('handles Turkish casing', () => {
    expect(trUpper('lale ile kan')).toBe('LALE İLE KAN');
    expect(trUpper('ışık')).toBe('IŞIK');
  });
});
