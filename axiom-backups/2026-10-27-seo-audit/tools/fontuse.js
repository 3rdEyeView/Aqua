// fontuse.js <url...>: which font families are actually used to render text (computed first family) and loaded faces
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
  for (const u of process.argv.slice(2)) { const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await p.goto(u, { waitUntil: 'load', timeout: 60000 }); await p.waitForTimeout(1500);
    const r = await p.evaluate(async () => { const fam = {}; document.querySelectorAll('body *').forEach(e => { if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return; const f = getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '').trim(); fam[f] = (fam[f] || 0) + 1; });
      await document.fonts.ready; const loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, '') + ' ' + f.weight + (f.style === 'italic' ? 'i' : '')); return { fam, loaded: [...new Set(loaded)] }; });
    console.log(u, JSON.stringify(r)); await p.close(); }
  await b.close(); })();
