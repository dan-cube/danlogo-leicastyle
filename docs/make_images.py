#!/usr/bin/env python3
"""Regenerate the README hero and the GitHub social preview in docs/images/.

    python3 docs/make_images.py                  # hero + social-preview (SVG and PNG)
    python3 docs/make_images.py social-preview   # only the named images

The marks are embedded from the case images in cases/; the text is set in system
fonts (these are README illustrations, not logo artwork). PNGs come from
scripts/render.sh, or from the converter named in $SVG2PNG, called as
`$SVG2PNG in.svg out.png width`. The committed PNGs were rendered on macOS with an
AppKit converter, with $MEASURE naming a helper that prints the width of a
letter-spaced string (`$MEASURE font size spacing text`).

The case images shown here are not covered by the MIT License; see LICENSE.
"""
import os, re, subprocess, sys

SANS = "Helvetica Neue, PingFang SC, sans-serif"
CN = "PingFang SC, Helvetica Neue, sans-serif"


def embed(path, x, y, w, h):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<\?xml[^>]*>\s*", "", s)
    head = re.match(r"<svg\b[^>]*>", s).group(0)
    new = re.sub(r'\s(width|height|x|y)="[^"]*"', "", head)
    new = new.replace("<svg", f'<svg x="{x}" y="{y}" width="{w}" height="{h}" '
                              f'preserveAspectRatio="xMidYMid meet"', 1)
    return s.replace(head, new, 1)


def t(x, y, s, size, col, weight=400, anchor="start", ls=0, fam=SANS):
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="{ls}" text-anchor="{anchor}" fill="{col}">{s}</text>')


def doc(w, h, inner, bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{inner}</svg>')


STYLE = dict(
    img="cases/eonpoint-precision/images",
    bg="#F0EDE6", ink="#151413", accent="#D8402A", mute="#8A867D", txt2="#5B5852",
    tile1="#E7E3DA", tile2="#151413",
    caps=("DANLOGO", "LEICA STYLE"), title="徕卡风格", tw=300,
    en="Complete logo identity systems, with German precision",
    cn="一个精确、只留本质的主体，加上一处有人的温度的签名。",
    en2="One precise body, one human signature. Remove the signature, and the body still holds.",
    social_en=("Complete logo identity systems,", "with German precision"),
    social_cn="精确的主体，一处签名",
    t1=("mark-main.svg", 0.60, "标志 Mark"), t2=("mark-inv.svg", 0.60, "反白 Reversed"),
    credit="案例 · EonPoint 亿触点 方案 C「空」",
)


def caps(x, y, size, st, anchor="start"):
    a, b = st["caps"]
    ls = size * 0.34
    # the dot between the two words is the one accent colour; it is drawn as a
    # circle because some SVG renderers ignore <tspan> fills
    w = text_width("HelveticaNeue-Medium", size, ls, a)
    cx = x + w + size * 0.42
    return (t(x, y, a, size, st["mute"], 500, ls=ls)
            + f'<circle cx="{cx:.1f}" cy="{y - size * 0.355:.1f}" r="{size * 0.15:.1f}" fill="{st["accent"]}"/>'
            + t(cx + size * 0.78, y, b, size, st["mute"], 500, ls=ls))


def text_width(font, size, ls, s):
    """Width of a letter-spaced string; uses the AppKit measuring helper when present."""
    tool = os.environ.get("MEASURE")
    if tool:
        return float(subprocess.check_output([tool, font, str(size), str(ls), s]).decode())
    return len(s) * (size * 0.71 + ls)


def tile(root, st, spec, x, y, s, fill, dark):
    f, k, cap = spec
    inner = s * k
    g = [f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{fill}"/>']
    g.append(embed(os.path.join(root, st["img"], f), x + (s - inner) / 2, y + (s - inner) / 2, inner, inner))
    g.append(t(x, y + s + 52, cap, 30, st["txt2"], 400, fam=CN))
    return "".join(g)


def hero(root, st):
    W, H = 2400, 900
    L = 180
    g = [caps(L, 250, 34, st),
         t(L - 6, 470, st["title"], 176, st["ink"], st["tw"], ls=10, fam=CN),
         t(L, 568, st["en"], 46, st["ink"], 400),
         t(L, 660, st["cn"], 34, st["txt2"], 400, fam=CN),
         t(L, 724, st["en2"], 28, st["mute"], 400),
         f'<rect x="1500" y="205" width="2" height="545" fill="{st["ink"]}" opacity="0.12"/>']
    S, x1 = 300, 1590
    g.append(tile(root, st, st["t1"], x1, 222, S, st["tile1"], False))
    g.append(tile(root, st, st["t2"], x1 + S + 30, 222, S, st["tile2"], True))
    g.append(t(2220, 724, st["credit"], 26, st["mute"], 400, "end", fam=CN))
    return doc(W, H, "".join(g), st["bg"])


def social(root, st):
    W, H = 1280, 640
    L = 96
    g = [caps(L, 160, 22, st),
         t(L - 4, 318, st["title"], 124, st["ink"], st["tw"], ls=8, fam=CN),
         t(L, 392, st["social_en"][0], 34, st["ink"], 400),
         t(L, 436, st["social_en"][1], 34, st["ink"], 400),
         t(L, 484, "for AI tools such as Claude &amp; Codex · brief to delivery", 22, st["txt2"], 400),
         f'<rect x="{L}" y="522" width="64" height="2" fill="{st["mute"]}"/>',
         t(L, 568, st["social_cn"], 26, st["txt2"], 400, fam=CN)]
    g.append(embed(os.path.join(root, st["img"], "mark-main.svg"), 820, 150, 340, 340))
    g.append(t(1184, 590, "案例 · EonPoint 亿触点", 18, st["mute"], 400, "end", fam=CN))
    return doc(W, H, "".join(g), st["bg"])


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "images")
IMAGES = {"hero": (hero, 2400), "social-preview": (social, 1280)}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in sys.argv[1:] or list(IMAGES):
        fn, width = IMAGES[name]
        svg = os.path.join(OUT, name + ".svg")
        png = svg[:-4] + ".png"
        with open(svg, "w", encoding="utf-8") as f:
            f.write(fn(ROOT, STYLE))
        conv = os.environ.get("SVG2PNG")
        cmd = ([conv, svg, png, str(width)] if conv
               else ["bash", os.path.join(ROOT, "scripts", "render.sh"), svg, str(width), png])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        print(os.path.relpath(png, ROOT))
