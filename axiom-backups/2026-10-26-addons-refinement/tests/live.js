// Live QA after publish. Google domains are blocked so no tags fire.
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = 'https://axiomsystems.systems';
const PAGES = ['/', '/pricing/', '/add-ons/', '/faq/', '/get-started/', '/how-it-works/', '/our-work/'];
const OLD = ['$149', '$199', '$647', '$48/', 'Save $48', 'Lead Response', 'Follow-Up Automation', 'each completed job'];
(async () => {
  const b = await chromium.launch(); const out = { pages: {}, links: {}, form: {}, errors: [] };
  const bust = () => `nc=${Date.now()}`;
  for (const path of PAGES) {
    const r = { widths: {} };
    for (const w of [1440, 1024, 768, 390]) {
      const p = await b.newPage({ viewport: { width: w, height: 900 } });
      const errs = []; p.on('pageerror', e => errs.push(e.message));
      await p.route(/google|doubleclick|gtag/, x => x.abort());
      const resp = await p.goto(`${BASE}${path}?${bust()}`, { waitUntil: 'networkidle' });
      const info = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, text: document.body.innerText, html: document.documentElement.outerHTML,
        links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')) }));
      r.widths[w] = { status: resp.status(), overflow: info.sw > w, jsErrors: errs };
      if (w === 1440) {
        r.oldRefs = OLD.filter(q => info.text.includes(q));
        r.gt = info.html.includes('GT-55XGH597'); r.tel = info.html.includes('tel:+17275917527');
        r.title = await p.title(); r.links = [...new Set(info.links)];
        r.prices = ['$299', '$349', '$599', '$1,500', '$648', 'Save $49'].filter(q => info.text.includes(q));
      }
      await p.close();
    }
    out.pages[path] = r;
  }
  const links = new Set(); Object.values(out.pages).forEach(r => r.links.forEach(l => { if (l.startsWith('/') || l.startsWith(BASE)) links.add(l); }));
  for (const l of links) {
    const u = l.startsWith('/') ? BASE + l : l;
    const res = await fetch(u.split('#')[0], { redirect: 'manual' }); out.links[l] = res.status;
  }
  for (const plan of ['lead-automation', 'lead-response', 'follow-up-automation', 'growth', 'essential', 'marketing']) {
    const p = await b.newPage(); await p.route(/google|doubleclick|gtag/, x => x.abort());
    let ajax = 0; p.on('request', q => { if (q.url().includes('grunion-contact-form')) ajax++; });
    await p.goto(`${BASE}/get-started/?plan=${plan}&${bust()}`, { waitUntil: 'networkidle' });
    const f = await p.evaluate(() => ({ label: document.querySelector('.axgs-plan')?.innerText,
      hidden: [...document.querySelectorAll('.axgs input[type=hidden]')].map(i => i.value).filter(v => v.includes('plan=')),
      leadJs: !!document.getElementById('axgs-lead-js'), sendTo: document.documentElement.outerHTML.includes('AW-17889231515/C8k6CJn4q6YdEJuFoNJC') }));
    if (plan === 'lead-automation') { await p.click('.axgs button[type=submit]').catch(e => f.clickErr = e.message); await p.waitForTimeout(1500); f.ajaxOnEmptySubmit = ajax; }
    out.form[plan] = f; await p.close();
  }
  await b.close();
  fs.writeFileSync('live-results.json', JSON.stringify(out, null, 1));
  for (const [k, r] of Object.entries(out.pages)) console.log(k, r.title, '| old:', r.oldRefs, '| overflow:', Object.entries(r.widths).filter(([, v]) => v.overflow || v.jsErrors.length || v.status !== 200).map(([w]) => w), '| GT', r.gt, 'tel', r.tel, '| prices', r.prices.join(' '));
  console.log('links not 200:', Object.entries(out.links).filter(([, s]) => s !== 200));
  console.log(JSON.stringify(out.form, null, 1));
})();
