"""Gera as peças fixas do perfil (banner, sobre, arsenal, rodapé).
Uso: python .github/stats/design.py"""
from ratm import (BLACK, CREAM, GREY, INK, RED, RED_DARK, barcode, place_icon, rays, section_head,
                  star, svg, text, write, _num)

W = 1280


def banner():
    H = 560
    fx, fy, fh = 1000, 236, 340  # punho
    dcy = H - 40  # centro do disco/raios
    title, tw = text("anton", "GIANDONN", 190, 0, 0, tracking=2)
    sub, sw = text("anton", "CODE AGAINST THE MACHINE", 46, 0, 0, tracking=5)
    file_no, _ = text("type", "ARQUIVO Nº 0020  //  FULL STACK  //  BRASIL", 19, 0, 0, tracking=1.5)
    motto, mw = text("type", "WAKE UP. BUILD IT. SHIP IT.", 22, 0, 0, tracking=2.5)
    year, _ = text("anton", "MMXXVI", 30, 0, 0, tracking=10)
    stack, _ = text("type", "PHP / LARAVEL / JAVA / REACT / VUE / TS", 15, 0, 0, tracking=1.5)
    slab = f"0,0 {W * 0.62:.0f},0 {W * 0.50:.0f},{H} 0,{H}"
    body = f"""
<g>
  <path d="{rays(fx, dcy, 28, 1100)}" fill="{RED}">
    <animateTransform attributeName="transform" type="rotate" from="0 {fx} {dcy}" to="360 {fx} {dcy}" dur="120s" repeatCount="indefinite"/>
  </path>
</g>
<circle cx="{fx}" cy="{dcy}" r="300" fill="{BLACK}"/>
<circle cx="{fx}" cy="{dcy}" r="282" fill="{CREAM}"/>
<circle cx="{fx}" cy="{dcy}" r="282" fill="url(#dots)" opacity="0.35"/>
<g>
  {place_icon("fist", fx - fh * 448 / 512 / 2, fy, fh, BLACK, f'stroke="{BLACK}" stroke-width="6"')}
  <animateTransform attributeName="transform" type="translate" values="0 0; 0 -14; 0 0; 0 0" keyTimes="0; 0.15; 0.3; 1" dur="2.4s" repeatCount="indefinite"/>
</g>
<polygon points="{slab}" fill="{BLACK}"/>
<polygon points="{W * 0.62:.0f},0 {W * 0.62 + 18:.0f},0 {W * 0.50 + 18:.0f},{H} {W * 0.50:.0f},{H}" fill="{RED}"/>
<polygon points="{W * 0.62 + 30:.0f},0 {W * 0.62 + 36:.0f},0 {W * 0.50 + 36:.0f},{H} {W * 0.50 + 30:.0f},{H}" fill="{BLACK}"/>
<rect x="0" y="{H - 170}" width="{W * 0.55:.0f}" height="170" fill="url(#dots)" mask="url(#halftoneL)" opacity="0.55"/>
<g transform="rotate(-7 60 330)">
  <path d="{star(74, 110, 13)}" fill="{RED}"/>
  <path d="{file_no}" fill="{GREY}" transform="translate(98 117)"/>
  <path d="{title}" fill="{RED}" transform="translate(70 318)"/>
  <path d="{title}" fill="{CREAM}" filter="url(#distress)" transform="translate(58 306)"/>
  <rect x="58" y="330" width="{_num(sw + 44)}" height="70" fill="{RED}"/>
  <path d="{sub}" fill="{BLACK}" transform="translate(80 385)"/>
  <rect x="58" y="422" width="{_num(mw + 40)}" height="46" fill="none" stroke="{CREAM}" stroke-width="3"/>
  <path d="{motto}" fill="{CREAM}" transform="translate(78 453)"/>
</g>
<g transform="translate(52 530)">
  {barcode(0, -26, 150, 26, 20, CREAM)}
</g>
<path d="{stack}" fill="{GREY}" transform="translate(222 526)"/>
<path d="{year}" fill="{CREAM}" transform="translate(1238 40) rotate(90)"/>
"""
    return svg(W, H, body, seed=11, grain=0.09)


