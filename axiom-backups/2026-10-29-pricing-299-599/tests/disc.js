// Screenshot the region around the ad-spend disclaimer at 1440 and 390.
const { chromium } = require('playwright');
(async () => {
  const [url, name] = process.argv.slice(2); const b = await chromium.launch();
  for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.route(/google|doubleclick|gtag|leadconnector/, x => x.abort());
    await p.goto(url, { waitUntil: 'networkidle' });
    const el = p.locator('text=We recommend considering approximately $500/month').first();
    await el.scrollIntoViewIfNeeded(); await p.evaluate(() => window.scrollBy(0, -250));
    const box = await el.boundingBox();
    console.log(name, w, 'visible', await el.isVisible(), 'box', JSON.stringify(box), 'sw', await p.evaluate(() => document.documentElement.scrollWidth));
    await p.screenshot({ path: `disc-${name}-${w}.png` }); await p.close();
  }
  await b.close();
})();
