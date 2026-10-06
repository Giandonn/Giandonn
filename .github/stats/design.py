"""Gera as peças fixas do perfil (banner, sobre, arsenal, rodapé).
Uso: python .github/stats/design.py"""
from bls import (ASH, BLACK, BONE, INK, SILVER, STEEL, bullseye, place_icon, rule, section_head, skull, svg, text,
                 text_arc, width, write, _num)

W = 1280


def emblem(cx, cy, r, top, bottom, spin=None):
    """Patch de motoclube: anel com rockers em arco, alvo do Zakk no miolo e caveira por cima."""
    band = r * 0.17
    inner = r - band - 8
    sep = r - band / 2 - 4
    dots = "".join(f'<circle cx="{_num(cx + sx * sep * 0.985)}" cy="{_num(cy + 11)}" r="5" fill="{BONE}"/>' for sx in (-1, 1))
    return f"""
<circle cx="{cx}" cy="{cy}" r="{r + 26}" fill="url(#spot)"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BLACK}" stroke="{BONE}" stroke-width="6"/>
<circle cx="{cx}" cy="{cy}" r="{r - 11}" fill="none" stroke="{BONE}" stroke-width="1.5"/>
<path d="{text_arc("caps", top, band * 0.62, cx, cy, inner + 13, "top", tracking=5)}" fill="{BONE}"/>
<path d="{text_arc("caps", bottom, band * 0.55, cx, cy, r - 24, "bottom", tracking=6)}" fill="{BONE}"/>
{dots}
<circle cx="{cx}" cy="{cy}" r="{inner}" fill="none" stroke="{BONE}" stroke-width="2.5"/>
{bullseye(cx, cy, inner - 9, rings=9, spin=spin)}
{skull(cx, cy + 6, inner * 0.92, BONE, BLACK, stroke=inner * 0.07)}
"""


def banner():
    H = 560
    ex, ey, er = 990, 282, 238
    name_w = width("goth", "Giandonn", 176)
    band_txt = "STACK LABEL SOCIETY"
    band_w = width("caps", band_txt, 34, tracking=6)
    left = 70
    body = f"""
<g opacity="0.07">{bullseye(ex, ey, 620, rings=14)}</g>
{emblem(ex, ey, er, "FULL STACK BERZERKER", "S.D.M.F.  ·  BRASIL", spin=9)}
<path d="{text("caps", "DESENVOLVEDOR FULL STACK  ·  CAPÍTULO BRASIL", 16, left + 2, 104, tracking=3)}" fill="{SILVER}"/>
{rule(left, 118, name_w - 6, SILVER)}
<path d="{text("goth", "Giandonn", 176, left + 6, 288)}" fill="{STEEL}"/>
<path d="{text("goth", "Giandonn", 176, left, 282)}" fill="{BONE}" filter="url(#distress)"/>
<path d="M{left - 6},318 Q{_num(left + band_w / 2 + 20)},298 {_num(left + band_w + 46)},318 L{_num(left + band_w + 46)},372 Q{_num(left + band_w / 2 + 20)},352 {left - 6},372 Z" fill="{BONE}"/>
<path d="{text("caps", band_txt, 34, left + 20, 357, tracking=6)}" fill="{BLACK}"/>
<path d="{text("caps", "STRENGTH · DETERMINATION · MERGE · FOREVER", 17, left + 2, 420, tracking=3.2)}" fill="{BONE}"/>
<path d="{text("caps", "PHP  /  LARAVEL  /  JAVA  /  REACT  /  VUE  /  TS", 14, left + 2, 498, tracking=2)}" fill="{ASH}"/>
<rect x="{left}" y="452" width="56" height="2" fill="{SILVER}"/>
<path d="{text("caps", "MMXXVI", 24, 0, 0, tracking=10)}" fill="{SILVER}" transform="translate(1242 40) rotate(90)"/>
"""
    return svg(W, H, body, seed=11, grain=0.08)


