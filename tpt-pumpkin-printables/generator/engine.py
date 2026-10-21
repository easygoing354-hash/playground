"""Tiny vector-art engine shared by the PDF printables and the web app.

Art is authored once as a list of primitive ops in an SVG-style coordinate
system (a 100 x 100 box centred on 0,0, y pointing down). It can then be
rendered two ways:

* ``draw_pdf``  - onto a ReportLab canvas (black-line "colour me" art, or colour)
* ``to_svg``    - as an SVG fragment (used by the web app and previews)

Fills are *semantic* names ("orange", "leaf", ...). In black & white mode every
fill becomes white except ``ink`` (always black) so the printables are
ink-friendly colouring pages.
"""
import math
import re

PALETTE = {
    "white": "#ffffff", "paper": "#ffffff", "ink": "#231f20", "none": None,
    "orange": "#f7902b", "orange2": "#e8741c", "orange3": "#ffb25e",
    "stem": "#7a5230", "stem2": "#9b6b3f", "brown": "#a0703c", "tan": "#e6c48f",
    "leaf": "#5fae4c", "leaf2": "#3f8a38", "green": "#8cc63f", "dark": "#2d2a32",
    "yellow": "#ffd43b", "gold": "#f5b700", "purple": "#7d4fa6", "purple2": "#5b3a82",
    "pink": "#f8a5c2", "red": "#e2483d", "blue": "#4aa3df", "sky": "#bfe3f7",
    "gray": "#a9a9b3", "lgray": "#e3e3e8", "cream": "#fff3dd", "teal": "#2bb3a3",
    "maple": "#e2483d", "rust": "#c4561d", "olive": "#9aa43a", "night": "#3b2f63",
    "ghost": "#fbfbff", "moon": "#fff2a8", "skin": "#c8e6a0", "denim": "#4f7cc9",
    "plaid": "#d9534f", "straw": "#f2cf63", "bone": "#f4f1e6", "silver": "#c9ced6",
}

BW_KEEP = {"ink", "none"}
DEFAULT_W = 2.4


