<?php
/**
 * Axiom Demo – Arroyos Page Enhancements
 * Page 1716 only (/arroyos-lawn-care-demo/ and its Elementor previews). Everything on the page is native
 * Elementor; this adds what Elementor's style editor cannot express:
 *  - heading accents: words wrapped in <em> get the Arroyo's lime underline (light sections) or lime text (dark);
 *  - before/after slider (#ba, #ba-before, #ba-handle): pointer drag, tap-to-jump, keyboard range, gentle intro nudge;
 *  - hero video (#hero): first-frame poster, honours prefers-reduced-motion;
 *  - responsive `sizes` for gallery images so phones fetch the smaller generated files;
 *  - readable credit links in the before/after caption (CC BY attribution for the grass texture).
 * Rollback: unpublish this snippet (the page still shows a 50/50 split and the video).
 */
namespace AngieSnippets\AxiomDemoArroyos;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// No named functions or constants: closures only, so the file can be re-validated while the live copy is loaded.
$axiom_arroyos_applies = static function () {
	if ( is_admin() || is_feed() || is_embed() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return false;
	}
	// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- read-only checks.
	if ( isset( $_GET['elementor_preview_token'] ) || isset( $_GET['elementor-preview'] ) ) {
		return true;
	}
	return is_page( 1716 );
};

add_action(
	'wp_head',
	function () use ( $axiom_arroyos_applies ) {
		if ( ! $axiom_arroyos_applies() ) {
			return;
		}
		?>
<style id="arl-demo-css">
[data-elementor-id="1716"] :is(h1,h2) em{font-style:normal;color:inherit;background-image:linear-gradient(#8edc1e,#8edc1e);background-repeat:no-repeat;background-size:100% .16em;background-position:0 92%;padding-bottom:.02em}
#hero :is(h1,h2) em,#results :is(h1,h2) em,#estimate :is(h1,h2) em{color:#8edc1e;background-image:none}
#hero .e-background-video__media{object-fit:cover;object-position:50% 50%}
#ba{touch-action:pan-y;cursor:ew-resize;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}
#ba img{pointer-events:none;-webkit-user-drag:none}
#results p a{color:#c3cbbb;text-decoration:underline;text-underline-offset:2px}#results p a:hover{color:#8edc1e}
#ba-before{will-change:clip-path}
#ba-handle{pointer-events:none;will-change:left}
#ba .arl-ba-range{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none;inset:auto}
#ba:focus-within #ba-handle>*{outline:3px solid #8edc1e;outline-offset:3px}
#ba.arl-dragging #ba-handle>*{transform:translate(-50%,-50%) scale(1.08)}
</style>
		<?php
	},
	50
);

add_action(
	'wp_footer',
	function () use ( $axiom_arroyos_applies ) {
		static $done = false;
		if ( $done || ! $axiom_arroyos_applies() ) {
			return;
		}
		$done = true;
		?>
<script id="arl-demo-js">
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  // hero: poster while the drone footage loads
  var v = document.querySelector('#hero video');
  if (v) { v.setAttribute('poster', <?php echo wp_json_encode( 'https://axiomsystems.systems/wp-content/uploads/2026/11/arroyos-demo-hero-poster.jpg' ); ?>); if (reduce) { v.removeAttribute('autoplay'); try { v.pause(); } catch (e) {} } }
  // gallery: let phones pick the smaller generated sizes
  document.querySelectorAll('#work img').forEach(function (i) { i.sizes = '(min-width: 1025px) 360px, (min-width: 768px) 46vw, 92vw'; });
  document.querySelectorAll('#ba img').forEach(function (i) { i.sizes = '(min-width: 1200px) 1120px, 100vw'; });

  var root = document.getElementById('ba'), before = document.getElementById('ba-before'), handle = document.getElementById('ba-handle');
  if (!root || !before || !handle) return;
  var pos = 50, raf = 0, touched = false;
  var range = document.createElement('input');
  range.type = 'range'; range.min = '0'; range.max = '100'; range.step = '1'; range.value = '50';
  range.className = 'arl-ba-range'; range.setAttribute('aria-label', 'Compare before and after: use the arrow keys to move the divider');
  root.appendChild(range);
  function paint() {
    raf = 0;
    before.style.clipPath = 'inset(0 ' + (100 - pos) + '% 0 0)';
    handle.style.left = pos + '%';
    range.value = String(Math.round(pos));
    range.setAttribute('aria-valuetext', Math.round(pos) + '% before, ' + Math.round(100 - pos) + '% after');
  }
  function set(p) { pos = Math.max(0, Math.min(100, p)); if (!raf) raf = requestAnimationFrame(paint); }
  function fromX(x) { var r = root.getBoundingClientRect(); return (x - r.left) / r.width * 100; }
  range.addEventListener('input', function () { touched = true; set(+range.value); });

  var id = null, sx = 0, sy = 0, moved = false;
  root.addEventListener('pointerdown', function (e) {
    if (e.button > 0) return;
    touched = true; id = e.pointerId; sx = e.clientX; sy = e.clientY; moved = false;
    if (e.pointerType === 'mouse') { root.setPointerCapture(id); root.classList.add('arl-dragging'); set(fromX(e.clientX)); moved = true; e.preventDefault(); }
  });
  root.addEventListener('pointermove', function (e) {
    if (e.pointerId !== id) return;
    if (!moved) {
      // touch: start dragging once the finger clearly moves sideways; vertical swipes stay page scrolls (touch-action: pan-y)
      if (Math.abs(e.clientX - sx) < 4) return;
      moved = true; try { root.setPointerCapture(id); } catch (err) {} root.classList.add('arl-dragging');
    }
    set(fromX(e.clientX));
  });
  function end(e) {
    if (e.pointerId !== id) return;
    if (!moved && e.type === 'pointerup' && Math.abs(e.clientY - sy) < 8) set(fromX(e.clientX)); // tap to jump
    id = null; root.classList.remove('arl-dragging');
  }
  root.addEventListener('pointerup', end); root.addEventListener('pointercancel', end);
  root.addEventListener('lostpointercapture', function () { root.classList.remove('arl-dragging'); });
  paint();

  // one gentle nudge the first time the slider scrolls into view, so it reads as interactive
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; io.disconnect();
      var keys = [[0, 50], [450, 30], [1050, 68], [1500, 50]], t0 = null;
      function ease(t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
      function step(ts) {
        if (touched) return; if (t0 === null) t0 = ts; var t = ts - t0;
        for (var i = 1; i < keys.length; i++) if (t <= keys[i][0]) {
          var a = keys[i - 1], b = keys[i], k = ease((t - a[0]) / (b[0] - a[0])); set(a[1] + (b[1] - a[1]) * k); return requestAnimationFrame(step);
        }
        set(50);
      }
      setTimeout(function () { requestAnimationFrame(step); }, 350);
    }, { threshold: 0.6 });
    io.observe(root);
  }
})();
</script>
		<?php
	},
	60
);
