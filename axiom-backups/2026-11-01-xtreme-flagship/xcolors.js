const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('https://xtremestpete.com/', { waitUntil: 'networkidle', timeout: 90000 });
  console.log(await p.evaluate(() => { const c = {}; for (const e of document.querySelectorAll('body *')) { const s = getComputedStyle(e); if (e.offsetWidth * e.offsetHeight < 10) continue;
    for (const v of [s.backgroundColor, s.color]) if (!/rgba\(0, 0, 0, 0\)/.test(v)) c[v] = (c[v] || 0) + (v === s.backgroundColor ? e.offsetWidth * e.offsetHeight / 1000 : 1); }
    return Object.entries(c).sort((a, b) => b[1] - a[1]).slice(0, 14).map(x => x[0] + ' ' + Math.round(x[1])).join('\n'); }));
  await b.close(); })();
