const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const out = {};
  for (const [n, o] of [['iPhone 13', devices['iPhone 13']], ['Pixel 7', devices['Pixel 7']], ['iPad Mini', devices['iPad Mini']]]) {
    const ctx = await b.newContext(o); const p = await ctx.newPage();
    await p.goto('https://axiomsystems.systems/advanced-fence-demo/?v=' + Date.now(), { waitUntil: 'networkidle', timeout: 60000 });
    await p.waitForTimeout(9000);
    out[n] = await p.evaluate(() => {
      const host = document.querySelector('chat-widget'); const bub = host && host.shadowRoot && host.shadowRoot.querySelector('.lc_text-widget--bubble');
      const nav = [...document.querySelectorAll('nav')].find(x => getComputedStyle(x).position === 'fixed');
      const btns = [...nav.querySelectorAll('a')].map(a => a.getBoundingClientRect());
      const bb = bub && bub.getBoundingClientRect();
      const hit = bb ? btns.some(r => !(bb.right <= r.left || bb.left >= r.right || bb.bottom <= r.top || bb.top >= r.bottom)) : null;
      return { bubble: bb && [bb.left, bb.top, bb.right, bb.bottom].map(Math.round), buttons: btns.map(r => [r.left, r.top, r.right, r.bottom].map(Math.round)), overlapsButtons: hit, sw: document.documentElement.scrollWidth, cw: innerWidth };
    });
    if (n === 'iPhone 13') await p.screenshot({ path: '/tmp/claude-0/-home-user-Aqua/201a40fe-0234-5724-8991-b990e4f05451/scratchpad/afs/live-bar.png', clip: { x: 0, y: 500, width: 390, height: 164 } });
    await ctx.close();
  }
  console.log(JSON.stringify(out)); await b.close();
})();
