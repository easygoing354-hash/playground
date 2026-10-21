// Render the app icons from art.js:  node icons.js <app dir>
const path = require('path');
const { chromium } = require('playwright');
const dir = path.resolve(process.argv[2]);
global.window = {};
require(path.join(dir, 'art.js'));
const svg = window.ART['jack-glow'].svg;
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
  const page = await browser.newPage();
  for (const [name, size, pad, round] of [['icon-512.png', 512, 0.1, 0.22], ['icon-192.png', 192, 0.1, 0.22],
    ['icon-maskable-512.png', 512, 0.2, 0], ['apple-touch-icon.png', 180, 0.12, 0]]) {
    await page.setViewportSize({ width: size, height: size });
    await page.setContent(`<html><body style="margin:0"><div style="width:${size}px;height:${size}px;background:radial-gradient(circle at 70% 20%,#5a3f7a,#2a2148);border-radius:${round * 100}%;display:flex;align-items:center;justify-content:center"><div style="width:${size * (1 - 2 * pad)}px;height:${size * (1 - 2 * pad)}px">${svg.replace('<svg ', '<svg width="100%" height="100%" ')}</div></div></body></html>`);
    await page.screenshot({ path: path.join(dir, name), omitBackground: round > 0 });
  }
  await browser.close();
})();
