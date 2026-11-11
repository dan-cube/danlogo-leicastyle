"""EonPoint 方案 C — 辅助图形的生成代码（从提案生成脚本中摘出）。
只学写法：同一个尺寸单位驱动全部构件、按规则排列。颜色用 CSS 变量 var(--f)（主色）与 var(--p)（偏差色）。
不要复用它的造型。"""


def n(x):
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def field_C(w=300, h=400, cls="pat", variant=0):
    """一线一点: one hairline, one point, the rest is white space (golden-ratio placement)."""
    gx, gy = w * 0.382, h * 0.618
    if variant == 0:
        inner = (f'<line x1="{n(gx)}" y1="{n(h * .12)}" x2="{n(gx)}" y2="{n(h * .88)}" stroke="var(--f)" stroke-width="1.6"/>'
                 f'<circle cx="{n(gx + 22)}" cy="{n(h * .88 - 5)}" r="5" fill="var(--p)"/>')
    else:
        inner = (f'<line x1="{n(w * .1)}" y1="{n(gy)}" x2="{n(w * .9)}" y2="{n(gy)}" stroke="var(--f)" stroke-width="1.6"/>'
                 f'<circle cx="{n(w * .618)}" cy="{n(gy - 26)}" r="5" fill="var(--p)"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">{inner}</svg>'


# ─────────────────────────── construction / rules ───────────────────────────
