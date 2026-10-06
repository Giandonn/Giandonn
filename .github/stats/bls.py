"""Kit visual do perfil: preto/marfim/prata na linha Black Label Society (Order of the Black + bullseye do Zakk).
Todo texto vira <path>, então o SVG renderiza igual em qualquer lugar do GitHub."""
import math
import os
import re

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "..", "assets")

BLACK = "#070707"
INK = "#131313"
STEEL = "#2c2a27"
ASH = "#5c5850"
SILVER = "#9c968b"
BONE = "#ece5d3"

FONTS = {
    "goth": TTFont(os.path.join(HERE, "fonts", "UnifrakturCook-Bold.ttf")),
    "caps": TTFont(os.path.join(HERE, "fonts", "CinzelBlack.ttf")),
    "anton": TTFont(os.path.join(HERE, "fonts", "Anton.ttf")),
}


def _num(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def _glyphs(font, s, size, tracking):
    f = FONTS[font]
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    scale = size / f["head"].unitsPerEm
    width, glyphs = 0.0, []
    for ch in s:
        name = cmap.get(ord(ch))
        if name is None:
            continue
        adv = hmtx[name][0] * scale
        glyphs.append((name, width, adv))
        width += adv + tracking
    return f.getGlyphSet(), scale, glyphs, width - tracking


def text(font, s, size, x, y, tracking=0.0, anchor="start"):
    """(d, largura) do texto como path; y é a baseline."""
    gs, scale, glyphs, width = _glyphs(font, s, size, tracking)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    pen = SVGPathPen(gs, ntos=_num)
    for name, off, _ in glyphs:
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x + off, y)))
    return pen.getCommands()


def width(font, s, size, tracking=0.0):
    return _glyphs(font, s, size, tracking)[3]


def text_arc(font, s, size, cx, cy, r, side="top", tracking=0.0):
    """Texto centrado num arco, como os rockers de um patch de motoclube.
    top: lido em cima, base no raio r e letras para fora. bottom: lido embaixo, letras para dentro."""
    gs, scale, glyphs, total = _glyphs(font, s, size, tracking)
    pen = SVGPathPen(gs, ntos=_num)
    sign = 1 if side == "top" else -1
    start = math.radians(-90 if side == "top" else 90) - sign * (total / 2) / r
    for name, off, adv in glyphs:
        a = start + sign * (off + adv / 2) / r
        t = a + sign * math.pi / 2
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        c, s_ = math.cos(t), math.sin(t)
        gs[name].draw(TransformPen(pen, (scale * c, scale * s_, scale * s_, -scale * c,
                                         px - adv / 2 * c, py - adv / 2 * s_)))
    return pen.getCommands()


def icon(name):
    """(d, largura_viewbox, altura_viewbox) de um ícone em icons/."""
    with open(os.path.join(HERE, "icons", f"{name}.svg"), encoding="utf-8") as fh:
        svg_ = fh.read()
    _, _, w, h = (float(v) for v in re.search(r'viewBox="([^"]+)"', svg_).group(1).split())
    return " ".join(re.findall(r' d="([^"]+)"', svg_)), w, h


def place_icon(name, cx, cy, size, fill, extra=""):
    """Ícone centrado em (cx, cy), lado maior = size."""
    d, w, h = icon(name)
    s = size / max(w, h)
    return (f'<path d="{d}" fill="{fill}" transform="translate({_num(cx - w * s / 2)} {_num(cy - h * s / 2)}) '
            f'scale({s:.4f})" {extra}/>')


def bullseye(cx, cy, r, rings=9, spin=None):
    """Alvo preto/marfim da Les Paul do Zakk; spin = segundos de uma volta do brilho de vinil."""
    out = []
    for i in range(rings):
        rr = r * (rings - i) / rings
        out.append(f'<circle cx="{_num(cx)}" cy="{_num(cy)}" r="{_num(rr)}" fill="{BONE if i % 2 else BLACK}"/>')
    if spin:
        k = r * 1.05
        wedge = (f"M{_num(cx)},{_num(cy)} L{_num(cx - k * 0.30)},{_num(cy - k)} L{_num(cx + k * 0.30)},{_num(cy - k)} Z "
                 f"M{_num(cx)},{_num(cy)} L{_num(cx - k * 0.30)},{_num(cy + k)} L{_num(cx + k * 0.30)},{_num(cy + k)} Z")
        out.append(f'<clipPath id="be{int(cx)}{int(cy)}"><circle cx="{_num(cx)}" cy="{_num(cy)}" r="{_num(r)}"/></clipPath>')
        out.append(f'<g clip-path="url(#be{int(cx)}{int(cy)})"><path d="{wedge}" fill="#fff" opacity="0.16" filter="url(#soft)">'
                   f'<animateTransform attributeName="transform" type="rotate" from="0 {_num(cx)} {_num(cy)}" '
                   f'to="360 {_num(cx)} {_num(cy)}" dur="{spin}s" repeatCount="indefinite"/></path></g>')
    return "".join(out)


