// Usage: node native/shots.js <url> <prefix>  -> preview/<prefix>-{desktop,phone}-*.jpg + layout facts
const { chromium, devices } = require('playwright');
(async () => {
  const [url, pre] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const [name, ctxo] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['phone', { ...devices['iPhone 13'] }]]) {
    const ctx = await b.newContext(ctxo); const p = await ctx.newPage();
    await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 }).catch(e => console.log('goto', e.message));
    await p.waitForTimeout(3500);
    const f = await p.evaluate(() => {
      const r = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return [Math.round(b.top + scrollY), Math.round(b.height)]; };
      return { title: document.title, sw: document.documentElement.scrollWidth, vw: innerWidth, doc: document.documentElement.scrollHeight,
               robots: (document.querySelector('meta[name=robots]') || {}).content, hero: r('#hero'), h1: r('#hero h1'), b2: r('#hero .e-button, #hero a[href^="tel"]'),
               gallery: r('#gallery'), quote: r('#quote-form'), brokenImgs: [...document.images].filter(i => i.complete && !i.naturalWidth).length,
               fonts: [document.fonts.check('40px Anton'), document.fonts.check('16px Figtree')] };
    });
    console.log(name, JSON.stringify(f));
    await p.screenshot({ path: `preview/${pre}-${name}-fold.jpg`, quality: 70 });
    for (const sec of ['#gallery', '#quote-form']) {
      await p.evaluate(s => document.querySelector(s) && document.querySelector(s).scrollIntoView(), sec); await p.waitForTimeout(900);
      await p.screenshot({ path: `preview/${pre}-${name}-${sec.slice(1)}.jpg`, quality: 70 });
    }
    await ctx.close();
  }
  await b.close();
})();
