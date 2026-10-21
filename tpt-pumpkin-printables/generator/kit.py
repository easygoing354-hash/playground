"""Document wrapper + reusable page recipes used by the product definitions."""
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics

import art as A
from engine import Art, PDFRenderer, bbox
import layout as L
from layout import PAGE_W, PAGE_H, M

TEMPLATE_S = 520          # size (pt) of the 100-unit box for full-page pumpkin templates
K = TEMPLATE_S / 100.0    # points per art unit at template scale


class Doc:
    def __init__(self, path, prod):
        self.c = c = rl_canvas.Canvas(path, pagesize=letter)
        c.setTitle(f"{prod['title']} | {L.STORE_NAME}")
        c.setAuthor(L.STORE_NAME)
        c.setSubject("Fall / Halloween pumpkin cut, colour & glue printable")
        c.setKeywords("pumpkin, fall, halloween, craft, cut and paste, kindergarten, first grade, TpT")
        c.setCreator(L.STORE_NAME)
        self.R = PDFRenderer(c, color=False)
        self.Rc = PDFRenderer(c, color=True)
        self.prod = prod
        self.started = False
        self.count = 0

    def page(self):
        if self.started:
            L.footer(self.c)
            self.c.showPage()
        self.started = True
        self.count += 1
        L.ink(self.c)
        return self.c

    def save(self):
        L.footer(self.c)
        self.c.showPage()
        self.c.save()


# ---------------------------------------------------------------------------
# art placement helpers
# ---------------------------------------------------------------------------

def tf(art, flip=False, rot=0, s=1.0):
    return Art().add(art, flip=flip, rot=rot, s=s)


def draw_centered(R, art, cx, cy, size):
    """Draw so the art's bounding-box centre lands on (cx, cy)."""
    x0, y0, x1, y1 = bbox(art)
    k = size / 100.0
    R.draw(art, cx - (x0 + x1) / 2 * k, cy + (y0 + y1) / 2 * k, size)


def draw_fit(R, art, cx, cy, max_w, max_h):
    """Scale art to fit a box, centred. Returns the size used."""
    x0, y0, x1, y1 = bbox(art)
    k = min(max_w / (x1 - x0), max_h / (y1 - y0))
    size = 100 * k
    R.draw(art, cx - (x0 + x1) / 2 * k, cy + (y0 + y1) / 2 * k, size)
    return size


def assembled(parts, behind=(), base=None):
    """Compose a craft: parts = [(art, dx, dy, size_units, flip, rot), ...] on a pumpkin."""
    a = Art()
    for p in behind:
        art, dx, dy, su, flip, rot = (list(p) + [False, 0])[:6]
        a.add(art, dx=dx, dy=dy, s=su / 100.0, flip=flip, rot=rot)
    a.add(base if base is not None else A.pumpkin())
    for p in parts:
        art, dx, dy, su, flip, rot = (list(p) + [False, 0])[:6]
        a.add(art, dx=dx, dy=dy, s=su / 100.0, flip=flip, rot=rot)
    return a


def example_of(art):
    """Teacher-page example callback for a finished-craft Art."""
    def ex(c, R, x, y, size):
        draw_fit(R, art, x, y, size, size)
    return ex


def example_page(fn):
    """Teacher-page example that shows a mini colour version of a student page."""
    def ex(c, R, x, y, size):
        s = size * 1.05 / PAGE_H
        w, h = PAGE_W * s, PAGE_H * s
        c.saveState()
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.setFillColorRGB(1, 1, 1)
        c.rect(x - w / 2, y - h / 2, w, h, stroke=1, fill=1)
        c.translate(x - w / 2, y - h / 2)
        c.scale(s, s)
        fn(c, R)
        c.restoreState()
    return ex


# ---------------------------------------------------------------------------
# page recipes
# ---------------------------------------------------------------------------

def _dry_header_y(title, sub, spooky=False):
    import io
    dc = rl_canvas.Canvas(io.BytesIO(), pagesize=letter)
    log = list(L.PAGE_LOG)
    y = L.header(dc, PDFRenderer(dc), title, sub, spooky=spooky)
    L.PAGE_LOG[:] = log
    return y


def _plan(items, y_top, gap):
    """Shelf-pack items into pages. Returns list of pages; page = list of rows (row_items, row_h)."""
    right, bottom = PAGE_W - M, 40
    pages, i = [], 0
    while i < len(items):
        y, x, row_h, cur, rows = y_top, M, 0, [], []
        while i < len(items):
            it = items[i]
            if x + it["w"] > right and cur:
                rows.append((cur, row_h))
                y -= row_h + gap
                x, row_h, cur = M, 0, []
                continue
            if y - it["h"] < bottom:
                break
            cur.append((it, x, y))
            x += it["w"] + gap
            row_h = max(row_h, it["h"])
            i += 1
        if cur:
            rows.append((cur, row_h))
        if not rows:
            raise RuntimeError("piece too large for page")
        pages.append(rows)
    return pages


