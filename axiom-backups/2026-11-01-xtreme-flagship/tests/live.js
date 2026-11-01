// Live verification of Home and Our Work after publishing.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const res = {};
  for (const [name, url] of [['home', 'https://axiomsystems.systems/?nocache=' + Date.now()], ['our-work', 'https://axiomsystems.systems/our-work/?nocache=' + Date.now()]]) {
    for (const w of [1440, 1024, 768, 390]) {
      const p = await b.newPage({ viewport: { width: w, height: 900 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
      const r = await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
      await p.evaluate(async () => { document.querySelectorAll('img').forEach(i => i.loading = 'eager'); for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); }
        await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 6000); }))); window.scrollTo(0, 0); });
      const d = await p.evaluate(() => {
        const t = document.body.innerText, html = document.documentElement.outerHTML;
        const pos = s => t.indexOf(s);
        const links = [...document.querySelectorAll('a')].filter(a => /xtremestpete|jetskiadventure|bragspressure/.test(a.href)).map(a => [a.innerText.trim().slice(0, 40), a.href, a.target]);
        const imgs = [...document.images].filter(i => /xtreme|aqua|brags/i.test(i.currentSrc)).map(i => [i.currentSrc.split('/').pop(), i.alt.slice(0, 50), i.naturalWidth > 0]);
        return { status: 0, sw: document.documentElement.scrollWidth, firstX: pos('Xtreme'), firstAqua: pos('Aqua Safari'), firstBrags: pos('Brags'),
          aquaHtml: (html.match(/aqua/gi) || []).length, xtremeHtml: (html.match(/xtreme/gi) || []).length,
          stale: ['Live client website: xtremestpete', 'glowing all-caps', 'Captain Mike', 'Two jet ski companies', 'axiom-portfolio-aqua-safari-mobile', 'Open Daily'].filter(s => html.includes(s)),
          broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src),
          gtm: (html.match(/GT-55XGH597/g) || []).length, getStarted: [...document.querySelectorAll('a[href*="get-started"]')].length, links, imgs };
      });
      d.status = r.status(); d.errors = errs.length; res[`${name}-${w}`] = d;
      if (w === 1440 || w === 390) await p.screenshot({ path: `after/shots/${name}-${w}.png`, fullPage: true });
      console.log(name, w, d.status, 'sw', d.sw, 'order X/Aqua/Brags', d.firstX, d.firstAqua, d.firstBrags, 'stale', d.stale, 'broken', d.broken.length, 'err', d.errors, 'getstarted', d.getStarted);
      await p.close();
    }
  }
  fs.writeFileSync('tests/live-results.json', JSON.stringify(res, null, 1)); await b.close();
})();
