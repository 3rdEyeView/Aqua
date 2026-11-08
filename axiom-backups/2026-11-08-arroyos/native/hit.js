const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const d of ['iPhone 13', 'desktop']) {
    const c = await b.newContext(d === 'desktop' ? { viewport: { width: 1440, height: 900 } } : devices[d]); const p = await c.newPage();
    await p.goto(process.argv[2], { waitUntil: 'networkidle' });
    console.log(d, await p.evaluate(() => {
      const k = document.querySelector('#hero .e-background-video-controls, #hero [class*=controls]');
      const cs = getComputedStyle(k);
      const out = { pos: cs.position, top: cs.top, bottom: cs.bottom, h: k.getBoundingClientRect().height, pe: cs.pointerEvents, cls: k.className.slice(0, 120) };
      out.hits = [...document.querySelectorAll('#hero a')].map(a => { const r = a.getBoundingClientRect(); const pts = [[r.right - 8, r.top + r.height / 2], [r.left + 8, r.top + r.height / 2]];
        return a.textContent.trim().slice(0, 18) + ':' + pts.map(([x, y]) => { const e = document.elementFromPoint(x, y); return e && (a.contains(e) ? 'ok' : 'BLOCKED by ' + e.className.slice(0, 60)); }).join('/'); });
      return out;
    }));
    await c.close();
  }
  await b.close();
})();
