# Christmas Communication Labels

A printable TPT resource: Christmas picture cards and visual supports for autistic learners and AAC users.

- `dist/Christmas-Communication-Labels.pdf`: the 23-page product file (US Letter)
- `dist/thumbnail.png`: square cover image for the TPT listing
- `LISTING.md`: title, description, grades and tags for the TPT listing

## Rebuilding

```
node build.js
```

- `icons.js` holds the illustrations. All of them are original SVG artwork drawn for this product.
- `build.js` holds the card lists, the page layouts and the PDF/PNG export. It uses the Playwright build that is already installed.
- To add, rename or reorder words, edit `CATS` in `build.js`. A new word also needs a matching icon in `icons.js`.

Fonts: Andika and Fredoka (SIL Open Font License, which allows embedding them in a commercial PDF).
