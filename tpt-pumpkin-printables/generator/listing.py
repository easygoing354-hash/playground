"""Build the TpT listing kit: Start Here guide, thumbnails, preview PDF and upload zip.

    python3 build.py && python3 export_web.py && python3 listing.py
"""
import glob
import io
import os
import shutil
import subprocess
import tempfile
import zipfile

from PIL import Image, ImageDraw, ImageFilter
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import letter

import art as A
import kit
import layout as L
from layout import PAGE_W, PAGE_H, M
from engine import PDFRenderer, _rgb
import build as B

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDFS = os.path.join(ROOT, "pdfs")
OUT = os.path.join(ROOT, "tpt-listing")
APP = os.path.abspath(os.path.join(ROOT, "..", "pumpkin-patch-pals"))
PRODUCTS = B.PRODUCTS
BY_NUM = {p["num"]: p for p in PRODUCTS}
STUDENT_PAGES = sum(len(PdfReader(f).pages) - 2 for f in glob.glob(os.path.join(PDFS, "*.pdf")))

CATEGORIES = [
    ("Pumpkin Face & Character Crafts", [1, 2, 3, 4, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]),
    ("Math", [6, 9, 28, 29, 30, 35, 36, 37, 38, 39, 40, 41]),
    ("Literacy & Writing", [27, 31, 32, 33, 34, 42, 43, 44]),
    ("Science", [23, 24, 25]),
    ("Social-Emotional", [5]),
    ("Fall Crafts & Decor", [26, 45, 46, 47, 48, 49, 50]),
]
STANDARDS = [
    ("K.CC.B.4 / K.CC.B.5  Count to tell how many", "#9, 28, 30"),
    ("K.CC.A.2 / K.CC.A.3  Count forward, write numbers", "#29"),
    ("K.OA.A.1 / K.OA.A.2  Add and subtract within 10", "#40, 41"),
    ("K.G.A.2 / K.G.B.5 / K.G.B.6  Name, build and compose shapes (2D and 3D)", "#6, 39, 48"),
    ("K.MD.A.2 / 1.MD.A.2  Compare sizes, measure lengths", "#36, 37"),
    ("K.MD.B.3 / 1.MD.C.4  Sort, count and graph data", "#36, 38, 39"),
    ("Pattern readiness (algebraic thinking)", "#35"),
    ("RF.K.1.d  Upper- and lowercase letters", "#27, 31, 47"),
    ("RF.K.2.a  Recognize rhyming words", "#33"),
    ("RF.K.2.d / RF.K.3.a  Initial sounds, letter-sound match", "#32, 34"),
    ("RF.K.3.c  Read common sight words", "#44"),
    ("W.K.2 / W.1.7  Informative & how-to writing", "#23, 24, 43"),
    ("W.K.3 / SL.K.5  Narrative writing, drawing to add detail", "#42 + all craft writing pages"),
    ("NGSS 1-LS1-1 / K-LS1-1  Plant parts and plant needs", "#23, 24, 25"),
    ("CASEL Self-Awareness  Identify emotions", "#5 + app check-in"),
]


# ---------------------------------------------------------------------------
def render_png(pdf, page, dpi, out):
    base = out[:-4]
    subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page), "-png", "-singlefile", pdf, base],
                   check=True)
    return out


def pdf_path(num):
    return glob.glob(os.path.join(PDFS, f"{num:02d}-*.pdf"))[0]


def composite(num):
    p = BY_NUM[num]
    return p.get("composite")


# ---------------------------------------------------------------------------
# Start Here guide
# ---------------------------------------------------------------------------

