const { chromium, devices } = require('playwright');
(async () => {
  const url = process.argv[2];
  const b = await chromium.launch(); const c = await b.newContext({ viewport: { width: 1440, height: 900 } }); const p = await c.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
  const info = await p.evaluate(() => {
    const v = document.querySelector('#hero video, video');
    const vh = v ? v.outerHTML.slice(0, 600) : null;
    const hero = document.getElementById('hero');
    const imgs = [...document.querySelectorAll('img')].map(i => ({ src: i.currentSrc.split('/').pop(), loading: i.getAttribute('loading'), srcset: !!i.getAttribute('srcset'), sizes: i.getAttribute('sizes'), w: i.getBoundingClientRect().width|0 }));
    const fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight);
    const h = getComputedStyle(document.querySelector('h1')).fontFamily;
    return { vh, heroHTML: hero ? hero.outerHTML.slice(0, 1500) : null, imgs, fonts: [...new Set(fonts)], h1font: h, sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth };
  });
  console.log(JSON.stringify(info, null, 1)); console.log('errors', errs);
  await b.close();
})();
