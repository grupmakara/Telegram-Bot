"""Replikleri seslendirir (ElevenLabs ya da Edge TTS). Kullanım: synth.py job.json
job: {"items":[{key,text,provider,voice,pitch,rate,settings?}], "outDir": "..."}
provider "elevenlabs": voice = ses kimliği; anahtar ağ vekilince xi-api-key başlığına eklenir.
Her öğe için outDir/<key>.mp3 ve <key>.json ({durationMs, words}) yazar; var olanları atlar."""
import asyncio, base64, json, os, subprocess, sys, time, urllib.request, urllib.error

RETRIES = 3


def words_from(chunks):
    out = []
    for c in chunks:
        if c.get("type") == "WordBoundary":
            start = c["offset"] // 10_000
            out.append({"text": c["text"], "startMs": start, "endMs": start + c["duration"] // 10_000})
    return out


def words_from_alignment(al):
    """ElevenLabs karakter zamanlarını kelimelere çevirir."""
    out, cur, start, end = [], "", None, None
    for ch, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                out.append({"text": cur, "startMs": round(start * 1000), "endMs": round(end * 1000)})
            cur, start = "", None
            continue
        if start is None:
            start = a
        cur += ch
        end = b
    if cur:
        out.append({"text": cur, "startMs": round(start * 1000), "endMs": round(end * 1000)})
    return out


class Unauthorized(Exception):
    pass


EL_MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")


def elevenlabs_one(item, mp3):
    body = {"text": item["text"], "model_id": EL_MODEL, "language_code": "tr",
            "voice_settings": item.get("settings") or {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35}}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{item['voice']}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise Unauthorized(f"ElevenLabs {e.code}: {e.read()[:200]!r}")
        raise
    except urllib.error.URLError as e:
        if "403" in str(e.reason):  # ağ vekili: anahtar kaydedilmemiş, host kapalı
            raise Unauthorized(f"ElevenLabs erişimi yok: {e.reason}")
        raise
    with open(mp3, "wb") as f:
        f.write(base64.b64decode(data["audio_base64"]))
    return words_from_alignment(data.get("normalized_alignment") or data["alignment"])


def duration_ms(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return int(round(float(r.stdout.strip()) * 1000))


async def _stream(item, mp3):
    import edge_tts
    comm = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"],
                                boundary="WordBoundary", proxy=os.environ.get("HTTPS_PROXY"))
    chunks = []
    with open(mp3, "wb") as f:
        async for c in comm.stream():
            if c["type"] == "audio":
                f.write(c["data"])
            else:
                chunks.append(c)
    return chunks


def synth_one(item, out_dir):
    mp3 = os.path.join(out_dir, item["key"] + ".mp3")
    if item.get("provider") == "elevenlabs":
        words = elevenlabs_one(item, mp3)
    else:
        words = words_from(asyncio.run(_stream(item, mp3)))
    meta = {"durationMs": duration_ms(mp3), "words": words}
    with open(os.path.join(out_dir, item["key"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)


def run(job):
    out_dir = job["outDir"]
    os.makedirs(out_dir, exist_ok=True)
    for item in job["items"]:
        base = os.path.join(out_dir, item["key"])
        if os.path.exists(base + ".mp3") and os.path.exists(base + ".json"):
            continue
        for attempt in range(1, RETRIES + 1):
            try:
                synth_one(item, out_dir)
                break
            except Unauthorized as e:
                print(f"ElevenLabs yetkisiz: {e}", file=sys.stderr)
                sys.exit(3)
            except Exception as e:  # ağ hataları dahil
                if attempt == RETRIES:
                    print(f"Seslendirme başarısız: {item['text']!r}: {e}", file=sys.stderr)
                    for ext in (".mp3", ".json"):
                        if os.path.exists(base + ext):
                            os.remove(base + ext)
                    sys.exit(1)
                time.sleep(2 * attempt)


if __name__ == "__main__":
    if os.path.exists("/root/.ccr/ca-bundle.crt"):
        os.environ.setdefault("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt")
    with open(sys.argv[1], encoding="utf-8") as f:
        run(json.load(f))
