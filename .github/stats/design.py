"""Gera as peças fixas do perfil (banner, sobre, arsenal, rodapé).
Uso: python .github/stats/design.py"""
import math

from bls import (ASH, BLACK, BONE, INK, SILVER, STEEL, bullseye, place_icon, rule, section_head, skull, svg, text,
                 text_arc, width, write, _num)

W = 1280


def _arc_band(cx, cy, ri, ro, half, side):
    """Faixa em arco entre os raios ri e ro, centrada no topo ou na base."""
    c = -90 if side == "top" else 90
    a1, a2 = math.radians(c - half), math.radians(c + half)

    def p(r, a):
        return f"{_num(cx + r * math.cos(a))},{_num(cy + r * math.sin(a))}"

    return f"M{p(ro, a1)} A{_num(ro)},{_num(ro)} 0 0 1 {p(ro, a2)} L{p(ri, a2)} A{_num(ri)},{_num(ri)} 0 0 0 {p(ri, a1)} Z"


def rocker(cx, cy, ri, ro, half, side, label, size):
    """Rocker de colete de motoclube: faixa marfim, costura tracejada e letra gótica."""
    base = ri + (ro - ri) * 0.24 if side == "top" else ro - (ro - ri) * 0.24
    return (f'<path d="{_arc_band(cx, cy, ri, ro, half, side)}" fill="{BONE}" stroke="{BLACK}" stroke-width="3"/>'
            f'<path d="{_arc_band(cx, cy, ri + 6, ro - 6, half - 1.6, side)}" fill="none" stroke="{BLACK}" stroke-width="1.4" stroke-dasharray="5 4"/>'
            f'<path d="{text_arc("goth", label, size, cx, cy, base, side, tracking=1.5)}" fill="{BLACK}"/>')


def patch(cx, cy, label, w=96, h=40):
    """Patch retangular pequeno com borda bordada."""
    return (f'<rect x="{_num(cx - w / 2)}" y="{_num(cy - h / 2)}" width="{w}" height="{h}" rx="4" fill="{BONE}" stroke="{BLACK}" stroke-width="3"/>'
            f'<rect x="{_num(cx - w / 2 + 5)}" y="{_num(cy - h / 2 + 5)}" width="{w - 10}" height="{h - 10}" rx="2" fill="none" stroke="{BLACK}" stroke-width="1.2" stroke-dasharray="4 3"/>'
            f'<path d="{text("caps", label, 15, cx, cy + 6, tracking=1.5, anchor="middle")}" fill="{BLACK}"/>')


def colors(cx, cy, r, spin=None):
    """Colete completo: rocker de cima, centro com o alvo do Zakk e a caveira, rocker de baixo."""
    ri, ro = r + 18, r + 82
    return f"""
<circle cx="{cx}" cy="{cy}" r="{ro + 30}" fill="url(#spot)"/>
{rocker(cx, cy, ri, ro, 56, "top", "Black Label", 50)}
{rocker(cx, cy, ri, ro, 40, "bottom", "Society", 50)}
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BLACK}" stroke="{BONE}" stroke-width="5"/>
<circle cx="{cx}" cy="{cy}" r="{r - 9}" fill="none" stroke="{BONE}" stroke-width="1.3" stroke-dasharray="5 4"/>
{bullseye(cx, cy, r - 17, rings=9, spin=spin)}
{skull(cx, cy + 5, (r - 17) * 0.8, BONE, BLACK, stroke=r * 0.06)}
"""


def banner():
    H = 560
    ex, ey, er = 985, 280, 140
    name_w = width("goth", "Giandonn", 176)
    band_txt = "DOOM CREW INC."
    band_w = width("caps", band_txt, 34, tracking=7)
    left = 70
    body = f"""
<g opacity="0.07">{bullseye(ex, ey, 620, rings=14)}</g>
{colors(ex, ey, er, spin=9)}
{patch(ex - er - 78, ey + 4, "S.D.M.F.")}
<path d="{text("caps", "DESENVOLVEDOR FULL STACK  ·  BERZERKER BRASIL", 16, left + 2, 104, tracking=2.6)}" fill="{SILVER}"/>
{rule(left, 118, name_w - 6, SILVER)}
<path d="{text("goth", "Giandonn", 176, left + 6, 288)}" fill="{STEEL}"/>
<path d="{text("goth", "Giandonn", 176, left, 282)}" fill="{BONE}" filter="url(#distress)"/>
<path d="M{left - 6},318 Q{_num(left + band_w / 2 + 20)},298 {_num(left + band_w + 46)},318 L{_num(left + band_w + 46)},372 Q{_num(left + band_w / 2 + 20)},352 {left - 6},372 Z" fill="{BONE}"/>
<path d="{text("caps", band_txt, 34, left + 20, 357, tracking=7)}" fill="{BLACK}"/>
<path d="{text("caps", "STRENGTH · DETERMINATION · MERCILESS · FOREVER", 16, left + 2, 420, tracking=2.6)}" fill="{BONE}"/>
<path d="{text("caps", "PHP  /  LARAVEL  /  JAVA  /  REACT  /  VUE  /  TS", 14, left + 2, 498, tracking=2)}" fill="{ASH}"/>
<rect x="{left}" y="452" width="56" height="2" fill="{SILVER}"/>
<path d="{text("caps", "MMXXVI", 24, 0, 0, tracking=10)}" fill="{SILVER}" transform="translate(1242 40) rotate(90)"/>
"""
    return svg(W, H, body, seed=11, grain=0.08)


