"""Regenerate the Instagram story posters and pack them by publishing slot.

  python3 engine/story_paketi.py [ilk_bolum son_bolum]   (default: 1 24)

Writes cikti/<dizi>/story/storyNN.png (via engine/story.py) and
cikti/<dizi>/story_paketi.zip with files named gunD_HHMM_bolumNN.png, where three
episodes go out per day at 12:30, 18:00 and 21:00.
"""
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import story  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIZI = "bodrum_kattaki_adam"
SLOTS = ["1230", "1800", "2100"]


def main(first=1, last=24):
    eps = ROOT / "diziler" / DIZI / "bolumler"
    for n in range(first, last + 1):
        story.make_story(eps / f"bolum{n:02d}.json")
    out = ROOT / "cikti" / DIZI / "story_paketi.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in range(1, 25):
            png = ROOT / "cikti" / DIZI / "story" / f"story{n:02d}.png"
            if png.exists():
                z.write(png, f"gun{(n - 1) // 3 + 1}_{SLOTS[(n - 1) % 3]}_bolum{n:02d}.png")
    print(out)


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:3]]
    main(*a) if a else main()
