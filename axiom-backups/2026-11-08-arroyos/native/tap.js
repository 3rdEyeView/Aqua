const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const c = await b.newContext(devices['iPhone 13']); const p = await c.newPage();
  await p.goto(process.argv[2], { waitUntil: 'networkidle' });
  const ba = await p.$('#ba'); await ba.scrollIntoViewIfNeeded(); await p.waitForTimeout(2500);
  const box = await ba.boundingBox();
  const g = () => p.evaluate(() => document.getElementById('ba-handle').style.left);
  console.log('start', await g());
  await p.touchscreen.tap(box.x + box.width * 0.2, box.y + box.height / 2); await p.waitForTimeout(200); console.log('tap 20% ->', await g());
  await p.touchscreen.tap(box.x + box.width * 0.75, box.y + box.height / 2); await p.waitForTimeout(200); console.log('tap 75% ->', await g());
  await p.screenshot({ path: '../preview/live-iphone13-tap.png' });
  const ctl = await p.evaluate(() => { const e = document.querySelector('#hero .e-background-video-controls, #hero [class*=controls]'); return e && JSON.stringify(e.getBoundingClientRect()); });
  console.log('controls', ctl); await b.close();
})();
