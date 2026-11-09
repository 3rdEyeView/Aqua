// Live checks for /fence-it-up-demo/ (page 1764): node native/verify.js [url] [outdir]
const { chromium, devices } = require('playwright');
const URL = process.argv[2] || 'https://axiomsystems.systems/fence-it-up-demo/';
const OUT = process.argv[3] || require('path').join(__dirname, '..', 'preview');
require('fs').mkdirSync(OUT, { recursive: true });
const PROFILES = [
  ['desktop', { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 }],
  ['iphone13', devices['iPhone 13']],
  ['pixel7', devices['Pixel 7']],
  ['ipadmini', devices['iPad Mini']],
];
const ok = (c, m) => console.log((c ? '  ✓ ' : '  ✗ ') + m);

(async () => {
  const b = await chromium.launch();
  for (const [name, prof] of PROFILES) {
    console.log(`\n== ${name}`);
    const ctx = await b.newContext(prof);
    const p = await ctx.newPage();
    const errors = [];
    p.on('pageerror', e => errors.push(String(e)));
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errors.push(m.text().slice(0, 160)); });
    const failedHosts = new Set();
    p.on('requestfailed', r => failedHosts.add(new globalThis.URL(r.url()).host));
    await p.goto(URL + '?v=' + Date.now(), { waitUntil: 'networkidle', timeout: 90000 });
    await p.waitForTimeout(1500);

    const s = await p.evaluate(async () => {
      const q = s => document.querySelector(s);
      const imgs = [...document.querySelectorAll('[data-elementor-id="1764"] img')];
      for (const i of imgs) { i.loading = 'eager'; }
      await Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 8000); })));
      const r = el => el.getBoundingClientRect();
      const heroImg = q('#hero img'), heroH1 = q('#hero h1');
      return {
        sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
        robots: q('meta[name="robots"]')?.content,
        canvas: document.body.className.includes('elementor-template-canvas'),
        fonts: { archivo: document.fonts.check('800 20px Archivo'), figtree: document.fonts.check('400 16px Figtree') },
        h1: heroH1?.textContent, h1Accent: getComputedStyle(q('#hero h1 em') || heroH1).color,
        anchors: ['top', 'hero', 'services', 'work', 'why', 'estimate', 'fiu-form', 'fiu-bar', 'q-vinyl', 'q-wood', 'q-chain', 'q-gates'].filter(id => !document.getElementById(id)),
        imgs: imgs.map(i => { const m = (i.srcset || '').split(',').map(x => x.trim().split(/\s+/)).find(x => x[0] === i.currentSrc); return { f: i.currentSrc.split('/').pop(), nw: i.naturalWidth, fw: m ? parseInt(m[1]) : i.naturalWidth, w: Math.round(r(i).width), h: Math.round(r(i).height), alt: !!i.alt }; }),
        hero: heroImg && { img: r(heroImg).toJSON(), h1: r(heroH1).toJSON(), frame: r(heroImg.parentElement).toJSON() },
        estLinks: [...document.querySelectorAll('a[href="#estimate"]')].filter(a => a.offsetParent || getComputedStyle(a).position === 'fixed').length,
        estLinksAll: document.querySelectorAll('a[href="#estimate"]').length,
        telLinks: document.querySelectorAll('a[href^="tel:"]').length,
        phoneText: /\(\d{3}\)\s?\d{3}-\d{4}/.test(document.querySelector('[data-elementor-id="1764"]').innerText.replace(/\(407\) 555-01\d\d/g, '')),
        formReady: !!q('#fiu-form.fiu-ready'), formTags: document.querySelectorAll('#fiu-form form').length,
        bar: q('#fiu-bar') && getComputedStyle(q('#fiu-bar')).display,
        labels: [...document.querySelectorAll('#work [class*="e-paragraph"], #work p')].map(e => e.textContent.trim()).filter(t => /, FL$/.test(t)),
      };
    });
    ok(s.sw === s.cw, `no horizontal scroll (${s.sw}/${s.cw})`);
    ok(/noindex/.test(s.robots) && /nofollow/.test(s.robots), `robots: ${s.robots}`);
    ok(s.canvas, 'Canvas template');
    ok(s.fonts.archivo && s.fonts.figtree, `fonts ${JSON.stringify(s.fonts)}`);
    ok(s.h1 === 'Fence Installation in Orlando', `H1 "${s.h1}" accent ${s.h1Accent}`);
    ok(s.anchors.length === 0, 'anchors present' + (s.anchors.length ? ' — missing ' + s.anchors : ''));
    const broken = s.imgs.filter(i => !i.nw);
    const uniq = new Set(s.imgs.map(i => i.f.replace(/-\d+x\d+(?=\.jpg)/, '')));
    ok(s.imgs.length === 9 && !broken.length && uniq.size === 9, `${s.imgs.length} photos, ${uniq.size} unique, ${broken.length} broken, alt on all: ${s.imgs.every(i => i.alt)}`);
    const dpr = prof.deviceScaleFactor || 1;
    const dens = s.imgs.map(i => ({ f: i.f, d: +(i.fw / (i.w * dpr)).toFixed(2), css: i.w }));
    console.log(`    density (file px / device px): min ${Math.min(...dens.map(x => x.d))} · ` + dens.map(x => `${x.f.replace('fenceitup-demo-', '').replace('.jpg', '')} ${x.css}css→${x.d}`).join(' · '));
    if (s.hero) {
      const side = s.hero.img.left > s.hero.h1.right - 5;
      const stacked = s.hero.img.top > s.hero.h1.bottom;
      ok(name === 'desktop' ? side : stacked, name === 'desktop' ? `hero photo beside copy (photo ${Math.round(s.hero.frame.width)}×${Math.round(s.hero.frame.height)} css)` : `hero stacked under copy (photo ${Math.round(s.hero.frame.width)} css wide)`);
    }
    console.log(`    gallery labels: ${s.labels.join(' | ')}`);
    ok(s.telLinks === 0 && !s.phoneText, `no phone number (tel links ${s.telLinks})`);
    ok(s.formReady && s.formTags === 0, `form rendered by snippet, no <form> element`);
    console.log(`    #estimate links: ${s.estLinksAll} total, ${s.estLinks} visible here; mobile bar display: ${s.bar}`);
    await p.screenshot({ path: `${OUT}/${name}-fold.png` });

    // every visible estimate link lands on the estimate section
    const linkIds = await p.$$eval('a[href="#estimate"]', as => as.map((a, i) => { a.dataset.vk = i; const r = a.getBoundingClientRect(); return { i, t: a.textContent.trim(), vis: !!(a.offsetParent || getComputedStyle(a).position === 'fixed') && r.width > 0 }; }));
    let landed = 0, tried = 0;
    for (const l of linkIds.filter(l => l.vis)) {
      await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(150);
      const a = p.locator(`a[data-vk="${l.i}"]`);
      if (!(await a.isVisible())) continue;
      tried++;
      await a.click();
      let top = 1e9, prev = -1e9;
      for (let k = 0; k < 20 && Math.abs(top - prev) > 0.5; k++) { await p.waitForTimeout(250); prev = top; top = await p.evaluate(() => document.getElementById('estimate').getBoundingClientRect().top); }
      if (Math.abs(top) < 120) landed++; else console.log(`    ✗ "${l.t}" → estimate top ${Math.round(top)}`);
    }
    ok(landed === tried && tried > 0, `estimate buttons: ${landed}/${tried} visible links land on #estimate`);

    // services links preselect the fence type
    const pre = {};
    for (const k of ['vinyl', 'wood', 'chain', 'gates']) {
      await p.evaluate(() => window.scrollTo(0, 0));
      await p.locator(`#q-${k} a, a#q-${k}`).first().click(); await p.waitForTimeout(2200);
      pre[k] = await p.$eval('#fiu-t', s => s.value);
    }
    ok(pre.vinyl === 'Vinyl privacy' && pre.wood === 'Wood' && pre.chain === 'Chain link' && pre.gates === 'Gate', `type preselect ${JSON.stringify(pre)}`);

    // mobile bar steps aside at the form
    if (name !== 'desktop') {
      const barState = await p.evaluate(() => ({ off: document.getElementById('fiu-bar').classList.contains('fiu-off') }));
      ok(barState.off, 'mobile bar hidden while the form is on screen');
    }

    // form: empty submit → errors; sample → confirmation; no network traffic during the form flow
    await p.$eval('#fiu-t', s => { s.value = ''; });
    await p.focus('#fiu-n'); await p.focus('#fiu-p'); await p.focus('#fiu-z');
    const early = await p.$$eval('#fiu-form .fiu-err.on', e => e.length);
    ok(early === 0, `tabbing past empty fields shows no errors (${early})`);
    const reqs = [];
    const onReq = r => reqs.push(r.method() + ' ' + r.url().slice(0, 110));
    p.on('request', onReq);
    await p.locator('#fiu-go').click(); await p.waitForTimeout(300);
    const errs = await p.$$eval('#fiu-form .fiu-err.on', e => e.map(x => x.id));
    const focused = await p.evaluate(() => document.activeElement.id);
    ok(errs.length === 4 && focused === 'fiu-n', `empty submit → ${errs.length} errors (${errs.join(',')}), focus ${focused}`);
    await p.fill('#fiu-p', '407555'); await p.locator('#fiu-p').blur(); await p.fill('#fiu-z', '32a8');
    const partial = await p.evaluate(() => ({ p: document.getElementById('fiu-p-e').classList.contains('on'), z: document.getElementById('fiu-z').value }));
    ok(partial.p && partial.z === '328', `short phone flagged, ZIP keeps digits only ("${partial.z}")`);
    await p.locator('#fiu-sample').click(); await p.waitForTimeout(200);
    await p.locator('#fiu-go').click(); await p.waitForTimeout(800);
    const done = await p.evaluate(() => ({ on: document.getElementById('fiu-form').classList.contains('is-done'), t: document.getElementById('fiu-done').innerText, vis: document.getElementById('fiu-done').getBoundingClientRect().height > 0, top: document.getElementById('fiu-done').getBoundingClientRect().top }));
    ok(done.on && done.vis && /Thanks, Sam!/.test(done.t) && /nothing was sent/.test(done.t), `confirmation shown (top ${Math.round(done.top)}): "${done.t.split('\n').slice(0, 3).join(' / ')}"`);
    await p.screenshot({ path: `${OUT}/${name}-confirmation.png` });
    await p.waitForTimeout(1500);
    p.off('request', onReq);
    ok(reqs.length === 0, `network requests during the form flow: ${reqs.length}` + (reqs.length ? '\n      ' + reqs.join('\n      ') : ''));
    await p.locator('#fiu-again').click(); await p.waitForTimeout(200);
    const reset = await p.evaluate(() => ({ done: document.getElementById('fiu-form').classList.contains('is-done'), n: document.getElementById('fiu-n').value, f: document.activeElement.id }));
    ok(!reset.done && reset.n === '' && reset.f === 'fiu-n', 'Start a new request resets the form');

    // mobile bar vs the site chat: the button gets the tap, the bubble keeps its corner, the bar hides while chat is open
    if (name !== 'desktop') {
      await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(900);
      const g = await p.evaluate(() => {
        const bar = document.getElementById('fiu-bar'), btn = bar.querySelector('a'), br = btn.getBoundingClientRect(), nr = bar.getBoundingClientRect();
        const pts = [[0.5, 0.5], [0.1, 0.2], [0.9, 0.2], [0.5, 0.9]].map(([fx, fy]) => document.elementFromPoint(br.left + br.width * fx, br.top + br.height * fy));
        const cw = document.querySelector('chat-widget'), bub = cw && cw.shadowRoot && cw.shadowRoot.querySelector('.lc_text-widget--bubble');
        const u = bub && bub.getBoundingClientRect();
        const hit = u && !(u.right <= nr.left || u.left >= nr.right || u.bottom <= nr.top || u.top >= nr.bottom);
        const onBubble = u && cw.shadowRoot.elementFromPoint ? cw.shadowRoot.elementFromPoint(u.left + u.width / 2, u.top + u.height / 2) : null;
        return { tapOk: pts.every(e => e && e.closest && e.closest('#fiu-bar')), bubble: !!bub, overlap: !!hit, bubbleTop: onBubble ? !!onBubble.closest('.lc_text-widget--bubble') : null,
                 bar: [Math.round(nr.left), Math.round(nr.right)], bub: u && [Math.round(u.left), Math.round(u.right)] };
      });
      ok(g.tapOk, 'bar button receives taps (center + corners), above the chat greeting box');
      ok(g.bubble && !g.overlap && g.bubbleTop !== false, `chat bubble clear of the bar (bar x ${g.bar}, bubble x ${g.bub}), still on top at its center`);
      await p.screenshot({ path: `${OUT}/${name}-bar.png` });
      await p.locator('#fiu-bar a').click();
      let top = 1e9, prev = -1e9;
      for (let k = 0; k < 20 && Math.abs(top - prev) > 0.5; k++) { await p.waitForTimeout(250); prev = top; top = await p.evaluate(() => document.getElementById('estimate').getBoundingClientRect().top); }
      ok(Math.abs(top) < 120, `real tap on the bar button → #estimate (top ${Math.round(top)})`);
      await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(700);
      await p.evaluate(() => document.querySelector('chat-widget').setAttribute('data-active', 'true')); await p.waitForTimeout(400);
      const hidOpen = await p.evaluate(() => document.getElementById('fiu-bar').classList.contains('fiu-off'));
      await p.evaluate(() => document.querySelector('chat-widget').setAttribute('data-active', 'false')); await p.waitForTimeout(400);
      const back = await p.evaluate(() => !document.getElementById('fiu-bar').classList.contains('fiu-off'));
      ok(hidOpen && back, 'bar hides while the chat is open and returns when it closes');
    }
    await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(300);
    await p.screenshot({ path: `${OUT}/${name}-full.png`, fullPage: true });
    console.log(`    console errors (excluding blocked loads): ${errors.length}${errors.length ? ' — ' + errors.join(' | ') : ''}`);
    console.log(`    blocked/failed hosts: ${[...failedHosts].join(', ') || 'none'}`);
    await ctx.close();
  }
  await b.close();
})();
