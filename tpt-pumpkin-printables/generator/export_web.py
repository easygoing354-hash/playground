"""Export the shared art library + fonts for the Pumpkin Patch Pals web app.

    python3 export_web.py   ->  ../../pumpkin-patch-pals/art.js and fonts/*.woff2
"""
import json
import os

import art as A
from engine import Art, bbox, to_svg

APP = os.path.join(os.path.dirname(__file__), "..", "..", "pumpkin-patch-pals")


def entry(a, size=None):
    x0, y0, x1, y1 = bbox(a)
    view = f"{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}"
    svg = to_svg(a, color=True, view=view)
    d = {"svg": svg, "x0": round(x0, 1), "y0": round(y0, 1), "w": round(x1 - x0, 1), "h": round(y1 - y0, 1)}
    if size:
        d["size"] = size
    return d


ART = {}

# --- decorate-a-pumpkin parts: (category, key, art, size in pumpkin units, default x, y) ------
PARTS = []


def part(cat, key, a, size, x=0, y=0, pair=False):
    ART[key] = entry(a, size)
    PARTS.append({"cat": cat, "key": key, "size": size, "x": x, "y": y, "pair": pair})


for k in ["triangle", "round", "happy", "star", "heart", "angry", "googly", "cute", "cat", "owl", "moon",
          "sleepy", "square", "spiral", "wink", "x"]:
    part("eyes", f"eye-{k}", A.eye(k, "yellow" if k == "cat" else "dark"), 24 if k == "owl" else 20,
         -15, -2, pair=True)
for k in ["triangle", "down", "circle", "heart", "button", "pig", "star", "cat", "square"]:
    part("noses", f"nose-{k}", A.nose(k), 13, 0, 12)
for k in ["grin", "smile", "zigzag", "vampire", "tongue", "buck", "monster", "stitch", "o", "cat", "frown", "wavy"]:
    part("mouths", f"mouth-{k}", A.mouth(k), 36 if k not in ("o", "cat") else 26, 0, 27)
for key, a, s, x, y, pair in [
        ("witch-hat", A.witch_hat(), 62, 0, -46, False), ("top-hat", A.top_hat(), 44, 0, -46, False),
        ("crown", A.crown(), 44, 0, -44, False), ("pirate-hat", A.pirate_hat(), 64, 0, -44, False),
        ("farmer-hat", A.farmer_hat(), 68, 0, -42, False), ("hair-bow", A.hair_bow(), 28, 22, -32, False),
        ("bow-tie", A.bow_tie(), 34, 0, 46, False), ("glasses", A.glasses(), 56, 0, -2, False),
        ("mustache", A.mustache(), 30, 0, 18, False), ("cat-ear", A.cat_ear(), 30, -26, -34, True),
        ("horn", A.horn(), 26, -27, -34, True), ("unicorn-horn", A.unicorn_horn(), 30, 0, -46, False),
        ("antenna", A.antenna(), 30, 0, -50, False), ("hero-mask", A.hero_mask(), 62, 0, -2, False),
        ("eye-patch", A.eye_patch(), 40, -15, -4, False), ("cheek", A.cheek(), 10, -25, 12, True),
        ("bat-wing", A.bat_wing(), 56, 46, -6, True), ("owl-tuft", A.owl_tuft(), 28, -26, -34, True),
        ("feather", A.feather("red"), 34, 30, -40, False), ("flower", A.flower(), 16, 22, -30, False),
        ("whiskers", A.whiskers(), 50, 0, 13, False), ("bandage", A.bandage(), 80, 0, -18, False),
        ("leaf-piece", A.maple_leaf(), 20, -30, 30, False), ("spider-piece", A.spider(), 24, 34, 20, False)]:
    part("extras", key, a, s, x, y, pair)

