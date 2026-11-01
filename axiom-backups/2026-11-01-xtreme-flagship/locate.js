// prints page y of elements by data-id
const { chromium } = require('playwright');
(async () => {
  const [url, w, ...ids] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: 900 } });
  await p.goto(url, { waitUntil: 'networkidle' });
  for (const id of ids) console.log(id, JSON.stringify(await p.evaluate(id => { const e = document.querySelector(`[data-id="${id}"]`); if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.top + scrollY), Math.round(r.height), Math.round(r.left), Math.round(r.width)]; }, id)));
  await b.close();
})();