class Art:
    """A list of drawing ops. Every helper returns self for chaining."""

    def __init__(self, ops=None):
        self.ops = list(ops or [])

    # ---- primitives -------------------------------------------------
    def path(self, d, fill="white", stroke="ink", w=DEFAULT_W):
        self.ops.append(("path", d, fill, stroke, w))
        return self

    def ellipse(self, cx, cy, rx, ry, fill="white", stroke="ink", w=DEFAULT_W):
        self.ops.append(("ellipse", cx, cy, rx, ry, fill, stroke, w))
        return self

    def circle(self, cx, cy, r, fill="white", stroke="ink", w=DEFAULT_W):
        return self.ellipse(cx, cy, r, r, fill, stroke, w)

    def rect(self, x, y, w_, h, r=0, fill="white", stroke="ink", w=DEFAULT_W):
        self.ops.append(("rect", x, y, w_, h, r, fill, stroke, w))
        return self

    def poly(self, pts, fill="white", stroke="ink", w=DEFAULT_W, close=True):
        d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + (" Z" if close else "")
        return self.path(d, fill if close else "none", stroke, w)

    def line(self, x1, y1, x2, y2, stroke="ink", w=DEFAULT_W):
        return self.path(f"M {x1} {y1} L {x2} {y2}", "none", stroke, w)

    def curve(self, d, stroke="ink", w=DEFAULT_W):
        return self.path(d, "none", stroke, w)

    # ---- composition ------------------------------------------------
    def add(self, other, dx=0, dy=0, s=1.0, rot=0, flip=False, sy=None):
        """Insert another Art with a transform (s = uniform scale)."""
        self.ops.append(("group", dx, dy, s, s if sy is None else sy, rot, flip, other.ops))
        return self

    def merge(self, other):
        """Draw `other` as one silhouette (outline of the union, no inner lines)."""
        self.ops.append(("merge", other.ops))
        return self


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def star_pts(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def heart_d(cx=0, cy=0, s=1.0):
    def p(x, y):
        return f"{cx + x * s:.2f} {cy + y * s:.2f}"
    return (f"M {p(0, 38)} C {p(-20, 22)} {p(-46, 6)} {p(-46, -14)} "
            f"C {p(-46, -34)} {p(-24, -44)} {p(0, -24)} "
            f"C {p(24, -44)} {p(46, -34)} {p(46, -14)} "
            f"C {p(46, 6)} {p(20, 22)} {p(0, 38)} Z")


# ---------------------------------------------------------------------------
# path parser (M L H V C S Q T Z, absolute + relative) -> list of segments
# ---------------------------------------------------------------------------
_TOK = re.compile(r"[MmLlHhVvCcSsQqTtZz]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?")


def parse_path(d):
    toks = _TOK.findall(d)
    i, cmd = 0, None
    x = y = sx = sy = 0.0
    lcx = lcy = None  # last control point for S/T
    out = []

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v

    while i < len(toks):
        t = toks[i]
        if re.match(r"[A-Za-z]", t):
            cmd = t
            i += 1
            if cmd in "Zz":
                out.append(("Z",))
                x, y = sx, sy
                lcx = lcy = None
                continue
        rel = cmd.islower()
        C = cmd.upper()
        if C == "M":
            nx, ny = num(), num()
            if rel:
                nx, ny = x + nx, y + ny
            out.append(("M", nx, ny))
            x, y, sx, sy = nx, ny, nx, ny
            cmd = "l" if rel else "L"
            lcx = lcy = None
        elif C == "L":
            nx, ny = num(), num()
            if rel:
                nx, ny = x + nx, y + ny
            out.append(("L", nx, ny))
            x, y = nx, ny
            lcx = lcy = None
        elif C == "H":
            nx = num()
            x = x + nx if rel else nx
            out.append(("L", x, y))
            lcx = lcy = None
        elif C == "V":
            ny = num()
            y = y + ny if rel else ny
            out.append(("L", x, y))
            lcx = lcy = None
        elif C == "C":
            a = [num() for _ in range(6)]
            if rel:
                a = [a[0] + x, a[1] + y, a[2] + x, a[3] + y, a[4] + x, a[5] + y]
            out.append(("C", *a))
            lcx, lcy = a[2], a[3]
            x, y = a[4], a[5]
        elif C == "S":
            a = [num() for _ in range(4)]
            if rel:
                a = [a[0] + x, a[1] + y, a[2] + x, a[3] + y]
            c1x, c1y = (2 * x - lcx, 2 * y - lcy) if lcx is not None else (x, y)
            out.append(("C", c1x, c1y, *a))
            lcx, lcy = a[0], a[1]
            x, y = a[2], a[3]
        elif C == "Q":
            a = [num() for _ in range(4)]
            if rel:
                a = [a[0] + x, a[1] + y, a[2] + x, a[3] + y]
            qx, qy, ex, ey = a
            out.append(("C", x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y),
                        ex + 2 / 3 * (qx - ex), ey + 2 / 3 * (qy - ey), ex, ey))
            lcx, lcy = qx, qy
            x, y = ex, ey
        else:
            raise ValueError(f"unsupported path command {cmd} in {d!r}")
    return out


# ---------------------------------------------------------------------------
# PDF backend
# ---------------------------------------------------------------------------
BASE_PT = 2.0   # printed thickness (points) of a default-weight line


def _rgb(hexs):
    hexs = hexs.lstrip("#")
    return tuple(int(hexs[i:i + 2], 16) / 255 for i in (0, 2, 4))


