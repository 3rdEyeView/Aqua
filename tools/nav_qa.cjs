// Mobile navigation QA on live pages: opens the JetBlocks mobile menu, screenshots open/closed states,
// reports the panel's computed background/position/z-index, checks each menu link is the topmost element
// at its own position (not covered), and optionally clicks the header Book link.
// Usage: NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt NODE_PATH=$(npm root -g) node tools/nav_qa.cjs <outDir> <widths comma> <url> [url...]
const { chromium, webkit } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');

function curlFetch(u, ua) {
  const outp = execFileSync('curl', ['-sS', '-L', '-A', ua, '-D', '-', u], { maxBuffer: 64 * 1024 * 1024 });
  let pos = 0, hdrEnd = 0;
  while (true) { const e = outp.indexOf(Buffer.from('\r\n\r\n'), pos); if (e < 0) break; if (!outp.slice(pos, e).toString().startsWith('HTTP/')) break; hdrEnd = e + 4; pos = hdrEnd; }
  const head = outp.slice(0, hdrEnd).toString();
  const ct = (head.match(/content-type:\s*([^\r\n]+)/gi) || []).pop();
  return { body: outp.slice(hdrEnd), contentType: ct ? ct.split(':').slice(1).join(':').trim() : undefined };
}

(async () => {
  const [out, widthsArg, ...urls] = process.argv.slice(2);
  const widths = widthsArg.split(',').map(Number);
  const ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1 XtremeAudit-Claude/1.0';
  const engines = [['chromium', chromium, { executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }]];
  try { if (fs.existsSync('/opt/pw-browsers') && fs.readdirSync('/opt/pw-browsers').some(d => d.startsWith('webkit'))) engines.push(['webkit', webkit, {}]); } catch (e) {}
  for (const [ename, engine, opts] of engines) {
    const browser = await engine.launch(opts);
    for (const url of urls) {
      const slug = (new URL(url).pathname.replace(/\//g, '-').replace(/^-|-$/g, '') || 'home');
      const htmlPath = `${out}/${slug}.html`;
      execFileSync('curl', ['-sS', '-A', ua, '-o', htmlPath, url + (url.includes('?') ? '&' : '?') + 'qa=' + Date.now()]);
      fs.writeFileSync(htmlPath, fs.readFileSync(htmlPath, 'utf8').replace('<head>', `<head><base href="${url}">`));
      for (const w of widths) {
        const ctx = await browser.newContext({ viewport: { width: w, height: 844 }, isMobile: ename === 'chromium', hasTouch: true, userAgent: ua });
        await ctx.route(/^https?:/, async r => {
          const u = r.request().url();
          if (!/xtremestpete\.com|waverez\.com|googleapis|gstatic/.test(u)) { try { await r.fulfill({ response: await r.fetch({ timeout: 20000 }) }); } catch (e) { await r.abort(); } return; }
          try { const f = curlFetch(u, 'Mozilla/5.0 Chrome/128.0 XtremeAudit-Claude/1.0'); await r.fulfill({ status: 200, body: f.body, contentType: f.contentType }); } catch (e) { await r.abort(); }
        });
        const page = await ctx.newPage();
        await page.goto('file://' + htmlPath, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.addStyleTag({ content: '.cmplz-cookiebanner,.cmplz-soft-cookiewall{display:none!important}' });
        if (process.env.INJECT_CSS) await page.addStyleTag({ content: fs.readFileSync(process.env.INJECT_CSS, 'utf8') }); // preview a fix before publishing
        await page.waitForTimeout(2500);
        const tag = `${ename}-${slug}-${w}`;
        await page.screenshot({ path: `${out}/${tag}-closed.png` });
        const trig = page.locator('.jet-nav__mobile-trigger').first();
        if (!(await trig.isVisible())) { console.log(tag, 'mobile trigger not visible (desktop nav shown)'); await ctx.close(); continue; }
        await trig.click();
        await page.waitForTimeout(900);
        await page.screenshot({ path: `${out}/${tag}-open.png` });
        const info = await page.evaluate(() => {
          const wrap = document.querySelector('.jet-nav-wrap.jet-mobile-menu');
          const nav = wrap && wrap.querySelector('.jet-nav');
          const cs = nav ? getComputedStyle(nav) : null;
          const links = [...(nav ? nav.querySelectorAll('.menu-item-link-top') : [])];
          const covered = links.filter(a => { const r = a.getBoundingClientRect(); if (!r.width) return false; const el = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return !(el && (a === el || a.contains(el))); }).map(a => a.innerText.trim());
          const vis = links.filter(a => { const r = a.getBoundingClientRect(); return r.width && r.bottom > 0 && r.top < innerHeight; }).map(a => a.innerText.trim());
          const r = nav ? nav.getBoundingClientRect() : {};
          return { active: !!(wrap && wrap.classList.contains('jet-mobile-menu-active')), bg: cs && cs.backgroundColor, pos: cs && cs.position, z: cs && cs.zIndex, top: Math.round(r.top), height: Math.round(r.height), width: Math.round(r.width), links: links.map(a => a.innerText.trim() + '→' + (a.getAttribute('href') || '').replace('https://xtremestpete.com', '')), visible: vis.length, covered };
        });
        console.log(tag, JSON.stringify(info));
        await ctx.close();
      }
    }
    await browser.close();
  }
})().catch(e => { console.error(e); process.exit(1); });
