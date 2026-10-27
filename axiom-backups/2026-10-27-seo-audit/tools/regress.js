// regress.js <out.json>: functional regression on live pages (no form submission reaches the server).
const { chromium } = require('playwright'); const fs = require('fs');
const B = 'https://axiomsystems.systems', pages = ['/', '/how-it-works/', '/our-work/', '/pricing/', '/add-ons/', '/faq/', '/get-started/', '/privacy-policy/'];
(async () => {
  const b = await chromium.launch(); const res = {};
  for (const w of [1440, 390]) for (const path of pages) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 }, isMobile: w < 768, hasTouch: w < 768 });
    await ctx.route(/(googletagmanager|google-analytics|googleadservices|doubleclick|stats\.wp\.com|leadconnectorhq)/, r => r.abort());
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    const html = await (await p.goto(B + path + '?nc=' + Date.now(), { waitUntil: 'load', timeout: 60000 })).text(); await p.waitForTimeout(800);
    const r = await p.evaluate(() => ({ overflow: document.documentElement.scrollWidth > innerWidth, tel: document.querySelectorAll('a[href="tel:+17275917527"]').length, h1: [...document.querySelectorAll('h1')].map(h => h.innerText.replace(/\s+/g, ' ')), getStarted: [...document.querySelectorAll('a')].filter(a => a.pathname.startsWith('/get-started')).length }));
    r.gtag = /GT-55XGH597/.test(html); r.chat = (html.match(/data-widget-id="6adfdfee388cb81c668e729a"/g) || []).length; r.lead = /AW-17889231515\/C8k6CJn4q6YdEJuFoNJC/.test(html); r.errors = errs;
    if (w === 390) { const t = await p.$('.axm-toggle'); if (t) { await t.click(); await p.waitForTimeout(400); r.menuOpen = await p.evaluate(() => !document.querySelector('.axm-panel').hidden && document.querySelectorAll('.axm-panel a').length); } }
    res[w + ' ' + path] = r; await ctx.close();
  }
  // Get Started form: plan labels and empty-submit block (no network submission expected)
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } }); await ctx.route(/(googletagmanager|google-analytics|googleadservices|doubleclick|stats\.wp\.com|leadconnectorhq)/, r => r.abort());
  const p = await ctx.newPage(); const posts = []; p.on('request', q => { if (q.method() === 'POST') posts.push(q.url()); });
  for (const plan of ['essential', 'growth', 'lead-automation', 'marketing']) {
    await p.goto(`${B}/get-started/?plan=${plan}&nc=${Date.now()}`, { waitUntil: 'load' }); await p.waitForTimeout(600);
    res['plan ' + plan] = await p.evaluate(() => { const f = document.querySelector('form'); return { fields: f ? [...f.querySelectorAll('input,textarea,select')].filter(i => i.type !== 'hidden').map(i => i.name).length : 0, label: (document.body.innerText.match(/Axiom [A-Za-z ]+— [^\n]*/) || [''])[0] }; });
  }
  const btn = await p.$('form [type=submit], form button'); posts.length = 0; if (btn) { await btn.click(); await p.waitForTimeout(1500); }
  res['empty submit'] = { posts: posts.filter(u => !/nc=/.test(u)), stillOnPage: p.url().includes('/get-started/') };
  await b.close(); fs.writeFileSync(process.argv[2], JSON.stringify(res, null, 1));
  for (const [k, v] of Object.entries(res)) console.log(k.padEnd(22), JSON.stringify(v));
})();