class PDFRenderer:
    def __init__(self, canvas, color=False, base_pt=BASE_PT, overrides=None):
        self.c = canvas
        self.color = color
        self.base_pt = base_pt
        self.scale = [1.0]
        self.overrides = overrides or {}

    def _fill(self, name):
        if name in (None, "none"):
            return None
        name = self.overrides.get(name, name)
        if not self.color and name not in BW_KEEP:
            return "#ffffff"
        if name.startswith("#"):
            return name
        return PALETTE[name]

    def _stroke(self, name):
        if name in (None, "none"):
            return None
        if name.startswith("#"):
            return name if self.color else PALETTE["ink"]
        return PALETTE[name] if self.color else PALETTE["ink"]

    def _apply(self, fill, stroke, w, mode):
        """mode: 'normal' | 'outline' (merge pass 1) | 'fill' (merge pass 2)"""
        c = self.c
        f = self._fill(fill)
        s = self._stroke(stroke)
        if mode == "outline":
            if s is None:
                return False, False
            c.setStrokeColorRGB(*_rgb(s))
            c.setLineWidth(2 * w / DEFAULT_W * self.base_pt / self.scale[-1])
            return False, True
        if mode == "fill":
            if f is None:
                return False, False
            c.setFillColorRGB(*_rgb(f))
            return True, False
        if f is not None:
            c.setFillColorRGB(*_rgb(f))
        if s is not None:
            c.setStrokeColorRGB(*_rgb(s))
            c.setLineWidth(w / DEFAULT_W * self.base_pt / self.scale[-1])
        return f is not None, s is not None

    def draw(self, art, x, y, size, rot=0, flip=False):
        """Draw `art` centred at page point (x, y); `size` = width of the 100 box in pt."""
        c = self.c
        c.saveState()
        c.setLineJoin(1)
        c.setLineCap(1)
        c.translate(x, y)
        if rot:
            c.rotate(-rot)
        k = size / 100.0
        c.scale(-k if flip else k, -k)
        self.scale.append(self.scale[-1] * k)
        self._ops(art.ops if isinstance(art, Art) else art, "normal")
        self.scale.pop()
        c.restoreState()

    def _ops(self, ops, mode):
        c = self.c
        for op in ops:
            kind = op[0]
            if kind == "group":
                _, dx, dy, sx, sy, rot, flip, sub = op
                c.saveState()
                c.translate(dx, dy)
                if rot:
                    c.rotate(rot)
                c.scale(-sx if flip else sx, sy)
                self.scale.append(self.scale[-1] * abs(sx))
                self._ops(sub, mode)
                self.scale.pop()
                c.restoreState()
            elif kind == "merge":
                if mode == "normal":
                    self._ops(op[1], "outline")
                    self._ops(op[1], "fill")
                else:
                    self._ops(op[1], mode)
            else:
                self._prim(op, mode)

    def _prim(self, op, mode):
        c = self.c
        kind = op[0]
        if kind == "ellipse":
            _, cx, cy, rx, ry, fill, stroke, w = op
            f, s = self._apply(fill, stroke, w, mode)
            if f or s:
                c.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, stroke=int(s), fill=int(f))
        elif kind == "rect":
            _, x, y, w_, h, r, fill, stroke, w = op
            f, s = self._apply(fill, stroke, w, mode)
            if f or s:
                if r:
                    c.roundRect(x, y, w_, h, r, stroke=int(s), fill=int(f))
                else:
                    c.rect(x, y, w_, h, stroke=int(s), fill=int(f))
        elif kind == "path":
            _, d, fill, stroke, w = op
            f, s = self._apply(fill, stroke, w, mode)
            if not (f or s):
                return
            p = c.beginPath()
            for seg in parse_path(d):
                if seg[0] == "M":
                    p.moveTo(seg[1], seg[2])
                elif seg[0] == "L":
                    p.lineTo(seg[1], seg[2])
                elif seg[0] == "C":
                    p.curveTo(*seg[1:])
                elif seg[0] == "Z":
                    p.close()
            c.drawPath(p, stroke=int(s), fill=int(f), fillMode=0)


# ---------------------------------------------------------------------------
# SVG backend
# ---------------------------------------------------------------------------

def _svg_fill(name, color):
    if name in (None, "none"):
        return "none"
    if name.startswith("#"):
        return name if color else "#ffffff"
    if not color and name not in BW_KEEP:
        return "#ffffff"
    return PALETTE[name]


