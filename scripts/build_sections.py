"""data/portfolio.json から README 用の静的 SVG を assets/{light,dark}/ に書き出す。

    node scripts/sync_portfolio.mjs     # ポートフォリオから内容を取り込む
    python scripts/build_sections.py    # SVG を作り直す

セクションの構成はポートフォリオサイトと同じ（Hero / About / Works / Tech Stack / Contact）。
"""

from __future__ import annotations

import datetime as dt
import json
import re

from svgkit import PAD, ROOT, THEMES, W, deck_label, esc, open_svg, text_w, wrap, write

DATA = json.loads((ROOT / "data" / "portfolio.json").read_text(encoding="utf-8"))
PROJECTS = DATA["projects"]
HANDLE = "apt"
GITHUB = "lapt12"

CATEGORY_LABEL = {
    "language": "Language",
    "frontend": "Frontend",
    "backend": "Backend",
    "ai": "AI / ML",
    "infra": "Infra",
}
STATUS_LABEL = {"completed": "完成", "wip": "開発中"}


def year_range() -> str:
    years = sorted({p["createdAt"][:4] for p in PROJECTS})
    return years[0] if len(years) == 1 else f"{years[0]} — {years[-1]}"


def languages() -> list[str]:
    return [x["label"] for x in DATA["techs"] if x["category"] == "language" and not x["learning"]]


# ─── Hero ───────────────────────────────────────────────────────


def hero(t: dict) -> str:
    h = 480
    band_w = 2200  # textLength で帯 1 本の幅を固定し、継ぎ目なくループさせる
    css = f"""  .band {{ animation: band 60s linear infinite; }}
  @keyframes band {{ to {{ transform: translateX(-{band_w}px); }} }}
  .rise {{ transform-box: fill-box; animation: rise 1s cubic-bezier(.32,.72,0,1) both; }}
  @keyframes rise {{ from {{ transform: translateY(110%); }} }}
  .cue {{ animation: cue 2s cubic-bezier(.32,.72,0,1) infinite; }}
  @keyframes cue {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY(40px); }} }}"""
    o = [open_svg(W, h, f"{HANDLE} — Portfolio", t, css)]

    # ヘッダ（サイトの sticky ヘッダを模す）
    o.append(
        f'<text x="{PAD}" y="34" font-size="14" font-weight="700" fill="{t["body"]}">Portfolio</text>'
        f'<text x="{W - PAD}" y="34" text-anchor="end" font-size="12" fill="{t["muted"]}" word-spacing="14">About Works Tech Contact</text>'
        f'<rect class="draw" x="0" y="0" width="{W * 0.42:.0f}" height="2" fill="{t["signal"]}"/>'
    )

    # 背景を流れる輪郭の帯
    phrase = "PORTFOLIO — ENGINEER — " * 2
    o.append('<g aria-hidden="true"><g class="band">')
    for i in range(2):
        o.append(
            f'<text x="{i * band_w}" y="188" textLength="{band_w}" lengthAdjust="spacingAndGlyphs" font-size="150" '
            f'font-weight="900" letter-spacing="-6" fill="none" stroke="{t["rule_strong"]}" stroke-width="1.2">{phrase}</text>'
        )
    o.append("</g></g>")

    # 眉書き + 氏名（1 字ずつマスクからせり上がる）
    o.append(
        f'<text class="fade" x="{PAD}" y="222" font-size="13" letter-spacing="2" fill="{t["subtle"]}">PORTFOLIO / {year_range()}</text>'
    )
    o.append(
        f'<clipPath id="nm"><rect x="0" y="228" width="{W}" height="196"/></clipPath><g clip-path="url(#nm)">'
        f'<text class="rise" style="animation-delay:.3s" x="{PAD - 8}" y="386" font-size="190" '
        f'font-weight="800" letter-spacing="-7" fill="{t["body"]}">{esc(HANDLE)}</text></g>'
    )

    # 肩書き（左）と柱（右）
    after = .3 + len(HANDLE) * .07 + .4
    o.append(
        f'<text class="up" style="animation-delay:{after - .15:.2f}s" x="{PAD}" y="{h - 30}" font-size="16" fill="{t["muted"]}">{esc(DATA["tagline"])}</text>'
    )
    meta = [("Stack", " · ".join(languages())), ("Works", f"{len(PROJECTS)} projects"), ("GitHub", f"@{GITHUB}")]
    mx = W - PAD
    for term, val in reversed(meta):
        vw = max(text_w(val, 13), text_w(term, 13))
        mx -= vw
        o.append(
            f'<g class="up" style="animation-delay:{after:.2f}s">'
            f'<text x="{mx:.1f}" y="{h - 66}" font-size="13" fill="{t["subtle"]}">{term}</text>'
            f'<text x="{mx:.1f}" y="{h - 44}" font-size="13" fill="{t["body"]}">{esc(val)}</text></g>'
        )
        mx -= 36
    o.append(
        f'<line class="draw" style="animation-delay:{after - .4:.2f}s" x1="{PAD}" y1="{h - 12}" x2="{W - PAD}" y2="{h - 12}" stroke="{t["body"]}"/>'
    )
    o.append("</svg>")
    return "\n".join(o)


