const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const url of process.argv.slice(2)) {
    const ctx = await b.newContext({ ...devices['Pixel 7'] }); const p = await ctx.newPage();
    await p.addInitScript(() => { window.__s = []; new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__s.push({ v: +e.value.toFixed(3), t: Math.round(e.startTime), src: e.sources.map(s => { const n = s.node; return n ? (n.nodeType === 1 ? n.tagName + '.' + [...n.classList].slice(0, 3).join('.') + ' "' + (n.textContent || '').trim().slice(0, 40) + '"' : '#text "' + n.textContent.trim().slice(0, 40) + '"') : null; }) }); }).observe({ type: 'layout-shift', buffered: true }); });
    await p.goto(url + '?cls=' + Date.now(), { waitUntil: 'load' }); await p.waitForTimeout(3000);
    console.log(url); (await p.evaluate(() => window.__s)).forEach(s => console.log('  ', s.v, '@' + s.t + 'ms', s.src.join(' | ')));
    await ctx.close();
  }
  await b.close();
})();