def sobre():
    H = 470
    rows = [
        ("NOME", "GIANDONN"),
        ("OFÍCIO", "DESENVOLVEDOR FULL STACK"),
        ("PATENTE", "BERZERKER"),
        ("CAPÍTULO", "BRASIL"),
        ("CREW", "DOOM CREW INC."),
        ("STATUS", "ON THE ROAD"),
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

    cx, cy, r = 1010, 232, 134
    parts.append(f"""<g transform="rotate(-7 {cx} {cy})" filter="url(#distress)" opacity="0.94">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BONE}" stroke-width="6"/>
  <circle cx="{cx}" cy="{cy}" r="{r - 11}" fill="none" stroke="{BONE}" stroke-width="1.3" stroke-dasharray="5 4"/>
  <circle cx="{cx}" cy="{cy}" r="{r - 50}" fill="none" stroke="{BONE}" stroke-width="2"/>
  <path d="{text_arc("caps", "STRENGTH · DETERMINATION", 13.5, cx, cy, r - 41, "top", tracking=1.6)}" fill="{BONE}"/>
  <path d="{text_arc("caps", "MERCILESS · FOREVER", 13.5, cx, cy, r - 21, "bottom", tracking=2.4)}" fill="{BONE}"/>
  <circle cx="{cx - r + 31}" cy="{cy + 6}" r="4" fill="{BONE}"/><circle cx="{cx + r - 31}" cy="{cy + 6}" r="4" fill="{BONE}"/>
  {skull(cx, cy - 8, 62, BONE)}
  <path d="{text("caps", "S.D.M.F.", 17, cx, cy + 50, tracking=3, anchor="middle")}" fill="{BONE}"/>
</g>""")

    parts.append(f'<rect x="0" y="{H - 76}" width="{W}" height="76" fill="{BONE}"/>')
    parts.append(f'<rect x="0" y="{H - 84}" width="{W}" height="2" fill="{BONE}" opacity="0.6"/>')
    q = "ORDER OF THE BLACK   ·   IN ZAKK WE TRUST   ·   HAIL THE BERZERKERS"
    parts.append(f'<path d="{text("caps", q, 20, W / 2, H - 31, tracking=2.5, anchor="middle")}" fill="{BLACK}"/>')
    parts.append(skull(64, H - 38, 32, BLACK) + skull(W - 64, H - 38, 32, BLACK))
    return svg(W, H, "\n".join(parts), seed=31)


def arsenal():
    items = [("php", "PHP"), ("laravel", "LARAVEL"), ("java", "JAVA"), ("typescript", "TYPESCRIPT"),
             ("react", "REACT"), ("vuedotjs", "VUE"), ("mysql", "MYSQL"), ("supabase", "SUPABASE"),
             ("docker", "DOCKER"), ("python", "PYTHON"), ("git", "GIT"), (None, "FIRE IT UP")]
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
    H = 250
    phrase = "Stronger Than Death"
    pw = width("goth", phrase, 92)
    disco = ("SONIC BREW · STRONGER THAN DEATH · 1919 ETERNAL · THE BLESSED HELLRIDE · MAFIA · SHOT TO HELL · "
             "ORDER OF THE BLACK · CATACOMBS OF THE BLACK VATICAN · GRIMMEST HITS · DOOM CREW INC.")
    body = f"""
<g opacity="0.05">{bullseye(W / 2, H / 2, 700, rings=22)}</g>
{skull(W / 2 - pw / 2 - 70, 88, 66, BONE)}
{skull(W / 2 + pw / 2 + 70, 88, 66, BONE)}
<path d="{text("goth", phrase, 92, W / 2, 122, anchor="middle")}" fill="{BONE}" filter="url(#distress)"/>
<path d="{text("caps", "—  GIANDONN  ·  BERZERKER  ·  S.D.M.F.  ·  MMXXVI  —", 18, W / 2, 170, tracking=4, anchor="middle")}" fill="{SILVER}"/>
{rule(60, 190, W - 120, STEEL)}
<path d="{text("caps", disco, 11 * min(1, (W - 140) / width("caps", disco, 11, tracking=1.6)), W / 2, 222, tracking=1.2, anchor="middle")}" fill="{ASH}"/>
"""
    return svg(W, H, body, seed=51, grain=0.1)


if __name__ == "__main__":
    write("banner.svg", banner())
    write("sobre.svg", sobre())
    write("arsenal.svg", arsenal())
    write("footer.svg", rodape())
