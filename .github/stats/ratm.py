"""Kit visual do perfil: pôster de propaganda preto/vermelho/creme (vibe RATM).
Todo texto vira <path>, então o SVG renderiza igual em qualquer lugar do GitHub."""
import math
import os
import random
import re

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "..", "assets")

BLACK = "#0b0b0b"
INK = "#161616"
RED = "#d10f1f"
RED_DARK = "#6e0710"
CREAM = "#efe6d2"
GREY = "#8a8378"

FONTS = {
    "anton": TTFont(os.path.join(HERE, "fonts", "Anton.ttf")),
    "type": TTFont(os.path.join(HERE, "fonts", "CourierPrime.ttf")),
}


def _num(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def text(font, s, size, x, y, tracking=0.0, anchor="start"):
    """(d, largura) do texto como path; y é a baseline."""
    f = FONTS[font]
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    scale = size / f["head"].unitsPerEm
    width, glyphs = 0.0, []
    for ch in s:
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
    pen = SVGPathPen(gs, ntos=_num)
    for name, off in glyphs:
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x + off, y)))
    return pen.getCommands(), width


def icon(name):
    """(d, largura_viewbox, altura_viewbox) de um ícone em icons/."""
    with open(os.path.join(HERE, "icons", f"{name}.svg"), encoding="utf-8") as fh:
        svg = fh.read()
    _, _, w, h = (float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split())
    return " ".join(re.findall(r' d="([^"]+)"', svg)), w, h


def place_icon(name, x, y, size, fill, extra=""):
    d, w, h = icon(name)
    s = size / max(w, h)
    return f'<path d="{d}" fill="{fill}" transform="translate({_num(x)} {_num(y)}) scale({s:.4f})" {extra}/>'


def star(cx, cy, r, rot=-90):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.382
        a = math.radians(rot + i * 36)
        pts.append(f"{_num(cx + rr * math.cos(a))},{_num(cy + rr * math.sin(a))}")
    return "M" + " L".join(pts) + " Z"


def rays(cx, cy, n, length, width_deg=None):
    """Raios de sol estilo propaganda soviética, centrados em (cx, cy)."""
    step = 360 / n
    half = (width_deg or step / 2) / 2
    out = []
    for i in range(n):
        a = i * step
        p1 = (cx + length * math.cos(math.radians(a - half)), cy + length * math.sin(math.radians(a - half)))
        p2 = (cx + length * math.cos(math.radians(a + half)), cy + length * math.sin(math.radians(a + half)))
        out.append(f"M{_num(cx)},{_num(cy)} L{_num(p1[0])},{_num(p1[1])} L{_num(p2[0])},{_num(p2[1])} Z")
    return " ".join(out)


def barcode(x, y, w, h, seed, fill):
    rnd = random.Random(seed)
    out, cx = [], x
    while cx < x + w:
        bw = rnd.choice([1.5, 1.5, 3, 4.5])
        out.append(f'<rect x="{_num(cx)}" y="{y}" width="{bw}" height="{h}" fill="{fill}"/>')
        cx += bw + rnd.choice([1.5, 3])
    return "".join(out)


def defs(seed=11, grain=0.10):
    return f"""<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="{seed}"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.94  0 0 0 0 0.9  0 0 0 0 0.82  0 0 0 {grain} 0"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>
  <filter id="distress" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.07" numOctaves="4" seed="{seed + 3}" result="t"/>
    <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -14 10.9" result="speck"/>
    <feComposite in="SourceGraphic" in2="speck" operator="in"/>
  </filter>
  <pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <circle cx="4.5" cy="4.5" r="2.1" fill="{RED}"/>
  </pattern>
  <pattern id="dotsCream" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <circle cx="4" cy="4" r="1.5" fill="{CREAM}"/>
  </pattern>
  <linearGradient id="fadeR" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="fadeL" x1="1" x2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="halftoneL"><rect width="100%" height="100%" fill="url(#fadeL)"/></mask>
  <mask id="halftoneR"><rect width="100%" height="100%" fill="url(#fadeR)"/></mask>
</defs>"""


def section_head(num, label, x=40, y=40, width=1200, icon_name=None):
    """Cabeçalho de card: bloco vermelho com número + título creme + trilho vermelho."""
    nd, nw = text("anton", num, 40, 0, 0)
    ld, lw = text("anton", label, 52, 0, 0, tracking=4)
    bx = x + nw + 28
    lx = bx + 22
    rail = lx + lw + 24
    out = [
        f'<rect x="{x}" y="{y}" width="{_num(nw + 28)}" height="64" fill="{RED}"/>',
        f'<path d="{nd}" fill="{BLACK}" transform="translate({x + 14} {y + 50})"/>',
        f'<path d="{ld}" fill="{CREAM}" filter="url(#distress)" transform="translate({_num(lx)} {y + 56})"/>',
        f'<rect x="{_num(rail)}" y="{y + 26}" width="{_num(x + width - rail)}" height="6" fill="{RED}"/>',
        f'<rect x="{_num(rail)}" y="{y + 38}" width="{_num(x + width - rail)}" height="2" fill="{RED_DARK}"/>',
    ]
    if icon_name:
        out.append(f'<rect x="{x + width - 74}" y="{y + 4}" width="74" height="56" fill="{BLACK}"/>')
        out.append(place_icon(icon_name, x + width - 62, y + 8, 48, CREAM))
    return "\n".join(out)


def svg(w, h, body, seed=11, grain=0.10, border=True):
    frame = f'<rect x="3" y="3" width="{w - 6}" height="{h - 6}" fill="none" stroke="{RED}" stroke-width="6"/>' if border else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{defs(seed, grain)}
<rect width="{w}" height="{h}" fill="{BLACK}"/>
{body}
<rect width="{w}" height="{h}" filter="url(#grain)" fill="#000"/>
{frame}
</svg>"""


def write(name, content):
    os.makedirs(ASSETS, exist_ok=True)
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"{name:14} {len(content) // 1024} KB")
