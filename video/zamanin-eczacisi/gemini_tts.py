"""Gemini TTS (gemini-3.8-flash-tts) istemcisi. Anahtar ağ katmanında eklenir; burada yer tutucu gönderilir."""
import base64, json, time, urllib.request, urllib.error

URL = 'https://generativelanguage.googleapis.com/v1beta/interactions'


class KotaDoldu(Exception):
    """Modelin günlük ücretsiz kotası bitti."""


def synth(text, voice, style, out, model='gemini-3.8-flash-tts', tries=6):
    modern = model.startswith('gemini-3.8-')
    content = {'type': 'text', 'text': text if (modern or not style) else f'Read the following text with this delivery: {style}\n\n{text}'}
    if style and modern:
        content['annotations'] = [{'type': 'speech_metadata', 'style': style}]
    body = json.dumps({'model': model, 'input': [{'type': 'user_input', 'content': [content]}],
                       'response_format': {'type': 'audio', 'mime_type': 'audio/wav'} if modern else {'type': 'audio'},
                       'generation_config': {'speech_config': [{'voice': voice}]}, 'store': False}).encode()
    for attempt in range(tries):
        req = urllib.request.Request(URL, data=body, headers={'Content-Type': 'application/json', 'x-goog-api-key': 'yer-tutucu'})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                p = json.load(r)
            audio = [c for s in p.get('steps', []) if s.get('type') == 'model_output' for c in s.get('content', []) if c.get('type') == 'audio']
            if p.get('status') != 'completed' or len(audio) != 1:
                raise RuntimeError(f"tamamlanmadı: {p.get('status')}")
            data = base64.b64decode(audio[0]['data'])
            if data[:4] != b'RIFF':  # eski modeller: ham PCM -> WAV
                import re as _re, struct
                rate = int((_re.search(r'rate=(\d+)', audio[0].get('mime_type', '')) or [0, 24000])[1])
                data = b'RIFF' + struct.pack('<I', 36 + len(data)) + b'WAVEfmt ' + struct.pack('<IHHIIHH', 16, 1, 1, rate, rate * 2, 2, 16) + b'data' + struct.pack('<I', len(data)) + data
            open(out, 'wb').write(data)
            return True
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            if e.code == 429 and 'per day' in msg:
                raise KotaDoldu(model)
            if e.code in (429, 500, 503) and attempt < tries - 1:
                wait = 20 * (attempt + 1)
                print(f'  {e.code}, {wait} sn bekleniyor', flush=True); time.sleep(wait); continue
            raise RuntimeError(f'HTTP {e.code}: {msg}')
