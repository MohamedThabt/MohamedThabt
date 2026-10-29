"""Render the hand-authored cards: banner.svg and info-card.svg.

Edit the content lists below, then run: python scripts/make_cards.py   (STATIC=1 for a frozen frame)
"""

import os
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
STATIC = os.environ.get("STATIC") == "1"

FLIP = [
    "Software engineer & Applied AI engineer.",
    "I build AI agents, robust APIs & real-time systems.",
    "Building AI systems that ship.",
    "RAG pipelines · intelligent agents · secure infra.",
    "Laravel · FastAPI · Go · Python.",
    "Open for work — full-time, freelance, collabs.",
]

INFO = [
    ("Name", "Mohamed Thabet  ·  aka SirThabet"),
    ("Role", "Software & Applied AI Engineer"),
    ("Now", "Freelance AI Engineer — agents, RAG, platforms"),
    ("Prev", "Founding Engineer @ Sirius · led 7 engineers"),
    ("Base", "Cairo, Egypt · UTC+2 · remote-friendly"),
    ("Langs", "Python · PHP · Go · TypeScript"),
    ("Backend", "FastAPI · Laravel · Node.js · REST"),
    ("AI", "Agents · RAG · LangChain · DSPy · Ollama"),
    ("Data", "PostgreSQL · Redis · MySQL · Vector DBs"),
    ("Ops", "Docker · GitHub Actions · Cloudflare · VPS"),
    ("Observe", "Sentry · OpenTelemetry · Prometheus · Grafana"),
    ("Edu", "B.Sc. Computer Science · Beni-Suef Univ. '26"),
]

HIGHLIGHTS = [
    "Led a team of 7 on Sirius — AI pre-code planning",
    "Shipped 3 e-learning platforms + the Rilrz MVP",
    "SaveIn — open-source Chrome MV3 → Notion sync",
]

# "MT" monogram on an 11x4 grid — same cells as src/components/brand.tsx on sirthabet.dev
MARK = [(1, 0, 3, 1), (0, 1, 1, 3), (2, 1, 1, 2), (4, 1, 1, 3), (6, 0, 5, 1), (8, 1, 1, 3)]
STEEL = ["#1c1d22", "#2f3540", "#4a5361", "#6f7a89", "#a3adba", "#e4e8ee"]
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,monospace"


def chrome(w, h, title):
    return (
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="#0e0e11" stroke="#27272a"/>'
        f'<path d="M.5 34.5h{w - 1}" stroke="#27272a"/>'
        '<circle cx="20" cy="17.5" r="5" fill="#3f3f46"/><circle cx="37" cy="17.5" r="5" fill="#3f3f46"/>'
        '<circle cx="54" cy="17.5" r="5" fill="#3f3f46"/>'
        f'<text x="{w / 2}" y="21.5" text-anchor="middle" class="t">{escape(title)}</text>'
    )


def banner():
    W, H = 860, 232
    cmd, cw = "whoami", 9.6  # glyph advance at 16px

    cells = []
    cx0, cy0, c = 590, 84, 20
    for x, y, w, h in MARK:
        for i in range(w):
            for j in range(h):
                col, row = x + i, y + j
                px, py = cx0 + col * c, cy0 + row * c
                delay = 0.5 + col * 0.07 + row * 0.04
                cells.append(
                    f'<g class="px" style="animation-delay:{delay:.2f}s">'
                    f'<path d="M{px} {py}l7 7h{c}l-7 -7zM{px + c} {py}l7 7v{c}l-7 -7z" fill="#2f3540"/>'
                    f'<rect x="{px}" y="{py}" width="{c}" height="{c}" fill="url(#steel)" stroke="#0e0e11" stroke-width="1"/></g>'
                )

    flips = "".join(
        f'<text x="48" y="184" class="flip" style="animation-delay:{1.9 + i * 3:.1f}s">{escape(s)}</text>'
        for i, s in enumerate(FLIP)
    )
    period = len(FLIP) * 3
    show = 100 / len(FLIP)

    anim = "" if STATIC else f"""
  .type{{animation:type .6s .3s steps({len(cmd)}) both}}
  @keyframes type{{to{{transform:translateX({len(cmd) * cw:.1f}px)}}}}
  .in{{animation:up .7s cubic-bezier(.2,.8,.2,1) both}}
  .px{{animation:pop .45s cubic-bezier(.3,1.6,.5,1) both;transform-box:fill-box;transform-origin:center}}
  .flip{{fill-opacity:0;animation:flip {period}s ease-in-out infinite both}}
  .blink{{animation:blink 1.1s steps(1) infinite}}
  .pulse{{animation:pulse 2.4s ease-in-out infinite}}
  .sword{{stroke-dasharray:520;stroke-dashoffset:520;animation:draw 1.1s 1.2s cubic-bezier(.6,0,.2,1) forwards}}
  @keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
  @keyframes pop{{from{{opacity:0;transform:translateY(-14px) scale(.4)}}to{{opacity:1;transform:none}}}}
  @keyframes flip{{0%{{fill-opacity:0}}{show * .1:.1f}%{{fill-opacity:1}}{show * .9:.1f}%{{fill-opacity:1}}{show:.1f}%,100%{{fill-opacity:0}}}}
  @keyframes blink{{50%{{opacity:0}}}}
  @keyframes pulse{{50%{{opacity:.35}}}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}"""
    if STATIC:
        flips = f'<text x="48" y="184" class="flip">{escape(FLIP[0])}</text>'

    # a background-coloured cover steps off the command, one glyph at a time
    typed = "" if STATIC else f'<rect class="type" x="80" y="56" width="{len(cmd) * cw + 4:.1f}" height="24" fill="#0e0e11"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Mohamed Thabet — Software and Applied AI Engineer">
