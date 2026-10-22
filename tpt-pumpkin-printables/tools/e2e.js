// Drive every activity of the web app in headless Chromium.  node e2e.js <url> <outdir>
const { chromium } = require('playwright');
const [url, out] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const errors = [];
  const run = async (vw, vh, tag, full) => {
    const page = await browser.newPage({ viewport: { width: vw, height: vh } });
    await page.addInitScript(() => { window.speechSynthesis && (window.speechSynthesis.speak = () => {}); });
    page.on('pageerror', (e) => errors.push(`${tag} pageerror: ${e.stack}`));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(`${tag} console: ${m.text()}`); });
    await page.goto(url);
    await page.waitForSelector('.tile');
    await page.screenshot({ path: `${out}/${tag}-home.png`, fullPage: true });
    if (!full) { await page.close(); return; }
    const ids = await page.$$eval('.tile', (t) => t.map((x) => x.dataset.id));
    for (const id of ids) {
      await page.goto(url + '#' + id); await page.waitForTimeout(300);
      await page.screenshot({ path: `${out}/${tag}-${id}.png` });
      if (['count', 'add', 'pattern', 'letters', 'sounds', 'rhyme'].includes(id)) {
        for (let r = 0; r < 5; r++) {
          const n = await page.$$eval('.choice', (c) => c.length);
          for (let i = 0; i < n; i++) {
            const btn = (await page.$$('.choice'))[i];
            await btn.click();
            await page.waitForTimeout(150);
            if (await page.$('.choice.right')) break;
          }
          await page.waitForTimeout(1600);
        }
        const done = await page.$('.celebrate');
        if (!done) errors.push(`${id}: did not reach celebration`);
      }
      if (id === 'tenframe') {
        const t = await page.$eval('.prompt b', (b) => +b.textContent);
        for (let i = 0; i < t; i++) await page.click(`.tenframe button[data-i="${i}"]`);
        await page.click('#check'); await page.waitForTimeout(300);
        await page.screenshot({ path: `${out}/${tag}-tenframe-done.png` });
      }
      if (id === 'lifecycle') {
        for (let s = 0; s < 6; s++) { await page.click(`.cards6 .choice[data-i="${s}"]`); await page.waitForTimeout(80); }
        await page.waitForTimeout(2500);
        if (!(await page.$('#again'))) errors.push('lifecycle: not finished');
        await page.screenshot({ path: `${out}/${tag}-lifecycle-done.png` });
      }
      if (id === 'spell') {
        const word = await page.evaluate(() => null);
        await page.screenshot({ path: `${out}/${tag}-spell.png` });
      }
      if (id === 'roll') {
        for (let s = 0; s < 3; s++) { await page.click('#rollBtn'); await page.waitForTimeout(900); }
        await page.screenshot({ path: `${out}/${tag}-roll-done.png` });
      }
      if (id === 'memory') {
        const cards = await page.$$('.mcard');
        await cards[0].click(); await cards[1].click(); await page.waitForTimeout(400);
        await page.screenshot({ path: `${out}/${tag}-memory-flip.png` });
      }
      if (id === 'feelings') {
        await page.click('.feel-grid .choice'); await page.waitForTimeout(300);
        await page.screenshot({ path: `${out}/${tag}-feelings-result.png` });
      }
      if (id === 'decorate') {
        await page.click('#clearAll');
        await page.click('#tray button:nth-child(1)');
        await page.click('.tray-tabs button[data-c="noses"]'); await page.click('#tray button:nth-child(3)');
        await page.click('.tray-tabs button[data-c="mouths"]'); await page.click('#tray button:nth-child(1)');
        await page.click('.tray-tabs button[data-c="extras"]'); await page.click('#tray button:nth-child(1)');
        const part = await page.$('.deco-stage .part:last-child');
        const b = await part.boundingBox();
        await page.mouse.move(b.x + b.width / 2, b.y + b.height / 2); await page.mouse.down();
        await page.mouse.move(b.x + b.width / 2 + 20, b.y + b.height / 2 - 10, { steps: 5 }); await page.mouse.up();
        await page.screenshot({ path: `${out}/${tag}-decorate-built.png` });
        const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 5000 }).catch(() => null), page.click('#savePng')]);
        if (!dl) errors.push('decorate: no download'); else await dl.saveAs(`${out}/${tag}-saved-pumpkin.png`);
        await page.click('#surprise'); await page.waitForTimeout(200);
        await page.screenshot({ path: `${out}/${tag}-decorate-surprise.png` });
      }
    }
    const misses = await page.evaluate(() => window.__voiceMisses);
    const hasVoice = await page.evaluate(() => !!window.VOICE);
    if (!hasVoice) errors.push(`${tag}: voice.js did not load`);
    if (misses.length) errors.push(`${tag}: lines with no recording: ${JSON.stringify([...new Set(misses)])}`);
    await page.close();
  };
  await run(1280, 860, 'desk', true);
  await run(390, 844, 'phone', false);
  const p = await browser.newPage({ viewport: { width: 390, height: 844 } });
  for (const id of ['decorate', 'count', 'lifecycle', 'memory']) { await p.goto(url + '#' + id); await p.waitForTimeout(300); await p.screenshot({ path: `${out}/phone-${id}.png`, fullPage: true }); }
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  if (overflow) errors.push('phone: horizontal overflow on memory');
  await browser.close();
  console.log(errors.length ? errors.join('\n') : 'NO ERRORS');
})();
