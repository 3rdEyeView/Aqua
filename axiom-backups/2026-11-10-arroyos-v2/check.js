// Checks the built preview at desktop and phone sizes and writes screenshots to shots/.
const { chromium, devices } = require('playwright');
const path = require('path');
const url = 'file://' + path.join(__dirname, 'arroyo-v2-preview.html');
const out = (n) => path.join(__dirname, 'shots', n);
(async () => {
  const browser = await chromium.launch();
  const runs = [
    ['desktop', { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 }],
    ['mobile', { ...devices['iPhone 13'] }],
    ['mobile-reduced-motion', { ...devices['iPhone 13'], reducedMotion: 'reduce' }],
  ];
  for (const [name, opts] of runs) {
    const ctx = await browser.newContext(opts);
    const page = await ctx.newPage();
    const external = [], errors = [];
    page.on('request', (r) => { if (!/^(file|data|blob):/.test(r.url())) external.push(r.url()); });
    page.on('pageerror', (e) => errors.push(e.message));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(url, { waitUntil: 'load' });
    await page.waitForTimeout(2500);
    const r = { name };
    r.video = await page.evaluate(() => { const v = document.querySelector('.hero video'); return { hasSrc: !!v.src, playing: !v.paused && v.currentTime > 0, muted: v.muted, loop: v.loop, inline: v.playsInline, w: v.videoWidth, h: v.videoHeight, dur: v.duration }; });
    r.hscroll = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    r.fonts = await page.evaluate(() => [document.fonts.check('700 40px "Barlow Condensed"'), document.fonts.check('400 16px Figtree')]);
    r.heroFits = await page.evaluate(() => { const b = document.querySelector('.hero__act').getBoundingClientRect(); return b.bottom <= window.innerHeight && b.top > 0; });
    if (name === 'mobile-reduced-motion') { await page.screenshot({ path: out('mobile-reduced-motion-hero.jpg') }); console.log(JSON.stringify(r)); await ctx.close(); continue; }
    await page.screenshot({ path: out(name + '-hero.jpg') });
    // estimate buttons all point at #estimate; tel links
    r.estimateLinks = await page.$$eval('a[href="#estimate"]', (a) => a.length);
    r.telLinks = await page.$$eval('a[href="tel:+19419621124"]', (a) => a.length);
    // navigation
    if (name === 'mobile') {
      await page.click('.hd__burger'); await page.waitForTimeout(200);
      r.menuOpen = await page.isVisible('.mnav'); await page.screenshot({ path: out('mobile-menu.jpg') });
      await page.click('.mnav a[href="#work"]');
    } else { await page.click('.hd__nav a[href="#work"]'); }
    await page.waitForTimeout(2500);
    r.navToWork = await page.evaluate(() => Math.abs(document.getElementById('work').getBoundingClientRect().top - document.querySelector('.hd').offsetHeight) < 8);
    r.menuClosedAfterNav = !(await page.isVisible('.mnav'));
    await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(700);
    // hero estimate button
    await page.click('.hero__act a[href="#estimate"]'); await page.waitForTimeout(2500);
    r.heroBtnToEstimate = await page.evaluate(() => Math.abs(document.getElementById('estimate').getBoundingClientRect().top - document.querySelector('.hd').offsetHeight) < 8);
    // form: empty submit shows errors
    await page.click('#est-form button[type=submit]'); await page.waitForTimeout(300);
    r.errorsOnEmpty = await page.$$eval('#est-form .is-bad', (e) => e.length);
    await page.fill('#f-phone', '123'); await page.fill('#f-email', 'nope'); await page.click('#est-form button[type=submit]');
    r.errorsOnBadPhoneEmail = await page.$$eval('#est-form .is-bad', (e) => e.length);
    await page.addStyleTag({ content: '.hd,.mbar{visibility:hidden}' });
    await page.locator('#est-form').screenshot({ path: out(name + '-form-errors.png') });
    await page.addStyleTag({ content: '.hd,.mbar{visibility:visible}' });
    for (const sel of ['input[name=property_type][value=Residential]', 'input[name=services][value="Lawn Maintenance"]', 'input[name=services][value="Tree & Palm Services"]']) {
      await page.locator(sel).evaluate((e) => e.scrollIntoView({ block: 'center', behavior: 'instant' }));
      await page.locator(sel).locator('xpath=..').click();
    }
    r.chipsChecked = await page.$$eval('#est-form input:checked', (e) => e.length);
    await page.fill('#f-first', 'Jordan'); await page.fill('#f-last', 'Sample');
    await page.fill('#f-phone', '(941) 555-0142'); await page.fill('#f-email', 'jordan@example.com');
    await page.fill('#f-addr', '123 Palm Terrace, Lakewood Ranch'); await page.selectOption('#f-when', 'Within a month');
    await page.click('#est-form button[type=submit]'); await page.waitForTimeout(500);
    r.confirmationShown = await page.isVisible('#est-done');
    r.confirmationInView = await page.evaluate(() => { const b = document.querySelector('#est-done h3').getBoundingClientRect(); return b.top > document.querySelector('.hd').offsetHeight && b.bottom < innerHeight; }); r.formHidden = !(await page.isVisible('#est-form'));
    await page.addStyleTag({ content: '.hd,.mbar{visibility:hidden}' });
    await page.locator('.form').screenshot({ path: out(name + '-form-confirmation.png') });
    await page.addStyleTag({ content: '.hd,.mbar{visibility:visible}' });
    await page.click('#d-reset'); r.resetWorks = await page.isVisible('#est-form');
    r.mobileBar = await page.isVisible('.mbar');
    r.external = external; r.errors = errors;
    await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(500);
    // full page (lazy images: scroll through first)
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 80)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(600);
    r.brokenImgs = await page.$$eval('img', (i) => i.filter((x) => !x.complete || !x.naturalWidth).length);
    await page.addStyleTag({ content: '.mbar{display:none!important}' }); // fixed bar would be stamped mid-page in a full-page capture
    await page.screenshot({ path: out(name + '-full.jpg'), fullPage: true, quality: 80 });
    console.log(JSON.stringify(r));
    await ctx.close();
  }
  await browser.close();
})();
