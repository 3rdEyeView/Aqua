// usage: node shoot.js outdir url... ; full-page screenshots at 1440 and 390
const { chromium } = require('playwright');
(async () => {
  const [out, ...urls] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const u of urls) for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: w > 500 ? 900 : 844 }, deviceScaleFactor: 1 });
    await p.goto(u, { waitUntil: 'networkidle', timeout: 60000 });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); } window.scrollTo(0, 0); });
    await p.waitForTimeout(800);
    const name = (new URL(u).pathname.replace(/\//g, '') || 'home') + '-' + w;
    await p.screenshot({ path: `${out}/${name}.png`, fullPage: true });
    await p.screenshot({ path: `${out}/${name}-fold.png` });
    console.log(name, await p.evaluate(() => document.documentElement.scrollWidth));
    await p.close();
  }
  await b.close();
})();