<defs>
  <linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e4e8ee"/><stop offset=".55" stop-color="#a3adba"/><stop offset="1" stop-color="#6f7a89"/></linearGradient>
  <linearGradient id="blade" gradientUnits="userSpaceOnUse" x1="70" x2="520" y1="0" y2="0"><stop offset="0" stop-color="#e4e8ee"/><stop offset="1" stop-color="#e4e8ee" stop-opacity="0"/></linearGradient>
  <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#27272a"/></pattern>
  <linearGradient id="fade" x1="0" x2="1"><stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <mask id="m"><rect x="0" y="35" width="{W}" height="{H - 35}" fill="url(#fade)"/></mask>
</defs>
<style>
  text{{font-family:{MONO}}}
  .t{{font-size:12px;fill:#a1a1aa}}
  .p{{font-size:16px;fill:#6f7a89}}
  .cmd{{font-size:16px;fill:#e4e4e7}}
  .name{{font-size:46px;font-weight:700;fill:#f4f4f5;letter-spacing:-1.5px}}
  .flip{{font-size:15px;fill:#a1a1aa}}
  .chev{{font-size:15px;fill:#6f7a89}}
  .meta{{font-size:12px;fill:#71717a}}{anim}
</style>
{chrome(W, H, "sirthabet@github: ~")}
<rect x="1" y="35" width="{W - 2}" height="{H - 36}" rx="11" fill="url(#dots)" mask="url(#m)"/>
<text x="48" y="74" class="p">~ $</text>
<text x="82" y="74" class="cmd">{cmd}</text>{typed}
<g class="in" style="animation-delay:.95s"><text x="46" y="134" class="name">Mohamed Thabet</text></g>
<g stroke-linecap="round">
  <path class="sword" d="M70 153H520" stroke="url(#blade)" stroke-width="2"/>
  <path class="in" style="animation-delay:1.2s" d="M62 146v14M50 153h12" stroke="#a3adba" stroke-width="2.5"/>
  <rect class="in" style="animation-delay:1.2s" x="44" y="150" width="6" height="6" transform="rotate(45 47 153)" fill="#e4e8ee"/>
</g>
<text x="32" y="184" class="chev">›</text>
{flips}
<g class="in" style="animation-delay:1.5s">
  <circle class="pulse" cx="52" cy="208" r="3.5" fill="#4ade80"/>
  <text x="62" y="212" class="meta">open for work  ·  Cairo, EG  ·  sirthabet.dev</text>
</g>
{''.join(cells)}
<text x="590" y="212" class="meta in" style="animation-delay:1.6s">Fig. 1 — the MT mark</text>
<rect class="blink" x="{82 + len(cmd) * cw + 3:.1f}" y="60" width="9" height="17" fill="#a3adba" opacity=".8"/>
</svg>
"""


def info_card():
    W, H = 490, 440
    lines, y = [], 100
    for i, (k, v) in enumerate(INFO):
        lines.append(
            f'<g class="ln" style="animation-delay:{0.55 + i * 0.07:.2f}s">'
            f'<text x="26" y="{y}" class="k">{escape(k)}</text><text x="108" y="{y}" class="v">{escape(v)}</text></g>'
        )
        y += 18
    y += 12
    base = 0.55 + len(INFO) * 0.07
    lines.append(f'<g class="ln" style="animation-delay:{base:.2f}s"><text x="26" y="{y}" class="h">Highlights</text></g>')
    for i, h in enumerate(HIGHLIGHTS):
        y += 18
        lines.append(
            f'<g class="ln" style="animation-delay:{base + 0.08 * (i + 1):.2f}s">'
            f'<text x="26" y="{y}" class="k">›</text><text x="42" y="{y}" class="v">{escape(h)}</text></g>'
        )
    blocks = "".join(
        f'<rect class="ln" style="animation-delay:{base + 0.4 + i * 0.05:.2f}s" x="{26 + i * 26}" y="{y + 18}" width="22" height="12" rx="2" fill="{c}"/>'
        for i, c in enumerate(STEEL)
    )
    anim = "" if STATIC else """
  .ln{animation:slide .5s cubic-bezier(.2,.8,.2,1) both}
  @keyframes slide{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Profile card: Mohamed Thabet, Software and Applied AI Engineer, Cairo">
<style>
  text{{font-family:{MONO};font-size:12px}}
  .t{{fill:#a1a1aa}}
  .u{{font-size:14px;font-weight:700;fill:#e4e8ee}}
  .at{{font-size:14px;font-weight:700;fill:#6f7a89}}
  .k{{font-weight:700;fill:#a3adba}}
  .v{{fill:#e4e4e7}}
  .h{{font-weight:700;fill:#f4f4f5;letter-spacing:.5px}}
  .d{{fill:#3f3f46}}{anim}
</style>
{chrome(W, H, "neofetch")}
<g class="ln" style="animation-delay:.3s"><text x="26" y="64"><tspan class="u">sirthabet</tspan><tspan class="at">@</tspan><tspan class="u">github</tspan></text></g>
<g class="ln" style="animation-delay:.4s"><text x="26" y="78" class="d">{"─" * 22}</text></g>
{''.join(lines)}
{blocks}
</svg>
"""


def main():
    (ASSETS / "banner.svg").write_text(banner(), encoding="utf-8")
    (ASSETS / "info-card.svg").write_text(info_card(), encoding="utf-8")
    print("banner.svg, info-card.svg")


if __name__ == "__main__":
    main()
