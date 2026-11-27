#!/usr/bin/env python3
"""Hikâye / bölüm seslendirici (Türkçe, duygulu).

Motorlar (--motor):
  voxcpm  (varsayılan) VoxCPM2 (VoiceStudio motoru) — yerel, tamamen ücretsiz, Apache-2.0
  gemini  Gemini 3.1 Flash TTS — Google API; ücretsiz kota günde 10 istek
  ikisi   her replik iki motorla üretilir, Whisper'ın daha doğru bulduğu kalır

Kullanım:
    /opt/voxcpm/bin/python tts/hikaye_seslendir.py bolum1.txt -o bolum1.mp3
    /opt/voxcpm/bin/python tts/hikaye_seslendir.py bolum1.txt --motor gemini

Senaryo dosyası biçimi:

    # '#' ile başlayan satırlar yorumdur.
    # Karakterler: @ad: sesin İngilizce tarifi [| Gemini ses adı] (bir kez tanımlanır)
    @anlatici: Middle-aged man, warm deep voice, calm storyteller | Charon
    @elif: Young girl, bright cheerful voice

    # Replikler: ad [duygu]: metin      (duygu isteğe bağlı)
    anlatici [sakin]: Bir zamanlar küçük bir köyde Elif adında bir kız yaşarmış.
    elif [mutlu]: Bugün hava ne kadar güzel!
    elif [fısıltı]: Sana bir sır vereceğim, kimseye söyleme.

Duygu olarak aşağıdaki Türkçe anahtarlardan biri ya da doğrudan İngilizce bir
tarif ("nervous, stuttering") yazılabilir.

Karakter sesleri bölümden bölüme değişmez: Gemini için karakter→ses eşlemesi
tts/sesler/gemini_sesler.json'da (ses adı verilmezse tarife göre seçilir),
VoxCPM2 için tasarlanan ses tts/sesler/<ad>.wav'da saklanır. Yeni ses için
ilgili kaydı silin.

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


GEMINI_MODEL = "gemini-3.1-flash-tts-preview"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
GEMINI_ERKEK = ["Charon", "Orus", "Fenrir", "Iapetus", "Puck", "Algenib", "Enceladus", "Rasalgethi", "Alnilam", "Umbriel"]
GEMINI_KADIN = ["Kore", "Leda", "Aoede", "Zephyr", "Despina", "Callirrhoe", "Autonoe", "Erinome", "Laomedeia", "Sulafat"]
GEMINI_JSON = os.path.join(SESLER_DIR, "gemini_sesler.json")


class GeminiHatasi(Exception):
    pass


class Gemini:
    """Gemini 3.1 Flash TTS (varsayılan motor). Hazır sesler, her bölümde aynı."""

    sr = 24000

    def __init__(self, karakterler, kullanilan):
        import json
        self.json = json
        os.makedirs(SESLER_DIR, exist_ok=True)
        self.sesler = json.load(open(GEMINI_JSON)) if os.path.exists(GEMINI_JSON) else {}
        self.tarif = {}
        for ad in kullanilan:
            tarif, _, ses = karakterler[ad].partition("|")
            self.tarif[ad] = tarif.strip()
            if ses.strip():
                self.sesler[ad] = ses.strip()
            elif ad not in self.sesler:
                erkek = re.search(r"\b(man|male|boy|gentleman|grandfather|father)\b", tarif, re.I)
                havuz = GEMINI_ERKEK if erkek else GEMINI_KADIN
                bos = [v for v in havuz if v not in self.sesler.values()] or havuz
                self.sesler[ad] = bos[0]
                print(f"[ses] '{ad}' için Gemini sesi seçildi: {bos[0]} ({tarif.strip()})", flush=True)
        json.dump(self.sesler, open(GEMINI_JSON, "w"), ensure_ascii=False, indent=2)

    def uret(self, ad, stil, metin, deneme):
        import base64, time, urllib.error, urllib.request
        tarif = ", ".join(x for x in (self.tarif[ad], stil) if x)
        prompt = f"Read the following Turkish text aloud exactly as written. Voice and style: {tarif}.\n\n{metin}"
        body = {"contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {
                    "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": self.sesler[ad]}}}}}
        req = urllib.request.Request(GEMINI_URL, self.json.dumps(body).encode(), {
            "Content-Type": "application/json",
            # Anahtar ortamdaki proxy tarafından eklenir; başka ortamda GEMINI_API_KEY kullanılır.
            "x-goog-api-key": os.environ.get("GEMINI_API_KEY", "proxy")})
        for bekle in (0, 5, 15, 45):
            time.sleep(bekle)
            try:
                d = self.json.load(urllib.request.urlopen(req, timeout=180))
                veri = d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
                return np.frombuffer(base64.b64decode(veri), dtype="<i2").astype(np.float32) / 32768
            except urllib.error.HTTPError as e:
                govde = e.read().decode()
                hata = f"HTTP {e.code}: {govde[:300]}"
                if "PerDay" in govde or "per day" in govde:
                    hata = "Gemini günlük ücretsiz kotası doldu (yaklaşık 24 saatte yenilenir)"
                    break
                if e.code not in (429, 500, 503):
                    break
            except (KeyError, IndexError) as e:
                hata = f"beklenmeyen yanıt: {e}"
        raise GeminiHatasi(hata)


class VoxCPM2:
    """VoxCPM2 (yedek, yerel ve ücretsiz). Sesler tts/sesler/<ad>.wav olarak saklanır."""

    def __init__(self, karakterler, kullanilan, dinle_ve_puanla, deneme_sayisi, esik):
        from voxcpm import VoxCPM
        self.model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False, device="cpu")
        self.sr = self.model.tts_model.sample_rate
        os.makedirs(SESLER_DIR, exist_ok=True)
        self.refler = {}
        for ad in kullanilan:
            yol = os.path.join(SESLER_DIR, f"{ad}.wav")
            if not os.path.exists(yol):
                tarif = karakterler[ad].partition("|")[0].strip()
                print(f"[ses] '{ad}' için yeni VoxCPM2 sesi tasarlanıyor: {tarif}", flush=True)
                en_iyi = None
                for d in range(1, deneme_sayisi + 1):
                    torch.manual_seed(d)
                    wav = self.model.generate(text=f"({tarif}, clear articulation){REF_METIN}")
                    puan = dinle_ve_puanla(wav, self.sr, REF_METIN)[0]
                    if en_iyi is None or puan > en_iyi[0]:
                        en_iyi = (puan, wav)
                    if puan >= esik:
                        break
                sf.write(yol, en_iyi[1], self.sr)
            self.refler[ad] = yol

    def uret(self, ad, stil, metin, deneme):
        torch.manual_seed(deneme)
        girdi = f"({stil}){metin}" if stil else metin
        return self.model.generate(text=girdi, reference_wav_path=self.refler[ad], cfg_value=2.0, inference_timesteps=10)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("senaryo")
    ap.add_argument("-o", "--cikti", help="çıktı dosyası (.mp3 veya .wav)")
    ap.add_argument("--motor", choices=["voxcpm", "gemini", "ikisi"], default="voxcpm",
                    help="voxcpm (varsayılan): VoxCPM2, yerel ve tamamen ücretsiz; gemini: Gemini 3.1 Flash TTS "
                         "(günde 10 ücretsiz istek); ikisi: her replik iki motorla, daha doğru olan kalır")
    ap.add_argument("--deneme", type=int, default=4, help="replik başına en fazla deneme")
    ap.add_argument("--esik", type=float, default=0.99, help="kabul için Whisper kelime benzerliği eşiği (1 = birebir)")
    ap.add_argument("--ara", type=float, default=0.45, help="replikler arası sessizlik (sn)")
    ap.add_argument("--whisper", default="small", help="kontrol için Whisper modeli")
    a = ap.parse_args()
    cikti = a.cikti or os.path.splitext(a.senaryo)[0] + ".mp3"

    karakterler, replikler = oku(a.senaryo)
    kullanilan = sorted({r[0] for r in replikler})
    torch.set_num_threads(os.cpu_count() or 1)
    import whisper
    asr = whisper.load_model(a.whisper)

    def dinle_ve_puanla(wav, sr, beklenen):
        with tempfile.NamedTemporaryFile(suffix=".wav") as t:
            sf.write(t.name, wav, sr)
            duyulan = asr.transcribe(t.name, language="tr")["text"].strip()
        return benzerlik(beklenen, duyulan), duyulan

    SR = 48000  # çıktı örnekleme hızı; motorların çıktısı buna çevrilir
    motorlar = {}
    if a.motor in ("ikisi", "gemini"):
        motorlar["gemini"] = Gemini(karakterler, kullanilan)
    if a.motor in ("ikisi", "voxcpm"):
        motorlar["voxcpm"] = VoxCPM2(karakterler, kullanilan, dinle_ve_puanla, a.deneme, a.esik)
    print(f"Motor: {', '.join(motorlar)}", flush=True)

    def sr48(wav, sr):
        if sr == SR:
            return wav.astype(np.float32)
        import librosa
        return librosa.resample(wav.astype(np.float32), orig_sr=sr, target_sr=SR)

    ara = np.zeros(int(SR * a.ara), dtype=np.float32)
    parcalar, sorunlu, sayac = [], [], {}
    for i, (ad, duygu, metin) in enumerate(replikler, 1):
        stil = DUYGULAR.get(duygu.lower(), duygu) if duygu else ""
        adaylar = []  # (puan, öncelik, motor, wav, duyulan, deneme)
        for oncelik, (isim, motor) in enumerate(list(motorlar.items())):
            en_iyi = None
            for deneme in range(1, a.deneme + 1):
                try:
                    wav = motor.uret(ad, stil, metin, deneme)
                except GeminiHatasi as e:
                    if len(motorlar) == 1:
                        raise SystemExit(f"Gemini hatası ({e}).\nÜcretsiz motorla devam etmek için: --motor voxcpm")
                    print(f"  ! Gemini kullanılamadı ({e}); bundan sonra sadece VoxCPM2", flush=True)
                    del motorlar[isim]
                    break
                puan, duyulan = dinle_ve_puanla(wav, motor.sr, metin)
                if en_iyi is None or puan > en_iyi[0]:
                    en_iyi = (puan, -oncelik, isim, sr48(wav, motor.sr), duyulan, deneme)
                if puan >= a.esik:
                    break
            if en_iyi:
                adaylar.append(en_iyi)
                print(f"    {isim}: puan={en_iyi[0]:.2f} deneme={en_iyi[5]} | {en_iyi[4]}", flush=True)
        # En yüksek puan kazanır; eşitlikte listedeki ilk motor (Gemini) seçilir.
        puan, _, isim, wav, duyulan, deneme = max(adaylar, key=lambda x: (x[0], x[1]))
        sayac[isim] = sayac.get(isim, 0) + 1
        durum = "OK" if puan >= a.esik else "KONTROL ET"
        if puan < a.esik:
            sorunlu.append((i, metin, duyulan))
        print(f"[{i}/{len(replikler)}] {durum} {ad}[{duygu or '-'}] → {isim} (puan={puan:.2f})", flush=True)
        parcalar += [wav, ara]

    ses = np.concatenate(parcalar[:-1])
    if cikti.lower().endswith(".wav"):
        sf.write(cikti, ses, SR)
    else:
        with tempfile.NamedTemporaryFile(suffix=".wav") as t:
            sf.write(t.name, ses, SR)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", t.name, "-b:a", "192k", cikti], check=True)
    print(f"\nBitti: {cikti} ({len(ses) / SR:.1f} sn) — seçilen motorlar: {sayac}")
    if sorunlu:
        print("Whisper'ın tam doğrulayamadığı replikler (dinleyip kontrol edin):")
        for i, metin, duyulan in sorunlu:
            print(f"  {i}. beklenen: {metin}\n     duyulan : {duyulan}")


if __name__ == "__main__":
    main()
