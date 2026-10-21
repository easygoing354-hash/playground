"""Original line-art library (all drawn from scratch for this product line).

Every function returns an engine.Art sized to roughly fill a 100 x 100 box
centred on (0, 0) with y pointing down.
"""
import math
from engine import Art, star_pts, heart_d

W = 2.4      # default outline
T = 1.5      # thin detail line


# ===========================================================================
# PUMPKINS
# ===========================================================================

def _stem(a, fill="stem"):
    a.path("M -6 -23 C -7 -31 -6 -39 -3 -45 L 5 -44 C 3 -38 4 -31 7 -23 Z", fill)
    a.ellipse(1, -44.5, 4.2, 1.8, "stem2")


def _leaf_and_vine(a, leaf=True, vine=True, fill="leaf"):
    if vine:
        a.curve("M -4 -33 C -12 -43 -25 -41 -27 -33 C -28 -27 -21 -25 -20 -30 C -19 -33 -23 -34 -24 -32", w=1.9)
    if leaf:
        a.path("M 5 -31 C 11 -43 26 -46 35 -40 C 30 -31 17 -26 5 -31 Z", fill)
        a.curve("M 7 -31 C 15 -36 24 -38 31 -39", w=T)


def pumpkin(ribs=True, leaf=True, vine=True, body="orange", back="orange2", stem=True,
            wide=1.0):
    """Classic cartoon pumpkin. ribs=False -> smooth silhouette with short rib hints."""
    a = Art()
    if stem:
        _stem(a)
    lobes = [(-28, 10, 20, 30, back), (28, 10, 20, 30, back),
             (-15, 9, 22, 33, body), (15, 9, 22, 33, body), (0, 8, 19, 35, body)]
    lobes = [(x * wide, y, rx * wide, ry, f) for x, y, rx, ry, f in lobes]
    if ribs:
        for x, y, rx, ry, f in lobes:
            a.ellipse(x, y, rx, ry, f)
    else:
        sil = Art()
        for x, y, rx, ry, f in lobes:
            sil.ellipse(x, y, rx, ry, body)
        a.merge(sil)
        for sx in (-1, 1):
            a.curve(f"M {sx * 8 * wide:.1f} -25 C {sx * 4 * wide:.1f} -20 {sx * 3 * wide:.1f} -16 {sx * 3 * wide:.1f} -12", w=T)
            a.curve(f"M {sx * 8 * wide:.1f} 42 C {sx * 4 * wide:.1f} 38 {sx * 3 * wide:.1f} 35 {sx * 3 * wide:.1f} 31", w=T)
            a.curve(f"M {sx * 27 * wide:.1f} -19 C {sx * 23 * wide:.1f} -14 {sx * 21 * wide:.1f} -10 {sx * 21 * wide:.1f} -6", w=T)
            a.curve(f"M {sx * 27 * wide:.1f} 39 C {sx * 23 * wide:.1f} 35 {sx * 21 * wide:.1f} 32 {sx * 21 * wide:.1f} 28", w=T)
    _leaf_and_vine(a, leaf, vine)
    return a


def mini_pumpkin(body="orange"):
    """Simpler, chunkier pumpkin for small counters/icons."""
    a = Art()
    a.path("M -4 -22 C -5 -30 -3 -38 1 -42 L 7 -39 C 4 -35 3 -29 5 -22 Z", "stem")
    for x, y, rx, ry in [(-22, 8, 26, 30), (22, 8, 26, 30)]:
        a.ellipse(x, y, rx, ry, body)
    a.ellipse(0, 6, 24, 34, body)
    a.path("M 6 -28 C 12 -38 24 -40 30 -34 C 24 -27 14 -24 6 -28 Z", "leaf")
    return a


def pumpkin_seed(fill="cream"):
    a = Art()
    a.path("M 0 -42 C 22 -40 30 -6 24 16 C 18 36 -18 36 -24 16 C -30 -6 -22 -40 0 -42 Z", fill)
    a.path("M 0 -32 C 14 -30 20 -6 16 12 C 12 26 -12 26 -16 12 C -20 -6 -14 -30 0 -32 Z", "none", w=T)
    return a


# ===========================================================================
# FACE PARTS (one piece each; place pairs with flip=True for the right eye)
# ===========================================================================

def eye(kind="triangle", fill="dark"):
    a = Art()
    if kind == "triangle":
        a.poly([(0, -36), (38, 30), (-38, 30)], fill)
    elif kind == "round":
        a.circle(0, 0, 36, fill)
        a.circle(12, -12, 10, "paper")
    elif kind == "happy":
        a.path("M -40 14 C -28 -34 28 -34 40 14 C 28 -6 -28 -6 -40 14 Z", fill)
    elif kind == "star":
        a.poly(star_pts(0, 3, 42, 18), fill)
    elif kind == "heart":
        a.path(heart_d(0, 2, 0.85), fill)
    elif kind == "angry":
        a.poly([(-38, -24), (38, 4), (32, 30), (-34, 30)], fill)
    elif kind == "googly":
        a.circle(0, 0, 38, "paper")
        a.circle(8, 8, 18, "ink")
        a.circle(13, 2, 5, "paper", stroke="none")
    elif kind == "sleepy":
        a.path("M -40 -6 C -36 34 36 34 40 -6 Z", fill)
        for x1, y1, x2, y2 in [(-30, 20, -38, 32), (0, 28, 0, 40), (30, 20, 38, 32)]:
            a.line(x1, y1, x2, y2, w=3)
    elif kind == "square":
        a.rect(-32, -32, 64, 64, 10, fill)
    elif kind == "diamond":
        a.poly([(0, -40), (32, 0), (0, 40), (-32, 0)], fill)
    elif kind == "moon":
        a.path("M 10 -38 C -26 -36 -36 10 -10 32 C 10 46 34 36 38 18 C 18 30 -6 18 -6 -6 C -6 -22 0 -32 10 -38 Z", fill)
    elif kind == "cute":
        a.circle(0, 0, 36, fill)
        a.circle(-11, -12, 11, "paper")
        a.circle(12, 10, 6, "paper")
    elif kind == "wink":
        a.path("M -40 0 C -18 26 18 26 40 0 C 18 12 -18 12 -40 0 Z", fill)
    elif kind == "spiral":
        a.circle(0, 0, 38, "paper")
        a.curve("M 0 0 C 6 -2 6 8 0 9 C -10 10 -12 -6 -2 -12 C 12 -18 22 -2 16 12 C 10 24 -14 26 -22 12 C -30 -4 -20 -26 2 -28", w=3)
    elif kind == "cat":
        a.path("M -40 0 C -24 -30 24 -30 40 0 C 24 30 -24 30 -40 0 Z", fill)
        a.path("M 0 -22 C 8 -10 8 10 0 22 C -8 10 -8 -10 0 -22 Z", "ink")
    elif kind == "owl":
        a.circle(0, 0, 40, "yellow")
        a.circle(0, 0, 26, "orange3")
        a.circle(0, 2, 14, "ink")
        a.circle(5, -3, 4, "paper", stroke="none")
    elif kind == "x":
        a.path("M -32 -22 L -22 -32 L 0 -10 L 22 -32 L 32 -22 L 10 0 L 32 22 L 22 32 L 0 10 L -22 32 L -32 22 L -10 0 Z", fill)
    return a


EYE_KINDS = ["triangle", "round", "happy", "star", "heart", "angry", "googly", "sleepy",
             "square", "diamond", "moon", "cute", "wink", "spiral", "cat", "x"]


def nose(kind="triangle", fill="dark"):
    a = Art()
    if kind == "triangle":
        a.poly([(0, -32), (30, 26), (-30, 26)], fill)
    elif kind == "down":
        a.poly([(-30, -24), (30, -24), (0, 30)], fill)
    elif kind == "circle":
        a.circle(0, 0, 28, fill)
        a.circle(-9, -9, 7, "paper")
    elif kind == "heart":
        a.path(heart_d(0, 0, 0.7), fill)
    elif kind == "button":
        a.ellipse(0, 0, 34, 24, fill)
        a.ellipse(-11, 0, 5, 7, "ink")
        a.ellipse(11, 0, 5, 7, "ink")
    elif kind == "square":
        a.rect(-24, -24, 48, 48, 6, fill)
    elif kind == "star":
        a.poly(star_pts(0, 3, 34, 15), fill)
    elif kind == "pig":
        a.ellipse(0, 0, 36, 26, "pink")
        a.ellipse(-12, 0, 6, 10, "ink")
        a.ellipse(12, 0, 6, 10, "ink")
    elif kind == "cat":
        a.path("M -22 -12 C -10 -20 10 -20 22 -12 C 18 4 6 14 0 16 C -6 14 -18 4 -22 -12 Z", "pink")
    return a


