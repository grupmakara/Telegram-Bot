'use strict';

// /ses <metin>  → metni OmniVoice ile seslendirip sesli mesaj olarak gönderir.
// Bir mesaja yanıt olarak /ses yazılırsa o mesajın metnini okur.
//
// Ortam değişkenleri:
//   OMNIVOICE_PYTHON   OmniVoice kurulu Python (varsayılan: /opt/omnivoice/bin/python)
//   OMNIVOICE_INSTRUCT Ses tarifi, ör. "female", "male, elderly" (varsayılan: female)
//   TTS_MAX_CHARS      Tek istekte en fazla karakter (varsayılan: 300)

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { spawn } = require('child_process');
const Composer = require('telegraf/composer');

const PYTHON = process.env.OMNIVOICE_PYTHON || '/opt/omnivoice/bin/python';
const WORKER = path.join(__dirname, '..', 'tts', 'omnivoice_worker.py');
const MAX_CHARS = parseInt(process.env.TTS_MAX_CHARS, 10) || 300;
const TIMEOUT_MS = 5 * 60 * 1000;

let worker = null;
let ready = null;
let nextId = 1;
const pending = new Map();

function failAll(err) {
    for (const p of pending.values()) {
        clearTimeout(p.timer);
        p.reject(err);
    }
    pending.clear();
}

function startWorker() {
    if (ready) return ready;
    ready = new Promise((resolve, reject) => {
        worker = spawn(PYTHON, [WORKER], { stdio: ['pipe', 'pipe', 'inherit'] });
        worker.on('error', (err) => {
            reject(err);
            failAll(err);
            worker = null;
            ready = null;
        });
        worker.on('exit', (code) => {
            const err = new Error(`OmniVoice işçisi kapandı (kod ${code})`);
            reject(err);
            failAll(err);
            worker = null;
            ready = null;
        });
        readline.createInterface({ input: worker.stdout }).on('line', (line) => {
            let msg;
            try { msg = JSON.parse(line); } catch (e) { return; }
            if (msg.ready) {
                console.log(`OmniVoice hazır (${msg.device})`);
                return resolve();
            }
            const p = pending.get(msg.id);
            if (!p) return;
            pending.delete(msg.id);
            clearTimeout(p.timer);
            if (msg.error) p.reject(new Error(msg.error));
            else p.resolve(msg.path);
        });
    });
    return ready;
}

async function synthesize(text) {
    await startWorker();
    const id = nextId++;
    return new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
            pending.delete(id);
            reject(new Error('Seslendirme zaman aşımına uğradı'));
        }, TIMEOUT_MS);
        pending.set(id, { resolve, reject, timer });
        const req = { id, text };
        if (process.env.OMNIVOICE_INSTRUCT !== undefined) req.instruct = process.env.OMNIVOICE_INSTRUCT;
        worker.stdin.write(JSON.stringify(req) + '\n');
    });
}

module.exports = Composer.command('ses', async (ctx, next) => {
    const msg = ctx.message;
    let text = (msg.text || '').replace(/^\/ses(@\w+)?\s*/i, '').trim();
    if (!text && msg.reply_to_message) {
        text = (msg.reply_to_message.text || msg.reply_to_message.caption || '').trim();
    }
    if (!text) {
        await ctx.reply('Kullanım: /ses <metin> ya da bir mesaja yanıt olarak /ses');
        return next();
    }
    if (text.length > MAX_CHARS) {
        await ctx.reply(`Metin çok uzun, en fazla ${MAX_CHARS} karakter.`);
        return next();
    }

    ctx.replyWithChatAction('record_voice').catch(() => {});
    try {
        const file = await synthesize(text);
        await ctx.replyWithVoice({ source: fs.createReadStream(file) }, { reply_to_message_id: msg.message_id });
        fs.unlink(file, () => {});
    } catch (err) {
        console.log('Seslendirme hatası:', err.message);
        await ctx.reply('Seslendirme şu an yapılamadı.');
    }
    return next();
});

// Model ilk istekte değil, bot açılırken yüklensin (ilk yanıt gecikmesin).
startWorker().catch((err) => console.log('OmniVoice başlatılamadı:', err.message));
