// Live-site QA as a visitor: screenshots (desktop/mobile), overflow, fonts, tel links,
// WaveRez lightframe click test, tracking presence, broken images.
// Usage: NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt NODE_PATH=$(npm root -g) node tools/live_qa.cjs <outDir> <url> [url...]
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
(async () => {
  const [out, ...urls] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const url of urls) {
    const slug = (new URL(url).pathname.replace(/\//g, '-').replace(/^-|-$/g, '') || 'home');
    for (const [name, w, h, mobile] of [['desktop', 1440, 900, false], ['mobile', 390, 844, true]]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: mobile, hasTouch: mobile,
        userAgent: (mobile ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) Mobile Safari/604.1' : 'Mozilla/5.0 Chrome/128.0') + ' XtremeAudit-Claude/1.0' });
      // Node-side fetch verifies TLS with the proxy CA (NODE_EXTRA_CA_CERTS); Chromium's own store lacks it.
      await ctx.route(/^https?:/, async r => {
        // curl passes Cloudflare where headless fetches are challenged; TLS is verified via the system CA config.
        const u = r.request().url();
        if (!/xtremestpete\.com|waverez\.com|googleapis|gstatic|cloudflare|jsdelivr/.test(u)) { try { await r.fulfill({ response: await r.fetch({ timeout: 20000 }) }); } catch (e) { await r.abort(); } return; }
        try {
          const outp = execFileSync('curl', ['-sS', '-L', '-A', 'Mozilla/5.0 Chrome/128.0 XtremeAudit-Claude/1.0', '-D', '-', u], { maxBuffer: 64 * 1024 * 1024 });
          let idx = outp.lastIndexOf(Buffer.from('\r\n\r\n')); const firstBody = outp.indexOf(Buffer.from('\r\n\r\n'));
          // skip proxy 'Connection Established' and redirect header blocks: body starts after the last header block that begins with HTTP/
          let pos = 0, hdrEnd = 0; while (true) { const e = outp.indexOf(Buffer.from('\r\n\r\n'), pos); if (e < 0) break; const blk = outp.slice(pos, e).toString(); if (!blk.startsWith('HTTP/')) break; hdrEnd = e + 4; pos = hdrEnd; }
          const head = outp.slice(0, hdrEnd).toString(); const body = outp.slice(hdrEnd);
          const ct = (head.match(/content-type:\s*([^\r\n]+)/gi) || []).pop();
          await r.fulfill({ status: 200, body, contentType: ct ? ct.split(':').slice(1).join(':').trim() : undefined });
        } catch (e) { await r.abort(); }
      });
      const page = await ctx.newPage();
      const bust = url + (url.includes('?') ? '&' : '?') + 'qa=' + Date.now();
      // Cloudflare challenges headless document requests; fetch the live HTML with curl (allowed),
      // then render it with a <base> so every asset still loads from the live site.
      const ua = mobile ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) Mobile Safari/604.1 XtremeAudit-Claude/1.0' : 'Mozilla/5.0 Chrome/128.0 XtremeAudit-Claude/1.0';
      const htmlPath = `${out}/${slug}-${name}.html`;
      const code = execFileSync('curl', ['-sS', '-A', ua, '-o', htmlPath, '-w', '%{http_code}', bust]).toString();
      fs.writeFileSync(htmlPath, fs.readFileSync(htmlPath, 'utf8').replace('<head>', `<head><base href="${url}">`));
      const resp = { status: () => code };
      await page.goto('file://' + htmlPath, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.addStyleTag({ content: '.cmplz-cookiebanner,.cmplz-soft-cookiewall{display:none!important}' });
      await page.evaluate(() => document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; }));
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } window.scrollTo(0, 0); });
      await page.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 45000 }).catch(() => {});
      await page.waitForTimeout(1200);
      const info = await page.evaluate(() => ({
        overflow: document.documentElement.scrollWidth - window.innerWidth,
        h1: [...document.querySelectorAll('h1')].map(h => h.innerText.trim().slice(0, 60)),
        barlow: document.fonts.check('800 40px "Barlow Condensed"'), manrope: document.fonts.check('500 16px Manrope'),
        brokenImgs: [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.src).map(i => i.src.slice(-60)),
        tel: [...new Set([...document.querySelectorAll('a[href^="tel:"]')].map(a => a.getAttribute('href')))],
        wr: [...new Set([...document.querySelectorAll('a[href*="reservations.waverez.com"],[data-waverez-id]')].map(a => a.getAttribute('href') || 'data-waverez-id=' + a.getAttribute('data-waverez-id')))],
      }));
      await page.screenshot({ path: `${out}/${slug}-${name}-fold.png` });
      await page.screenshot({ path: `${out}/${slug}-${name}-full.png`, fullPage: true });
      let lf = 'n/a';
      if (name === 'mobile') {
        const a = page.locator('.elementor[data-elementor-type="wp-page"] a[href*="reservations.waverez.com"], .elementor[data-elementor-type="wp-page"] [data-waverez-id]').first();
        if (await a.count()) {
          await a.scrollIntoViewIfNeeded(); await a.click({ noWaitAfter: true }); await page.waitForTimeout(3500);
          lf = await page.$$eval('.waverez_popup iframe', fs => fs.map(f => f.src)); lf = JSON.stringify(lf) + ' stayed=' + page.url().startsWith('file://');
          await page.screenshot({ path: `${out}/${slug}-mobile-lightframe.png` });
        }
      }
      console.log(`${slug} ${name} status=${resp.status()} overflow=${info.overflow} h1=${JSON.stringify(info.h1)} fonts=${info.barlow}/${info.manrope} broken=${info.brokenImgs.length} tel=${info.tel} wr=${info.wr.length} lightframe=${lf}`);
      await ctx.close();
    }
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