NOSE_KINDS = ["triangle", "down", "circle", "heart", "button", "square", "star", "pig", "cat"]


def mouth(kind="grin", fill="dark"):
    a = Art()
    if kind == "grin":
        a.path("M -46 -16 C -36 -5 -26 -1 -18 0 L -18 9 L -7 9 L -7 1 L 7 1 L 7 9 L 18 9 L 18 0 "
               "C 26 -1 36 -5 46 -16 C 42 16 24 28 6 28 L 6 19 L -6 19 L -6 28 C -24 28 -42 16 -46 -16 Z", fill)
    elif kind == "smile":
        a.path("M -44 -10 C -26 6 26 6 44 -10 C 36 26 -36 26 -44 -10 Z", fill)
    elif kind == "o":
        a.ellipse(0, 4, 20, 24, fill)
    elif kind == "zigzag":
        top = [(-46, -10), (-34, 0), (-23, -10), (-11, 0), (0, -10), (11, 0), (23, -10), (34, 0), (46, -10)]
        bot = [(36, 14), (24, 6), (12, 16), (0, 6), (-12, 16), (-24, 6), (-36, 14)]
        a.poly(top + bot, fill)
    elif kind == "vampire":
        a.path("M -44 -10 C -26 6 26 6 44 -10 C 36 26 -36 26 -44 -10 Z", fill)
        a.poly([(-26, -2), (-14, 2), (-21, 16)], "paper")
        a.poly([(26, -2), (14, 2), (21, 16)], "paper")
    elif kind == "tongue":
        a.path("M -44 -12 C -26 4 26 4 44 -12 C 36 22 -36 22 -44 -12 Z", fill)
        a.path("M -10 10 C -12 30 12 30 10 10 C 4 14 -4 14 -10 10 Z", "pink")
        a.curve("M 0 13 L 0 22", w=T)
    elif kind == "frown":
        a.path("M -42 18 C -26 -10 26 -10 42 18 C 26 4 -26 4 -42 18 Z", fill)
    elif kind == "buck":
        a.path("M -44 -10 C -26 6 26 6 44 -10 C 36 26 -36 26 -44 -10 Z", fill)
        a.rect(-9, -2, 18, 16, 2, "paper")
        a.line(0, -2, 0, 14, w=T)
    elif kind == "stitch":
        a.rect(-42, -5, 84, 10, 5, fill)
        for x in (-28, -14, 0, 14, 28):
            a.line(x, -14, x, 14, w=3)
    elif kind == "wavy":
        a.path("M -44 -4 C -34 -14 -24 -14 -14 -4 C -4 6 6 6 16 -4 C 24 -12 36 -12 44 -4 "
               "L 44 6 C 36 -2 26 -2 16 6 C 6 16 -4 16 -14 6 C -24 -4 -34 -4 -44 6 Z", fill)
    elif kind == "monster":
        a.path("M -46 -12 C -26 10 26 10 46 -12 C 40 24 -40 24 -46 -12 Z", fill)
        for x in (-30, -12, 6, 24):
            a.poly([(x, 1 if abs(x) < 20 else -3), (x + 10, 2 if abs(x) < 20 else -2), (x + 5, 12)], "paper")
    elif kind == "cat":
        a.path("M -30 -6 C -26 8 -6 10 0 -4 C 6 10 26 8 30 -6 L 34 -2 C 28 16 6 18 0 6 C -6 18 -28 16 -34 -2 Z", fill)
    elif kind == "surprised":
        a.ellipse(0, 2, 13, 16, fill)
    return a


MOUTH_KINDS = ["grin", "smile", "o", "zigzag", "vampire", "tongue", "frown", "buck", "stitch",
               "wavy", "monster", "cat", "surprised"]


def brow(angle=0):
    a = Art()
    a.rect(-34, -7, 68, 14, 7, "dark")
    return a


def cheek():
    a = Art()
    a.circle(0, 0, 30, "pink")
    return a


# ===========================================================================
# ACCESSORIES
# ===========================================================================

def witch_hat():
    a = Art()
    a.ellipse(0, 30, 49, 11, "purple2")
    a.path("M -28 30 C -20 4 -10 -26 6 -47 C 12 -40 8 -30 12 -22 C 16 -6 22 12 28 30 Z", "purple")
    a.path("M -25 21 C -8 26 8 26 25 21 L 27 29 C 8 34 -8 34 -27 29 Z", "orange")
    a.rect(-7, 19, 14, 13, 2, "yellow")
    a.rect(-3, 23, 6, 5, 1, "paper", w=T)
    return a


def top_hat():
    a = Art()
    a.rect(-46, 26, 92, 12, 6, "dark")
    a.path("M -28 28 L -30 -40 C -12 -46 12 -46 30 -40 L 28 28 Z", "dark")
    a.path("M -29 8 L 29 8 L 28 22 L -28 22 Z", "orange")
    return a


def hair_bow():
    a = Art()
    a.path("M -6 -6 C -24 -30 -46 -26 -44 -2 C -46 22 -24 26 -6 6 Z", "pink")
    a.path("M 6 -6 C 24 -30 46 -26 44 -2 C 46 22 24 26 6 6 Z", "pink")
    a.curve("M -10 -2 C -22 -12 -32 -12 -36 -6", w=T)
    a.curve("M 10 -2 C 22 -12 32 -12 36 -6", w=T)
    a.rect(-9, -11, 18, 22, 6, "pink")
    return a


def bow_tie(fill="red"):
    a = Art()
    a.path("M -6 -8 L -44 -26 C -50 -8 -50 8 -44 26 L -6 8 Z", fill)
    a.path("M 6 -8 L 44 -26 C 50 -8 50 8 44 26 L 6 8 Z", fill)
    a.rect(-9, -12, 18, 24, 5, fill)
    for x, y in [(-28, -6), (-24, 8), (28, -6), (24, 8)]:
        a.circle(x, y, 3, "paper", w=T)
    return a


def glasses():
    a = Art()
    a.circle(-24, 0, 20, "paper", w=4)
    a.circle(24, 0, 20, "paper", w=4)
    a.curve("M -6 -2 C -2 -8 2 -8 6 -2", w=4)
    a.curve("M -44 -4 L -50 -10", w=4)
    a.curve("M 44 -4 L 50 -10", w=4)
    a.curve("M -32 -8 C -28 -12 -22 -12 -20 -10", w=T)
    a.curve("M 16 -8 C 20 -12 26 -12 28 -10", w=T)
    return a


def mustache():
    a = Art()
    a.path("M 0 -6 C 8 -14 20 -14 30 -6 C 36 -1 42 2 48 -6 C 48 6 40 14 28 12 C 16 10 8 4 0 4 "
           "C -8 4 -16 10 -28 12 C -40 14 -48 6 -48 -6 C -42 2 -36 -1 -30 -6 C -20 -14 -8 -14 0 -6 Z", "dark")
    return a


def crown():
    a = Art()
    a.poly([(-42, 26), (-42, -18), (-24, 2), (-12, -30), (0, -2), (12, -30), (24, 2), (42, -18), (42, 26)], "gold")
    a.rect(-42, 14, 84, 12, 2, "yellow")
    for x, f in [(-26, "red"), (0, "blue"), (26, "leaf")]:
        a.circle(x, 20, 4.5, f, w=T)
    for x, y in [(-42, -20), (-12, -32), (12, -32), (42, -20)]:
        a.circle(x, y, 4.5, "red", w=T)
    return a


def pirate_hat():
    a = Art()
    a.path("M -48 18 C -40 -8 -24 -28 0 -30 C 24 -28 40 -8 48 18 C 30 8 -30 8 -48 18 Z", "dark")
    a.path("M -48 18 C -30 8 30 8 48 18 C 40 26 -40 26 -48 18 Z", "gold")
    a.circle(0, -10, 9, "paper")
    a.circle(-3, -11, 2.2, "ink", stroke="none")
    a.circle(3, -11, 2.2, "ink", stroke="none")
    a.line(-12, 2, 12, -2, w=3)
    a.line(-12, -2, 12, 2, w=3)
    return a


