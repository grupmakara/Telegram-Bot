"""Write HAZIR_VIDEOLAR.md: which episodes are ready to publish, with title, caption and file.

An episode is ready when its video exists and either it is one of the published
ElevenLabs episodes (1-6) or every spoken line has a VoxCPM2 clip and the video was
rendered after the newest clip.

  python3 engine/hazir_liste.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from voices import clip_name, spoken_lines  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIZI = "bodrum_kattaki_adam"
PUBLISHED_ELEVENLABS = range(1, 7)
TAGS = "#bodrumkattakiadam #minidizi #animasyon #dizi #reels"


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True).stdout
    return float(out or 0)


def is_ready(n, ep, video):
    if not video.exists():
        return False, ""
    if n in PUBLISHED_ELEVENLABS:
        return True, "ElevenLabs (yayında)"
    for engine, label in [("cb", "Chatterbox (yeni sesler)"), ("vox", "VoxCPM2 (eski, düzeltilecek)")]:
        d = ROOT / "seslendirme" / DIZI / engine / f"bolum{n:02d}"
        clips = [d / clip_name(si, li) for si, li, _ in spoken_lines(ep)]
        if clips and all(c.exists() for c in clips):
            newest = max(c.stat().st_mtime for c in clips)
            return video.stat().st_mtime > newest, label
    return False, ""


def main():
    md = (ROOT / "instagram" / "aciklamalar.md").read_text(encoding="utf-8")
    caps = {int(m.group(1)): (m.group(2).strip(), m.group(3).strip())
            for m in re.finditer(r"## (\d+)\. Bölüm\n\*\*(.+?)\*\*\n(.+)", md)}
    ready, pending = [], []
    for ep_path in sorted((ROOT / "diziler" / DIZI / "bolumler").glob("bolum*.json")):
        ep = json.loads(ep_path.read_text(encoding="utf-8"))
        n = ep["episode"]
        video = ROOT / "cikti" / DIZI / f"{ep_path.stem}.mp4"
        ok, voice = is_ready(n, ep, video)
        short, caption = caps.get(n, (ep["title"].split(" | ")[0], ""))
        (ready if ok else pending).append((n, ep["title"], short, caption, video.relative_to(ROOT.parent), voice,
                                           duration(video) if ok else 0))
    out = ["# Bodrum Kattaki Adam: Hazır Videolar", "",
           f"Her paylaşımda etiketler: `{TAGS}`", "",
           "Yayın sırası: günde 3 bölüm (12:30, 18:00, 21:00). Story görselleri: "
           "`cizgi_dizi/cikti/bodrum_kattaki_adam/story/storyNN.png`.", "",
           f"## Hazır ({len(ready)} bölüm)", "", "| Bölüm | Süre | Ses | Dosya |", "|---|---|---|---|"]
    out += [f"| {n} | {d:.0f} sn | {v} | `{p}` |" for n, _, _, _, p, v, d in ready]
    out.append("")
    for n, title, short, caption, path, voice, dur in ready:
        out += [f"### {n}. Bölüm", f"**Başlık:** {title}", f"**Kısa başlık (Instagram):** {short}",
                f"**Açıklama:** {caption}", f"**Etiketler:** {TAGS}", f"**Dosya:** `{path}` ({dur:.0f} sn)", ""]
    out += [f"## Henüz hazır değil ({len(pending)} bölüm)", "",
            "Bu bölümler Chatterbox ile yeniden seslendiriliyor; bitince render edilip yukarıdaki listeye eklenecek. "
            "Klasörde bu bölümlerin eski taslak videoları (düz Edge sesi) olabilir: onları yayınlama.", ""]
    out += [f"- **{n}. Bölüm:** {title}. {caption}" for n, title, _, caption, _, _, _ in pending]
    (ROOT / "HAZIR_VIDEOLAR.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{len(ready)} hazır, {len(pending)} bekliyor")


if __name__ == "__main__":
    main()
