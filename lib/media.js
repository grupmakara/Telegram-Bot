'use strict';

// Video indirme (yt-dlp), altyazı çıkarma (Whisper) ve altyazı gömme (FFmpeg)
// işlemleri. Telegram'dan bağımsızdır; tüm komutlar shell kullanmadan execFile
// ile çalıştırılır, böylece kullanıcı girdisi komut olarak yorumlanamaz.

const { execFile } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const http = require('http');
const https = require('https');

const MB = 1024 * 1024;

const settings = {
    // Telegram botları en fazla 50 MB dosya gönderebilir.
    maxUploadBytes: Number(process.env.MAX_UPLOAD_MB || 50) * MB,
    whisperModel: process.env.WHISPER_MODEL || 'base',
    // CPU'da Whisper yavaştır; çok uzun kayıtları reddet.
    maxSubtitleSeconds: Number(process.env.MAX_SUBTITLE_MINUTES || 10) * 60,
    downloadTimeoutMs: 10 * 60 * 1000,
    whisperTimeoutMs: 30 * 60 * 1000,
    ffmpegTimeoutMs: 20 * 60 * 1000
};

class UserError extends Error {}

function run(cmd, args, options) {
    return new Promise((resolve, reject) => {
        execFile(cmd, args, Object.assign({ maxBuffer: 20 * MB }, options), (err, stdout, stderr) => {
            if (err) {
                err.stderr = String(stderr || '');
                return reject(err);
            }
            resolve(String(stdout || ''));
        });
    });
}

function makeWorkDir() {
    return fs.promises.mkdtemp(path.join(os.tmpdir(), 'tgbot-'));
}

function removeWorkDir(dir) {
    return fs.promises.rm
        ? fs.promises.rm(dir, { recursive: true, force: true })
        : fs.promises.rmdir(dir, { recursive: true });
}

function isHttpUrl(text) {
    try {
        const u = new URL(text);
        return u.protocol === 'http:' || u.protocol === 'https:';
    } catch (e) {
        return false;
    }
}

async function findFile(dir, prefix) {
    const names = await fs.promises.readdir(dir);
    const match = names.find(n => n.startsWith(prefix + '.') && !n.endsWith('.part'));
    return match ? path.join(dir, match) : null;
}

async function fileSize(file) {
    return (await fs.promises.stat(file)).size;
}

// Bir bağlantıdaki videoyu yt-dlp ile indirir ve dosya yolunu döndürür.
async function downloadVideo(url, dir) {
    if (!isHttpUrl(url)) throw new UserError('Geçerli bir http(s) bağlantısı gönderin.');

    const limit = Math.floor(settings.maxUploadBytes / MB);
    const args = [
        '--no-playlist',
        '--no-warnings',
        '--quiet',
        '--compat-options', 'no-certifi',
        '-f', `b[ext=mp4][filesize<${limit}M]/bv*[ext=mp4][filesize<${limit}M]+ba[ext=m4a]/b[filesize<${limit}M]/b`,
        '--merge-output-format', 'mp4',
        '--max-filesize', `${limit}M`,
        '-o', path.join(dir, 'video.%(ext)s'),
        '--', url
    ];

    try {
        await run('yt-dlp', args, { timeout: settings.downloadTimeoutMs });
    } catch (err) {
        console.log('yt-dlp hata:', err.stderr || err.message);
        throw new UserError('Video indirilemedi. Bağlantıyı kontrol edin veya site desteklenmiyor olabilir.');
    }

    const file = await findFile(dir, 'video');
    if (!file) throw new UserError(`Video bulunamadı ya da ${limit} MB sınırını aşıyor.`);
    if (await fileSize(file) > settings.maxUploadBytes) {
        throw new UserError(`Video ${limit} MB sınırını aşıyor, Telegram'a gönderilemez.`);
    }
    return file;
}

// Telegram'ın verdiği dosya bağlantısını diske indirir.
function downloadToFile(url, dest) {
    return new Promise((resolve, reject) => {
        const client = url.startsWith('https:') ? https : http;
        const req = client.get(url, res => {
            if (res.statusCode !== 200) {
                res.resume();
                return reject(new Error(`İndirme başarısız: HTTP ${res.statusCode}`));
            }
            const out = fs.createWriteStream(dest);
            res.pipe(out);
            out.on('finish', () => out.close(() => resolve(dest)));
            out.on('error', reject);
        });
        req.on('error', reject);
        req.setTimeout(settings.downloadTimeoutMs, () => req.destroy(new Error('İndirme zaman aşımına uğradı')));
    });
}

async function probe(file) {
    const out = await run('ffprobe', [
        '-v', 'error',
        '-show_entries', 'format=duration:stream=codec_type',
        '-of', 'json',
        file
    ]);
    const data = JSON.parse(out);
    const types = (data.streams || []).map(s => s.codec_type);
    return {
        duration: Number((data.format && data.format.duration) || 0),
        hasVideo: types.includes('video'),
        hasAudio: types.includes('audio')
    };
}

// Whisper ile .srt altyazı dosyası üretir ve yolunu döndürür.
async function transcribe(input, dir, language) {
    const info = await probe(input);
    if (!info.hasAudio) throw new UserError('Bu dosyada ses yok, altyazı çıkarılamaz.');
    if (info.duration > settings.maxSubtitleSeconds) {
        const max = Math.round(settings.maxSubtitleSeconds / 60);
        throw new UserError(`Kayıt çok uzun. En fazla ${max} dakikalık kayıtlar için altyazı çıkarılabilir.`);
    }

    const args = [
        input,
        '--model', settings.whisperModel,
        '--output_format', 'srt',
        '--output_dir', dir,
        '--fp16', 'False',
        '--verbose', 'False'
    ];
    if (language) args.push('--language', language);

    try {
        await run('whisper', args, { timeout: settings.whisperTimeoutMs });
    } catch (err) {
        console.log('whisper hata:', err.stderr || err.message);
        throw new UserError('Altyazı çıkarılırken bir hata oluştu.');
    }

    const srt = path.join(dir, path.basename(input, path.extname(input)) + '.srt');
    if (!fs.existsSync(srt) || (await fileSize(srt)) === 0) {
        throw new UserError('Kayıtta anlaşılır bir konuşma bulunamadı.');
    }
    return srt;
}

// Altyazıyı videonun görüntüsüne gömer (hardsub). FFmpeg dosya yollarındaki
// özel karakterlerden etkilenmesin diye göreli dosya adlarıyla çalışılır.
async function burnSubtitles(video, srt, dir) {
    const output = path.join(dir, 'altyazili.mp4');
    const subName = 'burn.srt';
    await fs.promises.copyFile(srt, path.join(dir, subName));

    try {
        await run('ffmpeg', [
            '-y', '-v', 'error',
            '-i', video,
            '-vf', `subtitles=${subName}:force_style='Fontsize=22,Outline=2,MarginV=30'`,
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23',
            '-c:a', 'aac',
            '-movflags', '+faststart',
            output
        ], { cwd: dir, timeout: settings.ffmpegTimeoutMs });
    } catch (err) {
        console.log('ffmpeg hata:', err.stderr || err.message);
        throw new UserError('Altyazı videoya eklenemedi.');
    }
    return output;
}

module.exports = {
    settings,
    UserError,
    makeWorkDir,
    removeWorkDir,
    isHttpUrl,
    downloadVideo,
    downloadToFile,
    probe,
    transcribe,
    burnSubtitles,
    fileSize
};
