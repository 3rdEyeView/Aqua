const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, locale: 'en-US' });
  const p = await ctx.newPage(); const hosts = new Set(), failed = new Set();
  p.on('request', r => hosts.add(new URL(r.url()).host)); p.on('requestfailed', r => failed.add(new URL(r.url()).host));
  const url = process.argv[2];
  await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }); await p.waitForTimeout(6000);
  for (const sel of ['[aria-label="Close"]', 'div[role=dialog] [aria-label="Close"]']) { try { await p.locator(sel).first().click({ timeout: 1500 }); } catch {} }
  for (let i = 0; i < 8; i++) { await p.mouse.wheel(0, 1500); await p.waitForTimeout(1200); }
  const r = await p.evaluate(() => ({ title: document.title, url: location.href, text: document.body.innerText.slice(0, 2500),
    imgs: [...document.querySelectorAll('img')].map(i => ({ src: i.src, w: i.naturalWidth, h: i.naturalHeight, alt: i.alt })).filter(i => i.w >= 200) }));
  console.log(JSON.stringify({ ...r, failed: [...failed] }, null, 1));
  await p.screenshot({ path: 'ig1.png' }); await b.close();
})();
