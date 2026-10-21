"""Build all printable PDFs:  python3 build.py [num ...]"""
import os
import re
import sys

import kit
import layout as L
import products_faces
try:
    import products_learn
    LEARN = products_learn.PRODUCTS
except ImportError:
    LEARN = []

OUT = os.path.join(os.path.dirname(__file__), "..", "pdfs")
PRODUCTS = sorted(products_faces.PRODUCTS + LEARN, key=lambda p: p["num"])


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")


def dry_run(prod):
    """Build once in memory to learn the student page titles for the 'What's inside' box."""
    import io
    doc = kit.Doc(io.BytesIO(), prod)
    doc.page()
    L.PAGE_LOG.clear()
    prod["build"](doc)
    prod["contents"] = list(L.PAGE_LOG)


def build(prod):
    os.makedirs(OUT, exist_ok=True)
    dry_run(prod)
    path = os.path.join(OUT, f"{prod['num']:02d}-{slug(prod['title'])}.pdf")
    doc = kit.Doc(path, prod)
    c = doc.page()
    L.teacher_page(c, prod, prod["example"])
    prod["build"](doc)
    c = doc.page()
    L.terms_page(c, prod)
    doc.save()
    return path, doc.count


if __name__ == "__main__":
    want = {int(a) for a in sys.argv[1:]}
    for p in PRODUCTS:
        if want and p["num"] not in want:
            continue
        path, n = build(p)
        print(f"{os.path.basename(path):55s} {n:2d} pages")
    print(len(PRODUCTS), "products defined")
