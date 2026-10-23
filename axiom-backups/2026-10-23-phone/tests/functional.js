// Live functional checks: tel links, keyboard focus, mobile-menu call row,
// Get Started form + lead tracking untouched (no submission is sent).
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
	const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', proxy: { server: process.env.HTTPS_PROXY } });
	const out = {};
	const block = ctx => ctx.route(/(googletagmanager|google-analytics|googleadservices|doubleclick|stats\.wp\.com)/, r => r.abort());
	// 1. Desktop: clicking each tel link requests tel:+17275917527 and stays on the page.
	{
		const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } }); await block(ctx);
		const p = await ctx.newPage();
		await p.goto('https://axiomsystems.systems/', { waitUntil: 'load' });
		const telNav = [];
		p.on('request', r => { if (r.url().startsWith('tel:')) telNav.push(r.url()); });
		const links = await p.$$('a[href^="tel:"]:not(#axm-panel a)');
		out.desktopClicks = [];
		for (const l of links) { await l.scrollIntoViewIfNeeded(); await l.click({ noWaitAfter: true }).catch(e => out.desktopClicks.push('err ' + e.message)); await p.waitForTimeout(300); out.desktopClicks.push(p.url()); }
		out.telRequests = telNav;
		// Keyboard: Tab from the last nav link reaches the phone link, then Get Started.
		await p.evaluate(() => window.scrollTo(0, 0));
		await p.focus('nav a[href="/faq/"]');
		await p.keyboard.press('Tab'); const f1 = await p.evaluate(() => [document.activeElement.className, document.activeElement.getAttribute('href'), document.activeElement.textContent.trim(), getComputedStyle(document.activeElement).outlineStyle]);
		await p.keyboard.press('Tab'); const f2 = await p.evaluate(() => [document.activeElement.className.split(' ')[0], document.activeElement.getAttribute('href')]);
		out.keyboard = [f1, f2];
		out.accName = await p.evaluate(() => { const a = document.querySelector('.axp-call'); return a.innerText.trim() + ' | textContent=' + a.textContent.trim(); });
		await ctx.close();
	}
	// 2. Mobile: menu contains the call row; tap targets size.
	for (const w of [390, 360]) {
		const ctx = await b.newContext({ viewport: { width: w, height: 800 }, isMobile: true, hasTouch: true }); await block(ctx);
		const p = await ctx.newPage(); await p.goto('https://axiomsystems.systems/pricing/', { waitUntil: 'load' });
		await p.tap('.axm-toggle'); await p.waitForTimeout(300);
		out['menu' + w] = await p.evaluate(() => [...document.querySelectorAll('#axm-panel a')].map(a => a.textContent.trim() + ' -> ' + a.getAttribute('href')));
		out['tap' + w] = await p.evaluate(() => { const r = document.querySelector('.axp-call').getBoundingClientRect(); return [r.width, r.height]; });
		await ctx.close();
	}
	// 3. Get Started form intact (plan label, validation blocks empty submit, no AJAX, no conversion).
	{
		const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); await block(ctx);
		const p = await ctx.newPage(); const ajax = [];
		p.on('request', r => { if (r.url().includes('grunion-contact-form') || r.url().includes('lead-check')) ajax.push(r.url()); });
		await p.goto('https://axiomsystems.systems/get-started/?plan=growth', { waitUntil: 'load' });
		out.form = await p.evaluate(() => ({
			form: !!document.querySelector('.axgs form'), fields: document.querySelectorAll('.axgs form input, .axgs form textarea').length,
			plan: document.querySelector('.axgs-plan') && document.querySelector('.axgs-plan').textContent,
			hidden: [...document.querySelectorAll('.axgs form input[type=hidden]')].map(i => i.value).filter(v => /Growth/.test(v)),
			leadJs: !!document.getElementById('axgs-lead-js'), tracking: !!window.axiomLeadTracking,
			gtagTags: [...document.querySelectorAll('script[src*="googletagmanager"]')].map(s => s.src.split('?')[1]),
			direct: document.querySelector('.axp-direct').textContent,
		}));
		await p.click('.axgs button[type=submit]'); await p.waitForTimeout(2000);
		out.formAfterEmptySubmit = await p.evaluate(() => ({ errors: !!document.querySelector('.contact-form__error.show-errors, .contact-form__input-error'), success: !!document.querySelector('.contact-form-submission'), fired: window.axiomLeadTracking && window.axiomLeadTracking.fired }));
		out.formAjax = ajax;
		await ctx.close();
	}
	// 4. Schema is valid JSON with one Organization carrying the telephone.
	{
		const ctx = await b.newContext(); await block(ctx); const p = await ctx.newPage();
		await p.goto('https://axiomsystems.systems/faq/', { waitUntil: 'load' });
		out.schema = await p.evaluate(() => [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => { const j = JSON.parse(s.textContent); return (j['@graph'] || [j]).map(n => n['@type'] + (n.telephone ? ':' + n.telephone : '')).join(','); }));
		await ctx.close();
	}
	console.log(JSON.stringify(out, null, 1));
	await b.close();
})().catch(e => { console.error(e); process.exit(1); });
