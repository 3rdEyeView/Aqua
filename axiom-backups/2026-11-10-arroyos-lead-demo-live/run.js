// Runs the lead walkthrough end to end. Usage: node run.js <base-url> <tag>   (base-url without the hash)
const { chromium, devices } = require('playwright');
const [base, tag] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  for (const [name, o] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['mobile', { ...devices['iPhone 13'] }]]) {
    const c = await b.newContext(o); const p = await c.newPage(); const errors = []; let reqs = [];
    p.on('pageerror', (e) => errors.push(e.message));
    p.on('request', (r) => reqs.push(r.method() + ' ' + r.url().slice(0, 110)));
    const r = { name };
    // normal visit: nothing mounted
    await p.goto(base, { waitUntil: 'load', timeout: 90000 }); await p.waitForTimeout(1500);
    r.normal = await p.evaluate(() => ({ host: !!document.getElementById('axl-lead-demo'), open: document.documentElement.classList.contains('axl-lead-open'), tplInert: !!document.getElementById('axl-lead-tpl') && document.querySelectorAll('.view-lead, #ld-start').length === 0, forms: document.forms.length }));
    // fresh tab straight to the hash URL
    const p2 = await c.newPage(); p2.on('pageerror', (e) => errors.push(e.message)); reqs = []; p2.on('request', (q) => reqs.push(q.method() + ' ' + q.url().slice(0, 110)));
    await p2.goto(base + '#lead-demo', { waitUntil: 'load', timeout: 90000 }); await p2.waitForTimeout(3000);
    await p2.evaluate(() => { window.__seen = []; ['click', 'submit', 'input', 'change', 'keydown'].forEach((t) => document.addEventListener(t, (e) => window.__seen.push(t))); });
    const S = (sel) => p2.locator('#axl-lead-demo').locator(sel);
    r.opened = { visible: await S('#ld-start').isVisible(), label: (await S('.bar').innerText()).replace(/\s+/g, ' ').slice(0, 60), title: await p2.title(), pageHidden: await p2.evaluate(() => getComputedStyle(document.body.firstElementChild).visibility) };
    await p2.screenshot({ path: `shots/${tag}-${name}-0-open.png` });
    const before = reqs.length;
    await S('#ld-start').click(); r.source = (await S('#ph-url').innerText()).slice(0, 60);
    await S('#ld-s1').click(); await p2.waitForTimeout(500);
    r.m1 = { stage: await S('.col.is-on h3').innerText(), n: await S('#crm-tl .ev').count(), owner: (await S('#crm-owner').innerText()).replace(/\s+/g, ' ').slice(0, 70), sms: await S('#ph-msgs .msg--sms').count() };
    await p2.screenshot({ path: `shots/${tag}-${name}-1-new.png` });
    await S('#ld-s2').click(); await p2.waitForTimeout(400);
    r.m2 = { clock: await S('#ld-clock').innerText(), stage: await S('.col.is-on h3').innerText(), next: await S('#auto-next').innerText() };
    await S('#ld-s3b').click(); await p2.waitForTimeout(400);
    r.m3 = { clock: await S('#ld-clock').innerText(), stage: await S('.col.is-on h3').innerText(), auto: await S('#auto-state').innerText(), top: await S('#crm-tl .ev b').first().innerText() };
    await p2.screenshot({ path: `shots/${tag}-${name}-3-booked.png` });
    await S('#ld-reset').click();
    r.reset = (await S('#ph-ad').isVisible()) && (await S('#crm-empty').isVisible()) && (await S('#crm-tl .ev').count()) === 0 && (await S('#ld-clock').innerText()) === 'Tue · 10:41 AM';
    // second run: no SMS opt-in, homeowner replies
    await S('#ld-start').click(); await S('#l-sms').uncheck(); await S('#ph-send').click(); await S('#ld-s3a').click(); await p2.waitForTimeout(300);
    r.run2 = { sms: await S('#ph-msgs .msg--sms').count(), stage: await S('.col.is-on h3').innerText(), auto: await S('#auto-state').innerText() };
    await S('#ld-reset').click();
    await p2.waitForTimeout(1500);
    r.requestsDuringDemo = reqs.slice(before).filter((u) => !/\.(mp4|jpg|jpeg|png|webp|woff2?)(\?|$)/.test(u));
    r.eventsSeenByPage = await p2.evaluate(() => window.__seen.length);
    r.dataLayer = await p2.evaluate(() => (window.dataLayer || []).length);
    // back to website, then hash again in the same tab
    await S('#axl-close').click(); await p2.waitForTimeout(300);
    r.closed = await p2.evaluate(() => ({ url: location.href.includes('#'), open: document.documentElement.classList.contains('axl-lead-open'), hidden: document.getElementById('axl-lead-demo').hidden }));
    await p2.evaluate(() => { location.hash = '#lead-demo'; }); await p2.waitForTimeout(300); r.reopened = await S('#ld-start').isVisible();
    r.errors = errors; console.log(JSON.stringify(r)); await c.close();
  }
  await b.close();
})();
