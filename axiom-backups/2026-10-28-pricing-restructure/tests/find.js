const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.route(/google|doubleclick|gtag|leadconnector/, x => x.abort());
  await p.goto(process.argv[2] + '?nc=' + Date.now(), { waitUntil: 'networkidle' });
  const r = await p.evaluate((qs) => { const t = document.body.innerText, h = document.documentElement.outerHTML; const o = {};
    for (const q of qs) { let i = t.indexOf(q); o['T:' + q] = i < 0 ? null : t.slice(Math.max(0, i - 80), i + 60);
      let j = h.indexOf(q); o['H:' + q] = j < 0 ? null : h.slice(Math.max(0, j - 200), j + 60); } return o; }, ['$299', 'Axiom Essential\n', 'Axiom Essential ']);
  console.log(JSON.stringify(r, null, 1)); await b.close();
})();
