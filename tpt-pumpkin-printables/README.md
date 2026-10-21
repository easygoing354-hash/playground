# Pumpkin Patch Pals: TpT pumpkin crafts and activities

Fifty printable fall and Halloween cut, colour and glue resources for PreK-2, plus the **Pumpkin Patch Pals** interactive classroom app (in `../pumpkin-patch-pals/`). It is all original artwork, drawn in code, so you can sell it commercially without clip-art licenses.

| Folder | What it is |
|---|---|
| `pdfs/` | The 50 finished PDFs (247 pages) |
| `tpt-listing/` | Everything for TpT: upload zip, 4 thumbnails, watermarked preview, Start Here guide, listing copy (`LISTING.md`), a CSV for the 50 individual listings, and per-product thumbnails |
| `generator/` | Python source that draws every page |
| `fonts/` | Sniglet, Andika and Creepster (all SIL Open Font License, so commercial use is OK) and their licenses |
| `tools/` | Icon renderer and end-to-end browser test for the app |

## Rebuild everything

Requires Python 3 with `reportlab`, `pypdf`, `Pillow` and `fonttools[woff]`, and `pdftoppm` (poppler).

```bash
cd generator
python3 build.py          # all 50 PDFs  (or: python3 build.py 1 5 16  for selected ones)
python3 export_web.py     # art + fonts for the web app
python3 listing.py        # Start Here guide, thumbnails, preview, CSV, upload zip
```

## Use your own store name

Change `STORE_NAME` (and `YEAR`) at the top of `generator/layout.py`, then run the three commands above. Every footer, terms of use page, credits line and preview watermark updates.

## How it's built

- `engine.py`: a small vector engine. Each drawing is authored once and rendered both to PDF (black-line "colour me" art or full colour) and to SVG for the app.
- `art.py`: the illustration library: pumpkins, 16 eye, 9 nose and 13 mouth styles, hats and accessories, characters, fall items, life-cycle stages, masks and more.
- `layout.py`: page furniture: headers, name lines, cut lines with scissors, primary-ruled writing lines, the teacher page and the terms page.
- `kit.py`: page recipes: auto-packing cut-out pieces (it prints 2 sets per page when they fit), templates, card grids and draw-and-write pages.
- `products_faces.py` (#1-22) and `products_learn.py` (#23-50): the 50 products.

## Testing the app

```bash
cd ..                                  # repo root
python3 -m http.server 8765 &
cd tpt-pumpkin-printables/tools
NODE_PATH=$(npm root -g) node e2e.js http://localhost:8765/pumpkin-patch-pals/ /tmp/shots
```

The test plays every activity through to its end screen, drags and saves a decorated pumpkin, and checks for console errors and phone-width overflow.
