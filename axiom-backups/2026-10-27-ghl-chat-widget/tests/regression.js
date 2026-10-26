// Desktop/mobile regression after installing the chat widget. Google and LeadConnector hosts are blocked here,
// so this checks the site with the widget unable to load (no errors) and what sits where the bubble will appear.
const { chromium } = require('playwright'); const fs = require('fs');
const BASE = 'https://axiomsystems.systems';
const PAGES = ['/', '/pricing/', '/add-ons/', '/faq/', '/get-started/?plan=lead-automation', '/how-it-works/', '/our-work/'];
(async () => {
  const b = await chromium.launch(); const out = {};
  for (const [label, vp] of [['desktop', { width: 1440, height: 900 }], ['mobile', { width: 390, height: 844, isMobile: true, hasTouch: true }]]) {
    for (const path of PAGES) {
      const ctx = await b.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.isMobile, hasTouch: !!vp.hasTouch });
      const p = await ctx.newPage(); const errs = []; const widgetReq = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.route(/google|doubleclick|gtag|leadconnectorhq/, r => { if (r.request().url().includes('leadconnectorhq')) widgetReq.push(r.request().url()); r.abort(); });
      const resp = await p.goto(BASE + path, { waitUntil: 'networkidle' });
      const info = await p.evaluate(() => {
        const W = innerWidth, H = innerHeight;
        const fixed = [...document.querySelectorAll('body *')].filter(e => { const s = getComputedStyle(e); return (s.position === 'fixed' || s.position === 'sticky') && e.offsetWidth > 0; })
          .map(e => { const r = e.getBoundingClientRect(); return { el: e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : ''), pos: getComputedStyle(e).position, right: Math.round(W - r.right), bottom: Math.round(H - r.bottom), w: Math.round(r.width), h: Math.round(r.height) }; });
        const tags = document.querySelectorAll('script[data-widget-id="6adf9aa5388cb81c665a7bda"]').length;
        const btn = document.querySelector('.axgs button[type=submit]'); const br = btn && btn.getBoundingClientRect();
        return { sw: document.documentElement.scrollWidth, tags, fixed, submit: br ? { right: Math.round(W - br.right), width: Math.round(br.width) } : null, form_inputs: document.querySelectorAll('.axgs form [name]').length };
      });
      out[`${label} ${path}`] = { status: resp.status(), overflow: info.sw > vp.width, js_errors: errs, widget_tags: info.tags, widget_requests: widgetReq.length, fixed_or_sticky: info.fixed, submit: info.submit, form_inputs: info.form_inputs };
      if (label === 'mobile' && path === '/') {
        const t = await p.$('.axm-toggle, [aria-label*="menu" i]'); if (t) { await t.click().catch(() => {}); await p.waitForTimeout(400); out[`${label} ${path}`].menu_opens = await p.evaluate(() => !!document.querySelector('.axm-open, [aria-expanded="true"]')); }
      }
      if (path.startsWith('/get-started')) {
        let ajax = 0; p.on('request', q => { if (q.url().includes('grunion-contact-form')) ajax++; });
        await p.click('.axgs button[type=submit]'); await p.waitForTimeout(1200);
        out[`${label} ${path}`].empty_submit_ajax = ajax;
        out[`${label} ${path}`].plan_label = await p.evaluate(() => document.querySelector('.axgs-plan')?.innerText);
      }
      await ctx.close();
    }
  }
  await b.close(); fs.writeFileSync('regression.json', JSON.stringify(out, null, 1));
  for (const [k, v] of Object.entries(out)) console.log(k, '|', v.status, 'overflow', v.overflow, 'js_errors', v.js_errors.length, 'widget_tags', v.widget_tags, 'widget_requests', v.widget_requests, '| fixed:', JSON.stringify(v.fixed_or_sticky), v.submit ? '| submit ' + JSON.stringify(v.submit) + ' inputs ' + v.form_inputs + ' empty-submit ajax ' + v.empty_submit_ajax + ' label ' + JSON.stringify(v.plan_label) : '', v.menu_opens !== undefined ? '| menu opens ' + v.menu_opens : '');
})();
