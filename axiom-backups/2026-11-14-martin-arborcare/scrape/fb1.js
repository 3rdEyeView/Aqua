const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, locale: 'en-US' });
  const p = await ctx.newPage(); const failed = new Set();
  p.on('requestfailed', r => failed.add(new URL(r.url()).host));
  const url = process.argv[2], out = process.argv[3] || 'fb1';
  await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }); await p.waitForTimeout(6000);
  for (const sel of ['div[role=dialog] [aria-label="Close"]', '[aria-label="Close"]']) { try { await p.locator(sel).first().click({ timeout: 1500 }); } catch {} }
  for (let i = 0; i < 12; i++) { await p.mouse.wheel(0, 1500); await p.waitForTimeout(1200);
    for (const sel of ['div[role=dialog] [aria-label="Close"]']) { try { await p.locator(sel).first().click({ timeout: 500 }); } catch {} } }
  const r = await p.evaluate(() => ({ title: document.title, url: location.href, text: document.body.innerText.slice(0, 3000),
    links: [...document.querySelectorAll('a[href*="photo"]')].map(a => a.href).slice(0, 300),
    imgs: [...document.querySelectorAll('img')].map(i => ({ src: i.src, w: i.naturalWidth, h: i.naturalHeight, alt: i.alt })).filter(i => i.w >= 150) }));
  require('fs').writeFileSync(out + '.json', JSON.stringify({ ...r, failed: [...failed] }, null, 1));
  console.log(r.title, r.url, 'imgs', r.imgs.length, 'links', r.links.length); console.log(r.text.slice(0, 1500));
  await p.screenshot({ path: out + '.png' }); await b.close();
})();
