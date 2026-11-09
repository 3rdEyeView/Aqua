<?php
/**
 * Axiom Demo – Fence It Up Page Enhancements
 * Page 1764 only (/fence-it-up-demo/ and its Elementor previews). The page is native Elementor; this adds:
 *  - the demo estimate form, rendered into #fiu-form: name, phone, ZIP code, fence type and a short description,
 *    with inline validation and an on-page confirmation. DEMO MODE: it runs entirely in the browser. There is no
 *    <form> element, no submit event and no request of any kind, so nothing reaches the CRM, email or SMS.
 *    (Axiom CRM Sync / Form Protection only handle Jetpack form 1096 on page 1095, server-side.)
 *  - estimate links: smooth scroll to the form, and the "… estimate →" links in Services preselect that fence type;
 *  - the gold accent on the hero headline (<em>), and hiding the phone/tablet bar while the form is on screen.
 * Rollback: unpublish this snippet (the page then shows "The estimate form is loading…" in the form card).
 */
namespace AngieSnippets\AxiomDemoFenceItUp;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Closures only (no named functions/constants), so the file can be re-validated while the live copy is loaded.
$axiom_fiu_applies = static function () {
	if ( is_admin() || is_feed() || is_embed() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return false;
	}
	// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- read-only checks.
	if ( isset( $_GET['elementor_preview_token'] ) || isset( $_GET['elementor-preview'] ) ) {
		return true;
	}
	return is_page( 1764 );
};

