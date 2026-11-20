<?php
/**
 * Axiom Demo – Dave's Plumbing Page Enhancements
 * Page 2164 only: is_page(2164), its WordPress/Elementor previews, and signed Elementor preview links for post 2164.
 * It outputs nothing on any other page.
 * The page is native Elementor V4; this adds:
 *  - the demo estimate form in #dp-form: name, phone, service, ZIP, optional details. DEMO MODE: it runs entirely in the
 *    browser. There is no <form> element, no submit event, no field names and no request of any kind, so nothing reaches
 *    the CRM, email or SMS (Axiom CRM Sync / Form Protection only handle Jetpack form 1096).
 *  - estimate links: smooth scroll to the form card; each Services card's link (#q-1..6) preselects its service;
 *  - heading accents and inline <strong> colours, the header colour (the site's Additional CSS repaints every <header>),
 *    the sticky-header fix, and the phone bar, hidden over the hero buttons, at the form and while the site chat is open.
 * Rollback: unpublish this snippet. The page still shows every section and photo; the form card says to call.
 */
namespace AngieSnippets\AxiomDemoDavesPlumbing;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Closures only (no named functions/constants), so the file can be re-validated while the live copy is loaded.
$axiom_ma_applies = static function () {
	$pid = 2164;
	if ( is_admin() || is_feed() || is_embed() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return false;
	}
	// phpcs:disable WordPress.Security.NonceVerification.Recommended -- read-only scoping checks; Elementor validates the token itself.
	if ( isset( $_GET['elementor_preview_token'] ) ) {
		$parts   = explode( '.', sanitize_text_field( wp_unslash( $_GET['elementor_preview_token'] ) ) );
		$payload = json_decode( (string) base64_decode( strtr( $parts[0], '-_', '+/' ) ), true );
		return is_array( $payload ) && isset( $payload['p'] ) && $pid === (int) $payload['p'];
	}
	if ( isset( $_GET['elementor-preview'] ) ) {
		return $pid === (int) $_GET['elementor-preview'];
	}
	// phpcs:enable
	return is_page( $pid );
};