def eye_patch():
    a = Art()
    a.curve("M -48 -22 C -20 -10 20 -10 48 -22", w=4)
    a.ellipse(0, 6, 24, 20, "dark")
    return a


def cat_ear(inner="pink", fill="dark"):
    a = Art()
    a.path("M -34 36 C -32 6 -22 -22 -6 -42 C 10 -20 26 8 34 36 Z", fill)
    a.path("M -20 30 C -18 10 -12 -8 -5 -22 C 4 -8 14 10 20 30 Z", inner)
    return a


def whiskers():
    a = Art()
    a.ellipse(0, 0, 18, 13, "pink")
    for sx in (-1, 1):
        for y0, y1 in [(-6, -14), (0, 0), (6, 14)]:
            a.line(sx * 18, y0, sx * 48, y1, w=3)
    return a


def owl_tuft():
    a = Art()
    a.path("M -26 34 C -26 10 -16 -18 4 -40 C 8 -20 22 10 26 34 Z", "brown")
    a.curve("M -10 26 C -8 12 -4 0 2 -12", w=T)
    a.curve("M 8 26 C 8 14 6 2 4 -6", w=T)
    return a


def owl_wing():
    a = Art()
    a.path("M 0 -46 C 26 -36 34 -4 26 24 C 22 36 12 46 0 46 C -12 30 -16 -10 0 -46 Z", "brown")
    for y in (-14, 4, 22):
        a.curve(f"M {-6 + (y + 14) * 0.05:.1f} {y} C 4 {y + 8} 16 {y + 8} 26 {y - 2}", w=T)
    return a


def beak(fill="orange"):
    a = Art()
    a.path("M -24 -20 C -10 -28 10 -28 24 -20 C 16 0 6 22 0 34 C -6 22 -16 0 -24 -20 Z", fill)
    a.curve("M -18 -16 C -6 -12 6 -12 18 -16", w=T)
    return a


def feather(fill="red"):
    a = Art()
    a.path("M 0 46 C -6 30 -26 6 -24 -16 C -22 -36 -10 -46 0 -46 C 10 -46 22 -36 24 -16 C 26 6 6 30 0 46 Z", fill)
    a.curve("M 0 44 C 0 20 0 -10 0 -38", w=T)
    for y in (-24, -8, 8):
        a.curve(f"M 0 {y + 8} L -12 {y}", w=1.2)
        a.curve(f"M 0 {y + 8} L 12 {y}", w=1.2)
    return a


def wattle():
    a = Art()
    a.path("M -6 -34 C 10 -30 14 -10 12 8 C 10 26 4 36 -4 34 C -14 30 -10 12 -12 -4 C -14 -18 -14 -30 -6 -34 Z", "red")
    return a


def turkey_feet():
    a = Art()
    for sx in (-1, 1):
        x = sx * 20
        a.path(f"M {x - 3} -30 L {x + 3} -30 L {x + 3} 6 L {x + 16} 26 L {x + 11} 29 L {x + 1} 14 L {x + 2} 32 "
               f"L {x - 3} 32 L {x - 2} 14 L {x - 11} 29 L {x - 16} 26 L {x - 3} 6 Z", "orange")
    return a


def straw_tuft():
    a = Art()
    pts = [(-40, 26), (-46, -8), (-30, 6), (-30, -34), (-14, 0), (-6, -42), (4, -2), (16, -38),
           (20, 4), (38, -26), (34, 10), (48, 0), (40, 26)]
    a.poly(pts, "straw")
    for x1, y1, x2, y2 in [(-30, 20, -34, 0), (-12, 20, -12, -6), (6, 20, 8, -6), (24, 20, 28, 0)]:
        a.line(x1, y1, x2, y2, w=1.2)
    return a


def farmer_hat():
    a = Art()
    a.path("M -50 22 C -40 10 40 10 50 22 C 30 32 -30 32 -50 22 Z", "straw")
    a.path("M -30 18 C -30 -6 -22 -30 0 -30 C 22 -30 30 -6 30 18 C 10 22 -10 22 -30 18 Z", "straw")
    a.path("M -30 6 C -10 12 10 12 30 6 L 30 16 C 10 22 -10 22 -30 16 Z", "red")
    a.rect(8, -18, 14, 13, 1, "blue", w=T)
    for x, y in [(8, -18), (22, -18), (8, -5), (22, -5)]:
        a.line(x - 2, y - 2, x + 2, y + 2, w=1.2)
    for x in (-40, -20, 0, 20, 40):
        a.line(x, 20, x + 2, 26, w=1.2)
    return a


def patch(fill="blue"):
    a = Art()
    a.rect(-30, -30, 60, 60, 4, fill)
    for i in range(-24, 25, 12):
        for x1, y1, x2, y2 in [(i - 3, -33, i + 3, -27), (i - 3, 27, i + 3, 33),
                               (-33, i - 3, -27, i + 3), (27, i - 3, 33, i + 3)]:
            a.line(x1, y1, x2, y2, w=1.4)
    return a


def bandage(length=96, tilt=0):
    a = Art()
    a.rect(-length / 2, -8, length, 16, 4, "bone")
    for x in range(int(-length / 2) + 12, int(length / 2) - 4, 16):
        a.line(x, -8, x + 4, 8, w=1.1)
    return a


def bat_wing():
    a = Art()
    a.path("M 0 -14 C 16 -30 36 -36 48 -26 C 42 -18 44 -10 48 -4 C 40 -6 34 -2 32 6 "
           "C 26 0 18 2 14 10 C 10 2 4 0 0 4 Z", "dark")
    a.curve("M 4 -10 C 16 -16 28 -18 40 -16", w=T)
    return a


def bat_ear():
    a = Art()
    a.path("M -20 30 C -18 4 -10 -20 0 -40 C 10 -20 18 4 20 30 Z", "dark")
    a.path("M -10 24 C -8 8 -4 -6 0 -18 C 4 -6 8 8 10 24 Z", "pink")
    return a


def unicorn_horn():
    a = Art()
    a.path("M -16 40 L 0 -46 L 16 40 C 6 44 -6 44 -16 40 Z", "gold")
    for y in (20, 0, -20):
        hw = 14 * (y + 46) / 86
        a.curve(f"M {-hw:.1f} {y + 6} L {hw:.1f} {y - 4}", w=T)
    return a


def mane_lock(fill="purple"):
    a = Art()
    a.path("M -10 -44 C 18 -40 26 -14 18 6 C 12 22 18 32 26 40 C 6 44 -16 34 -20 12 C -24 -10 -24 -32 -10 -44 Z", fill)
    a.curve("M -8 -32 C 4 -24 6 -6 0 10", w=T)
    return a


def flower(petal="pink", center="yellow"):
    a = Art()
    for i in range(5):
        ang = math.radians(-90 + i * 72)
        a.circle(22 * math.cos(ang), 22 * math.sin(ang), 18, petal)
    a.circle(0, 0, 14, center)
    return a


def antenna():
    a = Art()
    a.rect(-4, -18, 8, 60, 3, "silver")
    a.circle(0, -30, 14, "red")
    a.circle(-4, -34, 4, "paper", stroke="none")
    a.rect(-18, 34, 36, 12, 4, "silver")
    return a


def bolt():
    a = Art()
    a.rect(-14, -30, 28, 60, 4, "silver")
    a.rect(-26, -14, 52, 28, 5, "gray")
    a.line(-26, 0, 26, 0, w=T)
    return a


def robot_mouth():
    a = Art()
    a.rect(-44, -16, 88, 32, 6, "silver")
    for x in (-22, 0, 22):
        a.line(x, -16, x, 16, w=T)
    a.line(-44, 0, 44, 0, w=T)
    return a


def control_panel():
    a = Art()
    a.rect(-44, -30, 88, 60, 8, "lgray")
    a.circle(-24, -10, 9, "red")
    a.circle(0, -10, 9, "yellow")
    a.circle(24, -10, 9, "leaf")
    a.rect(-30, 8, 60, 12, 6, "blue")
    return a


def horn(fill="purple"):
    a = Art()
    a.path("M -16 40 C -18 12 -12 -20 14 -44 C 8 -18 12 10 18 40 C 6 44 -6 44 -16 40 Z", fill)
    a.curve("M -14 24 C -4 22 8 22 16 24", w=T)
    a.curve("M -11 6 C -2 4 8 4 14 6", w=T)
    return a


