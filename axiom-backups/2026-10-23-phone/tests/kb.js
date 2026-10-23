const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
	const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', proxy: { server: process.env.HTTPS_PROXY } });
	const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
	await p.route(/(googletagmanager|google-analytics|googleadservices|doubleclick|stats\.wp\.com)/, r => r.abort());
	await p.goto('https://axiomsystems.systems/', { waitUntil: 'load' });
	const seq = [];
	for (let i = 0; i < 9; i++) { await p.keyboard.press('Tab'); seq.push(await p.evaluate(() => { const a = document.activeElement; return (a.getAttribute('href') || a.tagName) + (a.matches(':focus-visible') ? ' [focus-visible:' + getComputedStyle(a).outlineStyle + ']' : ''); })); }
	await p.keyboard.press('Shift+Tab'); 
	console.log(seq.join('\n'));
	await p.focus('.axp-call'); await p.screenshot({ path: 'shots-live/focus-header.png', clip: { x: 900, y: 0, width: 540, height: 72 } });
	await b.close();
})();