def _svg_stroke(name, color):
    if name in (None, "none"):
        return "none"
    if not color:
        return PALETTE["ink"]
    return name if name.startswith("#") else PALETTE[name]


def _svg_ops(ops, color, mode="normal"):
    out = []
    for op in ops:
        kind = op[0]
        if kind == "group":
            _, dx, dy, sx, sy, rot, flip, sub = op
            tf = f"translate({dx:g} {dy:g})"
            if rot:
                tf += f" rotate({rot:g})"
            if flip or sx != 1 or sy != 1:
                tf += f" scale({-sx if flip else sx:g} {sy:g})"
            out.append(f'<g transform="{tf}">' + _svg_ops(sub, color, mode) + "</g>")
            continue
        if kind == "merge":
            if mode == "normal":
                out.append(_svg_ops(op[1], color, "outline") + _svg_ops(op[1], color, "fill"))
            else:
                out.append(_svg_ops(op[1], color, mode))
            continue
        fill, stroke, w = op[-3], op[-2], op[-1]
        f = _svg_fill(fill, color)
        s = _svg_stroke(stroke, color)
        if mode == "outline":
            if s == "none":
                continue
            attrs = f'fill="none" stroke="{s}" stroke-width="{2 * w:g}"'
        elif mode == "fill":
            if f == "none":
                continue
            attrs = f'fill="{f}" stroke="none"'
        else:
            attrs = f'fill="{f}" stroke="{s}" stroke-width="{w:g}"' if s != "none" else f'fill="{f}" stroke="none"'
        if kind == "ellipse":
            _, cx, cy, rx, ry = op[:5]
            out.append(f'<ellipse cx="{cx:g}" cy="{cy:g}" rx="{rx:g}" ry="{ry:g}" {attrs}/>')
        elif kind == "rect":
            _, x, y, w_, h, r = op[:6]
            out.append(f'<rect x="{x:g}" y="{y:g}" width="{w_:g}" height="{h:g}" rx="{r:g}" {attrs}/>')
        elif kind == "path":
            out.append(f'<path d="{op[1]}" fill-rule="evenodd" {attrs}/>')
    return "".join(out)


def to_svg(art, color=True, view="-52 -52 104 104", standalone=True, size=None):
    body = _svg_ops(art.ops, color)
    g = f'<g stroke-linejoin="round" stroke-linecap="round">{body}</g>'
    if not standalone:
        return g
    dim = f' width="{size}" height="{size}"' if size else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}"{dim}>{g}</svg>'


# ---------------------------------------------------------------------------
# bounding box (control-point hull - slightly generous, never too small)
# ---------------------------------------------------------------------------

def _pts(ops, tf):
    for op in ops:
        kind = op[0]
        if kind == "group":
            _, dx, dy, sx, sy, rot, flip, sub = op
            ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            fx = -sx if flip else sx

            def child(x, y, tf=tf, dx=dx, dy=dy, fx=fx, sy=sy, ca=ca, sa=sa):
                x, y = x * fx, y * sy
                x, y = x * ca - y * sa, x * sa + y * ca
                return tf(x + dx, y + dy)
            yield from _pts(sub, child)
        elif kind == "merge":
            yield from _pts(op[1], tf)
        elif kind == "ellipse":
            _, cx, cy, rx, ry = op[:5]
            for i in range(16):
                a = i * math.pi / 8
                yield tf(cx + rx * math.cos(a), cy + ry * math.sin(a))
        elif kind == "rect":
            _, x, y, w, h = op[:5]
            for px, py in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
                yield tf(px, py)
        elif kind == "path":
            for seg in parse_path(op[1]):
                if seg[0] == "Z":
                    continue
                vals = seg[1:]
                for i in range(0, len(vals), 2):
                    yield tf(vals[i], vals[i + 1])


def bbox(art):
    """(x0, y0, x1, y1) in art units (y down)."""
    ops = art.ops if isinstance(art, Art) else art
    xs, ys = zip(*_pts(ops, lambda x, y: (x, y)))
    pad = 1.5
    return min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
