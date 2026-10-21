"""Products 1-22: build-a-pumpkin face & character crafts (cut, colour, glue onto a pumpkin)."""
import math
import art as A
from engine import Art
import kit
from kit import K, pack_pages, template_page, writing_page, assembled, example_of
import layout as L

PRODUCTS = []

CRAFT_SKILLS = ["Fine-motor cutting and gluing", "Following multi-step directions",
                "Creative expression and spatial reasoning"]
CRAFT_STEPS = [
    "Colour the pumpkin template and all of the pieces. Or skip the colouring: print the pumpkin on orange paper.",
    "Cut out the pumpkin and each piece along the thick black lines.",
    "Lay the pieces on the pumpkin to plan the face before gluing. There is no wrong answer!",
    "Glue the pieces in place. Pieces may hang over the edge of the pumpkin.",
    "Complete the draw-and-write page, then glue the craft on top of it for a hallway display.",
]


def face(eyes="triangle", nose="triangle", mouth="grin", fill="dark", es=20, ns=13, ms=36,
         eye_y=-2, nose_y=12, mouth_y=27):
    return [(A.eye(eyes, fill), -15, eye_y, es, False), (A.eye(eyes, fill), 15, eye_y, es, True),
            (A.nose(nose, fill), 0, nose_y, ns), (A.mouth(mouth, fill), 0, mouth_y, ms)]


def pieces_from(parts, k=K):
    out = []
    for p in parts:
        art, dx, dy, su = p[:4]
        flip = p[4] if len(p) > 4 else False
        rot = p[5] if len(p) > 5 else 0
        out.append((art, su * k, flip, 0))
    return out


def craft(num, title, parts, extras=(), behind=(), prompt=None, starter=None, skills=None,
          steps=None, tip=None, grades="PreK - 2", sub=None, extra_pages=None, pieces_title=None,
          template_title=None, wtitle=None):
    composite = assembled(parts, behind)

    def build(doc):
        template_page(doc, template_title or title, sub or "Colour me, cut me out, then glue on the pieces!")
        pcs = pieces_from(behind) + pieces_from(parts) + list(extras)
        pack_pages(doc, pieces_title or f"{title}: Pieces", "Colour and cut out the pieces.", pcs)
        if extra_pages:
            extra_pages(doc)
        if prompt:
            writing_page(doc, wtitle or f"My {title}", prompt, starter)

    PRODUCTS.append(dict(num=num, title=title, build=build, example=example_of(composite),
                         skills=skills or CRAFT_SKILLS, steps=steps or CRAFT_STEPS, tip=tip,
                         grades=grades, composite=composite))


def ex_pieces(art_list, su, flip_pairs=False):
    out = []
    for a in art_list:
        out.append((a, su * K, False, 0))
        if flip_pairs:
            out.append((a, su * K, True, 0))
    return out


# ---------------------------------------------------------------------------
# 1 Classic jack-o'-lantern (+ black ready-to-cut set)
# ---------------------------------------------------------------------------

def _classic_black(doc):
    pcs = []
    for k in ["triangle", "round", "happy", "angry"]:
        pcs += [(A.eye(k, "ink"), 20 * K), (A.eye(k, "ink"), 20 * K, True)]
    pcs += [(A.nose(k, "ink"), 13 * K) for k in ["triangle", "down", "circle"]]
    pcs += [(A.mouth(k, "ink"), 36 * K) for k in ["grin", "smile", "zigzag"]]
    pack_pages(doc, "Jack-o'-Lantern Pieces (no-colour set)",
               "Already black! Just cut out the pieces and glue them on.", pcs)


craft(1, "Build a Jack-o'-Lantern", face("triangle", "triangle", "grin"),
      extras=ex_pieces([A.eye("round"), A.eye("happy"), A.eye("angry")], 20, True)
      + ex_pieces([A.nose("down"), A.nose("circle")], 13)
      + ex_pieces([A.mouth("smile"), A.mouth("zigzag")], 36),
      extra_pages=_classic_black,
      wtitle="My Jack-o'-Lantern", prompt="What does your jack-o'-lantern look like?", starter="My jack-o'-lantern is",
      tip="For a quick no-colour version, print the template on orange paper and use the black pieces page.")

