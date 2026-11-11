"""04「点·线·面」深化 — three complete identities built from one set of primitives.
A 模数 Modular · B 缝 Stencil · C 空 Emptiness (Kenya Hara).
Marks live in a 0 0 100 100 box. Lettering is drawn as centre-line strokes, so the mark,
the English wordmark and the Chinese wordmark share stroke weight, terminals, curves and dots."""
import math
def n(x):
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s

# ─────────────────────────── schemes ───────────────────────────
S = {
    "A": dict(key="A", cn="模数", en="Modular", ink="#0E1330", brand="#2848E6", brand_d="#6F8BFF", accent="#FF5A36",
              paper="#FFFFFF", W=9.0, Wc=8.6, cap="round", join="round", corner=9, gap=0, dot=0.72, sp=8.5, osp=6.0),
    "B": dict(key="B", cn="缝", en="Stencil", ink="#10142E", brand="#10142E", brand_d="#FFFFFF", accent="#2F5BFF",
              paper="#FFFFFF", W=10.4, Wc=9.8, cap="square", join="miter", corner=0, gap=3.1, dot=0.66, sp=8.0, osp=6.0),
    "C": dict(key="C", cn="空", en="Emptiness", ink="#1C1B19", brand="#1C1B19", brand_d="#F2EFE8", accent="#D2452B",
              paper="#F6F4EF", W=4.0, Wc=5.0, cap="butt", join="miter", corner=2.5, gap=0, dot=1.05, sp=17.0, osp=15.0),
}


def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def poly_d(pts, r=0.0, closed=False):
    if closed:
        pts = pts + [pts[0], pts[1]]
    d = f"M{n(pts[0][0])} {n(pts[0][1])}"
    if r <= 0 or len(pts) < 3:
        d += "".join(f"L{n(x)} {n(y)}" for x, y in pts[1:])
        return d + ("Z" if closed else "")
    for i in range(1, len(pts) - 1):
        p, v, q = pts[i - 1], pts[i], pts[i + 1]
        l1, l2 = dist(p, v), dist(v, q)
        rr = min(r, l1 / 2, l2 / 2)
        a = (v[0] + (p[0] - v[0]) * rr / l1, v[1] + (p[1] - v[1]) * rr / l1)
        b = (v[0] + (q[0] - v[0]) * rr / l2, v[1] + (q[1] - v[1]) * rr / l2)
        d += f"L{n(a[0])} {n(a[1])}Q{n(v[0])} {n(v[1])} {n(b[0])} {n(b[1])}"
    if not closed:
        d += f"L{n(pts[-1][0])} {n(pts[-1][1])}"
    return d


def trim(pts, t0, t1, amt):
    pts = list(pts)
    if t0 and amt:
        a, b = pts[0], pts[1]
        L = dist(a, b)
        pts[0] = (a[0] + (b[0] - a[0]) * amt / L, a[1] + (b[1] - a[1]) * amt / L)
    if t1 and amt:
        a, b = pts[-1], pts[-2]
        L = dist(a, b)
        pts[-1] = (a[0] + (b[0] - a[0]) * amt / L, a[1] + (b[1] - a[1]) * amt / L)
    return pts


# ─────────────────────────── Chinese: 亿 触 点 (em 100, centre-lines) ───────────────────────────
# ("p", pts, attached_start, attached_end, corner_scale) · ("box", x0, y0, x1, y1) · ("dot", cx, cy)
CN = {
    "亿": [
        ("p", [(31, 7), (9, 47)], 0, 0, 0),
        ("p", [(20, 27), (20, 94)], 1, 0, 0),
        ("p", [(42, 17), (85, 17), (45, 63), (45, 89), (91, 89), (91, 72)], 0, 0, 1),
    ],
    "触": [
        ("p", [(21, 4), (9, 21)], 0, 0, 0),
        ("p", [(15.35, 12), (35, 12), (28, 26)], 1, 0, .4),
        ("p", [(6, 95), (12, 80), (12, 26), (42, 26), (42, 88), (36, 95)], 0, 0, .5),
        ("p", [(12, 44), (42, 44)], 1, 0, 0),
        ("p", [(12, 62), (42, 62)], 1, 0, 0),
        ("p", [(27, 26), (27, 62)], 1, 0, 0),
        ("box", 54, 26, 90, 55),
        ("p", [(72, 9), (72, 85.12)], 0, 1, 0),
        ("p", [(52, 91), (86, 81)], 0, 0, 0),
        ("dot", 87, 69),
    ],
    "点": [
        ("p", [(50, 4), (50, 36)], 0, 1, 0),
        ("p", [(50, 19), (77, 19)], 1, 0, 0),
        ("box", 23, 36, 77, 64),
        ("dot", 15, 86), ("dot", 38, 86), ("dot", 62, 86), ("dot", 85, 86),
    ],
}

