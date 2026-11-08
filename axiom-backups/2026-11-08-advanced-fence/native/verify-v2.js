// v2 check: originals only, each photo once, tabs + counts, no overflow, cards <= 400px, mobile bar vs chat bubble.
const { chromium, devices } = require('playwright');
const URL_ = process.argv[2], OUT = process.argv[3];
const VIEWS = [['desktop', { viewport: { width: 1440, height: 900 } }], ['iphone13', devices['iPhone 13']], ['pixel7', devices['Pixel 7']], ['ipadmini', devices['iPad Mini']]];
(async () => {
  const b = await chromium.launch(); const res = {};
  for (const [name, opts] of VIEWS) {
    const ctx = await b.newContext(opts); const p = await ctx.newPage();
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(URL_, { waitUntil: 'networkidle', timeout: 60000 });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); } });
    await p.waitForTimeout(2500);
    const r = await p.evaluate(() => {
      const all = [...document.querySelectorAll('img')].filter(i => i.src.includes('/uploads/'));
      const photos = all.filter(i => !i.src.includes('logo'));
      const names = photos.map(i => i.src.split('/').pop().replace(/-\d+x\d+(?=\.)/, ''));
      const over = [...document.querySelectorAll('body *')].filter(e => { const q = e.getBoundingClientRect(); return q.width > 0 && q.right > document.documentElement.clientWidth + 1; }).slice(0, 5).map(e => e.tagName + '.' + String(e.className).slice(0, 50));
      return { sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, over,
        photos: photos.length, unique: new Set(names).size, names, fbCrops: all.filter(i => /-fb-|hero-wood/.test(i.src)).length,
        logos: all.filter(i => i.src.includes('logo')).length, broken: all.filter(i => !i.naturalWidth).length,
        tabs: [...document.querySelectorAll('[role=tab]')].map(t => t.textContent.trim().replace(/\s+/g, ' ')),
        panels: [...document.querySelectorAll('[role=tabpanel]')].map(x => x.querySelectorAll('img').length),
        footer: document.body.innerText.includes('Website concept by Axiom Systems. Demo only.'),
        robots: (document.querySelector('meta[name=robots]') || {}).content,
        canvas: document.body.className.includes('elementor-template-canvas'),
        ids: ['top', 'work', 'types', 'about', 'estimate'].filter(i => !document.getElementById(i)) };
    });
    const tabs = p.locator('[role=tab]'); r.cardW = []; r.tabRes = [];
    for (let i = 0; i < await tabs.count(); i++) {
      await tabs.nth(i).click(); await p.waitForTimeout(500);
      r.tabRes.push(await p.evaluate(() => { const v = [...document.querySelectorAll('[role=tabpanel]')].find(x => x.offsetHeight > 0); const im = [...v.querySelectorAll('img')]; return im.length + ' shown, ' + im.filter(i => i.naturalWidth).length + ' loaded, maxW ' + Math.max(...im.map(i => Math.round(i.getBoundingClientRect().width))) + ', href ' + (v.querySelector('a') || {}).target; }));
    }
    await tabs.nth(0).click();
    await p.waitForTimeout(1500);
    r.bar = await p.evaluate(() => {
      const n = [...document.querySelectorAll('nav')].find(n => getComputedStyle(n).position === 'fixed' && n.offsetHeight > 0);
      const host = document.querySelector('chat-widget'); let bub = null;
      if (host && host.shadowRoot) { const e = host.shadowRoot.querySelector('.lc_text-widget--bubble, button'); if (e) { const q = e.getBoundingClientRect(); bub = [Math.round(q.left), Math.round(q.top), Math.round(q.right), Math.round(q.bottom)]; } }
      let btnR = null; if (n) { btnR = Math.max(...[...n.querySelectorAll('a')].map(a => Math.round(a.getBoundingClientRect().right))); }
      return { bar: !!n, btnRight: btnR, bubble: bub, overlap: !!(n && bub && bub[0] < btnR && bub[3] > n.getBoundingClientRect().top) };
    });
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300);
    await p.screenshot({ path: `${OUT}/v2-${name}-full.png`, fullPage: true });
    await p.screenshot({ path: `${OUT}/v2-${name}-fold.png` });
    r.errs = errs; res[name] = r; await ctx.close();
  }
  console.log(JSON.stringify(res, null, 1)); await b.close();
})();
