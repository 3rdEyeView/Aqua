// Live QA after publish (2026-10-28 pricing restructure). Google + LeadConnector hosts are blocked so no tags fire.
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = 'https://axiomsystems.systems';
const PAGES = ['/', '/pricing/', '/add-ons/', '/faq/', '/get-started/', '/how-it-works/', '/our-work/', '/privacy-policy/'];
const OLD = ['$297', '$597', '$1,500', '$349', '$648', 'GoHighLevel', 'paid directly to Google', 'Paid separately to Google', 'included in the $599', 'included in the $597'];
(async () => {
  const b = await chromium.launch(); const out = { pages: {}, links: {}, form: {} };
  const bust = () => `nc=${Date.now()}`;
  for (const path of PAGES) {
    const r = { widths: {} };
    for (const w of [1440, 1024, 768, 390]) {
      const p = await b.newPage({ viewport: { width: w, height: 900 } });
      const errs = []; p.on('pageerror', e => errs.push(e.message));
      await p.route(/google|doubleclick|gtag|leadconnector/, x => x.abort());
      const resp = await p.goto(`${BASE}${path}?${bust()}`, { waitUntil: 'networkidle' });
      const info = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, text: document.body.innerText, html: document.documentElement.outerHTML,
        links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')) }));
      r.widths[w] = { status: resp.status(), overflow: info.sw > w, jsErrors: errs };
      if (w === 1440) {
        const head = info.html.slice(0, info.html.indexOf('</head>'));
        r.oldRefs = OLD.filter(q => info.text.includes(q) || head.includes(q.trim()));
        r.htmlOld = ['$297', '$597', '$1,500', '$349'].filter(q => info.html.includes(q));
        r.gt = (info.html.match(/gtag\/js\?id=GT-55XGH597/g) || []).length;
        r.adsCfg = (info.html.match(/AW-17878870459/g) || []).length;
        r.ghl = (info.html.match(/data-widget-id="6adfdfee388cb81c668e729a"/g) || []).length;
        r.tel = info.html.includes('tel:+17275917527');
        r.ogImage = (head.match(/og:image" content="([^"]+)"/) || [])[1];
        r.desc = (head.match(/name="description" content="([^"]+)"/) || [])[1];
        r.title = await p.title(); r.links = [...new Set(info.links)];
        r.prices = ['$299', '$599', '$0 setup'].filter(q => info.text.includes(q));
        r.disclaimer = (info.text.match(/Advertising spend is not included\. We recommend considering approximately \$500\/month to start, but your advertising budget is flexible and paid separately to Google and\/or Meta\./g) || []).length;
        r.faqSchema = (info.html.match(/"@type":"FAQPage"/g) || []).length;
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
  for (const plan of ['essential', 'essentials', 'growth', 'custom-quote', 'marketing', 'lead-automation', 'lead-response', 'follow-up-automation', 'review-automation', 'bogus', '']) {
    const p = await b.newPage(); await p.route(/google|doubleclick|gtag|leadconnector/, x => x.abort());
    let ajax = 0; p.on('request', q => { if (q.url().includes('grunion-contact-form')) ajax++; });
    await p.goto(`${BASE}/get-started/?${plan ? 'plan=' + plan + '&' : ''}utm_source=test&gclid=TEST123&${bust()}`, { waitUntil: 'networkidle' });
    const f = await p.evaluate(() => ({ label: document.querySelector('.axgs-plan')?.innerText.replace(/\n/g, ' '),
      hidden: [...document.querySelectorAll('.axgs input[type=hidden]')].map(i => i.value).filter(v => v.includes('plan=') || v.includes('no plan')),
      url: location.search.includes('gclid=TEST123') && location.search.includes('utm_source=test'),
      leadJs: !!document.getElementById('axgs-lead-js'), sendTo: document.documentElement.outerHTML.includes('AW-17889231515\\/C8k6CJn4q6YdEJuFoNJC'),
      fields: document.querySelectorAll('.axgs input:not([type=hidden]), .axgs textarea').length }));
    if (plan === 'growth') { await p.click('.axgs button[type=submit]').catch(e => f.clickErr = e.message); await p.waitForTimeout(1500); f.ajaxOnEmptySubmit = ajax; }
    out.form[plan || '(none)'] = f; await p.close();
  }
  await b.close();
  fs.writeFileSync('live-results.json', JSON.stringify(out, null, 1));
  for (const [k, r] of Object.entries(out.pages)) console.log(k, '|', r.title, '| old:', r.oldRefs, r.htmlOld, '| bad widths:', Object.entries(r.widths).filter(([, v]) => v.overflow || v.jsErrors.length || v.status !== 200).map(([w, v]) => w + JSON.stringify(v)), '| GT', r.gt, 'AW', r.adsCfg, 'GHL', r.ghl, 'tel', r.tel, 'faq', r.faqSchema, '| prices', r.prices.join(' '), '| og', (r.ogImage || '').split('/').pop(), '| disclaimer', r.disclaimer);
  console.log('links not 200:', Object.entries(out.links).filter(([, s]) => s !== 200));
  for (const [k, f] of Object.entries(out.form)) console.log(k.padEnd(22), JSON.stringify(f));
})();
