#!/usr/bin/env python3
"""OmniVoice seslendirme işçisi.

Node.js botu bu betiği bir kez başlatır; model bellekte kalır ve her istek
için yeniden yüklenmez. Protokol: stdin'den satır başına bir JSON istek,
stdout'a satır başına bir JSON yanıt.

  istek : {"id": 1, "text": "Merhaba", "instruct": "female"}
  yanıt : {"id": 1, "path": "/tmp/.../1.ogg"}  ya da  {"id": 1, "error": "..."}

Başlangıçta model yüklenince {"ready": true} yazılır.
"""
import json
import os
import subprocess
import sys
import tempfile

# Kütüphanelerin yazdığı her şey stderr'e gitsin; stdout sadece protokol için.
_proto = os.fdopen(os.dup(sys.stdout.fileno()), "w", buffering=1)
sys.stdout = sys.stderr

import soundfile as sf  # noqa: E402
import torch  # noqa: E402
from omnivoice import OmniVoice  # noqa: E402

SAMPLE_RATE = 24000
MODEL_ID = os.environ.get("OMNIVOICE_MODEL", "k2-fsa/OmniVoice")
LANGUAGE = os.environ.get("OMNIVOICE_LANGUAGE", "tr")
DEFAULT_INSTRUCT = os.environ.get("OMNIVOICE_INSTRUCT", "female") or None
OUT_DIR = tempfile.mkdtemp(prefix="omnivoice-")


def send(obj):
    _proto.write(json.dumps(obj, ensure_ascii=False) + "\n")


def to_ogg(wav_path, ogg_path):
    # Telegram sesli mesajı (voice) OGG/Opus ister.
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
         "-c:a", "libopus", "-b:a", "48k", "-ac", "1", ogg_path],
        check=True,
    )


def main():
    torch.set_num_threads(int(os.environ.get("OMNIVOICE_THREADS", os.cpu_count() or 1)))
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device != "cpu" else torch.float32
    model = OmniVoice.from_pretrained(MODEL_ID, device_map=device, dtype=dtype)
    send({"ready": True, "device": device})

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        req_id = None
        try:
            req = json.loads(line)
            req_id = req.get("id")
            text = (req.get("text") or "").strip()
            if not text:
                raise ValueError("boş metin")
            instruct = req.get("instruct", DEFAULT_INSTRUCT) or None
            kwargs = {"instruct": instruct} if instruct else {}
            audio = model.generate(text=text, language=LANGUAGE, **kwargs)
            wav_path = os.path.join(OUT_DIR, f"{req_id}.wav")
            ogg_path = os.path.join(OUT_DIR, f"{req_id}.ogg")
            sf.write(wav_path, audio[0], SAMPLE_RATE)
            to_ogg(wav_path, ogg_path)
            os.remove(wav_path)
            send({"id": req_id, "path": ogg_path})
        except Exception as e:  # tek bir hatalı istek işçiyi düşürmesin
            send({"id": req_id, "error": str(e)})


if __name__ == "__main__":
    main()
