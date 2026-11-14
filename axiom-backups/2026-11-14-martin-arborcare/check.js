const { chromium, devices } = require('playwright'); const path = require('path');
const FILE = 'file://' + path.resolve(__dirname, 'martin-arborcare-demo.html');
(async () => {
  const b = await chromium.launch(); let fails = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };
  for (const [name, opt] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['iphone13', devices['iPhone 13']]]) {
    const ctx = await b.newContext(opt); const p = await ctx.newPage(); const net = [], errs = [];
    p.on('request', r => { if (!r.url().startsWith('data:') && !r.url().startsWith('file:')) net.push(r.url()); });
    p.on('pageerror', e => errs.push(e.message));
    await p.goto(FILE); await p.waitForTimeout(800);
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 250)); } scrollTo({top: 0, behavior: 'instant'}); });
    await p.waitForTimeout(500);
    const r = await p.evaluate(() => ({ hs: document.documentElement.scrollWidth > innerWidth,
      broken: [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.alt.slice(0,30)).join('|'), imgs: document.images.length,
      noalt: [...document.images].filter(i => !i.alt).length, fonts: document.fonts.check('700 20px "Barlow Condensed"') }));
    ok(!r.hs, `${name}: no horizontal scroll`); ok(!r.broken, `${name}: ${r.imgs} images, 0 broken ${r.broken}`); ok(r.noalt === 0, `${name}: alt on all`);
    ok(r.fonts, `${name}: heading font loaded`);
    await p.screenshot({ path: `shots/${name}-fold.png` }); await p.screenshot({ path: `shots/${name}-full.png`, fullPage: true });
    await p.locator('#f-go').scrollIntoViewIfNeeded(); await p.click('#f-go');
    ok(await p.locator('.err:not(:empty)').count() === 4, `${name}: empty submit shows 4 errors`);
    await p.click('#f-sample'); await p.click('#f-go');
    ok(await p.locator('#est-done.on').isVisible(), `${name}: sample → confirmation`);
    await p.locator('#est-card').screenshot({ path: `shots/${name}-confirmation.png` });
    ok(net.length === 0, `${name}: 0 network requests` + (net.length ? ' ' + net.slice(0, 3) : '')); ok(errs.length === 0, `${name}: no JS errors ${errs}`);
    await ctx.close();
  }
  await b.close(); console.log(fails ? `${fails} failed` : 'all passed'); process.exit(fails ? 1 : 0);
})();
