// Screenshots the region around given element IDs on a page (preview or live URL).
// Usage: node preview.js <outdir> <tag> <url> <id,id,...> [widths]
const { chromium } = require('playwright');
const [out, tag, url, ids, ws] = process.argv.slice(2);
(async () => {
	const b = await chromium.launch();
	for (const w of (ws || '1440,390').split(',').map(Number)) {
		const ctx = await b.newContext({ viewport: { width: w, height: 900 }, isMobile: w < 768 });
		await ctx.route(/(googletagmanager|google-analytics|googleadservices|doubleclick|stats\.wp\.com)/, r => r.abort());
		const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
		await p.goto(url, { waitUntil: 'load', timeout: 90000 }); await p.waitForTimeout(800);
		for (const id of ids.split(',')) {
			const box = await p.evaluate(id => {
				const el = document.querySelector(`[data-interaction-id="${id}"]`) || document.querySelector(`.elementor-element-${id}`);
				if (!el) return null;
				let c = el; for (let i = 0; i < 3 && c.parentElement && c.getBoundingClientRect().height < 380; i++) c = c.parentElement;
				const r = c.getBoundingClientRect(); return { y: r.y + scrollY, h: r.height };
			}, id);
			if (!box) { console.log(tag, w, id, 'NOT FOUND'); continue; }
			await p.screenshot({ path: `${out}/${tag}-${w}-${id}.png`, fullPage: true, clip: { x: 0, y: Math.max(0, box.y - 24), width: w, height: Math.min(box.h + 48, 1600) } });
		}
		const hs = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth);
		console.log(tag, w, 'hscroll', hs, 'errors', errs.length);
		await ctx.close();
	}
	await b.close();
})();
