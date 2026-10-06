"""Gera assets/stats.svg (card de estatísticas do perfil, rodado diariamente pela Action).
Uso: GITHUB_TOKEN=... python .github/stats/stats.py"""
import json
import os
import urllib.request
from collections import Counter

from bls import ASH, BLACK, BONE, INK, SILVER, STEEL, _num, rule, section_head, skull, svg, text, write

LOGIN = "Giandonn"

# Estilo/markup e notebooks (saídas salvas inflam o tamanho) distorcem o ranking.
IGNORED_LANGS = {"CSS", "SCSS", "Less", "HTML", "Jupyter Notebook"}

QUERY = """
query($login: String!) {
  user(login: $login) {
    pullRequests { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount } }
      }
    }
  }
}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    body = json.load(urllib.request.urlopen(req))
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]["user"]


def fmt(n):
    return f"{n:,}".replace(",", ".")


def render(u):
    W, H = 1280, 706
    cc = u["contributionsCollection"]
    repos = u["repositories"]
    langs = Counter()
    for r in repos["nodes"]:
        for e in r["languages"]["edges"]:
            if e["node"]["name"] not in IGNORED_LANGS:
                langs[e["node"]["name"]] += e["size"]
    total_size = sum(langs.values()) or 1

    numbers = [
        (fmt(cc["totalCommitContributions"] + cc["restrictedContributionsCount"]), "COMMITS / 12 MESES"),
        (fmt(u["pullRequests"]["totalCount"]), "PULL REQUESTS"),
        (fmt(repos["totalCount"]), "REPOSITÓRIOS"),
        (fmt(sum(r["stargazerCount"] for r in repos["nodes"])), "ESTRELAS"),
    ]

    parts = [section_head("III", "Registros", icon_name=None)]
    add = parts.append

    # Placar: 4 blocos, o primeiro em marfim.
    bw, bh, top = 136, 124, 144
    for i, (val, label) in enumerate(numbers):
        x = 40 + (i % 2) * (bw * 2 + 20)
        y = top + (i // 2) * (bh + 16)
        hot = i == 0
        add(f'<rect x="{x}" y="{y}" width="{bw * 2 + 4}" height="{bh}" fill="{BONE if hot else INK}" stroke="{BONE if hot else STEEL}" stroke-width="1.5"/>')
        if not hot:
            add(f'<rect x="{x}" y="{y}" width="5" height="{bh}" fill="{SILVER}"/>')
        add(f'<path d="{text("anton", val, 70, x + 22, y + 82)}" fill="{BLACK if hot else BONE}" filter="url(#distress)"/>')
        add(f'<path d="{text("caps", label, 13, x + 24, y + 108, tracking=2)}" fill="{BLACK if hot else SILVER}"/>')
    add(skull(40 + bw * 2 - 22, top + 30, 30, BLACK))

    # Linguagens.
    lx, lw = 640, 600
    add(f'<path d="{text("caps", "LINGUAGENS EM USO", 15, lx, top + 12, tracking=3)}" fill="{SILVER}"/>')
    shades = [BONE, "#c9c2b2", SILVER, "#7b766d", ASH, "#4a4741"]
    for i, (name, size) in enumerate(langs.most_common(6)):
        y = top + 50 + i * 44
        pct = size / total_size
        add(f'<path d="{text("caps", name.upper(), 19, lx, y, tracking=2)}" fill="{BONE}"/>')
        add(f'<path d="{text("anton", f"{pct * 100:.1f}%", 22, lx + lw, y, anchor="end")}" fill="{BONE if i == 0 else SILVER}"/>')
        add(f'<rect x="{lx}" y="{y + 7}" width="{lw}" height="9" fill="{INK}"/>')
        add(f'<rect x="{lx}" y="{y + 7}" width="{_num(max(lw * pct, 4))}" height="9" fill="{shades[i]}"/>')

    # Calendário de contribuições.
    cal = cc["contributionCalendar"]
    weeks = cal["weeks"][-53:]
    gy = 500
    add(rule(40, gy - 52, 1200, STEEL))
    add(f'<path d="{text("goth", "The Blessed Hellride", 36, 40, gy - 6)}" fill="{BONE}"/>')
    add(f'<path d="{text("caps", f"{fmt(cal['totalContributions'])} CONTRIBUIÇÕES NOS ÚLTIMOS 12 MESES", 13, 1240, gy - 10, tracking=2, anchor="end")}" fill="{SILVER}"/>')
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=0) or 1
    ramp = [INK, "#3a3733", "#6d6860", "#aaa396", BONE]
    cell, gap = 18.8, 3.8
    ox = 40 + (1200 - (len(weeks) * (cell + gap) - gap)) / 2
    for wi, w in enumerate(weeks):
        for di, d in enumerate(w["contributionDays"]):
            c = d["contributionCount"]
            lvl = 0 if c == 0 else min(4, 1 + int(3 * c / peak))
            add(f'<rect x="{_num(ox + wi * (cell + gap))}" y="{_num(gy + 14 + di * (cell + gap))}" width="{cell}" height="{cell}" fill="{ramp[lvl]}"/>')

    return svg(W, H, "\n".join(parts), seed=61)


if __name__ == "__main__":
    write("stats.svg", render(fetch()))