def eye_stalk():
    a = Art()
    a.path("M -6 44 C -8 24 -4 0 -4 -12 L 4 -12 C 4 0 8 24 6 44 Z", "skin")
    a.circle(0, -26, 20, "paper")
    a.circle(3, -24, 9, "ink")
    return a


def vampire_collar():
    a = Art()
    a.path("M -48 -40 L -20 24 L 0 10 L 20 24 L 48 -40 C 30 -16 20 -4 0 -4 C -20 -4 -30 -16 -48 -40 Z", "dark")
    a.path("M -40 -26 L -18 14 L 0 4 C -14 0 -28 -10 -40 -26 Z", "red", w=T)
    a.path("M 40 -26 L 18 14 L 0 4 C 14 0 28 -10 40 -26 Z", "red", w=T)
    return a


def hair_peak():
    a = Art()
    a.path("M -48 -20 C -30 -36 30 -36 48 -20 C 40 -8 30 -6 20 -10 C 12 -14 6 -6 0 10 "
           "C -6 -6 -12 -14 -20 -10 C -30 -6 -40 -8 -48 -20 Z", "dark")
    return a


def witch_hair(fill="leaf"):
    a = Art()
    a.path("M -10 -40 C 0 -36 10 -36 14 -40 C 10 -10 14 20 20 44 C 12 38 8 30 4 22 C 4 32 2 40 -4 46 "
           "C -6 34 -6 24 -6 14 C -10 24 -16 30 -22 34 C -16 10 -14 -14 -10 -40 Z", fill)
    return a


def bandana(fill="red"):
    a = Art()
    a.path("M -48 -20 C -20 -30 20 -30 48 -20 C 30 0 14 18 0 34 C -14 18 -30 0 -48 -20 Z", fill)
    for x, y in [(-24, -12), (0, -14), (24, -12), (-10, 4), (12, 4), (0, 20)]:
        a.circle(x, y, 3.5, "paper", w=1.2)
    return a


def leaf_crown_band():
    a = Art()
    a.rect(-48, -10, 96, 20, 4, "paper")
    return a


# ===========================================================================
# FALL + HALLOWEEN ITEMS
# ===========================================================================

def maple_leaf(fill="maple"):
    a = Art()
    pts = [(0, -46), (8, -30), (16, -34), (14, -16), (30, -26), (28, -18), (44, -18), (34, -6),
           (40, -2), (22, 10), (26, 18), (6, 14), (4, 26), (-4, 26), (-6, 14), (-26, 18), (-22, 10),
           (-40, -2), (-34, -6), (-44, -18), (-28, -18), (-30, -26), (-14, -16), (-16, -34), (-8, -30)]
    a.poly(pts, fill)
    a.path("M 0 20 L 0 46", "none", w=3)
    for x2, y2 in [(0, -34), (28, -14), (-28, -14), (16, 10), (-16, 10)]:
        a.curve(f"M 0 16 L {x2} {y2}", w=T)
    return a


def oak_leaf(fill="rust"):
    a = Art()
    a.path("M 0 -46 C 10 -46 14 -38 10 -32 C 20 -34 24 -24 16 -18 C 28 -18 30 -6 20 -2 "
           "C 30 2 30 14 18 14 C 24 22 18 30 6 26 L 2 32 L 2 46 L -2 46 L -2 32 L -6 26 "
           "C -18 30 -24 22 -18 14 C -30 14 -30 2 -20 -2 C -30 -6 -28 -18 -16 -18 "
           "C -24 -24 -20 -34 -10 -32 C -14 -38 -10 -46 0 -46 Z", fill)
    a.curve("M 0 30 L 0 -38", w=T)
    for y, x in [(-24, 10), (-10, 14), (6, 12)]:
        a.curve(f"M 0 {y + 6} L {x} {y}", w=1.2)
        a.curve(f"M 0 {y + 6} L {-x} {y}", w=1.2)
    return a


def simple_leaf(fill="gold"):
    a = Art()
    a.path("M 0 -46 C 26 -30 30 6 4 32 L 2 46 L -2 46 L -4 32 C -30 6 -26 -30 0 -46 Z", fill)
    a.curve("M 0 32 L 0 -36", w=T)
    for y in (-20, -6, 8, 20):
        a.curve(f"M 0 {y + 6} L 14 {y - 4}", w=1.2)
        a.curve(f"M 0 {y + 6} L -14 {y - 4}", w=1.2)
    return a


def acorn():
    a = Art()
    a.path("M -26 -8 C -28 18 -14 40 0 46 C 14 40 28 18 26 -8 Z", "tan")
    a.path("M -32 -6 C -34 -24 -18 -34 0 -34 C 18 -34 34 -24 32 -6 C 20 0 -20 0 -32 -6 Z", "brown")
    for x1, x2 in [(-20, -10), (-6, 4), (8, 18)]:
        a.line(x1, -26, x2, -4, w=1.2)
        a.line(x2, -26, x1, -4, w=1.2)
    a.path("M -2 -34 C -2 -40 0 -44 6 -46 L 8 -42 C 4 -40 3 -37 3 -34 Z", "stem")
    a.curve("M 12 18 C 14 12 14 6 12 2", w=T)
    return a


def apple(fill="red"):
    a = Art()
    a.path("M 0 -26 C 14 -38 44 -34 44 -2 C 44 26 24 46 10 42 C 4 40 -4 40 -10 42 "
           "C -24 46 -44 26 -44 -2 C -44 -34 -14 -38 0 -26 Z", fill)
    a.path("M -2 -24 C -2 -32 0 -40 4 -46 L 8 -43 C 5 -38 3 -32 3 -24 Z", "stem")
    a.path("M 5 -34 C 12 -46 26 -46 32 -40 C 26 -32 14 -30 5 -34 Z", "leaf")
    a.curve("M -28 -12 C -30 -4 -28 4 -24 10", w=T)
    return a


def sunflower():
    a = Art()
    for i in range(12):
        ang = i * 30
        p = Art().path("M 0 -2 C 8 -12 8 -30 0 -46 C -8 -30 -8 -12 0 -2 Z", "yellow")
        a.add(p, rot=ang)
    a.circle(0, 0, 20, "brown")
    for x, y in [(-8, -8), (0, -10), (8, -8), (-10, 0), (0, 0), (10, 0), (-8, 8), (0, 10), (8, 8)]:
        a.circle(x, y, 2, "ink", stroke="none")
    return a


def corn():
    a = Art()
    a.path("M 0 -46 C 16 -46 20 -20 18 4 C 16 28 8 40 0 42 C -8 40 -16 28 -18 4 C -20 -20 -16 -46 0 -46 Z", "yellow")
    for y in range(-36, 36, 9):
        hw = 15 if -28 < y < 22 else 10
        a.line(-hw, y, hw, y, w=1.1)
    for x in (-8, 0, 8):
        a.curve(f"M {x} -42 C {x * 1.2} -10 {x * 1.2} 20 {x * 0.6} 40", w=1.1)
    a.path("M -4 46 C -20 30 -30 6 -32 -26 C -18 -10 -12 10 -4 30 Z", "leaf")
    a.path("M 4 46 C 20 30 30 6 32 -26 C 18 -10 12 10 4 30 Z", "leaf")
    return a


def candy_corn():
    a = Art()
    a.path("M -32 34 C -24 6 -12 -26 -4 -40 C -2 -44 2 -44 4 -40 C 12 -26 24 6 32 34 "
           "C 32 42 -32 42 -32 34 Z", "yellow")
    a.path("M -27 20 C -20 -2 -14 -16 -11 -22 C -4 -20 4 -20 11 -22 C 14 -16 20 -2 27 20 C 10 24 -10 24 -27 20 Z", "orange")
    a.path("M -11 -22 C -8 -30 -6 -36 -4 -40 C -2 -44 2 -44 4 -40 C 6 -36 8 -30 11 -22 C 4 -20 -4 -20 -11 -22 Z", "white")
    return a


def ghost(face=True):
    a = Art()
    a.path("M -34 40 C -36 10 -38 -10 -32 -26 C -24 -44 24 -44 32 -26 C 38 -10 36 10 34 40 "
           "C 28 34 22 34 17 42 C 12 34 5 34 0 42 C -5 34 -12 34 -17 42 C -22 34 -28 34 -34 40 Z", "ghost")
    a.path("M -34 0 C -44 -4 -48 4 -44 10 C -40 12 -36 10 -34 8", "ghost")
    a.path("M 34 0 C 44 -4 48 4 44 10 C 40 12 36 10 34 8", "ghost")
    if face:
        a.ellipse(-12, -16, 5, 7, "ink")
        a.ellipse(12, -16, 5, 7, "ink")
        a.ellipse(0, 0, 6, 8, "ink")
        a.circle(-20, -6, 4, "pink", stroke="none")
        a.circle(20, -6, 4, "pink", stroke="none")
    return a