# planes (enclosed counters) for the 空 diagram: per char list of (kind, data)
CN_PLANES = {"触": [("rect", 54, 26, 90, 55)], "点": [("rect", 23, 36, 77, 64)]}


def cn_glyph(ch, sc, ink, dotc=None, rel=None):
    """strokes for one character at origin; returns svg markup."""
    W, g = sc["Wc"], sc["gap"]
    amt = (W + g) if g else 0
    body, dots, planes, gaps = "", "", "", ""
    for it in CN[ch]:
        if it[0] == "p":
            _, pts, t0, t1, cs = it
            tp = trim(pts, t0, t1, amt)
            body += f'<path d="{poly_d(tp, sc["corner"] * cs)}"/>'
            if rel == "B" and amt:
                for flag, o, t in ((t0, pts[0], tp[0]), (t1, pts[-1], tp[-1])):
                    if flag:
                        L = dist(o, t)
                        ux, uy = (o[0] - t[0]) / L, (o[1] - t[1]) / L
                        a = (t[0] + ux * W / 2, t[1] + uy * W / 2)
                        b = (o[0] - ux * W / 2, o[1] - uy * W / 2)
                        gaps += f'<path d="M{n(a[0])} {n(a[1])}L{n(b[0])} {n(b[1])}"/>'
        elif it[0] == "box":
            _, x0, y0, x1, y1 = it
            body += f'<path d="{poly_d([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], sc["corner"] * .3, True)}"/>'
        else:
            _, cx, cy = it
            dots += f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(W * sc["dot"])}"/>'
    if rel == "C":
        for kind, x0, y0, x1, y1 in CN_PLANES.get(ch, []):
            planes += f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/>'
    lc = {"round": "round", "square": "square", "butt": "butt"}[sc["cap"]]
    out = ""
    if planes:
        out += f'<g fill="{sc["accent"]}" fill-opacity=".14">{planes}</g>'
    out += (f'<g fill="none" stroke="{ink}" stroke-width="{n(W)}" stroke-linecap="{lc}" '
            f'stroke-linejoin="{sc["join"]}" stroke-miterlimit="3">{body}</g>')
    out += f'<g fill="{dotc or ink}">{dots}</g>'
    if gaps:
        out += f'<g stroke="{sc["accent"]}" stroke-width="{n(W * .9)}" stroke-linecap="butt" fill="none">{gaps}</g>'
    return out


def cn_word(sc, ink, track=None, dotc=None, rel=None, text="亿触点"):
    """returns (inner, width) in em units (height 100)."""
    tr = sc["sp"] * 1.6 if track is None else track
    x, out = 0.0, ""
    for i, ch in enumerate(text):
        out += f'<g transform="translate({n(x)} 0)">{cn_glyph(ch, sc, ink, dotc, rel)}</g>'
        x += 100 + (tr if i < len(text) - 1 else 0)
    return out, x


# ─────────────────────────── Latin: EonPoint (baseline 100, x-height 48, cap 30) ───────────────────────────
BL, XH, CH = 100.0, 48.0, 30.0


