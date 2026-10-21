"""Products 23-50: science, literacy, math and fall craft printables (cut, colour, glue)."""
import math
import random

import art as A
from engine import Art
import kit
from kit import K, pack_pages, template_page, writing_page, assembled, example_of, example_page, draw_fit
import layout as L
from layout import PAGE_W, PAGE_H, M

PRODUCTS = []
CUT_GLUE = ["Crayons or markers", "Scissors", "Glue stick"]


def add(num, title, build, example, skills, steps, tip=None, grades="PreK - 2", **kw):
    PRODUCTS.append(dict(num=num, title=title, build=build, example=example, skills=skills,
                         steps=steps, tip=tip, grades=grades, **kw))


def single(page_fn):
    """Build function that draws one page from a (c, R) page function."""
    def b(doc):
        c = doc.page()
        page_fn(c, doc.R)
    return b


def box(c, x, y, w, h, r=10, lw=1.5, dash=None):
    c.saveState()
    L.ink(c)
    c.setLineWidth(lw)
    if dash:
        c.setDash(*dash)
    c.roundRect(x, y, w, h, r, stroke=1, fill=0)
    c.restoreState()


def arrow(c, x1, y1, x2, y2, lw=2.2):
    c.saveState()
    L.ink(c)
    c.setLineWidth(lw)
    c.line(x1, y1, x2, y2)
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (1, -1):
        c.line(x2, y2, x2 - 10 * math.cos(ang + s * 0.5), y2 - 10 * math.sin(ang + s * 0.5))
    c.restoreState()


def num_pumpkin(c, R, n, cx, cy, size, font_size=None, font="Head"):
    R.draw(A.pumpkin(ribs=False, vine=False, leaf=False), cx, cy, size)
    fs = font_size or size * 0.36
    L.text(c, str(n), cx, cy - size * 0.06 - fs * 0.3, fs, font)


def number_cards(doc, title, sub, nums, cols, rows, art_fn=None):
    c = doc.page()
    y = L.header(c, doc.R, title, sub)
    cw, ch = (PAGE_W - 2 * M) / cols, (y - 40) / rows
    for i, n in enumerate(nums):
        cx = M + (i % cols + 0.5) * cw
        cy = y - (i // cols + 0.5) * ch
        L.cut_box(c, doc.R, cx - cw / 2 + 4, cy - ch / 2 + 4, cw - 8, ch - 8, r=8, icon=(i == 0))
        if art_fn:
            art_fn(c, doc.R, n, cx, cy, min(cw, ch) * 0.8)
        else:
            num_pumpkin(c, doc.R, n, cx, cy, min(cw, ch) * 0.8)


def seeds_card(c, R, n, cx, cy, size):
    """n pumpkin seeds arranged in rows of up to 5."""
    rows = [2] * (n // 2) + ([1] if n % 2 else [])
    s = size * 0.42
    for r, cnt in enumerate(rows):
        yy = cy + (len(rows) - 1) * s * 0.45 - r * s * 0.9
        for i in range(cnt):
            xx = cx + (i - (cnt - 1) / 2) * s * 0.7
            R.draw(A.pumpkin_seed(), xx, yy, s)


# ===========================================================================
# 23 Parts of a pumpkin
# ===========================================================================
PARTS_WORDS = ["stem", "leaf", "vine", "skin", "pulp", "seeds"]


def _parts_page(c, R, answers=False):
    y = L.header(c, R, "Parts of a Pumpkin", "Cut out the words. Glue each word in the box that names that part.")
    X1, Y1, S1 = M + 175, y - 165, 300
    X2, Y2, S2 = PAGE_W - M - 175, y - 470, 300
    R.draw(A.pumpkin(), X1, Y1, S1)
    R.draw(A.pumpkin_inside(), X2, Y2, S2)
    L.text(c, "outside", X1, Y1 - S1 * 0.5 - 6, 15, "Head")
    L.text(c, "inside", X2, Y2 - S2 * 0.5 - 6, 15, "Head")
    spots = [  # word, art point (page), label box centre
        ("stem", (X1 + 1 * S1 / 100, Y1 + 38 * S1 / 100), (X1 + 200, Y1 + 130)),
        ("leaf", (X1 + 24 * S1 / 100, Y1 + 38 * S1 / 100), (X1 + 260, Y1 + 50)),
        ("vine", (X1 - 26 * S1 / 100, Y1 + 32 * S1 / 100), (X1 - 60, Y1 + 160)),
        ("skin", (X2 - 47 * S2 / 100, Y2 - 10 * S2 / 100), (X2 - 250, Y2 + 70)),
        ("pulp", (X2 - 30 * S2 / 100, Y2 + 2 * S2 / 100), (X2 - 250, Y2 - 10)),
        ("seeds", (X2 - 4 * S2 / 100, Y2 - 14 * S2 / 100), (X2 - 250, Y2 - 90)),
    ]
    bw, bh = 110, 38
    for word, (ax, ay), (bx, by) in spots:
        c.saveState()
        L.ink(c)
        c.setLineWidth(1.3)
        tx = bx + (bw / 2 if ax > bx else -bw / 2)
        if abs(ax - bx) < bw / 2:
            tx, ty = bx, by - bh / 2
        else:
            ty = by
        c.line(tx, ty, ax, ay)
        c.circle(ax, ay, 3, stroke=0, fill=1)
        c.setFillColorRGB(1, 1, 1)
        c.roundRect(bx - bw / 2, by - bh / 2, bw, bh, 8, stroke=1, fill=1)
        c.restoreState()
        if answers:
            L.text(c, word, bx, by - 7, 20, "BodyB", color=L.PURPLE)


def _parts_build(doc):
    c = doc.page()
    _parts_page(c, doc.R)
    kit.card_grid(doc, "Parts of a Pumpkin: Words", "Cut apart the word cards (3 sets per page).",
                  [None] * 18, 3, 6, labels=PARTS_WORDS * 3, label_size=17)
    writing_page(doc, "Pumpkin Facts", "Draw and write about the inside of a pumpkin.",
                 "The inside of a pumpkin has")


add(23, "Parts of a Pumpkin", _parts_build, example_page(lambda c, R: _parts_page(c, R, True)),
    ["Science: identify the parts of a plant (stem, leaf, vine, skin, pulp, seeds)",
     "Vocabulary and word reading", "Cutting and gluing labels"],
    ["Cut open a real pumpkin together, or show pictures of one. Name each part as you point to it.",
     "Students colour both pumpkins.",
     "Cut apart the word cards. Each page holds 3 sets.",
     "Read each word and glue it in the box that points to that part.",
     "Finish the 'Pumpkin Facts' draw-and-write page."],
    "The teacher example doubles as an answer key. Project it for students to check their work.",
    grades="K - 2")

# ===========================================================================
# 24 Life cycle cut & paste
# ===========================================================================
STAGES = [("seed", A.pumpkin_seed), ("sprout", A.sprout), ("vine", A.vine_plant),
          ("flower", A.pumpkin_flower), ("green pumpkin", A.green_pumpkin), ("orange pumpkin", A.pumpkin)]


def _cycle_page(c, R, answers=False):
    y = L.header(c, R, "Pumpkin Life Cycle", "Cut out the pictures. Glue them in order. Then write the word.")
    bw, bh = 150, 150
    xs = [M + 20, PAGE_W / 2 - bw / 2, PAGE_W - M - 20 - bw]
    rows_y = [y - 30, y - 330]
    order = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1)]
    for i, (col, row) in enumerate(order):
        x, top = xs[col], rows_y[row]
        box(c, x, top - bh, bw, bh, 14)
        c.setFillColorRGB(*L.ORANGE)
        c.circle(x + 16, top - 16, 13, stroke=0, fill=1)
        L.text(c, str(i + 1), x + 16, top - 22, 15, "Head", color=(1, 1, 1))
        L.simple_lines(c, x + 6, top - bh - 34, bw - 12, 1)
        if answers:
            draw_fit(R, STAGES[i][1](), x + bw / 2, top - bh / 2, bw * 0.8, bh * 0.8)
            L.text(c, STAGES[i][0], x + bw / 2, top - bh - 30, 15, "BodyB", color=L.PURPLE)
    my = rows_y[0] - bh / 2
    arrow(c, xs[0] + bw + 6, my, xs[1] - 6, my)
    arrow(c, xs[1] + bw + 6, my, xs[2] - 6, my)
    arrow(c, xs[2] + bw / 2, rows_y[0] - bh - 44, xs[2] + bw / 2, rows_y[1] + 6)
    my2 = rows_y[1] - bh / 2
    arrow(c, xs[2] - 6, my2, xs[1] + bw + 6, my2)
    arrow(c, xs[1] - 6, my2, xs[0] + bw + 6, my2)
    arrow(c, xs[0] + bw / 2, rows_y[1] + 6, xs[0] + bw / 2, rows_y[0] - bh - 44)
    L.text(c, "Word bank:  seed  •  sprout  •  vine  •  flower  •  green pumpkin  •  orange pumpkin",
           PAGE_W / 2, 50, 12, "Body")


def _cycle_build(doc):
    c = doc.page()
    _cycle_page(c, doc.R)
    order = [3, 0, 5, 1, 4, 2]
    kit.card_grid(doc, "Life Cycle Pictures", "Colour and cut out the pictures (2 sets per page).",
                  [STAGES[i][1]() for i in order] * 2, 4, 3, art_frac=0.85, icon=True)
    writing_page(doc, "How a Pumpkin Grows", "Draw your favourite stage of the life cycle.", "First, a pumpkin is a")


