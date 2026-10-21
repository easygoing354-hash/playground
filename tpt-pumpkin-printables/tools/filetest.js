const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage(); const errs = [];
  p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => m.type() === 'error' && errs.push(m.text()));
  await p.goto('file://' + process.argv[2] + '/index.html');
  await p.waitForSelector('.tile'); await p.click('.tile[data-id="count"]'); await p.waitForTimeout(500);
  await p.evaluate(() => document.fonts.ready);
  const fonts = await p.evaluate(() => [document.fonts.check('800 20px Sniglet'), document.fonts.check('20px Andika')]);
  console.log('fonts loaded:', fonts, 'errors:', errs.length ? errs : 'none');
  await b.close();
})();
