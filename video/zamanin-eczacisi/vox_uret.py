#!/opt/voxcpm/bin/python
"""VoxCPM2 (Apache-2.0, ücretsiz) ile Türkçe seslendirme — Bölüm 4'ten itibaren.
Her karakter referans/<karakter>.wav (VoxCPM2 ile tasarlanmış yapay Türkçe ses) üzerinden klonlanır,
böylece ses bölümden bölüme aynı kalır. Duygu, metnin başına eklenen İngilizce talimatla verilir;
bağırma talimatları ölçülü karşılıklarına çevrilir.
Kullanım: vox_uret.py bolum4 bolum5 ...   (çıktı ses6/, var olanlar atlanır; SEED_EK ile farklı tohum)
DUZEN=1 (2. sezon varsayılanı): hızı karakter bandının çok dışında kalan replik 3 tohuma kadar denenir,
en dengelisi seçilir ve duzen.py ile hız/seviye/tını düzenlenir. Ham çıktı ses_ham/ altında saklanır.
"""
import importlib, os, re, subprocess, sys, time
import soundfile as sf
import torch
from num2words import num2words
from voxcpm import VoxCPM

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, os.environ.get('SES_DIR', 'ses6'))
REF = os.path.join(ROOT, 'referans')
SAYI = {'1665': 'bin altı yüz altmış beş', '2026': 'iki bin yirmi altı'}
sys.path.insert(0, ROOT)
from duzen import duzenle, hece, hiz_bandi
DUZEN = os.environ.get('DUZEN', '1') == '1'
HAM = os.path.join(ROOT, 'ses_ham')
os.makedirs(HAM, exist_ok=True)

# Bağırma yok: yüksek sesli talimatları ölçülü karşılıklarına çevir
YUMUSAT = [
    (r'\b(shouting|yelling|screaming|loud)\b', 'intense, firm, raised voice but not shouting'),
    (r'\bwhisper(ing)?\b', 'quiet breathy whisper, speaking slowly and clearly'),
    (r'\bpanick?ed\b', 'urgent, worried, fast'),
    (r'\bangry\b', 'angry but controlled'),
]


def stil_yaz(style):
    s = (style or 'natural, conversational').lower()
    for pat, rep in YUMUSAT:
        s = re.sub(pat, rep, s)
    return s + ', natural Turkish speech'


def hedef_lufs(style):
    s = (style or '').lower()
    if any(w in s for w in ('whisper', 'quiet', 'soft', 'weak', 'sleepy', 'praying', 'to himself', 'calm')):
        return -22
    if any(w in s for w in ('angry', 'shout', 'loud', 'commanding', 'panick', 'urgent', 'shock')):
        return -19
    return -20


def sayi_yaz(m):
    return SAYI.get(m.group()) or num2words(int(m.group()), lang='tr')


torch.set_num_threads(os.cpu_count() or 4)
os.makedirs(OUT, exist_ok=True)
model = VoxCPM.from_pretrained('openbmb/VoxCPM2', load_denoiser=False, optimize=False, device='cpu')
sr = model.tts_model.sample_rate
for ep in sys.argv[1:]:
    mod = importlib.import_module(ep)
    for key, spec in mod.LINES.items():
        if len(spec) < 5:
            # kanca (h0): kesmek yerine aynı karakter ve duyguyla ayrı seslendirilir
            hc = getattr(mod, 'HOOK_CUT', None)
            if not hc or hc[2] != key or not os.environ.get('KANCA_TTS', '1') == '1':
                continue
            kaynak = mod.LINES[hc[0]]
            spec = (spec[0], spec[1], spec[2], spec[3], kaynak[4], kaynak[5] if len(kaynak) > 5 else '')
        fname, who, text = spec[:3]
        dst = os.path.join(OUT, fname)
        if os.path.exists(dst):
            continue
        style = spec[5] if len(spec) > 5 else ''
        clean = re.sub(r'\d+', sayi_yaz, text.replace('"', ''))
        seed0 = sum(map(ord, fname)) + int(os.environ.get('SEED_EK', '0'))
        t = time.time()
        alt, ust = hiz_bandi(who, style)
        en_iyi = None
        for d in range(3 if DUZEN else 1):
            torch.manual_seed(seed0 + d * 7919)
            wav = model.generate(text=f'({stil_yaz(style)}){clean}',
                                 reference_wav_path=os.path.join(REF, f'{who}.wav'),
                                 cfg_value=2.0, inference_timesteps=10)
            # konuşma süresi (baş/son sessizlik hariç kaba ölçüm)
            import numpy as np
            a = np.abs(wav); ses = np.where(a > a.max() * 0.03)[0]
            konusma = (ses[-1] - ses[0]) / sr if len(ses) else len(wav) / sr
            hiz = hece(clean) / max(0.3, konusma)
            sapma = max(0.0, alt * 0.88 - hiz, hiz - ust * 1.12)
            if en_iyi is None or sapma < en_iyi[0]:
                en_iyi = (sapma, wav, hiz)
            if sapma == 0:
                break
        raw = os.path.join(HAM, fname)
        sf.write(raw, en_iyi[1], sr)
        if DUZEN:
            _, tempo = duzenle(raw, dst, clean, who, style)
        else:
            tempo = 1.0
            flt = ('silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
                   f'loudnorm=I={hedef_lufs(style)}:TP=-2:LRA=11,aresample=24000')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', flt, '-ac', '1', dst], check=True)
        print(f'{fname} {who} hız={en_iyi[2]:.1f} deneme={d + 1} tempo={tempo}', end=' ')
        print(f'{time.time() - t:.0f}s', flush=True)
print('TAMAM', flush=True)
