<?php
/**
 * Axiom Demo – Comer's Landscaping Page Enhancements
 * DRAFT page 1996 only: its WordPress preview (?page_id=1996&preview=true), Elementor previews of 1996, and the
 * signed Elementor preview links for post 1996. It outputs nothing on any other page, so publishing this snippet
 * changes nothing a visitor can see until page 1996 itself is published.
 * The page is native Elementor V4; this adds:
 *  - the demo quote form in #cmz-form: name, phone, optional email, service, optional city/ZIP, details. DEMO MODE: it
 *    runs entirely in the browser. There is no <form> element, no submit event, no field names and no request of any
 *    kind, so nothing reaches the CRM, email or SMS (Axiom CRM Sync / Form Protection only handle Jetpack form 1096).
 *  - quote links: smooth scroll to the form card; each Services card's link preselects its service;
 *  - Our Work: filter chips, "Show all" (8 photos shown first), and a lightbox with arrows, swipe, Esc and focus return;
 *  - the hero's one-time crossfade from hydroseed day to grown in (skipped with reduced motion);
 *  - heading accents, the header colour (the site's Additional CSS repaints every <header>), and the phone bar, which
 *    stays hidden over the hero and while the quote form or the site chat is open.
 * Rollback: unpublish this snippet. Without it the page still shows every section and all 31 photos, and the form card
 * reads "The quote form is loading. You can also call 803.422.8031."
 */
