"""SVG 生成の共通部品。ポートフォリオサイト（lapt12/portfolio）の Editorial Deck に合わせる。

- 地は生成り、墨はほぼ黒。装飾は罫線・面・活字だけで、影も光彩も角丸も使わない
- 見出しは「— ラベル / 欧文キャプション」の二段
- アクセントは朱。文字には accent、塗り・線には signal を使う
- 数値は「大きな数字 + 小さな単位」で組む

トークンは portfolio/src/index.css の :root / [data-theme="dark"] と同じ値。
README では <picture> でライト / ダークを出し分けるため、テーマごとに書き出す。
"""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

THEMES = {
    "light": {
        "canvas": "#f6f5f1",
        "surface": "#eeece6",
        "elevated": "#e6e3dc",
        "body": "#111111",
        "muted": "#5c5c5c",
        "subtle": "#676767",
        "rule": "#d8d6cf",
        "rule_strong": "#aeaba3",
        "accent": "#b8390f",
        "signal": "#ff4d1c",
        "sage": "#3a7259",
        "sand": "#85601f",
        "tint_sage": "#e4eae3",
        "tint_sand": "#f0e8da",
    },
    "dark": {
        "canvas": "#141412",
        "surface": "#1e1d1a",
        "elevated": "#292824",
        "body": "#f2f0ea",
        "muted": "#a8a49b",
        "subtle": "#918d84",
        "rule": "#302e29",
        "rule_strong": "#4b4840",
        "accent": "#ff7a50",
        "signal": "#ff4d1c",
        "sage": "#7cba9d",
        "sand": "#d7ab6d",
        "tint_sage": "#1b2622",
        "tint_sand": "#2a241a",
    },
}

FONT = (
    "system-ui, -apple-system, 'Helvetica Neue', 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', "
    "'Noto Sans JP', 'BIZ UDPGothic', Meiryo, sans-serif"
)
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

W = 900  # README の版面幅
PAD = 48  # 左右の余白

# 行頭に来てはいけない文字（簡易禁則）
NO_HEAD = set("、。，．・：；？！）」』】〉》ー々ぁぃぅぇぉっゃゅょァィゥェォッャュョ,.:;!?)]}%")

esc = html.escape


def is_wide(c: str) -> bool:
    return ord(c) > 0x2E80


def text_w(s: str, size: float, bold: bool = False) -> float:
    """大まかな文字幅。全角 1em、半角はボールドで 0.6em / 標準で 0.55em。"""
    narrow = 0.6 if bold else 0.55
    total = 0.0
    for c in s:
        if is_wide(c):
            total += size
        elif c == " ":
            total += size * 0.28
        elif c in "il.,:;'|!":
            total += size * 0.28
        elif c.isdigit():
            total += size * 0.57
        elif c in "mwMW":
            total += size * (narrow + 0.25)
        elif c.isupper():
            total += size * (narrow + 0.08)
        else:
            total += size * narrow
    return total


def wrap(s: str, size: float, width: float, bold: bool = False) -> list[str]:
    """幅で折り返す。英単語は割らず、禁則文字は前の行に残す。"""
    tokens: list[str] = []
    buf = ""
    for c in s:
        if is_wide(c) or c == " ":
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(c)
        else:
            buf += c
    if buf:
        tokens.append(buf)

    lines, cur = [], ""
    for t in tokens:
        if cur and text_w(cur + t, size, bold) > width and not (t[0] in NO_HEAD):
            lines.append(cur.rstrip())
            cur = t.lstrip()
        else:
            cur += t
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def open_svg(w: int, h: int, title: str, t: dict, extra_css: str = "") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>
  text {{ font-family: {FONT}; }}
  .mono {{ font-family: {MONO}; }}
  /* 既定は最終状態。アニメーションが止まる環境でも内容が欠けないよう、from 側だけを書く */
  .up {{ animation: up .9s cubic-bezier(.32,.72,0,1) both; }}
  .fade {{ animation: fade .9s cubic-bezier(.32,.72,0,1) both; }}
  .draw {{ transform-box: fill-box; transform-origin: left center; animation: draw 1.1s cubic-bezier(.32,.72,0,1) both; }}
  @keyframes up {{ from {{ opacity: 0; transform: translateY(14px); }} }}
  @keyframes fade {{ from {{ opacity: 0; }} }}
  @keyframes draw {{ from {{ transform: scaleX(0); }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
{extra_css}
</style>
<rect width="{w}" height="{h}" fill="{t['canvas']}"/>
"""


def deck_label(x: float, y: float, label: str, caption: str, t: dict, delay: float = 0) -> str:
    """サイトの SectionLabel。「—— LABEL / Caption」"""
    return (
        f'<g class="fade" style="animation-delay:{delay:.2f}s">'
        f'<line x1="{x}" y1="{y - 4.5}" x2="{x + 24}" y2="{y - 4.5}" stroke="{t["muted"]}"/>'
        f'<text x="{x + 36}" y="{y}" font-size="13" fill="{t["body"]}">'
        f'<tspan font-weight="600" letter-spacing="1.8">{esc(label.upper())}</tspan>'
        f'<tspan dx="8" letter-spacing=".4" fill="{t["subtle"]}">/ {esc(caption)}</tspan></text>'
        f"</g>"
    )


def write(name: str, theme: str, svg: str) -> None:
    p = ASSETS / theme / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(svg, encoding="utf-8")
