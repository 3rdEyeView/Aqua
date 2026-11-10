// Checks both offline files at desktop and phone sizes, takes hero screenshots at the three stages, and records video.
const { chromium, devices } = require('playwright');
const path = require('path'); const fs = require('fs');
const file = (n) => 'file://' + path.join(__dirname, n); const out = (n) => path.join(__dirname, 'shots', n);
(async () => {
  const b = await chromium.launch();
  for (const [variant, f] of [['v4', 'arroyo-v4-higgsfield-preview.html'], ['current', 'arroyo-current-hero-reference.html']])
    for (const [name, o] of [['desktop', { viewport: { width: 1280, height: 720 } }], ['mobile', { ...devices['iPhone 13'] }]]) {
      const dir = path.join(__dirname, 'rec', `${variant}-${name}`); fs.rmSync(dir, { recursive: true, force: true });
      const c = await b.newContext({ ...o, recordVideo: { dir, size: name === 'desktop' ? { width: 1280, height: 720 } : { width: 390, height: 664 } } });
      const p = await c.newPage(); const ext = [], errs = [];
      p.on('request', (r) => { if (!/^(file|data|blob):/.test(r.url())) ext.push(r.url().slice(0, 80)); });
      p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text().slice(0, 140)); });
      const t0 = Date.now(); await p.goto(file(f), { waitUntil: 'load' });
      const r = { variant, name };
      const state = () => p.evaluate(() => { const h = document.getElementById('hero'), v = h.querySelector('video'), c = h.querySelector('.v4-chip'); const b = [...h.querySelectorAll('a')].find((a) => /Estimate/.test(a.textContent)).getBoundingClientRect(); const h1 = h.querySelector('h1').getBoundingClientRect(); return { t: +v.currentTime.toFixed(1), paused: v.paused, chip: c ? c.innerText.trim() : null, settled: h.classList.contains('v4-settled'), btnInView: b.top > 0 && b.bottom <= innerHeight, h1InView: h1.top >= 0 && h1.bottom <= innerHeight }; });
      await p.waitForTimeout(3000); r.at3 = await state(); await p.screenshot({ path: out(`${variant}-${name}-1-drone.jpg`), quality: 85 });
      if (variant === 'v4') {
        await p.waitForFunction(() => document.querySelector('#hero video').currentTime > 9.2, null, { timeout: 30000 }); r.ai = await state(); await p.screenshot({ path: out(`${variant}-${name}-2-ai-transition.jpg`), quality: 85 });
        await p.waitForFunction(() => document.getElementById('hero').classList.contains('v4-settled'), null, { timeout: 30000 }); await p.waitForTimeout(1500); r.photo = await state(); await p.screenshot({ path: out(`${variant}-${name}-3-real-photo.jpg`), quality: 85 });
        await p.waitForFunction(() => !document.getElementById('hero').classList.contains('v4-settled'), null, { timeout: 30000 }); await p.waitForTimeout(800); r.loopedBack = await state();
        await p.click('#hero .e-background-video__pause', { force: true }); await p.waitForTimeout(300); r.pauseWorks = (await state()).paused;
        await p.click('#hero .e-background-video__play', { force: true }); await p.waitForTimeout(500); r.playWorks = !(await state()).paused;
      } else { await p.waitForTimeout(18000); r.later = await state(); }
      r.recordedSeconds = Math.round((Date.now() - t0) / 1000);
      // rest of page: nav/menu, FAQ, estimate anchor
      if (name === 'mobile') { const menu = p.locator('.axm-toggle, header [class*="accordion"] button, header summary').first(); r.menuControl = await menu.count(); }
      r.estimateLinks = await p.$$eval('a[href="#estimate"]', (a) => a.length); r.telLinks = await p.$$eval('a[href^="tel:"]', (a) => a.length); r.mailto = await p.$$eval('a[href^="mailto:info@arroyoslawncare.com"]', (a) => a.length);
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } });
      r.brokenImgs = await p.$$eval('img', (i) => i.filter((x) => !x.complete || !x.naturalWidth).length);
      r.hscroll = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth); r.height = await p.evaluate(() => document.documentElement.scrollHeight);
      r.leadDemo = await p.evaluate(() => !!document.getElementById('axl-lead-tpl')); r.external = ext; r.errors = errs;
      console.log(JSON.stringify(r)); await c.close();
    }
  await b.close();
})();
