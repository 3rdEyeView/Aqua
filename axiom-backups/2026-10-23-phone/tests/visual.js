// Renders saved pages (before/after) through Chromium with the live site's assets
// and reports header/footer/contact-line layout at several widths.
// Usage: node visual.js <html-dir> <1135-main.php> <shots-dir> [live]
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const fs = require('fs'), path = require('path');
const [dir, menuPhp, shots, live] = process.argv.slice(2);
const menuJs = menuPhp && fs.existsSync(menuPhp) ? fs.readFileSync(menuPhp, 'utf8').split("<<<'AXMJS'\n")[1].split('\nAXMJS;')[0] : null;
const pages = { home: '/', pricing: '/pricing/', 'add-ons': '/add-ons/', faq: '/faq/', 'get-started': '/get-started/', 'how-it-works': '/how-it-works/', 'our-work': '/our-work/' };
const widths = [1440, 1280, 1100, 1025, 1024, 768, 414, 390, 360, 320];
fs.mkdirSync(shots, { recursive: true });
(async () => {
	const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', proxy: { server: process.env.HTTPS_PROXY } });
	const out = {};
	for (const [name, p] of Object.entries(pages)) {
		for (const w of widths) {
			const ctx = await b.newContext({ viewport: { width: w, height: 900 }, isMobile: w < 768, hasTouch: w < 768 });
			await ctx.route(/(googletagmanager|google-analytics|googleadservices|doubleclick|stats\.wp\.com)/, r => r.abort());
			if (!live) {
				let html = fs.readFileSync(path.join(dir, name + '.html'), 'utf8');
				if (menuJs) html = html.replace(/<script id="axm-menu-js">[\s\S]*?<\/script>/, () => '<script id="axm-menu-js">' + menuJs.trim() + '</script>');
				await ctx.route(u => u.href === 'https://axiomsystems.systems' + p, r => r.fulfill({ status: 200, contentType: 'text/html; charset=UTF-8', body: html }));
			}
			const pg = await ctx.newPage();
			const errs = []; pg.on('pageerror', e => errs.push(e.message));
			await pg.goto('https://axiomsystems.systems' + p + (live ? '?nocache=' + Date.now() : ''), { waitUntil: 'load', timeout: 90000 });
			await pg.waitForTimeout(600);
			const r = await pg.evaluate(() => {
				const box = el => { if (!el) return null; const b = el.getBoundingClientRect(); const s = getComputedStyle(el); return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), vis: s.display !== 'none' && s.visibility !== 'hidden' && b.width > 0 }; };
				const header = document.querySelector('nav').parentElement.parentElement;
				const cta = header.querySelector('a.ax-btn');
				const call = header.querySelector('.axp-call');
				const tog = header.querySelector('.axm-toggle');
				const logo = header.querySelector('a[href="/"]');
				const num = call && call.querySelector('.axp-num');
				const kids = [logo, header.querySelector('nav'), call, cta, tog].filter(Boolean).map(box).filter(b => b.vis);
				let overlap = false;
				for (let i = 0; i < kids.length; i++) for (let j = i + 1; j < kids.length; j++) { const a = kids[i], c = kids[j]; if (a.x < c.x + c.w && c.x < a.x + a.w && a.y < c.y + c.h && c.y < a.y + a.h) overlap = true; }
				const foot = document.querySelector('.axp-foot');
				const direct = [...document.querySelectorAll('.axp-direct')];
				const tels = [...document.querySelectorAll('a[href^="tel:"]')].map(a => a.getAttribute('href'));
				return {
					header: box(header), logo: box(logo), cta: box(cta), call: box(call), toggle: box(tog),
					numVisible: num ? num.getBoundingClientRect().width > 2 : null,
					callName: call ? call.textContent.replace(/\s+/g, ' ').trim() : null,
					overlap, hscroll: document.documentElement.scrollWidth > window.innerWidth,
					foot: box(foot), footText: foot && foot.textContent.trim(),
					direct: direct.map(d => ({ text: d.textContent.trim(), font: getComputedStyle(d).fontSize, color: getComputedStyle(d).color, link: getComputedStyle(d.querySelector('a')).color, box: box(d) })),
					tels, emailCount: (document.body.innerText.match(/axiom\.systems\.co@gmail\.com/g) || []).length,
				};
			});
			// Mobile menu still opens and closes.
			if (r.toggle && r.toggle.vis) {
				await pg.click('.axm-toggle'); await pg.waitForTimeout(300);
				r.menuOpen = await pg.evaluate(() => !document.querySelector('#axm-panel').hidden && document.querySelectorAll('#axm-panel a').length);
				await pg.keyboard.press('Escape'); await pg.waitForTimeout(200);
				r.menuClosed = await pg.evaluate(() => document.querySelector('#axm-panel').hidden);
			}
			r.errors = errs;
			out[name + '@' + w] = r;
			if (['home', 'get-started', 'faq'].includes(name) || w === 1100) {
				await pg.screenshot({ path: `${shots}/${name}-${w}-header.png`, clip: { x: 0, y: 0, width: w, height: 90 } });
			}
			if (w === 1440 || w === 390) {
				const foot = await pg.$('.axp-foot');
				if (foot) { await foot.scrollIntoViewIfNeeded(); const fb = await pg.evaluate(() => { const f = document.querySelector('.axp-foot').closest('footer, .e-con:not(.e-con .e-con)') || document.body; const e = document.querySelector('.axp-foot').parentElement.parentElement.parentElement; const b = e.getBoundingClientRect(); return { y: b.y + scrollY, h: b.height }; }); await pg.screenshot({ path: `${shots}/${name}-${w}-footer.png`, fullPage: true, clip: { x: 0, y: Math.max(0, fb.y - 20), width: w, height: Math.min(fb.h + 40, 700) } }); }
				const d = await pg.$('.axp-direct');
				if (d) { const db = await pg.evaluate(() => { const e = document.querySelector('.axp-direct').parentElement; const b = e.getBoundingClientRect(); return { y: b.y + scrollY, h: b.height }; }); await pg.screenshot({ path: `${shots}/${name}-${w}-contact.png`, fullPage: true, clip: { x: 0, y: Math.max(0, db.y - 20), width: w, height: Math.min(db.h + 40, 1400) } }); }
			}
			await ctx.close();
		}
	}
	fs.writeFileSync(path.join(shots, 'results.json'), JSON.stringify(out, null, 1));
	await b.close();
	console.log('done', Object.keys(out).length);
})().catch(e => { console.error(e); process.exit(1); });
