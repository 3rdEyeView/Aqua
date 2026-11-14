const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, locale: 'en-US' });
  const p = await ctx.newPage(); const big = new Map();
  p.on('response', async r => { const u = r.url(); if (/scontent.*\.(jpg|webp)/.test(u)) { const h = r.headers()['content-length']; big.set(u.split('?')[0], { u, len: +h || 0 }); } });
  await p.goto('https://www.facebook.com/MartinArborcareLLC/photos', { waitUntil: 'domcontentloaded', timeout: 60000 }); await p.waitForTimeout(6000);
  try { await p.locator('div[role=dialog] [aria-label="Close"]').first().click({ timeout: 2000 }); } catch {}
  const a = p.locator('a[href*="photo.php?fbid"]').first(); await a.scrollIntoViewIfNeeded(); await a.click(); await p.waitForTimeout(6000);
  const r = await p.evaluate(() => ({ url: location.href, text: document.body.innerText.slice(0, 600),
    imgs: [...document.querySelectorAll('img')].map(i => ({ src: i.src.slice(0,140), w: i.naturalWidth, h: i.naturalHeight })).filter(i => i.w >= 400) }));
  console.log(JSON.stringify(r, null, 1)); await p.screenshot({ path: 'click1.png' }); await b.close();
})();
