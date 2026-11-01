// Live checks: Home has no Aqua Safari on the rendered page; Our Work order Xtreme, Brags, Tile Father, Aqua Safari.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const res = {};
  for (const [name, url] of [['home', 'https://axiomsystems.systems/?nc=' + Date.now()], ['our-work', 'https://axiomsystems.systems/our-work/?nc=' + Date.now()]])
  for (const w of [1440, 1024, 768, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
    const r = await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await p.evaluate(async () => { document.querySelectorAll('img').forEach(i => i.loading = 'eager'); for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); }
      await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 6000); }))); window.scrollTo(0, 0); });
    const d = await p.evaluate(() => { const t = document.body.innerText, h = document.documentElement.outerHTML; const pos = s => t.indexOf(s);
      return { sw: document.documentElement.scrollWidth, aquaText: (t.match(/aqua|safari|jetskiadventure/gi) || []).length, aquaHtml: (h.match(/aqua safari|jetskiadventure|aqua-safari/gi) || []).length,
        order: { xtreme: pos('Xtreme Jet Ski Watersports'), brags: pos('Brags Global'), tile: pos('The Tile Father'), aqua: pos('Aqua Safari Jet Ski Adventures') },
        nums: [...t.matchAll(/\n0([1-4])\n/g)].map(m => m[1]).join(''),
        broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).length,
        links: [...document.querySelectorAll('a')].filter(a => /xtremestpete|jetskiadventure|bragspressure|thetilefather/.test(a.href)).map(a => (a.innerText.trim() || '[img]') + ' -> ' + a.href),
        tileImgs: [...document.images].filter(i => /tile-father/.test(i.currentSrc)).map(i => i.currentSrc.split('/').pop()) }; });
    d.status = r.status(); d.errors = errs.length; res[`${name}-${w}`] = d;
    if (w === 1440 || w === 390) await p.screenshot({ path: `after/shots/${name}-${w}.png`, fullPage: true });
    console.log(name, w, d.status, 'sw', d.sw, 'aquaText', d.aquaText, 'aquaHtml', d.aquaHtml, JSON.stringify(d.order), 'nums', d.nums, 'broken', d.broken, 'err', d.errors);
    await p.close(); }
  fs.writeFileSync('tests/live-results.json', JSON.stringify(res, null, 1)); await b.close(); })();