def bat():
    a = Art()
    w = bat_wing()
    a.add(w, dx=6, dy=0)
    a.add(w, dx=-6, dy=0, flip=True)
    a.path("M -16 -12 L -14 -30 L -6 -18 L 6 -18 L 14 -30 L 16 -12 C 18 6 10 16 0 16 C -10 16 -18 6 -16 -12 Z", "dark")
    a.circle(-6, -6, 3.5, "paper", stroke="none")
    a.circle(6, -6, 3.5, "paper", stroke="none")
    a.poly([(-4, 4), (-2, 9), (0, 4)], "paper", w=0.8)
    a.poly([(4, 4), (2, 9), (0, 4)], "paper", w=0.8)
    return a


def black_cat():
    a = Art()
    a.path("M 16 38 C 42 38 50 14 42 -2 C 38 -10 30 -10 30 -4 C 30 0 34 0 36 2 C 40 14 34 30 14 30 Z", "dark")
    a.path("M -26 42 C -30 18 -22 -2 0 -4 C 22 -2 30 18 26 42 Z", "dark")
    a.path("M -24 -18 L -22 -46 L -8 -32 L 8 -32 L 22 -46 L 24 -18 C 26 -2 14 6 0 6 C -14 6 -26 -2 -24 -18 Z", "dark")
    a.ellipse(-10, -18, 5, 6, "yellow")
    a.ellipse(10, -18, 5, 6, "yellow")
    a.ellipse(-10, -18, 1.6, 5, "ink", stroke="none")
    a.ellipse(10, -18, 1.6, 5, "ink", stroke="none")
    a.poly([(-3, -10), (3, -10), (0, -6)], "pink", w=1)
    for sx in (-1, 1):
        a.line(sx * 8, -7, sx * 22, -10, stroke="lgray", w=1)
        a.line(sx * 8, -5, sx * 22, -3, stroke="lgray", w=1)
    return a


def owl():
    a = Art()
    a.path("M -32 -16 C -34 -40 -18 -40 -16 -32 C -6 -36 6 -36 16 -32 C 18 -40 34 -40 32 -16 "
           "C 40 10 30 42 0 42 C -30 42 -40 10 -32 -16 Z", "brown")
    a.path("M -18 4 C -20 30 -10 38 0 38 C 10 38 20 30 18 4 C 10 -2 -10 -2 -18 4 Z", "tan")
    for x, y in [(-8, 14), (8, 14), (0, 22), (-8, 30), (8, 30)]:
        a.curve(f"M {x - 4} {y} C {x - 2} {y + 4} {x + 2} {y + 4} {x + 4} {y}", w=1.2)
    for sx in (-1, 1):
        a.circle(sx * 13, -16, 12, "paper")
        a.circle(sx * 13, -15, 6, "ink")
        a.circle(sx * 13 + 2, -17, 2, "paper", stroke="none")
    a.poly([(-5, -6), (5, -6), (0, 4)], "orange")
    a.path("M -32 -6 C -44 6 -40 24 -28 30 C -30 16 -28 4 -24 -4 Z", "stem")
    a.path("M 32 -6 C 44 6 40 24 28 30 C 30 16 28 4 24 -4 Z", "stem")
    return a


def spider():
    a = Art()
    a.line(0, -50, 0, -18, w=1.4)
    for sx in (-1, 1):
        for y, dy in [(-6, -22), (0, -8), (6, 8), (12, 22)]:
            a.curve(f"M {sx * 10} {y} C {sx * 24} {y + dy * 0.2 - 10} {sx * 34} {y + dy * 0.4} {sx * 40} {y + dy}", w=3)
    a.ellipse(0, 6, 18, 20, "dark")
    a.circle(0, -14, 11, "dark")
    a.circle(-4, -15, 3, "paper", stroke="none")
    a.circle(4, -15, 3, "paper", stroke="none")
    return a


def spider_web():
    a = Art()
    n = 8
    for i in range(n):
        ang = math.radians(i * 360 / n)
        a.line(0, 0, 46 * math.cos(ang), 46 * math.sin(ang), w=T)
    for r in (12, 24, 36, 46):
        d = ""
        for i in range(n + 1):
            ang = math.radians(i * 360 / n)
            ang2 = math.radians((i - 0.5) * 360 / n)
            x, y = r * math.cos(ang), r * math.sin(ang)
            if i == 0:
                d = f"M {x:.1f} {y:.1f}"
            else:
                q = r * 0.8
                d += f" Q {q * math.cos(ang2):.1f} {q * math.sin(ang2):.1f} {x:.1f} {y:.1f}"
        a.curve(d, w=T)
    return a


def moon():
    a = Art()
    a.path("M 6 -44 C -30 -40 -44 4 -22 30 C -4 50 30 46 42 22 C 14 30 -12 12 -10 -14 C -8 -30 -4 -38 6 -44 Z", "moon")
    a.circle(-18, 4, 4, "none", w=T)
    a.circle(-6, 24, 3, "none", w=T)
    return a


def star(fill="yellow"):
    a = Art()
    a.poly(star_pts(0, 4, 46, 20), fill)
    return a


def hay_bale():
    a = Art()
    a.rect(-46, -28, 92, 56, 10, "straw")
    a.rect(-24, -28, 8, 56, 0, "brown", w=T)
    a.rect(16, -28, 8, 56, 0, "brown", w=T)
    for x, y in [(-38, -16), (-2, -10), (34, -14), (-34, 14), (4, 16), (36, 12)]:
        a.curve(f"M {x - 5} {y} C {x - 2} {y - 4} {x + 2} {y + 4} {x + 5} {y}", w=1.2)
    return a


def mushroom():
    a = Art()
    a.path("M -12 4 C -14 20 -12 34 -16 42 L 16 42 C 12 34 14 20 12 4 Z", "cream")
    a.path("M -44 8 C -46 -20 -24 -40 0 -40 C 24 -40 46 -20 44 8 C 20 14 -20 14 -44 8 Z", "red")
    for x, y, r in [(-22, -16, 6), (2, -28, 5), (22, -12, 7), (-4, -6, 4)]:
        a.circle(x, y, r, "paper", w=T)
    return a


def haunted_house():
    a = Art()
    a.rect(-38, -6, 56, 50, 0, "purple")
    a.poly([(-44, -4), (-10, -32), (24, -4)], "purple2")
    a.rect(18, -30, 24, 74, 0, "purple")
    a.poly([(14, -28), (30, -50), (46, -28)], "purple2")
    for x, y in [(-30, 4), (-6, 4), (24, -18), (24, 6)]:
        a.rect(x, y, 12, 14, 1, "yellow", w=T)
        a.line(x + 6, y, x + 6, y + 14, w=1.1)
    a.path("M -22 44 L -22 30 C -22 22 -10 22 -10 30 L -10 44 Z", "brown")
    a.circle(-14, 36, 1.4, "ink", stroke="none")
    a.circle(-10, -14, 5, "yellow", w=T)
    return a


def cauldron():
    a = Art()
    for x, y, r in [(-12, -26, 7), (6, -34, 9), (18, -22, 5)]:
        a.circle(x, y, r, "green")
    a.path("M -40 -12 C -46 14 -30 38 0 38 C 30 38 46 14 40 -12 Z", "dark")
    a.rect(-44, -18, 88, 12, 6, "dark")
    a.path("M -38 -14 C -20 -22 20 -22 38 -14", "green", w=T)
    a.path("M -22 36 L -28 46 L -18 46 Z", "dark")
    a.path("M 22 36 L 28 46 L 18 46 Z", "dark")
    return a


def broom():
    a = Art()
    a.rect(-4, -48, 8, 62, 3, "stem")
    a.path("M -10 12 L 10 12 C 18 24 26 36 30 46 L -30 46 C -26 36 -18 24 -10 12 Z", "straw")
    a.rect(-12, 10, 24, 8, 2, "red")
    for x in (-18, -8, 2, 12, 20):
        a.line(x * 0.5, 20, x, 44, w=1.1)
    return a


