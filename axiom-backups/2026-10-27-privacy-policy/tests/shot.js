// Screenshots of a URL at desktop/tablet/mobile + basic checks: node shot.js <url> <prefix>
const { chromium } = require('playwright');
(async () => {
  const [url, prefix] = process.argv.slice(2); const b = await chromium.launch();
  for (const w of [1440, 900, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } }); const errs = [];
    p.on('pageerror', e => errs.push(e.message)); await p.route(/google|doubleclick|leadconnectorhq/, r => r.abort());
    const r = await p.goto(url, { waitUntil: 'networkidle' });
    const info = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, h1: document.querySelector('h1')?.innerText, h2: document.querySelectorAll('h2').length,
      bodyFont: getComputedStyle(document.querySelector('#policy p') || document.body).fontFamily.slice(0, 40), p: document.querySelectorAll('#policy p').length }));
    await p.screenshot({ path: `shots/${prefix}-${w}.png`, fullPage: true });
    console.log(w, r.status(), JSON.stringify(info), 'errors', errs.length); await p.close();
  }
  await b.close();
})();
