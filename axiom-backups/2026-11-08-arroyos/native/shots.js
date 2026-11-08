// node shots.js <url> <prefix>  → fold + full screenshots at desktop 1440 and iPhone 13, plus slices of the full pages
const { chromium, devices } = require('playwright');
(async () => {
  const [url, out] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const [name, opts] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['iphone', devices['iPhone 13']]]) {
    const c = await b.newContext({ ...opts, deviceScaleFactor: 1 }); const p = await c.newPage();
    await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
    await p.waitForTimeout(2500);
    await p.screenshot({ path: `${out}-${name}-fold.jpg`, quality: 75 });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 150)); } window.scrollTo(0, 0); });
    await p.waitForTimeout(2500);
    await p.screenshot({ path: `${out}-${name}-full.jpg`, fullPage: true, quality: 65 });
    const m = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h: document.body.scrollHeight }));
    console.log(name, JSON.stringify(m));
    await c.close();
  }
  await b.close();
})();
