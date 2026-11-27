#!/usr/bin/env python3
"""Hikâye / bölüm seslendirici (VoxCPM2, Türkçe, duygulu).

Kullanım:
    /opt/voxcpm/bin/python tts/hikaye_seslendir.py bolum1.txt -o bolum1.mp3

Senaryo dosyası biçimi:

    # '#' ile başlayan satırlar yorumdur.
    # Karakterler: @ad: sesin İngilizce tarifi (bir kez tanımlanır)
    @anlatici: Middle-aged man, warm deep voice, calm storyteller
    @elif: Young girl, bright cheerful voice

    # Replikler: ad [duygu]: metin      (duygu isteğe bağlı)
    anlatici [sakin]: Bir zamanlar küçük bir köyde Elif adında bir kız yaşarmış.
    elif [mutlu]: Bugün hava ne kadar güzel!
    elif [fısıltı]: Sana bir sır vereceğim, kimseye söyleme.

Duygu olarak aşağıdaki Türkçe anahtarlardan biri ya da doğrudan İngilizce bir
tarif ("nervous, stuttering") yazılabilir.

Karakter sesleri tts/sesler/<ad>.wav olarak saklanır ve sonraki bölümlerde
aynen yeniden kullanılır; böylece karakterlerin sesi bölümden bölüme değişmez.
Yeni bir ses istemek için o dosyayı silin.

Her replik Whisper ile yazıya çevrilip metinle karşılaştırılır; tutmazsa farklı
tohumla yeniden üretilir (varsayılan en fazla 4 deneme) ve en iyi sonuç kalır.
"""
import argparse
import difflib
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf
import torch

DUYGULAR = {
    "sakin": "calm, neutral, steady pace",
    "anlatıcı": "warm storytelling tone, expressive, steady pace",
    "mutlu": "very happy and cheerful, smiling",
    "heyecanlı": "excited, energetic, fast",
    "coşkulu": "very excited and joyful, enthusiastic",
    "üzgün": "sad, crying softly, slow",
    "ağlamaklı": "on the verge of tears, trembling voice, slow",
    "öfkeli": "angry, shouting",
    "sinirli": "irritated, annoyed, sharp",
    "korkmuş": "scared, frightened, trembling, fast breathing",
    "şaşkın": "surprised, astonished",
    "fısıltı": "quiet breathy whisper, mysterious, speaking slowly and clearly",
    "gizemli": "mysterious, low voice, slow",
    "alaycı": "sarcastic, mocking",
    "yorgun": "tired, exhausted, slow",
    "sevecen": "tender, loving, soft",
    "kararlı": "determined, confident, firm",
}
TR_ASCII = str.maketrans("ıİşŞğĞüÜöÖçÇ", "iIsSgGuUoOcC")
# Anahtarlar Türkçe karaktersiz de yazılabilsin (uzgun, ofkeli, fisilti...)
DUYGULAR.update({k.translate(TR_ASCII): v for k, v in list(DUYGULAR.items())})

SESLER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sesler")
REF_METIN = ("Merhaba, bu benim sesim. Bugün size güzel bir hikâye anlatacağım; "
             "dikkatle dinlerseniz çok seveceksiniz.")
SATIR_RE = re.compile(r"^\s*([\wçğıöşüÇĞİÖŞÜ-]+)\s*(?:\[([^\]]*)\])?\s*:\s*(.+)$")


def oku(yol):
    karakterler, replikler = {}, []
    with open(yol, encoding="utf-8") as f:
        for no, satir in enumerate(f, 1):
            satir = satir.strip()
            if not satir or satir.startswith("#"):
                continue
            if satir.startswith("@"):
                ad, _, tarif = satir[1:].partition(":")
                karakterler[ad.strip().lower()] = tarif.strip()
                continue
            m = SATIR_RE.match(satir)
            if not m:
                sys.exit(f"{yol}:{no}: satır anlaşılamadı: {satir}")
            ad, duygu, metin = m.group(1).lower(), (m.group(2) or "").strip(), m.group(3).strip()
            if ad not in karakterler:
                sys.exit(f"{yol}:{no}: '{ad}' karakteri tanımlı değil (@{ad}: ... ekleyin)")
            replikler.append((ad, duygu, metin))
    if not replikler:
        sys.exit("Senaryoda replik yok.")
    return karakterler, replikler


