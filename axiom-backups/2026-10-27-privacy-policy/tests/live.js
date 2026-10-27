// Live checks: footer link click (desktop + mobile), policy page render, Get Started form still blocks empty submit.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const out = {};
  for (const [label, w] of [['desktop', 1440], ['mobile', 390]]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } }); const errs = [];
    p.on('pageerror', e => errs.push(e.message)); await p.route(/google|doubleclick|leadconnectorhq/, r => r.abort());
    await p.goto('https://axiomsystems.systems/pricing/', { waitUntil: 'networkidle' });
    const link = p.locator('a[href="/privacy-policy/"]').last(); await link.scrollIntoViewIfNeeded();
    const visible = await link.isVisible();
    const [resp] = await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), link.click()]);
    const info = await p.evaluate(() => ({ url: location.pathname, h1: document.querySelector('h1')?.innerText, sections: document.querySelectorAll('#policy h2').length, sw: document.documentElement.scrollWidth,
      linksUnderlined: [...document.querySelectorAll('#policy a')].every(a => a.querySelector('u') || getComputedStyle(a).textDecorationLine.includes('underline')) }));
    await p.screenshot({ path: `shots/live-${label}.png`, fullPage: true });
    await p.goto('https://axiomsystems.systems/get-started/?plan=lead-automation', { waitUntil: 'networkidle' });
    let ajax = 0; p.on('request', q => { if (q.url().includes('grunion-contact-form')) ajax++; });
    await p.click('.axgs button[type=submit]'); await p.waitForTimeout(1200);
    out[label] = { footer_link_visible: visible, nav_status: resp ? resp.status() : 'loaded', ...info, overflow: info.sw > w, js_errors: errs.length, get_started_empty_submit_ajax: ajax,
      plan_label: await p.evaluate(() => document.querySelector('.axgs-plan')?.innerText.replace('\n', ' ')) };
    await p.close();
  }
  await b.close(); fs.writeFileSync('live-results.json', JSON.stringify(out, null, 1)); console.log(JSON.stringify(out, null, 1));
})();
