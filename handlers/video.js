'use strict';

// /indir  <link>          -> videoyu indirip gönderir
// /altyazi [dil] [link]   -> bir videoya/sese yanıt olarak ya da linkle kullanılır;
//                            .srt dosyası ve altyazısı gömülü video gönderir

const path = require('path');
const { Composer } = require('telegraf');
const media = require('../lib/media');

const composer = new Composer();

// Telegram botları en fazla 20 MB'lık dosyaları indirebilir.
const TELEGRAM_DOWNLOAD_LIMIT = 20 * 1024 * 1024;
const MAX_QUEUE = Number(process.env.MAX_MEDIA_QUEUE || 5);

// Whisper ve FFmpeg CPU'yu yoğun kullandığı için işler sırayla çalıştırılır.
let queue = Promise.resolve();
let pending = 0;

// İş arka planda başlatılır; güncelleme işleyicisi beklemez. Aksi halde webhook
// yanıtı dakikalarca gecikir ve Telegram aynı mesajı yeniden gönderir.
function enqueue(ctx, job) {
    if (pending >= MAX_QUEUE) {
        ctx.reply('Şu an çok fazla istek var, lütfen biraz sonra tekrar deneyin.', replyTo(ctx)).catch(() => {});
        return;
    }
    if (pending > 0) {
        ctx.reply(`İsteğiniz sıraya alındı (önünüzde ${pending} iş var).`, replyTo(ctx)).catch(() => {});
    }
    pending++;
    queue = queue.then(() => runJob(ctx, job)).catch(err => console.log('Kuyruk hatası:', err));
}

async function runJob(ctx, job) {
    let dir = null;
    try {
        dir = await media.makeWorkDir();
        await job(dir);
    } catch (err) {
        if (err instanceof media.UserError) {
            await ctx.reply(`⚠️ ${err.message}`, replyTo(ctx)).catch(() => {});
        } else {
            console.log('Medya işlemi hatası:', err);
            await ctx.reply('⚠️ Beklenmeyen bir hata oluştu.', replyTo(ctx)).catch(() => {});
        }
    } finally {
        pending--;
        if (dir) await media.removeWorkDir(dir).catch(() => {});
    }
}

function replyTo(ctx) {
    return { reply_to_message_id: ctx.message.message_id };
}

function commandArgs(ctx) {
    return (ctx.message.text || '').trim().split(/\s+/).slice(1);
}

// Yanıtlanan mesajdaki video/ses dosyasını bulur.
function findAttachment(message) {
    if (!message) return null;
    const candidates = [
        message.video,
        message.video_note,
        message.audio,
        message.voice,
        message.animation
    ];
    const doc = message.document;
    if (doc && /^(video|audio)\//.test(doc.mime_type || '')) candidates.push(doc);
    return candidates.find(Boolean) || null;
}

composer.command('indir', ctx => {
    const url = commandArgs(ctx)[0];
    if (!url || !media.isHttpUrl(url)) {
        return ctx.reply('Kullanım: /indir <video bağlantısı>', replyTo(ctx));
    }

    enqueue(ctx, async dir => {
        const status = await ctx.reply('⏬ Video indiriliyor...', replyTo(ctx));
        ctx.replyWithChatAction('upload_video').catch(() => {});

        const file = await media.downloadVideo(url, dir);
        await ctx.replyWithVideo(
            { source: file, filename: path.basename(file) },
            Object.assign({ supports_streaming: true }, replyTo(ctx))
        );
        await ctx.deleteMessage(status.message_id).catch(() => {});
    });
});

composer.command('altyazi', ctx => {
    const args = commandArgs(ctx);
    let language = null;
    let url = null;
    for (const arg of args) {
        if (media.isHttpUrl(arg)) url = arg;
        else if (/^[a-z]{2,3}$/i.test(arg)) language = arg.toLowerCase();
    }

    const attachment = findAttachment(ctx.message.reply_to_message);
    if (!url && !attachment) {
        return ctx.reply(
            'Kullanım:\n' +
            '• Bir video veya sese yanıt olarak: /altyazi\n' +
            '• Bağlantıyla: /altyazi <video bağlantısı>\n' +
            'Dil belirtmek için: /altyazi tr (belirtilmezse otomatik algılanır)',
            replyTo(ctx)
        );
    }
    if (!url && attachment.file_size > TELEGRAM_DOWNLOAD_LIMIT) {
        return ctx.reply('Telegram botları en fazla 20 MB\'lık dosyaları indirebilir. Daha küçük bir dosya veya bağlantı gönderin.', replyTo(ctx));
    }

    enqueue(ctx, async dir => {
        const status = await ctx.reply('⏬ Dosya alınıyor...', replyTo(ctx));
        const edit = text => ctx.telegram
            .editMessageText(status.chat.id, status.message_id, undefined, text)
            .catch(() => {});

        let input;
        if (url) {
            input = await media.downloadVideo(url, dir);
        } else {
            const link = await ctx.telegram.getFileLink(attachment.file_id);
            const ext = path.extname(new URL(link).pathname) || '.bin';
            input = await media.downloadToFile(link, path.join(dir, 'kaynak' + ext));
        }

        await edit('📝 Altyazı çıkarılıyor... (bu işlem birkaç dakika sürebilir)');
        ctx.replyWithChatAction('typing').catch(() => {});
        const srt = await media.transcribe(input, dir, language);

        await ctx.replyWithDocument(
            { source: srt, filename: 'altyazi.srt' },
            replyTo(ctx)
        );

        const info = await media.probe(input);
        if (info.hasVideo) {
            await edit('🎬 Altyazı videoya ekleniyor...');
            ctx.replyWithChatAction('upload_video').catch(() => {});
            const burned = await media.burnSubtitles(input, srt, dir);
            if (await media.fileSize(burned) <= media.settings.maxUploadBytes) {
                await ctx.replyWithVideo(
                    { source: burned, filename: 'altyazili.mp4' },
                    Object.assign({ supports_streaming: true }, replyTo(ctx))
                );
            } else {
                await ctx.reply('Altyazılı video Telegram sınırını aştığı için gönderilemedi; .srt dosyasını kullanabilirsiniz.', replyTo(ctx));
            }
        }
        await ctx.deleteMessage(status.message_id).catch(() => {});
    });
});

module.exports = composer;
