const { chromium, devices } = require('playwright');
const fs = require('fs'), path = require('path');
const URL_ = process.argv[2], OUT = process.argv[3], LOCAL = process.argv[4]; // LOCAL dir => route images locally
(async () => {
  const b = await chromium.launch();
  const res = {};
  for (const [name, opts] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['phone', devices['iPhone 13']]]) {
    const ctx = await b.newContext(opts); const p = await ctx.newPage();
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    if (LOCAL) await p.route(/\/wp-content\/uploads\/2026\/11\/branham-demo-[^/]+$/, r => {
      const f = path.join(LOCAL, path.basename(new URL(r.request().url()).pathname));
      fs.existsSync(f) ? r.fulfill({ path: f, contentType: 'image/jpeg' }) : r.fulfill({ status: 404 });
    });
    await p.goto(URL_, { waitUntil: 'networkidle', timeout: 60000 });
    await p.waitForTimeout(4000);
    const r = await p.evaluate(() => {
      const imgs = [...document.querySelectorAll('img')].filter(i => i.src.includes('branham-demo-'));
      const over = [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > document.documentElement.clientWidth + 1; }).slice(0, 8).map(e => e.tagName + '.' + String(e.className).slice(0, 60) + ' r=' + Math.round(e.getBoundingClientRect().right));
      const tabs = [...document.querySelectorAll('[role=tab]')].map(t => t.textContent.trim());
      const panels = [...document.querySelectorAll('[role=tabpanel]')].map(p => p.querySelectorAll('a img').length);
      return { sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, imgCount: imgs.length,
        broken: imgs.filter(i => i.complete && !i.naturalWidth).length, logo: (imgs.find(i => i.src.endsWith('logo.jpg')) || {}).naturalWidth,
        over, tabs, panels, ids: ['top','featured','types','work','about','estimate'].map(i => !!document.getElementById(i)),
        footer: document.body.innerText.includes('Website concept by Axiom Systems. Demo only.'),
        robots: (document.querySelector('meta[name=robots]') || {}).content };
    });
    // all-tab images loaded after scrolling
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } });
    await p.waitForTimeout(1500);
    r.allTabLoaded = await p.evaluate(() => { const pan = document.querySelector('[role=tabpanel]'); return [...pan.querySelectorAll('img')].filter(i => i.naturalWidth > 0).length; });
    // tab switching
    const tabRes = [];
    const tabs = p.locator('[role=tab]');
    for (let i = 0; i < await tabs.count(); i++) {
      await tabs.nth(i).click(); await p.waitForTimeout(400);
      tabRes.push(await p.evaluate(() => { const v = [...document.querySelectorAll('[role=tabpanel]')].filter(x => x.offsetHeight > 0); return v.map(x => x.querySelectorAll('a').length + ':' + [...x.querySelectorAll('img')].filter(i => i.naturalWidth > 0 || !i.complete).length).join('|') + ' sel=' + document.querySelector('[role=tab][aria-selected=true]').textContent.trim(); }));
    }
    r.tabRes = tabRes;
    await tabs.nth(0).click();
    r.firstTileHref = await p.evaluate(() => { const a = document.querySelector('[role=tabpanel] a'); return a && [a.getAttribute('href'), a.getAttribute('target')]; });
    if (name === 'phone') {
      r.mobileBar = await p.evaluate(() => { const n = [...document.querySelectorAll('nav')].find(n => getComputedStyle(n).position === 'fixed'); if (!n) return null; const b = n.getBoundingClientRect(); return { top: b.top, bottom: b.bottom, h: b.height, vh: innerHeight }; });
      await p.locator('summary').first().click(); await p.waitForTimeout(400);
      r.menuOpen = await p.evaluate(() => { const d = document.querySelector('details'); return d.open + ' links=' + [...d.querySelectorAll('a')].filter(a => a.offsetHeight > 0).length; });
      await p.screenshot({ path: `${OUT}/${name}-menu.png` });
      await p.locator('summary').first().click();
    }
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300);
    await p.screenshot({ path: `${OUT}/${name}-full.png`, fullPage: true });
    r.errs = errs; res[name] = r; await ctx.close();
  }
  console.log(JSON.stringify(res, null, 1)); await b.close();
})();
