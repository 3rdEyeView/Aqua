// Records every third-party request, script and cookie on key pages (Google/LeadConnector hosts are blocked here,
// so their own sub-requests are listed by URL only).
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const out = {};
  for (const path of ['/', '/get-started/', '/pricing/']) {
    const ctx = await b.newContext(); const p = await ctx.newPage(); const hosts = {};
    p.on('request', r => { const h = new URL(r.url()).host; if (h !== 'axiomsystems.systems') hosts[h] = (hosts[h] || 0) + 1; });
    await p.goto('https://axiomsystems.systems' + path, { waitUntil: 'networkidle' }).catch(() => {});
    await p.waitForTimeout(2000);
    out[path] = {
      third_party_hosts: hosts,
      scripts: await p.evaluate(() => [...document.scripts].map(s => s.src).filter(Boolean).map(s => s.split('?')[0])),
      cookies: (await ctx.cookies()).map(c => ({ name: c.name, domain: c.domain, expires: c.expires > 0 ? Math.round((c.expires * 1000 - Date.now()) / 86400000) + 'd' : 'session' })),
      localStorage: await p.evaluate(() => Object.keys(localStorage)),
    };
    await ctx.close();
  }
  await b.close(); fs.writeFileSync('inventory/site-inventory.json', JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out, null, 1));
})();
