const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1280, height: 860 } }); const errs = [];
  p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => m.type() === 'error' && errs.push(m.text()));
  p.on('request', (r) => { if (!r.url().startsWith('file:') && !r.url().startsWith('data:')) errs.push('external request: ' + r.url()); });
  await p.goto('file://' + process.argv[2]);
  await p.waitForSelector('.tile');
  const n = await p.$$eval('.tile', (t) => t.length);
  for (const id of await p.$$eval('.tile', (t) => t.map((x) => x.dataset.id))) {
    await p.click('#homeBtn'); await p.click(`.tile[data-id="${id}"]`); await p.waitForTimeout(250);
  }
  await p.click('#homeBtn'); await p.click('.tile[data-id="decorate"]'); await p.click('#surprise'); await p.waitForTimeout(200);
  const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 5000 }).catch(() => null), p.click('#savePng')]);
  const fonts = await p.evaluate(async () => { await document.fonts.ready; return document.fonts.check('800 20px Sniglet'); });
  await p.screenshot({ path: process.argv[3] });
  console.log({ tiles: n, sniglet: fonts, savedPng: !!dl, errors: errs.length ? errs : 'none' });
  await b.close();
})();
