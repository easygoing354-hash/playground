"""Page building blocks shared by all 50 printables."""
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

import art as A
from engine import Art, PDFRenderer, PALETTE, _rgb

# ---------------------------------------------------------------------------
# Brand settings - change STORE_NAME to your TpT store name and rebuild.
# ---------------------------------------------------------------------------
STORE_NAME = "Pumpkin Patch Pals"
YEAR = "2026"
PAGE_W, PAGE_H = letter
M = 36  # page margin

FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "fonts")
pdfmetrics.registerFont(TTFont("Head", os.path.join(FONT_DIR, "Sniglet-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("Head2", os.path.join(FONT_DIR, "Sniglet-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Body", os.path.join(FONT_DIR, "Andika-Regular.ttf")))
pdfmetrics.registerFont(TTFont("BodyB", os.path.join(FONT_DIR, "Andika-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Spooky", os.path.join(FONT_DIR, "Creepster-Regular.ttf")))

INK = _rgb(PALETTE["ink"])
ORANGE = _rgb(PALETTE["orange"])
PURPLE = _rgb(PALETTE["purple"])
GREEN = _rgb(PALETTE["leaf2"])
SOFT = _rgb("#fff3e3")


def ink(c):
    c.setFillColorRGB(*INK)
    c.setStrokeColorRGB(*INK)


def text(c, s, x, y, size=14, font="Body", align="center", color=None):
    c.setFont(font, size)
    c.setFillColorRGB(*(color or INK))
    if align == "center":
        c.drawCentredString(x, y, s)
    elif align == "right":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)


def fit_text(c, s, x, y, max_w, size=14, font="Body", align="center", color=None, min_size=7):
    while size > min_size and pdfmetrics.stringWidth(s, font, size) > max_w:
        size -= 0.5
    text(c, s, x, y, size, font, align, color)
    return size


def wrap(s, font, size, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(c, s, x, y, max_w, size=11, font="Body", leading=None, color=None):
    """Draw wrapped paragraph top-down starting at baseline y. Returns next y."""
    leading = leading or size * 1.35
    for ln in wrap(s, font, size, max_w):
        text(c, ln, x, y, size, font, "left", color)
        y -= leading
    return y


# ---------------------------------------------------------------------------
# decorations
# ---------------------------------------------------------------------------

def scissors():
    a = Art()
    a.circle(-30, -18, 12, "paper", w=3)
    a.circle(-30, 18, 12, "paper", w=3)
    a.path("M -20 -12 L 40 10 L 36 14 L -18 -4 Z", "paper", w=2)
    a.path("M -20 12 L 40 -10 L 36 -14 L -18 4 Z", "paper", w=2)
    a.circle(0, 0, 3, "ink", stroke="none")
    return a


def cut_box(c, R, x, y, w, h, r=10, icon=True, dash=(6, 4), lw=1.3):
    """Dashed cutting line (rounded rect) with a scissors icon. (x, y) = bottom-left."""
    c.saveState()
    ink(c)
    c.setLineWidth(lw)
    c.setDash(*dash)
    c.roundRect(x, y, w, h, r, stroke=1, fill=0)
    c.restoreState()
    if icon:
        c.saveState()
        c.setFillColorRGB(1, 1, 1)
        c.rect(x + 10, y + h - 7, 20, 14, stroke=0, fill=1)
        c.restoreState()
        R.draw(scissors(), x + 20, y + h, 18)


def cut_line(c, R, x1, y1, x2, y2, icon=True):
    c.saveState()
    ink(c)
    c.setLineWidth(1.3)
    c.setDash(6, 4)
    c.line(x1, y1, x2, y2)
    c.restoreState()
    if icon:
        R.draw(scissors(), x1 + 12, y1, 18)


def glue_box(c, x, y, w, h, label="glue"):
    c.saveState()
    c.setStrokeColorRGB(0.55, 0.55, 0.55)
    c.setLineWidth(1)
    c.setDash(2, 3)
    c.roundRect(x, y, w, h, 6, stroke=1, fill=0)
    c.restoreState()
    if label:
        text(c, label, x + w / 2, y + h / 2 - 4, 10, "Body", color=(0.6, 0.6, 0.6))


def primary_lines(c, x, y, w, n=4, gap=54, head=0.5):
    """Primary ruled writing lines. y = top line of first row. gap = row pitch."""
    lh = gap * 0.62
    for i in range(n):
        top = y - i * gap
        base = top - lh
        c.saveState()
        ink(c)
        c.setLineWidth(1.1)
        c.line(x, top, x + w, top)
        c.line(x, base, x + w, base)
        c.setDash(4, 4)
        c.setLineWidth(0.8)
        c.setStrokeColorRGB(0.45, 0.45, 0.45)
        c.line(x, top - lh / 2, x + w, top - lh / 2)
        c.restoreState()


def simple_lines(c, x, y, w, n, gap=26):
    c.saveState()
    ink(c)
    c.setLineWidth(1)
    for i in range(n):
        c.line(x, y - i * gap, x + w, y - i * gap)
    c.restoreState()


def name_line(c, y=None, date=False):
    y = PAGE_H - 30 if y is None else y
    text(c, "Name:", M, y, 13, "BodyB", "left")
    c.saveState()
    ink(c)
    c.setLineWidth(1)
    c.line(M + 44, y - 2, M + 250, y - 2)
    if date:
        text(c, "Date:", PAGE_W - M - 160, y, 13, "BodyB", "left")
        c.line(PAGE_W - M - 120, y - 2, PAGE_W - M, y - 2)
    c.restoreState()


PAGE_LOG = []   # titles of student pages, collected during a dry-run build


def header(c, R, title, subtitle=None, name=True, spooky=False, deco=True, title_size=30):
    """Student page header. Returns y below header."""
    PAGE_LOG.append(title)
    y = PAGE_H - 30
    if name:
        name_line(c, y)
        y -= 40
    else:
        y -= 12
    font = "Spooky" if spooky else "Head"
    s = fit_text(c, title, PAGE_W / 2, y - title_size * 0.7, PAGE_W - 2 * M - 110, title_size, font)
    if deco:
        R.draw(A.mini_pumpkin(), M + 22, y - s * 0.4, 38)
        R.draw(A.maple_leaf(), PAGE_W - M - 22, y - s * 0.4, 38, rot=15)
    y -= s * 0.7 + 14
    if subtitle:
        for ln in wrap(subtitle, "Body", 13, PAGE_W - 2 * M - 40):
            text(c, ln, PAGE_W / 2, y - 6, 13, "Body")
            y -= 17
        y -= 4
    return y - 6


def footer(c, page_label=None):
    s = f"© {YEAR} {STORE_NAME}  •  Licensed for single-classroom use"
    text(c, s, PAGE_W / 2, 16, 7.5, "Body", color=(0.45, 0.45, 0.45))


def page_border(c, color=ORANGE, inset=14, r=18, lw=2.2):
    c.saveState()
    c.setStrokeColorRGB(*color)
    c.setLineWidth(lw)
    c.roundRect(inset, inset + 10, PAGE_W - 2 * inset, PAGE_H - 2 * inset - 10, r, stroke=1, fill=0)
    c.restoreState()


def place_grid(c, R, pieces, x0, y_top, w, h, cols, rows=None, size=None, labels=None,
               box=False, label_font="BodyB", label_size=12, pad=6):
    """Lay pieces (list of Art or (Art, kwargs)) in a grid inside rect (x0, y_top-h, w, h)."""
    n = len(pieces)
    rows = rows or -(-n // cols)
    cw, ch = w / cols, h / rows
    size = size or min(cw, ch) * 0.86
    for i, p in enumerate(pieces):
        cx = x0 + (i % cols + 0.5) * cw
        cy = y_top - (i // cols + 0.5) * ch
        kw = {}
        if isinstance(p, tuple):
            p, kw = p
        if box:
            cut_box(c, R, cx - cw / 2 + pad, cy - ch / 2 + pad, cw - 2 * pad, ch - 2 * pad, r=8,
                    icon=(i == 0))
        lab = labels[i] if labels else None
        dy = 8 if lab else 0
        if p is not None:
            R.draw(p, cx, cy + dy, kw.pop("size", size), **kw)
        if lab:
            fit_text(c, lab, cx, cy - ch / 2 + pad + 8, cw - 2 * pad - 6, label_size, label_font)
    return cw, ch


# ---------------------------------------------------------------------------
# teacher page + terms page (one of each in every product)
# ---------------------------------------------------------------------------

def teacher_page(c, prod, example):
    """Colourful instruction page with a finished example."""
    Rc = PDFRenderer(c, color=True)
    c.setFillColorRGB(*SOFT)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    page_border(c)
    # title banner
    c.setFillColorRGB(*ORANGE)
    c.roundRect(M, PAGE_H - 112, PAGE_W - 2 * M, 72, 16, stroke=0, fill=1)
    fit_text(c, prod["title"], PAGE_W / 2, PAGE_H - 74, PAGE_W - 2 * M - 120, 28, "Head", color=(1, 1, 1))
    text(c, f"#{prod['num']:02d}  •  {prod.get('grades', 'PreK - 2')}  •  Teacher Directions",
         PAGE_W / 2, PAGE_H - 98, 12, "Body", color=(1, 1, 1))
    Rc.draw(A.mini_pumpkin(), M + 34, PAGE_H - 76, 50)
    Rc.draw(A.maple_leaf(), PAGE_W - M - 34, PAGE_H - 76, 48, rot=-15)

    # example panel (right)
    px, pw, ptop, ph = PAGE_W - M - 262, 262, PAGE_H - 128, 330
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(*ORANGE)
    c.setLineWidth(1.5)
    c.roundRect(px, ptop - ph, pw, ph, 14, stroke=1, fill=1)
    text(c, "Finished example", px + pw / 2, ptop - 22, 14, "Head", color=PURPLE)
    example(c, Rc, px + pw / 2, ptop - ph / 2 - 8, 220)

    # left column text
    x, y, colw = M + 6, PAGE_H - 146, PAGE_W - 2 * M - 270
    text(c, "Skills", x, y, 15, "Head", "left", GREEN)
    y -= 18
    for s in prod["skills"]:
        y = para(c, "• " + s, x, y, colw, 11)
    y -= 6
    text(c, "You will need", x, y, 15, "Head", "left", GREEN)
    y -= 18
    for s in prod.get("materials", ["Crayons or markers", "Scissors", "Glue stick"]):
        y = para(c, "• " + s, x, y, colw, 11)
    y -= 6
    text(c, "Prep", x, y, 15, "Head", "left", GREEN)
    y -= 18
    y = para(c, prod.get("prep", "Print the student pages on white paper or cardstock. "
                                 "Print pumpkin templates on orange paper for a no-colour option."), x, y, colw, 11)

    # steps (full width)
    y = min(y, ptop - ph) - 18
    text(c, "Directions", M + 6, y, 16, "Head", "left", GREEN)
    y -= 21
    for i, s in enumerate(prod["steps"], 1):
        c.setFillColorRGB(*ORANGE)
        c.circle(M + 16, y + 4, 9, stroke=0, fill=1)
        text(c, str(i), M + 16, y, 11, "BodyB", color=(1, 1, 1))
        y = para(c, s, M + 32, y, PAGE_W - 2 * M - 40, 12.5) - 4
    if prod.get("tip"):
        y -= 6
        tip_lines = wrap(prod["tip"], "Body", 11, PAGE_W - 2 * M - 70)
        bh = 26 + 14 * len(tip_lines)
        c.setFillColorRGB(0.93, 0.89, 0.98)
        c.roundRect(M + 6, y - bh + 14, PAGE_W - 2 * M - 12, bh, 10, stroke=0, fill=1)
        text(c, "Teacher tip", M + 20, y - 2, 13, "Head", "left", PURPLE)
        yy = y - 18
        for ln in tip_lines:
            text(c, ln, M + 20, yy, 11, "Body", "left")
            yy -= 14
        y = yy
    contents = prod.get("contents")
    if contents:
        y -= 14
        items = []
        for t in contents:
            if items and items[-1][0] == t:
                items[-1][1] += 1
            else:
                items.append([t, 1])
        labels = [f"{t} ({n} pages)" if n > 1 else t for t, n in items]
        lines = wrap("  \u2022  ".join(labels), "Body", 11, PAGE_W - 2 * M - 40)
        bh = 30 + 14 * len(lines)
        by = max(y - bh, 40)
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColorRGB(*ORANGE)
        c.setLineWidth(1.2)
        c.roundRect(M + 6, by, PAGE_W - 2 * M - 12, bh, 10, stroke=1, fill=1)
        text(c, f"What's inside: {len(contents)} student pages", M + 20, by + bh - 18, 13, "Head", "left", ORANGE)
        yy = by + bh - 34
        for ln in lines:
            text(c, ln, M + 20, yy, 11, "Body", "left")
            yy -= 14


def terms_page(c, prod=None):
    Rc = PDFRenderer(c, color=True)
    page_border(c, PURPLE)
    text(c, "Thank you!", PAGE_W / 2, PAGE_H - 84, 40, "Head", color=ORANGE)
    Rc.draw(A.pumpkin(), PAGE_W / 2 - 170, PAGE_H - 74, 60)
    Rc.draw(A.ghost(), PAGE_W / 2 + 170, PAGE_H - 74, 56)
    y = PAGE_H - 120
    y = para(c, f"Thank you for choosing {STORE_NAME}! I hope your students have a "
                "fantastic fall. If you enjoy this resource, please leave a review on TpT. "
                "Reviews help other teachers find it, and you earn TpT credits toward future purchases.",
             M + 20, y, PAGE_W - 2 * M - 40, 12)
    y -= 10
    text(c, "Terms of Use", M + 20, y, 18, "Head", "left", PURPLE)
    y -= 22
    rules = [
        ("You MAY", [
            "use this resource with your own students and in your own classroom, and send copies home with them.",
            "print as many copies as you need for your own class, year after year.",
            "share the TpT product link with colleagues so they can buy their own copy.",
        ]),
        ("You MAY NOT", [
            "share, email or give the files to other teachers, a whole school or a district. "
            "Please buy additional licenses at a discount on TpT.",
            "upload these files to a public website, a shared drive, a blog or a district server.",
            "claim this work as your own, sell it, or use the art or pages in your own products.",
        ]),
    ]
    for head, items in rules:
        text(c, head, M + 20, y, 13, "BodyB", "left", GREEN if head == "You MAY" else (0.8, 0.2, 0.2))
        y -= 17
        for s in items:
            y = para(c, "• " + s, M + 32, y, PAGE_W - 2 * M - 60, 11) - 2
        y -= 6
    text(c, "Credits", M + 20, y, 18, "Head", "left", PURPLE)
    y -= 22
    credits = [
        f"All illustrations and page designs are original artwork by {STORE_NAME}. "
        f"© {YEAR} {STORE_NAME}. All rights reserved.",
        "Fonts: Sniglet by Haley Fiege; Andika by SIL International; Creepster by Font Diner. "
        "All are used under the SIL Open Font License 1.1, which allows commercial use.",
        "Copyright law protects this product. Copying it for more than one teacher or classroom, "
        "or posting it online, violates the Digital Millennium Copyright Act (DMCA).",
    ]
    for s in credits:
        y = para(c, s, M + 20, y, PAGE_W - 2 * M - 40, 10.5) - 4
    y -= 10
    c.setFillColorRGB(*SOFT)
    c.roundRect(M + 20, y - 60, PAGE_W - 2 * M - 40, 64, 12, stroke=0, fill=1)
    text(c, "Want more fall fun?", PAGE_W / 2, y - 20, 15, "Head", color=ORANGE)
    text(c, "Follow my store on TpT to hear about new resources and freebies!", PAGE_W / 2, y - 40, 11.5, "Body")
