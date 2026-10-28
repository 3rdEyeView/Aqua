// simulate.js <outprefix> <url> <specjson>: render live page, replace element texts in the DOM, screenshot regions (no site writes)
const { chromium } = require('playwright'); const fs = require('fs');
const [out, url, specFile] = process.argv.slice(2); const spec = JSON.parse(fs.readFileSync(specFile));
(async () => {
  const b = await chromium.launch();
  for (const w of [1440, 768, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(url + '?sim=' + Date.now(), { waitUntil: 'load' }); await p.waitForTimeout(1500);
    for (const mode of ['before', 'after']) {
      if (mode === 'after') await p.evaluate(spec => { for (const [id, html] of Object.entries(spec)) { const el = document.querySelector(`[data-interaction-id="${id}"]`); if (el) el.innerHTML = html; else console.log('missing', id); } }, spec);
      await p.waitForTimeout(300);
      const r = await p.evaluate(ids => ids.map(id => { const el = document.querySelector(`[data-interaction-id="${id}"]`); let c = el; for (let i = 0; i < 3 && c.parentElement && c.getBoundingClientRect().height < 380; i++) c = c.parentElement; const b = c.getBoundingClientRect(); return { id, y: b.y + scrollY, h: b.height, elH: el.getBoundingClientRect().height }; }), Object.keys(spec));
      for (const x of r) await p.screenshot({ path: `${out}-${mode}-${w}-${x.id}.png`, fullPage: true, clip: { x: 0, y: Math.max(0, x.y - 16), width: w, height: Math.min(x.h + 32, 1400) } });
      console.log(w, mode, r.map(x => `${x.id} block=${Math.round(x.h)} el=${Math.round(x.elH)}`).join(' | '), 'overflow', await p.evaluate(() => document.documentElement.scrollWidth > innerWidth));
    }
    await p.close();
  }
  await b.close();
})();
