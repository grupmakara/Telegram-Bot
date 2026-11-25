"""ElevenLabs Music ile dizinin fon müziğini üretir. Kullanım: music.py <çıktı.mp3> [süre_sn] [istem]
Anahtar ağ vekilince xi-api-key başlığına eklenir."""
import json, os, sys, urllib.request

PROMPT = ("Dark cinematic Ottoman period drama underscore, 18th century Istanbul, ney flute and oud over low "
          "string drones and soft frame drum, slow 70 bpm, tense and melancholic, building suspense, "
          "no vocals, loopable, sits under dialogue")


def main():
    out = sys.argv[1]
    secs = int(sys.argv[2]) if len(sys.argv) > 2 else 180
    prompt = sys.argv[3] if len(sys.argv) > 3 else PROMPT
    body = {"prompt": prompt, "music_length_ms": secs * 1000, "force_instrumental": True}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128", data=json.dumps(body).encode(),
                                 method="POST", headers={"Content-Type": "application/json",
                                                         "xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")})
    with urllib.request.urlopen(req, timeout=600) as r, open(out, "wb") as f:
        f.write(r.read())
    print(out)


if __name__ == "__main__":
    if os.path.exists("/root/.ccr/ca-bundle.crt"):
        os.environ.setdefault("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt")
    main()
