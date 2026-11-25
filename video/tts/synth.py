"""Edge TTS ile replikleri seslendirir. Kullanım: synth.py job.json
job: {"items":[{key,text,voice,pitch,rate}], "outDir": "..."}
Her öğe için outDir/<key>.mp3 ve <key>.json ({durationMs, words}) yazar; var olanları atlar."""
import asyncio, json, os, subprocess, sys, time

RETRIES = 3


def words_from(chunks):
    out = []
    for c in chunks:
        if c.get("type") == "WordBoundary":
            start = c["offset"] // 10_000
            out.append({"text": c["text"], "startMs": start, "endMs": start + c["duration"] // 10_000})
    return out


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
    chunks = asyncio.run(_stream(item, mp3))
    meta = {"durationMs": duration_ms(mp3), "words": words_from(chunks)}
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
