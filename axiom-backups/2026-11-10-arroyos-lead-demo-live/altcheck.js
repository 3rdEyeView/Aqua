// Logged-out check of a URL: does the demo open, and does a full run + reset work? node altcheck.js <url-with-hash> [loads]
const { chromium, devices } = require('playwright');
const url = process.argv[2], n = +(process.argv[3] || 3);
(async () => {
  const b = await chromium.launch(); let ok = 0, total = 0;
  for (let i = 0; i < n; i++) for (const [name, o] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['mobile', { ...devices['iPhone 13'] }]]) {
    const c = await b.newContext(o); const p = await c.newPage(); total++;
    const resp = await p.goto(url, { waitUntil: 'load', timeout: 90000 }); await p.waitForTimeout(1200);
    const S = (s) => p.locator('#axl-lead-demo').locator(s); const r = { name, age: resp.headers()['age'] || '-', kinsta: resp.headers()['x-kinsta-cache'] };
    r.open = await S('#ld-start').isVisible().catch(() => false);
    if (r.open) {
      const dl0 = await p.evaluate(() => (window.dataLayer || []).length);
      await S('#ld-start').click(); await S('#ld-s1').click(); await S('#ld-s2').click(); await S('#ld-s3b').click();
      r.stage = await S('.col.is-on h3').innerText(); r.auto = await S('#auto-state').innerText();
      await S('#ld-reset').click(); r.reset = await S('#crm-empty').isVisible(); await p.waitForTimeout(600);
      r.dataLayerUnchanged = (await p.evaluate(() => (window.dataLayer || []).length)) === dl0;
      if (r.reset) ok++;
    }
    console.log(JSON.stringify(r)); await c.close();
  }
  console.log(`RESULT ${ok}/${total} loads opened the demo and completed run + reset`); await b.close();
})();