def sprout():
    a = Art()
    a.path("M -40 44 C -30 26 30 26 40 44 Z", "brown")
    a.curve("M 0 32 C 0 18 -2 4 0 -8", w=3)
    a.path("M 0 -8 C -6 -24 -26 -30 -38 -22 C -30 -8 -12 -2 0 -8 Z", "leaf")
    a.path("M 0 -8 C 6 -24 26 -30 38 -22 C 30 -8 12 -2 0 -8 Z", "leaf")
    return a


def vine_plant():
    a = Art()
    a.path("M -46 44 C -36 34 36 34 46 44 Z", "brown")
    a.curve("M -40 30 C -24 22 -10 34 4 24 C 18 14 30 24 42 14", w=3)
    for x, y, rot in [(-26, 18, -20), (8, 10, 10), (32, 2, 30)]:
        lf = Art().path("M 0 10 C -16 6 -18 -14 -6 -22 C 0 -16 6 -18 10 -22 C 20 -10 14 6 0 10 Z", "leaf")
        lf.curve("M 0 8 L 0 -14", w=1.2)
        a.add(lf, dx=x, dy=y, rot=rot)
    a.curve("M -10 30 C -12 40 -2 42 -2 36 C -2 32 -6 32 -6 34", w=1.4)
    a.curve("M 20 20 C 22 30 32 30 30 24 C 28 20 24 22 25 24", w=1.4)
    return a


def pumpkin_flower():
    a = Art()
    a.path("M -46 44 C -36 34 36 34 46 44 Z", "brown")
    a.curve("M 0 36 C -2 26 0 14 0 8", w=3)
    lf = Art().path("M 0 10 C -16 6 -18 -14 -6 -22 C 0 -16 6 -18 10 -22 C 20 -10 14 6 0 10 Z", "leaf")
    a.add(lf, dx=-22, dy=24, rot=-60, s=0.9)
    a.add(lf, dx=24, dy=24, rot=60, s=0.9)
    for i in range(5):
        ang = -90 + i * 72
        p = Art().path("M 0 0 C 12 -6 16 -22 0 -32 C -16 -22 -12 -6 0 0 Z", "yellow")
        a.add(p, dx=0, dy=-12, rot=ang)
    a.circle(0, -12, 8, "orange")
    return a


def green_pumpkin():
    return pumpkin(body="green", back="olive", leaf=True, vine=True)


def pie_slice():
    a = Art()
    a.path("M -46 22 L 34 -30 C 44 -18 48 2 42 18 Z", "orange")
    a.path("M -46 22 L 42 18 L 42 30 L -46 34 Z", "tan")
    a.path("M 34 -30 C 44 -18 48 2 42 18 L 42 30 C 52 14 50 -16 38 -36 Z", "tan")
    a.path("M -6 4 C -12 -4 -4 -12 4 -8 C 6 -16 18 -14 16 -6 C 24 -4 22 6 14 6 Z", "paper")
    return a


def scarecrow_head():
    a = Art()
    a.circle(0, 4, 36, "tan")
    for sx in (-1, 1):
        a.circle(sx * 13, -2, 5, "ink")
    a.poly([(-6, 6), (6, 6), (0, 16)], "orange")
    a.curve("M -18 22 C -6 30 6 30 18 22", w=2)
    for x in (-12, -4, 4, 12):
        a.line(x, 21 + abs(x) * -0.2 + 3, x + 1, 29 - abs(x) * 0.3, w=1.1)
    return a


def shirt(fill="plaid"):
    a = Art()
    a.path("M -20 -40 L -46 -26 L -38 -4 L -28 -10 L -28 40 L 28 40 L 28 -10 L 38 -4 L 46 -26 L 20 -40 "
           "C 12 -30 -12 -30 -20 -40 Z", fill)
    for x in (-14, 0, 14):
        a.line(x, -32, x, 40, w=1.1)
    for y in (-14, 4, 22):
        a.line(-28, y, 28, y, w=1.1)
    return a


def overalls():
    a = Art()
    a.path("M -26 -40 L -18 -40 L -18 -14 L 18 -14 L 18 -40 L 26 -40 L 26 -14 L 30 46 L 6 46 L 2 14 "
           "L -2 14 L -6 46 L -30 46 L -26 -14 Z", "denim")
    a.rect(-12, -10, 24, 16, 2, "denim", w=T)
    a.circle(-22, -12, 3, "gold", w=1.2)
    a.circle(22, -12, 3, "gold", w=1.2)
    return a


def crow():
    a = Art()
    a.path("M -30 6 C -30 -16 -10 -24 6 -18 C 14 -30 30 -30 34 -18 L 46 -14 L 34 -10 "
           "C 34 10 22 22 4 24 L -10 36 L -12 24 C -26 20 -30 14 -30 6 Z", "dark")
    a.circle(22, -20, 3.5, "paper", stroke="none")
    a.curve("M -18 0 C -8 -6 6 -4 12 4", stroke="lgray", w=1.4)
    a.line(0, 24, -2, 38, w=2)
    a.line(8, 22, 8, 38, w=2)
    return a


# ---- simple picture words (rhyming / beginning sounds) -------------------

def hat_simple():
    return top_hat()


def spoon():
    a = Art()
    a.ellipse(0, -26, 16, 20, "silver")
    a.path("M -4 -8 L 4 -8 L 6 44 L -6 44 Z", "silver")
    return a


def car():
    a = Art()
    a.path("M -46 16 L -46 -2 C -46 -8 -40 -10 -34 -10 L -22 -28 C -18 -32 16 -32 22 -28 L 32 -10 "
           "C 42 -10 46 -6 46 2 L 46 16 Z", "red")
    a.path("M -18 -12 L -12 -24 L 0 -24 L 0 -12 Z", "sky", w=T)
    a.path("M 6 -12 L 6 -24 L 16 -24 L 24 -12 Z", "sky", w=T)
    for x in (-26, 26):
        a.circle(x, 18, 11, "dark")
        a.circle(x, 18, 4, "silver")
    return a


def rake():
    a = Art()
    a.rect(-3, -48, 6, 70, 2, "stem")
    a.path("M -30 22 L 30 22 L 30 28 L -30 28 Z", "gray")
    for x in range(-28, 31, 8):
        a.rect(x - 1.5, 28, 3, 18, 1, "gray", w=1.2)
    return a


def cake():
    a = Art()
    a.rect(-40, -6, 80, 44, 4, "pink")
    a.path("M -40 4 C -32 14 -24 -2 -16 8 C -8 18 0 -2 8 8 C 16 18 24 -2 32 8 C 36 12 40 8 40 4 L 40 -6 L -40 -6 Z", "cream")
    for x in (-20, 0, 20):
        a.rect(x - 3, -30, 6, 24, 1, "blue")
        a.path(f"M {x} -44 C {x + 6} -38 {x + 4} -32 {x} -32 C {x - 4} -32 {x - 6} -38 {x} -44 Z", "yellow")
    return a


def bee():
    a = Art()
    a.ellipse(-8, -22, 14, 18, "sky")
    a.ellipse(10, -22, 14, 18, "sky")
    a.ellipse(0, 6, 36, 26, "yellow")
    for x in (-12, 4, 18):
        a.path(f"M {x - 5} -16 C {x - 9} -4 {x - 9} 16 {x - 5} 28 L {x + 3} 28 C {x - 1} 16 {x - 1} -4 {x + 3} -16 Z", "dark", w=1.2)
    a.circle(-26, 0, 4, "ink")
    a.path("M 36 6 L 48 8 L 36 12 Z", "dark")
    return a


def tree():
    a = Art()
    a.path("M -8 46 L -6 10 L 6 10 L 8 46 Z", "stem")
    canopy = Art()
    for x, y, r in [(-20, -6, 20), (20, -6, 20), (0, -24, 24), (-14, -30, 16), (16, -30, 16), (0, -4, 18)]:
        canopy.circle(x, y, r, "orange")
    a.merge(canopy)
    return a


def bug():
    a = Art()
    a.circle(0, -28, 12, "dark")
    a.ellipse(0, 6, 30, 32, "red")
    a.line(0, -24, 0, 38, w=2)
    for x, y in [(-14, -6), (14, -6), (-16, 14), (16, 14), (-8, 28), (8, 28)]:
        a.circle(x, y, 5, "ink")
    a.curve("M -6 -38 C -10 -46 -16 -48 -20 -46", w=2)
    a.curve("M 6 -38 C 10 -46 16 -48 20 -46", w=2)
    return a


