// Checks the V3 demo at desktop and phone sizes; writes screenshots to shots/.
const { chromium, devices } = require('playwright');
const path = require('path');
const url = 'file://' + path.join(__dirname, 'arroyo-v3-sales-demo.html');
const out = (n) => path.join(__dirname, 'shots', n);
(async () => {
  const browser = await chromium.launch();
  const runs = [
    ['desktop', { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 }],
    ['mobile', { ...devices['iPhone 13'] }],
    ['mobile-reduced', { ...devices['iPhone 13'], reducedMotion: 'reduce' }],
  ];
  for (const [name, opts] of runs) {
    const ctx = await browser.newContext(opts);
    const page = await ctx.newPage();
    const external = [], errors = [];
    page.on('request', (r) => { if (!/^(file|data|blob):/.test(r.url())) external.push(r.url()); });
    page.on('pageerror', (e) => errors.push(e.message));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(url, { waitUntil: 'load' });
    await page.waitForTimeout(2000);
    const r = { name };
    r.mode = await page.evaluate(() => document.documentElement.className);
    r.video = await page.evaluate(() => { const v = document.querySelector('.rv video'); return { hasSrc: !!v.src, playing: !v.paused && v.currentTime > 0 }; });
    r.hscroll = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    const visibleCta = () => page.evaluate(() => [...document.querySelectorAll('.view-home a[href="#estimate"]')].filter((a) => { const b = a.getBoundingClientRect(), s = getComputedStyle(a); if (s.visibility === 'hidden' || +s.opacity < .5 || b.width === 0) return false; const x = b.left + b.width / 2, y = b.top + b.height / 2; if (y < 0 || y > innerHeight) return false; const t = document.elementFromPoint(x, y); return t && (t === a || a.contains(t)); }).length);
    if (name === 'desktop') {
      const travel = await page.evaluate(() => document.querySelector('.rv').offsetHeight - innerHeight);
      r.ctaAt = {};
      for (const p of [0, 0.32, 0.4, 0.66, 0.82, 1]) {
        await page.evaluate((y) => window.scrollTo(0, y), Math.round(travel * p)); await page.waitForTimeout(350);
        r.ctaAt[p] = await visibleCta();
        await page.screenshot({ path: out(`desktop-reveal-${String(p).replace('.', '_')}.jpg`), quality: 82 });
      }
      await page.click('.rv__rail button[data-to="0"]'); await page.waitForTimeout(4000);
      r.railBackToStart = await page.evaluate(() => scrollY < 60);
    } else {
      await page.screenshot({ path: out(name + '-01-intro.jpg'), quality: 85 });
      r.ctaAt = {};
      for (const [k, sel] of [['type', '.rv__type'], ['project', '.rv__proj']]) {
        await page.evaluate((s) => { const e = document.querySelector(s); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - (s === '.rv__proj' ? 0 : 60)); }, sel);
        await page.waitForTimeout(1300);
        r.ctaAt[k] = await visibleCta();
        await page.screenshot({ path: out(`${name}-0${k === 'type' ? 2 : 3}-${k}.jpg`), quality: 85 });
      }
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 150)); } window.scrollTo(0, 0); }); await page.waitForTimeout(800);
      r.brokenImgs = await page.$$eval('.view-home img', (i) => i.filter((x) => !x.complete || !x.naturalWidth).length);
    }
    if (name !== 'mobile-reduced') {
      // lead view
      await page.click('.pbar button[data-view="lead"]'); await page.waitForTimeout(300);
      r.leadView = await page.isVisible('#lead-view') && !(await page.isVisible('.view-home .rv'));
      await page.screenshot({ path: out(name + '-lead-0-start.jpg'), quality: 85 });
      await page.click('#ld-start'); r.formOpen = await page.isVisible('#ph-form');
      r.source = await page.textContent('#ph-url');
      await page.fill('#l-phone', '12'); await page.click('#ld-s1'); r.validation = await page.$$eval('#ph-form .is-bad', (e) => e.length);
      await page.fill('#l-phone', '(941) 555-0142'); await page.click('#ph-form button[type=submit]'); await page.waitForTimeout(700);
      r.m1 = { lead: (await page.textContent('#crm-lead')).replace(/\s+/g, ' '), src: (await page.textContent('#crm-src')).slice(0, 60), stage: await page.$eval('.col.is-on h3', (e) => e.textContent), events: await page.$$eval('#crm-tl .ev b', (e) => e.map((x) => x.textContent)), sms: await page.$$eval('#ph-msgs .msg--sms', (e) => e.length) };
      await page.evaluate(() => window.scrollTo(0, 0)); await page.screenshot({ path: out(name + '-lead-1-new.jpg'), quality: 85, fullPage: name === 'mobile' });
      await page.click('#ld-s2'); await page.waitForTimeout(600);
      r.m2 = { clock: await page.textContent('#ld-clock'), stage: await page.$eval('.col.is-on h3', (e) => e.textContent), auto: await page.textContent('#auto-next') };
      await page.screenshot({ path: out(name + '-lead-2-followup.jpg'), quality: 85 });
      await page.click('#ld-s3b'); await page.waitForTimeout(600);
      r.m3 = { clock: await page.textContent('#ld-clock'), stage: await page.$eval('.col.is-on h3', (e) => e.textContent), auto: await page.textContent('#auto-state'), top: await page.$eval('#crm-tl .ev b', (e) => e.textContent) };
      await page.evaluate(() => window.scrollTo(0, 0)); await page.screenshot({ path: out(name + '-lead-3-booked.jpg'), quality: 85, fullPage: name === 'mobile' });
      // reset, then the no-SMS + reply path
      await page.click('#ld-reset'); r.reset = (await page.isVisible('#ph-ad')) && (await page.isVisible('#crm-empty')) && (await page.$$eval('#crm-tl .ev', (e) => e.length)) === 0;
      await page.click('#ld-start'); await page.uncheck('#l-sms'); await page.click('#ld-s1'); await page.click('#ld-s3a'); await page.waitForTimeout(400);
      r.noSms = { sms: await page.$$eval('#ph-msgs .msg--sms', (e) => e.length), skipped: await page.$$eval('#crm-tl .ev b', (e) => e.some((x) => x.textContent === 'Text not sent')), stage: await page.$eval('.col.is-on h3', (e) => e.textContent), optin: (await page.textContent('#crm-lead')).includes('No') };
      await page.click('#ld-reset');
      await page.click('.pbar button[data-view="home"]'); r.backHome = await page.isVisible('.view-home .rv');
    }
    r.external = external; r.errors = errors;
    console.log(JSON.stringify(r));
    await ctx.close();
  }
  await browser.close();
})();
