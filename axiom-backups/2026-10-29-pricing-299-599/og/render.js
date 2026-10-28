const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + process.argv[2], { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  console.log('fonts', await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + f.weight).join(',')));
  await p.screenshot({ path: process.argv[3], type: 'jpeg', quality: 90 });
  await b.close();
})();
