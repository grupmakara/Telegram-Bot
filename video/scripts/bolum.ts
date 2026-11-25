/** Kullanım: npm run bolum -- <bölüm no | yaml yolu> [--sadece-kapak] */
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { loadEpisode } from '../src/story/load';
import { synthEpisode } from '../src/audio/synth';
import { buildTimeline } from '../src/timeline/build';

const ROOT = resolve(import.meta.dirname, '..');
const arg = process.argv[2];
if (!arg) {
  console.error('Kullanım: npm run bolum -- <bölüm no | yaml yolu>');
  process.exit(1);
}
const yamlPath = /^\d+$/.test(arg) ? join(ROOT, 'story/episodes', `ep${arg.padStart(2, '0')}.yaml`) : resolve(arg);
if (!existsSync(yamlPath)) {
  console.error(`Bulunamadı: ${yamlPath}`);
  process.exit(1);
}

const ep = loadEpisode(yamlPath);
const name = `ep${String(ep.bolum).padStart(2, '0')}`;
const out = join(ROOT, 'out');
mkdirSync(out, { recursive: true });

console.log(`▶ ${name}: seslendiriliyor…`);
const audio = synthEpisode(ep, join(ROOT, 'public/audio'));
const timeline = buildTimeline(ep, audio, 30);
const secs = timeline.durationInFrames / 30;
const propsFile = join(out, `${name}.props.json`);
writeFileSync(propsFile, JSON.stringify({ episode: ep, timeline }));

const remotion = (cmd: string, ...rest: string[]) =>
  execFileSync('npx', ['remotion', cmd, 'src/index.ts', 'Episode', ...rest, `--props=${propsFile}`, '--log=error'], { cwd: ROOT, stdio: 'inherit' });

console.log(`▶ ${name}: kapak…`);
remotion('still', join(out, `${name}_kapak.png`), '--frame=20');
if (!process.argv.includes('--sadece-kapak')) {
  console.log(`▶ ${name}: video (${secs.toFixed(1)} sn)…`);
  remotion('render', join(out, `${name}.mp4`), '--concurrency=4');
}
writeFileSync(join(out, `${name}_aciklama.txt`), `${ep.aciklama.trim()}\n\n${ep.etiketler.join(' ')}\n`);

console.log(`✔ ${name} hazır: ${secs.toFixed(1)} sn`);
if (secs < 60 || secs > 90) console.warn(`⚠ Süre 60–90 sn hedefinin dışında (${secs.toFixed(1)} sn)`);
