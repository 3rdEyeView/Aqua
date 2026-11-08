// usage: node shoot2.js outdir name url : full-page at 1440 and 390 with lazy images forced
const { chromium } = require('playwright');
(async () => {
  const [out, name, url] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: w > 500 ? 900 : 844 } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await p.evaluate(async () => { document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager');
      for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
      await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 6000); }))); window.scrollTo(0, 0); });
    await p.waitForTimeout(1200);
    await p.screenshot({ path: `${out}/${name}-${w}.png`, fullPage: true });
    const info = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src) }));
    console.log(name, w, JSON.stringify(info), 'errors', errs.length);
    await p.close();
  }
  await b.close();
})();
