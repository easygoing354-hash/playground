# Daily Checklist

A small, private daily habit tracker. Tap a goal each time you do it, keep your
streak alive, and jot an optional diary note. One HTML file, no build step, no
account, no tracking.

## Features

- Tap-to-count goals (tap again for ×2, ×3…; **−** to undo)
- Progress ring, current streak, best streak and perfect-day count
- 30-day heatmap and a history list — tap any day to view or fix it
- Optional diary per day
- Spanish "palabra del día"
- Works offline and installs to your home screen (PWA)
- Export / import a JSON backup to move between devices

## Privacy

Everything is stored in your browser's `localStorage` on your device. Nothing is
sent to a server. Clearing site data deletes your history, so export a backup
now and then.

## Run it

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

Then visit <http://localhost:8000>. Offline mode and "Install app" need
`localhost` or HTTPS (for example GitHub Pages).

## Make it yours

Edit the `ITEMS` list near the top of the `<script>` in `index.html`:

```js
const ITEMS = [
  { id:"read",  label:"Read" },
  { id:"walk",  label:"Power / long walk" },
  { id:"code",  label:"Build something", since:"2026-11-06" },
];
```

- `id` is the key saved with your history — don't rename it once you've used it.
- `since` (optional) makes a new goal count only from that date, so older
  perfect days stay perfect.

Swap the `WORDS` list for any vocabulary you're learning. If you change the
icons or `sw.js`, bump `VERSION` in `sw.js` so installed copies update.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole app |
| `manifest.webmanifest` | Install metadata |
| `sw.js` | Offline cache |
| `icon-*.png`, `apple-touch-icon.png` | App icons |

## License

[MIT](LICENSE) — free to use, change and share.
