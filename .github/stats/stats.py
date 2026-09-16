"""Gera assets/stats.svg (estatisticas do perfil na estetica RATM XX).
Uso: GITHUB_TOKEN=... python .github/stats/stats.py"""
import json
import os
import urllib.request
from collections import Counter

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

LOGIN = "Giandonn"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "assets", "stats.svg")

FONTS = {
    "anton": TTFont(os.path.join(HERE, "fonts", "Anton.ttf")),
    "type": TTFont(os.path.join(HERE, "fonts", "CourierPrime.ttf")),
}

# Estilo/markup e notebooks (saidas salvas inflam o tamanho) distorcem o ranking.
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


def text_path(font, text, size, x, y, tracking=0.0, anchor="start"):
    f = FONTS[font]
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    scale = size / f["head"].unitsPerEm
    width, glyphs = 0.0, []
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            continue
        glyphs.append((name, width))
        width += hmtx[name][0] * scale + tracking
    width -= tracking
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    pen = SVGPathPen(gs, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
    for name, off in glyphs:
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x + off, y)))
    return pen.getCommands()


def fmt(n):
    return f"{n:,}".replace(",", ".")


def render(u):
    W, H = 1280, 600
    cc = u["contributionsCollection"]
    repos = u["repositories"]
    langs = Counter()
    for r in repos["nodes"]:
        for e in r["languages"]["edges"]:
            if e["node"]["name"] not in IGNORED_LANGS:
                langs[e["node"]["name"]] += e["size"]
    total_size = sum(langs.values()) or 1
    top = langs.most_common(6)

    numbers = [
        (fmt(cc["totalCommitContributions"] + cc["restrictedContributionsCount"]), "COMMITS / 12 MESES"),
        (fmt(u["pullRequests"]["totalCount"]), "PULL REQUESTS"),
        (fmt(repos["totalCount"]), "REPOSITÓRIOS"),
        (fmt(sum(r["stargazerCount"] for r in repos["nodes"])), "ESTRELAS"),
    ]

    parts = []
    add = parts.append
    add(f'<path d="{text_path("type", "BOLETIM DE OCORRÊNCIAS", 18, 40, 52, tracking=2)}" fill="#8c8c8c"/>')
    add('<rect x="40" y="66" width="560" height="3" fill="#e8e8e8"/>')
    for i, (val, label) in enumerate(numbers):
        x, y = 40 + (i % 2) * 290, 170 + (i // 2) * 130
        add(f'<path d="{text_path("anton", val, 78, x, y)}" fill="#f2f2f2" filter="url(#distress)"/>')
        add(f'<path d="{text_path("type", label, 15, x + 2, y + 30, tracking=1.5)}" fill="#7a7a7a"/>')

    lx = 680
    add(f'<path d="{text_path("type", "LINGUAGENS EM USO", 18, lx, 52, tracking=2)}" fill="#8c8c8c"/>')
    add(f'<rect x="{lx}" y="66" width="560" height="3" fill="#e8e8e8"/>')
    shades = ["#f2f2f2", "#cfcfcf", "#adadad", "#8c8c8c", "#6e6e6e", "#555555"]
    for i, (name, size) in enumerate(top):
        y = 112 + i * 52
        pct = size / total_size
        add(f'<path d="{text_path("anton", name.upper(), 24, lx, y, tracking=2)}" fill="#e0e0e0"/>')
        add(f'<path d="{text_path("type", f"{pct * 100:.1f}%", 16, lx + 560, y, anchor="end")}" fill="#8c8c8c"/>')
        add(f'<rect x="{lx}" y="{y + 10}" width="560" height="10" fill="#1c1c1c"/>')
        add(f'<rect x="{lx}" y="{y + 10}" width="{max(560 * pct, 4):.1f}" height="10" fill="{shades[i]}"/>')

    cal = cc["contributionCalendar"]
    weeks = cal["weeks"][-53:]
    gy = 430
    title = f"FREQUÊNCIA DE ATAQUE  //  {fmt(cal['totalContributions'])} CONTRIBUIÇÕES NO ANO"
    add(f'<path d="{text_path("type", title, 16, 40, gy - 14, tracking=1.5)}" fill="#8c8c8c"/>')
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=0) or 1
    ramp = ["#161616", "#3a3a3a", "#6e6e6e", "#adadad", "#f2f2f2"]
    cell, gap = 19, 3.2
    for wi, w in enumerate(weeks):
        for di, d in enumerate(w["contributionDays"]):
            c = d["contributionCount"]
            lvl = 0 if c == 0 else min(4, 1 + int(3 * c / peak))
            add(f'<rect x="{40 + wi * (cell + gap):.1f}" y="{gy + di * (cell + gap):.1f}" width="{cell}" height="{cell}" fill="{ramp[lvl]}"/>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="23"/>
    <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.09 0"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>
  <filter id="distress" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="4" seed="7" result="t"/>
    <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -14 10.7" result="speck"/>
    <feComposite in="SourceGraphic" in2="speck" operator="in"/>
  </filter>
</defs>
<rect width="{W}" height="{H}" fill="#0a0a0a"/>
{chr(10).join(parts)}
<rect width="{W}" height="{H}" filter="url(#grain)" fill="#000"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="none" stroke="#2a2a2a" stroke-width="2"/>
</svg>"""


if __name__ == "__main__":
    svg = render(fetch())
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("stats.svg", len(svg) // 1024, "KB")
