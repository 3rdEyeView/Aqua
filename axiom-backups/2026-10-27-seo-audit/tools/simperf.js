// simperf.js: full-page screenshots live vs simulated perf snippet (blocked assets + early viewport); pixel diff + JS errors
const { chromium, devices } = require('playwright'); const fs = require('fs');
const { PNG } = (() => { try { return require('pngjs'); } catch (e) { return {}; } })();
const B = 'https://axiomsystems.systems', pages = ['/', '/how-it-works/', '/our-work/', '/pricing/', '/add-ons/', '/faq/', '/get-started/', '/privacy-policy/'];
const BLOCK = /(woocommerce\/assets\/(css|js)\/|sourcebuster|order-attribution|woocommerce-analytics|ppcp-blocks-css-mini-cart|family=Roboto)/;
const THIRD = /(googletagmanager|google-analytics|googleadservices|doubleclick|stats\.wp\.com|leadconnectorhq)/;
(async () => { const b = await chromium.launch(); const out = {};
  for (const [label, dev] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['mobile', devices['Pixel 7']]]) for (const path of pages) {
    const shots = {};
    for (const mode of ['live', 'sim']) { const ctx = await b.newContext(dev); await ctx.route(THIRD, r => r.abort());
      if (mode === 'sim') { await ctx.route(BLOCK, r => r.abort()); await ctx.route(u => u.pathname === path && u.hostname === 'axiomsystems.systems', async r => { const resp = await r.fetch(); let h = await resp.text(); h = h.replace('<meta charset="UTF-8">', '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />'); await r.fulfill({ response: resp, body: h }); }); }
      const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/ERR_FAILED|net::/.test(m.text())) errs.push('console: ' + m.text().slice(0, 120)); });
      await p.goto(B + path + '?nc=' + Date.now(), { waitUntil: 'load', timeout: 60000 }); await p.waitForTimeout(1500);
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
      await p.waitForTimeout(800);
      const f = `tests/sim/${label}${path.replace(/\//g, '_') || '_'}${mode}.png`; await p.screenshot({ path: f, fullPage: true });
      shots[mode] = { f, errs, h: await p.evaluate(() => document.documentElement.scrollHeight), menu: await p.evaluate(() => !!document.querySelector('.axm-toggle')) };
      await ctx.close(); }
    out[label + ' ' + path] = { liveH: shots.live.h, simH: shots.sim.h, liveErr: shots.live.errs, simErr: shots.sim.errs, menu: [shots.live.menu, shots.sim.menu], files: [shots.live.f, shots.sim.f] };
    console.log((label + ' ' + path).padEnd(26), 'height', shots.live.h, shots.sim.h, '| errs', shots.live.errs.length, shots.sim.errs.length, shots.sim.errs.slice(0, 2).join(' ; '));
  }
  fs.writeFileSync('tests/sim/results.json', JSON.stringify(out, null, 1)); await b.close(); })();