# ─── About ──────────────────────────────────────────────────────


def about(t: dict) -> str:
    size, lh = 28, 1.6
    paras = [re.sub(r"\s*\n\s*", "", p).strip() for p in re.split(r"\n{2,}", DATA["bio"])]
    paras = [p for p in paras if p]
    lines: list[str | None] = []
    for i, p in enumerate(paras):
        if i:
            lines.append(None)  # 段落の間
        lines.extend(wrap(p, size, W - PAD * 2, bold=True))

    top = 96
    h = int(top + sum(size * lh if ln else size * .9 for ln in lines) + 40)
    # サイトはスクロールに合わせて 1 字ずつ墨が乗る。README では行ごとに順に濃くする
    css = f"""  .ink {{ animation: ink .9s cubic-bezier(.32,.72,0,1) both; }}
  @keyframes ink {{ from {{ fill-opacity: .14; }} }}"""
    o = [open_svg(W, h, "About", t, css), deck_label(PAD, 44, "About", "Introduction", t)]
    y, n = top, 0
    for ln in lines:
        if ln is None:
            y += size * .9
            continue
        o.append(
            f'<text class="ink" style="animation-delay:{.3 + n * .35:.2f}s" x="{PAD}" y="{y + size:.0f}" font-size="{size}" '
            f'font-weight="700" letter-spacing="-.3" fill="{t["body"]}">{esc(ln)}</text>'
        )
        y += size * lh
        n += 1
    o.append("</svg>")
    return "\n".join(o)


# ─── Works ──────────────────────────────────────────────────────


def badge(x: float, y: float, status: str, t: dict) -> tuple[str, float]:
    c = t["sage"] if status == "completed" else t["sand"]
    bg = t["tint_sage"] if status == "completed" else t["tint_sand"]
    label = STATUS_LABEL[status]
    bw = text_w(label, 11) + 26
    return (
        f'<rect x="{x}" y="{y}" width="{bw:.1f}" height="20" rx="2" fill="{bg}" stroke="{c}"/>'
        f'<circle cx="{x + 9}" cy="{y + 10}" r="3" fill="{c}"/>'
        f'<text x="{x + 17}" y="{y + 14.5}" font-size="11" font-weight="600" fill="{c}">{label}</text>'
    ), bw