def latin(ch, W, g):
    h = W / 2
    G = dict(w=0, straight=[], curve=[], dots=[], cuts=[], planes=[])
    if ch == "E":
        G["w"] = 40
        G["straight"] += [f"M{n(40 - h)} {n(CH + h)}H{n(h)}V{n(BL - h)}H{n(40 - h)}", f"M{n(h)} 65H{n(35 - h)}"]
        G["cuts"] += [(W, CH - 3, W + g, BL + 3)]
    elif ch == "o":
        R = 27.0
        r = R - h
        G["w"] = 2 * R
        G["curve"] += [f"M{n(R - r)} 74A{n(r)} {n(r)} 0 1 1 {n(R + r)} 74A{n(r)} {n(r)} 0 1 1 {n(R - r)} 74Z"]
        G["planes"] += [f'<circle cx="{n(R)}" cy="74" r="{n(r - h)}"/>']
    elif ch == "n":
        w = 44
        rr = w / 2 - h
        cy = XH + h + rr
        G["w"] = w
        G["straight"] += [f"M{n(h)} {n(XH + h)}V{n(BL - h)}", f"M{n(w - h)} {n(cy)}V{n(BL - h)}"]
        G["curve"] += [f"M{n(h)} {n(cy)}A{n(rr)} {n(rr)} 0 0 1 {n(w - h)} {n(cy)}"]
        G["cuts"] += [(W, XH - 3, W + g, BL + 3)]
    elif ch == "P":
        w, bb = 42, 72
        rb = (bb - CH) / 2 - h
        bx = w - h - rb
        G["w"] = w
        G["straight"] += [f"M{n(h)} {n(CH + h)}V{n(BL - h)}", f"M{n(h)} {n(CH + h)}H{n(bx)}", f"M{n(bx)} {n(bb - h)}H{n(h)}"]
        G["curve"] += [f"M{n(bx)} {n(CH + h)}A{n(rb)} {n(rb)} 0 0 1 {n(bx)} {n(bb - h)}"]
        G["cuts"] += [(W, CH - 3, W + g, BL + 3)]
        G["planes"] += [f'<path d="M{n(W)} {n(CH + W)}H{n(bx)}A{n(rb - h)} {n(rb - h)} 0 0 1 {n(bx)} {n(bb - W)}H{n(W)}Z"/>']
    elif ch == "i":
        G["w"] = W
        G["straight"] += [f"M{n(h)} {n(XH + h)}V{n(BL - h)}"]
        G["dots"] += [(h, None)]
    elif ch == "t":
        w, sx = 26, 10.0
        G["w"] = w
        G["straight"] += [f"M{n(sx)} {n(35 + h)}V{n(BL - h)}", f"M{n(h)} {n(XH + h)}H{n(w - h)}"]
    return G


PAIRS = {("E", "o"): -1.5, ("o", "n"): -2.5, ("n", "P"): 1.0, ("P", "o"): -2.5, ("o", "i"): -2.0, ("i", "n"): 1.0, ("n", "t"): 0.0}


def en_word(sc, ink, dotc, rel=None, uid="w", word="EonPoint"):
    """returns (inner, width) — glyph units, viewBox y from 26 to 104."""
    W, g = sc["W"], sc["gap"]
    h = W / 2
    lc = sc["cap"]
    x, prev = 0.0, None
    straight = curve = dots = planes = cuts = ""
    for ch in word:
        if prev:
            x += sc["sp"] + PAIRS.get((prev, ch), 0) * (sc["sp"] / 8.5)
        G = latin(ch, W, g)
        tr = f'transform="translate({n(x)} 0)"'
        straight += "".join(f'<path {tr} d="{d}"/>' for d in G["straight"])
        curve += "".join(f'<path {tr} d="{d}"/>' for d in G["curve"])
        for (dx, _) in G["dots"]:
            rd = W * sc["dot"] * 1.12
            dots += f'<circle cx="{n(x + dx)}" cy="{n(CH + rd)}" r="{n(rd)}"/>'
        if g:
            cuts += "".join(f'<rect x="{n(x + a)}" y="{n(b)}" width="{n(c - a)}" height="{n(d - b)}"/>' for a, b, c, d in G["cuts"])
        if rel == "C":
            planes += "".join(f'<g {tr}>{p}</g>' for p in G["planes"])
        x += G["w"]
        prev = ch
    curve_col = sc["brand"] if rel == "A" else ink
    st = f'fill="none" stroke-width="{n(W)}" stroke-linecap="{lc}" stroke-linejoin="{sc["join"]}" stroke-miterlimit="3"'
    body = (f'<g {st} stroke="{"#C9CEDB" if rel in ("A", "B") else ink}">{straight}</g>'
            f'<g {st} stroke="{curve_col if rel != "B" else "#C9CEDB"}">{curve}</g>')
    out = ""
    if planes:
        out += f'<g fill="{sc["accent"]}" fill-opacity=".14">{planes}</g>'
    if g:
        mask = (f'<mask id="{uid}k" maskUnits="userSpaceOnUse" x="-20" y="0" width="{n(x + 40)}" height="130">'
                f'<rect x="-20" y="0" width="{n(x + 40)}" height="130" fill="#fff"/><g fill="#000">{cuts}</g></mask>')
        out += f'<defs>{mask}</defs><g mask="url(#{uid}k)">{body}</g>'
        if rel == "B":
            out += f'<g fill="{sc["accent"]}" fill-opacity=".9">{cuts}</g>'
    else:
        out += body
    out += f'<g fill="{dotc}">{dots}</g>'
    return out, x


