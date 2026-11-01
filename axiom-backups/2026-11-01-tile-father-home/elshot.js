// usage: node elshot.js url width dataid out [scale]
const { chromium } = require('playwright');
(async () => { const [url, w, id, out, s] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: 900 }, deviceScaleFactor: +(s || 2) });
  await p.goto(url, { waitUntil: 'networkidle' }); const el = p.locator(`[data-id="${id}"]`).first(); await el.scrollIntoViewIfNeeded();
  await p.evaluate(() => document.querySelectorAll('img').forEach(i => i.loading = 'eager')); await p.waitForTimeout(1500);
  await el.screenshot({ path: out }); await b.close(); })();
