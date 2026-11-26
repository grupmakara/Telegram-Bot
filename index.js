require("dotenv").config();

const BOT_API       = process.env.BOT_API || '';
const PORT          = process.env.PORT || 3000;
// URL verilirse webhook, verilmezse polling kullanılır (domain'i olmayan sunucular için).
const URL           = process.env.URL || '';

const Telegraf  = require("telegraf");
const bot       = new Telegraf(BOT_API);

const config = require('./config');

async function SendMessage(message) {
    await bot.telegram.sendMessage(config.chat_id, `${message}`, { parse_mode: 'HTML'});
}

var AutoPost = function() {
  SendMessage('Test123')
}

var CronJob = require('cron').CronJob;
new CronJob({
  cronTime: "*/2 * * * *",
  onTick: AutoPost,
  start: true,
  timeZone: "Europe/Moscow"
})

bot.start((ctx) => {
    return ctx.reply("Hey");
});

bot.hears(/selam/ig, async (ctx, next) => {
        ctx.telegram.sendPhoto(ctx.chat.id, 'https://www.ajanskirim.com/wp-content/uploads/2019/03/1525995635Merhaba.jpg', { caption:  `<b>${ctx.from.first_name}</b>`,  parse_mode: 'HTML' })
    return next();
});

bot.command('komut', async (ctx, next) => {
    ctx.telegram.sendMessage(ctx.chat.id, `<b>${ctx.from.first_name}</b>`, { parse_mode: 'HTML' })
    return next();
});


bot.use(require('./handlers/video'));

bot.use(
    require('./handlers/middlewares'),
    require('./plugin')
);


bot.telegram.getMe().then(me => {
    console.log(`Bot Başlatıldı! => ${me.username}`);
}).catch(err => console.log('Bot bilgisi alınamadı:', err.message));


bot.catch((err) => {
    console.log('Error: ', err)
})

if (URL) {
  bot.launch({
    webhook: {
      domain: `${URL}`,
      port: `${PORT}`
    }
  })
} else {
  // Daha önce ayarlanmış bir webhook varsa polling çalışmaz; önce onu kaldır.
  bot.telegram.deleteWebhook()
    .then(() => bot.launch())
    .catch(err => {
      // Çıkış kodu sayesinde Docker/systemd botu yeniden başlatır.
      console.log('Telegram\'a bağlanılamadı:', err.message)
      process.exit(1)
    })
  console.log('URL tanımlı değil, polling modunda çalışılıyor.')
}