add_action(
	'wp_head',
	function () use ( $axiom_ma_applies ) {
		if ( ! $axiom_ma_applies() ) {
			return;
		}
		?>
<style id="dp-demo-css">
@media (prefers-reduced-motion: no-preference){html{scroll-behavior:smooth}}
#top{background-color:rgba(11,42,74,.96)!important}
/* the site sets overflow-x:hidden on html/body, which turns body into a scroll container and breaks the sticky header */
html:not(#dp-x),body:not(#dp-x){overflow-x:clip!important;overflow-y:visible!important}
#hero h1 em,#estimate h2 em{font-style:normal;color:#35c3e8}
#services h2 em,#showcase h2 em,#work h2 em,#process h2 em,#about h2 em{font-style:normal;color:#0b6b8a}
#hero b{color:#35c3e8;font-weight:700}
#services strong,#showcase strong,#process strong,#about strong{color:#12202e}
#estimate strong,footer strong{color:#ffffff}
#top a[href^="tel:"]{white-space:nowrap}
#dp-ribbon strong{color:#35c3e8}
/* service icons */
#ic-1{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2312507f' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='6' y='3' width='12' height='18' rx='3'/%3E%3Cpath d='M10 7h4M12 11v5M10 16h4'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:30px 30px}
#ic-2{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2312507f' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 3s6 6.2 6 10.5A6 6 0 0 1 6 13.5C6 9.2 12 3 12 3z'/%3E%3Cpath d='M9.5 14a2.5 2.5 0 0 0 2.5 2.5'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:30px 30px}
#ic-3{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2312507f' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14.7 6.3a4 4 0 0 0-5 5L3 18l3 3 6.7-6.7a4 4 0 0 0 5-5l-2.4 2.4-2.6-.6-.6-2.6z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:30px 30px}
#ic-4{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2312507f' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 9h9a4 4 0 0 1 4 4v1'/%3E%3Cpath d='M8 9V6h4M17 14v2a1 1 0 0 0 2 0v-2zM4 9v4'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:30px 30px}
#ic-5{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2312507f' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 8h8v8h10'/%3E%3Cpath d='M3 6v4M21 14v4M11 6v4'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:30px 30px}
#ic-6{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2312507f' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='4' y='3' width='16' height='18' rx='1'/%3E%3Cpath d='M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:30px 30px}
/* phone bar */
#dp-bar{transition:transform .25s ease,opacity .25s ease}
#dp-bar.dp-hide{transform:translateY(110%);opacity:0;pointer-events:none}
/* demo estimate form */
#dp-form{font-family:"Figtree",system-ui,sans-serif;color:#12202e;overflow-wrap:anywhere}
#dp-form .dp-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px 12px}
#dp-form .dp-full{grid-column:1/-1}
@media (max-width:767px){#dp-form .dp-grid{grid-template-columns:minmax(0,1fr)}}
#dp-form label{display:block;font-weight:600;font-size:.9rem;margin:0 0 6px;color:#12202e}
#dp-form label .dp-opt{font-weight:400;color:#566574}
#dp-form input,#dp-form select,#dp-form textarea{display:block;width:100%;box-sizing:border-box;font:inherit;font-size:16px;line-height:1.35;color:#12202e;background:#fafcfe;border:1.5px solid #cdd8e2;border-radius:10px;padding:12px 14px;min-height:50px;margin:0;box-shadow:none;transition:border-color .15s,box-shadow .15s}
#dp-form select{appearance:none;-webkit-appearance:none;padding-right:42px;background-image:linear-gradient(45deg,transparent 50%,#12202e 50%),linear-gradient(135deg,#12202e 50%,transparent 50%);background-position:calc(100% - 22px) 52%,calc(100% - 16px) 52%;background-size:6px 6px;background-repeat:no-repeat}
#dp-form textarea{min-height:100px;resize:vertical}
#dp-form input:focus,#dp-form select:focus,#dp-form textarea:focus{outline:none;border-color:#0b6b8a;background:#fff;box-shadow:0 0 0 3px rgba(53,195,232,.35)}
#dp-form [aria-invalid="true"]{border-color:#b3261e}
#dp-form .dp-err{display:none;color:#b3261e;font-size:.85rem;font-weight:600;margin:5px 0 0}
#dp-form .dp-err.on{display:block}
#dp-form .dp-count{float:right;font-weight:400;color:#566574;font-size:.8rem}
#dp-form .dp-actions{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;margin-top:18px}
#dp-form .dp-go{display:inline-flex;align-items:center;justify-content:center;min-height:54px;padding:0 28px;border:0;border-radius:999px;background:#35c3e8;color:#062033;font:600 16px/1 "Figtree",system-ui,sans-serif;cursor:pointer;transition:background-color .15s}
#dp-form .dp-go:hover,#dp-form .dp-go:focus{background:#6fd8f2;color:#062033}
#dp-form .dp-link,#dp-form .dp-link:hover,#dp-form .dp-link:focus{background:none;border:0;padding:6px 0;font:inherit;font-weight:500;font-size:.92rem;color:#566574;text-decoration:underline;cursor:pointer}
#dp-form .dp-fine{flex-basis:100%;margin:0;font-size:.85rem;color:#566574}
#dp-form button:focus-visible{outline:3px solid #35c3e8;outline-offset:3px}
@media (max-width:767px){#dp-form .dp-go{width:100%}}
#dp-form.is-done .dp-f{display:none}
#dp-form .dp-done{display:none}
#dp-form.is-done .dp-done{display:block}
#dp-form .dp-done:focus{outline:none}
#dp-form .dp-tick{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;background:#35c3e8;color:#062033;font-size:24px;font-weight:800;margin-bottom:14px}
#dp-form .dp-badge{display:inline-block;font-size:.85rem;background:#e2f6fc;color:#0b5a75;border-radius:8px;padding:6px 10px;margin-bottom:12px}
#dp-form .dp-done h4{font-family:"Barlow Condensed",system-ui,sans-serif;font-weight:700;font-size:1.9rem;line-height:1.05;margin:0 0 10px;color:#0b6b8a}
#dp-form .dp-done p{margin:0 0 14px;color:#566574;line-height:1.55}
#dp-form dl{margin:0 0 16px;border-top:1px solid #dbe4ec}
#dp-form dl div{display:grid;grid-template-columns:90px minmax(0,1fr);gap:10px;padding:9px 0;border-bottom:1px solid #dbe4ec}
#dp-form dt{color:#566574;font-size:.92rem}
#dp-form dd{margin:0;font-weight:600}
</style>
		<?php
	},
	60
);

add_action(
	'wp_footer',
	function () use ( $axiom_ma_applies ) {
		static $done = false;
		if ( $done || ! $axiom_ma_applies() ) {
			return;
		}
		$done = true;
		?>
<script id="dp-demo-js">
(function () {
  var d = document, $ = function (s, r) { return (r || d).querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  /* ---------- demo estimate form ---------- */
  var mount = $('#dp-form');
  // order matches the Services cards #q-1..6
  var SERVICES = ['Water heater', 'Drain cleaning', 'Leak / repair', 'Fixtures / faucets', 'Repipe / water lines', 'Commercial / mechanical', 'Something else'];
  var MAX = 400;
  if (mount) {
    mount.innerHTML =
      '<div class="dp-f" role="group" aria-label="Estimate request (demo)">' +
      '<div class="dp-grid">' +
        '<div><label for="dp-n">Your name</label><input id="dp-n" type="text" autocomplete="off" maxlength="80" aria-describedby="dp-n-e"><p class="dp-err" id="dp-n-e">Please enter your name.</p></div>' +
        '<div><label for="dp-p">Phone</label><input id="dp-p" type="tel" inputmode="tel" autocomplete="off" maxlength="20" placeholder="(941) 555-0123" aria-describedby="dp-p-e"><p class="dp-err" id="dp-p-e">Please enter a 10-digit phone number.</p></div>' +
        '<div><label for="dp-s">Service</label><select id="dp-s" aria-describedby="dp-s-e"><option value="">Choose one…</option>' + SERVICES.map(function (s) { return '<option>' + esc(s) + '</option>'; }).join('') + '</select><p class="dp-err" id="dp-s-e">Pick the service you need.</p></div>' +
        '<div><label for="dp-z">ZIP code</label><input id="dp-z" type="text" inputmode="numeric" autocomplete="off" maxlength="5" placeholder="34285" aria-describedby="dp-z-e"><p class="dp-err" id="dp-z-e">Please enter a 5-digit ZIP.</p></div>' +
        '<div class="dp-full"><label for="dp-d">What is going on? <span class="dp-opt">(optional)</span><span class="dp-count" id="dp-c" aria-hidden="true">0/' + MAX + '</span></label><textarea id="dp-d" maxlength="' + MAX + '" placeholder="e.g. Water heater is leaking and the house has no hot water"></textarea></div>' +
      '</div>' +
      '<div class="dp-actions">' +
        '<button type="button" class="dp-go" id="dp-go">Send My Request</button>' +
        '<button type="button" class="dp-link" id="dp-sample">Fill in sample details</button>' +
        '<p class="dp-fine">Demo mode: nothing is sent, texted or emailed.</p>' +
      '</div></div>' +
      '<div class="dp-done" id="dp-done" role="status" aria-live="polite" tabindex="-1"></div>';
    var F = { n: $('#dp-n'), p: $('#dp-p'), s: $('#dp-s'), z: $('#dp-z'), d: $('#dp-d') };
    var phone10 = function (s) { var x = (s || '').replace(/\D/g, ''); if (x.length === 11 && x.charAt(0) === '1') x = x.slice(1); return x; };
    var fmt = function (x) { return x.length === 10 ? '(' + x.slice(0, 3) + ') ' + x.slice(3, 6) + '-' + x.slice(6) : x; };
    var CHECK = {
      n: function () { return F.n.value.trim().length >= 2; },
      p: function () { return phone10(F.p.value).length === 10; },
      s: function () { return F.s.value !== ''; },
      z: function () { return /^\d{5}$/.test(F.z.value); }
    };
    var mark = function (k, ok) { F[k].setAttribute('aria-invalid', ok ? 'false' : 'true'); $('#dp-' + k + '-e').classList.toggle('on', !ok); };
    var touched = {}, attempted = false;
    Object.keys(CHECK).forEach(function (k) {
      // errors show after a submit attempt or once something was typed, never just for tabbing past
      F[k].addEventListener('blur', function () { if (!attempted && F[k].value.trim() === '') return; touched[k] = true; mark(k, CHECK[k]()); });
      F[k].addEventListener(k === 's' ? 'change' : 'input', function () { if (touched[k]) mark(k, CHECK[k]()); });
    });
    F.p.addEventListener('blur', function () { var x = phone10(F.p.value); if (x.length === 10) F.p.value = fmt(x); });
    F.z.addEventListener('input', function () { F.z.value = F.z.value.replace(/\D/g, '').slice(0, 5); });
    F.d.addEventListener('input', function () { $('#dp-c').textContent = F.d.value.length + '/' + MAX; });
    var submit = function () {
      var bad = null; attempted = true;
      Object.keys(CHECK).forEach(function (k) { touched[k] = true; var ok = CHECK[k](); mark(k, ok); if (!ok && !bad) bad = k; });
      if (bad) { F[bad].focus(); return; }
      var first = F.n.value.trim().split(/\s+/)[0];
      var rows = [['Name', F.n.value.trim()], ['Phone', fmt(phone10(F.p.value))], ['Service', F.s.value], ['ZIP', F.z.value]];
      if (F.d.value.trim()) rows.push(['Details', F.d.value.trim()]);
      var done = $('#dp-done');
      done.innerHTML = '<div class="dp-tick" aria-hidden="true">✓</div>' +
        '<h4>Thanks, ' + esc(first) + '! Request received.</h4>' +
        '<p>We will reach out soon to set up a time.</p>' +
        '<dl>' + rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + esc(r[1]) + '</dd></div>'; }).join('') + '</dl>' +
        '<p class="dp-badge">Demo preview: nothing was sent.</p>' +
        '<p><button type="button" class="dp-link" id="dp-again">Start a new request</button></p>';
      mount.classList.add('is-done');
      done.focus({ preventScroll: true });
      var card = $('#estimate-form') || mount, r = card.getBoundingClientRect();
      if (r.top < 90 || r.top > innerHeight * 0.5) card.scrollIntoView({ block: 'start' });
      $('#dp-again').addEventListener('click', function () {
        Object.keys(F).forEach(function (k) { F[k].value = ''; F[k].removeAttribute('aria-invalid'); });
        Object.keys(CHECK).forEach(function (k) { $('#dp-' + k + '-e').classList.remove('on'); });
        touched = {}; attempted = false; $('#dp-c').textContent = '0/' + MAX;
        mount.classList.remove('is-done'); done.innerHTML = ''; F.n.focus();
      });
    };
    $('#dp-go').addEventListener('click', submit);
    mount.addEventListener('keydown', function (e) { if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); submit(); } });
    $('#dp-sample').addEventListener('click', function () {
      F.n.value = 'Sam Rivera'; F.p.value = '(941) 555-0142'; F.z.value = '34285';
      if (!F.s.value) F.s.value = SERVICES[0];
      F.d.value = 'Water heater is leaking at the base and we have no hot water.';
      $('#dp-c').textContent = F.d.value.length + '/' + MAX;
      Object.keys(CHECK).forEach(function (k) { touched[k] = true; mark(k, CHECK[k]()); });
      $('#dp-go').focus();
    });

    // estimate links: Services cards (#q-1..6) preselect their service; desktop focuses the first empty field
    var fine = window.matchMedia && matchMedia('(pointer: fine)').matches;
    d.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href="#estimate-form"]');
      if (!a) return;
      var host = a.id && /^q-\d$/.test(a.id) ? a : a.closest('[id^="q-"]');
      var n = host ? parseInt(host.id.slice(2), 10) : 0;
      if (n && SERVICES[n - 1] && !mount.classList.contains('is-done')) { F.s.value = SERVICES[n - 1]; if (touched.s) mark('s', true); }
      if (fine && !mount.classList.contains('is-done')) setTimeout(function () { (F.n.value ? (F.p.value ? F.s : F.p) : F.n).focus({ preventScroll: true }); }, 700);
    });
  }

  /* ---------- phone bar: hidden over the hero buttons, at the form, and while the site chat is open ---------- */
  var bar = $('#dp-bar'), ctas = $('#hero-ctas') || $('#hero'), ef = $('#estimate-form');
  if (bar && 'IntersectionObserver' in window) {
    var atHero = true, atForm = false, chatOpen = false;
    var sync = function () { bar.classList.toggle('dp-hide', atHero || atForm || chatOpen); };
    sync();
    if (ctas) new IntersectionObserver(function (en) { atHero = en[0].isIntersecting; sync(); }, { threshold: 0 }).observe(ctas);
    if (ef) new IntersectionObserver(function (en) { atForm = en[0].isIntersecting; sync(); }, { threshold: 0.1 }).observe(ef);
    var watchChat = function (cw) {
      var read = function () { chatOpen = cw.getAttribute('data-active') === 'true'; sync(); };
      new MutationObserver(read).observe(cw, { attributes: true, attributeFilter: ['data-active'] }); read();
    };
    var cw = $('chat-widget');
    if (cw) watchChat(cw);
    else new MutationObserver(function (m, o) { var c = $('chat-widget'); if (c) { o.disconnect(); watchChat(c); } }).observe(d.body, { childList: true, subtree: true });
  }
})();
</script>
		<?php
	},
	60
);