def mug():
    a = Art()
    a.path("M 24 -14 C 52 -14 52 26 24 26 L 24 17 C 40 17 40 -5 24 -5 Z", "orange")
    a.rect(-32, -24, 60, 64, 8, "orange")
    a.rect(-32, -24, 60, 10, 4, "brown")
    for x in (-18, 0, 16):
        a.curve(f"M {x} -30 C {x - 6} -36 {x + 6} -40 {x} -48", w=1.6)
    return a


def bat_simple():
    return bat()


def web_simple():
    return spider_web()


def hat_witch():
    return witch_hat()


def leaf_pic():
    return maple_leaf()


# Register picture words for literacy pages: word -> builder
PICTURES = {
    "apple": apple, "acorn": acorn, "bat": bat, "bee": bee, "broom": broom, "bug": bug,
    "cake": cake, "car": car, "cat": black_cat, "corn": corn, "ghost": ghost, "hat": top_hat,
    "leaf": maple_leaf, "moon": moon, "mug": mug, "mushroom": mushroom, "owl": owl,
    "pumpkin": lambda: pumpkin(), "pie": pie_slice, "rake": rake, "spider": spider, "spoon": spoon,
    "star": star, "sunflower": sunflower, "tree": tree, "web": spider_web, "witch hat": witch_hat,
    "candy corn": candy_corn, "cauldron": cauldron, "hay": hay_bale, "crow": crow,
    "house": haunted_house, "seed": pumpkin_seed,
}


# ===========================================================================
# SHAPES (math crafts)
# ===========================================================================

def shape(kind, fill="yellow"):
    a = Art()
    if kind == "circle":
        a.circle(0, 0, 40, fill)
    elif kind == "square":
        a.rect(-36, -36, 72, 72, 0, fill)
    elif kind == "triangle":
        a.poly([(0, -40), (44, 36), (-44, 36)], fill)
    elif kind == "rectangle":
        a.rect(-46, -24, 92, 48, 0, fill)
    elif kind == "oval":
        a.ellipse(0, 0, 46, 30, fill)
    elif kind == "hexagon":
        a.poly([(42 * math.cos(math.radians(60 * i)), 42 * math.sin(math.radians(60 * i))) for i in range(6)], fill)
    elif kind == "star":
        a.poly(star_pts(0, 4, 46, 20), fill)
    elif kind == "heart":
        a.path(heart_d(0, 2, 1.0), fill)
    elif kind == "rhombus":
        a.poly([(0, -44), (32, 0), (0, 44), (-32, 0)], fill)
    elif kind == "semicircle":
        a.path("M -44 14 C -44 -46 44 -46 44 14 Z", fill)
    return a


SHAPE_KINDS = ["circle", "square", "triangle", "rectangle", "oval", "hexagon", "star", "heart", "rhombus", "semicircle"]


# ===========================================================================
# EXTRA CRAFT PIECES
# ===========================================================================

def hero_mask(fill="blue"):
    a = Art()
    a.path("M -48 -8 C -44 -24 -20 -24 0 -14 C 20 -24 44 -24 48 -8 C 50 8 36 18 20 16 "
           "C 10 14 6 8 0 8 C -6 8 -10 14 -20 16 C -36 18 -50 8 -48 -8 Z", fill)
    a.ellipse(-20, -3, 11, 8, "paper")
    a.ellipse(20, -3, 11, 8, "paper")
    return a


def cape(fill="red"):
    a = Art()
    a.path("M -26 -44 C -10 -36 10 -36 26 -44 L 48 40 C 30 30 16 46 0 38 C -16 46 -30 30 -48 40 Z", fill)
    a.curve("M -10 -36 L -18 36", w=T)
    a.curve("M 10 -36 L 18 36", w=T)
    return a


def badge(fill="yellow"):
    a = Art()
    a.circle(0, 0, 40, fill)
    a.poly(star_pts(0, 3, 28, 12), "red")
    return a


def unicorn_ear():
    return cat_ear(inner="pink", fill="white")


def pumpkin_inside():
    """Pumpkin cut in half: skin, pulp (flesh), strings and seeds."""
    a = Art()
    _stem(a)
    sil = Art()
    for x, y, rx, ry in [(-28, 10, 20, 30), (28, 10, 20, 30), (-15, 9, 22, 33), (15, 9, 22, 33), (0, 8, 19, 35)]:
        sil.ellipse(x, y, rx, ry, "orange")
    a.merge(sil)
    a.path("M -38 10 C -38 -14 -20 -22 0 -22 C 20 -22 38 -14 38 10 C 38 30 20 38 0 38 "
           "C -20 38 -38 30 -38 10 Z", "orange3")
    a.path("M -24 8 C -24 -6 -12 -10 0 -10 C 12 -10 24 -6 24 8 C 24 22 12 26 0 26 "
           "C -12 26 -24 22 -24 8 Z", "cream")
    for d in ["M -18 0 C -10 6 -6 -2 2 4 C 8 8 12 2 18 6", "M -18 14 C -10 8 -4 18 4 12 C 10 8 14 16 20 12"]:
        a.curve(d, w=1.4)
    seed = pumpkin_seed()
    for x, y, r in [(-12, 6, 20), (0, 0, -10), (12, 8, 30), (-4, 16, 80), (10, 18, -40), (-14, 18, 60)]:
        a.add(seed, dx=x, dy=y, s=0.13, rot=r)
    return a


def pumpkin_open():
    """Pumpkin with its lid off and seeds scooped out (carving step)."""
    a = Art()
    sil = Art()
    for x, y, rx, ry in [(-28, 14, 20, 28), (28, 14, 20, 28), (-15, 13, 22, 31), (15, 13, 22, 31), (0, 12, 19, 33)]:
        sil.ellipse(x, y, rx, ry, "orange")
    a.merge(sil)
    a.path("M -22 -12 L -8 -20 L 8 -20 L 22 -12 C 12 -6 -12 -6 -22 -12 Z", "orange3")
    a.ellipse(0, -14, 20, 5, "cream")
    lid = Art()
    lid.path("M -14 6 C -14 -4 14 -4 14 6 Z", "orange")
    lid.path("M -3 -2 L -3 -12 L 4 -12 L 3 -2 Z", "stem")
    a.add(lid, dx=34, dy=-34, rot=25, s=0.9)
    sp = spoon()
    a.add(sp, dx=-30, dy=-30, s=0.5, rot=-30)
    seed = pumpkin_seed()
    for x, y, r in [(-40, 40, 20), (-30, 44, 70), (40, 42, -30), (32, 46, 10)]:
        a.add(seed, dx=x, dy=y, s=0.12, rot=r)
    return a


def pumpkin_face(fill="dark", glow=False):
    """Pumpkin with a jack-o'-lantern face (for sequencing pictures)."""
    f = "yellow" if glow else fill
    a = pumpkin(leaf=False, vine=False)
    a.add(eye("triangle", f), dx=-15, dy=-2, s=0.2)
    a.add(eye("triangle", f), dx=15, dy=-2, s=0.2)
    a.add(nose("triangle", f), dx=0, dy=12, s=0.12)
    a.add(mouth("grin", f), dx=0, dy=27, s=0.36)
    if glow:
        for ang in range(0, 360, 30):
            r1, r2 = 50, 56
            x1, y1 = r1 * math.cos(math.radians(ang)), r1 * math.sin(math.radians(ang)) + 4
            x2, y2 = r2 * math.cos(math.radians(ang)), r2 * math.sin(math.radians(ang)) + 4
            a.line(x1, y1, x2, y2, stroke="gold", w=2)
    return a


def pumpkin_drawn_face():
    a = pumpkin(leaf=False, vine=False)
    for p, dx, dy, s in [(eye("triangle", "none"), -15, -2, 0.2), (eye("triangle", "none"), 15, -2, 0.2),
                         (nose("triangle", "none"), 0, 12, 0.12), (mouth("grin", "none"), 0, 27, 0.36)]:
        a.add(p, dx=dx, dy=dy, s=s)
    mk = Art()
    mk.rect(-5, -30, 10, 50, 2, "purple")
    mk.poly([(-5, 20), (5, 20), (0, 32)], "tan")
    a.add(mk, dx=40, dy=10, rot=30, s=0.7)
    return a


def pumpkin_patch_pick():
    a = Art()
    a.path("M -48 40 C -30 32 30 32 48 40 L 48 46 L -48 46 Z", "leaf")
    a.add(pumpkin(), dx=0, dy=-2, s=0.78)
    a.curve("M -46 38 C -40 26 -30 30 -26 24", w=1.8)
    return a


