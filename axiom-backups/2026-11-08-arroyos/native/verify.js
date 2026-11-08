// node verify.js <url> <outdir> — live checks on desktop 1440, iPhone 13, Pixel 7
const { chromium, devices } = require('playwright');
(async () => {
  const [url, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const res = {};
  for (const [name, opts] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['iphone13', devices['iPhone 13']], ['pixel7', devices['Pixel 7']]]) {
    const c = await b.newContext({ ...opts, ...(name === 'desktop' ? { deviceScaleFactor: 1 } : {}) }); const p = await c.newPage();
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    const t0 = Date.now();
    await p.goto(url + '?v=' + Date.now(), { waitUntil: 'domcontentloaded', timeout: 90000 });
    await p.waitForLoadState('networkidle', { timeout: 60000 }).catch(() => {});
    const r = await p.evaluate(() => {
      const v = document.querySelector('#hero video');
      const h1 = document.querySelector('h1'), em = h1 && h1.querySelector('em');
      return {
        robots: (document.querySelector('meta[name=robots]') || {}).content,
        canvas: document.body.className.includes('elementor-template-canvas'),
        poster: v && v.getAttribute('poster'), playing: v && !v.paused, vtime: v && v.currentTime, vsrc: v && v.currentSrc.split('/').pop(),
        objectFit: v && getComputedStyle(v).objectFit, vrect: v && JSON.stringify(v.getBoundingClientRect()),
        h1: h1 && h1.textContent.trim(), emColor: em && getComputedStyle(em).color, h2emBg: (document.querySelector('#about h2 em') ? getComputedStyle(document.querySelector('#about h2 em')).backgroundImage.slice(0, 40) : null),
        sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
        anchors: ['top','hero','about','services','process','results','work','areas','faq','estimate'].filter(id => !document.getElementById(id)),
        quoteLinks: [...document.querySelectorAll('a[href="#estimate"]')].length, telLinks: [...document.querySelectorAll('a[href^="tel:"]')].length,
      };
    });
    // hero fold screenshot after video has played a bit
    await p.waitForTimeout(1500);
    await p.screenshot({ path: `${out}/live-${name}-fold.png` });
    // scroll all, then check images
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } });
    await p.waitForTimeout(2000);
    r.imgs = await p.evaluate(() => [...document.querySelectorAll('img')].map(i => ({ f: (i.currentSrc || '').split('/').pop(), ok: i.complete && i.naturalWidth > 0, w: Math.round(i.getBoundingClientRect().width), nw: i.naturalWidth })));
    r.broken = r.imgs.filter(i => !i.ok).length;
    // slider
    const ba = await p.$('#ba'); await ba.scrollIntoViewIfNeeded(); await p.waitForTimeout(2200); // let the intro nudge finish
    const box = await ba.boundingBox();
    const rects = await p.evaluate(() => [...document.querySelectorAll('#ba img')].map(i => JSON.stringify(i.getBoundingClientRect()) + ' ' + getComputedStyle(i).objectPosition));
    r.baAligned = rects.length === 2 && rects[0].split(' ')[0] === rects[1].split(' ')[0]; r.baRects = rects;
    const clip = () => p.evaluate(() => document.getElementById('ba-before').style.clipPath + ' | handle ' + document.getElementById('ba-handle').style.left);
    r.baStart = await clip();
    const y = box.y + box.height / 2;
    if (name === 'desktop') {
      await p.mouse.move(box.x + box.width * 0.5, y); await p.mouse.down();
      for (let k = 1; k <= 10; k++) await p.mouse.move(box.x + box.width * (0.5 - 0.03 * k), y);
      await p.mouse.up(); r.baDrag = await clip();
      await p.focus('#ba .arl-ba-range'); for (let k = 0; k < 10; k++) await p.keyboard.press('ArrowRight'); r.baKeys = await clip();
    } else {
      const cdp = await c.newCDPSession(p);
      const touch = async (type, x, yy) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y: yy }] });
      // horizontal swipe: should move the divider
      await touch('touchStart', box.x + box.width * 0.5, y);
      for (let k = 1; k <= 12; k++) { await touch('touchMove', box.x + box.width * (0.5 + 0.03 * k), y); await p.waitForTimeout(16); }
      await touch('touchEnd'); await p.waitForTimeout(100); r.baSwipe = await clip();
      // vertical swipe on the slider: page should scroll, divider should not move
      const before = await clip(); const sy0 = await p.evaluate(() => scrollY);
      await touch('touchStart', box.x + box.width * 0.3, y + 40);
      for (let k = 1; k <= 12; k++) { await touch('touchMove', box.x + box.width * 0.3, y + 40 - 15 * k); await p.waitForTimeout(16); }
      await touch('touchEnd'); await p.waitForTimeout(600);
      r.vScroll = { scrolled: (await p.evaluate(() => scrollY)) - sy0, dividerUnchanged: (await clip()) === before };
      // tap to jump
      await touch('touchStart', box.x + box.width * 0.2, y); await touch('touchEnd'); await p.waitForTimeout(100); r.baTap = await clip();
    }
    await ba.scrollIntoViewIfNeeded(); await p.evaluate(() => window.scrollBy(0, -120)); await p.waitForTimeout(300);
    await p.screenshot({ path: `${out}/live-${name}-slider.png` });
    if (name !== 'desktop') {
      // mobile menu opens
      await p.evaluate(() => window.scrollTo(0, 0)); await p.click('#top summary, #top [role=button]').catch(() => {});
      await p.waitForTimeout(400);
      r.menuLinks = await p.evaluate(() => [...document.querySelectorAll('#top a[href^="#"]')].filter(a => a.offsetParent && a.getBoundingClientRect().height > 0).length);
      await p.screenshot({ path: `${out}/live-${name}-menu.png` });
      r.mobileBar = await p.evaluate(() => { const n = [...document.querySelectorAll('nav')].find(n => getComputedStyle(n).position === 'fixed'); return n ? JSON.stringify(n.getBoundingClientRect()) : null; });
    }
    r.errors = errs; r.ms = Date.now() - t0;
    res[name] = r; await c.close();
  }
  for (const [k, r] of Object.entries(res)) { const imgs = r.imgs; delete r.imgs; console.log(k, JSON.stringify(r, null, 1)); console.log(' imgs', imgs.map(i => `${i.f}:${i.w}/${i.nw}${i.ok ? '' : ' BROKEN'}`).join(', ')); }
  await b.close();
})();