# --- pictures used by the games ------------------------------------------------------------
PICS = {
    "pumpkin": A.pumpkin(), "pumpkin-plain": A.pumpkin(ribs=False, vine=False, leaf=False),
    "pumpkin-template": A.pumpkin(ribs=False), "mini": A.mini_pumpkin(), "seed": A.pumpkin_seed(),
    "maple": A.maple_leaf(), "oak": A.oak_leaf(), "leaf": A.simple_leaf(), "acorn": A.acorn(), "apple": A.apple(),
    "ghost": A.ghost(), "bat": A.bat(), "cat": A.black_cat(), "owl": A.owl(), "spider": A.spider(),
    "web": A.spider_web(), "moon": A.moon(), "star": A.star(), "hat": A.top_hat(), "witch": A.witch_hat(),
    "candy-corn": A.candy_corn(), "corn": A.corn(), "sunflower": A.sunflower(), "mushroom": A.mushroom(),
    "house": A.haunted_house(), "cauldron": A.cauldron(), "broom": A.broom(), "rake": A.rake(), "cake": A.cake(),
    "car": A.car(), "spoon": A.spoon(), "bee": A.bee(), "tree": A.tree(), "bug": A.bug(), "mug": A.mug(),
    "pie": A.pie_slice(), "hay": A.hay_bale(), "crow": A.crow(), "scarecrow": A.scarecrow_head(),
    "sprout": A.sprout(), "vine": A.vine_plant(), "pumpkin-flower": A.pumpkin_flower(),
    "green-pumpkin": A.green_pumpkin(), "jack": A.pumpkin_face(), "jack-glow": A.pumpkin_face(glow=True),
    "fall-tree": A.fall_tree(),
}
for name, body, back in [("orange", "orange", "orange2"), ("green", "green", "olive"), ("white", "cream", "lgray"),
                         ("purple", "purple", "purple2"), ("teal", "teal", "#1f8a7e"), ("pink", "pink", "#e486a6")]:
    PICS[f"base-{name}"] = A.pumpkin(body=body, back=back)
for name in A.EMOTIONS + ["scared", "proud"]:
    p = Art().add(A.pumpkin(ribs=False, vine=False)).add(A.emotion_face(name), dy=6, s=0.6)
    PICS[f"feel-{name}"] = p
for k, a in PICS.items():
    ART[k] = entry(a)


def subset_fonts():
    from fontTools import subset
    src = os.path.join(os.path.dirname(__file__), "..", "fonts")
    out = os.path.join(APP, "fonts")
    os.makedirs(out, exist_ok=True)
    text = "".join(chr(i) for i in range(32, 127)) + "’‘“”•—–é©…·"
    for f, name in [("Sniglet-ExtraBold.ttf", "sniglet-extrabold.woff2"), ("Andika-Regular.ttf", "andika.woff2"),
                    ("Andika-Bold.ttf", "andika-bold.woff2")]:
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga"]
        fnt = subset.load_font(os.path.join(src, f), opts)
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(fnt)
        subset.save_font(fnt, os.path.join(out, name), opts)
    for lic in ["OFL-Sniglet.txt", "OFL-Andika.txt"]:
        with open(os.path.join(src, lic)) as r, open(os.path.join(out, lic), "w") as w:
            w.write(r.read())


if __name__ == "__main__":
    os.makedirs(APP, exist_ok=True)
    with open(os.path.join(APP, "art.js"), "w") as f:
        f.write("// Generated by tpt-pumpkin-printables/generator/export_web.py - do not edit by hand.\n")
        f.write("// Original artwork (c) Pumpkin Patch Pals. Shared with the printable PDF set.\n")
        f.write("window.ART = " + json.dumps(ART, separators=(",", ":")) + ";\n")
        f.write("window.PARTS = " + json.dumps(PARTS, separators=(",", ":")) + ";\n")
    subset_fonts()
    print(len(ART), "art entries,", len(PARTS), "parts;",
          os.path.getsize(os.path.join(APP, "art.js")) // 1024, "KB")