add_action(
	'wp_head',
	function () use ( $axiom_fiu_applies ) {
		if ( ! $axiom_fiu_applies() ) {
			return;
		}
		?>
<style id="fiu-demo-css">
@media (prefers-reduced-motion: no-preference){html{scroll-behavior:smooth}}
#hero h1 em{font-style:normal;color:#e8b931}
/* the site's Additional CSS paints every <header> charcoal (!important); keep this page's header navy */
#top{background-color:#0f1c2e!important}
#fiu-bar{transition:transform .25s ease,opacity .25s ease}
#fiu-bar.fiu-off{transform:translateY(110%);opacity:0;pointer-events:none}
#fiu-form{font-family:"Figtree",system-ui,sans-serif;color:#0f1c2e}
#fiu-form .fiu-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:14px 12px}
#fiu-form .fiu-full{grid-column:1/-1}
#fiu-form label{display:block;font-weight:700;font-size:.92rem;margin:0 0 6px}
#fiu-form label .fiu-opt{font-weight:500;color:#53647a}
#fiu-form input,#fiu-form select,#fiu-form textarea{display:block;width:100%;box-sizing:border-box;font:inherit;font-size:16px;line-height:1.35;color:#0f1c2e;background:#fff;border:1.5px solid #c9d4e0;border-radius:10px;padding:13px 14px;min-height:52px;margin:0;box-shadow:none;transition:border-color .15s,box-shadow .15s}
#fiu-form select{appearance:none;-webkit-appearance:none;padding-right:42px;background-image:linear-gradient(45deg,transparent 50%,#0f1c2e 50%),linear-gradient(135deg,#0f1c2e 50%,transparent 50%);background-position:calc(100% - 22px) 52%,calc(100% - 16px) 52%;background-size:6px 6px;background-repeat:no-repeat}
#fiu-form textarea{min-height:104px;resize:vertical}
#fiu-form input:focus,#fiu-form select:focus,#fiu-form textarea:focus{outline:none;border-color:#1d6fa5;box-shadow:0 0 0 3px rgba(91,180,236,.35)}
#fiu-form [aria-invalid="true"]{border-color:#c0392b}
#fiu-form [aria-invalid="true"]:focus{box-shadow:0 0 0 3px rgba(192,57,43,.25)}
#fiu-form .fiu-err{display:none;color:#b0291c;font-size:.86rem;font-weight:600;margin:6px 0 0}
#fiu-form .fiu-err.on{display:block}
#fiu-form .fiu-count{float:right;font-weight:500;color:#53647a;font-size:.82rem}
#fiu-form .fiu-actions{display:flex;flex-direction:column;gap:10px;margin-top:6px}
#fiu-form .fiu-submit{display:inline-flex;align-items:center;justify-content:center;width:100%;min-height:56px;border:2px solid #e8b931;border-radius:12px;background:#e8b931;color:#0f1c2e;font:inherit;font-size:1.06rem;font-weight:700;cursor:pointer;box-shadow:0 12px 28px -12px rgba(232,185,49,.75);transition:background-color .2s,border-color .2s}
#fiu-form .fiu-submit:hover{background:#f3c94e;border-color:#f3c94e}
#fiu-form button:focus-visible,#fiu-form .fiu-link:focus-visible{outline:3px solid #1d6fa5;outline-offset:3px}
#fiu-form .fiu-link{background:none;border:0;padding:4px 0;font:inherit;font-size:.92rem;font-weight:700;color:#1d6fa5;text-decoration:underline;text-underline-offset:3px;cursor:pointer;align-self:center}
#fiu-form .fiu-fine{margin:0;font-size:.84rem;color:#53647a;text-align:center}
#fiu-form .fiu-done{display:none}
#fiu-form.is-done .fiu-grid,#fiu-form.is-done .fiu-actions{display:none}
#fiu-form.is-done .fiu-done{display:block}
#fiu-form .fiu-check{display:flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:50%;background:#e7f6ec;color:#1f8a4c;font-size:28px;font-weight:800;margin:0 0 14px}
#fiu-form .fiu-done h4{font-family:"Archivo",system-ui,sans-serif;font-weight:800;font-size:1.5rem;line-height:1.15;margin:0 0 8px;color:#0f1c2e}
#fiu-form .fiu-done p{margin:0 0 14px;line-height:1.55;color:#53647a}
#fiu-form dl{margin:0 0 16px;border:1px solid #dbe3ec;border-radius:12px;overflow:hidden}
#fiu-form dl div{display:grid;grid-template-columns:110px minmax(0,1fr);gap:10px;padding:10px 14px;border-top:1px solid #dbe3ec}
#fiu-form dl div:first-child{border-top:0}
#fiu-form dt{font-weight:700;font-size:.88rem;color:#53647a;margin:0}
#fiu-form dd{margin:0;font-size:.95rem;overflow-wrap:anywhere;white-space:pre-line}
#fiu-form .fiu-badge{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;background:#e8b931;color:#0f1c2e;border-radius:6px;padding:4px 8px;margin:0 0 10px}
#fiu-form .fiu-again{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 18px;border:2px solid #0f1c2e;border-radius:12px;background:transparent;color:#0f1c2e;font:inherit;font-weight:700;cursor:pointer}
#fiu-form .fiu-again:hover{background:#0f1c2e;color:#f3f6f9}
@media (max-width:420px){#fiu-form .fiu-grid{grid-template-columns:minmax(0,1fr)}#fiu-form dl div{grid-template-columns:minmax(0,1fr);gap:2px}}
</style>
		<?php
	},
	50
);

add_action(
	'wp_footer',
	function () use ( $axiom_fiu_applies ) {
		static $done = false;
		if ( $done || ! $axiom_fiu_applies() ) {
			return;
		}
		$done = true;
		?>
<script id="fiu-demo-js">
(function () {
  var mount = document.getElementById('fiu-form');
  if (!mount) return;
  var TYPES = ['Vinyl privacy', 'Wood', 'Chain link', 'Gate', 'Not sure yet'];
  var KEYS = { 'q-vinyl': 'Vinyl privacy', 'q-wood': 'Wood', 'q-chain': 'Chain link', 'q-gates': 'Gate' };
  var MAX = 400;
  var opts = TYPES.map(function (t) { return '<option>' + t + '</option>'; }).join('');
  mount.innerHTML =
    '<div class="fiu-f" role="group" aria-label="Free estimate request (demo)">' +
    '<div class="fiu-grid">' +
      '<div class="fiu-full"><label for="fiu-n">Your name</label><input id="fiu-n" name="fiu_n" type="text" autocomplete="name" maxlength="80" aria-describedby="fiu-n-e"><p class="fiu-err" id="fiu-n-e">Please enter your name.</p></div>' +
      '<div><label for="fiu-p">Phone</label><input id="fiu-p" name="fiu_p" type="tel" inputmode="tel" autocomplete="tel-national" maxlength="20" placeholder="(407) 555-0123" aria-describedby="fiu-p-e"><p class="fiu-err" id="fiu-p-e">Enter a 10-digit phone number.</p></div>' +
      '<div><label for="fiu-z">ZIP code</label><input id="fiu-z" name="fiu_z" type="text" inputmode="numeric" autocomplete="postal-code" maxlength="5" placeholder="32801" aria-describedby="fiu-z-e"><p class="fiu-err" id="fiu-z-e">Enter a 5-digit ZIP code.</p></div>' +
      '<div class="fiu-full"><label for="fiu-t">Fence type</label><select id="fiu-t" name="fiu_t" aria-describedby="fiu-t-e"><option value="">Choose a fence type</option>' + opts + '</select><p class="fiu-err" id="fiu-t-e">Choose a fence type, or “Not sure yet”.</p></div>' +
      '<div class="fiu-full"><label for="fiu-d">About your project <span class="fiu-opt">(optional)</span><span class="fiu-count" id="fiu-c" aria-hidden="true">0/' + MAX + '</span></label><textarea id="fiu-d" name="fiu_d" maxlength="' + MAX + '" placeholder="About how many feet, gates needed, replacing an old fence…"></textarea></div>' +
    '</div>' +
    '<div class="fiu-actions">' +
      '<button type="button" class="fiu-submit" id="fiu-go">Send My Estimate Request</button>' +
      '<button type="button" class="fiu-link" id="fiu-sample">Fill in sample details</button>' +
      '<p class="fiu-fine">Demo mode: nothing is sent, texted or emailed.</p>' +
    '</div>' +
    '<div class="fiu-done" id="fiu-done" role="status" aria-live="polite" tabindex="-1"></div>' +
    '</div>';
  mount.classList.add('fiu-ready');

  var $ = function (id) { return document.getElementById(id); };
  var F = { n: $('fiu-n'), p: $('fiu-p'), z: $('fiu-z'), t: $('fiu-t'), d: $('fiu-d') };
  var digits = function (s) { return (s || '').replace(/\D/g, ''); };
  var phone10 = function (s) { var d = digits(s); if (d.length === 11 && d.charAt(0) === '1') d = d.slice(1); return d; };
  var fmt = function (d) { return d.length === 10 ? '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6) : d; };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var CHECK = {
    n: function () { return F.n.value.trim().length >= 2; },
    p: function () { return phone10(F.p.value).length === 10; },
    z: function () { return /^\d{5}$/.test(F.z.value.trim()); },
    t: function () { return F.t.value !== ''; }
  };
  var show = function (k, ok) { F[k].setAttribute('aria-invalid', ok ? 'false' : 'true'); $('fiu-' + k + '-e').classList.toggle('on', !ok); };
  var touched = {}, attempted = false;
  Object.keys(CHECK).forEach(function (k) {
    // errors appear after a submit attempt, or once something has been entered (never just for tabbing past)
    F[k].addEventListener('blur', function () { if (!attempted && F[k].value.trim() === '') return; touched[k] = true; show(k, CHECK[k]()); });
    F[k].addEventListener(k === 't' ? 'change' : 'input', function () { if (touched[k]) show(k, CHECK[k]()); });
  });
  F.p.addEventListener('blur', function () { var d = phone10(F.p.value); if (d.length === 10) F.p.value = fmt(d); });
  F.z.addEventListener('input', function () { var v = digits(F.z.value).slice(0, 5); if (v !== F.z.value) F.z.value = v; });
  F.d.addEventListener('input', function () { $('fiu-c').textContent = F.d.value.length + '/' + MAX; });

  var submit = function () {
    var bad = null; attempted = true;
    Object.keys(CHECK).forEach(function (k) { touched[k] = true; var ok = CHECK[k](); show(k, ok); if (!ok && !bad) bad = k; });
    if (bad) { F[bad].focus(); return; }
    var first = F.n.value.trim().split(/\s+/)[0];
    var rows = [['Name', F.n.value.trim()], ['Phone', fmt(phone10(F.p.value))], ['ZIP code', F.z.value.trim()], ['Fence type', F.t.value]];
    if (F.d.value.trim()) rows.push(['Project', F.d.value.trim()]);
    var done = $('fiu-done');
    done.innerHTML = '<span class="fiu-check" aria-hidden="true">✓</span><span class="fiu-badge">Demo preview</span>' +
      '<h4>Thanks, ' + esc(first) + '! Your estimate request is in.</h4>' +
      '<p>On the live site this would go straight to Fence It Up, and they’d follow up about your project. In this demo, nothing was sent.</p>' +
      '<dl>' + rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + esc(r[1]) + '</dd></div>'; }).join('') + '</dl>' +
      '<button type="button" class="fiu-again" id="fiu-again">Start a new request</button>';
    mount.classList.add('is-done');
    done.focus({ preventScroll: true });
    var r = mount.getBoundingClientRect();
    if (r.top < 70 || r.top > window.innerHeight * 0.6) mount.scrollIntoView({ block: 'start' });
    $('fiu-again').addEventListener('click', function () {
      Object.keys(F).forEach(function (k) { F[k].value = ''; F[k].removeAttribute('aria-invalid'); });
      Object.keys(CHECK).forEach(function (k) { $('fiu-' + k + '-e').classList.remove('on'); });
      touched = {}; attempted = false; $('fiu-c').textContent = '0/' + MAX;
      mount.classList.remove('is-done'); done.innerHTML = ''; F.n.focus();
    });
  };
  $('fiu-go').addEventListener('click', submit);
  mount.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); submit(); }
  });
  $('fiu-sample').addEventListener('click', function () {
    F.n.value = 'Sam Rivera'; F.p.value = '(407) 555-0142'; F.z.value = '32839';
    if (!F.t.value) F.t.value = 'Vinyl privacy';
    F.d.value = 'About 150 ft of 6 ft white vinyl privacy fence around the backyard, with one double gate for the side yard.';
    $('fiu-c').textContent = F.d.value.length + '/' + MAX;
    Object.keys(CHECK).forEach(function (k) { touched[k] = true; show(k, CHECK[k]()); });
    $('fiu-go').focus();
  });

  // estimate links: preselect the fence type from the Services card; focus the first field on desktop
  var fine = window.matchMedia && matchMedia('(pointer: fine)').matches;
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href="#estimate"]');
    if (!a) return;
    var host = a.closest('[id^="q-"]') || (a.id && a.id.indexOf('q-') === 0 ? a : null);
    var t = host && KEYS[host.id];
    if (t && !mount.classList.contains('is-done')) { F.t.value = t; if (touched.t) show('t', true); }
    if (fine && !mount.classList.contains('is-done')) setTimeout(function () { (F.n.value ? F.p : F.n).focus({ preventScroll: true }); }, 650);
  });

  // phone/tablet bar: step aside while the estimate section is on screen, or while the site chat is open
  // (the bar sits above the chat's greeting box so its button gets the tap; it must never cover the open chat)
  var bar = document.getElementById('fiu-bar'), est = document.getElementById('estimate');
  if (bar) {
    var atForm = false, chatOpen = false;
    var sync = function () { bar.classList.toggle('fiu-off', atForm || chatOpen); };
    if (est && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { atForm = en[0].isIntersecting; sync(); }, { threshold: 0.15 }).observe(est);
    }
    var watchChat = function (cw) {
      var read = function () { chatOpen = cw.getAttribute('data-active') === 'true'; sync(); };
      new MutationObserver(read).observe(cw, { attributes: true, attributeFilter: ['data-active'] }); read();
    };
    var cw = document.querySelector('chat-widget');
    if (cw) watchChat(cw);
    else new MutationObserver(function (m, o) { var c = document.querySelector('chat-widget'); if (c) { o.disconnect(); watchChat(c); } }).observe(document.body, { childList: true, subtree: true });
  }
})();
</script>
		<?php
	},
	60
);
