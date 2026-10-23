// One labeled test submission of the Get Started form with Google domains blocked
// (no real Ads conversion). Prints the Jetpack AJAX result (entry ID) only.
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
	const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', proxy: { server: process.env.HTTPS_PROXY } });
	const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
	const blocked = [];
	await ctx.route(/(google|googletagmanager|googleadservices|doubleclick|google-analytics)\./, r => { blocked.push(1); r.abort(); });
	const p = await ctx.newPage(); const out = {};
	p.on('response', async r => { if (r.url().includes('grunion-contact-form')) { try { const j = await r.json(); out.ajax = { status: r.status(), success: j.success, entry: j.refreshArgs && j.refreshArgs['contact-form-sent'] }; } catch (e) { out.ajax = { status: r.status() }; } } });
	await p.goto('https://axiomsystems.systems/get-started/?plan=growth', { waitUntil: 'load' });
	const f = p.locator('.axgs form'); const t0 = Date.now();
	await f.locator('[name$="-name"]').fill('Axiom hook probe test');
	await f.locator('[name$="-businessname"]').fill('Axiom test business (please ignore)');
	await f.locator('[name$="-email"]').fill('qa-test@example.com');
	await f.locator('[name$="-phone"]').fill('5555550100');
	await f.locator('[name$="-currentwebsite"]').fill('https://example.com');
	await f.locator('textarea[name$="-tellusaboutyourbusiness"]').fill('Automated test of the form submission hooks for the CRM integration. Please ignore.');
	await f.locator('button[type=submit]').click();
	await p.waitForSelector('.axgs .contact-form-submission, .axgs .submission-success', { timeout: 30000 }).catch(() => {});
	out.visibleMs = Date.now() - t0;
	out.successShown = await p.evaluate(() => !!document.querySelector('.axgs .submission-success, .axgs .contact-form-submission h4'));
	out.googleBlocked = blocked.length;
	console.log(JSON.stringify(out));
	await b.close();
})();