def normal(s):
    s = s.lower().replace("â", "a").replace("î", "i").replace("û", "u")
    return " ".join("".join(c if c.isalnum() else " " for c in s).split())


def benzerlik(a, b):
    return difflib.SequenceMatcher(None, normal(a).split(), normal(b).split()).ratio()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("senaryo")
    ap.add_argument("-o", "--cikti", help="çıktı dosyası (.mp3 veya .wav)")
    ap.add_argument("--deneme", type=int, default=4, help="replik başına en fazla deneme")
    ap.add_argument("--esik", type=float, default=0.99, help="kabul için Whisper kelime benzerliği eşiği (1 = birebir)")
    ap.add_argument("--ara", type=float, default=0.45, help="replikler arası sessizlik (sn)")
    ap.add_argument("--whisper", default="small", help="kontrol için Whisper modeli")
    a = ap.parse_args()
    cikti = a.cikti or os.path.splitext(a.senaryo)[0] + ".mp3"

    karakterler, replikler = oku(a.senaryo)
    torch.set_num_threads(os.cpu_count() or 1)
    from voxcpm import VoxCPM
    import whisper

    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False, device="cpu")
    sr = model.tts_model.sample_rate
    asr = whisper.load_model(a.whisper)

    def dinle(wav):
        with tempfile.NamedTemporaryFile(suffix=".wav") as t:
            sf.write(t.name, wav, sr)
            return asr.transcribe(t.name, language="tr")["text"].strip()

    def uret(metin, ref=None):
        en_iyi = (-1.0, None, "")
        for deneme in range(1, a.deneme + 1):
            torch.manual_seed(deneme)
            wav = model.generate(text=metin, reference_wav_path=ref, cfg_value=2.0, inference_timesteps=10)
            duyulan = dinle(wav)
            puan = benzerlik(re.sub(r"^\([^)]*\)", "", metin), duyulan)
            if puan > en_iyi[0]:
                en_iyi = (puan, wav, duyulan)
            if puan >= a.esik:
                break
        return en_iyi, deneme

    # 1) Karakter sesleri: yoksa tasarla ve sakla
    os.makedirs(SESLER_DIR, exist_ok=True)
    refler = {}
    for ad in sorted({r[0] for r in replikler}):
        yol = os.path.join(SESLER_DIR, f"{ad}.wav")
        if not os.path.exists(yol):
            print(f"[ses] '{ad}' için yeni ses tasarlanıyor: {karakterler[ad]}", flush=True)
            (puan, wav, _), _ = uret(f"({karakterler[ad]}, clear articulation){REF_METIN}")
            sf.write(yol, wav, sr)
        refler[ad] = yol

    # 2) Replikler
    ara = np.zeros(int(sr * a.ara), dtype=np.float32)
    parcalar, sorunlu = [], []
    for i, (ad, duygu, metin) in enumerate(replikler, 1):
        stil = DUYGULAR.get(duygu.lower(), duygu) if duygu else ""
        girdi = f"({stil}){metin}" if stil else metin
        (puan, wav, duyulan), deneme = uret(girdi, refler[ad])
        durum = "OK" if puan >= a.esik else "KONTROL ET"
        if puan < a.esik:
            sorunlu.append((i, metin, duyulan))
        print(f"[{i}/{len(replikler)}] {durum} {ad}[{duygu or '-'}] puan={puan:.2f} deneme={deneme} | {duyulan}", flush=True)
        parcalar += [wav.astype(np.float32), ara]

    ses = np.concatenate(parcalar[:-1])
    if cikti.lower().endswith(".wav"):
        sf.write(cikti, ses, sr)
    else:
        with tempfile.NamedTemporaryFile(suffix=".wav") as t:
            sf.write(t.name, ses, sr)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", t.name, "-b:a", "192k", cikti], check=True)
    print(f"\nBitti: {cikti} ({len(ses) / sr:.1f} sn)")
    if sorunlu:
        print("Whisper'ın tam doğrulayamadığı replikler (dinleyip kontrol edin):")
        for i, metin, duyulan in sorunlu:
            print(f"  {i}. beklenen: {metin}\n     duyulan : {duyulan}")


if __name__ == "__main__":
    main()
