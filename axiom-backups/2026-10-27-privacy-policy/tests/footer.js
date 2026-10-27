// Footer screenshot + computed style of the Privacy Policy link vs the FAQ link: node footer.js <url> <name>
const { chromium } = require('playwright');
(async () => {
  const [url, name] = process.argv.slice(2); const b = await chromium.launch(); const out = {};
  for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } }); await p.route(/google|doubleclick|leadconnectorhq/, r => r.abort());
    await p.goto(url, { waitUntil: 'networkidle' });
    const r = await p.evaluate(() => {
      const ft = [...document.querySelectorAll('a')].filter(a => ['FAQ', 'Privacy Policy'].includes(a.innerText.trim()) && a.getBoundingClientRect().top > document.body.scrollHeight - 700);
      const s = a => { const c = getComputedStyle(a); return [c.color, c.fontSize, c.fontWeight, c.backgroundColor, c.paddingTop].join(' '); };
      return { links: ft.map(a => [a.innerText.trim(), a.getAttribute('href'), s(a)]), sw: document.documentElement.scrollWidth };
    });
    out[w] = r;
    const f = await p.$('footer, [data-id] footer'); const el = f || (await p.$$('body > *')).pop();
    await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await p.waitForTimeout(300);
    await p.screenshot({ path: `shots/${name}-footer-${w}.png`, clip: { x: 0, y: Math.max(0, (await p.evaluate(() => document.body.scrollHeight)) - 420), width: w, height: 420 }, fullPage: true });
    await p.close();
  }
  await b.close(); console.log(JSON.stringify(out));
})();