def works(t: dict) -> str:
    col_year, col_idx, col_body = PAD, 170, 214
    body_w = W - PAD - col_body - 110
    rows = []
    for i, p in enumerate(PROJECTS):
        tl = wrap(p["tagline"], 14, body_w)
        rows.append((i, p, tl, 112 + len(tl) * 22))

    h = 96 + sum(r[3] for r in rows) + 30
    o = [open_svg(W, h, "Works", t), deck_label(PAD, 44, "Works", "Selected works", t)]
    y = 84
    last_year = None
    for i, p, tl, rh in rows:
        year = p["createdAt"][:4]
        d = f"animation-delay:{.15 + i * .07:.2f}s"
        o.append(f'<g class="up" style="{d}">')
        o.append(f'<line x1="{col_idx}" y1="{y}" x2="{W - PAD}" y2="{y}" stroke="{t["rule"]}"/>')
        if year != last_year:
            o.append(f'<line x1="{col_year}" y1="{y}" x2="{col_idx - 24}" y2="{y}" stroke="{t["body"]}"/>')
            o.append(f'<text x="{col_year}" y="{y + 44}" font-size="24" font-weight="700" fill="{t["body"]}">{year}</text>')
            last_year = year
        o.append(f'<text x="{col_idx}" y="{y + 40}" class="mono" font-size="12" fill="{t["subtle"]}">{i + 1:02d}</text>')
        o.append(
            f'<text x="{col_body}" y="{y + 50}" font-size="32" font-weight="700" letter-spacing="-.8" fill="{t["body"]}">{esc(p["title"])}</text>'
        )
        o.append(
            f'<text x="{W - PAD}" y="{y + 36}" text-anchor="end" class="mono" font-size="12" fill="{t["subtle"]}">{p["createdAt"]}</text>'
        )
        b, bw = badge(col_body, y + 64, p["status"], t)
        o.append(b)
        o.append(f'<text x="{col_body + bw + 10:.1f}" y="{y + 78.5}" font-size="12" fill="{t["subtle"]}">{esc(p["primaryLang"])}</text>')
        for j, ln in enumerate(tl):
            o.append(f'<text x="{col_body}" y="{y + 112 + j * 22}" font-size="14" fill="{t["muted"]}">{esc(ln)}</text>')
        o.append("</g>")
        y += rh
    o.append(f'<line x1="{col_idx}" y1="{y}" x2="{W - PAD}" y2="{y}" stroke="{t["rule"]}"/>')
    o.append("</svg>")
    return "\n".join(o)


# ─── Tech Stack ─────────────────────────────────────────────────