def start_here(path):
    c = rl_canvas.Canvas(path, pagesize=letter)
    c.setTitle(f"Start Here | {L.STORE_NAME} Pumpkin Crafts & Activities")
    c.setAuthor(L.STORE_NAME)
    R = PDFRenderer(c, color=True)

    # cover
    c.setFillColorRGB(*_rgb("#3b2f63"))
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    L.text(c, "50 Pumpkin Crafts", PAGE_W / 2, PAGE_H - 130, 46, "Head", color=_rgb("#ffd43b"))
    L.text(c, "& Fall Activities", PAGE_W / 2, PAGE_H - 182, 46, "Head", color=_rgb("#ffd43b"))
    L.text(c, "Cut  •  Colour  •  Glue  +  Interactive Classroom Games", PAGE_W / 2, PAGE_H - 222, 17, "BodyB",
           color=(1, 1, 1))
    picks = [1, 13, 16, 18, 11, 20, 12, 14, 17]
    for i, n in enumerate(picks):
        x = 120 + (i % 3) * 186
        y = PAGE_H - 320 - (i // 3) * 152
        c.setFillColorRGB(1, 0.965, 0.91)
        c.roundRect(x - 80, y - 70, 160, 140, 18, stroke=0, fill=1)
        kit.draw_fit(R, composite(n), x, y, 128, 124)
    c.setFillColorRGB(*_rgb("#f7902b"))
    c.roundRect(M, 50, PAGE_W - 2 * M, 50, 25, stroke=0, fill=1)
    L.text(c, "PreK - 2nd  •  Low prep  •  Ink-friendly  •  Works offline", PAGE_W / 2, 69, 17, "Head",
           color=(1, 1, 1))
    L.text(c, f"© {L.YEAR} {L.STORE_NAME}", PAGE_W / 2, 26, 9, "Body", color=(0.8, 0.8, 0.9))
    c.showPage()

    # how to use
    L.page_border(c)
    y = PAGE_H - 70
    L.text(c, "Welcome to the Pumpkin Patch!", PAGE_W / 2, y, 30, "Head", color=L.ORANGE)
    y -= 34
    y = L.para(c, "Thank you for downloading! This bundle gives you a whole fall season of low-prep, hands-on "
                  "learning: 50 printable cut, colour and glue resources plus an interactive app your class can "
                  "play on the board, tablets or Chromebooks.", M + 10, y, PAGE_W - 2 * M - 20, 13)
    sections = [
        ("What's in the folder", [
            "00-START-HERE.pdf: this guide (contents, standards and terms of use).",
            "Printables folder: 50 PDFs. Every PDF has a colour teacher page with directions and a finished "
            "example, black-and-white student pages, and a terms of use page.",
            "Classroom-App folder: the Pumpkin Patch Pals interactive games (13 activities).",
        ]),
        ("Printing tips", [
            "Student pages are black and white to save ink. Print the teacher page in colour, or skip it.",
            "Print pumpkin templates on orange paper for a no-colour option. Cardstock is best for the masks, "
            "headbands, wheel and fold-a-die.",
            "Choose 'Fit' or 'Actual size' in your print settings. Pages are US Letter with safe margins, so "
            "they also print well on A4.",
            "Many pieces pages print 2 sets per page. Cut the page in half and give each half to a student.",
        ]),
        ("Using the interactive app", [
            "Unzip the download. Open the Classroom-App folder and double-click index.html. It opens in Chrome, "
            "Edge, Safari or Firefox. No internet or log-in is needed.",
            "Project it on your interactive whiteboard or use it in a centre. Tap the speaker button to hear "
            "directions read aloud, which helps pre-readers.",
            "Turn sound effects and read-aloud on or off with the bell and speech buttons. Press the full-screen "
            "button for whiteboard use.",
            "'Decorate a Pumpkin' pairs with the printable crafts. 'Roll a Jack-o'-Lantern' matches printable #9.",
        ]),
        ("Ideas for the season", [
            "Week 1 Pumpkin science: #23-25 life cycle and parts, plus the app's Life Cycle game.",
            "Week 2 Pumpkin math: #28-30 and #35-41 as centres, plus the app's math games.",
            "Week 3 Literacy: #31-34 and #42-44, plus the app's letters, sounds, rhymes and spelling games.",
            "Fall party: character crafts #10-22, masks #50, banner #47 and headbands #46.",
        ]),
    ]
    for head, items in sections:
        y -= 10
        L.text(c, head, M + 10, y, 17, "Head", "left", L.GREEN)
        y -= 20
        for s in items:
            y = L.para(c, "• " + s, M + 20, y, PAGE_W - 2 * M - 40, 11.5) - 2
    L.footer(c)
    c.showPage()

    # table of contents
    def toc_page(cats):
        L.page_border(c)
        yy = PAGE_H - 64
        L.text(c, "What's Included", PAGE_W / 2, yy, 30, "Head", color=L.ORANGE)
        yy -= 30
        for cat, nums in cats:
            L.text(c, cat, M + 10, yy, 16, "Head", "left", L.PURPLE)
            yy -= 18
            for n in nums:
                p = BY_NUM[n]
                L.text(c, f"{n:02d}", M + 14, yy, 11, "BodyB", "left", L.ORANGE)
                L.text(c, p["title"], M + 40, yy, 11.5, "BodyB", "left")
                L.fit_text(c, p["skills"][0], M + 270, yy, PAGE_W - 2 * M - 340, 10, "Body", "left")
                L.text(c, p.get("grades", "PreK - 2"), PAGE_W - M - 10, yy, 10, "Body", "right")
                fname = os.path.basename(pdf_path(n))
                c.linkURL(f"Printables/{fname}", (M + 10, yy - 3, PAGE_W - M, yy + 11), relative=1)
                yy -= 15
            yy -= 8
        L.footer(c)
        c.showPage()

    toc_page(CATEGORIES[:2])
    toc_page(CATEGORIES[2:])

    # standards
    L.page_border(c)
    y = PAGE_H - 64
    L.text(c, "Standards Connections", PAGE_W / 2, y, 30, "Head", color=L.ORANGE)
    y -= 22
    y = L.para(c, "These resources support the following Common Core, NGSS and CASEL learning goals. "
                  "Use the numbers to find each resource.", M + 10, y, PAGE_W - 2 * M - 20, 11.5)
    y -= 8
    for i, (std, nums) in enumerate(STANDARDS):
        if i % 2 == 0:
            c.setFillColorRGB(*L.SOFT)
            c.rect(M + 4, y - 7, PAGE_W - 2 * M - 8, 24, stroke=0, fill=1)
        L.fit_text(c, std, M + 12, y, PAGE_W - 2 * M - 200, 11, "Body", "left")
        L.text(c, nums, PAGE_W - M - 12, y, 11, "BodyB", "right", L.PURPLE)
        y -= 24
    y -= 10
    y = L.para(c, "Every craft also builds fine-motor skills (cutting, gluing, folding) and following "
                  "multi-step directions. Most crafts include a draw-and-write page for writing practice.",
               M + 10, y, PAGE_W - 2 * M - 20, 11.5)
    L.footer(c)
    c.showPage()

    L.terms_page(c)
    L.footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------------------------
# thumbnails (1000 x 1000 px)
# ---------------------------------------------------------------------------
TH = 750  # points; rendered at 96 dpi -> 1000 px


def _thumb_canvas(path):
    c = rl_canvas.Canvas(path, pagesize=(TH, TH))
    return c, PDFRenderer(c, color=True, base_pt=1.6)


def _night(c):
    c.setFillColorRGB(*_rgb("#3b2f63"))
    c.rect(0, 0, TH, TH, stroke=0, fill=1)
    c.setFillColorRGB(*_rgb("#2a2148"))
    c.rect(0, TH - 150, TH, 150, stroke=0, fill=1)


def _pdf_to_png(pdf, png):
    render_png(pdf, 1, 96, png)
    os.remove(pdf)


def thumb_cover(png):
    pdf = png[:-4] + ".pdf"
    c, R = _thumb_canvas(pdf)
    _night(c)
    L.text(c, "50 Pumpkin Crafts", TH / 2, TH - 92, 58, "Head", color=_rgb("#ffd43b"))
    L.text(c, "& Fall Activities", TH / 2, TH - 150, 50, "Head", color=_rgb("#ffd43b"))
    L.text(c, "Cut • Colour • Glue  + Interactive Games", TH / 2, TH - 188, 24, "BodyB", color=(1, 1, 1))
    picks = [(13, 125, 410, 190), (1, 375, 430, 250), (16, 625, 410, 190), (18, 160, 215, 175), (11, 375, 200, 180),
             (20, 590, 215, 175)]
    for n, x, y, s in picks:
        kit.draw_fit(R, composite(n), x, y, s, s)
    c.setFillColorRGB(*_rgb("#f7902b"))
    c.roundRect(40, 30, TH - 80, 64, 32, stroke=0, fill=1)
    L.text(c, "PreK - 2nd  •  Low Prep  •  Ink-Friendly", TH / 2, 52, 28, "Head", color=(1, 1, 1))
    c.showPage()
    c.save()
    _pdf_to_png(pdf, png)


def thumb_included(png):
    pdf = png[:-4] + ".pdf"
    c, R = _thumb_canvas(pdf)
    c.setFillColorRGB(1, 0.965, 0.91)
    c.rect(0, 0, TH, TH, stroke=0, fill=1)
    c.setFillColorRGB(*_rgb("#f7902b"))
    c.rect(0, TH - 110, TH, 110, stroke=0, fill=1)
    L.text(c, "What's Included", TH / 2, TH - 62, 48, "Head", color=(1, 1, 1))
    L.text(c, "50 printable PDFs  •  220+ pages  •  teacher directions for each", TH / 2, TH - 96, 19,
           "BodyB", color=(1, 1, 1))
    picks = [1, 5, 12, 13, 16, 17, 19, 20, 21, 22, 14, 18]
    for i, n in enumerate(picks):
        x = 95 + (i % 4) * 187
        y = TH - 200 - (i // 4) * 200
        c.setFillColorRGB(1, 1, 1)
        c.roundRect(x - 85, y - 92, 170, 186, 16, stroke=0, fill=1)
        if n == 5:
            BY_NUM[5]["example"](c, R, x, y + 10, 140)
        else:
            kit.draw_fit(R, composite(n), x, y + 10, 140, 140)
        L.fit_text(c, BY_NUM[n]["title"], x, y - 82, 160, 14, "Head", color=L.PURPLE)
    L.text(c, "+ math, literacy, science, masks, banner & more!", TH / 2, 28, 22, "Head", color=L.ORANGE)
    c.showPage()
    c.save()
    _pdf_to_png(pdf, png)


def _page_collage(png, title, sub, pages, bg="#7d4fa6"):
    tmp = tempfile.mkdtemp()
    imgs = []
    for i, (num, pg) in enumerate(pages):
        f = os.path.join(tmp, f"p{i}.png")
        render_png(pdf_path(num), pg, 60, f)
        imgs.append(Image.open(f).convert("RGB"))
    W = 1000
    im = Image.new("RGB", (W, W), bg)
    head = os.path.join(tmp, "head.pdf")
    c = rl_canvas.Canvas(head, pagesize=(TH, 120))
    c.setFillColorRGB(*_rgb(bg))
    c.rect(0, 0, TH, 120, stroke=0, fill=1)
    L.text(c, title, TH / 2, 62, 44, "Head", color=(1, 1, 1))
    L.text(c, sub, TH / 2, 24, 19, "BodyB", color=_rgb("#ffd43b"))
    c.showPage()
    c.save()
    hp = render_png(head, 1, 96, os.path.join(tmp, "head.png"))
    im.paste(Image.open(hp).convert("RGB"), (0, 0))
    cols = 3
    tw = 290
    for i, p in enumerate(imgs):
        t = p.resize((tw, int(p.height * tw / p.width)))
        x = 30 + (i % cols) * (tw + 20)
        y = 180 + (i // cols) * (t.height + 24)
        sh = Image.new("RGBA", (t.width + 20, t.height + 20), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle((10, 10, t.width + 10, t.height + 10), fill=(0, 0, 0, 110))
        sh = sh.filter(ImageFilter.GaussianBlur(6))
        im.paste(sh, (x - 4, y), sh)
        im.paste(t, (x, y))
    im.save(png)
    shutil.rmtree(tmp)


def thumb_pages(png):
    _page_collage(png, "Low-Prep Printables", "Black & white student pages save ink!",
                  [(1, 3), (24, 2), (32, 2), (9, 2), (28, 2), (23, 2)])


def thumb_app(png):
    shots = os.path.join(ROOT, "tools", "screens")
    files = ["desk-home.png", "desk-decorate-built.png", "desk-roll-done.png", "desk-lifecycle-done.png"]
    W = 1000
    im = Image.new("RGB", (W, W), "#3b2f63")
    tmp = tempfile.mkdtemp()
    head = os.path.join(tmp, "head.pdf")
    c = rl_canvas.Canvas(head, pagesize=(TH, 150))
    c.setFillColorRGB(*_rgb("#2a2148"))
    c.rect(0, 0, TH, 150, stroke=0, fill=1)
    L.text(c, "BONUS: Interactive App", TH / 2, 92, 46, "Head", color=_rgb("#ffd43b"))
    L.text(c, "13 games • read-aloud directions • works offline", TH / 2, 50, 21, "BodyB", color=(1, 1, 1))
    L.text(c, "Interactive whiteboards • tablets • Chromebooks", TH / 2, 22, 17, "Body", color=(0.85, 0.85, 1))
    c.showPage()
    c.save()
    im.paste(Image.open(render_png(head, 1, 96, os.path.join(tmp, "h.png"))).convert("RGB"), (0, 0))
    tw = 460
    for i, f in enumerate(files):
        s = Image.open(os.path.join(shots, f)).convert("RGB")
        s = s.crop((0, 0, s.width, int(s.width * 0.68)))
        t = s.resize((tw, int(s.height * tw / s.width)))
        x = 27 + (i % 2) * (tw + 26)
        y = 230 + (i // 2) * (t.height + 40)
        ImageDraw.Draw(im).rounded_rectangle((x - 6, y - 6, x + t.width + 6, y + t.height + 6), 14, fill="#f7902b")
        im.paste(t, (x, y))
    im.save(png)
    shutil.rmtree(tmp)


def product_thumb(prod, png):
    pdf = png[:-4] + ".pdf"
    c, R = _thumb_canvas(pdf)
    c.setFillColorRGB(1, 0.965, 0.91)
    c.rect(0, 0, TH, TH, stroke=0, fill=1)
    c.setFillColorRGB(*_rgb("#3b2f63"))
    c.rect(0, TH - 150, TH, 150, stroke=0, fill=1)
    L.fit_text(c, prod["title"], TH / 2, TH - 85, TH - 60, 52, "Head", color=_rgb("#ffd43b"))
    L.text(c, "Cut • Colour • Glue", TH / 2, TH - 128, 24, "BodyB", color=(1, 1, 1))
    prod["example"](c, R, TH / 2, TH / 2 - 30, 470)
    c.setFillColorRGB(*_rgb("#f7902b"))
    c.roundRect(60, 26, TH - 120, 56, 28, stroke=0, fill=1)
    L.text(c, f"{prod.get('grades', 'PreK - 2')}  •  Low Prep  •  Fall", TH / 2, 45, 26, "Head", color=(1, 1, 1))
    c.showPage()
    c.save()
    _pdf_to_png(pdf, png)


# ---------------------------------------------------------------------------
# watermarked preview
# ---------------------------------------------------------------------------

def preview(path, cover_png):
    wm_buf = io.BytesIO()
    c = rl_canvas.Canvas(wm_buf, pagesize=letter)
    c.saveState()
    c.translate(PAGE_W / 2, PAGE_H / 2)
    c.rotate(45)
    c.setFillColorRGB(0.49, 0.31, 0.65)
    c.setFillAlpha(0.22)
    c.setFont("Head", 110)
    c.drawCentredString(0, -30, "PREVIEW")
    c.setFont("Head", 28)
    c.drawCentredString(0, -80, L.STORE_NAME)
    c.restoreState()
    c.showPage()
    c.save()
    wm = PdfReader(io.BytesIO(wm_buf.getvalue())).pages[0]

    w = PdfWriter()
    cov = io.BytesIO()
    c = rl_canvas.Canvas(cov, pagesize=letter)
    c.drawImage(cover_png, 30, (PAGE_H - (PAGE_W - 60)) / 2, PAGE_W - 60, PAGE_W - 60)
    c.showPage()
    c.save()
    w.add_page(PdfReader(io.BytesIO(cov.getvalue())).pages[0])
    sh = PdfReader(os.path.join(OUT, "00-START-HERE.pdf"))
    for i in (2, 3):
        pg = sh.pages[i]
        w.add_page(pg)
    samples = [(1, 1), (1, 2), (1, 3), (5, 2), (9, 2), (13, 3), (16, 1), (23, 2), (24, 2), (28, 2), (32, 2),
               (38, 2), (44, 2), (47, 2), (50, 2)]
    for num, pg in samples:
        page = PdfReader(pdf_path(num)).pages[pg - 1]
        page.merge_page(wm)
        w.add_page(page)
    with open(path, "wb") as f:
        w.write(f)


# ---------------------------------------------------------------------------

def listings_csv(path):
    """One row per product, for listing the 50 resources individually as well as the bundle."""
    import csv
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["#", "file", "TpT title (max ~80 chars)", "grades", "suggested price (USD)", "pages",
                    "short description", "skills", "thumbnail"])
        for p in PRODUCTS:
            fn = pdf_path(p["num"])
            pages = len(PdfReader(fn).pages)
            craft = p["num"] <= 22 or p["num"] in (26, 45, 46, 47, 48, 49, 50)
            kind = "Craft" if craft else "Activity"
            title = f"{p['title']} {kind} | Fall Pumpkin Cut and Paste | Halloween"
            if len(title) > 80:
                title = f"{p['title']} | Fall Pumpkin {kind} Cut and Paste"
            price = "3.00" if pages <= 5 else "3.50"
            desc = (f"{p['title']}: a low-prep fall pumpkin {kind.lower()} for {p.get('grades', 'PreK - 2')}. "
                    f"Includes a colour teacher page with directions and a finished example, black-and-white "
                    f"student pages ({pages - 2} pages), and terms of use. Students cut, colour and glue.")
            w.writerow([p["num"], os.path.basename(fn), title[:80], p.get("grades", "PreK - 2"), price, pages, desc,
                        "; ".join(p["skills"]), f"product-thumbnails/{p['num']:02d}-{B.slug(p['title'])}.png"])


def build_zip(path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(OUT, "00-START-HERE.pdf"), "Pumpkin Patch Pals/00-START-HERE.pdf")
        for f in sorted(glob.glob(os.path.join(PDFS, "*.pdf"))):
            z.write(f, f"Pumpkin Patch Pals/Printables/{os.path.basename(f)}")
        for root, _, files in os.walk(APP):
            for fn in files:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, APP)
                z.write(full, f"Pumpkin Patch Pals/Classroom-App/{rel}")
        z.writestr("Pumpkin Patch Pals/Classroom-App/HOW TO OPEN.txt",
                   "Double-click index.html to open Pumpkin Patch Pals in your web browser.\n"
                   "Keep every file in this folder together. No internet or log-in is needed.\n"
                   "Tip: press the full-screen button for interactive whiteboards.\n")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for p in PRODUCTS:
        if "contents" not in p:
            B.dry_run(p)
    start_here(os.path.join(OUT, "00-START-HERE.pdf"))
    thumbs = os.path.join(OUT, "thumbnails")
    os.makedirs(thumbs, exist_ok=True)
    thumb_cover(os.path.join(thumbs, "1-cover.png"))
    thumb_included(os.path.join(thumbs, "2-whats-included.png"))
    thumb_pages(os.path.join(thumbs, "3-printable-pages.png"))
    thumb_app(os.path.join(thumbs, "4-interactive-app.png"))
    pt = os.path.join(OUT, "product-thumbnails")
    os.makedirs(pt, exist_ok=True)
    for p in PRODUCTS:
        product_thumb(p, os.path.join(pt, f"{p['num']:02d}-{B.slug(p['title'])}.png"))
    preview(os.path.join(OUT, "PREVIEW-watermarked.pdf"), os.path.join(thumbs, "1-cover.png"))
    listings_csv(os.path.join(OUT, "individual-listings.csv"))
    build_zip(os.path.join(OUT, "Pumpkin-Patch-Pals-TpT-Upload.zip"))
    for f in sorted(os.listdir(OUT)):
        fp = os.path.join(OUT, f)
        print(f, os.path.getsize(fp) // 1024 if os.path.isfile(fp) else "dir", "KB")
