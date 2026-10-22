// Dump every line the app can speak:  node voice_catalog.js <app dir> <out.json>
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  await p.goto('file://' + process.argv[2] + '/index.html');
  await p.waitForSelector('.tile');
  const cat = await p.evaluate(() => window.PPP_SPEECH_CATALOG());
  fs.writeFileSync(process.argv[3], JSON.stringify(cat, null, 1));
  console.log(cat.length, 'lines');
  await b.close();
})();
