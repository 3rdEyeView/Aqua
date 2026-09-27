// Screenshot a local preview at desktop/tablet/mobile and verify WaveRez booking links open the lightframe.
// Usage: NODE_PATH=$(npm root -g) node tools/shots.cjs <preview.html> <outPrefix>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [file, prefix] = process.argv.slice(2);
  const url = 'file://' + path.resolve(file);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
  const hideBanner = '.cmplz-cookiebanner,.cmplz-soft-cookiewall{display:none!important}';
  const sizes = [['desktop', 1440, 900, false], ['tablet', 820, 1180, true], ['mobile', 390, 844, true]];
  for (const [name, w, h, mobile] of sizes) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: 1,
      userAgent: (mobile ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) Mobile Safari/604.1' : 'Mozilla/5.0 Chrome/128.0') + ' XtremeAudit-Claude/1.0' });
    // Chromium here has no proxy CA in its NSS store; fetch via Playwright's Node stack instead,
    // which verifies TLS against NODE_EXTRA_CA_CERTS (the proxy CA bundle). TLS is never disabled.
    await ctx.route(/^https?:/, async route => {
      try { const resp = await route.fetch({ timeout: 30000 }); await route.fulfill({ response: resp }); }
      catch (e) { await route.abort(); }
    });
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.addStyleTag({ content: hideBanner });
    await page.waitForTimeout(1500);
    // screenshots only: load every image now (production keeps loading="lazy")
    await page.evaluate(() => document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; }));
    // trigger lazy-loaded images before full-page capture
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
    await page.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 45000 }).catch(() => {});
    await page.waitForTimeout(800);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    await page.screenshot({ path: `${prefix}-${name}-fold.png` });
    await page.screenshot({ path: `${prefix}-${name}-full.png`, fullPage: true });
    console.log(name, 'horizontal overflow px:', overflow);
    if (name === 'mobile') {
      const links = await page.$$eval('a[href*="reservations.waverez.com"]', as => as.map(a => a.href));
      console.log('waverez links:', links.length, [...new Set(links)]);
      const loader = await page.$$eval('script[src*="_trip_book_widget.js"]', s => s.length);
      console.log('waverez loader scripts:', loader);
      if (links.length) {
        const a = page.locator('main a[href*="reservations.waverez.com"]').first();
        await a.scrollIntoViewIfNeeded();
        await a.click({ noWaitAfter: true });
        await page.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 45000 }).catch(() => {});
    await page.waitForTimeout(800);
        const frame = await page.$$eval('.waverez_popup iframe', fs => fs.map(f => f.src));
        console.log('lightframe iframe after click:', frame, 'still on page:', page.url() === url);
        await page.screenshot({ path: `${prefix}-mobile-lightframe.png` });
      }
    }
    await ctx.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
