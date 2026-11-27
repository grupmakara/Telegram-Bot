#!/opt/tts/bin/python
"""Chatterbox Multilingual (MIT) ile Türkçe seslendirme.
Her karakter, referans/<karakter>.wav içindeki Türkçe tasarlanmış yapay sesten konuşur.
Duygu yoğunluğu ölçülü tutulur (bağırma yok); ses seviyesi duyguya göre ayarlanır.
Kullanım: cb_uret.py bolum3 bolum4 ...   (var olan dosyaları atlar; SEED_EK ile farklı örnek)
"""
import importlib, os, re, subprocess, sys, time
import torch, torchaudio
from num2words import num2words
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'ses5')
REF = os.path.join(ROOT, 'referans')
SAYI = {'1665': 'bin altı yüz altmış beş', '360': 'üç yüz altmış'}
sys.path.insert(0, ROOT)
from vox_uret_stil import STYLE  # Bölüm 1-3 duygu yönlendirmeleri


def sayi_yaz(m):
    return SAYI.get(m.group()) or num2words(int(m.group()), lang='tr')


def hedef_lufs(style):
    s = (style or '').lower()
    if any(w in s for w in ('whisper', 'quiet', 'soft', 'weak', 'sleepy', 'praying', 'to himself', 'calm')):
        return -24
    if any(w in s for w in ('angry', 'shout', 'loud', 'commanding', 'panick', 'urgent', 'shock')):
        return -18
    return -20


torch.set_num_threads(4)
os.makedirs(OUT, exist_ok=True)
model = ChatterboxMultilingualTTS.from_pretrained(device='cpu')
for ep in sys.argv[1:]:
    for key, spec in importlib.import_module(ep).LINES.items():
        if len(spec) < 5:
            continue
        fname, who, text, _est, exag = spec[:5]
        dst = os.path.join(OUT, fname)
        if os.path.exists(dst):
            continue
        style = (spec[5] if len(spec) > 5 else None) or STYLE.get(fname, '')
        # 0.35..1.0 aralığındaki senaryo yoğunluğunu ölçülü 0.35..0.7 aralığına indir
        ex = round(min(0.7, max(0.35, 0.35 + (exag - 0.35) * 0.55)), 2)
        clean = re.sub(r'\d+', sayi_yaz, text.replace('"', ''))
        seed = sum(map(ord, fname)) + int(os.environ.get('SEED_EK', '0'))
        torch.manual_seed(seed)
        t = time.time()
        wav = model.generate(clean, language_id='tr', audio_prompt_path=os.path.join(REF, f'{who}.wav'),
                             exaggeration=ex, cfg_weight=0.45 if ex >= 0.6 else 0.5, temperature=0.7)
        raw = dst + '.raw.wav'
        torchaudio.save(raw, wav, model.sr)
        flt = ('silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
               f'loudnorm=I={hedef_lufs(style)}:TP=-2:LRA=11,aresample=24000')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', flt, '-ac', '1', dst], check=True)
        os.remove(raw)
        print(f'{fname} {who} ex={ex} {time.time() - t:.0f}s', flush=True)
print('TAMAM', flush=True)
