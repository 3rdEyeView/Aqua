// How often does a fresh logged-out browser get the demo markup on the plain URL? Prints cache headers per load.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (let i = 0; i < 5; i++) for (const [name, o] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['mobile', { ...devices['iPhone 13'] }]]) {
    const c = await b.newContext(o); const p = await c.newPage();
    const resp = await p.goto('https://axiomsystems.systems/arroyos-lawn-care-demo/', { waitUntil: 'domcontentloaded', timeout: 90000 });
    const h = resp.headers();
    console.log(name, JSON.stringify({ tpl: await p.evaluate(() => !!document.getElementById('axl-lead-tpl')), kinsta: h['x-kinsta-cache'], ki: h['ki-cf-cache-status'], age: h['age'], lastMod: h['last-modified'], enc: h['content-encoding'] }));
    await c.close();
  }
  await b.close();
})();
