// Verifies the Comer's draft (page 1996, live at /comers-landscaping-demo/ since 2026-11-14) on desktop 1440, iPhone 13 and Pixel 7, logged out, via a signed Elementor
// preview link. Usage: node native/verify.js <preview-url> [inject]
//   inject: before the snippet is deployed, splice snippet/main.php's <style>/<script> into the HTML response
//           (local test only; nothing is sent to the site).
// Writes preview/verify-log.txt and preview/v-*.jpg. Records every request made during the quote-form flow.
const { chromium, devices } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const [urlArg, mode] = process.argv.slice(2);
// signed preview links expire after ~10 minutes, so each device gets a fresh one ('auto') unless a URL is given
const freshUrl = () => urlArg && urlArg !== 'auto' ? urlArg : require('child_process').execFileSync('python3', ['-I', path.join(__dirname, 'plink.py')]).toString().trim();
const php = fs.readFileSync(path.join(ROOT, 'snippet', 'main.php'), 'utf8');
const css = php.match(/<style id="cmz-demo-css">[\s\S]*?<\/style>/)[0];
const js = php.match(/<script id="cmz-demo-js">[\s\S]*?<\/script>/)[0];
let pass = 0, fail = 0; const log = [];
const ok = (c, m) => { (c ? pass++ : fail++); log.push(`${c ? 'PASS' : 'FAIL'} ${m}`); console.log(`${c ? 'PASS' : 'FAIL'} ${m}`); };
const shot = (p, n) => p.screenshot({ path: path.join(ROOT, 'preview', `v-${n}.jpg`), quality: 72 });

