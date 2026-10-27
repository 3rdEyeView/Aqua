// shots.js <prefix> <url> [clipHeight]: hero screenshots at 1440 and 390 + hero height + overflow
const { chromium } = require('playwright');
(async () => {
  const [prefix, url, clipH] = process.argv.slice(2); const b = await chromium.launch();
  for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(url, { waitUntil: 'load', timeout: 60000 }); await p.waitForTimeout(2500);
    const info = await p.evaluate(() => { const h = document.querySelector('h1'); const sec = h && h.closest('.e-con.e-parent, .e-parent') ; return { h1: h && h.innerText, h1H: h && Math.round(h.getBoundingClientRect().height), secH: sec && Math.round(sec.getBoundingClientRect().height), overflow: document.documentElement.scrollWidth > innerWidth }; });
    console.log(w, JSON.stringify(info));
    await p.screenshot({ path: `${prefix}-${w}.png`, clip: { x: 0, y: 0, width: w, height: +(clipH || 1100) } }).catch(async () => p.screenshot({ path: `${prefix}-${w}.png` }));
    await p.close();
  }
  await b.close();
})();