# ─────────────────────────── marks ───────────────────────────

def mark_A(v, u, small=False):
    """模数 — stem ⌀ = dot ⌀ = 22, bowl R = 1.5 × 22, every gap 6; two flat colours; optical overshoot on round forms."""
    sc = S["A"]
    stem = '<rect x="19.5" y="3" width="22" height="94" rx="11"/>'
    bowl = '<path d="M47.5 2.6A33.4 33.4 0 0 1 47.5 69.4Z"/>'
    dot = '<circle cx="58.5" cy="86" r="11.5"/>'
    c1, c2 = {"color": (sc["brand"], sc["accent"]), "dark": (sc["brand_d"], sc["accent"]),
              "mono": (sc["ink"], sc["ink"]), "white": ("#FFFFFF", "#FFFFFF"), "brand": ("#FFFFFF", sc["accent"])}[v]
    return f'<g fill="{c1}">{stem}{bowl}</g><g fill="{c2}">{dot}</g>'


def mark_B(v, u, small=False):
    """缝 — a square emblem split by one constant gap (8 = 0.3 × stem): stem | plane (D) | point."""
    sc = S["B"]
    stem = '<rect x="3" y="3" width="26" height="94"/>'
    plane = '<path d="M37 3H67A30 30 0 0 1 67 63H37Z"/>'
    dot = '<circle cx="84" cy="84" r="13"/>'
    c1, c2 = {"color": (sc["ink"], sc["accent"]), "dark": ("#FFFFFF", "#5B83FF"),
              "mono": (sc["ink"], sc["ink"]), "white": ("#FFFFFF", "#FFFFFF")}[v]
    return f'<g fill="{c1}">{stem}{plane}</g><g fill="{c2}">{dot}</g>'


def mark_C(v, u, small=False, rel=False):
    """空 — one line rises, turns, and stops short of closing: the plane is left as white space; one vermilion point."""
    sc = S["C"]
    s = 9 if small else 5.2
    x, top, xc, R = 33, 5 + s / 2, 47, 25
    d = f"M{n(x)} {n(96 - s / 2)}V{n(top)}H{n(xc)}A{R} {R} 0 0 1 {n(xc)} {n(top + 2 * R)}"
    c1, c2 = {"color": (sc["ink"], sc["accent"]), "dark": (sc["brand_d"], sc["accent"]),
              "mono": (sc["ink"], sc["ink"]), "white": ("#FFFFFF", "#FFFFFF")}[v]
    plane = ""
    if rel:
        plane = (f'<path d="M{n(x)} {n(top)}H{n(xc)}A{R} {R} 0 0 1 {n(xc)} {n(top + 2 * R)}H{n(x)}Z" '
                 f'fill="{sc["accent"]}" fill-opacity=".12"/>')
    return (f'{plane}<path d="{d}" fill="none" stroke="{c1}" stroke-width="{s}" stroke-linecap="butt" stroke-linejoin="miter"/>'
            f'<circle cx="{n(xc)}" cy="{n(96 - (6.2 if small else 4.6))}" r="{6.2 if small else 4.6}" fill="{c2}"/>')


MARK = {"A": mark_A, "B": mark_B, "C": mark_C}
MARK_BOX = {"A": (19.5, 80.9), "B": (3, 97), "C": (30.4, 74.6)}   # visual left/right edges inside the 100 box
