/**
 * Kullanım: npm run bolum -- <bölüm no | yaml yolu> [--sadece-proje] [--muzik <dosya>]
 * YAML → seslendirme → HyperFrames projesi (projects/epNN) → kontrol → MP4 + kapak + açıklama (out/).
 */
import { execFileSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdirSync, readdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { loadEpisode } from '../src/story/load';
import { synthEpisode } from '../src/audio/synth';
import { buildTimeline } from '../src/timeline/build';
import { buildProject } from '../src/hf/build';

const ROOT = resolve(import.meta.dirname, '..');
const HF = join(ROOT, 'node_modules/.bin/hyperframes');
const args = process.argv.slice(2);
const arg = args[0];
if (!arg) {
  console.error('Kullanım: npm run bolum -- <bölüm no | yaml yolu> [--sadece-proje] [--muzik <dosya>]');
  process.exit(1);
}
const yamlPath = /^\d+$/.test(arg) ? join(ROOT, 'story/episodes', `ep${arg.padStart(2, '0')}.yaml`) : resolve(arg);
if (!existsSync(yamlPath)) {
  console.error(`Bulunamadı: ${yamlPath}`);
  process.exit(1);
}
const mi = args.indexOf('--muzik');
const defaultBgm = join(ROOT, 'assets/bgm/tema.mp3');
const bgm = mi >= 0 ? resolve(args[mi + 1]) : existsSync(defaultBgm) ? defaultBgm : undefined;

const ep = loadEpisode(yamlPath);
const name = `ep${String(ep.bolum).padStart(2, '0')}`;
const out = join(ROOT, 'out');
const proj = join(ROOT, 'projects', name);
mkdirSync(out, { recursive: true });

console.log(`▶ ${name}: seslendiriliyor…`);
const { audio, provider } = synthEpisode(ep, join(ROOT, 'cache/audio'));
console.log(`  ses: ${provider === 'elevenlabs' ? 'ElevenLabs' : 'Edge (yedek)'}`);
const timeline = buildTimeline(ep, audio, 30);
const { total } = buildProject(ep, timeline, proj, { bgm });
console.log(`▶ ${name}: proje hazır (${total.toFixed(1)} sn) → ${proj}${bgm ? '' : ' (müzik yok)'}`);
writeFileSync(join(out, `${name}_aciklama.txt`), `${ep.aciklama.trim()}\n\n${ep.etiketler.join(' ')}\n`);

const hf = (...a: string[]) => execFileSync(HF, a, { cwd: proj, stdio: ['ignore', 'pipe', 'inherit'], encoding: 'utf8' });
type Finding = { code: string; severity: string; message: string };
const check = JSON.parse(hf('check', '--json')) as { ok: boolean } & Record<string, { findings?: Finding[] }>;
const findings = Object.values(check).flatMap((v) => (v && typeof v === 'object' && Array.isArray(v.findings) ? v.findings : []));
for (const f of findings.filter((f) => f.severity === 'warning')) console.warn(`  ⚠ ${f.code}: ${f.message}`);
if (!check.ok) {
  for (const f of findings.filter((f) => f.severity === 'error')) console.error(`  ✗ ${f.code}: ${f.message}`);
  console.error('✗ HyperFrames kontrolü geçmedi');
  process.exit(1);
}
if (args.includes('--sadece-proje')) process.exit(0);

console.log(`▶ ${name}: kapak…`);
const snapDir = join(proj, '.hyperframes/kapak');
hf('snapshot', '--at', '1.2', '--no-end', '-o', snapDir);
const png = readdirSync(snapDir).find((f) => f.endsWith('.png'));
if (png) copyFileSync(join(snapDir, png), join(out, `${name}_kapak.png`));

console.log(`▶ ${name}: video…`);
hf('render', '-o', join(out, `${name}.mp4`), '-q', 'looks');
console.log(`✔ ${name} hazır: ${total.toFixed(1)} sn → out/${name}.mp4`);
if (total < 150 || total > 200) console.warn(`⚠ Süre 2,5–3,3 dk hedefinin dışında (${total.toFixed(1)} sn)`);
