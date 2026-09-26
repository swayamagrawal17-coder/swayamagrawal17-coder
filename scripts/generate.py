"""Regenerates every SVG in assets/ from assets/skills.json.

Run from the repo root:  python3 scripts/generate.py
"""
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DATA = json.loads((ASSETS / "skills.json").read_text())

FONT = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,monospace"

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", text="#e6edf3", muted="#8b949e",
                 accent="#aa9bef", grid="#30363d", green="#7ee787"),
    "light": dict(bg="#ffffff", border="#d0d7de", text="#1f2328", muted="#656d76",
                  accent="#6e56cf", grid="#d0d7de", green="#1a7f37"),
}


def banner(t):
    rows = [
        ("name", "Swayam Agrawal"),
        ("role", "B.Com student · finance & management"),
        ("college", "Indira College of Commerce and Science, Pune"),
        ("cma", "Foundation qualified · 276/400 · all 4 exemptions"),
        ("sgpa", "9.27"),
        ("status", "learning to code, vibe first"),
    ]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 330" width="880" height="330" font-family="{FONT}" font-size="15">',
           "<style>.l{animation:s .01s backwards}@keyframes s{from{opacity:0}}"
           ".c{animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}</style>",
           f'<rect x="1" y="1" width="878" height="328" rx="10" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="2"/>',
           f'<line x1="1" y1="40" x2="879" y2="40" stroke="{t["border"]}" stroke-width="2"/>']
    for i, col in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        out.append(f'<circle cx="{26 + i * 22}" cy="21" r="6" fill="{col}"/>')
    out.append(f'<text x="440" y="26" text-anchor="middle" fill="{t["muted"]}" font-size="13">profile.sh --live</text>')
    out.append(f'<text class="l" style="animation-delay:.3s" x="28" y="80" fill="{t["green"]}">$ <tspan fill="{t["text"]}">./profile.sh --live</tspan></text>')
    y, delay = 118, 1.0
    for key, val in rows:
        out.append(f'<text class="l" style="animation-delay:{delay:.1f}s" x="28" y="{y}" fill="{t["muted"]}">{key}<tspan x="118" fill="{t["accent"]}">: </tspan><tspan fill="{t["text"]}">{escape(val)}</tspan></text>')
        y += 30
        delay += 0.35
    out.append(f'<text class="l" style="animation-delay:{delay:.1f}s" x="28" y="{y + 4}" fill="{t["green"]}">$ <tspan class="c" fill="{t["accent"]}">█</tspan></text>')
    out.append("</svg>")
    return "\n".join(out)


def radar(t, spec):
    axes = spec["axes"]
    n, cx, cy, r = len(axes), 260, 210, 115

    def pt(i, frac):
        a = -math.pi / 2 + 2 * math.pi * i / n
        return cx + r * frac * math.cos(a), cy + r * frac * math.sin(a)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 420" width="520" height="420" font-family="{FONT}" font-size="12">',
           f'<text x="260" y="26" text-anchor="middle" fill="{t["accent"]}" font-size="14" font-weight="600">{escape(spec["title"])}</text>']
    for ring in (0.2, 0.4, 0.6, 0.8, 1.0):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, ring) for i in range(n)))
        out.append(f'<polygon points="{pts}" fill="none" stroke="{t["grid"]}" stroke-width="1"/>')
    for i in range(n):
        x, y = pt(i, 1)
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["grid"]}" stroke-width="1"/>')
    pts = [pt(i, v / 10) for i, (_, v) in enumerate(axes)]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<polygon points="{poly}" fill="{t["accent"]}" fill-opacity="0.25" stroke="{t["accent"]}" stroke-width="2"/>')
    for x, y in pts:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{t["accent"]}"/>')
    for i, (name, _) in enumerate(axes):
        x, y = pt(i, 1.2)
        anchor = "middle" if abs(x - cx) < 8 else ("start" if x > cx else "end")
        out.append(f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="{anchor}" fill="{t["text"]}">{escape(name)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def numbers(t):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 220" width="480" height="220" font-family="{FONT}">',
           f'<rect x="1" y="1" width="478" height="218" rx="10" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="2"/>',
           f'<text x="24" y="34" fill="{t["accent"]}" font-size="14" font-weight="600">numbers.json</text>']
    for i, (big, label) in enumerate(DATA["numbers"]):
        x = 24 + (i % 2) * 226
        y = 88 + (i // 2) * 68
        out.append(f'<text x="{x}" y="{y}" fill="{t["text"]}" font-size="28" font-weight="700">{escape(big)}</text>')
        out.append(f'<text x="{x}" y="{y + 22}" fill="{t["muted"]}" font-size="12">{escape(label)}</text>')
    out.append("</svg>")
    return "\n".join(out)


for name, t in THEMES.items():
    (ASSETS / f"banner-{name}.svg").write_text(banner(t))
    (ASSETS / f"radar-finance-{name}.svg").write_text(radar(t, DATA["radars"]["finance"]))
    (ASSETS / f"radar-management-{name}.svg").write_text(radar(t, DATA["radars"]["management"]))
    (ASSETS / f"card-numbers-{name}.svg").write_text(numbers(t))
print("generated", len(list(ASSETS.glob("*.svg"))), "svgs")