def _logo_paths(part):
    with open(os.path.join(HERE, "icons", "bls-logo.svg"), encoding="utf-8") as fh:
        paths = re.findall(r'data-tone="(\w+)" data-part="(\w+)" d="([^"]+)"', fh.read())
    paths = [(tone, d) for tone, p, d in paths if part == "all" or p == part]
    nums = [float(v) for _, d in paths for v in re.findall(r"-?\d+(?:\.\d+)?", d)]
    xs, ys = nums[0::2], nums[1::2]
    return paths, (min(xs), min(ys), max(xs), max(ys))


def bls_logo(cx, cy, size, fg=BONE, bg=BLACK, part="all"):
    """Logo do Black Label Society centrado em (cx, cy), lado maior = size. part: all, skull ou letters."""
    paths, (x0, y0, x1, y1) = _logo_paths(part)
    s = size / max(x1 - x0, y1 - y0)
    tx, ty = cx - (x0 + x1) / 2 * s, cy - (y0 + y1) / 2 * s
    body = "".join(f'<path d="{d}" fill="{fg if tone == "fg" else bg}"/>' for tone, d in paths)
    return f'<g transform="translate({_num(tx)} {_num(ty)}) scale({s:.4f})">{body}</g>'


def skull(cx, cy, size, fg=BONE, bg=BLACK):
    """A caveira do logo do BLS."""
    return bls_logo(cx, cy, size, fg, bg, part="skull")


def defs(seed=11, grain=0.10):
    return f"""<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="{seed}"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.93  0 0 0 0 0.9  0 0 0 0 0.83  0 0 0 {grain} 0"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>
  <filter id="distress" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.07" numOctaves="4" seed="{seed + 3}" result="t"/>
    <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -14 10.9" result="speck"/>
    <feComposite in="SourceGraphic" in2="speck" operator="in"/>
  </filter>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
  <radialGradient id="spot" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{BONE}" stop-opacity="0.13"/><stop offset="1" stop-color="{BONE}" stop-opacity="0"/>
  </radialGradient>
</defs>"""


def rule(x, y, w, color=BONE):
    """Filete duplo (grosso + fino), acabamento de rótulo antigo."""
    return (f'<rect x="{_num(x)}" y="{_num(y)}" width="{_num(w)}" height="3" fill="{color}"/>'
            f'<rect x="{_num(x)}" y="{_num(y + 7)}" width="{_num(w)}" height="1" fill="{color}" opacity="0.6"/>')


def section_head(num, label, x=40, y=40, width_=1200, icon_name="skull"):
    """Cabeçalho de card: algarismo romano num selo + título gótico + filete duplo."""
    nw = width("caps", num, 30)
    box = max(nw + 30, 58)
    lx = x + box + 24
    lw = width("goth", label, 64)
    rail = lx + lw + 26
    end = x + width_ - (70 if icon_name else 0)
    out = [
        f'<rect x="{x}" y="{y + 2}" width="{_num(box)}" height="58" fill="{BONE}"/>',
        f'<rect x="{x + 5}" y="{y + 7}" width="{_num(box - 10)}" height="48" fill="none" stroke="{BLACK}" stroke-width="1.5"/>',
        f'<path d="{text("caps", num, 30, x + box / 2, y + 43, anchor="middle")}" fill="{BLACK}"/>',
        f'<path d="{text("goth", label, 64, lx, y + 52)}" fill="{BONE}" filter="url(#distress)"/>',
        rule(rail, y + 26, end - rail - (16 if icon_name else 0)),
    ]
    if icon_name == "skull":
        out.append(skull(x + width_ - 30, y + 31, 56))
    elif icon_name:
        out.append(place_icon(icon_name, x + width_ - 30, y + 31, 50, BONE))
    return "\n".join(out)


def frame(w, h):
    return (f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" fill="none" stroke="{STEEL}" stroke-width="8"/>'
            f'<rect x="14" y="14" width="{w - 28}" height="{h - 28}" fill="none" stroke="{BONE}" stroke-width="1.2" opacity="0.55"/>')


def svg(w, h, body, seed=11, grain=0.10, border=True):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{defs(seed, grain)}
<rect width="{w}" height="{h}" fill="{BLACK}"/>
{body}
<rect width="{w}" height="{h}" filter="url(#grain)" fill="#000"/>
{frame(w, h) if border else ""}
</svg>"""


def write(name, content):
    os.makedirs(ASSETS, exist_ok=True)
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"{name:14} {len(content) // 1024} KB")
