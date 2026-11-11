"""prim.py — 整件的基本形与一笔画（danlogo-geomodular / danlogo-leicastyle 专用）

为什么有这个文件：把弧线拆成折线、用多边形去裁切出一个外形，会让标志变成「切出来的图」。
这里的每个函数都输出**整件的基本形**和**真正的圆弧**（SVG 的 A 命令），一件就是一两行代码。
一张速写如果要写十几行以上，多半已经太复杂。

形状与 geom.py 通用（{"k": "f"|"c"|"s", ...}），另带三个字段：
  "prim"  基本形的名字        "radii"  用到的半径        "bb"  外接框 (x0, y0, x1, y1)

整件的基本形（实的面）：
  disc(cx, cy, r)                       整圆
  half(cx, cy, r, side)                 半圆，平边过圆心；side = "right" / "left" / "top" / "bottom"（鼓出的方向）
  quarter(cx, cy, r, side)              四分之一圆，直角在 (cx, cy)；side = "ne" / "nw" / "se" / "sw"（鼓出的方向）
  capsule(x, y, w, h)                   两端圆的条（圆角 = 短边一半）
  rect(x, y, w, h, r=0)                 方与矩形，可带一个统一圆角
  tri(x, y, w, h, corner)               直角三角形，直角在 corner = "sw" / "se" / "nw" / "ne"；w == h 时是 45°
  band(cx, cy, r, w, a0, a1)            一段等宽的弧带（中线半径 r，宽 w，从 a0 到 a1 度；0° 向右，顺时针为正）；
                                        取整半圈或整四分之一圈，它才是一件整件的基本形
  turned(shapes, deg, cx, cy)           把一件或几件绕 (cx, cy) 转 deg 度（固定角度系统用，例如 45°）

一笔画（等宽的线，只用直线和圆弧）：
  p = Pen(x, y, heading=0)              heading：0 向右、90 向下、-90 向上
  p.fd(L)                               直走 L
  p.turn(r, deg)                        以半径 r 转 deg 度；正数顺时针（向右转），负数逆时针；转满一圈也可以
  p.corner(deg)                         原地折一个尖角（不走弧）
  p.shape(w, cap="butt")                得到描边形状；cap 可为 "round"

工具：
  report(shapes)                        列出件数、基本形、半径与大小层次（对照尺用）；role 为 "accent" 或 "sig" 的签名不计入半径
  save(shapes, path, colors=None, pad=8, bg="#FFFFFF", box=None)   写出 SVG；box=(x0, y0, x1, y1) 可固定画布

例（只说明写法）：
  shapes = [rect(0, 0, 40, 40), quarter(40, 40, 40, "ne"), disc(70, 70, 8, role="accent")]
  report(shapes); save(shapes, "sketch.svg")
只依赖 Python 标准库。
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import n, render, svg_doc, rotate as _rotate, _sample  # noqa: E402


def _f(d, prim, radii, bb, role=None):
    return {"k": "f", "d": d, "prim": prim, "radii": radii, "bb": bb, "role": role}


# ───────────────────────────── 整件的基本形 ─────────────────────────────

def disc(cx, cy, r, role=None):
    return {"k": "c", "x": cx, "y": cy, "r": r, "prim": "整圆", "radii": [r],
            "bb": (cx - r, cy - r, cx + r, cy + r), "role": role}


def half(cx, cy, r, side="right", role=None):
    a = {"right": ((cx, cy - r), (cx, cy + r), (cx, cy - r, cx + r, cy + r)),
         "left": ((cx, cy + r), (cx, cy - r), (cx - r, cy - r, cx, cy + r)),
         "top": ((cx - r, cy), (cx + r, cy), (cx - r, cy - r, cx + r, cy)),
         "bottom": ((cx + r, cy), (cx - r, cy), (cx - r, cy, cx + r, cy + r))}[side]
    (x0, y0), (x1, y1), bb = a
    d = f"M{n(x0)} {n(y0)}A{n(r)} {n(r)} 0 0 1 {n(x1)} {n(y1)}Z"
    return _f(d, "半圆", [r], bb, role)


def quarter(cx, cy, r, side="ne", role=None):
    p = {"ne": ((cx, cy - r), (cx + r, cy), (cx, cy - r, cx + r, cy)),
         "se": ((cx + r, cy), (cx, cy + r), (cx, cy, cx + r, cy + r)),
         "sw": ((cx, cy + r), (cx - r, cy), (cx - r, cy, cx, cy + r)),
         "nw": ((cx - r, cy), (cx, cy - r), (cx - r, cy - r, cx, cy))}[side]
    (x0, y0), (x1, y1), bb = p
    d = f"M{n(cx)} {n(cy)}L{n(x0)} {n(y0)}A{n(r)} {n(r)} 0 0 1 {n(x1)} {n(y1)}Z"
    return _f(d, "四分之一圆", [r], bb, role)


def _rrect(x, y, w, h, r):
    if r <= 0:
        return f"M{n(x)} {n(y)}H{n(x + w)}V{n(y + h)}H{n(x)}Z"
    return (f"M{n(x + r)} {n(y)}H{n(x + w - r)}A{n(r)} {n(r)} 0 0 1 {n(x + w)} {n(y + r)}"
            f"V{n(y + h - r)}A{n(r)} {n(r)} 0 0 1 {n(x + w - r)} {n(y + h)}H{n(x + r)}"
            f"A{n(r)} {n(r)} 0 0 1 {n(x)} {n(y + h - r)}V{n(y + r)}A{n(r)} {n(r)} 0 0 1 {n(x + r)} {n(y)}Z")


def capsule(x, y, w, h, role=None):
    r = min(w, h) / 2
    return _f(_rrect(x, y, w, h, r), "两端圆的条", [r], (x, y, x + w, y + h), role)


def rect(x, y, w, h, r=0, role=None):
    return _f(_rrect(x, y, w, h, r), "方" if abs(w - h) < 1e-9 else "矩形", [r] if r else [],
              (x, y, x + w, y + h), role)


def tri(x, y, w, h, corner="sw", role=None):
    c = {"sw": [(x, y), (x, y + h), (x + w, y + h)], "se": [(x + w, y), (x + w, y + h), (x, y + h)],
         "nw": [(x, y + h), (x, y), (x + w, y)], "ne": [(x, y), (x + w, y), (x + w, y + h)]}[corner]
    d = f"M{n(c[0][0])} {n(c[0][1])}L{n(c[1][0])} {n(c[1][1])}L{n(c[2][0])} {n(c[2][1])}Z"
    return _f(d, "直角三角形", [], (x, y, x + w, y + h), role)


def _pt(cx, cy, r, a):
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def band(cx, cy, r, w, a0, a1, role=None):
    ro, ri = r + w / 2, r - w / 2
    large = 1 if abs(a1 - a0) > 180 else 0
    sw = 1 if a1 > a0 else 0
    (ox0, oy0), (ox1, oy1) = _pt(cx, cy, ro, a0), _pt(cx, cy, ro, a1)
    (ix1, iy1), (ix0, iy0) = _pt(cx, cy, ri, a1), _pt(cx, cy, ri, a0)
    d = (f"M{n(ox0)} {n(oy0)}A{n(ro)} {n(ro)} 0 {large} {sw} {n(ox1)} {n(oy1)}"
         f"L{n(ix1)} {n(iy1)}A{n(ri)} {n(ri)} 0 {large} {1 - sw} {n(ix0)} {n(iy0)}Z")
    return _f(d, "弧带", [r], _bb_path(d), role)


def _bb_path(d, w=0):
    pts = _sample(d)
    e = w / 2
    return (min(p[0] for p in pts) - e, min(p[1] for p in pts) - e,
            max(p[0] for p in pts) + e, max(p[1] for p in pts) + e)


def turned(shapes, deg, cx=0, cy=0):
    """绕 (cx, cy) 旋转（正值顺时针）。保留基本形的名字和半径，重新算外接框。"""
    single = isinstance(shapes, dict)
    out = []
    for old, new in zip([shapes] if single else shapes, _rotate([shapes] if single else shapes, deg, cx, cy)):
        new = dict(new)
        if new["k"] == "c":
            r = new["r"]
            new["bb"] = (new["x"] - r, new["y"] - r, new["x"] + r, new["y"] + r)
        else:
            new["bb"] = _bb_path(new["d"], new.get("w", 0))
        out.append(new)
    return out[0] if single else out


# ───────────────────────────── 一笔画 ─────────────────────────────

class Pen:
    """一笔等宽的线：只走直线和圆弧。heading 以度计，0 向右、90 向下。"""

    def __init__(self, x, y, heading=0):
        self.x, self.y, self.h = x, y, heading
        self.d = f"M{n(x)} {n(y)}"
        self.pts = [(x, y)]
        self.radii = []

    def fd(self, length):
        self.x += length * math.cos(math.radians(self.h))
        self.y += length * math.sin(math.radians(self.h))
        self.d += f"L{n(self.x)} {n(self.y)}"
        self.pts.append((self.x, self.y))
        return self

    def corner(self, deg):
        self.h += deg
        return self

    def turn(self, r, deg):
        if abs(deg) > 180:  # 一个 A 命令画不了整圈：拆开
            half_ = 180 if deg > 0 else -180
            return self.turn(r, half_).turn(r, deg - half_)
        h = math.radians(self.h)
        s = 1 if deg > 0 else -1
        cx, cy = self.x - s * r * math.sin(h), self.y + s * r * math.cos(h)
        t = math.radians(deg)
        vx, vy = self.x - cx, self.y - cy
        self.x = cx + vx * math.cos(t) - vy * math.sin(t)
        self.y = cy + vx * math.sin(t) + vy * math.cos(t)
        self.h += deg
        large = 1 if abs(deg) > 180 else 0
        self.d += f"A{n(r)} {n(r)} 0 {large} {1 if deg > 0 else 0} {n(self.x)} {n(self.y)}"
        self.radii.append(r)
        # 外接框：取圆上经过的点
        a0 = math.degrees(math.atan2(vy, vx))
        for k in range(0, 13):
            self.pts.append(_pt(cx, cy, r, a0 + deg * k / 12))
        return self

    def shape(self, w, cap="butt", role=None):
        xs, ys = [p[0] for p in self.pts], [p[1] for p in self.pts]
        e = w / 2
        return {"k": "s", "d": self.d, "w": w, "cap": cap, "prim": "一笔", "radii": sorted(set(self.radii)),
                "bb": (min(xs) - e, min(ys) - e, max(xs) + e, max(ys) + e), "role": role}


# ───────────────────────────── 工具 ─────────────────────────────

def _size(sh):
    x0, y0, x1, y1 = sh["bb"]
    return max(x1 - x0, y1 - y0)


def report(shapes):
    """对照尺：件数、每件的基本形、半径种类、大小层次。返回一个字典，并打印一行摘要。"""
    prims = [sh.get("prim", "非基本形") for sh in shapes]
    body = [sh for sh in shapes if sh.get("role") not in ("accent", "sig")]
    radii = sorted({round(r, 2) for sh in body for r in sh.get("radii", [])})
    sizes = sorted((round(_size(sh), 1) for sh in shapes if "bb" in sh), reverse=True)
    odd = prims.count("非基本形")
    levels = len({round(s / sizes[0], 1) for s in sizes}) if sizes else 0
    info = {"件数": len(shapes), "基本形": prims, "半径": radii, "大小": sizes, "层次": levels, "非基本形": odd}
    warn = []
    if len(shapes) > 4:
        warn.append("超过 4 件")
    if odd:
        warn.append(f"{odd} 件不是基本形")
    if len(radii) > 3:
        warn.append("半径超过 3 种")
    print(f"{len(shapes)} 件 · {'、'.join(prims)} · 半径 {radii} · 大小 {sizes}"
          + (f" · 注意：{'；'.join(warn)}" if warn else ""))
    return info


def bbox(shapes):
    bs = [sh["bb"] for sh in shapes]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def save(shapes, path, colors=None, pad=8, bg="#FFFFFF", width=None, box=None):
    colors = colors or {None: "#1E1C1A", "accent": "#1E1C1A"}
    colors.setdefault(None, "#1E1C1A")
    for sh in shapes:  # 未登记的角色用默认色
        colors.setdefault(sh.get("role"), colors[None])
    doc = svg_doc(render(shapes, colors), box or bbox(shapes), bg=bg, pad=pad, width=width)
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    return path


if __name__ == "__main__":
    report([rect(0, 0, 40, 40), quarter(40, 40, 40, "ne"), disc(70, 70, 8, role="accent")])
    report([Pen(0, 0).fd(40).corner(90).fd(20).turn(10, 360).shape(4)])
