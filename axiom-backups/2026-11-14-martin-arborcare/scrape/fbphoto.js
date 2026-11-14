const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, locale: 'en-US' });
  const p = await ctx.newPage();
  await p.goto(process.argv[2], { waitUntil: 'domcontentloaded', timeout: 60000 }); await p.waitForTimeout(5000);
  const r = await p.evaluate(() => ({ url: location.href, text: document.body.innerText.slice(0, 800),
    imgs: [...document.querySelectorAll('img')].map(i => ({ src: i.src, w: i.naturalWidth, h: i.naturalHeight, alt: i.alt })).filter(i => i.w >= 300) }));
  console.log(JSON.stringify(r, null, 1)); await p.screenshot({ path: 'photo1.png' }); await b.close();
})();