(async () => {
  const b = await chromium.launch();
  for (const [dev, opts] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['iphone13', devices['iPhone 13']], ['pixel7', devices['Pixel 7']]]) {
    const url = freshUrl(); const ctx = await b.newContext(opts); const p = await ctx.newPage();
    if (mode === 'inject') await p.route(u => u.href.includes('elementor_preview_token'), async r => {
      const res = await r.fetch(); let h = await res.text();
      h = h.replace('</head>', () => css + '</head>').replace('</body>', () => js + '</body>');
      r.fulfill({ response: res, body: h });  // replace() uses the function form above: '$$' in a replacement string means '$'
    });
    const errors = []; p.on('pageerror', e => errors.push(e.message));
    console.log(`... ${dev}: loading`); await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 }).catch(e => console.log('goto', e.message)); console.log(`... ${dev}: loaded`);
    await p.waitForTimeout(4500);
    const phone = dev !== 'desktop', H = p.viewportSize().height;
    const base = await p.evaluate(() => ({
      sw: document.documentElement.scrollWidth, vw: innerWidth,
      robots: (document.querySelector('meta[name=robots]') || {}).content || '',
      fonts: document.fonts.check('40px Anton') && document.fonts.check('16px Figtree'),
      snippet: !!document.getElementById('cmz-demo-js'),
      anchors: ['top', 'hero', 'about', 'services', 'process', 'results', 'equipment', 'gallery', 'quote', 'quote-form', 'cmz-form', 'cmz-gal', 'cmz-chips', 'cmz-bar'].filter(i => !document.getElementById(i)),
      imgs: document.images.length,
    }));
    ok(base.snippet, `${dev}: page snippet present`);
    ok(base.sw <= base.vw, `${dev}: no horizontal scroll (${base.sw}/${base.vw})`);
    ok(base.fonts, `${dev}: Anton + Figtree loaded`);
    ok(base.anchors.length === 0, `${dev}: all anchors present ${base.anchors.join(',')}`);
    log.push(`INFO ${dev}: robots="${base.robots}" images=${base.imgs}`);
    // hero: H1 and both buttons on the first screen
    const hero = await p.evaluate(() => {
      const r = s => { const e = document.querySelector(s); const b = e.getBoundingClientRect(); return { t: Math.round(b.top), b: Math.round(b.bottom) }; };
      const btns = [...document.querySelectorAll('#hero a')].filter(a => a.offsetParent).map(a => { const b = a.getBoundingClientRect(); return Math.round(b.bottom); });
      const bar = document.getElementById('cmz-bar'); const bs = getComputedStyle(bar);
      return { h1: r('#hero h1'), btnBottom: Math.max(...btns), nBtn: btns.length, barShown: bs.display !== 'none' && !bar.classList.contains('cmz-hide') };
    });
    ok(hero.nBtn === 2 && hero.btnBottom <= H, `${dev}: hero H1 + both buttons on first screen (buttons end ${hero.btnBottom}px, viewport ${H}px)`);
    ok(!hero.barShown, `${dev}: phone bar not covering the hero`);
    await shot(p, `${dev}-fold`);
    // let every lazy image load, then count broken ones
    await p.evaluate(async () => { for (const i of document.images) { i.loading = 'eager'; } for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } });
    await p.evaluate(() => Promise.race([Promise.all([...document.images].map(i => i.decode().catch(() => null))), new Promise(r => setTimeout(r, 8000))]));
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(800);
    const broken = await p.evaluate(() => [...document.images].filter(i => i.closest('#cmz') || i.closest('[data-elementor-type]')).filter(i => !i.complete || !i.naturalWidth).map(i => i.src.split('/').pop()));
    ok(broken.length === 0, `${dev}: 0 broken page images ${broken.join(',')}`);
    // header stays at the top while scrolling
    await p.evaluate(() => scrollTo(0, 3000)); await p.waitForTimeout(500);
    const hdrTop = await p.evaluate(() => Math.round(document.getElementById('top').getBoundingClientRect().top));
    ok(Math.abs(hdrTop) <= 1, `${dev}: header sticks at the top (top=${hdrTop})`);
    if (phone) {
      const barMid = await p.evaluate(() => { const b = document.getElementById('cmz-bar'); return getComputedStyle(b).display !== 'none' && !b.classList.contains('cmz-hide'); });
      ok(barMid, `${dev}: phone bar shows mid-page`);
    }
    // navigation
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(400);
    for (const [label, id] of [['Services', 'services'], ['Our Work', 'gallery'], ['Results', 'results']]) {
      if (phone) { await p.click('#top summary'); await p.waitForTimeout(350); }
      const link = phone ? p.locator('#top details a', { hasText: label }) : p.locator('#top nav a', { hasText: label });
      await link.first().click(); await p.waitForTimeout(1400);
      const st = await p.evaluate(id => { const s = document.getElementById(id).getBoundingClientRect(), h = document.getElementById('top').getBoundingClientRect(); const det = document.querySelector('#top details'); return { top: Math.round(s.top), hb: Math.round(h.bottom), open: det ? det.open : false }; }, id);
      ok(st.top >= st.hb - 30 && st.top <= st.hb + 40 && !st.open, `${dev}: nav "${label}" lands on #${id} below the header (section ${st.top}px, header ends ${st.hb}px${phone ? ', menu closed' : ''})`);
    }
    if (phone) { await p.click('#top summary'); await p.waitForTimeout(400); await shot(p, `${dev}-menu`); await p.click('#top summary'); }
    // gallery
    await p.locator('#gallery').scrollIntoViewIfNeeded(); await p.waitForTimeout(600);
    const visCount = () => p.evaluate(() => [...document.querySelectorAll('#cmz-gal [id^="g-"]')].filter(t => t.offsetParent).length);
    const chips = await p.locator('#cmz-chips button').count();
    ok(chips === 7, `${dev}: 7 filter chips (${chips})`);
    ok(await visCount() === 8, `${dev}: gallery shows 8 photos first (${await visCount()})`);
    const galH = await p.evaluate(() => Math.round(document.getElementById('gallery').getBoundingClientRect().height));
    log.push(`INFO ${dev}: gallery section height collapsed ${galH}px`);
    await shot(p, `${dev}-gallery`);
    await p.click('.cmz-more button'); await p.waitForTimeout(400);
    ok(await visCount() === 31, `${dev}: "Show all" reveals 31 (${await visCount()})`);
    await p.click('.cmz-more button'); await p.waitForTimeout(400);
    ok(await visCount() === 8, `${dev}: "Show fewer" back to 8`);
    await p.locator('#cmz-chips button[data-f="equip"]').click(); await p.waitForTimeout(300);
    ok(await visCount() === 4 && await p.locator('.cmz-more').isHidden(), `${dev}: Equipment filter shows 4, no Show all`);
    await p.locator('#cmz-chips button[data-f="drain"]').click(); await p.waitForTimeout(300);
    ok(await visCount() === 8, `${dev}: Drainage filter shows 8 (${await visCount()})`);
    await p.locator('#cmz-chips button[data-f="all"]').click(); await p.waitForTimeout(300);
    const firstTile = p.locator('#cmz-gal [id^="g-"]').first();
    await firstTile.click(); await p.waitForTimeout(900);
    const lb1 = await p.evaluate(() => { const lb = document.querySelector('.cmz-lb'); const i = lb.querySelector('img'); return { open: lb.classList.contains('is-open'), cap: lb.querySelector('figcaption').textContent, w: i.naturalWidth, focus: document.activeElement.className }; });
    ok(lb1.open && lb1.w > 600 && lb1.focus === 'cmz-x', `${dev}: lightbox opens full-size photo (${lb1.cap}, ${lb1.w}px), focus on Close`);
    const xbg = await p.evaluate(() => getComputedStyle(document.querySelector('.cmz-lb .cmz-x')).backgroundColor);
    ok(!/204, 51, 102/.test(xbg), `${dev}: lightbox Close keeps its own colour when focused (${xbg})`);
    await shot(p, `${dev}-lightbox`);
    if (phone) {
      await p.evaluate(() => { const lb = document.querySelector('.cmz-lb'); const t = (x) => new Touch({ identifier: 1, target: lb, clientX: x, clientY: 300 }); lb.dispatchEvent(new TouchEvent('touchstart', { touches: [t(300)], changedTouches: [t(300)] })); lb.dispatchEvent(new TouchEvent('touchend', { touches: [], changedTouches: [t(120)] })); });
    } else { await p.click('.cmz-lb .cmz-n'); }
    await p.waitForTimeout(400);
    const cap2 = await p.locator('.cmz-lb figcaption').textContent();
    ok(cap2 !== lb1.cap && /2 of 31/.test(cap2), `${dev}: ${phone ? 'swipe' : 'next arrow'} moves to photo 2 (${cap2})`);
    await p.keyboard.press('Escape'); await p.waitForTimeout(300);
    const closed = await p.evaluate(() => ({ open: document.querySelector('.cmz-lb').classList.contains('is-open'), back: (document.activeElement.id || '').startsWith('g-') }));
    ok(!closed.open && closed.back, `${dev}: Esc closes and focus returns to the tile`);
    // quote buttons: every visible quote link lands on the form card
    const qlinks = await p.evaluate(() => [...document.querySelectorAll('a[href="#quote-form"]')].filter(a => a.offsetParent || a.closest('#cmz-bar')).length);
    let landed = 0, checked = 0;
    for (const sel of ['#hero a[href="#quote-form"]', '#about a[href="#quote-form"]', '#q-4, #q-4 a', '#cmz-bar a[href="#quote-form"]']) {
      const loc = p.locator(sel).first();
      if (sel.startsWith('#cmz-bar')) { await p.evaluate(() => scrollTo(0, document.getElementById('process').offsetTop)); await p.waitForTimeout(700); if (!(await loc.isVisible())) continue; }
      else await loc.scrollIntoViewIfNeeded();
      checked++; await loc.click(); await p.waitForTimeout(1500);
      const r = await p.evaluate(() => { const c = document.getElementById('quote-form').getBoundingClientRect(); return { t: Math.round(c.top), svc: document.getElementById('cmz-s').value }; });
      if (r.t >= 40 && r.t <= 140) landed++;
      if (sel.startsWith('#q-4')) ok(r.svc === 'Hardscaping', `${dev}: Hardscaping card preselects "Hardscaping" (${r.svc})`);
    }
    ok(landed === checked && checked >= 3, `${dev}: quote buttons land on the form card (${landed}/${checked}; ${qlinks} quote links on the page)`);
    await shot(p, `${dev}-quote`);
    const barAtForm = await p.evaluate(() => document.getElementById('cmz-bar').classList.contains('cmz-hide'));
    if (phone) ok(barAtForm, `${dev}: phone bar hides at the form`);
    // form flow: record every request from here on
    const reqs = []; const onReq = r => reqs.push(r.method() + ' ' + r.url().slice(0, 100)); p.on('request', onReq);
    await p.evaluate(() => { document.getElementById('cmz-s').value = ''; });
    await p.click('#cmz-go'); await p.waitForTimeout(300);
    const errs = await p.evaluate(() => ({ on: [...document.querySelectorAll('#cmz-form .cmz-err.on')].map(e => e.id), focus: document.activeElement.id }));
    ok(errs.on.join() === 'cmz-n-e,cmz-p-e,cmz-s-e' && errs.focus === 'cmz-n', `${dev}: empty send flags name, phone, service; focus on name (${errs.on})`);
    await p.fill('#cmz-n', 'Test'); await p.fill('#cmz-p', '80355'); await p.fill('#cmz-m', 'bad@'); await p.click('#cmz-go'); await p.waitForTimeout(200);
    const e2 = await p.evaluate(() => [...document.querySelectorAll('#cmz-form .cmz-err.on')].map(e => e.id));
    ok(e2.includes('cmz-p-e') && e2.includes('cmz-m-e') && !e2.includes('cmz-n-e'), `${dev}: short phone and bad email flagged (${e2})`);
    await p.fill('#cmz-m', ''); await p.click('#cmz-sample'); await p.waitForTimeout(200);
    await p.click('#cmz-go'); await p.waitForTimeout(1800);
    const conf = await p.evaluate(() => { const d = document.getElementById('cmz-done'); return { done: document.getElementById('cmz-form').classList.contains('is-done'), txt: d.innerText, rows: d.querySelectorAll('dl div').length, top: Math.round(document.getElementById('quote-form').getBoundingClientRect().top) }; });
    ok(conf.done && /nothing was sent/.test(conf.txt) && conf.rows >= 5, `${dev}: sample details -> on-page confirmation, ${conf.rows} rows, says nothing was sent`);
    await shot(p, `${dev}-confirmation`);
    await p.click('#cmz-again'); await p.waitForTimeout(300);
    const reset = await p.evaluate(() => !document.getElementById('cmz-form').classList.contains('is-done') && document.getElementById('cmz-n').value === '' && document.activeElement.id === 'cmz-n');
    ok(reset, `${dev}: "Start a new request" resets the form`);
    p.off('request', onReq);
    const sent = reqs.filter(r => !/\.(jpg|jpeg|png|webp|woff2?|css|js)(\?|$)/i.test(r.split(' ')[1]));
    ok(sent.length === 0, `${dev}: 0 non-asset requests during the form flow (${reqs.length} total: ${sent.join(' | ')})`);
    ok(!(await p.locator('#quote form, #cmz-form form').count()), `${dev}: no <form> element in the quote card`);
    log.push(`INFO ${dev}: page errors: ${errors.filter(e => !/leadconnector|msgsndr|chat/i.test(e)).join(' | ') || 'none'}`);
    await ctx.close();
  }
  await b.close();
  log.push(`\n${pass} passed, ${fail} failed`); console.log(`${pass} passed, ${fail} failed`);
  fs.writeFileSync(path.join(ROOT, 'preview', mode === 'inject' ? 'verify-inject-log.txt' : 'verify-log.txt'), log.join('\n') + '\n');
})();
