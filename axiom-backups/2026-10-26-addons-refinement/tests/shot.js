// Full-page screenshots of a URL at several widths: node shot.js <url> <prefix>
const { chromium } = require('playwright');
(async () => {
  const [url, prefix] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const w of [1440, 1024, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.route(/google|doubleclick|gtag/, r => r.abort());
    await p.goto(url, { waitUntil: 'networkidle' });
    await p.screenshot({ path: `shots/${prefix}-${w}.png`, fullPage: true });
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    console.log(w, 'scrollWidth', sw, 'height', await p.evaluate(() => document.body.scrollHeight));
    await p.close();
  }
  await b.close();
})();
