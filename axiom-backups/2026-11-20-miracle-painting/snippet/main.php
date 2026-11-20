<?php
/**
 * Axiom Demo – Miracle Painting Page Enhancements
 * Page 2118 only: is_page(2118), its WordPress/Elementor previews, and signed Elementor preview links for post 2118.
 * It outputs nothing on any other page.
 * The page is native Elementor V4; this adds:
 *  - the demo estimate form in #mp-form: name, phone, service, ZIP, optional details. DEMO MODE: it runs entirely in the
 *    browser. There is no <form> element, no submit event, no field names and no request of any kind, so nothing reaches
 *    the CRM, email or SMS (Axiom CRM Sync / Form Protection only handle Jetpack form 1096).
 *  - estimate links: smooth scroll to the form card; each Services card's link (#q-1..6) preselects its service;
 *  - heading accents and inline <strong> colours, the header colour (the site's Additional CSS repaints every <header>),
 *    the sticky-header fix, and the phone bar, hidden over the hero buttons, at the form and while the site chat is open.
 * Rollback: unpublish this snippet. The page still shows every section and photo; the form card says to call.
 */
namespace AngieSnippets\AxiomDemoMiraclePainting;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Closures only (no named functions/constants), so the file can be re-validated while the live copy is loaded.
$axiom_ma_applies = static function () {
	$pid = 2118;
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
<style id="mp-demo-css">
@media (prefers-reduced-motion: no-preference){html{scroll-behavior:smooth}}
#top{background-color:rgba(16,38,63,.96)!important}
/* the site sets overflow-x:hidden on html/body, which turns body into a scroll container and breaks the sticky header */
html:not(#mp-x),body:not(#mp-x){overflow-x:clip!important;overflow-y:visible!important}
#hero h1 em,#before-after h2 em,#before-after h3 em,#estimate h2 em{font-style:normal;color:#f4a62a}
#services h2 em,#work h2 em,#process h2 em,#about h2 em{font-style:normal;color:#94560a}
#hero b{color:#f4a62a;font-weight:700}
#services strong,#process strong,#about strong{color:#16202c}
#estimate strong,footer strong{color:#ffffff}
#top a[href^="tel:"]{white-space:nowrap}
#mp-ribbon strong{color:#f4a62a}
/* phone bar */
#mp-bar{transition:transform .25s ease,opacity .25s ease}
#mp-bar.mp-hide{transform:translateY(110%);opacity:0;pointer-events:none}
/* demo estimate form */
#mp-form{font-family:"Figtree",system-ui,sans-serif;color:#16202c;overflow-wrap:anywhere}
#mp-form .mp-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px 12px}
#mp-form .mp-full{grid-column:1/-1}
@media (max-width:767px){#mp-form .mp-grid{grid-template-columns:minmax(0,1fr)}}
#mp-form label{display:block;font-weight:600;font-size:.9rem;margin:0 0 6px;color:#16202c}
#mp-form label .mp-opt{font-weight:400;color:#58626e}
#mp-form input,#mp-form select,#mp-form textarea{display:block;width:100%;box-sizing:border-box;font:inherit;font-size:16px;line-height:1.35;color:#16202c;background:#fcfcfa;border:1.5px solid #d0d5dc;border-radius:10px;padding:12px 14px;min-height:50px;margin:0;box-shadow:none;transition:border-color .15s,box-shadow .15s}
#mp-form select{appearance:none;-webkit-appearance:none;padding-right:42px;background-image:linear-gradient(45deg,transparent 50%,#16202c 50%),linear-gradient(135deg,#16202c 50%,transparent 50%);background-position:calc(100% - 22px) 52%,calc(100% - 16px) 52%;background-size:6px 6px;background-repeat:no-repeat}
#mp-form textarea{min-height:100px;resize:vertical}
#mp-form input:focus,#mp-form select:focus,#mp-form textarea:focus{outline:none;border-color:#94560a;background:#fff;box-shadow:0 0 0 3px rgba(244,166,42,.35)}
#mp-form [aria-invalid="true"]{border-color:#b3261e}
#mp-form .mp-err{display:none;color:#b3261e;font-size:.85rem;font-weight:600;margin:5px 0 0}
#mp-form .mp-err.on{display:block}
#mp-form .mp-count{float:right;font-weight:400;color:#58626e;font-size:.8rem}
#mp-form .mp-actions{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;margin-top:18px}
#mp-form .mp-go{display:inline-flex;align-items:center;justify-content:center;min-height:54px;padding:0 28px;border:0;border-radius:999px;background:#f4a62a;color:#241500;font:600 16px/1 "Figtree",system-ui,sans-serif;cursor:pointer;transition:background-color .15s}
#mp-form .mp-go:hover,#mp-form .mp-go:focus{background:#ffb940;color:#241500}
#mp-form .mp-link,#mp-form .mp-link:hover,#mp-form .mp-link:focus{background:none;border:0;padding:6px 0;font:inherit;font-weight:500;font-size:.92rem;color:#58626e;text-decoration:underline;cursor:pointer}
#mp-form .mp-fine{flex-basis:100%;margin:0;font-size:.85rem;color:#58626e}
#mp-form button:focus-visible{outline:3px solid #f4a62a;outline-offset:3px}
@media (max-width:767px){#mp-form .mp-go{width:100%}}
#mp-form.is-done .mp-f{display:none}
#mp-form .mp-done{display:none}
#mp-form.is-done .mp-done{display:block}
#mp-form .mp-done:focus{outline:none}
#mp-form .mp-tick{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;background:#f4a62a;color:#241500;font-size:24px;font-weight:800;margin-bottom:14px}
#mp-form .mp-badge{display:inline-block;font-size:.85rem;background:#fff4d6;color:#7a5600;border-radius:8px;padding:6px 10px;margin-bottom:12px}
#mp-form .mp-done h4{font-family:"Barlow Condensed",system-ui,sans-serif;font-weight:700;font-size:1.9rem;line-height:1.05;margin:0 0 10px;color:#94560a}
#mp-form .mp-done p{margin:0 0 14px;color:#58626e;line-height:1.55}
#mp-form dl{margin:0 0 16px;border-top:1px solid #e2dfd6}
#mp-form dl div{display:grid;grid-template-columns:90px minmax(0,1fr);gap:10px;padding:9px 0;border-bottom:1px solid #e2dfd6}
#mp-form dt{color:#58626e;font-size:.92rem}
#mp-form dd{margin:0;font-weight:600}
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
<script id="mp-demo-js">
(function () {
  var d = document, $ = function (s, r) { return (r || d).querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  /* ---------- demo estimate form ---------- */
  var mount = $('#mp-form');
  // order matches the Services cards #q-1..6
  var SERVICES = ['Exterior painting', 'Interior painting', 'Commercial painting', 'Stucco / coastal homes', 'Decks / outdoor', 'Doors / trim', 'Something else'];
  var MAX = 400;
  if (mount) {
    mount.innerHTML =
      '<div class="mp-f" role="group" aria-label="Estimate request (demo)">' +
      '<div class="mp-grid">' +
        '<div><label for="mp-n">Your name</label><input id="mp-n" type="text" autocomplete="off" maxlength="80" aria-describedby="mp-n-e"><p class="mp-err" id="mp-n-e">Please enter your name.</p></div>' +
        '<div><label for="mp-p">Phone</label><input id="mp-p" type="tel" inputmode="tel" autocomplete="off" maxlength="20" placeholder="(727) 555-0123" aria-describedby="mp-p-e"><p class="mp-err" id="mp-p-e">Please enter a 10-digit phone number.</p></div>' +
        '<div><label for="mp-s">Service</label><select id="mp-s" aria-describedby="mp-s-e"><option value="">Choose one…</option>' + SERVICES.map(function (s) { return '<option>' + esc(s) + '</option>'; }).join('') + '</select><p class="mp-err" id="mp-s-e">Pick the service you need.</p></div>' +
        '<div><label for="mp-z">ZIP code</label><input id="mp-z" type="text" inputmode="numeric" autocomplete="off" maxlength="5" placeholder="33756" aria-describedby="mp-z-e"><p class="mp-err" id="mp-z-e">Please enter a 5-digit ZIP.</p></div>' +
        '<div class="mp-full"><label for="mp-d">What do you need? <span class="mp-opt">(optional)</span><span class="mp-count" id="mp-c" aria-hidden="true">0/' + MAX + '</span></label><textarea id="mp-d" maxlength="' + MAX + '" placeholder="e.g. Repaint the outside of a one-story stucco house before listing it"></textarea></div>' +
      '</div>' +
      '<div class="mp-actions">' +
        '<button type="button" class="mp-go" id="mp-go">Send My Request</button>' +
        '<button type="button" class="mp-link" id="mp-sample">Fill in sample details</button>' +
        '<p class="mp-fine">Demo mode: nothing is sent, texted or emailed.</p>' +
      '</div></div>' +
      '<div class="mp-done" id="mp-done" role="status" aria-live="polite" tabindex="-1"></div>';
    var F = { n: $('#mp-n'), p: $('#mp-p'), s: $('#mp-s'), z: $('#mp-z'), d: $('#mp-d') };
    var phone10 = function (s) { var x = (s || '').replace(/\D/g, ''); if (x.length === 11 && x.charAt(0) === '1') x = x.slice(1); return x; };
    var fmt = function (x) { return x.length === 10 ? '(' + x.slice(0, 3) + ') ' + x.slice(3, 6) + '-' + x.slice(6) : x; };
    var CHECK = {
      n: function () { return F.n.value.trim().length >= 2; },
      p: function () { return phone10(F.p.value).length === 10; },
      s: function () { return F.s.value !== ''; },
      z: function () { return /^\d{5}$/.test(F.z.value); }
    };
    var mark = function (k, ok) { F[k].setAttribute('aria-invalid', ok ? 'false' : 'true'); $('#mp-' + k + '-e').classList.toggle('on', !ok); };
    var touched = {}, attempted = false;
    Object.keys(CHECK).forEach(function (k) {
      // errors show after a submit attempt or once something was typed, never just for tabbing past
      F[k].addEventListener('blur', function () { if (!attempted && F[k].value.trim() === '') return; touched[k] = true; mark(k, CHECK[k]()); });
      F[k].addEventListener(k === 's' ? 'change' : 'input', function () { if (touched[k]) mark(k, CHECK[k]()); });
    });
    F.p.addEventListener('blur', function () { var x = phone10(F.p.value); if (x.length === 10) F.p.value = fmt(x); });
    F.z.addEventListener('input', function () { F.z.value = F.z.value.replace(/\D/g, '').slice(0, 5); });
    F.d.addEventListener('input', function () { $('#mp-c').textContent = F.d.value.length + '/' + MAX; });
    var submit = function () {
      var bad = null; attempted = true;
      Object.keys(CHECK).forEach(function (k) { touched[k] = true; var ok = CHECK[k](); mark(k, ok); if (!ok && !bad) bad = k; });
      if (bad) { F[bad].focus(); return; }
      var first = F.n.value.trim().split(/\s+/)[0];
      var rows = [['Name', F.n.value.trim()], ['Phone', fmt(phone10(F.p.value))], ['Service', F.s.value], ['ZIP', F.z.value]];
      if (F.d.value.trim()) rows.push(['Details', F.d.value.trim()]);
      var done = $('#mp-done');
      done.innerHTML = '<div class="mp-tick" aria-hidden="true">✓</div>' +
        '<h4>Thanks, ' + esc(first) + '! Request received.</h4>' +
        '<p>We\'ll reach out soon to set up a time to take a look.</p>' +
        '<dl>' + rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + esc(r[1]) + '</dd></div>'; }).join('') + '</dl>' +
        '<p class="mp-badge">Demo preview: nothing was sent.</p>' +
        '<p><button type="button" class="mp-link" id="mp-again">Start a new request</button></p>';
      mount.classList.add('is-done');
      done.focus({ preventScroll: true });
      var card = $('#estimate-form') || mount, r = card.getBoundingClientRect();
      if (r.top < 90 || r.top > innerHeight * 0.5) card.scrollIntoView({ block: 'start' });
      $('#mp-again').addEventListener('click', function () {
        Object.keys(F).forEach(function (k) { F[k].value = ''; F[k].removeAttribute('aria-invalid'); });
        Object.keys(CHECK).forEach(function (k) { $('#mp-' + k + '-e').classList.remove('on'); });
        touched = {}; attempted = false; $('#mp-c').textContent = '0/' + MAX;
        mount.classList.remove('is-done'); done.innerHTML = ''; F.n.focus();
      });
    };
    $('#mp-go').addEventListener('click', submit);
    mount.addEventListener('keydown', function (e) { if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); submit(); } });
    $('#mp-sample').addEventListener('click', function () {
      F.n.value = 'Sam Rivera'; F.p.value = '(727) 555-0142'; F.z.value = '33756';
      if (!F.s.value) F.s.value = SERVICES[0];
      F.d.value = 'Repaint the outside of a one-story stucco home, including trim and the garage door.';
      $('#mp-c').textContent = F.d.value.length + '/' + MAX;
      Object.keys(CHECK).forEach(function (k) { touched[k] = true; mark(k, CHECK[k]()); });
      $('#mp-go').focus();
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
  var bar = $('#mp-bar'), ctas = $('#hero-ctas') || $('#hero'), ef = $('#estimate-form');
  if (bar && 'IntersectionObserver' in window) {
    var atHero = true, atForm = false, chatOpen = false;
    var sync = function () { bar.classList.toggle('mp-hide', atHero || atForm || chatOpen); };
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
