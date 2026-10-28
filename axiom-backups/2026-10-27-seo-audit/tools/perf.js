// perf.js <out.json> <url...>: mobile lab metrics (LCP, CLS, weight, biggest resources, image sizing)
const { chromium, devices } = require('playwright');
const fs = require('fs');
(async () => {
  const [out, ...urls] = process.argv.slice(2); const res = {};
  const browser = await chromium.launch();
  for (const url of urls) {
    const ctx = await browser.newContext({ ...devices['Pixel 7'] });
    const page = await ctx.newPage(); const reqs = [];
    page.on('response', async r => { try { const b = await r.body(); reqs.push({ url: r.url(), type: r.request().resourceType(), bytes: b.length, status: r.status() }); } catch (e) {} });
    await page.addInitScript(() => {
      window.__lcp = null; window.__cls = 0;
      new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = { t: e.startTime, el: e.element ? e.element.tagName + ' ' + (e.element.currentSrc || e.element.textContent || '').slice(0, 80) : null, size: e.size }; }).observe({ type: 'largest-contentful-paint', buffered: true });
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
    });
    const t0 = Date.now();
    await page.goto(url + (url.includes('?') ? '&' : '?') + 'nc=' + Date.now(), { waitUntil: 'load', timeout: 60000 });
    await page.mouse.wheel(0, 4000); await page.waitForTimeout(2500);
    const m = await page.evaluate(() => {
      const nav = performance.getEntriesByType('navigation')[0];
      const imgs = [...document.images].map(i => ({ src: i.currentSrc, natural: [i.naturalWidth, i.naturalHeight], shown: [i.clientWidth, i.clientHeight], loading: i.loading, w: i.getAttribute('width'), h: i.getAttribute('height') }));
      return { lcp: window.__lcp, cls: window.__cls, ttfb: nav.responseStart, dcl: nav.domContentLoadedEventEnd, load: nav.loadEventEnd, imgs, overflow: document.documentElement.scrollWidth > innerWidth };
    });
    const total = reqs.reduce((a, r) => a + r.bytes, 0);
    const byType = {}; reqs.forEach(r => byType[r.type] = (byType[r.type] || 0) + r.bytes);
    res[url] = { ...m, requests: reqs.length, totalKB: Math.round(total / 1024), byTypeKB: Object.fromEntries(Object.entries(byType).map(([k, v]) => [k, Math.round(v / 1024)])), biggest: reqs.sort((a, b) => b.bytes - a.bytes).slice(0, 6).map(r => [Math.round(r.bytes / 1024) + 'KB', r.type, r.url.slice(0, 110)]) };
    await ctx.close();
  }
  await browser.close(); fs.writeFileSync(out, JSON.stringify(res, null, 1));
  for (const [u, r] of Object.entries(res)) console.log(u, '| TTFB', Math.round(r.ttfb), 'LCP', Math.round(r.lcp?.t || 0), r.lcp?.el, '| CLS', r.cls.toFixed(3), '|', r.requests, 'req', r.totalKB + 'KB', JSON.stringify(r.byTypeKB), '| overflow', r.overflow, '\n   ', r.biggest.map(b => b.join(' ')).join('\n    '), '\n    oversize imgs:', r.imgs.filter(i => i.natural[0] > 2.2 * i.shown[0] && i.shown[0] > 0).map(i => i.src.split('/').pop() + ' ' + i.natural + '>' + i.shown).join('; '), '\n    no w/h attrs:', r.imgs.filter(i => !i.w || !i.h).length);
})();
