"""Builds main.php for the live snippet "Axiom Demo – Arroyos Lead Walkthrough" from the V3 demo's lead view
(../2026-11-10-arroyos-v3/parts). Page 1716 only; nothing renders unless the URL ends in #lead-demo."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.join(HERE, "..", "2026-11-10-arroyos-v3", "parts")
rd = lambda *p: open(os.path.join(*p), encoding="utf8").read()
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a, s.count(a)); return s.replace(a, b)

css = rd(V3, "v3.css"); css = css[css.index("/* ---------- lead view ---------- */"):]
css = rep(css, "min-height:calc(100vh - var(--pb))", "min-height:calc(100% - var(--pb))")
css = rd(HERE, "base.css") + css

html = rd(V3, "lead.html")
html = rep(html, '<form class="ph__pane" id="ph-form" novalidate hidden>', '<div class="ph__pane" id="ph-form" role="group" aria-label="Sample estimate request" hidden>')
html = rep(html, "</form>", "</div>")
html = rep(html, '<button class="btn btn--lime" type="submit">Send Sample Request</button>', '<button class="btn btn--lime" type="button" id="ph-send">Send Sample Request</button>')
html, n = re.subn(r' name="[a-z]+"', "", html); assert n == 6, n
html = html.replace(" required>", ">")
html = rep(html, "Axiom Systems · simulated · sample data", "Simulation · Axiom Systems · sample data only")
html = rep(html, '<p class="ph__hint">Sample lead. Nothing is sent, stored, or tracked.</p>', '<p class="ph__hint">Simulation. This is not the website’s estimate form: nothing is sent, stored, or tracked.</p>')
assert "<form" not in html and "href=" not in html and "name=" not in html

js = rd(V3, "v3.js")
js = js[js.index("  var S, els={"):js.index("  reset(); setMode();")]
js = rep(js, "defaults[i.name]", "defaults[i.id]", 3)
js = rep(js, "els.form.elements.first.focus({preventScroll:true});", "$('#l-first').focus({preventScroll:true});")
js = rep(js, "var f=els.form.elements, digits=", "var f={first:$('#l-first'),last:$('#l-last'),phone:$('#l-phone'),email:$('#l-email'),service:$('#l-svc'),sms:$('#l-sms')}, digits=")
js = rep(js, "els.form.addEventListener('submit', function(e){ e.preventDefault(); submit(); });",
         "$('#ph-send').addEventListener('click', submit); els.form.addEventListener('keydown', function(e){ if(e.key==='Enter' && e.target.tagName==='INPUT' && e.target.type!=='checkbox'){ e.preventDefault(); submit(); } });")
js = rep(js, "$('.crm').scrollIntoView({block:'start'})", "$('.crm').scrollIntoView({block:'start'})")
for bad in ("fetch(", "XMLHttpRequest", "sendBeacon", "dataLayer", "gtag", "fbq", "localStorage", "document.cookie", "els.form.elements"):
    assert bad not in js, bad
loader = rep(rd(HERE, "loader.js"), "/*__LEAD_JS__*/", js)

tpl = ('<template id="axl-lead-tpl"><style>' + css + '</style><div class="ov" role="dialog" aria-label="Lead walkthrough, simulation">'
       '<div class="bar"><b>Simulation</b><span>Sample data only. Nothing here sends messages, submits the website form, or creates CRM records.</span>'
       '<button type="button" id="axl-close">Back to website</button></div>' + html + '</div></template>')
assert "<?" not in tpl + loader and "?>" not in tpl + loader and "</script" not in loader and "</template>" not in html

php = '''<?php
/**
 * Axiom Demo – Arroyos Lead Walkthrough
 * Page 1716 only (/arroyos-lawn-care-demo/). Adds the "See What Happens to a Lead" sales walkthrough, opened by adding
 * #lead-demo to the page URL. On a normal visit nothing is rendered: the markup sits in an inert <template> and is only
 * mounted (in a shadow root, so its styles stay inside it) when the hash is present.
 * Simulation only: sample data, no form element, no links, no network requests, no tracking or conversion calls.
 * Rollback: unpublish this snippet. It does not touch the page content, the Elementor document or snippet 1733.
 */
namespace AngieSnippets\\AxiomDemoArroyosLead;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Closures only (no named functions), so the file can be re-validated while the live copy is loaded.
$axiom_arroyos_lead_applies = static function () {
	if ( is_admin() || is_feed() || is_embed() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return false;
	}
	// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- read-only checks.
	if ( isset( $_GET['elementor-preview'] ) || isset( $_GET['elementor_preview_token'] ) ) {
		return false;
	}
	return is_page( 1716 );
};

add_action(
	'wp_head',
	function () use ( $axiom_arroyos_lead_applies ) {
		if ( ! $axiom_arroyos_lead_applies() ) {
			return;
		}
		?>
<style id="axl-lead-css">html.axl-lead-open{overflow:hidden}html.axl-lead-open body>*:not(#axl-lead-demo){visibility:hidden!important}#axl-lead-demo{position:fixed;inset:0;z-index:2147483647;visibility:visible}#axl-lead-demo[hidden]{display:none}</style>
<script id="axl-lead-early">if(location.hash==='#lead-demo'){document.documentElement.classList.add('axl-lead-open');}</script>
		<?php
	},
	60
);

add_action(
	'wp_footer',
	function () use ( $axiom_arroyos_lead_applies ) {
		static $done = false;
		if ( $done || ! $axiom_arroyos_lead_applies() ) {
			return;
		}
		$done = true;
		?>
__TPL__
<script id="axl-lead-js">
__JS__</script>
		<?php
	},
	99
);
'''
php = php.replace("__TPL__", tpl).replace("__JS__", loader)
open(os.path.join(HERE, "main.php"), "w", encoding="utf8").write(php)
# local harness: a stand-in page with the same head/footer output, for testing before anything goes live
head = re.search(r"\?>\n(<style id=\"axl-lead-css\">.*?</script>)\n", php, re.S).group(1)
open(os.path.join(HERE, "harness.html"), "w", encoding="utf8").write(
    '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stand-in page</title>'
    '<link rel="stylesheet" href="../2026-11-10-arroyos-v2/fonts/fonts.css">' + head +
    '</head><body><h1 id="page">Stand-in for page 1716</h1><p style="height:2000px">content</p>\n' + tpl + '\n<script>\n' + loader + '</script></body></html>')
print("main.php", len(php.encode()), "bytes")
