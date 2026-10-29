"""Turn a photo into an animated ASCII-portrait SVG (row-by-row wipe with a block cursor).

Run once per photo: python scripts/make_ascii_svg.py [photo]   (STATIC=1 for a frozen frame)
Pillow + numpy only. Bright areas (sky, background) become blank; dark areas become dense glyphs.
"""

import os
import sys
from html import escape
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "assets" / "source.jpg"
OUT = ROOT / "assets" / "ascii-portrait.svg"
STATIC = os.environ.get("STATIC") == "1"

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)
COLS, ROWS = 84, 50
W, H = 370, 440
FONT, LINE, CHAR = 7, 7.6, 4.05  # CHAR: glyph advance, 84 cols -> 340px
X0, Y0 = 15, 54
SPAN = COLS * CHAR


def to_grid(path):
    img = ImageOps.exif_transpose(Image.open(path)).convert("L")
    img = ImageOps.autocontrast(img, cutoff=2)
    # glyphs are ~2x taller than wide, so squash rows
    a = (np.asarray(img.resize((COLS, ROWS), Image.LANCZOS), dtype=float) / 255) ** 0.8
    # soft oval vignette fades the background to blank
    yy, xx = np.mgrid[0:ROWS, 0:COLS]
    d = np.hypot((xx - COLS * 0.47) / (COLS * 0.42), (yy - ROWS * 0.5) / (ROWS * 0.62))
    a = np.clip(a + np.clip((d - 0.8) * 4, 0, 1), 0, 1)
    a = np.clip((a - 0.25) / 0.7, 0, 1)
    idx = ((1 - a) * (len(RAMP) - 1)).round().astype(int)
    return ["".join(RAMP[i] for i in row).rstrip() for row in idx]


def render(lines):
    rows, covers = [], []
    for i, line in enumerate(lines):
        if not line:
            continue
        y = Y0 + i * LINE
        width = len(line) * CHAR  # textLength pins the width, whatever font the viewer has
        text = (f'<text x="{X0}" y="{y:.2f}" textLength="{width:.1f}" lengthAdjust="spacingAndGlyphs" '
                f'xml:space="preserve">{escape(line)}</text>')
        rows.append(text)
        if STATIC:
            continue
        # a background-coloured cover slides off each row, block cursor on its leading edge
        top = y - LINE + 1
        covers.append(
            f'<g class="cv" style="animation-delay:{0.25 + i * 0.045:.3f}s">'
            f'<rect x="{X0 - 2}" y="{top - 1:.2f}" width="{SPAN + 8}" height="{LINE + 1:.2f}" fill="#0e0e11"/>'
            f'<rect class="cur" x="{X0 - 2}" y="{top + 0.2:.2f}" width="3.6" height="{LINE - 1.4:.2f}" fill="#e4e8ee"/></g>'
        )

    anim = "" if STATIC else f"""
  .cv{{animation:wipe .6s steps(30) both}}
  .cur{{animation:hide .6s steps(1) both;animation-delay:inherit}}
  @keyframes wipe{{from{{transform:translateX(0)}}to{{transform:translateX({SPAN + 8:.0f}px)}}}}
  @keyframes hide{{from{{opacity:1}}to{{opacity:0}}}}"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="ASCII portrait of Mohamed Thabet">
<style>
  text{{font-family:'JetBrains Mono','SFMono-Regular',Consolas,monospace;font-size:{FONT}px;fill:#c4cad3}}
  .t{{font-size:12px;fill:#a1a1aa}}{anim}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="#0e0e11" stroke="#27272a"/>
<path d="M.5 34.5h{W - 1}" stroke="#27272a"/>
<circle cx="20" cy="17.5" r="5" fill="#3f3f46"/><circle cx="37" cy="17.5" r="5" fill="#3f3f46"/><circle cx="54" cy="17.5" r="5" fill="#3f3f46"/>
<text x="{W / 2}" y="21.5" text-anchor="middle" class="t">portrait.txt</text>
{''.join(rows)}
<clipPath id="body"><rect x="1" y="35" width="{W - 2}" height="{H - 36}" rx="11"/></clipPath>
<g clip-path="url(#body)">{''.join(covers)}</g>
</svg>
"""


def main():
    lines = to_grid(SRC)
    OUT.write_text(render(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
