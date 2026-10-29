"""Fetch public GitHub contributions and render an animated steel heatmap SVG.

No token, no GraphQL: scrapes https://github.com/users/<user>/contributions.
Run: python scripts/render_heatmap.py   (STATIC=1 for a frozen frame)
"""

import json
import os
import re
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USER", "MohamedThabt")
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "assets" / "contrib-heatmap.svg"
STATIC = os.environ.get("STATIC") == "1"

# Steel ramp, matching the --steel-* tokens on sirthabet.dev
PALETTE = ["#1c1d22", "#2f3540", "#4a5361", "#6f7a89", "#a3adba", "#e4e8ee"]

W, H = 860, 252
X0, Y0 = 44, 74
STEP, CELL = 14.6, 11.4


def fetch():
    html = requests.get(
        f"https://github.com/users/{USERNAME}/contributions",
        headers={"User-Agent": "profile-heatmap"},
        timeout=30,
    ).text
    soup = BeautifulSoup(html, "html.parser")
    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        tip = tips.get(td.get("id"), "")
        m = re.match(r"(\d[\d,]*) contribution", tip)
        days.append({
            "date": td["data-date"],
            "level": int(td.get("data-level", 0)),
            "count": int(m.group(1).replace(",", "")) if m else 0,
        })
    days.sort(key=lambda d: d["date"])
    return days


def stats(days):
    total = sum(d["count"] for d in days)
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    current = 0
    tail = list(days)
    if tail and not tail[-1]["count"]:
        tail = tail[:-1]  # today may simply not have started yet
    for d in reversed(tail):
        if not d["count"]:
            break
        current += 1
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    monthly = defaultdict(int)
    for d in days:
        monthly[d["date"][:7]] += d["count"]
    return {
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "active_days": sum(1 for d in days if d["count"]),
        "monthly": dict(monthly),
    }


def render(days, s):
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)  # back to Sunday
    cells, months, last_month = [], [], None
    for d in days:
        day = date.fromisoformat(d["date"])
        col, row = (day - start).days // 7, (day.weekday() + 1) % 7
        x, y = X0 + col * STEP, Y0 + row * STEP
        delay = (col + row) * 0.018
        cells.append(
            f'<rect class="c" x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2.4" '
            f'fill="{PALETTE[min(d["level"], 4) + (1 if d["count"] >= 20 else 0)]}" '
            f'style="animation-delay:{delay:.3f}s"/>'
        )
        if row == 0 and day.month != last_month and day.day <= 7 and col < 52:
            months.append(f'<text class="lbl" x="{x:.1f}" y="{Y0 - 8}">{day.strftime("%b")}</text>')
            last_month = day.month

    weekdays = "".join(
        f'<text class="lbl" x="{X0 - 10}" y="{Y0 + r * STEP + 9.5:.1f}" text-anchor="end">{n}</text>'
        for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )
    legend_x = W - 32 - 6 * 15 - 64
    legend = "".join(
        f'<rect x="{legend_x + 34 + i * 15}" y="{H - 38}" width="11" height="11" rx="2.4" fill="{c}"/>'
        for i, c in enumerate(PALETTE)
    )
    best = s["best_day"]
    best_label = date.fromisoformat(best["date"]).strftime("%b %d") if best["date"] else "-"
    footer = [
        (f'{s["total"]:,}', "contributions"),
        (f'{s["current_streak"]}d', "current streak"),
        (f'{s["longest_streak"]}d', "longest streak"),
        (f'{best["count"]}', f"best day · {best_label}"),
    ]
    foot = "".join(
        f'<text x="{32 + i * 132}" y="{H - 28}" class="v f" style="animation-delay:{1.6 + i * 0.12:.2f}s">{v}'
        f'<tspan class="k" dx="6">{k}</tspan></text>'
        for i, (v, k) in enumerate(footer)
    )
    anim = "" if STATIC else """
  .c{animation:drop .5s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:center}
  .f{animation:fade .6s ease-out both}
  @keyframes drop{from{opacity:0;transform:translateY(-6px) scale(.6)}to{opacity:1;transform:none}}
  @keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{s['total']} GitHub contributions in the last year">
<style>
  text{{font-family:'JetBrains Mono','SFMono-Regular',Consolas,monospace}}
  .lbl{{font-size:10px;fill:#71717a}}
  .t{{font-size:12px;fill:#a1a1aa}}
  .v{{font-size:13px;font-weight:700;fill:#f4f4f5}}
  .k{{font-size:11px;font-weight:400;fill:#71717a}}{anim}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="#0e0e11" stroke="#27272a"/>
<path d="M.5 34.5h{W - 1}" stroke="#27272a"/>
<circle cx="20" cy="17.5" r="5" fill="#3f3f46"/><circle cx="37" cy="17.5" r="5" fill="#3f3f46"/><circle cx="54" cy="17.5" r="5" fill="#3f3f46"/>
<text x="{W / 2}" y="21.5" text-anchor="middle" class="t">github.com/{USERNAME} · last 12 months</text>
{''.join(months)}{weekdays}
{''.join(cells)}
<path d="M24.5 {H - 56.5}h{W - 49}" stroke="#27272a" stroke-dasharray="2 4"/>
{foot}
<text x="{legend_x}" y="{H - 28}" class="lbl">less</text>{legend}<text x="{legend_x + 34 + 6 * 15 + 2}" y="{H - 28}" class="lbl">more</text>
</svg>
"""


def main():
    days = fetch()
    if not days:
        raise SystemExit("No contribution cells found — GitHub markup may have changed.")
    s = stats(days)
    DATA.parent.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps({"user": USERNAME, "stats": s, "days": days}, indent=1))
    OUT.write_text(render(days, s), encoding="utf-8")
    print(f"{len(days)} days · {s['total']} contributions -> {OUT.name}")


if __name__ == "__main__":
    main()
