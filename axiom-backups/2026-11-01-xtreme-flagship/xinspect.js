const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('https://xtremestpete.com/', { waitUntil: 'networkidle', timeout: 90000 });
  await p.waitForTimeout(4000);
  await p.screenshot({ path: 'media/raw-desktop.png' });
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
  await p.waitForTimeout(1500);
  await p.screenshot({ path: 'media/raw-desktop-full.png', fullPage: true });
  const t = await p.evaluate(() => document.body.innerText);
  require('fs').writeFileSync('media/xtreme-text.txt', t);
  const links = await p.evaluate(() => [...document.querySelectorAll('a')].map(a => a.innerText.trim().slice(0,40) + ' -> ' + a.href).filter((v,i,s)=>s.indexOf(v)===i));
  require('fs').writeFileSync('media/xtreme-links.txt', links.join('\n'));
  const forms = await p.evaluate(() => [...document.querySelectorAll('form, iframe')].map(f => f.tagName + ' ' + (f.action || f.src || '')));
  console.log(forms.join('\n'));
  await b.close();
})();