def fall_tree():
    a = Art()
    a.path("M -12 46 C -8 30 -8 10 -6 -6 C -16 -16 -30 -20 -42 -30 L -38 -34 C -26 -26 -16 -22 -6 -16 "
           "C -6 -28 -10 -38 -14 -46 L -8 -48 C -2 -38 0 -28 2 -18 C 10 -26 22 -34 36 -40 L 40 -36 "
           "C 26 -28 12 -18 6 -8 C 18 -10 30 -14 42 -20 L 44 -16 C 30 -8 16 -2 8 2 C 8 16 8 32 12 46 Z", "stem")
    a.path("M -48 46 C -30 40 30 40 48 46 Z", "leaf")
    return a


def vine_strip(n=6):
    a = Art()
    a.path("M -50 -3 C -40 -9 -30 3 -20 -3 C -10 -9 0 3 10 -3 C 20 -9 30 3 40 -3 C 44 -5 48 -5 50 -3 "
           "L 50 3 C 48 1 44 1 40 3 C 30 9 20 -3 10 3 C 0 9 -10 -3 -20 3 C -30 9 -40 -3 -50 3 Z", "leaf2")
    for i, x in enumerate((-36, -6, 24)):
        lf = Art().path("M 0 0 C -6 -4 -8 -12 -2 -16 C 0 -14 2 -14 4 -16 C 10 -12 6 -4 0 0 Z", "leaf")
        a.add(lf, dx=x, dy=-3, rot=-20 if i % 2 else 20)
    return a


def emotion_face(kind):
    a = Art()
    if kind == "happy":
        a.add(eye("happy"), dx=-18, dy=-12, s=0.24)
        a.add(eye("happy"), dx=18, dy=-12, s=0.24, flip=True)
        a.add(mouth("smile"), dx=0, dy=18, s=0.55)
    elif kind == "sad":
        a.add(eye("round"), dx=-18, dy=-10, s=0.2)
        a.add(eye("round"), dx=18, dy=-10, s=0.2, flip=True)
        a.add(brow(), dx=-18, dy=-26, s=0.26, rot=-18)
        a.add(brow(), dx=18, dy=-26, s=0.26, rot=18)
        a.add(mouth("frown"), dx=0, dy=20, s=0.5)
    elif kind == "mad":
        a.add(eye("angry"), dx=-18, dy=-10, s=0.24)
        a.add(eye("angry"), dx=18, dy=-10, s=0.24, flip=True)
        a.add(mouth("frown"), dx=0, dy=22, s=0.5)
    elif kind == "surprised":
        a.add(eye("round"), dx=-18, dy=-10, s=0.22)
        a.add(eye("round"), dx=18, dy=-10, s=0.22, flip=True)
        a.add(mouth("o"), dx=0, dy=22, s=0.6)
    elif kind == "sleepy":
        a.add(eye("sleepy"), dx=-18, dy=-10, s=0.24)
        a.add(eye("sleepy"), dx=18, dy=-10, s=0.24, flip=True)
        a.add(mouth("surprised"), dx=0, dy=20, s=0.6)
    elif kind == "silly":
        a.add(eye("googly"), dx=-18, dy=-10, s=0.24)
        a.add(eye("spiral"), dx=18, dy=-10, s=0.24)
        a.add(mouth("tongue"), dx=0, dy=20, s=0.55)
    elif kind == "scared":
        a.add(eye("round"), dx=-18, dy=-10, s=0.24)
        a.add(eye("round"), dx=18, dy=-10, s=0.24, flip=True)
        a.add(mouth("wavy"), dx=0, dy=22, s=0.5)
    elif kind == "proud":
        a.add(eye("star"), dx=-18, dy=-10, s=0.24)
        a.add(eye("star"), dx=18, dy=-10, s=0.24)
        a.add(mouth("grin"), dx=0, dy=20, s=0.5)
    return a


EMOTIONS = ["happy", "sad", "mad", "surprised", "sleepy", "silly"]


def mask_pumpkin():
    a = Art()
    sil = Art()
    for x, y, rx, ry in [(-30, 4, 22, 26), (30, 4, 22, 26), (-14, 2, 24, 30), (14, 2, 24, 30), (0, 2, 20, 32)]:
        sil.ellipse(x, y, rx, ry, "orange")
    sil.path("M -5 -26 C -6 -34 -4 -40 -1 -44 L 6 -42 C 4 -36 4 -32 6 -26 Z", "stem")
    a.merge(sil)
    a.path("M 5 -32 C 11 -42 24 -44 32 -38 C 26 -30 15 -27 5 -32 Z", "leaf")
    a.curve("M -10 26 C -6 20 -5 14 -5 10", w=T)
    a.curve("M 10 26 C 6 20 5 14 5 10", w=T)
    a.add(mouth("grin", "none"), dx=0, dy=16, s=0.38)
    return a


def mask_cat():
    a = Art()
    a.path("M -46 10 C -48 -14 -44 -30 -40 -46 C -28 -38 -20 -30 -14 -24 C -6 -27 6 -27 14 -24 "
           "C 20 -30 28 -38 40 -46 C 44 -30 48 -14 46 10 C 42 30 22 40 0 40 C -22 40 -42 30 -46 10 Z", "dark")
    a.path("M -38 -36 C -32 -32 -26 -28 -22 -24 L -36 -16 Z", "pink")
    a.path("M 38 -36 C 32 -32 26 -28 22 -24 L 36 -16 Z", "pink")
    a.path("M -6 14 C -2 12 2 12 6 14 C 4 18 2 20 0 20 C -2 20 -4 18 -6 14 Z", "pink")
    a.add(mouth("cat", "none"), dx=0, dy=26, s=0.4)
    for sx in (-1, 1):
        for y0, y1 in [(18, 12), (22, 24)]:
            a.line(sx * 12, y0, sx * 40, y1, stroke="lgray", w=1.4)
    return a


def mask_owl():
    a = Art()
    a.path("M -46 6 C -48 -20 -44 -34 -40 -46 C -30 -36 -22 -30 -14 -28 C -6 -30 6 -30 14 -28 "
           "C 22 -30 30 -36 40 -46 C 44 -34 48 -20 46 6 C 42 30 22 42 0 42 C -22 42 -42 30 -46 6 Z", "brown")
    a.circle(-20, -4, 20, "yellow")
    a.circle(20, -4, 20, "yellow")
    a.add(beak(), dx=0, dy=20, s=0.3)
    for x, y in [(-22, 30), (-8, 34), (8, 34), (22, 30)]:
        a.curve(f"M {x - 5} {y - 2} C {x - 2} {y + 2} {x + 2} {y + 2} {x + 5} {y - 2}", w=1.2)
    return a


def mask_bat():
    a = Art()
    a.path("M -48 -10 C -40 -20 -30 -22 -22 -18 L -18 -40 L -8 -24 C -4 -25 4 -25 8 -24 L 18 -40 L 22 -18 "
           "C 30 -22 40 -20 48 -10 C 42 -4 42 4 46 10 C 36 8 30 12 26 18 C 20 28 10 32 0 32 "
           "C -10 32 -20 28 -26 18 C -30 12 -36 8 -46 10 C -42 4 -42 -4 -48 -10 Z", "purple2")
    a.poly([(-6, 18), (-3, 26), (0, 18)], "paper", w=1)
    a.poly([(6, 18), (3, 26), (0, 18)], "paper", w=1)
    return a


def crayon(fill="orange"):
    a = Art()
    a.path("M -30 -10 L 26 -10 L 26 10 L -30 10 C -34 6 -34 -6 -30 -10 Z", fill)
    a.path("M 26 -10 L 46 -3 C 48 -2 48 2 46 3 L 26 10 Z", fill)
    a.line(-18, -10, -18, 10, w=1.4)
    a.line(14, -10, 14, 10, w=1.4)
    return a


def puppet_arm():
    a = Art()
    a.rect(-46, -7, 70, 14, 7, "leaf2")
    lf = Art().path("M 0 0 C 8 -14 26 -16 34 -8 C 28 2 14 8 0 0 Z", "leaf")
    a.add(lf, dx=18, dy=0)
    return a


def shoe():
    a = Art()
    a.path("M -40 10 C -42 -8 -26 -14 -10 -12 C 10 -10 28 -16 40 -4 C 46 4 42 14 30 14 L -34 14 C -38 14 -40 12 -40 10 Z", "stem")
    return a
