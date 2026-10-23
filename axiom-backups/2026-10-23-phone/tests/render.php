<?php
// Offline harness: applies the snippet's content filter to saved live HTML.
// Usage: php render.php ../live-snippets/1377-main.php <in-dir> <out-dir>
namespace {
define( 'ABSPATH', '/' );
$GLOBALS['axp_filters'] = array();
function add_filter( $h, $cb ) { $GLOBALS['axp_filters'][ $h ][] = $cb; }
function add_action( $h, $cb ) { $GLOBALS['axp_filters'][ $h ][] = $cb; }
function is_admin() { return false; } function wp_doing_ajax() { return false; }
function is_customize_preview() { return false; } function is_feed() { return false; }
function is_singular( $t ) { return true; }
require $argv[1];
// Undo Cloudflare email obfuscation so the HTML matches what the origin renders.
function cf_decode( $hex ) { $k = hexdec( substr( $hex, 0, 2 ) ); $s = ''; for ( $i = 2; $i < strlen( $hex ); $i += 2 ) { $s .= chr( hexdec( substr( $hex, $i, 2 ) ) ^ $k ); } return $s; }
@mkdir( $argv[3] );
foreach ( glob( $argv[2] . '/*.html' ) as $f ) {
	$h = file_get_contents( $f );
	$h = preg_replace_callback( '#<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="([0-9a-f]+)">\[email&\#160;protected\]</a>#', function ( $m ) { return cf_decode( $m[1] ); }, $h );
	$h = preg_replace_callback( '#<span class="__cf_email__" data-cfemail="([0-9a-f]+)">\[email&\#160;protected\]</span>#', function ( $m ) { return cf_decode( $m[1] ); }, $h );
	$i = strpos( $h, '<body' ); $j = strrpos( $h, '<footer' ) ?: strlen( $h );
	$body = substr( $h, $i );
	foreach ( $GLOBALS['axp_filters']['elementor/frontend/the_content'] as $cb ) { $body = $cb( $body ); $again = $cb( $body ); if ( $again !== $body ) { echo "NOT IDEMPOTENT\n"; } }
	ob_start(); foreach ( $GLOBALS['axp_filters']['wp_head'] as $cb ) { $cb(); } $css = ob_get_clean();
	$out = str_replace( '</head>', $css . '</head>', substr( $h, 0, $i ) ) . $body;
	$org = $GLOBALS['axp_filters']['wpseo_schema_organization'][0]( array( '@type' => 'Organization' ) );
	file_put_contents( $argv[3] . '/' . basename( $f ), $out );
	printf( "%-16s header=%d footer=%d direct=%d tel=%d schema=%s\n", basename( $f ), substr_count( $out, 'class="axp-call"' ), substr_count( $out, 'class="axp-foot"' ), substr_count( $out, 'axp-direct"' ), substr_count( $out, 'href="tel:+17275917527"' ), $org['telephone'] );
}
}
