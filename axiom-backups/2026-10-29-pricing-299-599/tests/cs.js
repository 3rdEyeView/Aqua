const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.route(/google|doubleclick|gtag|leadconnector/, x => x.abort());
  for (const [url, ids] of [['/pricing/', ['6ec3518e', '4aa219b8']], ['/add-ons/', ['960b165', '1a720fb3']], ['/', ['59b16f9b']]]) {
    await p.goto('https://axiomsystems.systems' + url + '?nc=' + Date.now(), { waitUntil: 'networkidle' });
    for (const id of ids) console.log(url, id, JSON.stringify(await p.evaluate((id) => {
      const e = document.querySelector('[data-id="' + id + '"],[data-interaction-id="' + id + '"],.elementor-element-' + id + ',[class*="' + id + '"]'); if (!e) return null;
      const s = getComputedStyle(e), bf = getComputedStyle(e, '::before');
      return { cls: e.className, pl: s.paddingLeft, fs: s.fontSize, color: s.color, lh: s.lineHeight, before: bf.content !== 'none' ? { w: bf.width, left: bf.left, pos: bf.position } : null, parentGap: getComputedStyle(e.parentElement).rowGap };
    }, id)));
  }
  await b.close();
})();