add(24, "Pumpkin Life Cycle Cut & Paste", _cycle_build, example_page(lambda c, R: _cycle_page(c, R, True)),
    ["Science: life cycle of a plant", "Sequencing (first, next, last)", "Vocabulary and writing"],
    ["Read a pumpkin life cycle book or watch a short video.",
     "Students colour and cut out the six picture cards.",
     "Put the cards in order on the desk first. Check with a partner.",
     "Glue each picture in its numbered box and copy the word from the word bank.",
     "Finish with the 'How a Pumpkin Grows' page."],
    "Plant real pumpkin seeds in a clear cup so students can watch the sprout stage.", grades="K - 2")

# ===========================================================================
# 25 Life cycle wheel
# ===========================================================================


def _wheel_base(c, R):
    y = L.header(c, R, "Life Cycle Wheel: Bottom", "Colour and cut out the circle. Push a brad through the centre dot.")
    cx, cy, r = PAGE_W / 2, (y + 40) / 2, min(250, (y - 50) / 2)
    c.saveState()
    L.ink(c)
    c.setLineWidth(2)
    c.circle(cx, cy, r, stroke=1, fill=0)
    for i in range(6):
        a = math.radians(90 + 30 + i * 60)
        c.setLineWidth(1.2)
        c.line(cx, cy, cx + r * math.cos(a), cy + r * math.sin(a))
    c.circle(cx, cy, 5, stroke=0, fill=1)
    c.restoreState()
    for i, (name, fn) in enumerate(STAGES):
        th = 90 - i * 60
        a = math.radians(th)
        px, py = cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)
        R.draw(fn(), px, py, r * 0.42, rot=90 - th)
        lx, ly = cx + r * 0.88 * math.cos(a), cy + r * 0.88 * math.sin(a)
        c.saveState()
        c.translate(lx, ly)
        c.rotate(th - 90)
        L.text(c, f"{i + 1}. {name}", 0, -5, 14, "BodyB")
        c.restoreState()


def _wheel_top(c, R):
    y = L.header(c, R, "Life Cycle Wheel: Top", "Cut out the circle and the window. Put it on top of the bottom wheel.")
    cx, cy, r = PAGE_W / 2, (y + 40) / 2, min(250, (y - 50) / 2)
    c.saveState()
    L.ink(c)
    c.setLineWidth(2)
    c.circle(cx, cy, r, stroke=1, fill=0)
    p = c.beginPath()
    a1, a2 = math.radians(60), math.radians(120)
    r1, r2 = r * 0.2, r * 0.98
    p.moveTo(cx + r1 * math.cos(a1), cy + r1 * math.sin(a1))
    p.lineTo(cx + r2 * math.cos(a1), cy + r2 * math.sin(a1))
    p.arcTo(cx - r2, cy - r2, cx + r2, cy + r2, 60, 60)
    p.lineTo(cx + r1 * math.cos(a2), cy + r1 * math.sin(a2))
    p.arcTo(cx - r1, cy - r1, cx + r1, cy + r1, 120, -60)
    p.close()
    c.setDash(6, 4)
    c.setLineWidth(1.5)
    c.drawPath(p, stroke=1, fill=0)
    c.setDash()
    c.circle(cx, cy, 5, stroke=0, fill=1)
    c.restoreState()
    L.text(c, "cut out the window", cx, cy + r * 0.5, 11, "Body", color=(0.5, 0.5, 0.5))
    L.text(c, "Pumpkin", cx, cy - r * 0.32, 34, "Head")
    L.text(c, "Life Cycle", cx, cy - r * 0.5, 34, "Head")
    L.text(c, "by ________________", cx, cy - r * 0.7, 15, "Body")
    for ang, fn in [(200, A.mini_pumpkin), (340, A.maple_leaf), (165, A.acorn), (15, A.simple_leaf)]:
        a = math.radians(ang)
        R.draw(fn(), cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a), r * 0.24)


def _wheel_build(doc):
    c = doc.page()
    _wheel_base(c, doc.R)
    c = doc.page()
    _wheel_top(c, doc.R)


add(25, "Pumpkin Life Cycle Wheel", _wheel_build, example_page(_wheel_base),
    ["Science: life cycle of a pumpkin", "Sequencing and retelling", "Fine-motor cutting (circles)"],
    ["Print the bottom and top wheels. Cardstock works best.",
     "Students colour the six stages on the bottom wheel, then cut out both circles.",
     "Cut out the window on the top wheel. An adult may need to start the cut.",
     "Stack the top wheel on the bottom wheel and push a brad through both centre dots.",
     "Spin the wheel and retell the life cycle to a partner."],
    "Send the wheel home so students can teach the life cycle to their families.",
    materials=["Crayons", "Scissors", "1 brad (paper fastener) per student", "Cardstock (optional)"],
    grades="K - 3")

# ===========================================================================
# 26 Build a scarecrow
# ===========================================================================
SCARE_PARTS = [(A.straw_tuft(), -30, 8, 18, False, -100), (A.straw_tuft(), 30, 8, 18, True, 100),
               (A.straw_tuft(), -9, 70, 16, False, 180), (A.straw_tuft(), 9, 70, 16, True, 180),
               (A.shirt(), 0, 12, 58), (A.overalls(), 0, 42, 46), (A.patch("leaf"), 9, 50, 9),
               (A.scarecrow_head(), 0, -30, 36), (A.farmer_hat(), 0, -50, 48), (A.crow(), 26, -60, 20)]
SCARE = Art()
SCARE_PARTS = [tuple(list(p) + [False, 0][len(p) - 4:]) for p in SCARE_PARTS]
for _p in SCARE_PARTS:
    SCARE.add(_p[0], dx=_p[1], dy=_p[2], s=_p[3] / 100, flip=_p[4], rot=_p[5])


def _scare_build(doc):
    k = 4.0
    pack_pages(doc, "Build a Scarecrow: Pieces", "Colour and cut out the pieces.",
               [(p[0], p[3] * k, p[4], p[5] if abs(p[5]) != 180 else 0) for p in SCARE_PARTS] +
               [(A.pumpkin(), 70), (A.pumpkin(), 60)], double=False)
    c = doc.page()
    y = L.header(c, doc.R, "My Scarecrow", "Glue your scarecrow in the field. Add a crow and some pumpkins!")
    c.saveState()
    L.ink(c)
    c.setLineWidth(2)
    c.line(M, 150, PAGE_W - M, 150)
    for x in range(int(M) + 10, int(PAGE_W - M), 70):
        c.rect(x, 150, 16, 90, stroke=1, fill=0)
        c.line(x + 0, 240, x + 8, 252)
        c.line(x + 16, 240, x + 8, 252)
    c.rect(M, 200, PAGE_W - 2 * M, 12, stroke=1, fill=0)
    c.rect(M, 170, PAGE_W - 2 * M, 12, stroke=1, fill=0)
    c.restoreState()
    doc.R.draw(A.sunflower(), PAGE_W - M - 50, y - 50, 80)
    doc.R.draw(A.hay_bale(), PAGE_W - M - 80, 105, 100)
    for x in range(int(M) + 30, int(PAGE_W - M), 60):
        c.line(x, 80, x + 10, 100)
    writing_page(doc, "My Scarecrow", "What is your scarecrow's name?", "My scarecrow's name is")


add(26, "Build a Scarecrow", _scare_build, example_of(SCARE),
    ["Following directions to assemble a figure", "Fine-motor cutting and gluing", "Fall vocabulary"],
    ["Colour all the scarecrow pieces with bright fall colours.",
     "Cut out the pieces along the thick lines.",
     "Build the scarecrow on the field page: shirt and overalls first, then head and hat.",
     "Tuck the straw pieces under the sleeves and pant legs. Add the crow and pumpkins.",
     "Name your scarecrow on the writing page."], "Add real raffia or yellow yarn for straw texture.")

# ===========================================================================
# 27 Pumpkin vine name craft
# ===========================================================================


def _name_example(c, R, x, y, size):
    k = size / 260
    R.draw(A.vine_strip(), x, y + 20 * k, 250 * k)
    for i, ch in enumerate("SAM"):
        px = x + (i - 1) * 74 * k
        R.draw(A.pumpkin(ribs=False, vine=False, leaf=False), px, y - 22 * k, 70 * k)
        L.text(c, ch, px, y - 34 * k, 30 * k, "Head")
    L.text(c, "+ more pumpkins for longer names!", x, y - 100 * k, 11 * k, "Body")


def _name_build(doc):
    pcs = [(A.pumpkin(ribs=False, vine=False, leaf=False), 118) for _ in range(12)]
    pack_pages(doc, "Pumpkin Name Vine: Pumpkins", "Write one letter of your name on each pumpkin. Colour and cut.",
               pcs, double=False)
    pack_pages(doc, "Pumpkin Name Vine: Vines", "Cut out the vines. Glue the ends together for long names.",
               [(A.vine_strip(), 520), (A.vine_strip(), 520), (A.vine_strip(), 520)],
               double=False)


add(27, "Pumpkin Name Vine", _name_build, _name_example,
    ["Name recognition and letter formation", "Counting letters in a name", "Cutting and gluing"],
    ["Write each student's name on a sentence strip as a model.",
     "Students write one letter on each pumpkin, starting with a capital letter.",
     "Colour and cut out the pumpkins they need, and one or two vines.",
     "Glue the pumpkins on the vine in order to spell their name.",
     "Count: 'My name has ___ letters.' Compare names to see whose is longest."],
    "Hang the name vines around the door frame for a pumpkin patch entrance.", grades="PreK - K")

