// Renders the built single-file preview on desktop and phone, checks behaviour, saves screenshots to shots/.
const { chromium, devices } = require('playwright');
const path = require('path');
const url = 'file://' + path.join(__dirname, 'comers-landscaping-demo.html');
const results = []; const ok = (name, cond, extra='') => { results.push([cond ? 'PASS' : 'FAIL', name, extra]); };
(async () => {
  const browser = await chromium.launch();
  for (const [label, opts] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['phone', devices['iPhone 13']]]) {
    const ctx = await browser.newContext(opts); const page = await ctx.newPage();
    const reqs = []; const errs = [];
    page.on('request', r => { if (!/^(data|file|blob):/.test(r.url())) reqs.push(r.url()); });
    page.on('pageerror', e => errs.push(String(e))); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await page.goto(url); await page.waitForTimeout(1200);
    const span = await page.evaluate(() => document.querySelector('#top').offsetHeight - window.innerHeight);
    ok(`${label}: fonts loaded`, await page.evaluate(() => document.fonts.check('40px Anton') && document.fonts.check('16px Figtree')));
    for (const p of [0, 0.5, 1]) {
      await page.evaluate(y => window.scrollTo(0, document.querySelector('#top').offsetTop + y), Math.round(span * p)); await page.waitForTimeout(1300);
      const o = await page.evaluate(() => +getComputedStyle(document.querySelector('.hm.after')).opacity);
      ok(`${label}: hero p=${p} -> grown-in opacity ${o.toFixed(2)}`, p === 0 ? o < 0.02 : p === 1 ? o > 0.98 : (o > 0.2 && o < 0.8));
      await page.screenshot({ path: `shots/${label}-hero-${String(p).replace('.', '_')}.jpg`, quality: 80, type: 'jpeg' });
    }
    ok(`${label}: no horizontal scroll`, await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
    for (const id of ['about', 'services', 'process', 'work', 'quote']) {
      await page.evaluate(i => document.getElementById(i).scrollIntoView({ block: 'start', behavior: 'instant' }), id); await page.waitForTimeout(1100);
      await page.screenshot({ path: `shots/${label}-${id}.jpg`, quality: 80, type: 'jpeg' });
    }
    ok(`${label}: images all decoded`, await page.evaluate(async () => { const im = [...document.images]; im.forEach(i => i.loading = 'eager'); await Promise.all(im.map(i => i.decode().catch(() => 0))); return im.every(i => i.naturalWidth > 0); }));
    if (label === 'desktop') {
      await page.evaluate(() => document.getElementById('services').scrollIntoView({ block: 'start', behavior: 'instant' }));
      await page.hover('.svc-item:nth-child(4) .svc-btn'); await page.waitForTimeout(900);
      ok('desktop: hovering service 4 shows its image', await page.evaluate(() => { const it = document.querySelectorAll('.svc-item')[3]; return it.classList.contains('is-active') && getComputedStyle(it.querySelector('.svc-fig')).opacity === '1'; }));
      await page.screenshot({ path: 'shots/desktop-services-hardscape.jpg', quality: 80, type: 'jpeg' });
    } else {
      ok('phone: call bar visible after hero', await page.evaluate(() => { window.scrollTo(0, document.getElementById('services').offsetTop); return new Promise(r => setTimeout(() => r(document.getElementById('mbar').classList.contains('is-on')), 500)); }));
      await page.click('#menuBtn').catch(() => {}); 
    }
    // form
    await page.evaluate(() => { document.getElementById('drawer').classList.remove('is-open'); document.body.style.overflow = ''; document.getElementById('qcard').scrollIntoView({ block: 'center', behavior: 'instant' }); });
    await page.waitForTimeout(600);
    const before = reqs.length;
    await page.click('#qSend'); ok(`${label}: empty send flags 4 fields`, await page.locator('.fld.bad').count() === 4);
    await page.click('#qFill'); await page.click('#qSend'); await page.waitForTimeout(300);
    ok(`${label}: confirmation shown`, await page.locator('#qDone').isVisible());
    await page.screenshot({ path: `shots/${label}-quote-confirmation.jpg`, quality: 80, type: 'jpeg' });
    await page.click('#qReset'); ok(`${label}: reset returns form`, await page.locator('#qSend').isVisible());
    ok(`${label}: zero network requests`, reqs.length === 0 && before === 0, reqs.slice(0, 3).join(' '));
    ok(`${label}: no console errors`, errs.length === 0, errs.slice(0, 2).join(' | '));
    ok(`${label}: 25 images present`, await page.locator("img").count() === 25);
    ok(`${label}: tel links`, await page.locator('a[href="tel:+18034228031"]').count() >= 4);
    await ctx.close();
  }
  // reduced motion
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }); const page = await ctx.newPage();
  await page.goto(url); await page.waitForTimeout(800);
  ok('reduced motion: hero is one screen, finished still shown', await page.evaluate(() => document.querySelector('#top').offsetHeight <= innerHeight + 2 && getComputedStyle(document.querySelector('.hm.after')).opacity === '1'));
  await page.screenshot({ path: 'shots/desktop-reduced-motion.jpg', quality: 80, type: 'jpeg' });
  await browser.close();
  for (const r of results) console.log(r.join('  '));
  const f = results.filter(r => r[0] === 'FAIL').length; console.log(`${results.length - f} passed, ${f} failed`); process.exit(f ? 1 : 0);
})();
