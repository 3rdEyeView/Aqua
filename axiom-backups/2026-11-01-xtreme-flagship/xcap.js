// Fresh Xtreme captures. Hides the floating "Sound On" video control and any consent banner; nothing else is altered.
const { chromium } = require('playwright');
const HIDE = `(() => { for (const el of document.querySelectorAll('body *')) { const t = (el.innerText||'').trim();
  if (/^🔊?\\s*Sound On$/.test(t) && getComputedStyle(el).position === 'fixed') el.style.display='none';
  if (/^🔊?\\s*Sound On$/.test(t)) { let p = el; while (p && p !== document.body) { if (getComputedStyle(p).position === 'fixed') { p.style.display='none'; break; } p = p.parentElement; } } }
  document.querySelectorAll('.cmplz-cookiebanner, #cmplz-cookiebanner-container, .cmplz-manage-consent').forEach(e => e.style.display='none'); })()`;
(async () => {
  const b = await chromium.launch();
  // mobile 390x780 @2x
  let ctx = await b.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1' });
  let p = await ctx.newPage(); await p.goto('https://xtremestpete.com/', { waitUntil: 'networkidle', timeout: 90000 });
  await p.waitForTimeout(6000); await p.evaluate(HIDE); await p.waitForTimeout(300);
  await p.screenshot({ path: 'media/x-mobile.png' }); await ctx.close();
  // desktop 1440x810 @2x
  ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  p = await ctx.newPage(); await p.goto('https://xtremestpete.com/', { waitUntil: 'networkidle', timeout: 90000 });
  await p.waitForTimeout(6000); await p.evaluate(HIDE); await p.waitForTimeout(300);
  await p.screenshot({ path: 'media/x-desktop.png' });
  // tours section
  const y = await p.evaluate(() => { const h = [...document.querySelectorAll('h1,h2,h3')].find(h => /PICK YOUR RIDE/i.test(h.innerText)); h.scrollIntoView(); return Math.round(h.getBoundingClientRect().top + scrollY); });
  await p.evaluate(async () => { for (let i = 0; i < 6; i++) { window.scrollBy(0, 200); await new Promise(r => setTimeout(r, 200)); } });
  await p.evaluate(async () => { const imgs=[...document.images]; imgs.forEach(i=>{i.loading='eager'; if(i.dataset.src) i.src=i.dataset.src; if(i.dataset.srcset) i.srcset=i.dataset.srcset;}); await Promise.all(imgs.map(i=>i.complete?0:new Promise(r=>{i.onload=i.onerror=r; setTimeout(r,8000);}))); });
  await p.evaluate(() => { const h = [...document.querySelectorAll('h1,h2,h3')].find(h => /PICK YOUR RIDE/i.test(h.innerText)); h.scrollIntoView({block:'start'}); });
  await p.waitForTimeout(4000); await p.evaluate(HIDE);
  await p.screenshot({ path: 'media/x-tours.png', fullPage: true, clip: { x: 0, y: y - 140, width: 1440, height: 1300 } });
  console.log('tours y', y);
  await b.close();
})();
