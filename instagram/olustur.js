const {chromium}=require('playwright');const fs=require('fs');
const P=[
["de","afspraak","randevu","Ik heb morgen een afspraak bij de huisarts.","Yarın aile hekiminde randevum var.","<b>een afspraak maken</b> = randevu almak<br><b>een afspraak afzeggen</b> = randevuyu iptal etmek"],
["","gezellig","samimi, keyifli, hoş","Het was gisteren erg gezellig bij jullie.","Dün sizde çok keyifliydi.","Hollanda kültürünün en sevilen kelimesi. Tam Türkçe karşılığı yok: sıcak, samimi, keyifli ortam."],
["de","huisarts","aile hekimi","Als je ziek bent, bel je eerst de huisarts.","Hasta olduğunda önce aile hekimini ararsın.","Hollanda'da ilk durak huisarts'tır. Hayati tehlikede <b>112</b>'yi ara."],
["","regelen","halletmek, ayarlamak","Geen zorgen, ik regel het vandaag.","Merak etme, bugün hallediyorum.","<b>Dat is geregeld!</b> = Hallettik, tamamdır!"],
["de","boodschappen","market alışverişi","Ik doe elke zaterdag boodschappen.","Her cumartesi market alışverişi yaparım.","<b>boodschappen doen</b> kalıp olarak öğren. Hep çoğul kullanılır."],
["","opstaan","kalkmak","Ik sta elke dag om zes uur op.","Her gün saat altıda kalkarım.","Ayrılabilen fiil: <b>sta … op</b>. Modal fiille birleşir: Ik moet vroeg <b>opstaan</b>."],
["de","vertraging","gecikme","De trein heeft twintig minuten vertraging.","Trenin yirmi dakika gecikmesi var.","Tren ve otobüs duyurularında çok sık duyarsın. Dinleme sınavında da çıkar!"],
["","beschikbaar","müsait","Bent u morgen beschikbaar voor een gesprek?","Yarın bir görüşme için müsait misiniz?","İş görüşmelerinde ve resmi e-postalarda sık kullanılır."],
["","eigenlijk","aslında","Eigenlijk wil ik liever thuisblijven.","Aslında evde kalmayı tercih ederim.","Hollandalılar bu kelimeyi konuşmada sürekli kullanır. Sen de kullan, daha doğal konuşursun."],
["de","rekening","hesap, fatura","Mag ik de rekening, alstublieft?","Hesabı alabilir miyim, lütfen?","Restoranda hesap isterken. Ev faturası için de: <b>de energierekening</b>."],
["","verhuizen","taşınmak","Wij verhuizen volgende maand naar Utrecht.","Gelecek ay Utrecht'e taşınıyoruz.","Geçmiş zamanı <b>zijn</b> ile kurulur: Wij <b>zijn</b> verhuisd."],
["","lekker","lezzetli, güzel, hoş","Wat ruikt dat lekker!","Ne güzel kokuyor!","Sadece yemek için değil: <b>lekker weer</b> (güzel hava), <b>lekker geslapen</b> (iyi uyudum)."],
["de","buren","komşular","Onze buren zijn heel vriendelijk.","Komşularımız çok cana yakın.","Tekil: <b>de buurman</b> (erkek komşu), <b>de buurvrouw</b> (kadın komşu)."],
["","proberen","denemek, çalışmak","Ik probeer elke dag Nederlands te spreken.","Her gün Hollandaca konuşmaya çalışıyorum.","Yapı: <b>proberen + te + mastar</b>. Modal fiillerde te kullanılmaz!"]];
const css=`*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;font-family:Inter,system-ui,sans-serif;background:#f3f5f9;color:#18202e}
.wrap{position:absolute;inset:0;padding:80px 84px;display:flex;flex-direction:column;gap:44px}
.top{display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:30px;letter-spacing:.06em;text-transform:uppercase;color:#1f4d8f}
.day{background:#e4640e;color:#fff;border-radius:999px;padding:12px 30px;letter-spacing:.04em}
.word{background:#1f4d8f;color:#fff;border-radius:44px;padding:64px 64px 58px;display:flex;flex-direction:column;gap:14px}
.art{font-size:40px;font-weight:600;color:#ffb27a}
.w{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:128px;line-height:1;letter-spacing:-.02em;white-space:nowrap}
.tr{font-size:46px;font-weight:500;opacity:.92}
.lbl{font-size:26px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#5b6578}
.ex{display:flex;flex-direction:column;gap:14px;border-left:8px solid #e4640e;padding-left:34px}
.nl{font-size:48px;font-weight:600;line-height:1.25}.ext{font-size:38px;color:#5b6578;line-height:1.3}
.tip{margin-top:auto;background:#fde9da;border-radius:32px;padding:36px 40px;font-size:34px;line-height:1.4}
.tip b{color:#c2510a}.tip .h{font-weight:700;color:#e4640e;font-size:26px;letter-spacing:.1em;text-transform:uppercase;display:block;margin-bottom:8px}
.foot{display:flex;justify-content:space-between;font-size:26px;color:#5b6578;font-weight:500}`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
let cap="";
for(let i=0;i<P.length;i++){const [a,w,tr,nl,ext,tip]=P[i];const d=String(i+1).padStart(2,'0');
const html=`<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Inter:wght@400;500;600;700&display=swap"><style>${css}</style></head><body><div class="wrap">
<div class="top"><span>Günün kelimesi</span><span class="day">Dag ${i+1}</span></div>
<div class="word">${a?`<span class="art">${a}</span>`:`<span class="art">${/en$/.test(w)?'werkwoord · fiil':'woord · kelime'}</span>`}<span class="w">${w}</span><span class="tr">${tr}</span></div>
<div class="lbl">Voorbeeldzin · Örnek cümle</div>
<div class="ex"><span class="nl">${nl}</span><span class="ext">${ext}</span></div>
<div class="tip"><span class="h">İpucu</span>${tip}</div>
<div class="foot"><span>Hollandaca · A2 → B1</span><span>Kaydet ve tekrar et ↻</span></div></div></body></html>`;
await p.setContent(html,{waitUntil:'networkidle'});await p.evaluate(()=>{const e=document.querySelector('.w');let s=128;while(e.scrollWidth>e.clientWidth&&s>60){s-=4;e.style.fontSize=s+'px';}});await p.screenshot({path:`gun-${d}-${w}.png`});
const plain=t=>t.replace(/<br>/g,"\n").replace(/<[^>]+>/g,"");
cap+=`===== GÜN ${i+1}: ${a?a+" ":""}${w} =====\n🇳🇱 Günün kelimesi: ${a?a+" ":""}${w}\n🇹🇷 Anlamı: ${tr}\n\n📌 ${nl}\n➡️ ${ext}\n\n💡 ${plain(tip)}\n\nSen de bu kelimeyle bir cümle kur ve yorumlara yaz 👇 Düzeltmeye yardım edelim!\n\n#hollandaca #nederlandsleren #hollandacaöğren #inburgering #inburgeringsexamen #nt2 #staatsexamennt2 #hollandadayaşam #nederland #dutch #learndutch #günlükkelime #woordvandedag\n\n`;}
fs.writeFileSync('aciklamalar.txt',cap);
console.log(await p.evaluate(()=>document.fonts.check('800 40px "Bricolage Grotesque"')));await b.close();})();
