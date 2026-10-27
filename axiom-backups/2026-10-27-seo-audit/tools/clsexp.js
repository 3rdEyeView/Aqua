// clsexp.js <url> : mobile CLS under variants (block patterns), 3 runs each
const { chromium, devices } = require('playwright');
const variants = { normal: null, noGoogleFonts: /fonts\.(googleapis|gstatic)\.com/, noWooCss: /woocommerce.*\.css/, noThirdParty: /(googletagmanager|stats\.wp\.com|leadconnectorhq)/ };
(async () => { const b = await chromium.launch(); const url = process.argv[2];
  for (const [name, re] of Object.entries(variants)) { const vals = [];
    for (let i = 0; i < 3; i++) { const ctx = await b.newContext({ ...devices['Pixel 7'] }); if (re) await ctx.route(re, r => r.abort());
      const p = await ctx.newPage(); await p.addInitScript(() => { window.__c = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__c += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
      await p.goto(url + '?nc=' + Date.now() + i, { waitUntil: 'load' }); await p.waitForTimeout(3500); vals.push(+(await p.evaluate(() => window.__c)).toFixed(3)); await ctx.close(); }
    console.log(name.padEnd(14), vals.join(' ')); }
  await b.close(); })();
