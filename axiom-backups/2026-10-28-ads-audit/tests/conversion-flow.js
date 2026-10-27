// Read-only conversion flow test on the live Get Started page. Jetpack's form POST is fulfilled in the browser
// (never reaches WordPress), so no entry, email, GHL sync or real conversion is created.
const { chromium } = require('playwright'); const fs = require('fs');
const URL0 = 'https://axiomsystems.systems/get-started/?plan=growth&nc=' + Date.now();
const conv = p => p.evaluate(() => (window.dataLayer || []).filter(a => a && a[0] === 'event' && a[1] === 'conversion').map(a => JSON.parse(JSON.stringify(a[2]))));
const allEvents = p => p.evaluate(() => (window.dataLayer || []).filter(a => a && (a[0] === 'event' || a[0] === 'config')).map(a => [a[0], a[1], a[2] && (a[2].send_to || '')]));
async function fill(p) {
  const f = '.axgs form';
  await p.fill(`${f} [name$="-name"]`, 'Audit Test'); await p.fill(`${f} [name$="-businessname"]`, 'Audit Co');
  await p.fill(`${f} [name$="-email"]`, 'audit-test@example.com'); await p.fill(`${f} [name$="-phone"]`, '7275550100');
  await p.fill(`${f} textarea`, 'Conversion tracking audit (not a real lead).');
}
const ok = (id, extra = {}) => JSON.stringify({ success: true, data: [], refreshArgs: { 'contact-form-id': '1095', 'contact-form-sent': String(id), 'contact-form-hash': 'x', _wpnonce: 'x' }, ...extra });
(async () => {
  const b = await chromium.launch(); const R = {};
  async function page(mockCheck, ajaxBody, delay = 0) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    await ctx.route(/(googletagmanager|google-analytics|googleadservices|doubleclick|stats\.wp\.com|leadconnectorhq|challenges\.cloudflare)/, r => r.abort());
    const log = { ajax: 0, check: [], ajaxAt: [] };
    await ctx.route(/admin-ajax\.php\?action=grunion-contact-form/, async r => { log.ajax++; log.ajaxAt.push(Date.now()); if (delay) await new Promise(s => setTimeout(s, delay)); await r.fulfill({ status: 200, contentType: 'application/json', body: ajaxBody }); });
    await ctx.route(/wp-json\/axiom\/v1\/lead-check/, async r => { const body = r.request().postData(); if (mockCheck) { log.check.push(['mocked', body]); await r.fulfill({ status: 200, contentType: 'application/json', body: '{"countable":true}' }); } else { const res = await r.fetch(); const j = await res.text(); log.check.push(['real', body, j]); await r.fulfill({ response: res, body: j }); } });
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(URL0, { waitUntil: 'load' }); await p.waitForTimeout(1500);
    return { ctx, p, log, errs };
  }
  // A + B: page load and empty submit
  let s = await page(false, ok(1));
  R.A_pageLoad = { conversions: await conv(s.p), gtagCalls: await allEvents(s.p) };
  await s.p.click('.axgs form button[type=submit]'); await s.p.waitForTimeout(1500);
  R.B_emptySubmitClick = { ajaxPosts: s.log.ajax, conversions: await conv(s.p) };
  // C: success for an entry that doesn't exist -> real server check must refuse
  await fill(s.p); await s.p.click('.axgs form button[type=submit]'); await s.p.waitForTimeout(3000);
  R.C_fakeEntryRealCheck = { ajaxPosts: s.log.ajax, check: s.log.check, conversions: await conv(s.p), tracker: await s.p.evaluate(() => window.axiomLeadTracking), errs: s.errs };
  await s.ctx.close();
  // D: successful, countable submission (check mocked); response delayed 2 s to see nothing fires on click
  s = await page(true, ok(990002), 2000);
  await fill(s.p); await s.p.click('.axgs form button[type=submit]'); await s.p.waitForTimeout(800);
  const atClick = await conv(s.p);
  await s.p.waitForTimeout(3500);
  R.D_success = { conversionsDuringPendingRequest: atClick, conversions: await conv(s.p), tracker: await s.p.evaluate(() => window.axiomLeadTracking), successShown: await s.p.evaluate(() => !!document.querySelector('.axgs .submission-success, .axgs [id^="contact-form-success"]')), urlAfter: s.p.url().replace(/_wpnonce=[^&]*/, '_wpnonce=…'), errs: s.errs };
  // E: same entry ID again (duplicate response) in the same page, then reload of the success URL
  await s.p.evaluate(() => fetch('/wp-admin/admin-ajax.php?action=grunion-contact-form', { method: 'POST', body: new FormData() }));
  await s.p.waitForTimeout(1500);
  R.E_duplicateSameEntry = { conversions: await conv(s.p), tracker: await s.p.evaluate(() => window.axiomLeadTracking) };
  await s.p.reload({ waitUntil: 'load' }); await s.p.waitForTimeout(1500);
  R.E_reloadSuccessUrl = { conversions: await conv(s.p) };
  await s.ctx.close();
  // F: failed submission
  s = await page(true, JSON.stringify({ success: false, data: { error: 'test failure' } }));
  await fill(s.p); await s.p.click('.axgs form button[type=submit]'); await s.p.waitForTimeout(2500);
  R.F_failedSubmission = { ajaxPosts: s.log.ajax, check: s.log.check.length, conversions: await conv(s.p) };
  await s.ctx.close(); await b.close();
  fs.writeFileSync('tests/conversion-flow-results.json', JSON.stringify(R, null, 1)); console.log(JSON.stringify(R, null, 1));
})();
