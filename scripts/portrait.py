"""Turns the dot-portrait source image into a transparent-background PNG.

Brightness of the red channel becomes opacity, and every pixel is repainted in
the accent color, so the portrait sits cleanly on any background.

Run from the repo root:  python3 scripts/portrait.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "source" / "portrait-original.webp"
OUT = ROOT / "assets" / "portrait.png"

ACCENT = (240, 180, 41)
BG_FLOOR, DOT_CEIL = 20, 240  # red-channel values treated as background / full dot
WIDTH = 480

src = Image.open(SRC).convert("RGB")
height = round(src.height * WIDTH / src.width)
src = src.resize((WIDTH, height), Image.LANCZOS)

red = src.getchannel("R")
alpha = red.point(lambda v: max(0, min(255, round((v - BG_FLOOR) * 255 / (DOT_CEIL - BG_FLOOR)))))

out = Image.new("RGBA", src.size, ACCENT + (0,))
out.putalpha(alpha)
out.save(OUT, optimize=True)
print(f"wrote {OUT.name} {out.size} {OUT.stat().st_size // 1024} KB")
