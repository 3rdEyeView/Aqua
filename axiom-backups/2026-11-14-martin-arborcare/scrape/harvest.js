// Walk the logged-out photo viewer from the first grid photo via "Next photo", saving the full-size image,
// post date, caption and Facebook's "AI content" label for each.
const { chromium } = require('playwright'); const fs = require('fs');
const OUT = process.argv[2], MAX = +(process.argv[3] || 200);
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, locale: 'en-US' });
  const p = await ctx.newPage();
  await p.goto('https://www.facebook.com/MartinArborcareLLC/photos', { waitUntil: 'domcontentloaded', timeout: 60000 }); await p.waitForTimeout(6000);
  try { await p.locator('div[role=dialog] [aria-label="Close"]').first().click({ timeout: 2000 }); } catch {}
  await p.locator('a[href*="photo.php?fbid"]').first().click(); await p.waitForTimeout(5000);
  const rows = [], seen = new Set();
  for (let i = 0; i < MAX; i++) {
    try { await p.locator('div[role=dialog] [aria-label="Close"]').first().click({ timeout: 800 }); } catch {}
    const r = await p.evaluate(() => {
      const imgs = [...document.querySelectorAll('img')].filter(i => /scontent/.test(i.src) && i.naturalWidth >= 400)
        .sort((a, b) => b.naturalWidth * b.naturalHeight - a.naturalWidth * a.naturalHeight);
      const t = document.body.innerText;
      return { url: location.href, src: imgs[0] && imgs[0].src, w: imgs[0] && imgs[0].naturalWidth, h: imgs[0] && imgs[0].naturalHeight,
        ai: /\nAI content\n/.test(t), text: t.slice(0, 1500) };
    });
    const fbid = (r.url.match(/fbid=(\d+)/) || [])[1];
    if (!fbid || seen.has(fbid)) { console.log('stop at', i, r.url); break; }
    seen.add(fbid);
    let file = '';
    if (r.src) { file = `${OUT}/fb-${String(i + 1).padStart(3, '0')}-${fbid}.jpg`; require('child_process').execFileSync('curl', ['-sSf', '-o', file, r.src]); }
    const m = r.text.match(/\n([A-Z][a-z]+ \d{1,2}(?:, \d{4})? at [\d:]+ [AP]M)|\n((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), [A-Z][a-z]+ \d{1,2}, \d{4})/);
    const cap = (r.text.split(/\n·\n/).slice(2).join(' ').split(/All reactions:|\nLike\n/)[0] || '').replace(/\s+/g, ' ').trim();
    rows.push({ n: i + 1, fbid, file, w: r.w, h: r.h, ai: r.ai, date: m ? (m[2] || m[1]) : '', caption: cap.slice(0, 400), url: r.url });
    console.log(i + 1, fbid, r.w + 'x' + r.h, r.ai ? 'AI' : '', (m ? (m[2] || m[1]) : ''), cap.slice(0, 70));
    fs.writeFileSync(`${OUT}/../harvest.json`, JSON.stringify(rows, null, 1));
    const next = p.locator('[aria-label="Next photo"]').first();
    try { await next.click({ timeout: 5000 }); } catch (e) { console.log('no next', i); break; }
    await p.waitForTimeout(2500);
  }
  await b.close();
})();