def pack_pages(doc, title, sub, pieces, gap=18, spooky=False, double=True):
    """Shelf-pack cut-out pieces over as many pages as needed.

    pieces: list of (art, size_pt) or (art, size_pt, flip, rot).
    If everything fits on one page with room for a second copy, two sets are printed."""
    items = []
    for p in pieces:
        art, size = p[0], p[1]
        flip = p[2] if len(p) > 2 else False
        rot = p[3] if len(p) > 3 else 0
        if flip or rot:
            art = tf(art, flip, rot)
        x0, y0, x1, y1 = bbox(art)
        k = size / 100.0
        items.append(dict(art=art, size=size, w=(x1 - x0) * k, h=(y1 - y0) * k,
                          bx=(x0 + x1) / 2 * k, by=(y0 + y1) / 2 * k))
    items.sort(key=lambda d: -d["h"])
    y_top = _dry_header_y(title, sub, spooky)
    pages = _plan(items, y_top, gap)
    if double and len(pages) == 1:
        two = _plan(items + items, y_top, gap)
        if len(two) == 1:
            pages = two
            sub = (sub + " " if sub else "") + "(2 sets per page)"
    for rows in pages:
        c = doc.page()
        L.header(c, doc.R, title, sub, spooky=spooky)
        for cur, rh in rows:
            used = sum(it["w"] for it, _, _ in cur) + gap * (len(cur) - 1)
            shift = (PAGE_W - 2 * M - used) / 2
            for it, x, yy in cur:
                cx = x + shift + it["w"] / 2
                cy = yy - rh / 2
                doc.R.draw(it["art"], cx - it["bx"], cy + it["by"], it["size"])


def template_page(doc, title="My Pumpkin", sub=None, base=None, size=TEMPLATE_S):
    c = doc.page()
    y = L.header(c, doc.R, title, sub, deco=False)
    art = base if base is not None else A.pumpkin(ribs=False)
    draw_fit(doc.R, art, PAGE_W / 2, (y + 30) / 2, PAGE_W - 2 * M, y - 50)


def writing_page(doc, title, prompt, starter=None, lines=3, box_h=300):
    c = doc.page()
    y = L.header(c, doc.R, title, None)
    L.text(c, prompt, PAGE_W / 2, y - 6, 16, "BodyB")
    y -= 24
    c.saveState()
    L.ink(c)
    c.setLineWidth(1.5)
    c.roundRect(M, y - box_h, PAGE_W - 2 * M, box_h, 14, stroke=1, fill=0)
    c.restoreState()
    L.text(c, "draw", PAGE_W - M - 26, y - box_h + 10, 10, "Body", color=(0.6, 0.6, 0.6))
    y -= box_h + 26
    if starter:
        L.text(c, starter, M, y, 18, "Body", "left")
        y -= 16
    L.primary_lines(c, M, y, PAGE_W - 2 * M, n=lines, gap=60)


def card_grid(doc, title, sub, cards, cols, rows, labels=None, art_frac=0.72, label_size=16,
              label_font="BodyB", icon=True):
    """Dashed cut-apart cards. cards = list of Art (or None) ; labels = list of str."""
    c = doc.page()
    y = L.header(c, doc.R, title, sub)
    x0, w, h = M, PAGE_W - 2 * M, y - 40
    cw, ch = w / cols, h / rows
    for i, art in enumerate(cards):
        cx = x0 + (i % cols + 0.5) * cw
        cy = y - (i // cols + 0.5) * ch
        L.cut_box(c, doc.R, cx - cw / 2 + 4, cy - ch / 2 + 4, cw - 8, ch - 8, r=10, icon=(icon and i == 0))
        lab = labels[i] if labels else None
        if art is not None:
            ah = (ch - 8) * art_frac - (label_size + 4 if lab else 0)
            draw_fit(doc.R, art, cx, cy + (label_size / 2 + 4 if lab else 0), (cw - 8) * 0.82, ah)
        if lab:
            yy = cy - ch / 2 + 14 if art is not None else cy - label_size / 3
            L.fit_text(c, lab, cx, yy, cw - 20, label_size if art is not None else label_size * 1.8, label_font)


def outline_text(c, s, x, y, size, font="Head", lw=1.6, align="center"):
    c.saveState()
    c.setFont(font, size)
    c.setFillColorRGB(1, 1, 1)
    L.ink(c)
    c.setFillColorRGB(1, 1, 1)
    c.setLineWidth(lw)
    t = c.beginText()
    t.setTextRenderMode(2)
    t.setFont(font, size)
    w = pdfmetrics.stringWidth(s, font, size)
    xx = x - w / 2 if align == "center" else x
    t.setTextOrigin(xx, y)
    t.textOut(s)
    c.drawText(t)
    c.restoreState()


def big_label(c, s, x, y, size=28, font="Head"):
    L.text(c, s, x, y - size * 0.35, size, font)
