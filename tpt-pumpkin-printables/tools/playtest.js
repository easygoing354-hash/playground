const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  await p.addInitScript(() => {
    window.__plays = []; window.__deviceSpeech = [];
    const orig = HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.play = function () {
      const el = this; const r = orig.call(this);
      r.then(() => window.__plays.push('ok'), (e) => window.__plays.push('blocked:' + e.name));
      el.addEventListener('ended', () => window.__plays.push('ended ' + el.duration.toFixed(2) + 's'), { once: true });
      return r;
    };
    speechSynthesis.speak = (u) => window.__deviceSpeech.push(u.text);
  });
  await p.goto(process.argv[2]);
  await p.waitForFunction(() => !!window.VOICE);
  await p.click('.tile[data-id="letters"]');
  await p.waitForTimeout(4500);
  await p.click('.say');
  await p.waitForTimeout(4500);
  console.log(await p.evaluate(() => ({ plays: window.__plays, deviceFallback: window.__deviceSpeech })));
  await b.close();
})();