def sobre():
    H = 470
    rows = [
        ("NOME", "GIANDONN"),
        ("FUNÇÃO", "DESENVOLVEDOR FULL STACK"),
        ("BASE", "BRASIL"),
        ("EM CAMPO", "APIs, painéis e apps"),
        ("DOUTRINA", "código legível é código livre"),
        ("STATUS", "EM ATIVIDADE"),
    ]
    parts = [section_head("01", "SOBRE", icon_name="bullhorn")]
    for i, (k, v) in enumerate(rows):
        y = 170 + i * 40
        kd, kw = text("type", k, 20, 40, y, tracking=1)
        dots, _ = text("type", "." * max(2, 12 - len(k)), 20, 40 + kw + 8, y, tracking=1)
        vx = 250
        if k == "STATUS":
            parts.append(f'<rect x="{vx}" y="{y - 19}" width="18" height="24" fill="{RED}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.2s" repeatCount="indefinite"/></rect>')
            vx += 30
        vd, _ = text("type", v, 20, vx, y, tracking=1)
        parts += [f'<path d="{kd}" fill="{GREY}"/>', f'<path d="{dots}" fill="#4a453e"/>', f'<path d="{vd}" fill="{CREAM}"/>']

    s1, s1w = text("anton", "SUBVERSIVO", 70, 0, 0, tracking=6)
    s2, s2w = text("type", "NÍVEL DE AMEAÇA: MÁXIMO", 17, 0, 0, tracking=2)
    parts.append(f"""<g transform="translate(1010 238) rotate(-9)" filter="url(#distress)" opacity="0.92">
  <rect x="{_num(-s1w / 2 - 26)}" y="-72" width="{_num(s1w + 52)}" height="136" fill="none" stroke="{RED}" stroke-width="7"/>
  <rect x="{_num(-s1w / 2 - 16)}" y="-62" width="{_num(s1w + 32)}" height="116" fill="none" stroke="{RED}" stroke-width="2"/>
  <path d="{s1}" fill="{RED}" transform="translate({_num(-s1w / 2)} 18)"/>
  <path d="{s2}" fill="{RED}" transform="translate({_num(-s2w / 2)} 44)"/>
</g>""")
    parts.append(f'<g opacity="0.8">{barcode(890, 346, 250, 20, 7, GREY)}</g>')

    q, qw = text("anton", "SEM FRAMEWORK MÁGICO.   SEM DEPLOY NA SEXTA.   SEM MEDO DO LEGADO.", 30, W / 2, 0, tracking=3, anchor="middle")
    parts.append(f'<rect x="0" y="{H - 76}" width="{W}" height="76" fill="{RED}"/>')
    parts.append(f'<path d="{q}" fill="{BLACK}" transform="translate(0 {H - 26})"/>')
    parts.append(f'<path d="{star(46, H - 38, 14)}" fill="{BLACK}"/><path d="{star(W - 46, H - 38, 14)}" fill="{BLACK}"/>')
    return svg(W, H, "\n".join(parts), seed=31)


def arsenal():
    items = [("php", "PHP"), ("laravel", "LARAVEL"), ("java", "JAVA"), ("typescript", "TYPESCRIPT"),
             ("react", "REACT"), ("vuedotjs", "VUE"), ("mysql", "MYSQL"), ("supabase", "SUPABASE"),
             ("docker", "DOCKER"), ("python", "PYTHON"), ("git", "GIT"), (None, "E O QUE VIER")]
    cols, gap, tw_, th = 6, 16, (1200 - 5 * 16) / 6, 170
    H = 40 + 64 + 34 + 2 * th + gap + 44
    parts = [section_head("02", "ARSENAL")]
    for i, (slug, label) in enumerate(items):
        x = 40 + (i % cols) * (tw_ + gap)
        y = 138 + (i // cols) * (th + gap)
        cx = x + tw_ / 2
        if slug is None:
            parts.append(f'<rect x="{_num(x)}" y="{y}" width="{_num(tw_)}" height="{th}" fill="{RED}"/>')
            parts.append(f'<path d="{star(cx, y + 62, 38)}" fill="{BLACK}"><animateTransform attributeName="transform" type="rotate" from="0 {_num(cx)} {y + 62}" to="72 {_num(cx)} {y + 62}" dur="3s" repeatCount="indefinite"/></path>')
            ld, _ = text("anton", label, 24, cx, y + 146, tracking=2, anchor="middle")
            parts.append(f'<path d="{ld}" fill="{BLACK}"/>')
            continue
        parts.append(f'<rect x="{_num(x)}" y="{y}" width="{_num(tw_)}" height="{th}" fill="{INK}"/>')
        parts.append(f'<rect x="{_num(x)}" y="{y}" width="{_num(tw_)}" height="6" fill="{RED}"/>')
        nd, _ = text("type", f"Nº{i + 1:02d}", 13, x + 12, y + 28, tracking=1)
        parts.append(f'<path d="{nd}" fill="{GREY}"/>')
        parts.append(place_icon(slug, cx - 30, y + 34, 60, CREAM))
        ld, _ = text("anton", label, 24, cx, y + 146, tracking=2, anchor="middle")
        parts.append(f'<path d="{ld}" fill="{CREAM}"/>')
        parts.append(f'<rect x="{_num(cx - 16)}" y="{y + 154}" width="32" height="3" fill="{RED}"/>')
    return svg(W, int(H), "\n".join(parts), seed=41)


def rodape():
    H = 230
    a, aw = text("anton", "NENHUM CÓDIGO É NEUTRO.", 84, W / 2, 128, tracking=6, anchor="middle")
    b, _ = text("type", "—  GIANDONN  ·  MMXXVI  ·  WAKE UP  —", 20, W / 2, 180, tracking=3, anchor="middle")
    left = W / 2 - aw / 2 - 60
    right = W / 2 + aw / 2 + 60
    body = f"""
<rect width="{W}" height="{H}" fill="{RED}"/>
<path d="{rays(W / 2, H / 2, 36, 900)}" fill="{RED_DARK}" opacity="0.55">
  <animateTransform attributeName="transform" type="rotate" from="0 {W / 2} {H / 2}" to="-360 {W / 2} {H / 2}" dur="160s" repeatCount="indefinite"/>
</path>
<rect x="0" y="0" width="{W}" height="{H}" fill="url(#dotsCream)" opacity="0.10"/>
<path d="{star(left, 100, 40)}" fill="{BLACK}"/>
<path d="{star(right, 100, 40)}" fill="{BLACK}"/>
<path d="{a}" fill="{BLACK}" filter="url(#distress)"/>
<path d="{b}" fill="{BLACK}"/>
<rect x="14" y="14" width="{W - 28}" height="{H - 28}" fill="none" stroke="{BLACK}" stroke-width="4"/>
"""
    return svg(W, H, body, seed=51, grain=0.12, border=False)


if __name__ == "__main__":
    write("banner.svg", banner())
    write("sobre.svg", sobre())
    write("arsenal.svg", arsenal())
    write("footer.svg", rodape())