# ===========================================================================
# 28 Seed counting match 1-10
# ===========================================================================


def _seed_page(c, R):
    y = L.header(c, R, "Count the Seeds", "Cut out the seed cards. Glue each card under the pumpkin with the same number.")
    cols, rows = 5, 2
    cw, ch = (PAGE_W - 2 * M) / cols, (y - 40) / rows
    for i in range(10):
        cx = M + (i % cols + 0.5) * cw
        top = y - (i // cols) * ch
        num_pumpkin(c, R, i + 1, cx, top - 62, 108)
        L.glue_box(c, cx - cw / 2 + 6, top - ch + 10, cw - 12, ch - 140, "glue")


def _seed_build(doc):
    c = doc.page()
    _seed_page(c, doc.R)
    nums = [3, 7, 1, 10, 5, 8, 2, 6, 9, 4]
    number_cards(doc, "Seed Cards", "Count the seeds. Cut out each card.", nums, 5, 2,
                 art_fn=lambda c, R, n, cx, cy, s: seeds_card(c, R, n, cx, cy, 120))


add(28, "Pumpkin Seed Counting 1-10", _seed_build, example_page(_seed_page),
    ["Counting objects 1-10 with one-to-one correspondence", "Number recognition", "Cutting and gluing"],
    ["Model counting seeds by touching each one as you count.",
     "Students cut out the 10 seed cards.",
     "Count the seeds on each card and find the pumpkin with that number.",
     "Glue the card in the box under the matching pumpkin."],
    "Use real pumpkin seeds on the pumpkin page as a hands-on centre before the cut-and-glue.",
    grades="PreK - K")

# ===========================================================================
# 29 Number order 1-20
# ===========================================================================


def _order_page(c, R, start=1):
    y = L.header(c, R, f"Pumpkin Number Order {start}-{start + 9}", "Cut out the pumpkins. Glue them on the vine in order.")
    bw = (PAGE_W - 2 * M) / 5
    for row in range(2):
        top = y - 30 - row * 300
        c.saveState()
        c.setStrokeColorRGB(*L.GREEN)
        c.setLineWidth(5)
        p = c.beginPath()
        p.moveTo(M, top - 150)
        for i in range(5):
            x0 = M + i * bw
            p.curveTo(x0 + bw * 0.3, top - 110, x0 + bw * 0.7, top - 190, x0 + bw, top - 150)
        c.drawPath(p, stroke=1, fill=0)
        c.restoreState()
        for i in range(5):
            n = start + row * 5 + i
            cx = M + (i + 0.5) * bw
            L.glue_box(c, cx - bw / 2 + 6, top - 230, bw - 12, 160, None)
            if n in (start, start + 4, start + 7):
                num_pumpkin(c, R, n, cx, top - 150, bw * 0.75)
            else:
                L.text(c, "?", cx, top - 160, 30, "Head", color=(0.75, 0.75, 0.75))


def _order_build(doc):
    for start in (1, 11):
        c = doc.page()
        _order_page(c, doc.R, start)
    rnd = random.Random(29)
    nums = [n for n in range(1, 21) if (n - 1) % 10 not in (0, 4, 7)]
    rnd.shuffle(nums)
    number_cards(doc, "Number Pumpkins", "Colour and cut out the pumpkins.", nums, 4, 4)


add(29, "Pumpkin Number Order 1-20", _order_build, example_page(lambda c, R: _order_page(c, R, 1)),
    ["Number order and sequencing to 20", "Number recognition", "Finding missing numbers"],
    ["Count to 20 together, pointing to a number line.",
     "Students cut out the number pumpkins.",
     "Start with the numbers already on the vine. Say what comes before and after.",
     "Glue the pumpkins in order on each vine.",
     "Read the finished vines out loud, forwards and backwards."],
    "Use the 1-10 page for PreK and K, and both pages for first grade.", grades="PreK - 1")

# ===========================================================================
# 30 Ten frame pumpkins
# ===========================================================================


def _tenframe_page(c, R, nums=(4, 7, 2, 9)):
    y = L.header(c, R, "Fill the Ten Frames", "Read the number. Glue that many pumpkins in the ten frame.")
    cell = 62
    for i, n in enumerate(nums):
        top = y - 10 - i * 160
        x0 = M + 110
        num_pumpkin(c, R, n, M + 45, top - 62, 95)
        c.saveState()
        L.ink(c)
        c.setLineWidth(2)
        for r in range(2):
            for k in range(5):
                c.rect(x0 + k * cell, top - 10 - (r + 1) * cell, cell, cell, stroke=1, fill=0)
        c.restoreState()


def _tenframe_build(doc):
    for nums in [(4, 7, 2, 9), (5, 10, 3, 8)]:
        c = doc.page()
        _tenframe_page(c, doc.R, nums)
    pack_pages(doc, "Ten Frame Pumpkins", "Colour and cut out the pumpkins.",
               [(A.mini_pumpkin(), 54) for _ in range(54)], gap=12, double=False)


add(30, "Pumpkin Ten Frames", _tenframe_build, example_page(_tenframe_page),
    ["Counting and representing numbers 1-10", "Ten-frame fluency", "One-to-one correspondence"],
    ["Show a ten frame and model filling the top row first, left to right.",
     "Students colour and cut out the small pumpkins.",
     "Read each number and glue that many pumpkins in the ten frame.",
     "Ask: 'How many more to make 10?'"],
    "Laminate the ten frame pages and use orange pom-poms for a reusable math centre.", grades="PreK - 1")

# ===========================================================================
# 31 Uppercase / lowercase match
# ===========================================================================


def _abc_page(c, R, letters):
    y = L.header(c, R, f"Letter Match {letters[0]}-{letters[-1]}", "Glue the lowercase letter under its uppercase pumpkin.")
    cols, rows = 4, 4
    cw, ch = (PAGE_W - 2 * M) / cols, (y - 40) / rows
    for i, ch_ in enumerate(letters):
        cx = M + (i % cols + 0.5) * cw
        top = y - (i // cols) * ch
        R.draw(A.pumpkin(ribs=False, vine=False, leaf=False), cx, top - 48, 92)
        L.text(c, ch_, cx, top - 64, 40, "BodyB")
        L.glue_box(c, cx - 30, top - ch + 10, 60, 56, None)


def _abc_build(doc):
    up = [chr(65 + i) for i in range(26)]
    for part in (up[:13], up[13:]):
        c = doc.page()
        _abc_page(c, doc.R, part)
    low = [chr(97 + i) for i in range(26)]
    random.Random(31).shuffle(low)
    kit.card_grid(doc, "Lowercase Letter Cards", "Cut apart the letter cards.",
                  [None] * 26 + [A.mini_pumpkin() for _ in range(4)], 6, 5,
                  labels=low + ["", "", "", ""], label_size=30)


add(31, "Pumpkin Letter Match A-Z", _abc_build, example_page(lambda c, R: _abc_page(c, R, [chr(65 + i) for i in range(13)])),
    ["Matching uppercase and lowercase letters", "Letter identification", "Cutting small pieces"],
    ["Sing the alphabet song while pointing to letters.",
     "Students cut apart the lowercase letter cards.",
     "Find the matching lowercase letter for each uppercase pumpkin.",
     "Glue it in the box under the pumpkin. Say the letter name and sound."],
    "Split it over two days: A-M on day one and N-Z on day two.", grades="PreK - K")

# ===========================================================================
# 32 Beginning sounds
# ===========================================================================
SOUNDS = [("b", "bat"), ("c", "cat"), ("g", "ghost"), ("h", "hat"), ("l", "leaf"), ("m", "moon"),
          ("o", "owl"), ("p", "pumpkin"), ("s", "star"), ("w", "web"), ("a", "apple"), ("r", "rake")]


def _sounds_page(c, R, answers=False):
    y = L.header(c, R, "Beginning Sounds", "Say the picture name. Glue it under the letter it starts with.")
    cols, rows = 4, 3
    cw, ch = (PAGE_W - 2 * M) / cols, (y - 40) / rows
    for i, (ltr, word) in enumerate(SOUNDS):
        cx = M + (i % cols + 0.5) * cw
        top = y - (i // cols) * ch
        R.draw(A.pumpkin(ribs=False, vine=False, leaf=False), cx, top - 48, 92)
        L.text(c, ltr, cx, top - 64, 40, "BodyB")
        L.glue_box(c, cx - 50, top - ch + 10, 100, ch - 108, None)
        if answers:
            draw_fit(R, A.PICTURES[word](), cx, top - ch + 10 + (ch - 108) / 2, 80, ch - 120)


def _sounds_build(doc):
    c = doc.page()
    _sounds_page(c, doc.R)
    order = [5, 9, 0, 7, 3, 11, 1, 6, 10, 4, 8, 2]
    kit.card_grid(doc, "Beginning Sound Pictures", "Colour and cut out the picture cards.",
                  [A.PICTURES[SOUNDS[i][1]]() for i in order], 4, 3, art_frac=0.8)


add(32, "Fall Beginning Sounds", _sounds_build, example_page(lambda c, R: _sounds_page(c, R, True)),
    ["Phonemic awareness: beginning sounds", "Letter-sound correspondence", "Vocabulary"],
    ["Name each picture together: bat, cat, ghost, hat, leaf, moon, owl, pumpkin, star, web, apple, rake.",
     "Students colour and cut out the picture cards.",
     "Say the picture name slowly and listen for the first sound.",
     "Glue the picture under the pumpkin with that letter."],
    "Stretch the first sound like a rubber band: 'mmmm-oon'.", grades="PreK - 1")

# ===========================================================================
# 33 Rhyming
# ===========================================================================
RHYMES = [("cat", "hat"), ("moon", "spoon"), ("star", "car"), ("rake", "cake"), ("bee", "tree"), ("bug", "mug")]
PIC = dict(A.PICTURES, spoon=A.spoon, car=A.car, cake=A.cake, tree=A.tree, mug=A.mug, bee=A.bee, bug=A.bug)


def _rhyme_page(c, R, answers=False):
    y = L.header(c, R, "Rhyme Time Pumpkins", "Find the picture that rhymes. Glue it in the box.")
    rh = (y - 40) / 6
    for i, (a, b) in enumerate(RHYMES):
        cy = y - (i + 0.5) * rh
        R.draw(A.mini_pumpkin(), M + 30, cy, 46)
        box(c, M + 70, cy - rh / 2 + 6, 150, rh - 12)
        draw_fit(R, PIC[a](), M + 120, cy, 80, rh - 26)
        L.text(c, a, M + 190, cy - 6, 18, "BodyB")
        arrow(c, M + 240, cy, M + 300, cy)
        L.text(c, "rhymes with", M + 270, cy + 8, 9, "Body")
        L.glue_box(c, M + 320, cy - rh / 2 + 6, 200, rh - 12, None if answers else "glue")
        if answers:
            draw_fit(R, PIC[b](), M + 380, cy, 80, rh - 26)
            L.text(c, b, M + 460, cy - 6, 18, "BodyB", color=L.PURPLE)


def _rhyme_build(doc):
    c = doc.page()
    _rhyme_page(c, doc.R)
    order = [3, 0, 5, 2, 4, 1]
    words = [RHYMES[i][1] for i in order] * 2
    kit.card_grid(doc, "Rhyming Picture Cards", "Cut out the cards (2 sets per page).",
                  [PIC[w]() for w in words], 3, 4, labels=words, art_frac=0.85)


add(33, "Rhyme Time Pumpkins", _rhyme_build, example_page(lambda c, R: _rhyme_page(c, R, True)),
    ["Phonological awareness: rhyming words", "Listening and speaking", "Cutting and gluing"],
    ["Play a quick rhyming game: 'Cat, hat. Do they rhyme? Thumbs up!'",
     "Name all the picture cards together.",
     "Students cut out the cards and say each word.",
     "Glue the rhyming picture next to its match."],
    "Challenge: think of a third rhyming word for each pair (cat, hat, bat!).", grades="PreK - 1")

# ===========================================================================
# 34 CVC words
# ===========================================================================
CVC = ["cat", "bat", "hat", "bug", "mug", "web"]
CVC_PIC = {"cat": A.black_cat, "bat": A.bat, "hat": A.top_hat, "bug": A.bug, "mug": A.mug, "web": A.spider_web}


def _cvc_page(c, R, answers=False):
    y = L.header(c, R, "Spooky CVC Words", "Say the word. Glue the letters to spell it.")
    rh = (y - 40) / 6
    for i, w in enumerate(CVC):
        cy = y - (i + 0.5) * rh
        box(c, M, cy - rh / 2 + 6, 130, rh - 12)
        draw_fit(R, CVC_PIC[w](), M + 65, cy, 100, rh - 26)
        for j in range(3):
            x = M + 170 + j * 110
            box(c, x, cy - rh / 2 + 10, 90, rh - 20, 10)
            if answers:
                L.text(c, w[j], x + 45, cy - 14, 40, "BodyB", color=L.PURPLE)
        R.draw(A.mini_pumpkin(), PAGE_W - M - 30, cy, 44)


def _cvc_build(doc):
    c = doc.page()
    _cvc_page(c, doc.R)
    letters = list("".join(CVC))
    random.Random(34).shuffle(letters)
    kit.card_grid(doc, "Letter Tiles", "Cut apart the letter tiles (2 sets per page).", [None] * 36, 6, 6,
                  labels=letters * 2, label_size=26)


add(34, "Spooky CVC Words", _cvc_build, example_page(lambda c, R: _cvc_page(c, R, True)),
    ["Phonics: blending and segmenting CVC words", "Spelling short-vowel words", "Letter-sound mapping"],
    ["Say each picture word and tap out the sounds: /c/ /a/ /t/.",
     "Students cut apart the letter tiles.",
     "Find the letter for each sound and glue it in order in the boxes.",
     "Read each finished word to a partner."],
    "Keep spare tiles in a baggie for word-building practice all month.", grades="K - 1")

# ===========================================================================
# 35 Patterns
# ===========================================================================
PATTERNS = [("AB", [A.mini_pumpkin, A.maple_leaf]), ("AB", [A.acorn, A.apple]),
            ("AAB", [A.ghost, A.ghost, A.bat]), ("ABB", [A.candy_corn, A.moon, A.moon]),
            ("ABC", [A.mini_pumpkin, A.simple_leaf, A.acorn]), ("AABB", [A.apple, A.apple, A.mini_pumpkin, A.mini_pumpkin])]


def _pattern_seq(fns, n=8):
    return [fns[i % len(fns)] for i in range(n)]


def _pattern_page(c, R, answers=False):
    y = L.header(c, R, "Pumpkin Patch Patterns", "What comes next? Glue the pictures to finish each pattern.")
    rh = (y - 40) / 6
    cell = (PAGE_W - 2 * M - 40) / 8
    for i, (kind, fns) in enumerate(PATTERNS):
        cy = y - (i + 0.5) * rh
        L.text(c, kind, M + 16, cy - 6, 14, "Head")
        seq = _pattern_seq(fns)
        for j, fn in enumerate(seq):
            x = M + 40 + j * cell
            if j < 6:
                box(c, x + 2, cy - cell / 2 + 2, cell - 4, cell - 4, 8, lw=1.2)
                draw_fit(R, fn(), x + cell / 2, cy, cell * 0.72, cell * 0.72)
            else:
                L.glue_box(c, x + 2, cy - cell / 2 + 2, cell - 4, cell - 4, None)
                if answers:
                    draw_fit(R, fn(), x + cell / 2, cy, cell * 0.72, cell * 0.72)


def _pattern_build(doc):
    c = doc.page()
    _pattern_page(c, doc.R)
    ans = []
    for kind, fns in PATTERNS:
        ans += _pattern_seq(fns)[6:]
    random.Random(35).shuffle(ans)
    kit.card_grid(doc, "Pattern Pieces", "Colour and cut out the pieces (2 sets per page).",
                  [f() for f in ans] * 2, 6, 4, art_frac=0.8)


add(35, "Pumpkin Patch Patterns", _pattern_build, example_page(lambda c, R: _pattern_page(c, R, True)),
    ["Math: extending AB, AAB, ABB, ABC and AABB patterns", "Visual discrimination", "Cutting and gluing"],
    ["Make a body pattern together: clap, stomp, clap, stomp...",
     "Read each pattern row out loud ('pumpkin, leaf, pumpkin, leaf').",
     "Students cut out the pattern pieces.",
     "Glue the two pieces that come next in each row."],
    "Have early finishers create their own pattern on the back with stickers or drawings.", grades="PreK - 1")

# ===========================================================================
# 36 Size sort
# ===========================================================================


def _size_page(c, R):
    y = L.header(c, R, "Small, Medium, Big", "Sort the fall pictures by size. Glue each one in the right column.")
    cw = (PAGE_W - 2 * M) / 3
    for i, (w, s) in enumerate([("small", 40), ("medium", 62), ("big", 86)]):
        x = M + i * cw
        box(c, x + 6, 50, cw - 12, y - 60, 14)
        R.draw(A.mini_pumpkin(), x + cw / 2, y - 106 + s / 2, s)
        L.text(c, w, x + cw / 2, y - 140, 24, "Head")
        c.saveState()
        L.ink(c)
        c.setLineWidth(1)
        c.line(x + 20, y - 154, x + cw - 20, y - 154)
        c.restoreState()


def _size_build(doc):
    c = doc.page()
    _size_page(c, doc.R)
    pcs = []
    for fn in [A.pumpkin, A.maple_leaf, A.acorn, A.apple]:
        for s in (55, 90, 135):
            pcs.append((fn(), s))
    pack_pages(doc, "Size Sort Pictures", "Colour and cut out the pictures.", pcs, double=False)


add(36, "Small, Medium, Big Sort", _size_build, example_page(_size_page),
    ["Math: comparing and sorting by size", "Measurement vocabulary (small, medium, big)", "Cutting and gluing"],
    ["Show three real pumpkins or gourds of different sizes and compare them.",
     "Students colour and cut out the 12 pictures.",
     "Find the three sizes of each picture.",
     "Glue the pictures in the small, medium or big column."],
    "Extend it: order the pictures from smallest to biggest on a sentence strip.", grades="PreK - K")

# ===========================================================================
# 37 Measure with seeds
# ===========================================================================
SEED_LEN = 30.0
MEASURE = [("candy corn", A.candy_corn, 3), ("acorn", A.acorn, 2), ("leaf", A.oak_leaf, 4),
           ("corn", A.corn, 5), ("broom", A.broom, 7)]


def _measure_page(c, R, answers=False):
    y = L.header(c, R, "Measure with Seeds", "Line up seeds under each picture. How many seeds long is it?")
    rh = (y - 40) / len(MEASURE)
    for i, (name, fn, n) in enumerate(MEASURE):
        top = y - i * rh
        art = kit.tf(fn(), rot=90)
        from engine import bbox
        x0, y0, x1, y1 = bbox(art)
        k = n * SEED_LEN / (x1 - x0)
        left = M + 20
        R.draw(art, left - x0 * k, top - 40 + (y0 + y1) / 2 * k, 100 * k)
        c.saveState()
        L.ink(c)
        c.setLineWidth(1.4)
        c.line(left, top - 72, left, top - 104)
        c.setDash(3, 3)
        c.line(left, top - 104, left + 240, top - 104)
        c.restoreState()
        if answers:
            for j in range(n):
                R.draw(A.pumpkin_seed(), left + SEED_LEN * (j + 0.5), top - 88, 38, rot=90)
        L.text(c, f"The {name} is", PAGE_W - M - 230, top - 50, 15, "Body", "left")
        box(c, PAGE_W - M - 230, top - 104, 60, 40, 8)
        if answers:
            L.text(c, str(n), PAGE_W - M - 200, top - 96, 26, "Head", color=L.PURPLE)
        L.text(c, "seeds long.", PAGE_W - M - 160, top - 90, 15, "Body", "left")


def _measure_build(doc):
    c = doc.page()
    _measure_page(c, doc.R)
    pack_pages(doc, "Seed Measuring Pieces", "Colour and cut out the seeds.",
               [(A.pumpkin_seed(), 38, False, 90) for _ in range(66)], gap=10, double=False)


add(37, "Measure with Pumpkin Seeds", _measure_build, example_page(lambda c, R: _measure_page(c, R, True)),
    ["Measurement with non-standard units", "Counting and comparing lengths", "Precise cutting"],
    ["Model measuring: start at the line and place the seeds end to end, with no gaps or overlaps.",
     "Students cut out the paper seeds (or use real dried pumpkin seeds).",
     "Measure each picture and glue the seeds in place.",
     "Count the seeds and write the number in the box.",
     "Ask: 'Which picture is the longest? The shortest?'"],
    "Real dried pumpkin seeds work well too. Just skip the glue and record the numbers.", grades="K - 1")

# ===========================================================================
# 38 Pumpkin glyph
# ===========================================================================
GLYPH = [
    ("Do you like pumpkin pie?", [("yes", A.eye("triangle")), ("no", A.eye("round"))], "eyes"),
    ("What is your favourite fall thing?", [("leaves", A.nose("triangle")), ("apples", A.nose("heart")),
                                            ("cocoa", A.nose("circle"))], "nose"),
    ("Do you like spooky stories?", [("yes", A.mouth("zigzag")), ("no", A.mouth("smile"))], "mouth"),
    ("Have you been to a pumpkin patch?", [("yes", A.top_hat()), ("no", A.hair_bow())], "hat or bow"),
]


def _glyph_key(c, R):
    y = L.header(c, R, "Pumpkin Glyph Key", "Answer each question. Glue on the piece that matches your answer.")
    rh = (y - 120) / len(GLYPH)
    for i, (q, opts, part) in enumerate(GLYPH):
        top = y - i * rh
        L.text(c, f"{i + 1}. {q}", M, top - 18, 16, "BodyB", "left")
        L.text(c, f"({part})", PAGE_W - M, top - 18, 12, "Body", "right")
        ow = (PAGE_W - 2 * M) / 3
        for j, (lab, art) in enumerate(opts):
            cx = M + (j + 0.5) * ow
            draw_fit(R, art, cx, top - rh / 2 - 6, 90, rh - 70)
            L.text(c, lab, cx, top - rh + 14, 15, "Head")
    top = y - len(GLYPH) * rh
    L.text(c, "5. How many people live in your home?", M, top - 20, 16, "BodyB", "left")
    L.text(c, "Glue on that many seeds!", M + 20, top - 42, 14, "Body", "left")
    for j in range(5):
        R.draw(A.pumpkin_seed(), PAGE_W - M - 180 + j * 34, top - 40, 40)


def _glyph_build(doc):
    c = doc.page()
    _glyph_key(c, doc.R)
    template_page(doc, "My Pumpkin Glyph", "Follow the key to build a pumpkin that tells about you!")
    pcs = [(A.eye("triangle"), 20 * K), (A.eye("triangle"), 20 * K, True), (A.eye("round"), 20 * K),
           (A.eye("round"), 20 * K, True)]
    pcs += [(A.nose(n), 13 * K) for n in ("triangle", "heart", "circle")]
    pcs += [(A.mouth(m), 36 * K) for m in ("zigzag", "smile")]
    pcs += [(A.top_hat(), 40 * K), (A.hair_bow(), 30 * K)]
    pcs += [(A.pumpkin_seed(), 50) for _ in range(10)]
    pack_pages(doc, "Glyph Pieces", "Cut out only the pieces that match your answers.", pcs, double=False)
    writing_page(doc, "My Glyph Tells About Me", "Read your glyph. What does it tell about you?", "My pumpkin shows that I")


GLYPH_EX = assembled([(A.top_hat(), 0, -44, 40), (A.eye("triangle"), -15, -2, 20), (A.eye("triangle"), 15, -2, 20, True),
                      (A.nose("heart"), 0, 12, 13), (A.mouth("smile"), 0, 27, 36),
                      (A.pumpkin_seed(), -30, 30, 8, False, 30), (A.pumpkin_seed(), 30, 30, 8, False, -30),
                      (A.pumpkin_seed(), -36, 14, 8), (A.pumpkin_seed(), 36, 14, 8)])
add(38, "Pumpkin Glyph: All About Me", _glyph_build, example_of(GLYPH_EX),
    ["Data: reading a key (legend)", "Listening and following directions", "Math talk: comparing class data"],
    ["Project the glyph key and read each question aloud.",
     "Students answer each question by gluing on the matching piece.",
     "For question 5, glue on one seed for each person at home.",
     "Write about the glyph on the writing page.",
     "Display the glyphs and ask: 'How many people like pumpkin pie? How do you know?'"],
    "Display the glyphs with the key so families can 'read' each pumpkin at open house.", grades="K - 2")

# ===========================================================================
# 39 Roll & graph with a fold-up die
# ===========================================================================
DIE_PICS = [A.mini_pumpkin, A.maple_leaf, A.acorn, A.apple, A.candy_corn, A.owl]
DIE_NAMES = ["pumpkin", "leaf", "acorn", "apple", "candy corn", "owl"]


def _die_page(c, R):
    y = L.header(c, R, "Make a Fall Die", "Colour, cut on the outside lines, fold on every line and glue the tabs.")
    s = 128
    cx0 = PAGE_W / 2 - 1.5 * s
    top = y - 20
    cells = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (1, 3)]
    tabs = [((0, 1), "top"), ((0, 1), "bottom"), ((2, 1), "top"), ((2, 1), "bottom"), ((1, 3), "left"),
            ((1, 3), "right"), ((1, 0), "left")]
    c.saveState()
    L.ink(c)
    for (col, row), fn in zip(cells, DIE_PICS):
        x, yy = cx0 + col * s, top - (row + 1) * s
        c.setLineWidth(2)
        c.rect(x, yy, s, s, stroke=1, fill=0)
        draw_fit(R, fn(), x + s / 2, yy + s / 2, s * 0.7, s * 0.7)
        L.ink(c)
    t = 26
    c.setLineWidth(1.5)
    for (col, row), side in tabs:
        x, yy = cx0 + col * s, top - (row + 1) * s
        if side == "top":
            pts = [(x, yy + s), (x + t, yy + s + t), (x + s - t, yy + s + t), (x + s, yy + s)]
        elif side == "bottom":
            pts = [(x, yy), (x + t, yy - t), (x + s - t, yy - t), (x + s, yy)]
        elif side == "left":
            pts = [(x, yy), (x - t, yy + t), (x - t, yy + s - t), (x, yy + s)]
        else:
            pts = [(x + s, yy), (x + s + t, yy + t), (x + s + t, yy + s - t), (x + s, yy + s)]
        p = c.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        c.drawPath(p, stroke=1, fill=0)
        mx = sum(px for px, _ in pts[1:3]) / 2
        my = sum(py for _, py in pts[1:3]) / 2
        mx = (mx + (pts[0][0] + pts[3][0]) / 2) / 2
        my = (my + (pts[0][1] + pts[3][1]) / 2) / 2
        L.text(c, "glue", mx, my - 3, 8, "Body", color=(0.5, 0.5, 0.5))
    c.restoreState()


def _graph_page(c, R):
    y = L.header(c, R, "Roll & Graph", "Roll your fall die. Colour one box above the picture you roll.")
    cols, rows = 6, 10
    gx0, gw = M + 30, PAGE_W - 2 * M - 30
    cw = gw / cols
    gh = y - 230
    rh = gh / rows
    base = y - 10 - gh
    c.saveState()
    L.ink(c)
    c.setLineWidth(1.4)
    for i in range(cols):
        for j in range(rows):
            c.rect(gx0 + i * cw, base + j * rh, cw, rh, stroke=1, fill=0)
    c.restoreState()
    for j in range(rows):
        L.text(c, str(j + 1), gx0 - 14, base + j * rh + rh / 2 - 5, 13, "BodyB")
    for i, fn in enumerate(DIE_PICS):
        draw_fit(R, fn(), gx0 + (i + 0.5) * cw, base - 36, cw * 0.6, 50)
        L.fit_text(c, DIE_NAMES[i], gx0 + (i + 0.5) * cw, base - 76, cw - 4, 12, "BodyB")
    L.text(c, "Which picture did you roll the most?", M, base - 108, 14, "Body", "left")
    L.simple_lines(c, M + 250, base - 110, PAGE_W - 2 * M - 250, 1)
    L.text(c, "Which picture did you roll the least?", M, base - 136, 14, "Body", "left")
    L.simple_lines(c, M + 250, base - 138, PAGE_W - 2 * M - 250, 1)


def _die_build(doc):
    c = doc.page()
    _die_page(c, doc.R)
    c = doc.page()
    _graph_page(c, doc.R)


add(39, "Fall Roll & Graph (Fold-a-Die)", _die_build, example_page(_die_page),
    ["Data: collecting and graphing results", "Comparing more and fewer", "Fine-motor cutting, folding and gluing (3D shape)"],
    ["Copy the die page on cardstock. Students colour the six pictures.",
     "Cut on the outside lines, fold on every line, and glue the tabs inside to make a cube.",
     "Roll the die and colour one box above the picture rolled. Keep going until one column reaches the top.",
     "Answer the questions at the bottom of the graph."],
    "Partners can share one die and race to fill a column first.",
    materials=["Crayons", "Scissors", "Glue stick or tape", "Cardstock (recommended)"], grades="K - 2")

# ===========================================================================
# 40 / 41 Addition & subtraction
# ===========================================================================
ADD = [(2, 3), (4, 1), (3, 3), (5, 2), (1, 6), (4, 4), (6, 3), (5, 5)]
SUB = [(5, 2), (6, 1), (4, 3), (7, 4), (8, 2), (9, 5), (10, 3), (6, 6)]


def _group(c, R, n, x, y, w, cross=0):
    s = 26
    per = 5
    for i in range(n):
        px = x + (i % per) * s * 1.02 + s / 2
        py = y + (0.5 - i // per) * s * 1.0 if n > per else y
        R.draw(A.mini_pumpkin(), px, py, s)
        if i >= n - cross:
            c.saveState()
            L.ink(c)
            c.setLineWidth(2.2)
            c.line(px - s / 2, py - s / 2, px + s / 2, py + s / 2)
            c.line(px - s / 2, py + s / 2, px + s / 2, py - s / 2)
            c.restoreState()


def _math_page(c, R, probs, op, answers=False):
    title = "Pumpkin Patch Addition" if op == "+" else "Pumpkin Patch Subtraction"
    sub = "Add the pumpkins. Glue the answer in the box." if op == "+" else "Cross out and take away. Glue the answer in the box."
    y = L.header(c, R, title, sub)
    rh = (y - 40) / 8
    for i, (a, b) in enumerate(probs):
        cy = y - (i + 0.5) * rh
        box(c, M, cy - rh / 2 + 4, PAGE_W - 2 * M, rh - 8, 12, lw=1.1)
        if op == "+":
            _group(c, R, a, M + 10, cy + 10, 140)
            L.text(c, "+", M + 170, cy + 2, 26, "Head")
            _group(c, R, b, M + 190, cy + 10, 140)
            eq = f"{a} + {b} ="
            ans = a + b
        else:
            _group(c, R, a, M + 10, cy + 10, 280, cross=b)
            eq = f"{a} - {b} ="
            ans = a - b
        L.text(c, eq, M + 430, cy - 9, 26, "Head", "right")
        L.glue_box(c, PAGE_W - M - 110, cy - rh / 2 + 10, 90, rh - 20, None)
        if answers:
            L.text(c, str(ans), PAGE_W - M - 65, cy - 10, 28, "Head", color=L.PURPLE)


def _math_build(probs, op):
    def b(doc):
        c = doc.page()
        _math_page(c, doc.R, probs, op)
        ans = [a + b_ if op == "+" else a - b_ for a, b_ in probs]
        random.Random(len(probs) + (1 if op == "+" else 2)).shuffle(ans)
        number_cards(doc, "Answer Pumpkins", "Cut out the answer pumpkins (2 sets per page).", ans * 2, 4, 4)
    return b


add(40, "Pumpkin Patch Addition", _math_build(ADD, "+"),
    example_page(lambda c, R: _math_page(c, R, ADD, "+", True)),
    ["Addition within 10 using pictures", "Number sentences", "Counting on"],
    ["Model one problem: count the first group, then count on with the second group.",
     "Students cut out the answer pumpkins.",
     "Solve each problem and glue the answer pumpkin in the box.",
     "Read each number sentence aloud: 'Two plus three equals five.'"],
    "Use orange counters on the pumpkins for students who need a hands-on model.", grades="K - 1")

add(41, "Pumpkin Patch Subtraction", _math_build(SUB, "-"),
    example_page(lambda c, R: _math_page(c, R, SUB, "-", True)),
    ["Subtraction within 10 using pictures", "Number sentences", "Understanding 'take away'"],
    ["Act it out: 5 'pumpkins' (students) stand up and 2 sit down. How many are left?",
     "Students cut out the answer pumpkins.",
     "Count the pumpkins left after the crossed-out ones are taken away.",
     "Glue the answer pumpkin in the box and read the number sentence."],
    "Talk about the last problem, where every pumpkin is taken away. What number is left?", grades="K - 1")

# ===========================================================================
# 42 If I were a pumpkin writing craft
# ===========================================================================


def _topper_example(c, R, x, y, size):
    w, h = size * 0.62, size * 0.62
    c.saveState()
    L.ink(c)
    c.setFillColorRGB(1, 1, 1)
    c.setLineWidth(1)
    c.rect(x - w / 2, y - size / 2, w, h, stroke=1, fill=1)
    for i in range(5):
        yy = y - size / 2 + h - 22 - i * 22
        c.line(x - w / 2 + 8, yy, x + w / 2 - 8, yy)
    c.restoreState()
    R.draw(assembled([(A.eye("happy"), -15, -2, 20), (A.eye("happy"), 15, -2, 20, True),
                      (A.nose("triangle"), 0, 12, 13), (A.mouth("smile"), 0, 27, 34)]),
           x, y + size * 0.18, size * 0.6)


def _topper_build(doc):
    template_page(doc, "Pumpkin Topper", "Draw your own pumpkin face. Colour it, cut it out and glue it on your writing.",
                  size=460)
    c = doc.page()
    y = L.header(c, doc.R, "If I Were a Pumpkin...", None)
    L.text(c, "If I were a pumpkin, I would", M, y - 10, 20, "Body", "left")
    L.primary_lines(c, M, y - 34, PAGE_W - 2 * M, 7, 82)
    c = doc.page()
    y = L.header(c, doc.R, "If I Were a Pumpkin...", "(lined paper for older writers)")
    L.text(c, "If I were a pumpkin, I would", M, y - 10, 16, "Body", "left")
    L.simple_lines(c, M, y - 40, PAGE_W - 2 * M, 22, 28)


add(42, "If I Were a Pumpkin Writing Craft", _topper_build, _topper_example,
    ["Narrative / imaginative writing", "Using a sentence starter", "Drawing to plan writing"],
    ["Brainstorm together: if you were a pumpkin, where would you live? What would you see?",
     "Students draw a face on the pumpkin topper, then colour it and cut it out.",
     "Write on the primary-lined page (K-1) or the lined page (2nd grade).",
     "Glue the topper to the top of the writing page so the pumpkin peeks over it."],
    "These make an adorable bulletin board: 'Our Writing Is Growing in the Pumpkin Patch!'", grades="K - 2")

# ===========================================================================
# 43 How to carve a pumpkin sequencing
# ===========================================================================
CARVE = [("Pick a pumpkin.", A.pumpkin_patch_pick), ("Scoop out the seeds.", A.pumpkin_open),
         ("Draw a face.", A.pumpkin_drawn_face), ("Light it up!", lambda: A.pumpkin_face(glow=True))]


def _carve_page(c, R, answers=False):
    y = L.header(c, R, "How to Carve a Pumpkin", "Glue the pictures in order. Write about each step.")
    cw, ch = (PAGE_W - 2 * M) / 2, (y - 40) / 2
    for i, word in enumerate(["First", "Next", "Then", "Last"]):
        x = M + (i % 2) * cw
        top = y - (i // 2) * ch
        box(c, x + 6, top - ch + 6, cw - 12, ch - 12, 14)
        L.text(c, word, x + 22, top - 30, 20, "Head", "left")
        L.glue_box(c, x + 22, top - 220, cw - 44, 180, None)
        if answers:
            draw_fit(R, CARVE[i][1](), x + cw / 2, top - 130, 150, 160)
            L.text(c, CARVE[i][0], x + 24, top - 252, 15, "Body", "left", L.PURPLE)
        L.simple_lines(c, x + 22, top - 256, cw - 44, 2, 30)


def _carve_build(doc):
    c = doc.page()
    _carve_page(c, doc.R)
    order = [2, 0, 3, 1]
    kit.card_grid(doc, "Pumpkin Carving Pictures", "Colour and cut out the pictures (2 sets per page).",
                  [CARVE[i][1]() for i in order] * 2, 2, 4, art_frac=0.85)


add(43, "How to Carve a Pumpkin", _carve_build, example_page(lambda c, R: _carve_page(c, R, True)),
    ["Procedural (how-to) writing", "Sequencing words: first, next, then, last", "Retelling steps in order"],
    ["Talk about carving a pumpkin at home. Only grown-ups use the knife!",
     "Students cut out the four picture cards.",
     "Put them in order, then glue each one under First, Next, Then and Last.",
     "Write a sentence about each step."],
    "Carve or decorate a class pumpkin first, and take photos of each step as an anchor chart.",
    grades="K - 2")

# ===========================================================================
# 44 Colour words emergent reader
# ===========================================================================
READER = [("orange", "an orange pumpkin", A.pumpkin, "orange"), ("red", "a red apple", A.apple, "red"),
          ("yellow", "a yellow corn", A.corn, "yellow"), ("brown", "a brown acorn", A.acorn, "stem"),
          ("green", "a green pumpkin", A.green_pumpkin, "leaf"), ("purple", "a purple hat", A.witch_hat, "purple"),
          ("black", "a black cat", A.black_cat, "dark"), ("white", "a white ghost", A.ghost, "white"),
          ("blue", "a blue car", lambda: _blue_car(), "blue")]


def _blue_car():
    a = A.car()
    a.ops = [op if not (op[0] == "path" and op[2] == "red") else (op[0], op[1], "blue", op[3], op[4]) for op in a.ops]
    return a


def _reader_half(c, R, idx, top, h):
    if idx == 0:
        L.text(c, "My Fall", PAGE_W / 2, top - 70, 44, "Head")
        L.text(c, "Colour Book", PAGE_W / 2, top - 118, 44, "Head")
        for i, (_, _, fn, _) in enumerate(READER[:5]):
            draw_fit(R, fn(), PAGE_W / 2 + (i - 2) * 92, top - 205, 70, 80)
        L.text(c, "by", M + 70, top - h + 50, 18, "Body", "left")
        L.simple_lines(c, M + 100, top - h + 48, 300, 1)
        return
    word, phrase, fn, col = READER[idx - 1]
    draw_fit(R, fn(), PAGE_W / 2, top - 130, 300, 190)
    L.text(c, f"I see {phrase}.", PAGE_W / 2, top - h + 50, 30, "Body")
    R.draw(A.crayon(col), M + 50, top - 40, 70, rot=-20)
    L.text(c, word, M + 50, top - 76, 13, "BodyB")
    L.text(c, str(idx), PAGE_W - M - 10, top - h + 28, 12, "Body", "right")


def _reader_page(c, R, idxs):
    L.PAGE_LOG.append("Colour Book pages")
    h = (PAGE_H - 50) / 2
    for k, idx in enumerate(idxs):
        top = PAGE_H - 20 - k * (h + 10)
        _reader_half(c, R, idx, top, h)
    L.cut_line(c, R, M - 10, PAGE_H / 2 + 5, PAGE_W - M + 10, PAGE_H / 2 + 5)


def _reader_build(doc):
    for i in range(0, 10, 2):
        c = doc.page()
        _reader_page(c, doc.R, [i, i + 1])


add(44, "My Fall Colour Book", _reader_build, example_page(lambda c, R: _reader_page(c, R, [0, 1])),
    ["Emergent reading: colour words and sight words 'I', 'see', 'a'", "One-to-one pointing while reading",
     "Following colour directions"],
    ["Print, cut each page in half on the dashed line and stack the pages in order.",
     "Staple on the left side to make a 10-page mini book.",
     "Students colour each picture using the colour word (look at the crayon for help).",
     "Read the book with a pointer finger under each word, then read it to a buddy."],
    "Colour the little crayon on each page first. Then students can check the word by the colour.",
    materials=["Crayons", "Scissors", "Stapler"], grades="PreK - K")

# ===========================================================================
# 45 Fall tree craft
# ===========================================================================


def _tree_build(doc):
    template_page(doc, "My Fall Tree", "Colour the tree. Glue colourful leaves on the branches and on the ground!",
                  base=A.fall_tree(), size=540)
    pcs = []
    cols = ["maple", "gold", "rust", "orange", "red"]
    for i in range(30):
        fn = [A.maple_leaf, A.oak_leaf, A.simple_leaf][i % 3]
        pcs.append((fn(cols[i % 5]), [70, 56, 86][i % 3], False, (i * 37) % 60 - 30))
    pack_pages(doc, "Fall Leaves", "Colour the leaves red, orange, yellow and brown. Cut them out.", pcs,
               gap=12, double=False)
    writing_page(doc, "My Fall Tree", "How many leaves did you glue on your tree?", "My tree has")


TREE_EX = Art().add(A.fall_tree())
for _i, (_x, _y, _r) in enumerate([(-30, -36, 10), (-10, -44, -20), (14, -40, 30), (32, -30, 0), (-38, -24, 40),
                                   (0, -28, -10), (24, -22, 20), (-20, -16, 50), (-30, 40, 80), (20, 42, -60)]):
    TREE_EX.add([A.maple_leaf, A.oak_leaf, A.simple_leaf][_i % 3](["maple", "gold", "rust", "orange", "red"][_i % 5]),
                dx=_x, dy=_y, s=0.16, rot=_r)
add(45, "Fall Tree Leaf Craft", _tree_build, example_of(TREE_EX),
    ["Science: seasonal change (leaves change colour)", "Counting", "Fine-motor cutting"],
    ["Take a nature walk to collect and compare real fall leaves.",
     "Students colour the tree trunk and the leaves with fall colours.",
     "Cut out the tree and the leaves.",
     "Glue the leaves on the branches and some 'falling' on the ground.",
     "Count the leaves and finish the writing page."],
    "Mix it up: glue on tissue paper squares or real pressed leaves instead.", grades="PreK - 2")

# ===========================================================================
# 46 Pumpkin headband
# ===========================================================================


def _band_strip(c, R, y, deco):
    w, h = PAGE_W - 2 * M, 78
    L.cut_box(c, R, M, y - h, w, h, r=6)
    for i in range(7):
        x = M + 40 + i * (w - 80) / 6
        R.draw(deco[i % len(deco)](), x, y - h / 2, 52, rot=(i % 2) * 20 - 10)
    L.text(c, "glue", M + 14, y - h / 2 - 4, 9, "Body", color=(0.6, 0.6, 0.6))


def _band_build(doc):
    c = doc.page()
    y = L.header(c, doc.R, "Pumpkin Headband", "Colour and cut out the pumpkin and both bands.")
    doc.R.draw(A.pumpkin(), PAGE_W / 2, y - 170, 330)
    _band_strip(c, doc.R, 250, [A.maple_leaf, A.acorn, A.simple_leaf])
    _band_strip(c, doc.R, 150, [A.oak_leaf, A.mini_pumpkin, A.maple_leaf])
    pack_pages(doc, "Headband Face Pieces", "Optional: give your headband pumpkin a face!",
               [(A.eye("triangle"), 20 * 3.3), (A.eye("triangle"), 20 * 3.3, True), (A.eye("happy"), 20 * 3.3),
                (A.eye("happy"), 20 * 3.3, True), (A.nose("triangle"), 13 * 3.3), (A.mouth("grin"), 36 * 3.3),
                (A.mouth("smile"), 36 * 3.3)])


BAND_EX = Art()
BAND_EX.rect(-50, 8, 100, 14, 3, "leaf")
for _x in (-40, -20, 20, 40):
    BAND_EX.add(A.maple_leaf("gold"), dx=_x, dy=15, s=0.12)
BAND_EX.add(A.pumpkin(), dx=0, dy=-8, s=0.5)
add(46, "Pumpkin Headband Crown", _band_build, example_of(BAND_EX),
    ["Fine-motor cutting (long straight lines)", "Measuring to fit", "Fall celebration craft"],
    ["Print on cardstock if possible. Students colour the pumpkin and both bands.",
     "Cut out the pumpkin and the two bands.",
     "Glue or staple the bands together, then glue the pumpkin in the middle.",
     "Wrap it around the student's head, mark the size and staple it closed."],
    "Perfect for a pumpkin patch field trip, a fall party or a class photo!",
    materials=["Crayons", "Scissors", "Glue and a stapler", "Cardstock (recommended)"])

# ===========================================================================
# 47 Pennant banner
# ===========================================================================
BANNER = list("HAPPY") + ["*"] + list("FALL") + ["*"] + list("BOO") + ["#"]


def _pennant(c, R, x, top, w, h, ch):
    c.saveState()
    L.ink(c)
    c.setLineWidth(1.4)
    c.setDash(6, 4)
    p = c.beginPath()
    p.moveTo(x, top)
    p.lineTo(x + w, top)
    p.lineTo(x + w / 2, top - h)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    c.setDash(2, 3)
    c.setLineWidth(1)
    c.line(x + 6, top - 26, x + w - 6, top - 26)
    c.restoreState()
    L.text(c, "fold", x + w / 2, top - 18, 9, "Body", color=(0.55, 0.55, 0.55))
    if ch == "*":
        R.draw(A.pumpkin(), x + w / 2, top - h * 0.36, w * 0.5)
    elif ch == "#":
        R.draw(A.ghost(), x + w / 2, top - h * 0.36, w * 0.45)
    else:
        kit.outline_text(c, ch, x + w / 2, top - h * 0.52, h * 0.42, "Head", lw=2)
        R.draw(A.maple_leaf() if ch in "HAPYFL" else A.bat(), x + w / 2, top - h * 0.7, w * 0.18)


def _banner_page(c, R, chars):
    L.PAGE_LOG.append("Banner pennants")
    w, h = 260, 340
    for i, ch in enumerate(chars):
        col, row = i % 2, i // 2
        x = PAGE_W / 2 - w - 6 + col * (w + 12)
        top = PAGE_H - 30 - row * (h + 24)
        _pennant(c, R, x, top, w, h, ch)


def _banner_build(doc):
    for i in range(0, len(BANNER), 4):
        c = doc.page()
        _banner_page(c, doc.R, BANNER[i:i + 4])


add(47, "Happy Fall & BOO Banner", _banner_build, example_page(lambda c, R: _banner_page(c, R, BANNER[:4])),
    ["Letter recognition and spelling a phrase", "Fine-motor colouring inside the lines", "Classroom community decor"],
    ["Give each student (or pair) a pennant to colour. Bubble letters are great for pattern colouring!",
     "Cut out each pennant on the dashed line.",
     "Fold the top flap over a long piece of yarn and glue or tape it down.",
     "Hang 'HAPPY FALL' and 'BOO' with the pumpkin and ghost pennants between the words."],
    "Use it as a classroom job: students put the letters in order to spell the words before hanging.",
    materials=["Crayons or markers", "Scissors", "Yarn or string", "Tape or glue"], grades="PreK - 3")

# ===========================================================================
# 48 3D paper strip pumpkin
# ===========================================================================


def _strips_page(c, R, n=8):
    y = L.header(c, R, "3D Pumpkin Strips", "Colour the strips orange. Cut them out and punch the dots.")
    sh = min(66, (y - 40) / n)
    for i in range(n):
        top = y - i * sh
        L.cut_box(c, R, M, top - sh + 8, PAGE_W - 2 * M, sh - 10, r=5, icon=(i == 0))
        for x in (M + 16, PAGE_W - M - 16):
            c.circle(x, top - sh / 2 + 3, 4, stroke=1, fill=0)
        c.saveState()
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setLineWidth(0.8)
        for k in range(1, 6):
            xx = M + 30 + k * (PAGE_W - 2 * M - 60) / 6
            c.line(xx, top - sh + 18, xx + 30, top - 10)
        c.restoreState()


def _strips_build(doc):
    c = doc.page()
    _strips_page(c, doc.R)
    pack_pages(doc, "3D Pumpkin Stem & Leaves", "Colour and cut out a stem, leaves and a curly vine.",
               [(_stem_piece(), 120), (A.simple_leaf("leaf"), 110), (A.simple_leaf("leaf"), 110, True),
                (_curl(), 120), (_stem_piece(), 120), (A.simple_leaf("leaf"), 110),
               (A.simple_leaf("leaf"), 110, True), (_curl(), 120)])


def _stem_piece():
    a = Art()
    a.path("M -12 40 C -14 10 -10 -20 -4 -40 L 12 -38 C 6 -16 8 12 12 40 Z", "stem")
    a.rect(-20, 36, 40, 10, 3, "stem2")
    return a


def _curl():
    a = Art()
    a.path("M -40 0 C -40 -20 -10 -24 -6 -6 C -2 10 -24 12 -22 0 C -21 -8 -12 -8 -12 -2 L -16 -2 "
           "C -16 -4 -18 -4 -18 0 C -18 6 -8 6 -10 -6 C -12 -18 -34 -16 -34 0 C -34 22 0 26 14 10 "
           "C 24 0 34 0 44 4 L 44 10 C 34 6 26 8 18 16 C 2 34 -40 28 -40 0 Z", "leaf2")
    return a


def _strip_pumpkin():
    a = Art()
    for rx in (48, 40, 30, 18, 6):
        a.ellipse(0, 6, rx, 40, "orange" if rx != 6 else "orange3")
    a.add(_stem_piece(), dx=0, dy=-40, s=0.25)
    a.add(A.simple_leaf("leaf"), dx=12, dy=-40, s=0.25, rot=60)
    return a


add(48, "3D Paper Strip Pumpkin", _strips_build, example_of(_strip_pumpkin()),
    ["Fine-motor cutting (long straight lines)", "3D shapes: making a sphere", "Following steps in order"],
    ["Print on orange paper (or colour the strips orange). Each student needs 8 strips.",
     "Cut out the strips and hole-punch (or poke with a pencil) the dots at both ends.",
     "Stack the strips and push a brad through the dots at one end.",
     "Bend the stack around and push the other ends onto the same brad, or staple them.",
     "Spread the strips out into a ball and glue the stem, leaves and curly vine on top."],
    "Stapling works if you don't have brads. Staple all the top ends together, then all the bottom ends.",
    materials=["Orange paper or crayons", "Scissors", "Hole punch", "2 brads or a stapler"], grades="K - 3")

# ===========================================================================
# 49 Paper bag puppet
# ===========================================================================


def _puppet_build(doc):
    head = assembled([(A.eye("happy"), -15, -2, 20), (A.eye("happy"), 15, -2, 20, True),
                      (A.nose("triangle", "none"), 0, 12, 13)], base=A.pumpkin(ribs=False))
    pack_pages(doc, "Pumpkin Puppet: Head & Body", "Colour and cut out. Fits a standard paper lunch bag.",
               [(head, 330), (A.shirt("orange3"), 300)], double=False)
    pack_pages(doc, "Pumpkin Puppet: Mouth, Arms & Shoes", "Glue the mouth under the flap of the bag.",
               [(A.mouth("smile"), 220), (A.puppet_arm(), 260), (A.puppet_arm(), 260, True),
                (A.shoe(), 130), (A.shoe(), 130, True), (A.hair_bow(), 110), (A.bow_tie(), 110)], double=False)
    writing_page(doc, "My Pumpkin Puppet", "What will your puppet say?", "Hello! My name is")


PUP = Art()
PUP.rect(-30, -44, 60, 92, 3, "tan")
PUP.add(A.puppet_arm(), dx=-40, dy=8, s=0.4, flip=True)
PUP.add(A.puppet_arm(), dx=40, dy=8, s=0.4)
PUP.add(A.shirt("orange3"), dx=0, dy=16, s=0.55)
PUP.add(A.mouth("smile"), dx=0, dy=-12, s=0.36)
PUP.add(assembled([(A.eye("happy"), -15, -2, 20), (A.eye("happy"), 15, -2, 20, True),
                   (A.nose("triangle"), 0, 12, 13)], base=A.pumpkin(ribs=False)), dx=0, dy=-36, s=0.6)
PUP.add(A.shoe(), dx=-14, dy=50, s=0.3, flip=True)
PUP.add(A.shoe(), dx=14, dy=50, s=0.3)
add(49, "Pumpkin Paper Bag Puppet", _puppet_build, example_of(PUP),
    ["Oral language and storytelling", "Following directions", "Fine-motor cutting and gluing"],
    ["Colour all the puppet pieces.",
     "Cut them out along the thick lines.",
     "Glue the pumpkin head on the bottom flap of a paper lunch bag.",
     "Lift the flap and glue the mouth underneath so it 'talks' when the flap moves.",
     "Glue the body on the bag, add the arms and shoes, then put on a puppet show!"],
    "Use the puppets to retell a pumpkin story or practise a fall poem.",
    materials=["Paper lunch bags (1 per student)", "Crayons", "Scissors", "Glue stick"], grades="PreK - 2")

# ===========================================================================
# 50 Masks
# ===========================================================================
MASKS = [("Pumpkin Mask", A.mask_pumpkin, (-16, -6)), ("Black Cat Mask", A.mask_cat, (-17, -4)),
         ("Owl Mask", A.mask_owl, (-20, -4)), ("Bat Mask", A.mask_bat, (-15, 2))]


def _mask_page(c, R, name, fn, eye):
    y = L.header(c, R, name, "Colour, cut out the mask and the eye holes, then tie on a string or glue on a craft stick.")
    S = 500
    X, Y = PAGE_W / 2, (y + 60) / 2 + 20
    R.draw(fn(), X, Y, S)
    k = S / 100
    c.saveState()
    L.ink(c)
    for sx in (-1, 1):
        ex, ey = X + sx * abs(eye[0]) * k, Y - eye[1] * k
        c.setFillColorRGB(1, 1, 1)
        c.setLineWidth(1.6)
        c.setDash(5, 3)
        c.ellipse(ex - 8.5 * k, ey - 6 * k, ex + 8.5 * k, ey + 6 * k, stroke=1, fill=1)
        c.setDash()
        c.setFillColorRGB(0.14, 0.12, 0.13)
        c.circle(X + sx * 44 * k, Y - eye[1] * k, 4, stroke=1, fill=0)
    c.restoreState()
    for sx in (-1, 1):
        L.text(c, "cut", X + sx * abs(eye[0]) * k, Y - eye[1] * k - 4, 11, "Body", color=(0.55, 0.55, 0.55))
    L.text(c, "Punch the small holes and tie on yarn, or tape a craft stick to one side.", PAGE_W / 2, 56, 11, "Body")


def _masks_build(doc):
    for name, fn, eye in MASKS:
        c = doc.page()
        _mask_page(c, doc.R, name, fn, eye)


def _masks_example(c, R, x, y, size):
    for i, (_, fn, _) in enumerate(MASKS):
        R.draw(fn(), x + (i % 2 - 0.5) * size * 0.5, y + (0.5 - i // 2) * size * 0.46, size * 0.46)


add(50, "Fall Friends Masks", _masks_build, _masks_example,
    ["Dramatic play and oral language", "Fine-motor cutting (inside cuts)", "Fall and Halloween celebration"],
    ["Print on cardstock. Students choose a mask and colour it.",
     "Cut out the mask. An adult cuts out the eye holes (fold the paper gently to start the cut).",
     "Punch the small side holes and tie on yarn, or tape a craft stick to one side.",
     "Wear the masks for a fall parade, a play or a costume-free Halloween party!"],
    "Masks with a craft stick are easier to take on and off and are a good fit for schools with costume rules.",
    materials=["Cardstock", "Crayons or markers", "Scissors", "Hole punch and yarn, or craft sticks"],
    grades="PreK - 3")