namespace AngieSnippets\AxiomDemoComersLandscaping;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Closures only (no named functions/constants), so the file can be re-validated while the live copy is loaded.
$axiom_cmz_applies = static function () {
	$pid = 1996;
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
	function () use ( $axiom_cmz_applies ) {
		if ( ! $axiom_cmz_applies() ) {
			return;
		}
		?>
<style id="cmz-demo-css">
@media (prefers-reduced-motion: no-preference){html{scroll-behavior:smooth}}
#top{background-color:rgba(6,10,7,.94)!important}
/* the site sets overflow-x:hidden on html/body, which turns body into a scroll container and breaks the sticky header */
html:not(#cmz-x),body:not(#cmz-x){overflow-x:clip!important;overflow-y:visible!important} /* :not(#id) out-ranks the later 'html, body' rule in Additional CSS */
#hero h1 em,#results h2 em,#equipment h2 em{font-style:normal;color:#c4d82e}
#about h2 em,#services h2 em,#process h2 em,#gallery h2 em,#quote h2 em{font-style:normal;color:#4f9a25}
#process h2 em{color:#4f9a25}
/* hero: hydroseed day -> grown in, once */
@keyframes cmzIn{from{opacity:0}to{opacity:1}}
@keyframes cmzOut{from{opacity:1}to{opacity:0}}
@media (prefers-reduced-motion: no-preference){
  #hero-after{animation:cmzIn 2.6s ease-in-out 1.4s both}
  #hero-chip-a{display:inline-flex!important;animation:cmzOut .5s ease 2.6s both}
  #hero-chip-b{animation:cmzIn .5s ease 2.9s both}
}
/* gallery */
#cmz-gal [id^="g-"]{cursor:zoom-in}
#cmz-gal [id^="g-"]:hover img{transform:scale(1.04)}
#cmz-gal [id^="g-"]:focus-visible{outline:3px solid #c4d82e;outline-offset:3px}
#cmz-gal .cmz-off{display:none!important}
#cmz-chips{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
#cmz-chips button{min-height:44px;padding:0 16px;border-radius:999px;border:1.5px solid rgba(16,22,15,.28);background:transparent;color:#10160f;font:800 12.5px/1 "Figtree",system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;flex:none;transition:background-color .2s,color .2s,border-color .2s}
#cmz-chips button:hover{border-color:#10160f}
#cmz-chips button[aria-pressed="true"]{background:#060a07;border-color:#060a07;color:#fff}
#cmz-chips button:focus-visible{outline:3px solid #4f9a25;outline-offset:2px}
#cmz-chips .cmz-count{font:700 12px/1 "Figtree",system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#59635a;margin-inline-start:6px}
@media (max-width:767px){
  #cmz-chips{flex-wrap:nowrap;overflow-x:auto;margin-inline:-16px;padding:0 16px 6px;scrollbar-width:none;-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}
  #cmz-chips::-webkit-scrollbar{display:none}
  #cmz-chips .cmz-count{display:none}
}
.cmz-more{display:flex;justify-content:center;margin-top:22px}
.cmz-more button{min-height:52px;padding:0 28px;border-radius:999px;border:2px solid #060a07;background:#060a07;color:#fff;font:800 14px/1 "Figtree",system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;cursor:pointer}
.cmz-more button:hover{background:#1b271c;border-color:#1b271c}
.cmz-more button:focus-visible{outline:3px solid #4f9a25;outline-offset:3px}
@media (max-width:767px){.cmz-more button{width:100%}}
.cmz-lb{position:fixed;inset:0;z-index:2147483000;background:rgba(3,6,4,.95);display:none;align-items:center;justify-content:center;padding:clamp(12px,3vw,40px)}
.cmz-lb.is-open{display:flex}
.cmz-lb figure{margin:0;display:grid;gap:12px;justify-items:center;max-width:min(1100px,100%)}
.cmz-lb img{max-width:100%;max-height:calc(100vh - 150px);max-height:calc(100svh - 150px);width:auto;height:auto;border-radius:12px;box-shadow:0 30px 90px rgba(0,0,0,.6)}
.cmz-lb figcaption{font:700 15px/1.3 "Figtree",system-ui,sans-serif;color:#fff;text-align:center}
.cmz-lb figcaption small{display:block;margin-top:4px;font-weight:600;color:rgba(255,255,255,.65)}
.cmz-lb button{position:absolute;width:50px;height:50px;border-radius:50%;border:1px solid rgba(255,255,255,.35);background:rgba(0,0,0,.55);color:#fff;font:400 22px/1 system-ui,sans-serif;cursor:pointer;display:grid;place-items:center;padding:0}
.cmz-lb button:hover{background:#c4d82e;color:#0a1005;border-color:#c4d82e}
.cmz-lb button:focus-visible{outline:3px solid #c4d82e;outline-offset:3px}
.cmz-lb .cmz-x{top:14px;right:14px}.cmz-lb .cmz-p{left:14px;top:50%;margin-top:-25px}.cmz-lb .cmz-n{right:14px;top:50%;margin-top:-25px}
@media (max-width:767px){.cmz-lb .cmz-p,.cmz-lb .cmz-n{top:auto;bottom:18px;margin-top:0}.cmz-lb img{max-height:calc(100svh - 190px)}}
/* phone bar */
#cmz-bar{transition:transform .25s ease,opacity .25s ease}
#cmz-bar.cmz-hide{transform:translateY(110%);opacity:0;pointer-events:none}
#quote-form,#cmz-form{overflow-wrap:anywhere}
/* demo quote form */
#cmz-form{font-family:"Figtree",system-ui,sans-serif;color:#10160f}
#cmz-form .cmz-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px 12px}
#cmz-form .cmz-full{grid-column:1/-1}
@media (max-width:767px){#cmz-form .cmz-grid{grid-template-columns:minmax(0,1fr)}}
#cmz-form label{display:block;font-weight:800;font-size:.76rem;letter-spacing:.12em;text-transform:uppercase;margin:0 0 7px;color:#10160f}
#cmz-form label .cmz-opt{font-weight:600;letter-spacing:.04em;text-transform:none;color:#59635a}
#cmz-form input,#cmz-form select,#cmz-form textarea{display:block;width:100%;box-sizing:border-box;font:inherit;font-size:16px;line-height:1.35;color:#10160f;background:#f7f8f2;border:1.5px solid #cfd6c0;border-radius:12px;padding:13px 14px;min-height:52px;margin:0;box-shadow:none;transition:border-color .15s,box-shadow .15s}
#cmz-form select{appearance:none;-webkit-appearance:none;padding-right:42px;background-image:linear-gradient(45deg,transparent 50%,#10160f 50%),linear-gradient(135deg,#10160f 50%,transparent 50%);background-position:calc(100% - 22px) 52%,calc(100% - 16px) 52%;background-size:6px 6px;background-repeat:no-repeat}
#cmz-form textarea{min-height:110px;resize:vertical}
#cmz-form input:focus,#cmz-form select:focus,#cmz-form textarea:focus{outline:none;border-color:#4f9a25;background:#fff;box-shadow:0 0 0 3px rgba(114,190,69,.35)}
#cmz-form [aria-invalid="true"]{border-color:#c0392b}
#cmz-form .cmz-err{display:none;color:#b0291c;font-size:.86rem;font-weight:600;margin:6px 0 0}
#cmz-form .cmz-err.on{display:block}
#cmz-form .cmz-count{float:right;font-weight:600;letter-spacing:0;text-transform:none;color:#59635a;font-size:.8rem}
#cmz-form .cmz-actions{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;margin-top:18px}
#cmz-form .cmz-go{display:inline-flex;align-items:center;justify-content:center;min-height:56px;padding:0 30px;border:2px solid #c4d82e;border-radius:999px;background:#c4d82e;color:#0a1005;font:800 15px/1 "Figtree",system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;transition:background-color .2s}
#cmz-form .cmz-go:hover{background:#d6ea3c;border-color:#d6ea3c}
#cmz-form .cmz-link{background:none;border:0;padding:6px 0;font:inherit;font-weight:700;font-size:.95rem;color:#3f7d1c;text-decoration:underline;cursor:pointer}
#cmz-form .cmz-fine{flex-basis:100%;margin:0;font-size:.86rem;color:#59635a}
#cmz-form button:focus-visible{outline:3px solid #4f9a25;outline-offset:3px}
@media (max-width:767px){#cmz-form .cmz-go{width:100%}}
#cmz-form.is-done .cmz-f{display:none}
#cmz-form .cmz-done{display:none}
#cmz-form.is-done .cmz-done{display:block}
#cmz-form .cmz-done:focus{outline:none}
#cmz-form .cmz-tick{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;background:#c4d82e;color:#0a1005;font-size:24px;font-weight:800;margin-bottom:14px}
#cmz-form .cmz-badge{display:inline-block;font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;background:#ff9f2e;color:#1a1000;border-radius:6px;padding:4px 8px;margin-bottom:10px}
#cmz-form .cmz-done h4{font-family:"Anton",Impact,sans-serif;font-weight:400;text-transform:uppercase;font-size:1.9rem;line-height:1;margin:0 0 10px;color:#10160f}
#cmz-form .cmz-done p{margin:0 0 14px;color:#59635a;line-height:1.55}
#cmz-form dl{margin:0 0 16px;border-top:1px solid #d9dfcc}
#cmz-form dl div{display:grid;grid-template-columns:110px minmax(0,1fr);gap:10px;padding:10px 0;border-bottom:1px solid #d9dfcc}
#cmz-form dt{font-weight:800;font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:#59635a}
#cmz-form dd{margin:0;font-weight:600}
/* the Hello Elementor theme paints every button:hover/:focus pink (#c36); keep this page's own colours */
#cmz-chips button:hover,#cmz-chips button:focus{background:transparent;color:#10160f}
#cmz-chips button[aria-pressed="true"]:hover,#cmz-chips button[aria-pressed="true"]:focus,#cmz-chips button[aria-pressed="true"]{background:#060a07;color:#fff}
.cmz-more button:focus{background:#060a07;color:#fff}
.cmz-more button:hover{background:#1b271c;color:#fff}
.cmz-lb button:focus{background:rgba(0,0,0,.55);color:#fff}
.cmz-lb button:hover{background:#c4d82e;color:#0a1005}
#cmz-form .cmz-link:hover,#cmz-form .cmz-link:focus{background:none;color:#3f7d1c}
#cmz-form .cmz-go:focus{background:#c4d82e;color:#0a1005}
#cmz-form .cmz-go:hover{background:#d6ea3c;color:#0a1005}
</style>
		<?php
	},
	60
);

add_action(
	'wp_footer',
	function () use ( $axiom_cmz_applies ) {
		static $done = false;
		if ( $done || ! $axiom_cmz_applies() ) {
			return;
		}
		$done = true;
		?>
<script id="cmz-demo-js">
(function () {
  var d = document, $ = function (s, r) { return (r || d).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || d).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  /* ---------- gallery: chips, "Show all", lightbox ---------- */
  var gal = $('#cmz-gal'), chipsBox = $('#cmz-chips');
  if (gal && chipsBox) {
    var tiles = $$('[id^="g-"]', gal), LIMIT = 8, expanded = false, filter = 'all', vis = [];
    var CATS = [['all', 'All'], ['drain', 'Drainage & erosion'], ['site', 'Site work'], ['hard', 'Hardscape & rock'], ['lawn', 'Lawns & grounds'], ['irr', 'Irrigation & sod'], ['equip', 'Equipment']];
    var catOf = function (t) { return t.id.split('-')[1]; };
    chipsBox.setAttribute('role', 'group'); chipsBox.setAttribute('aria-label', 'Filter photos');
    chipsBox.innerHTML = CATS.map(function (c) { return '<button type="button" data-f="' + c[0] + '" aria-pressed="' + (c[0] === 'all') + '">' + esc(c[1]) + '</button>'; }).join('') + '<span class="cmz-count" aria-live="polite"></span>';
    var more = d.createElement('div'); more.className = 'cmz-more'; more.innerHTML = '<button type="button" aria-expanded="false"></button>';
    gal.parentNode.insertBefore(more, gal.nextSibling);
    var moreBtn = $('button', more), count = $('.cmz-count', chipsBox);
    tiles.forEach(function (t) {
      var cap = $('p, span', t); t.setAttribute('role', 'button'); t.setAttribute('tabindex', '0');
      t.setAttribute('aria-label', 'Open photo: ' + (cap ? cap.textContent.trim() : 'job photo'));
    });
    var apply = function () {
      var match = tiles.filter(function (t) { return filter === 'all' || catOf(t) === filter; });
      vis = match;
      tiles.forEach(function (t) {
        var i = match.indexOf(t), show = i > -1 && (expanded || filter !== 'all' || i < LIMIT);
        t.classList.toggle('cmz-off', !show);
      });
      $$('button', chipsBox).forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-f') === filter)); });
      count.textContent = match.length + ' photo' + (match.length === 1 ? '' : 's');
      var collapsed = filter === 'all' && !expanded && match.length > LIMIT;
      more.style.display = filter === 'all' && match.length > LIMIT ? '' : 'none';
      moreBtn.textContent = collapsed ? 'Show all ' + match.length + ' photos' : 'Show fewer photos';
      moreBtn.setAttribute('aria-expanded', String(!collapsed));
    };
    chipsBox.addEventListener('click', function (e) { var b = e.target.closest('button[data-f]'); if (!b) return; filter = b.getAttribute('data-f'); apply(); });
    moreBtn.addEventListener('click', function () {
      expanded = !expanded; apply();
      if (expanded) { var t = vis[LIMIT]; if (t) t.focus({ preventScroll: true }); }
      else { var r = $('#gallery').getBoundingClientRect(); if (r.top < 0) chipsBox.scrollIntoView({ block: 'start' }); }
    });
    apply();

    var lb = d.createElement('div'); lb.className = 'cmz-lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Photo viewer');
    lb.innerHTML = '<button type="button" class="cmz-x" aria-label="Close">✕</button><button type="button" class="cmz-p" aria-label="Previous photo">←</button><figure><img alt=""><figcaption></figcaption></figure><button type="button" class="cmz-n" aria-label="Next photo">→</button>';
    d.body.appendChild(lb);
    var lbi = $('img', lb), lbc = $('figcaption', lb), cur = 0, opener = null;
    var big = function (img) {
      var best = img.currentSrc || img.src, bw = 0;
      (img.getAttribute('srcset') || '').split(',').forEach(function (c) { var p = c.trim().split(/\s+/), w = parseInt(p[1], 10) || 0; if (w > bw) { bw = w; best = p[0]; } });
      return best;
    };
    var show = function (i) {
      cur = (i + vis.length) % vis.length; var t = vis[cur], im = $('img', t), cap = $('p, span', t);
      lbi.src = big(im); lbi.alt = im.alt || ''; lbc.textContent = cap ? cap.textContent.trim() : '';
      var s = d.createElement('small'); s.textContent = (cur + 1) + ' of ' + vis.length; lbc.appendChild(s);
    };
    var openLb = function (t) { opener = t; lb.classList.add('is-open'); d.documentElement.style.overflow = 'hidden'; show(vis.indexOf(t)); $('.cmz-x', lb).focus(); };
    var closeLb = function () { lb.classList.remove('is-open'); d.documentElement.style.overflow = ''; if (opener) opener.focus({ preventScroll: true }); };
    tiles.forEach(function (t) {
      t.addEventListener('click', function (e) { e.preventDefault(); openLb(t); });
      t.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLb(t); } });
    });
    $('.cmz-x', lb).addEventListener('click', closeLb);
    $('.cmz-p', lb).addEventListener('click', function () { show(cur - 1); });
    $('.cmz-n', lb).addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    d.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') closeLb(); else if (e.key === 'ArrowLeft') show(cur - 1); else if (e.key === 'ArrowRight') show(cur + 1);
      else if (e.key === 'Tab') { var b = $$('button', lb), f = b[0], l = b[b.length - 1]; if (e.shiftKey && d.activeElement === f) { e.preventDefault(); l.focus(); } else if (!e.shiftKey && d.activeElement === l) { e.preventDefault(); f.focus(); } }
    });
    var tx = null;
    lb.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; tx = null; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); }, { passive: true });
  }

  /* ---------- demo quote form ---------- */
  var mount = $('#cmz-form');
  var SERVICES = ['Commercial Grounds Maintenance', 'Residential Lawn Care', 'Installation of Decorative Rock', 'Hardscaping', 'Irrigation Installation & Repair', 'Landscape Design & Lighting', 'Erosion Control', 'Not sure yet'];
  var MAX = 500;
  if (mount) {
    mount.innerHTML =
      '<div class="cmz-f" role="group" aria-label="Quote request (demo)">' +
      '<div class="cmz-grid">' +
        '<div><label for="cmz-n">Name</label><input id="cmz-n" type="text" autocomplete="off" maxlength="80" aria-describedby="cmz-n-e"><p class="cmz-err" id="cmz-n-e">Please enter your name.</p></div>' +
        '<div><label for="cmz-p">Phone</label><input id="cmz-p" type="tel" inputmode="tel" autocomplete="off" maxlength="20" placeholder="(803) 555-0100" aria-describedby="cmz-p-e"><p class="cmz-err" id="cmz-p-e">Enter a 10-digit phone number.</p></div>' +
        '<div class="cmz-full"><label for="cmz-m">Email <span class="cmz-opt">(optional)</span></label><input id="cmz-m" type="email" inputmode="email" autocomplete="off" maxlength="120" aria-describedby="cmz-m-e"><p class="cmz-err" id="cmz-m-e">That email address doesn’t look right.</p></div>' +
        '<div class="cmz-full"><label for="cmz-s">Service</label><select id="cmz-s" aria-describedby="cmz-s-e"><option value="">Choose a service</option>' + SERVICES.map(function (s) { return '<option>' + esc(s) + '</option>'; }).join('') + '</select><p class="cmz-err" id="cmz-s-e">Choose a service, or “Not sure yet”.</p></div>' +
        '<div class="cmz-full"><label for="cmz-z">Property location <span class="cmz-opt">(city or ZIP, optional)</span></label><input id="cmz-z" type="text" autocomplete="off" maxlength="60" placeholder="Columbia, Cayce, Lexington…"></div>' +
        '<div class="cmz-full"><label for="cmz-d">About the job <span class="cmz-opt">(optional)</span><span class="cmz-count" id="cmz-c" aria-hidden="true">0/' + MAX + '</span></label><textarea id="cmz-d" maxlength="' + MAX + '" placeholder="What you have in mind, rough size of the area, any timing."></textarea></div>' +
      '</div>' +
      '<div class="cmz-actions">' +
        '<button type="button" class="cmz-go" id="cmz-go">Send quote request</button>' +
        '<button type="button" class="cmz-link" id="cmz-sample">Fill in sample details</button>' +
        '<p class="cmz-fine">Demo mode: nothing is sent, texted or emailed.</p>' +
      '</div></div>' +
      '<div class="cmz-done" id="cmz-done" role="status" aria-live="polite" tabindex="-1"></div>';
    var F = { n: $('#cmz-n'), p: $('#cmz-p'), m: $('#cmz-m'), s: $('#cmz-s'), z: $('#cmz-z'), d: $('#cmz-d') };
    var phone10 = function (s) { var x = (s || '').replace(/\D/g, ''); if (x.length === 11 && x.charAt(0) === '1') x = x.slice(1); return x; };
    var fmt = function (x) { return x.length === 10 ? '(' + x.slice(0, 3) + ') ' + x.slice(3, 6) + '-' + x.slice(6) : x; };
    var CHECK = {
      n: function () { return F.n.value.trim().length >= 2; },
      p: function () { return phone10(F.p.value).length === 10; },
      m: function () { var v = F.m.value.trim(); return !v || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); },
      s: function () { return F.s.value !== ''; }
    };
    var mark = function (k, ok) { F[k].setAttribute('aria-invalid', ok ? 'false' : 'true'); $('#cmz-' + k + '-e').classList.toggle('on', !ok); };
    var touched = {}, attempted = false;
    Object.keys(CHECK).forEach(function (k) {
      // errors show after a submit attempt or once something was typed, never just for tabbing past
      F[k].addEventListener('blur', function () { if (!attempted && F[k].value.trim() === '') return; touched[k] = true; mark(k, CHECK[k]()); });
      F[k].addEventListener(k === 's' ? 'change' : 'input', function () { if (touched[k]) mark(k, CHECK[k]()); });
    });
    F.p.addEventListener('blur', function () { var x = phone10(F.p.value); if (x.length === 10) F.p.value = fmt(x); });
    F.d.addEventListener('input', function () { $('#cmz-c').textContent = F.d.value.length + '/' + MAX; });
    var submit = function () {
      var bad = null; attempted = true;
      Object.keys(CHECK).forEach(function (k) { touched[k] = true; var ok = CHECK[k](); mark(k, ok); if (!ok && !bad) bad = k; });
      if (bad) { F[bad].focus(); return; }
      var first = F.n.value.trim().split(/\s+/)[0];
      var rows = [['Name', F.n.value.trim()], ['Phone', fmt(phone10(F.p.value))]];
      if (F.m.value.trim()) rows.push(['Email', F.m.value.trim()]);
      rows.push(['Service', F.s.value]);
      if (F.z.value.trim()) rows.push(['Location', F.z.value.trim()]);
      if (F.d.value.trim()) rows.push(['Details', F.d.value.trim()]);
      var done = $('#cmz-done');
      done.innerHTML = '<div class="cmz-tick" aria-hidden="true">✓</div><span class="cmz-badge">Demo preview</span>' +
        '<h4>Thanks, ' + esc(first) + '! We’ll be in touch soon.</h4>' +
        '<p>On the live site this request would go straight to Comer’s phone and inbox. In this demo, nothing was sent.</p>' +
        '<dl>' + rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + esc(r[1]) + '</dd></div>'; }).join('') + '</dl>' +
        '<button type="button" class="cmz-link" id="cmz-again">Start a new request</button>';
      mount.classList.add('is-done');
      done.focus({ preventScroll: true });
      var card = $('#quote-form') || mount, r = card.getBoundingClientRect();
      if (r.top < 90 || r.top > innerHeight * 0.5) card.scrollIntoView({ block: 'start' });  // 90: below the sticky header
      $('#cmz-again').addEventListener('click', function () {
        Object.keys(F).forEach(function (k) { F[k].value = ''; F[k].removeAttribute('aria-invalid'); });
        Object.keys(CHECK).forEach(function (k) { $('#cmz-' + k + '-e').classList.remove('on'); });
        touched = {}; attempted = false; $('#cmz-c').textContent = '0/' + MAX;
        mount.classList.remove('is-done'); done.innerHTML = ''; F.n.focus();
      });
    };
    $('#cmz-go').addEventListener('click', submit);
    mount.addEventListener('keydown', function (e) { if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); submit(); } });
    $('#cmz-sample').addEventListener('click', function () {
      F.n.value = 'Sam Carter'; F.p.value = '(803) 555-0142'; F.m.value = 'sam@example.com'; F.z.value = 'Cayce';
      if (!F.s.value) F.s.value = 'Hardscaping';
      F.d.value = 'Backyard paver patio, about 16 by 20 feet, with a fire pit. Hoping to start this spring.';
      $('#cmz-c').textContent = F.d.value.length + '/' + MAX;
      Object.keys(CHECK).forEach(function (k) { touched[k] = true; mark(k, CHECK[k]()); });
      $('#cmz-go').focus();
    });

    // quote links: Services cards (#q-1..7) preselect their service; desktop focuses the first empty field
    var fine = window.matchMedia && matchMedia('(pointer: fine)').matches;
    d.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href="#quote-form"]');
      if (!a) return;
      var host = a.id && /^q-\d$/.test(a.id) ? a : a.closest('[id^="q-"]');
      var n = host ? parseInt(host.id.slice(2), 10) : 0;
      if (n && SERVICES[n - 1] && !mount.classList.contains('is-done')) { F.s.value = SERVICES[n - 1]; if (touched.s) mark('s', true); }
      if (fine && !mount.classList.contains('is-done')) setTimeout(function () { (F.n.value ? (F.p.value ? F.s : F.p) : F.n).focus({ preventScroll: true }); }, 700);
    });
  }

  /* ---------- mobile menu (native <details>): close it when one of its links is tapped ---------- */
  $$('#top details').forEach(function (det) {
    det.addEventListener('click', function (e) { if (e.target.closest('a') && det.open) det.open = false; });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && det.open) { det.open = false; var s = $('summary', det); if (s) s.focus(); } });
  });

  /* ---------- phone bar: hidden over the hero, at the quote form, and while the site chat is open ---------- */
  var bar = $('#cmz-bar'), hero = $('#hero'), qf = $('#quote-form');
  if (bar && 'IntersectionObserver' in window) {
    var atHero = true, atForm = false, chatOpen = false;
    var sync = function () { bar.classList.toggle('cmz-hide', atHero || atForm || chatOpen); };
    sync();
    if (hero) new IntersectionObserver(function (en) { atHero = en[0].isIntersecting; sync(); }, { threshold: 0, rootMargin: '0px 0px -40% 0px' }).observe(hero);
    if (qf) new IntersectionObserver(function (en) { atForm = en[0].isIntersecting; sync(); }, { threshold: 0.1 }).observe(qf);
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
