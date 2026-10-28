// Customer-facing provider-name audit: visible text, head meta, JSON-LD, alt/title/aria/placeholder attributes,
// form labels and the success message template. Script/style URLs and class names are internal and not counted.
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = 'https://axiomsystems.systems';
const PAGES = ['/', '/pricing/', '/add-ons/', '/faq/', '/get-started/', '/how-it-works/', '/our-work/', '/privacy-policy/', '/no-such-page-xyz/'];
const TERMS = /GoHighLevel|HighLevel|\bGHL\b|LeadConnector|Lead Connector|Elementor|WordPress|Kinsta|FluentSMTP|Fluent SMTP|Jetpack|Adspirer|Akismet|Yoast|WooCommerce|Cloudflare|Turnstile|Site Kit|Twilio|Mailgun|Stripe|Calendly|Zapier|Angie/gi;
(async () => {
  const b = await chromium.launch(); const out = {};
  for (const path of PAGES) for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.route(/google|doubleclick|gtag|leadconnector/, x => x.abort());
    const resp = await p.goto(`${BASE}${path}?nc=${Date.now()}`, { waitUntil: 'networkidle' });
    if (w === 390) { await p.click('.axm-toggle, [aria-controls*=axm], button[aria-label*=enu]').catch(() => {}); await p.waitForTimeout(300); }
    const r = await p.evaluate((src) => {
      const re = new RegExp(src, 'gi'), hits = [];
      const add = (where, s) => { if (!s) return; let m; re.lastIndex = 0; while ((m = re.exec(s))) hits.push([where, m[0], s.slice(Math.max(0, m.index - 70), m.index + 70).replace(/\s+/g, ' ')]); };
      add('text', document.body.innerText);
      add('title', document.title);
      document.querySelectorAll('meta[content]').forEach(m => add('meta:' + (m.name || m.getAttribute('property')), m.content));
      document.querySelectorAll('script[type="application/ld+json"]').forEach(s => add('jsonld', s.textContent));
      document.querySelectorAll('[alt],[title],[aria-label],[placeholder]').forEach(e => ['alt', 'title', 'aria-label', 'placeholder'].forEach(a => add('attr:' + a, e.getAttribute(a))));
      document.querySelectorAll('noscript').forEach(n => add('noscript', n.textContent));
      // Jetpack keeps the success message in data attributes / hidden markup
      document.querySelectorAll('.axgs [data-wp-context], .axgs .contact-form-submission, .axgs form').forEach(e => add('form-hidden', (e.getAttribute('data-wp-context') || '') + ' ' + e.textContent));
      return hits;
    }, TERMS.source);
    out[`${path} @${w}`] = { status: resp.status(), hits: r };
    await p.close();
  }
  await b.close();
  fs.writeFileSync(process.argv[2] || 'audit-before.json', JSON.stringify(out, null, 1));
  for (const [k, v] of Object.entries(out)) { console.log(k, v.status, v.hits.length); for (const h of v.hits) console.log('   ', h[0], '|', h[1], '|', h[2]); }
})();
