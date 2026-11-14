<?php
/**
 * Axiom Demo – Martin Arborcare Page Enhancements
 * Page 2057 only: is_page(2057), its WordPress/Elementor previews, and signed Elementor preview links for post 2057.
 * It outputs nothing on any other page.
 * The page is native Elementor V4; this adds:
 *  - the demo estimate form in #ma-form: name, phone, service, ZIP, optional details. DEMO MODE: it runs entirely in the
 *    browser. There is no <form> element, no submit event, no field names and no request of any kind, so nothing reaches
 *    the CRM, email or SMS (Axiom CRM Sync / Form Protection only handle Jetpack form 1096).
 *  - estimate links: smooth scroll to the form card; each Services card's link (#q-1..6) preselects its service;
 *  - heading accents and inline <strong> colours, the header colour (the site's Additional CSS repaints every <header>),
 *    the sticky-header fix, and the phone bar, hidden over the hero buttons, at the form and while the site chat is open.
 * Rollback: unpublish this snippet. The page still shows every section and photo; the form card says to call.
 */
namespace AngieSnippets\AxiomDemoMartinArborcare;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Closures only (no named functions/constants), so the file can be re-validated while the live copy is loaded.
$axiom_ma_applies = static function () {
	$pid = 2057;
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
<style id="ma-demo-css">
@media (prefers-reduced-motion: no-preference){html{scroll-behavior:smooth}}
#top{background-color:rgba(18,59,36,.96)!important}
/* the site sets overflow-x:hidden on html/body, which turns body into a scroll container and breaks the sticky header */
html:not(#ma-x),body:not(#ma-x){overflow-x:clip!important;overflow-y:visible!important}
#hero h1 em,#before-after h2 em,#estimate h2 em{font-style:normal;color:#7cc142}
#services h2 em,#work h2 em,#reviews h2 em,#about h2 em{font-style:normal;color:#2f6b12}
#hero b{color:#7cc142;font-weight:700}
#services strong,#reviews strong,#about strong{color:#18241c}
#estimate strong,footer strong{color:#ffffff}
#top a[href^="tel:"]{white-space:nowrap}
#estimate a[href^="mailto:"]{overflow-wrap:anywhere}
#ma-ribbon strong{color:#e8b44a}
/* phone bar */
#ma-bar{transition:transform .25s ease,opacity .25s ease}
#ma-bar.ma-hide{transform:translateY(110%);opacity:0;pointer-events:none}
/* demo estimate form */
#ma-form{font-family:"Figtree",system-ui,sans-serif;color:#18241c;overflow-wrap:anywhere}
#ma-form .ma-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px 12px}
#ma-form .ma-full{grid-column:1/-1}
@media (max-width:767px){#ma-form .ma-grid{grid-template-columns:minmax(0,1fr)}}
#ma-form label{display:block;font-weight:600;font-size:.9rem;margin:0 0 6px;color:#18241c}
#ma-form label .ma-opt{font-weight:400;color:#56635a}
#ma-form input,#ma-form select,#ma-form textarea{display:block;width:100%;box-sizing:border-box;font:inherit;font-size:16px;line-height:1.35;color:#18241c;background:#fbfcf9;border:1.5px solid #cfd6ca;border-radius:10px;padding:12px 14px;min-height:50px;margin:0;box-shadow:none;transition:border-color .15s,box-shadow .15s}
#ma-form select{appearance:none;-webkit-appearance:none;padding-right:42px;background-image:linear-gradient(45deg,transparent 50%,#18241c 50%),linear-gradient(135deg,#18241c 50%,transparent 50%);background-position:calc(100% - 22px) 52%,calc(100% - 16px) 52%;background-size:6px 6px;background-repeat:no-repeat}
#ma-form textarea{min-height:100px;resize:vertical}
#ma-form input:focus,#ma-form select:focus,#ma-form textarea:focus{outline:none;border-color:#2f6b12;background:#fff;box-shadow:0 0 0 3px rgba(124,193,66,.3)}
#ma-form [aria-invalid="true"]{border-color:#b3261e}
#ma-form .ma-err{display:none;color:#b3261e;font-size:.85rem;font-weight:600;margin:5px 0 0}
#ma-form .ma-err.on{display:block}
#ma-form .ma-count{float:right;font-weight:400;color:#56635a;font-size:.8rem}
#ma-form .ma-actions{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;margin-top:18px}
#ma-form .ma-go{display:inline-flex;align-items:center;justify-content:center;min-height:54px;padding:0 28px;border:0;border-radius:999px;background:#7cc142;color:#0e2a17;font:600 16px/1 "Figtree",system-ui,sans-serif;cursor:pointer;transition:background-color .15s}
#ma-form .ma-go:hover,#ma-form .ma-go:focus{background:#8fd352;color:#0e2a17}
#ma-form .ma-link,#ma-form .ma-link:hover,#ma-form .ma-link:focus{background:none;border:0;padding:6px 0;font:inherit;font-weight:500;font-size:.92rem;color:#56635a;text-decoration:underline;cursor:pointer}
#ma-form .ma-fine{flex-basis:100%;margin:0;font-size:.85rem;color:#56635a}
#ma-form button:focus-visible{outline:3px solid #7cc142;outline-offset:3px}
@media (max-width:767px){#ma-form .ma-go{width:100%}}
#ma-form.is-done .ma-f{display:none}
#ma-form .ma-done{display:none}
#ma-form.is-done .ma-done{display:block}
#ma-form .ma-done:focus{outline:none}
#ma-form .ma-tick{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;background:#7cc142;color:#0e2a17;font-size:24px;font-weight:800;margin-bottom:14px}
#ma-form .ma-badge{display:inline-block;font-size:.85rem;background:#fff4d6;color:#7a5600;border-radius:8px;padding:6px 10px;margin-bottom:12px}
#ma-form .ma-done h4{font-family:"Barlow Condensed",system-ui,sans-serif;font-weight:700;font-size:1.9rem;line-height:1.05;margin:0 0 10px;color:#2f6b12}
#ma-form .ma-done p{margin:0 0 14px;color:#56635a;line-height:1.55}
#ma-form dl{margin:0 0 16px;border-top:1px solid #dfe3d8}
#ma-form dl div{display:grid;grid-template-columns:90px minmax(0,1fr);gap:10px;padding:9px 0;border-bottom:1px solid #dfe3d8}
#ma-form dt{color:#56635a;font-size:.92rem}
#ma-form dd{margin:0;font-weight:600}
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
<script id="ma-demo-js">
(function () {
  var d = document, $ = function (s, r) { return (r || d).querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  /* ---------- demo estimate form ---------- */
  var mount = $('#ma-form');
  // order matches the Services cards #q-1..6
  var SERVICES = ['Tree trimming / removal', 'Tree health / cabling', 'Storm cleanup', 'Pavers', 'Artificial turf', 'Landscaping / lighting', 'Stump grinding', 'Something else'];
  var MAX = 400;
  if (mount) {
    mount.innerHTML =
      '<div class="ma-f" role="group" aria-label="Estimate request (demo)">' +
      '<div class="ma-grid">' +
        '<div><label for="ma-n">Your name</label><input id="ma-n" type="text" autocomplete="off" maxlength="80" aria-describedby="ma-n-e"><p class="ma-err" id="ma-n-e">Please enter your name.</p></div>' +
        '<div><label for="ma-p">Phone</label><input id="ma-p" type="tel" inputmode="tel" autocomplete="off" maxlength="20" placeholder="(727) 555-0123" aria-describedby="ma-p-e"><p class="ma-err" id="ma-p-e">Please enter a 10-digit phone number.</p></div>' +
        '<div><label for="ma-s">Service</label><select id="ma-s" aria-describedby="ma-s-e"><option value="">Choose one…</option>' + SERVICES.map(function (s) { return '<option>' + esc(s) + '</option>'; }).join('') + '</select><p class="ma-err" id="ma-s-e">Pick the service you need.</p></div>' +
        '<div><label for="ma-z">ZIP code</label><input id="ma-z" type="text" inputmode="numeric" autocomplete="off" maxlength="5" placeholder="33714" aria-describedby="ma-z-e"><p class="ma-err" id="ma-z-e">Please enter a 5-digit ZIP.</p></div>' +
        '<div class="ma-full"><label for="ma-d">What do you need? <span class="ma-opt">(optional)</span><span class="ma-count" id="ma-c" aria-hidden="true">0/' + MAX + '</span></label><textarea id="ma-d" maxlength="' + MAX + '" placeholder="e.g. Large oak over the roof needs trimming before storm season"></textarea></div>' +
      '</div>' +
      '<div class="ma-actions">' +
        '<button type="button" class="ma-go" id="ma-go">Send My Request</button>' +
        '<button type="button" class="ma-link" id="ma-sample">Fill in sample details</button>' +
        '<p class="ma-fine">Demo mode: nothing is sent, texted or emailed.</p>' +
      '</div></div>' +
      '<div class="ma-done" id="ma-done" role="status" aria-live="polite" tabindex="-1"></div>';
    var F = { n: $('#ma-n'), p: $('#ma-p'), s: $('#ma-s'), z: $('#ma-z'), d: $('#ma-d') };
    var phone10 = function (s) { var x = (s || '').replace(/\D/g, ''); if (x.length === 11 && x.charAt(0) === '1') x = x.slice(1); return x; };
    var fmt = function (x) { return x.length === 10 ? '(' + x.slice(0, 3) + ') ' + x.slice(3, 6) + '-' + x.slice(6) : x; };
    var CHECK = {
      n: function () { return F.n.value.trim().length >= 2; },
      p: function () { return phone10(F.p.value).length === 10; },
      s: function () { return F.s.value !== ''; },
      z: function () { return /^\d{5}$/.test(F.z.value); }
    };
    var mark = function (k, ok) { F[k].setAttribute('aria-invalid', ok ? 'false' : 'true'); $('#ma-' + k + '-e').classList.toggle('on', !ok); };
    var touched = {}, attempted = false;
    Object.keys(CHECK).forEach(function (k) {
      // errors show after a submit attempt or once something was typed, never just for tabbing past
      F[k].addEventListener('blur', function () { if (!attempted && F[k].value.trim() === '') return; touched[k] = true; mark(k, CHECK[k]()); });
      F[k].addEventListener(k === 's' ? 'change' : 'input', function () { if (touched[k]) mark(k, CHECK[k]()); });
    });
    F.p.addEventListener('blur', function () { var x = phone10(F.p.value); if (x.length === 10) F.p.value = fmt(x); });
    F.z.addEventListener('input', function () { F.z.value = F.z.value.replace(/\D/g, '').slice(0, 5); });
    F.d.addEventListener('input', function () { $('#ma-c').textContent = F.d.value.length + '/' + MAX; });
    var submit = function () {
      var bad = null; attempted = true;
      Object.keys(CHECK).forEach(function (k) { touched[k] = true; var ok = CHECK[k](); mark(k, ok); if (!ok && !bad) bad = k; });
      if (bad) { F[bad].focus(); return; }
      var first = F.n.value.trim().split(/\s+/)[0];
      var rows = [['Name', F.n.value.trim()], ['Phone', fmt(phone10(F.p.value))], ['Service', F.s.value], ['ZIP', F.z.value]];
      if (F.d.value.trim()) rows.push(['Details', F.d.value.trim()]);
      var done = $('#ma-done');
      done.innerHTML = '<div class="ma-tick" aria-hidden="true">✓</div>' +
        '<h4>Thanks, ' + esc(first) + '! Request received.</h4>' +
        '<p>Joe will reach out soon to set up a time to take a look.</p>' +
        '<dl>' + rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + esc(r[1]) + '</dd></div>'; }).join('') + '</dl>' +
        '<p class="ma-badge">Demo preview: nothing was sent.</p>' +
        '<p><button type="button" class="ma-link" id="ma-again">Start a new request</button></p>';
      mount.classList.add('is-done');
      done.focus({ preventScroll: true });
      var card = $('#estimate-form') || mount, r = card.getBoundingClientRect();
      if (r.top < 90 || r.top > innerHeight * 0.5) card.scrollIntoView({ block: 'start' });
      $('#ma-again').addEventListener('click', function () {
        Object.keys(F).forEach(function (k) { F[k].value = ''; F[k].removeAttribute('aria-invalid'); });
        Object.keys(CHECK).forEach(function (k) { $('#ma-' + k + '-e').classList.remove('on'); });
        touched = {}; attempted = false; $('#ma-c').textContent = '0/' + MAX;
        mount.classList.remove('is-done'); done.innerHTML = ''; F.n.focus();
      });
    };
    $('#ma-go').addEventListener('click', submit);
    mount.addEventListener('keydown', function (e) { if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); submit(); } });
    $('#ma-sample').addEventListener('click', function () {
      F.n.value = 'Sam Rivera'; F.p.value = '(727) 555-0142'; F.z.value = '33704';
      if (!F.s.value) F.s.value = SERVICES[0];
      F.d.value = 'Two live oaks over the driveway need thinning before storm season.';
      $('#ma-c').textContent = F.d.value.length + '/' + MAX;
      Object.keys(CHECK).forEach(function (k) { touched[k] = true; mark(k, CHECK[k]()); });
      $('#ma-go').focus();
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
  var bar = $('#ma-bar'), ctas = $('#hero-ctas') || $('#hero'), ef = $('#estimate-form');
  if (bar && 'IntersectionObserver' in window) {
    var atHero = true, atForm = false, chatOpen = false;
    var sync = function () { bar.classList.toggle('ma-hide', atHero || atForm || chatOpen); };
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
