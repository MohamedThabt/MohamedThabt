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
    "I build AI agents, robust APIs & real-time systems.",
    "Building AI systems that ship.",
    "RAG pipelines · intelligent agents · secure infra.",
    "Laravel · FastAPI · Go · Python.",
    "Open for work — full-time, freelance, collabs.",
]

CHIPS = ["AI Agents", "RAG", "Backend", "Real-time", "Security"]

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
    W, H = 860, 274
    cmd, cw = "whoami", 9.6  # glyph advance at 16px

    # MT mark: all extrusions first, then all faces, so inner side walls stay hidden
    walls, faces, clips = [], [], []
    cx0, cy0, c, depth = 584, 72, 22, 8
    for x, y, w, h in MARK:
        for i in range(w):
            for j in range(h):
                col, row = x + i, y + j
                px, py = cx0 + col * c, cy0 + row * c
                style = f'style="animation-delay:{0.5 + col * 0.07 + row * 0.04:.2f}s"'
                walls.append(
                    f'<path class="px" {style} d="M{px + c} {py}l{depth} {depth}v{c}l-{depth} -{depth}z" fill="#2f3540"/>'
                    f'<path class="px" {style} d="M{px} {py + c}l{depth} {depth}h{c}l-{depth} -{depth}z" fill="#1c1d22"/>'
                )
                faces.append(f'<rect class="px" {style} x="{px}" y="{py}" width="{c}" height="{c}" fill="url(#steel)" stroke="#0e0e11"/>')
                clips.append(f'<rect x="{px}" y="{py}" width="{c}" height="{c}"/>')
    mark_w = 11 * c

    chips, chx = [], 48
    for i, label in enumerate(CHIPS):
        w = len(label) * 6.6 + 22
        chips.append(
            f'<g class="in" style="animation-delay:{1.7 + i * 0.08:.2f}s">'
            f'<rect x="{chx}" y="226" width="{w:.1f}" height="22" rx="11" fill="#141418" stroke="#3f3f46"/>'
            f'<text x="{chx + w / 2:.1f}" y="241" text-anchor="middle" class="chip">{escape(label)}</text></g>'
        )
        chx += w + 8

    flips = "".join(
        f'<text x="48" y="208" class="flip" style="animation-delay:{1.9 + i * 3:.1f}s">{escape(s)}</text>'
        for i, s in enumerate(FLIP)
    )
    period = len(FLIP) * 3
    show = 100 / len(FLIP)

    anim = "" if STATIC else f"""
  .type{{animation:type .6s .3s steps({len(cmd)}) both}}
  @keyframes type{{to{{transform:translateX({len(cmd) * cw:.1f}px)}}}}
  .in{{animation:up .7s cubic-bezier(.2,.8,.2,1) both}}
  .px{{animation:pop .45s cubic-bezier(.3,1.6,.5,1) both}}
  .flip{{fill-opacity:0;animation:flip {period}s ease-in-out infinite both}}
  .blink{{animation:blink 1.1s steps(1) infinite}}
  .pulse{{animation:pulse 2.4s ease-in-out infinite}}
  .sword{{stroke-dasharray:460;stroke-dashoffset:460;animation:draw 1.1s 1.2s cubic-bezier(.6,0,.2,1) forwards}}
  .glint{{animation:glint 6s 2.4s ease-in-out infinite both}}
  .shine{{animation:shine 6s 2s ease-in-out infinite both}}
  .cta{{animation:ring 3s 2s ease-in-out infinite}}
  .arrow{{animation:nudge 3s 2s ease-in-out infinite}}
  @keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
  @keyframes pop{{from{{opacity:0;transform:translateY(-16px)}}to{{opacity:1;transform:none}}}}
  @keyframes flip{{0%{{fill-opacity:0}}{show * .1:.1f}%{{fill-opacity:1}}{show * .9:.1f}%{{fill-opacity:1}}{show:.1f}%,100%{{fill-opacity:0}}}}
  @keyframes blink{{50%{{opacity:0}}}}
  @keyframes pulse{{50%{{opacity:.35}}}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}
  @keyframes glint{{0%{{transform:translateX(0);opacity:0}}3%{{opacity:1}}22%{{transform:translateX(400px);opacity:0}}100%{{transform:translateX(400px);opacity:0}}}}
  @keyframes shine{{0%{{transform:translateX(0)}}25%,100%{{transform:translateX({mark_w + 160}px)}}}}
  @keyframes ring{{50%{{stroke:#a3adba}}}}
  @keyframes nudge{{0%,60%,100%{{transform:none}}75%{{transform:translate(3px,-3px)}}}}"""
    if STATIC:
        flips = f'<text x="48" y="208" class="flip">{escape(FLIP[0])}</text>'

    # a background-coloured cover steps off the command, one glyph at a time
    typed = "" if STATIC else f'<rect class="type" x="80" y="58" width="{len(cmd) * cw + 4:.1f}" height="24" fill="#0e0e11"/>'
    btn_y = cy0 + 4 * c + 40
    glint = "" if STATIC else '  <rect class="glint" x="70" y="156.5" width="70" height="3" rx="1.5" fill="url(#spark)"/>'
    shine = "" if STATIC else (
        f'<g clip-path="url(#mk)"><g transform="skewX(-20)"><rect class="shine" x="{cx0 - 60}" y="{cy0 - 10}" width="60" '
        f'height="{4 * c + 20}" fill="url(#band)"/></g></g>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Mohamed Thabet — Software and Applied AI Engineer. Visit sirthabet.dev">
<defs>
  <linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f6f9"/><stop offset=".5" stop-color="#a3adba"/><stop offset="1" stop-color="#6f7a89"/></linearGradient>
  <linearGradient id="blade" gradientUnits="userSpaceOnUse" x1="70" x2="500" y1="0" y2="0"><stop offset="0" stop-color="#e4e8ee"/><stop offset="1" stop-color="#e4e8ee" stop-opacity="0"/></linearGradient>
  <linearGradient id="spark" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="band" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#a3adba" stop-opacity=".16"/><stop offset="1" stop-color="#a3adba" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#27272a"/></pattern>
  <linearGradient id="fade" x1="0" x2="1"><stop offset=".4" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <mask id="m"><rect x="0" y="35" width="{W}" height="{H - 35}" fill="url(#fade)"/></mask>
  <clipPath id="mk">{''.join(clips)}</clipPath>
</defs>
<style>
  text{{font-family:{MONO}}}
  .t{{font-size:12px;fill:#a1a1aa}}
  .p{{font-size:16px;fill:#6f7a89}}
  .cmd{{font-size:16px;fill:#e4e4e7}}
  .name{{font-size:48px;font-weight:700;fill:#f4f4f5;letter-spacing:-1.5px}}
  .role{{font-size:16px;font-weight:700;fill:#e4e8ee}}
  .flip{{font-size:14px;fill:#a1a1aa}}
  .chev{{font-size:14px;fill:#6f7a89}}
  .chip{{font-size:11px;fill:#a1a1aa}}
  .ok{{font-size:11px;fill:#a1a1aa}}
  .fig{{font-size:10px;fill:#52525b}}
  .go{{font-size:13px;font-weight:700;fill:#f4f4f5}}{anim}
</style>
{chrome(W, H, "sirthabet@github: ~ — zsh")}
<g class="in" style="animation-delay:.2s"><circle class="pulse" cx="{W - 116}" cy="17.5" r="3.5" fill="#4ade80"/><text x="{W - 106}" y="21.5" class="ok">open for work</text></g>
<rect x="1" y="35" width="{W - 2}" height="{H - 36}" rx="11" fill="url(#dots)" mask="url(#m)"/>
<ellipse cx="{cx0 + mark_w / 2}" cy="{cy0 + 2 * c + 6}" rx="190" ry="96" fill="url(#glow)"/>

<text x="48" y="76" class="p">~ $</text>
<text x="82" y="76" class="cmd">{cmd}</text>{typed}
<rect class="blink" x="{82 + len(cmd) * cw + 3:.1f}" y="62" width="9" height="17" fill="#a3adba" opacity=".8"/>
<g class="in" style="animation-delay:.95s"><text x="46" y="138" class="name">Mohamed Thabet</text></g>
<g stroke-linecap="round">
  <path class="sword" d="M70 158H500" stroke="url(#blade)" stroke-width="2"/>
{glint}
  <path class="in" style="animation-delay:1.2s" d="M62 151v14M50 158h12" stroke="#a3adba" stroke-width="2.5"/>
  <rect class="in" style="animation-delay:1.2s" x="44" y="155" width="6" height="6" transform="rotate(45 47 158)" fill="#e4e8ee"/>
</g>
<g class="in" style="animation-delay:1.4s"><text x="48" y="186" class="role">Software &amp; Applied AI Engineer</text></g>
<text x="32" y="208" class="chev">›</text>
{flips}
{''.join(chips)}

{''.join(walls)}
{''.join(faces)}
{shine}
<text x="{cx0 + mark_w + depth}" y="{cy0 + 4 * c + 24}" text-anchor="end" class="fig in" style="animation-delay:1.6s">Fig. 1.</text>

<g class="in" style="animation-delay:1.8s">
  <rect class="cta" x="{cx0}" y="{btn_y}" width="{mark_w + depth}" height="38" rx="9" fill="#141418" stroke="#52525b"/>
  <text x="{cx0 + 18}" y="{btn_y + 24}" class="go">sirthabet.dev</text>
  <text x="{cx0 + mark_w + depth - 18}" y="{btn_y + 24}" text-anchor="end" class="chip">visit the site</text>
  <path class="arrow" d="M{cx0 + 134} {btn_y + 24}l8 -8M{cx0 + 136} {btn_y + 16}h6v6" stroke="#e4e8ee" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</g>
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