# 2 Silly faces
craft(2, "Silly Pumpkin Faces",
      face("googly", "pig", "buck", es=22, ns=17),
      extras=ex_pieces([A.eye("spiral"), A.eye("cute")], 22, True)
      + ex_pieces([A.mouth("tongue"), A.mouth("wavy")], 36)
      + ex_pieces([A.mustache()], 34) + ex_pieces([A.glasses()], 54) + ex_pieces([A.nose("button")], 15),
      wtitle="My Silly Pumpkin", prompt="Make your pumpkin as silly as you can!", starter="My pumpkin is silly because",
      tip="Read a silly fall picture book first. Then let students vote for the silliest pumpkin!")

# 3 Spooky faces
craft(3, "Spooky Pumpkin Faces",
      [(A.eye("angry"), -15, -2, 20), (A.eye("angry"), 15, -2, 20, True), (A.nose("down"), 0, 12, 13),
       (A.mouth("monster"), 0, 28, 40)],
      extras=ex_pieces([A.eye("moon"), A.eye("x"), A.eye("cat")], 20, True)
      + ex_pieces([A.mouth("vampire"), A.mouth("stitch"), A.mouth("zigzag")], 36)
      + ex_pieces([A.brow(), A.brow()], 18),
      wtitle="My Spooky Pumpkin", prompt="Is your pumpkin spooky or silly-spooky?", starter="My spooky pumpkin says",
      tip="Turn the finished pumpkins into a 'Guess Whose Pumpkin?' game with names hidden on the back.")

# 4 Cute / kawaii
craft(4, "Cute Pumpkin Faces",
      [(A.eye("cute"), -15, -2, 18), (A.eye("cute"), 15, -2, 18, True), (A.nose("heart"), 0, 10, 9),
       (A.mouth("cat"), 0, 19, 26), (A.cheek(), -25, 12, 10), (A.cheek(), 25, 12, 10),
       (A.hair_bow(), 22, -32, 28, False, 15)],
      extras=ex_pieces([A.eye("heart"), A.eye("happy"), A.eye("star")], 18, True)
      + ex_pieces([A.mouth("smile")], 30) + ex_pieces([A.nose("circle")], 10),
      wtitle="My Cute Pumpkin", prompt="Give your pumpkin a name!", starter="My pumpkin's name is",
      tip="Pink cheeks look great with a little cotton ball of crayon shavings rubbed on.")


# ---------------------------------------------------------------------------
# 5 Feelings pumpkins (SEL)
# ---------------------------------------------------------------------------

