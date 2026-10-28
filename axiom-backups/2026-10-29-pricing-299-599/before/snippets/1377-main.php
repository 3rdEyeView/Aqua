<?php
/**
 * Axiom Business Phone
 * Adds the business phone number, as a click-to-call link, to the rendered
 * Elementor pages: next to the header's Get Started button (icon-only at
 * tablet/mobile widths; on phones narrower than 385px the header has no room,
 * so the number is in the mobile menu instead), under the footer tagline, and as a secondary line
 * after the contact lines in the Get Started sections. Also sets the
 * telephone on Yoast's existing Organization schema.
 * Page content is not edited; each insertion is skipped when its anchor
 * text is not found, so the page renders exactly as before.
 * Rollback: unpublish or delete this snippet.
 */
namespace AngieSnippets\AxiomBusinessPhone_1377;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const PHONE_DISPLAY = '(727) 591-7527';
const PHONE_HREF    = 'tel:+17275917527';
const PHONE_SCHEMA  = '+1-727-591-7527';

function should_run() {
	if ( is_admin() || wp_doing_ajax() || is_customize_preview() || is_feed() ) {
		return false;
	}
	if ( \defined( 'REST_REQUEST' ) && REST_REQUEST ) {
		return false;
	}
	// Skip inside the Elementor editor preview iframe.
	if ( isset( $_GET['elementor-preview'] ) ) {
		return false;
	}
	return is_singular( 'page' );
}

function icon( $size ) {
	return '<svg class="axp-icon" viewBox="0 0 24 24" width="' . $size . '" height="' . $size . '" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>';
}

function header_link() {
	return '<a class="axp-call" href="' . PHONE_HREF . '">' . icon( 16 ) . '<span class="axp-sr">Call us at </span><span class="axp-num">' . PHONE_DISPLAY . '</span></a>';
}

function footer_link() {
	return '<a class="axp-foot" href="' . PHONE_HREF . '">' . icon( 14 ) . '<span class="axp-sr">Call us at </span>' . PHONE_DISPLAY . '</a>';
}

function direct_line( $attrs ) {
	$class = preg_match( '/\bclass="([^"]*)"/', $attrs, $m ) ? $m[1] . ' ' : '';
	return '<p class="' . $class . 'axp-direct">Prefer to speak directly? Call us at <a class="axp-direct-link" href="' . PHONE_HREF . '">' . PHONE_DISPLAY . '</a>.</p>';
}

function add_phone( $content ) {
	if ( ! is_string( $content ) || ! should_run() || false !== strpos( $content, 'axp-call' ) ) {
		return $content;
	}

	// Header: group the phone link with the Get Started button that follows the
	// nav. The Axiom Mobile Menu snippet adds its menu button to this group.
	$content = preg_replace(
		'#(</nav>\s*)(<a\b[^>]*\bclass="ax-btn\b[^"]*"[^>]*>\s*Get Started\s*</a>)#',
		'$1<div class="axm-group axp-group">' . header_link() . '$2</div>',
		$content,
		1
	);

	// Footer: under the brand tagline.
	$content = preg_replace(
		'#(Managed websites, automation and lead generation for local businesses\.\s*</span>)#',
		'$1' . footer_link(),
		$content,
		1
	);

	// Get Started sections: after the email line, and after the form note on
	// the Get Started page. The new line reuses that paragraph's classes.
	$content = preg_replace_callback(
		'#<p\b([^>]*)>\s*(?:Or write to us directly at|Prefer email\?|Sending this form doesn(?:\'|&\#8217;|&\#039;|\x{2019})t start a subscription)[^<]*</p>#u',
		function ( $m ) {
			return $m[0] . direct_line( $m[1] );
		},
		$content
	);

	return $content;
}

add_filter( 'elementor/frontend/the_content', __NAMESPACE__ . '\\add_phone', 30 );

add_action(
	'wp_head',
	function () {
		if ( ! should_run() ) {
			return;
		}
		echo '<style id="axp-phone-css">' . \trim( CSS ) . '</style>' . "\n";
	},
	51
);

// Yoast already outputs an Organization piece; add the telephone to it.
add_filter(
	'wpseo_schema_organization',
	function ( $data ) {
		if ( is_array( $data ) ) {
			$data['telephone'] = PHONE_SCHEMA;
		}
		return $data;
	}
);

// Classes are doubled to stay above the Elementor kit's link colour rule.
const CSS = <<<'AXPCSS'
.axp-sr{position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.axp-group{display:flex;align-items:center;gap:8px;flex:0 0 auto}
.axp-call.axp-call,.axp-call.axp-call:hover,.axp-call.axp-call:focus,.axp-call.axp-call:active{display:inline-flex;align-items:center;gap:.45rem;padding:.6rem .2rem;border-radius:8px;font-family:var(--ax-body,Inter),sans-serif;font-weight:600;font-size:.9375rem;line-height:1.2;letter-spacing:-.005em;color:var(--ax-ink,#0A1628);text-decoration:none;white-space:nowrap;-webkit-tap-highlight-color:transparent}
.axp-call.axp-call .axp-icon{flex:0 0 auto;color:var(--ax-blue,#1D6CE2)}
.axp-call.axp-call:hover .axp-num{color:var(--ax-blue,#1D6CE2)}
.axp-call.axp-call:focus-visible,.axp-foot.axp-foot:focus-visible,.axp-direct-link:focus-visible{outline:2px solid var(--ax-blue,#1D6CE2);outline-offset:2px}
@media (min-width:1025px){.axm-group.axp-group{gap:1.25rem}}
@media (max-width:1024px){
.axp-call.axp-call,.axp-call.axp-call:hover,.axp-call.axp-call:focus,.axp-call.axp-call:active{justify-content:center;width:44px;height:44px;margin:-3px 0;padding:0;border:1px solid var(--ax-line,#E2E7EE);border-radius:10px;background:#fff;flex:0 0 44px;box-sizing:border-box}
.axp-call.axp-call:hover{border-color:#C9D2DE;background:var(--ax-paper,#F5F7FA)}
.axp-call.axp-call .axp-icon{width:18px;height:18px}
.axp-call.axp-call .axp-num{position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
}
@media (max-width:767px){
.axp-call.axp-call,.axp-call.axp-call:hover,.axp-call.axp-call:focus,.axp-call.axp-call:active{width:36px;flex-basis:36px;margin-right:-4px;border-color:transparent;background:transparent}
.axp-call.axp-call:hover{background:var(--ax-paper,#F5F7FA)}
.axp-call.axp-call .axp-icon{width:20px;height:20px}
}
@media (max-width:384px){.axp-group .axp-call.axp-call{display:none}}
.axp-foot.axp-foot,.axp-foot.axp-foot:focus,.axp-foot.axp-foot:active{display:inline-flex;align-items:center;align-self:flex-start;gap:.45rem;margin-top:.5rem;font-family:var(--ax-body,Inter),sans-serif;font-weight:600;font-size:.9375rem;line-height:1.3;color:#C9D2DE;text-decoration:none;white-space:nowrap}
.axp-foot.axp-foot .axp-icon{flex:0 0 auto;color:#7FA8EA}
.axp-foot.axp-foot:hover{color:#FFFFFF;text-decoration:underline;text-underline-offset:3px}
.axp-direct .axp-direct-link,.axp-direct .axp-direct-link:hover,.axp-direct .axp-direct-link:focus{color:inherit;font-weight:600;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px;white-space:nowrap}
.axp-direct .axp-direct-link:hover{text-decoration-thickness:2px}

AXPCSS;