def sobre():
    H = 470
    rows = [
        ("NOME", "GIANDONN"),
        ("FUNÇÃO", "DESENVOLVEDOR FULL STACK"),
        ("CAPÍTULO", "BRASIL"),
        ("EM CAMPO", "APIs, painéis e apps"),
        ("JURAMENTO", "código legível é código livre"),
        ("STATUS", "NA ESTRADA"),
    ]
    parts = [section_head("I", "Sobre", icon_name="skull")]
    for i, (k, v) in enumerate(rows):
        y = 172 + i * 40
        kw = width("caps", k, 17, tracking=2)
        parts.append(f'<path d="{text("caps", k, 17, 40, y, tracking=2)}" fill="{SILVER}"/>')
        parts.append(f'<path d="{text("caps", "." * max(2, 14 - len(k)), 17, 48 + kw, y, tracking=2)}" fill="{STEEL}"/>')
        vx = 270
        if k == "STATUS":
            parts.append(f'<circle cx="{vx + 8}" cy="{y - 7}" r="7" fill="{BONE}"><animate attributeName="opacity" values="1;1;0.15;0.15" keyTimes="0;0.5;0.5;1" dur="1.4s" repeatCount="indefinite"/></circle>')
            vx += 28
        parts.append(f'<path d="{text("caps", v, 19, vx, y, tracking=1.5)}" fill="{BONE}"/>')

    cx, cy, r = 1015, 236, 128
    parts.append(f"""<g transform="rotate(-8 {cx} {cy})" filter="url(#distress)" opacity="0.93">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BONE}" stroke-width="6"/>
  <circle cx="{cx}" cy="{cy}" r="{r - 12}" fill="none" stroke="{BONE}" stroke-width="1.5"/>
  <circle cx="{cx}" cy="{cy}" r="{r - 48}" fill="none" stroke="{BONE}" stroke-width="2"/>
  <path d="{text_arc("caps", "MEMBRO VITALÍCIO", 17, cx, cy, r - 41, "top", tracking=2.5)}" fill="{BONE}"/>
  <path d="{text_arc("caps", "S.D.M.F.", 18, cx, cy, r - 19, "bottom", tracking=8)}" fill="{BONE}"/>
  <circle cx="{cx - r + 30}" cy="{cy + 12}" r="3.5" fill="{BONE}"/><circle cx="{cx + r - 30}" cy="{cy + 12}" r="3.5" fill="{BONE}"/>
  {skull(cx, cy + 2, 92, BONE)}
</g>""")

    parts.append(f'<rect x="0" y="{H - 76}" width="{W}" height="76" fill="{BONE}"/>')
    parts.append(f'<rect x="0" y="{H - 84}" width="{W}" height="2" fill="{BONE}" opacity="0.6"/>')
    q = "SEM FRAMEWORK MÁGICO   ·   SEM DEPLOY NA SEXTA   ·   SEM MEDO DO LEGADO"
    parts.append(f'<path d="{text("caps", q, 20, W / 2, H - 31, tracking=2.5, anchor="middle")}" fill="{BLACK}"/>')
    parts.append(skull(64, H - 38, 32, BLACK) + skull(W - 64, H - 38, 32, BLACK))
    return svg(W, H, "\n".join(parts), seed=31)


def arsenal():
    items = [("php", "PHP"), ("laravel", "LARAVEL"), ("java", "JAVA"), ("typescript", "TYPESCRIPT"),
             ("react", "REACT"), ("vuedotjs", "VUE"), ("mysql", "MYSQL"), ("supabase", "SUPABASE"),
             ("docker", "DOCKER"), ("python", "PYTHON"), ("git", "GIT"), (None, "E O QUE VIER")]
    cols, gap, tw_, th = 6, 16, (1200 - 5 * 16) / 6, 170
    H = 40 + 64 + 34 + 2 * th + gap + 44
    parts = [section_head("II", "Arsenal", icon_name="guitar")]
    for i, (slug, label) in enumerate(items):
        x = 40 + (i % cols) * (tw_ + gap)
        y = 138 + (i // cols) * (th + gap)
        cx = x + tw_ / 2
        parts.append(f'<rect x="{_num(x)}" y="{y}" width="{_num(tw_)}" height="{th}" fill="{INK}" stroke="{STEEL}" stroke-width="1.5"/>')
        if slug is None:
            parts.append(f'<circle cx="{_num(cx)}" cy="{y + 74}" r="49" fill="none" stroke="{BONE}" stroke-width="1.5"/>')
            parts.append(bullseye(cx, y + 74, 44, rings=7, spin=4))
            parts.append(f'<path d="{text("caps", label, 19, cx, y + 142, tracking=2, anchor="middle")}" fill="{BONE}"/>')
            parts.append(f'<rect x="{_num(cx - 14)}" y="{y + 152}" width="28" height="2" fill="{SILVER}"/>')
            continue
        parts.append(rule(x + 10, y + 10, tw_ - 20, STEEL))
        parts.append(f'<path d="{text("caps", f"Nº {i + 1:02d}", 12, x + 12, y + 38, tracking=1.5)}" fill="{ASH}"/>')
        parts.append(place_icon(slug, cx, y + 76, 56, BONE))
        parts.append(f'<path d="{text("caps", label, 19, cx, y + 142, tracking=2, anchor="middle")}" fill="{BONE}"/>')
        parts.append(f'<rect x="{_num(cx - 14)}" y="{y + 152}" width="28" height="2" fill="{SILVER}"/>')
    return svg(W, int(H), "\n".join(parts), seed=41)


def rodape():
    H = 230
    phrase = "Stronger Than Tech Debt"
    pw = width("goth", phrase, 88)
    body = f"""
<g opacity="0.05">{bullseye(W / 2, H / 2, 700, rings=22)}</g>
{skull(W / 2 - pw / 2 - 70, 92, 66, BONE)}
{skull(W / 2 + pw / 2 + 70, 92, 66, BONE)}
<path d="{text("goth", phrase, 88, W / 2, 124, anchor="middle")}" fill="{BONE}" filter="url(#distress)"/>
<path d="{text("caps", "—  GIANDONN  ·  S.D.M.F.  ·  MMXXVI  —", 18, W / 2, 180, tracking=4, anchor="middle")}" fill="{SILVER}"/>
"""
    return svg(W, H, body, seed=51, grain=0.1)


if __name__ == "__main__":
    write("banner.svg", banner())
    write("sobre.svg", sobre())
    write("arsenal.svg", arsenal())
    write("footer.svg", rodape())
