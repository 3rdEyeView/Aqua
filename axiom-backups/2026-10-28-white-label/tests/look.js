const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const checks = { '/pricing/': ['Google Search Ads campaign setup', 'not included in the $597', 'Axiom CRM & Lead Management Pipeline'],
    '/add-ons/': ['Includes', 'access to the Axiom CRM, advanced lead follow-up automations, and Google Ads management'],
    '/': ['Includes access to the Axiom CRM, advanced lead follow-up automations, and Google Ads management', 'Axiom CRM & Lead Management Pipeline'],
    '/faq/': ['What is the Axiom CRM?', 'Is the Google Ads budget included?'] };
  for (const [path, qs] of Object.entries(checks)) for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.route(/google|doubleclick|gtag|leadconnector/, x => x.abort());
    await p.goto('https://axiomsystems.systems' + path + '?nc=' + Date.now(), { waitUntil: 'networkidle' });
    const t = await p.evaluate(() => document.body.innerText + document.body.textContent);
    console.log(path, w, qs.map(q => q.slice(0, 30) + ':' + t.includes(q)).join(' | '));
    if (path === '/pricing/') { const el = await p.$('text=Axiom CRM & Lead Management Pipeline'); if (el) { await el.scrollIntoViewIfNeeded(); await p.screenshot({ path: `shots-pricing-${w}.png` }); } }
    if (path === '/') { const el = await p.$('text=Includes access to the Axiom CRM'); if (el) { await el.scrollIntoViewIfNeeded(); await p.screenshot({ path: `shots-home-${w}.png` }); } }
    await p.close();
  }
  await b.close();
})();
