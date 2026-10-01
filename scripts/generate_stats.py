"""GitHub の統計を取得して assets/{light,dark}/activity.svg を書き出す。

使い方:
    GH_TOKEN=xxxx python scripts/generate_stats.py

GitHub Actions (.github/workflows/stats.yml) から毎日実行される。
プライベートリポジトリの数値も含めたい場合は repo / read:user スコープを持つ
PAT を Secrets の GH_STATS_TOKEN に登録する。
"""

from __future__ import annotations

import datetime as dt
import json
import os
import urllib.request
from collections import defaultdict

from svgkit import PAD, THEMES, W, deck_label, esc, open_svg, text_w, write

USERNAME = os.environ.get("GH_USER", "lapt12")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

# 言語グラフから除外する言語 (マークアップ等で比率が歪む場合に追加する)
EXCLUDED_LANGS = {"HTML", "CSS", "Jupyter Notebook", "Batchfile", "Shell", "Dockerfile", "TeX"}

def gql(query: str, variables: dict | None = None) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]


def fetch() -> dict:
    base = gql(
        """
        query($login: String!) {
          user(login: $login) {
            createdAt
            followers { totalCount }
            contributionsCollection { contributionYears }
            pullRequests { totalCount }
            issues { totalCount }
          }
        }
        """,
        {"login": USERNAME},
    )["user"]

    years = sorted(base["contributionsCollection"]["contributionYears"])
    commits_by_year: dict[int, int] = {}
    days: dict[str, int] = {}
    total_contrib = 0
    for year in years:
        c = gql(
            """
            query($login: String!, $from: DateTime!, $to: DateTime!) {
              user(login: $login) {
                contributionsCollection(from: $from, to: $to) {
                  totalCommitContributions
                  restrictedContributionsCount
                  contributionCalendar {
                    totalContributions
                    weeks { contributionDays { date contributionCount } }
                  }
                }
              }
            }
            """,
            {"login": USERNAME, "from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"},
        )["user"]["contributionsCollection"]
        # 権限の無いプライベート分は restricted にまとめられるため合算する
        commits_by_year[year] = c["totalCommitContributions"] + c["restrictedContributionsCount"]
        total_contrib += c["contributionCalendar"]["totalContributions"]
        for w in c["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]

    repos, stars, langs = 0, 0, defaultdict(lambda: {"size": 0, "color": "#888"})
    cursor = None
    while True:
        r = gql(
            """
            query($login: String!, $cursor: String) {
              user(login: $login) {
                repositories(ownerAffiliations: OWNER, isFork: false, first: 100, after: $cursor) {
                  pageInfo { hasNextPage endCursor }
                  nodes {
                    stargazerCount
                    languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                      edges { size node { name color } }
                    }
                  }
                }
              }
            }
            """,
            {"login": USERNAME, "cursor": cursor},
        )["user"]["repositories"]
        for n in r["nodes"]:
            repos += 1
            stars += n["stargazerCount"]
            for e in n["languages"]["edges"]:
                name = e["node"]["name"]
                if name in EXCLUDED_LANGS:
                    continue
                langs[name]["size"] += e["size"]
                langs[name]["color"] = e["node"]["color"] or "#888"
        if not r["pageInfo"]["hasNextPage"]:
            break
        cursor = r["pageInfo"]["endCursor"]

    return {
        "created": base["createdAt"][:10],
        "followers": base["followers"]["totalCount"],
        "prs": base["pullRequests"]["totalCount"],
        "issues": base["issues"]["totalCount"],
        "commits_by_year": commits_by_year,
        "total_commits": sum(commits_by_year.values()),
        "total_contrib": total_contrib,
        "days": days,
        "repos": repos,
        "stars": stars,
        "langs": dict(langs),
    }


def streaks(days: dict[str, int]) -> tuple[int, int]:
    today = dt.date.today()
    ordered = sorted((dt.date.fromisoformat(k), v) for k, v in days.items() if dt.date.fromisoformat(k) <= today)
    longest = run = 0
    for _, v in ordered:
        run = run + 1 if v > 0 else 0
        longest = max(longest, run)
    current = 0
    for i, (d, v) in enumerate(reversed(ordered)):
        if v > 0:
            current += 1
        elif i == 0:  # 今日まだコミットしていない場合は昨日から数える
            continue
        else:
            break
    return current, longest


def fmt(n: int) -> str:
    return f"{n:,}"


def caption(x: float, y: float, label: str, t: dict) -> str:
    return f'<text x="{x}" y="{y}" font-size="12" font-weight="600" letter-spacing="1.6" fill="{t["muted"]}">{esc(label)}</text>'


def activity(s: dict, t: dict) -> str:
    cur, longest = streaks(s["days"])
    inner = W - PAD * 2
    years = sorted(s["commits_by_year"].items())
    langs = sorted(s["langs"].items(), key=lambda kv: -kv[1]["size"])[:8]
    lang_total = sum(v["size"] for _, v in langs) or 1

    y_numbers = 84
    y_years = y_numbers + 150
    y_heat = y_years + 40 + len(years) * 24 + 24
    cell, gap = 12, 3
    y_lang = y_heat + 40 + 7 * (cell + gap) + 44
    h = y_lang + 96

    o = [open_svg(W, h, f"{USERNAME} GitHub activity", t), deck_label(PAD, 44, "Activity", "GitHub in numbers", t)]

    # 大きな数字 + 小さな単位
    cols = [
        ("Commits", s["total_commits"], "commits", f"since {s['created'][:4]}"),
        ("Contributions", s["total_contrib"], "total", f"PR {s['prs']} · Stars {s['stars']}"),
        ("Repositories", s["repos"], "repos", "owned, non-fork"),
        ("Longest streak", longest, "days", f"current {cur} days"),
    ]
    cw = inner / len(cols)
    o.append(f'<line x1="{PAD}" y1="{y_numbers}" x2="{W - PAD}" y2="{y_numbers}" stroke="{t["body"]}" class="draw"/>')
    for i, (label, val, unit, sub) in enumerate(cols):
        x = PAD + i * cw + (0 if i == 0 else 20)
        num = fmt(val)
        o.append(
            f'<g class="up" style="animation-delay:{.1 + i * .08:.2f}s">'
            f'<text x="{x:.1f}" y="{y_numbers + 30}" font-size="12" fill="{t["subtle"]}">{label}</text>'
            f'<text x="{x:.1f}" y="{y_numbers + 88}" fill="{t["body"]}"><tspan font-size="52" font-weight="700" letter-spacing="-1.5">{num}</tspan>'
            f'<tspan dx="6" font-size="14" fill="{t["muted"]}">{unit}</tspan></text>'
            f'<text x="{x:.1f}" y="{y_numbers + 114}" font-size="12" fill="{t["subtle"]}">{esc(sub)}</text></g>'
        )
        if i:
            o.append(f'<line x1="{PAD + i * cw:.1f}" y1="{y_numbers + 16}" x2="{PAD + i * cw:.1f}" y2="{y_numbers + 120}" stroke="{t["rule"]}"/>')
    o.append(f'<line x1="{PAD}" y1="{y_numbers + 136}" x2="{W - PAD}" y2="{y_numbers + 136}" stroke="{t["rule"]}"/>')

    # 年別コミット
    o.append(caption(PAD, y_years + 24, "COMMITS BY YEAR", t))
    peak = max([v for _, v in years] + [1])
    bar_x, bar_w = PAD + 70, inner - 70 - 70
    for i, (year, v) in enumerate(years):
        yy = y_years + 48 + i * 24
        o.append(
            f'<text x="{PAD}" y="{yy + 5}" class="mono" font-size="12" fill="{t["subtle"]}">{year}</text>'
            f'<rect x="{bar_x}" y="{yy - 3}" width="{bar_w}" height="6" fill="{t["surface"]}"/>'
            f'<rect class="draw" style="animation-delay:{.3 + i * .1:.2f}s" x="{bar_x}" y="{yy - 3}" width="{max(2, v / peak * bar_w):.1f}" height="6" fill="{t["signal"]}"/>'
            f'<text x="{W - PAD}" y="{yy + 5}" text-anchor="end" class="mono" font-size="12" fill="{t["body"]}">{fmt(v)}</text>'
        )

    # 草（直近 53 週）。signal の濃淡で 5 段階
    today = dt.date.today()
    start = today - dt.timedelta(days=(today.weekday() + 1) % 7 + 52 * 7)
    window = {k: v for k, v in s["days"].items() if start <= dt.date.fromisoformat(k) <= today}
    peak_d = max(window.values(), default=1) or 1
    o.append(caption(PAD, y_heat + 24, "LAST 12 MONTHS", t))
    o.append(
        f'<text x="{W - PAD}" y="{y_heat + 24}" text-anchor="end" font-size="12" fill="{t["subtle"]}">'
        f'<tspan font-weight="700" fill="{t["body"]}">{sum(window.values()):,}</tspan> contributions</text>'
    )
    gx, gy = PAD + 30, y_heat + 56
    last_month = None
    for wk in range(53):
        first = start + dt.timedelta(days=wk * 7)
        if first.month != last_month and first.day <= 7:
            o.append(f'<text x="{gx + wk * (cell + gap)}" y="{gy - 8}" font-size="10" fill="{t["subtle"]}">{first:%b}</text>')
            last_month = first.month
        for d in range(7):
            day = first + dt.timedelta(days=d)
            if day > today:
                continue
            v = s["days"].get(day.isoformat(), 0)
            lv = 0 if v == 0 else min(4, 1 + int(v / peak_d * 3.999))
            fill = f'fill="{t["surface"]}" stroke="{t["rule"]}" stroke-width=".5"' if lv == 0 else f'fill="{t["signal"]}" fill-opacity="{lv * .25:.2f}"'
            o.append(
                f'<rect class="fade" style="animation-delay:{wk * .012:.3f}s" x="{gx + wk * (cell + gap)}" y="{gy + d * (cell + gap)}" '
                f'width="{cell}" height="{cell}" {fill}><title>{day}: {v}</title></rect>'
            )
    for label, row in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
        o.append(f'<text x="{PAD}" y="{gy + row * (cell + gap) + 10}" font-size="10" fill="{t["subtle"]}">{label}</text>')

    # 言語構成（言語色はサイトでも色数制約の例外）
    o.append(caption(PAD, y_lang + 4, "LANGUAGES", t))
    o.append(f'<clipPath id="lb"><rect x="{PAD}" y="{y_lang + 22}" width="{inner}" height="8"/></clipPath><g clip-path="url(#lb)">')
    x = float(PAD)
    for i, (name, v) in enumerate(langs):
        bw = v["size"] / lang_total * inner
        o.append(f'<rect class="draw" style="animation-delay:{.2 + i * .06:.2f}s" x="{x:.2f}" y="{y_lang + 22}" width="{bw + .5:.2f}" height="8" fill="{v["color"]}"/>')
        x += bw
    o.append("</g>")
    x = float(PAD)
    ly = y_lang + 56
    for name, v in langs:
        pct = f"{v['size'] / lang_total * 100:.1f}%"
        iw = 14 + text_w(name, 12) + 6 + text_w(pct, 12) + 22
        if x + iw > W - PAD:
            x, ly = float(PAD), ly + 22
        o.append(
            f'<rect x="{x:.1f}" y="{ly - 9}" width="8" height="8" fill="{v["color"]}"/>'
            f'<text x="{x + 14:.1f}" y="{ly}" font-size="12" fill="{t["body"]}">{esc(name)}'
            f'<tspan class="mono" fill="{t["subtle"]}" dx="6">{pct}</tspan></text>'
        )
        x += iw
    o.append(
        f'<text x="{W - PAD}" y="{h - 14}" text-anchor="end" font-size="10" fill="{t["subtle"]}">updated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d} UTC · includes private repositories</text>'
    )
    o.append("</svg>")
    return "\n".join(o)

def main() -> None:
    if not TOKEN:
        raise SystemExit("GH_TOKEN が設定されていません")
    s = fetch()
    for name, t in THEMES.items():
        write("activity.svg", name, activity(s, t))
    print(f"commits={s['total_commits']} contributions={s['total_contrib']} repos={s['repos']}")


if __name__ == "__main__":
    main()
