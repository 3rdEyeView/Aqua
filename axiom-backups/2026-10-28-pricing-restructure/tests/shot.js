// Screenshots of a URL at given widths, with overflow + JS error check: node shot.js <url> <prefix> [widths]
const { chromium } = require('playwright');
(async () => {
  const [url, prefix, ws] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const w of (ws || '1440,390').split(',').map(Number)) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.route(/google|doubleclick|gtag|leadconnector/, r => r.abort());
    await p.goto(url, { waitUntil: 'networkidle' });
    await p.screenshot({ path: `shots/${prefix}-${w}.png`, fullPage: true });
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    console.log(w, 'scrollWidth', sw, 'height', await p.evaluate(() => document.body.scrollHeight), 'jsErrors', errs);
    await p.close();
  }
  await b.close();
})();