def tech(t: dict) -> str:
    techs = [x for x in DATA["techs"] if not x["learning"]]
    groups = [(c, [x for x in techs if x["category"] == c]) for c in CATEGORY_LABEL]
    groups = [(c, items) for c, items in groups if items]

    def usage(tid: str) -> str:
        ps = [p for p in PROJECTS if tid in p["tech"]]
        if not ps:
            return ""
        ys = sorted({p["createdAt"][:4] for p in ps})
        span = ys[0] if len(ys) == 1 else f"{ys[0]}–{ys[-1]}"
        return f"{len(ps)} project{'s' if len(ps) > 1 else ''} · {span}"

    cols, gap = 3, 12
    cw = (W - PAD * 2 - 140 - gap * (cols - 1)) / cols
    grid_h = sum(28 + ((len(items) + cols - 1) // cols) * (58 + gap) + 20 for _, items in groups)
    h = int(300 + grid_h)

    # 輪郭の巨大な技術名が 2 段で逆向きに流れる
    labels = [x["label"] for x in techs]
    row = " ".join(labels) + " "
    band_w = max(1400, int(text_w(row, 64, True) * 1.05))
    css = f"""  .ma {{ animation: ma 50s linear infinite; }}
  .mb {{ animation: mb 50s linear infinite; }}
  @keyframes ma {{ to {{ transform: translateX(-{band_w}px); }} }}
  @keyframes mb {{ from {{ transform: translateX(-{band_w}px); }} to {{ transform: translateX(0); }} }}"""
    o = [open_svg(W, h, "Tech Stack", t, css), deck_label(PAD, 44, "Tech Stack", "Tools and languages", t)]

    def band(y: float, cls: str, offset: int) -> None:
        o.append(f'<g class="{cls}" aria-hidden="true">')
        for k in range(2):
            x = k * band_w
            for j, lab in enumerate(labels):
                filled = (j + offset) % 3 == 0
                attrs = f'fill="{t["body"]}"' if filled else f'fill="none" stroke="{t["body"]}" stroke-width="1.2"'
                o.append(f'<text x="{x:.0f}" y="{y}" font-size="64" font-weight="800" letter-spacing="-2" {attrs}>{esc(lab)}</text>')
                x += text_w(lab, 64, True) + 48
        o.append("</g>")

    band(140, "ma", 2)
    band(216, "mb", 0)

    y = 272
    o.append(f'<line x1="{PAD + 110}" y1="{y - 16}" x2="{PAD + 110}" y2="{h - 24}" stroke="{t["rule"]}"/>')
    n = 0
    for c, items in groups:
        o.append(
            f'<text class="fade" x="{PAD + 140}" y="{y + 10}" font-size="12" font-weight="600" letter-spacing="1.6" fill="{t["muted"]}">{CATEGORY_LABEL[c].upper()}</text>'
        )
        y += 28
        for k, x_ in enumerate(items):
            cx = PAD + 140 + (k % cols) * (cw + gap)
            cy = y + (k // cols) * (58 + gap)
            u = usage(x_["id"])
            o.append(
                f'<g class="up" style="animation-delay:{.1 + n * .05:.2f}s">'
                f'<rect x="{cx:.1f}" y="{cy}" width="{cw:.1f}" height="58" rx="2" fill="{t["canvas"]}" stroke="{t["rule"]}"/>'
                f'<text x="{cx + 14:.1f}" y="{cy + (25 if u else 34)}" font-size="14" font-weight="500" fill="{t["body"]}">{esc(x_["label"])}</text>'
                + (f'<text x="{cx + 14:.1f}" y="{cy + 44}" font-size="11.5" fill="{t["subtle"]}">{u}</text>' if u else "")
                + "</g>"
            )
            n += 1
        y += ((len(items) + cols - 1) // cols) * (58 + gap) + 20
    o.append("</svg>")
    return "\n".join(o)


# ─── Contact ────────────────────────────────────────────────────


def contact(t: dict) -> str:
    h = 400
    o = [open_svg(W, h, "Contact", t), deck_label(PAD, 44, "Contact", "Get in touch", t)]
    o.append(
        f'<text class="up" style="animation-delay:.1s" x="{PAD - 4}" y="150" font-size="92" font-weight="800" letter-spacing="-4" fill="{t["body"]}">Let’s build</text>'
    )
    o.append(
        f'<text class="up" style="animation-delay:.2s" x="{PAD - 4}" y="240" font-size="92" font-weight="800" letter-spacing="-4" fill="{t["body"]}">'
        f'something<tspan dx="28">→</tspan></text>'
    )
    o.append(f'<line class="draw" style="animation-delay:.4s" x1="{PAD}" y1="282" x2="{W * .62:.0f}" y2="282" stroke="{t["rule"]}"/>')
    # GitHub マーク（Octicons mark-github 16px）
    o.append(
        f'<g class="fade" style="animation-delay:.5s"><path transform="translate({PAD} 302)" fill="{t["body"]}" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8Z"/>'
        f'<text x="{PAD + 26}" y="315" font-size="14" fill="{t["body"]}">GitHub</text>'
        f'<text x="{PAD + 84}" y="315" class="mono" font-size="12" fill="{t["subtle"]}">@{GITHUB}</text></g>'
    )
    o.append(f'<line x1="{PAD}" y1="{h - 52}" x2="{W - PAD}" y2="{h - 52}" stroke="{t["rule"]}"/>')
    o.append(
        f'<text x="{PAD}" y="{h - 24}" font-size="12" fill="{t["subtle"]}">© {dt.date.today().year} {HANDLE}</text>'
        f'<text x="{W - PAD}" y="{h - 24}" text-anchor="end" font-size="12" fill="{t["subtle"]}">Content synced from the portfolio site.</text>'
    )
    o.append("</svg>")
    return "\n".join(o)


# ─── README の作品詳細 ──────────────────────────────────────────


def readme_works() -> None:
    """README の WORKS マーカー間を、作品ごとの折りたたみ詳細で置き換える。"""
    blocks = []
    for i, p in enumerate(PROJECTS):
        hl = "\n".join(f"- {h}" for h in p["highlights"])
        blocks.append(
            f"<details>\n<summary><code>{i + 1:02d}</code> <b>{esc(p['title'])}</b> — {esc(p['tagline'])}</summary>\n\n"
            f"> {p['description']}\n\n{hl}\n\n"
            f"<sub>{p['createdAt']} · {STATUS_LABEL[p['status']]} · {p['primaryLang']}</sub>\n\n</details>"
        )
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    start, end = "<!-- WORKS:START -->", "<!-- WORKS:END -->"
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    path.write_text(f"{head}{start}\n{chr(10).join(blocks)}\n{end}{tail}", encoding="utf-8")


def main() -> None:
    for name, t in THEMES.items():
        write("hero.svg", name, hero(t))
        write("about.svg", name, about(t))
        write("works.svg", name, works(t))
        write("tech.svg", name, tech(t))
        write("contact.svg", name, contact(t))
    readme_works()
    print(f"sections: {len(PROJECTS)} works × {len(THEMES)} themes")


if __name__ == "__main__":
    main()