def _feelings_build(doc):
    c = doc.page()
    y = L.header(c, doc.R, "Pumpkin Feelings", "Cut out the faces. Glue each face on the pumpkin with the same feeling word.")
    cols, rows = 3, 2
    w, h = L.PAGE_W - 2 * L.M, y - 50
    cw, ch = w / cols, h / rows
    for i, emo in enumerate(A.EMOTIONS):
        cx = L.M + (i % cols + 0.5) * cw
        cy = y - (i // cols + 0.5) * ch
        kit.draw_fit(doc.R, A.pumpkin(ribs=False, vine=False), cx, cy + 14, cw * 0.92, ch * 0.78)
        L.glue_box(c, cx - 48, cy - 16, 96, 62, None)
        L.fit_text(c, emo, cx, cy - ch / 2 + 6, cw - 10, 22, "Head")
    order = [3, 0, 5, 1, 4, 2]
    kit.card_grid(doc, "Feeling Faces", "Colour and cut out each face card (2 sets per page).",
                  [A.emotion_face(A.EMOTIONS[i]) for i in order] * 2, 3, 4, art_frac=0.62)
    c = doc.page()
    y = L.header(c, doc.R, "Today I Feel...", "Draw a face on the pumpkin to show how you feel today.")
    kit.draw_fit(doc.R, A.pumpkin(ribs=False), L.PAGE_W / 2, y - 200, 400, 380)
    L.text(c, "Today I feel", L.M, y - 430, 20, "Body", "left")
    L.primary_lines(c, L.M, y - 445, L.PAGE_W - 2 * L.M, 2, 60)
    L.text(c, "because", L.M, y - 570, 20, "Body", "left")


def _feelings_example(c, R, x, y, size):
    a = Art()
    for i, emo in enumerate(["happy", "silly", "surprised", "sad"]):
        p = assembled([(A.emotion_face(emo), 0, 6, 60)], base=A.pumpkin(ribs=False, vine=False))
        a.add(p, dx=(i % 2) * 110 - 55, dy=(i // 2) * 110 - 55)
    kit.draw_fit(R, a, x, y, size, size)


PRODUCTS.append(dict(
    num=5, title="Pumpkin Feelings", build=_feelings_build, example=_feelings_example, grades="PreK - 2",
    skills=["Social-emotional learning: naming feelings", "Matching pictures to words",
            "Cutting and gluing", "Expressive writing"],
    steps=["Talk about each feeling word together. Ask students to show the face with their own faces first.",
           "Students colour and cut out the six feeling face cards.",
           "Read each word on the pumpkin page and glue the matching face on top.",
           "Use the 'Today I Feel' page as a morning check-in or calm-down corner activity."],
    tip="Laminate an extra set of face cards and pumpkins for a reusable feelings check-in chart."))

# ---------------------------------------------------------------------------
# 6 Shape pumpkins (math)
# ---------------------------------------------------------------------------


def _shape_record(doc):
    c = doc.page()
    y = L.header(c, doc.R, "Shape Count", "Count the shapes you used. Write the number.")
    kinds = ["circle", "square", "triangle", "rectangle", "oval", "hexagon", "star", "heart"]
    rh = (y - 60) / 4
    for i, k in enumerate(kinds):
        col, row = i % 2, i // 2
        x0 = L.M + col * (L.PAGE_W - 2 * L.M) / 2
        cy = y - (row + 0.5) * rh
        kit.draw_fit(doc.R, A.shape(k, "white"), x0 + 50, cy + 10, 70, 70)
        L.text(c, k, x0 + 50, cy - rh / 2 + 18, 15, "BodyB")
        c.saveState()
        L.ink(c)
        c.setLineWidth(1.5)
        c.roundRect(x0 + 120, cy - 30, 100, 70, 10, stroke=1, fill=0)
        c.restoreState()


craft(6, "Shape Jack-o'-Lanterns",
      [(A.shape("triangle", "dark"), -15, -2, 18), (A.shape("triangle", "dark"), 15, -2, 18),
       (A.shape("circle", "dark"), 0, 12, 10), (A.shape("rectangle", "dark"), 0, 27, 30)],
      extras=[(A.shape(k, "dark"), s * K) for k, s in
              [("circle", 18), ("circle", 18), ("square", 16), ("square", 16), ("oval", 18), ("oval", 18),
               ("hexagon", 16), ("hexagon", 16), ("star", 18), ("star", 18), ("heart", 16), ("heart", 16),
               ("triangle", 12), ("square", 10), ("rectangle", 26), ("semicircle", 30), ("rhombus", 14),
               ("rhombus", 14)]],
      skills=["Identify and name 2D shapes", "Count and record", "Composing shapes to make a picture",
              "Fine-motor cutting"],
      extra_pages=_shape_record, wtitle="My Shape Pumpkin", prompt="Which shapes did you use?", starter="I used",
      steps=["Name each 2D shape on the pieces pages together.",
             "Students colour, then cut out the pumpkin and the shapes they want.",
             "Build a face using only shapes, then glue it down.",
             "Count each kind of shape used and write the numbers on the recording page.",
             "Share: 'My pumpkin has 2 triangles and 1 circle.'"],
      tip="Challenge early finishers to make a face using exactly 5 shapes.")

# ---------------------------------------------------------------------------
# 7 Dress-up accessories
# ---------------------------------------------------------------------------
craft(7, "Pumpkin Dress-Up",
      [(A.top_hat(), 0, -44, 44), (A.eye("round"), -15, -2, 16), (A.eye("round"), 15, -2, 16, True),
       (A.glasses(), 0, -2, 56), (A.mustache(), 0, 18, 30), (A.mouth("smile"), 0, 29, 28),
       (A.bow_tie(), 0, 46, 34)],
      extras=ex_pieces([A.witch_hat()], 56) + ex_pieces([A.crown()], 46) + ex_pieces([A.hair_bow()], 30)
      + ex_pieces([A.nose("triangle")], 12) + ex_pieces([A.eye("triangle")], 18, True),
      wtitle="My Dressed-Up Pumpkin", prompt="Where is your pumpkin going all dressed up?", starter="My pumpkin is going to",
      tip="Pair with a fall dress-up day: students design a pumpkin that matches their own outfit.")

# ---------------------------------------------------------------------------
# 8 Real pumpkin glue-on kit (3 sizes, no template)
# ---------------------------------------------------------------------------


def _real_build(doc):
    for label, k in [("Small", 1.7), ("Medium", 2.6), ("Large", 3.6)]:
        pcs = []
        for e in ["triangle", "round"]:
            pcs += [(A.eye(e, "ink"), 20 * k), (A.eye(e, "ink"), 20 * k, True)]
        pcs += [(A.nose("triangle", "ink"), 13 * k), (A.nose("circle", "ink"), 13 * k)]
        pcs += [(A.mouth("grin", "ink"), 36 * k), (A.mouth("smile", "ink"), 36 * k)]
        pack_pages(doc, f"Real Pumpkin Face Kit: {label}",
                   "Cut out the pieces and glue or tape them onto a real pumpkin or gourd.", pcs)


def _real_example(c, R, x, y, size):
    kit.draw_fit(R, assembled(face("round", "triangle", "grin", "ink"), base=A.pumpkin()), x, y, size, size)


PRODUCTS.append(dict(
    num=8, title="Real Pumpkin Face Kit", build=_real_build, example=_real_example, grades="PreK - 3",
    skills=["Fine-motor cutting", "Estimating size and scale", "No-carve pumpkin decorating"],
    materials=["Real pumpkins, mini pumpkins or gourds", "Scissors",
               "Glue dots, double-sided tape or tacky glue"],
    prep="Print on black cardstock or regular paper (the pieces are already black). Small fits mini "
         "pumpkins, Medium fits a pie pumpkin and Large fits a carving pumpkin.",
    steps=["Choose the page that matches the size of your pumpkin.",
           "Cut out a set of eyes, a nose and a mouth.",
           "Plan the face on the pumpkin before sticking anything down.",
           "Attach with glue dots or tape. No knives needed, so it's safe for little hands!"],
    tip="A no-carve pumpkin patch makes a great class party station or family take-home kit."))

# ---------------------------------------------------------------------------
# 9 Roll a jack-o'-lantern
# ---------------------------------------------------------------------------
ROLL_EYES = ["triangle", "round", "star", "heart", "angry", "googly"]
ROLL_NOSE = ["triangle", "circle", "heart", "down", "square", "star"]
ROLL_MOUTH = ["grin", "smile", "zigzag", "vampire", "o", "tongue"]


def _die(c, x, y, n, s=34):
    c.saveState()
    L.ink(c)
    c.setLineWidth(1.6)
    c.setFillColorRGB(1, 1, 1)
    c.roundRect(x - s / 2, y - s / 2, s, s, 6, stroke=1, fill=1)
    pip = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
           4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
           6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}[n]
    c.setFillColorRGB(0.14, 0.12, 0.13)
    for px, py in pip:
        c.circle(x + px * s * 0.27, y + py * s * 0.27, s * 0.08, stroke=0, fill=1)
    c.restoreState()


def _roll_chart(c, R):
    y = L.header(c, R, "Roll a Jack-o'-Lantern", "Roll a die for the eyes, the nose and the mouth. Then draw or glue them on!", name=False)
    cols = ["", "Eyes", "Nose", "Mouth"]
    x0, cw0, cw = L.M, 70, (L.PAGE_W - 2 * L.M - 70) / 3
    rh = (y - 50 - 30) / 6
    for j, t in enumerate(cols[1:]):
        L.text(c, t, x0 + cw0 + (j + 0.5) * cw, y - 18, 20, "Head")
    y -= 30
    for i in range(6):
        cy = y - (i + 0.5) * rh
        c.saveState()
        L.ink(c)
        c.setLineWidth(1.2)
        c.line(x0, y - i * rh, L.PAGE_W - L.M, y - i * rh)
        c.restoreState()
        _die(c, x0 + cw0 / 2, cy, i + 1)
        R.draw(A.eye(ROLL_EYES[i]), x0 + cw0 + 0.5 * cw - 22, cy, rh * 0.55)
        R.draw(A.eye(ROLL_EYES[i]), x0 + cw0 + 0.5 * cw + 22, cy, rh * 0.55, flip=True)
        R.draw(A.nose(ROLL_NOSE[i]), x0 + cw0 + 1.5 * cw, cy, rh * 0.62)
        R.draw(A.mouth(ROLL_MOUTH[i]), x0 + cw0 + 2.5 * cw, cy, rh * 1.15)


def _roll_build(doc):
    c = doc.page()
    _roll_chart(c, doc.R)
    c = doc.page()
    y = L.header(c, doc.R, "Roll & Draw", "Roll the die and draw what you rolled on each pumpkin.")
    for i in range(4):
        cx = L.M + (i % 2 + 0.5) * (L.PAGE_W - 2 * L.M) / 2
        cy = y - (i // 2 + 0.5) * (y - 40) / 2
        kit.draw_fit(doc.R, A.pumpkin(ribs=False), cx, cy, 240, (y - 60) / 2 - 10)
    template_page(doc, "Roll & Glue Pumpkin", "Roll the die, then cut and glue the matching pieces.")
    pcs = []
    for e in ROLL_EYES:
        pcs += [(A.eye(e), 20 * K), (A.eye(e), 20 * K, True)]
    pcs += [(A.nose(n), 13 * K) for n in ROLL_NOSE]
    pcs += [(A.mouth(m), 36 * K) for m in ROLL_MOUTH]
    pack_pages(doc, "Roll & Glue Pieces", "Cut out only the pieces you roll!", pcs)


PRODUCTS.append(dict(
    num=9, title="Roll a Jack-o'-Lantern", build=_roll_build, example=kit.example_page(_roll_chart),
    grades="K - 2",
    skills=["Subitizing dice patterns 1-6", "Turn-taking and game play", "Drawing and fine-motor skills"],
    materials=["A die (or the web app's dice!)", "Crayons", "Scissors and glue (for the glue version)"],
    steps=["Model one turn: roll for the eyes, find the dots on the chart, then draw the matching eyes.",
           "Roll again for the nose and again for the mouth.",
           "Roll & Draw: draw the face on one of the four pumpkins. Play again!",
           "Roll & Glue: cut out the pieces you rolled and glue them onto the big pumpkin.",
           "Compare: did anyone roll the same face?"],
    tip="Project the roll chart on the board and roll as a whole class for a 5-minute brain break."))

# ---------------------------------------------------------------------------
# 10 - 22 Character pumpkins
# ---------------------------------------------------------------------------
craft(10, "Monster Pumpkin",
      [(A.horn("purple"), -27, -34, 26, False, -25), (A.horn("purple"), 27, -34, 26, True, 25),
       (A.eye("googly"), 0, -4, 26), (A.mouth("monster"), 0, 26, 40)],
      extras=ex_pieces([A.eye_stalk()], 28, True) + ex_pieces([A.eye("googly")], 14, True)
      + ex_pieces([A.horn("leaf")], 22, True),
      prompt="Describe your monster pumpkin.", starter="My monster pumpkin likes to")

craft(11, "Witch Pumpkin",
      [(A.witch_hair(), -42, 0, 34), (A.witch_hair(), 42, 0, 34, True), (A.witch_hat(), 0, -46, 64),
       (A.eye("round"), -15, -2, 18), (A.eye("round"), 15, -2, 18, True), (A.nose("down"), 0, 12, 13),
       (A.mouth("smile"), 0, 26, 32)],
      extras=ex_pieces([A.broom()], 50) + ex_pieces([A.cauldron()], 34),
      prompt="What spell would your witch pumpkin cast?", starter="My witch pumpkin would")

craft(12, "Black Cat Pumpkin",
      [(A.cat_ear(), -26, -34, 30, False, -12), (A.cat_ear(), 26, -34, 30, True, 12),
       (A.eye("cat", "yellow"), -15, -2, 20), (A.eye("cat", "yellow"), 15, -2, 20, True),
       (A.whiskers(), 0, 13, 50), (A.mouth("cat"), 0, 25, 26)],
      prompt="What does your cat pumpkin do at night?", starter="At night my cat pumpkin")

craft(13, "Owl Pumpkin",
      [(A.owl_wing(), -46, 12, 40, True), (A.owl_wing(), 46, 12, 40), (A.owl_tuft(), -26, -34, 28, False, -20),
       (A.owl_tuft(), 26, -34, 28, True, 20), (A.eye("owl"), -15, -2, 26), (A.eye("owl"), 15, -2, 26, True),
       (A.beak(), 0, 15, 16)],
      prompt="Owls say 'Whoo!' What would your owl say?", starter="My owl pumpkin says")

craft(14, "Scarecrow Pumpkin",
      [(A.straw_tuft(), -42, -14, 28, False, -60), (A.straw_tuft(), 42, -14, 28, True, 60),
       (A.farmer_hat(), 0, -42, 70), (A.eye("triangle"), -15, -2, 18), (A.eye("triangle"), 15, -2, 18, True),
       (A.nose("triangle"), 0, 12, 12), (A.mouth("stitch"), 0, 26, 34), (A.patch("leaf"), 26, 22, 12)],
      extras=ex_pieces([A.crow()], 34),
      prompt="How does your scarecrow help the farm?", starter="My scarecrow pumpkin")

craft(15, "Mummy Pumpkin",
      [(A.bandage(), 0, -18, 70, False, -8), (A.bandage(), 4, 20, 86, False, 8), (A.bandage(), -6, 36, 70, False, -6),
       (A.eye("googly"), -15, 0, 20), (A.eye("googly"), 15, 2, 18, True), (A.bandage(), 0, -32, 50, False, 5)],
      extras=ex_pieces([A.bandage(), A.bandage()], 86) + ex_pieces([A.mouth("o")], 20),
      prompt="Where is your mummy pumpkin going?", starter="My mummy pumpkin is going to",
      tip="Hand out real strips of white tissue paper or gauze for a 3D mummy version.")

TURKEY_COLORS = ["red", "orange", "yellow", "rust", "leaf", "purple", "gold"]
craft(16, "Turkey Pumpkin",
      [(A.eye("round"), -13, -6, 16), (A.eye("round"), 13, -6, 16, True), (A.beak(), 0, 8, 13),
       (A.wattle(), 7, 20, 14), (A.turkey_feet(), 0, 52, 30)],
      behind=[(A.feather(col), 52 * math.sin(math.radians(ang)),
               -6 - 52 * math.cos(math.radians(ang)), 38, False, ang)
              for ang, col in zip(range(-75, 76, 25), TURKEY_COLORS)],
      prompt="What are you thankful for?", starter="I am thankful for",
      tip="Write one thing you are thankful for on each feather before gluing.")

craft(17, "Bat Pumpkin",
      [(A.bat_ear(), -18, -38, 22), (A.bat_ear(), 18, -38, 22, True), (A.bat_wing(), 46, -6, 56),
       (A.bat_wing(), -46, -6, 56, True), (A.eye("cute"), -15, -2, 18), (A.eye("cute"), 15, -2, 18, True),
       (A.mouth("vampire"), 0, 24, 30)],
      prompt="Where would your bat pumpkin fly?", starter="My bat pumpkin would fly to")

craft(18, "Unicorn Pumpkin",
      [(A.mane_lock("purple"), -40, -18, 30, False, -20), (A.mane_lock("pink"), -46, 4, 30, False, -35),
       (A.mane_lock("blue"), -40, 24, 28, False, -50), (A.unicorn_ear(), -24, -36, 22, False, -15),
       (A.unicorn_ear(), 24, -36, 22, True, 15), (A.unicorn_horn(), 0, -46, 30),
       (A.flower("pink"), 22, -30, 16), (A.eye("wink"), -15, 0, 18), (A.eye("wink"), 15, 0, 18, True),
       (A.cheek(), -24, 12, 10), (A.cheek(), 24, 12, 10), (A.mouth("smile"), 0, 22, 26)],
      extras=ex_pieces([A.mane_lock("leaf"), A.mane_lock("yellow")], 30) + ex_pieces([A.flower("yellow")], 16),
      prompt="What is your unicorn pumpkin's magic power?", starter="My unicorn pumpkin can")

craft(19, "Pirate Pumpkin",
      [(A.pirate_hat(), 0, -44, 66), (A.eye_patch(), -15, -4, 40), (A.eye("round"), 15, -2, 18, True),
       (A.mustache(), 0, 16, 28), (A.mouth("smile"), 0, 28, 28)],
      extras=ex_pieces([A.bandana()], 60) + ex_pieces([A.mouth("grin")], 32),
      prompt="Where would your pirate pumpkin sail?", starter="Ahoy! My pirate pumpkin")

craft(20, "Robot Pumpkin",
      [(A.antenna(), 0, -50, 30), (A.bolt(), -50, 4, 18), (A.bolt(), 50, 4, 18),
       (A.eye("square", "silver"), -15, -4, 18), (A.eye("square", "silver"), 15, -4, 18),
       (A.robot_mouth(), 0, 26, 36)],
      extras=ex_pieces([A.control_panel()], 32) + ex_pieces([A.eye("googly")], 16, True),
      prompt="What job does your robot pumpkin do?", starter="Beep boop! My robot pumpkin")

craft(21, "Vampire Pumpkin",
      [(A.hair_peak(), 0, -22, 62), (A.eye("round"), -15, 0, 17), (A.eye("round"), 15, 0, 17, True),
       (A.brow(), -15, -12, 16, False, 15), (A.brow(), 15, -12, 16, False, -15),
       (A.mouth("vampire"), 0, 24, 34)],
      behind=[(A.vampire_collar(), 0, 38, 100)],
      prompt="Your vampire pumpkin is friendly! What does it do?", starter="My vampire pumpkin")

craft(22, "Superhero Pumpkin",
      [(A.hero_mask(), 0, -2, 62), (A.mouth("smile"), 0, 24, 30), (A.badge(), 0, 44, 20)],
      behind=[(A.cape(), 0, 22, 110)],
      extras=ex_pieces([A.hero_mask("purple"), A.hero_mask("leaf")], 62) + ex_pieces([A.badge("blue")], 20),
      prompt="What is your superhero pumpkin's power?", starter="My superhero pumpkin can",
      tip="Connect to a kindness unit: a hero pumpkin's superpower can be a kind act.")
