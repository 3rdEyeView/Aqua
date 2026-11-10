// Logged-out snapshot of the live page (normal URL): full-page screenshots with motion reduced so frames are comparable.
const { chromium, devices } = require('playwright');
const tag = process.argv[2];
(async () => {
  const b = await chromium.launch();
  for (const [name, o] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['mobile', { ...devices['iPhone 13'] }]]) {
    const c = await b.newContext({ ...o, reducedMotion: 'reduce' }); const p = await c.newPage();
    await p.goto('https://axiomsystems.systems/arroyos-lawn-care-demo/?nocache=' + tag, { waitUntil: 'load', timeout: 90000 });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); } scrollTo(0, 0); });
    await p.waitForTimeout(2500);
    const info = await p.evaluate(() => ({ h: document.documentElement.scrollHeight, els: document.querySelectorAll('[data-elementor-id="1716"] *').length, forms: document.forms.length, host: !!document.getElementById('axl-lead-demo'), tpl: !!document.getElementById('axl-lead-tpl'), text: document.querySelector('[data-elementor-id="1716"]').innerText.length }));
    await p.screenshot({ path: `shots/${tag}-${name}.png`, fullPage: true });
    console.log(tag, name, JSON.stringify(info)); await c.close();
  }
  await b.close();
})();
