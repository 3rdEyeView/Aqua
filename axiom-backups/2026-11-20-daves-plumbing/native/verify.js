// node native/verify.js <url|auto>  -> desktop 1440, iPhone 13, Pixel 7, logged out. 'auto' mints a preview link per device.
const { chromium, devices } = require('playwright'); const { execFileSync } = require('child_process'); const path = require('path');
const ARG = process.argv[2]; const OUT = path.join(__dirname, '..', 'preview');
const url = () => ARG === 'auto' ? execFileSync('python3', ['-I', path.join(__dirname, 'plink.py')]).toString().trim() : ARG;
(async () => {
  const b = await chromium.launch(); let pass = 0, fail = 0;
  const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); c ? pass++ : fail++; };
  for (const [name, opt] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['iphone13', devices['iPhone 13']], ['pixel7', devices['Pixel 7']]]) {
    const ctx = await b.newContext(opt); const p = await ctx.newPage(); const errs = []; let formNet = null;
    p.on('pageerror', e => errs.push(e.message));
    p.on('request', r => { if (formNet && !/\.(png|jpe?g|webp|gif|svg|woff2?|css)(\?|$)/.test(r.url())) formNet.push(r.url()); });
    await p.goto(url(), { waitUntil: 'load', timeout: 90000 }); await p.waitForTimeout(2500);
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo({ top: y, behavior: 'instant' }); await new Promise(r => setTimeout(r, 200)); } scrollTo({ top: 0, behavior: 'instant' }); });
    await p.waitForTimeout(1200);
    const r = await p.evaluate(() => {
      const imgs = [...document.querySelectorAll('img')].filter(i => i.closest('#hero, section, header, footer'));
      const rob = (document.querySelector('meta[name=robots]') || {}).content || '';
      return { hs: document.documentElement.scrollWidth > innerWidth + 1, rob, n: imgs.length,
        broken: imgs.filter(i => !i.complete || !i.naturalWidth).map(i => i.alt).join('|'), noalt: imgs.filter(i => !i.alt).length,
        fonts: document.fonts.check('700 20px "Barlow Condensed"') && document.fonts.check('400 16px "Figtree"'),
        anchors: ['top', 'hero', 'services', 'work', 'process', 'about', 'estimate', 'estimate-form', 'dp-form', 'dp-bar'].filter(id => !document.getElementById(id)),
        snippet: !!document.getElementById('dp-demo-css') && !!document.getElementById('dp-demo-js'), form: !!document.getElementById('dp-go'),
        h1: (document.querySelector('h1') || {}).innerText, tels: document.querySelectorAll('a[href="tel:+19732942238"]').length,
        accent: getComputedStyle(document.querySelector('#hero h1 em') || document.body).color,
        hdr: getComputedStyle(document.getElementById('top')).backgroundColor };
    });
    ok(!r.hs, `${name}: no horizontal scroll`); ok(/noindex/.test(r.rob) && /nofollow/.test(r.rob), `${name}: robots "${r.rob}"`);
    ok(r.snippet && r.form, `${name}: snippet CSS/JS + form present`); ok(r.anchors.length === 0, `${name}: anchors present ${r.anchors}`);
    ok(r.n >= 4 && !r.broken, `${name}: ${r.n} images, broken: ${r.broken || 0}`); ok(r.noalt === 0, `${name}: alt on all`);
    ok(r.fonts, `${name}: Barlow Condensed + Figtree loaded`); ok(r.accent === 'rgb(53, 195, 232)', `${name}: hero accent ${r.accent}`);
    ok(r.tels >= 4, `${name}: ${r.tels} tel links`); ok(/rgba?\(11, 42, 74/.test(r.hdr), `${name}: header colour ${r.hdr}`);
    await p.screenshot({ path: `${OUT}/${name}-fold.png` });
    const sticky = await p.evaluate(async () => { scrollTo({ top: 1500, behavior: 'instant' }); await new Promise(r => setTimeout(r, 300)); return document.getElementById('top').getBoundingClientRect().top; });
    ok(Math.abs(sticky) < 2, `${name}: sticky header (top ${sticky})`);
    if (name !== 'desktop') {
      await p.waitForTimeout(500);
      const bar = await p.evaluate(() => !document.getElementById('dp-bar').classList.contains('dp-hide') && getComputedStyle(document.getElementById('dp-bar')).display !== 'none');
      ok(bar, `${name}: phone bar shown mid-page`);
      await p.evaluate(() => scrollTo({ top: 0, behavior: 'instant' })); await p.waitForTimeout(500);
      ok(await p.evaluate(() => document.getElementById('dp-bar').classList.contains('dp-hide')), `${name}: phone bar hidden over hero buttons`);
    }
    // service card preselect + land on form
    await p.locator('#q-4 a').scrollIntoViewIfNeeded(); await p.locator('#q-4 a').click(); await p.waitForTimeout(1500);
    const land = await p.evaluate(() => ({ s: document.getElementById('dp-s').value, top: document.getElementById('estimate-form').getBoundingClientRect().top }));
    ok(land.s === 'Fixtures / faucets' && land.top > 40 && land.top < 160, `${name}: Fixtures card preselects (${land.s}) and lands on form (top ${Math.round(land.top)})`);
    if (name !== 'desktop') ok(await p.evaluate(() => document.getElementById('dp-bar').classList.contains('dp-hide')), `${name}: phone bar hidden at form`);
    formNet = [];
    await p.evaluate(() => { document.getElementById('dp-s').value = ''; }); await p.click('#dp-go');
    ok(await p.locator('#dp-form .dp-err.on').count() === 4, `${name}: empty send → 4 errors`);
    await p.click('#dp-sample'); await p.click('#dp-go'); await p.waitForTimeout(400);
    ok(await p.locator('#dp-done').isVisible() && /nothing was sent/.test(await p.locator('#dp-done').innerText()), `${name}: sample → confirmation`);
    await p.locator('#estimate-form').screenshot({ path: `${OUT}/${name}-confirmation.png` });
    await p.click('#dp-again'); ok(await p.locator('#dp-n').isVisible(), `${name}: reset`);
    ok(formNet.length === 0, `${name}: 0 requests during form flow ${formNet.slice(0, 3)}`);
    ok(await p.locator('#dp-form form, form#dp-form').count() === 0, `${name}: no <form> element`);
    ok(errs.filter(e => !/leadconnector|msgsndr|chat/i.test(e)).length === 0, `${name}: no page errors ${errs.slice(0, 2)}`);
    await p.evaluate(() => scrollTo({ top: 0, behavior: 'instant' })); await p.waitForTimeout(400);
    await p.screenshot({ path: `${OUT}/${name}-full.png`, fullPage: true });
    await ctx.close();
  }
  await b.close(); console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
})();
