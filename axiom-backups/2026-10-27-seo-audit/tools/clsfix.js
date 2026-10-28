// clsfix.js <url>: mobile CLS, live HTML vs HTML with an early viewport meta (served via interception), 4 runs each
const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const url = process.argv[2];
  for (const fix of [false, true]) { const vals = [];
    for (let i = 0; i < 4; i++) { const ctx = await b.newContext({ ...devices['Pixel 7'] });
      if (fix) await ctx.route(u => u.pathname === new URL(url).pathname, async r => { const resp = await r.fetch(); let h = await resp.text();
        h = h.replace('<meta charset="UTF-8">', '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />'); await r.fulfill({ response: resp, body: h }); });
      const p = await ctx.newPage(); await p.addInitScript(() => { window.__c = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__c += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
      await p.goto(url + '?f=' + Date.now() + i, { waitUntil: 'load' }); await p.waitForTimeout(3000); vals.push(+(await p.evaluate(() => window.__c)).toFixed(3)); await ctx.close(); }
    console.log(fix ? 'early viewport' : 'live          ', vals.join(' ')); }
  await b.close(); })();
