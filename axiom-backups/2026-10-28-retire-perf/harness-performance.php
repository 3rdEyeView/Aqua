<?php
namespace { define( 'ABSPATH', '/' ); $GLOBALS['H'] = array(); $GLOBALS['S'] = array( 'admin' => false, 'singular' => true, 'tpl' => 'elementor_canvas', 'woo' => false ); $GLOBALS['DQ'] = array();
function add_action( $h, $cb, $p = 10 ) { $GLOBALS['H'][ $h ][] = $cb; } function add_filter( $h, $cb, $p = 10 ) { $GLOBALS['H'][ $h ][] = $cb; }
function is_admin() { return $GLOBALS['S']['admin']; } function wp_doing_ajax() { return false; } function is_customize_preview() { return false; }
function is_singular() { return $GLOBALS['S']['singular']; } function get_page_template_slug() { return $GLOBALS['S']['tpl']; }
function is_woocommerce() { return $GLOBALS['S']['woo']; } function is_cart() { return false; } function is_checkout() { return false; } function is_account_page() { return false; }
function wp_dequeue_style( $h ) { $GLOBALS['DQ'][] = 's:' . $h; } function wp_dequeue_script( $h ) { $GLOBALS['DQ'][] = 'j:' . $h; }
require $argv[1]; }
namespace T { $f = 0; function ok( $c, $m ) { global $f; echo ( $c ? 'PASS ' : 'FAIL ' ) . $m . "\n"; if ( ! $c ) $f++; }
$H = &$GLOBALS['H']; $S = &$GLOBALS['S'];
$head = function () use ( &$H ) { ob_start(); $H['wp_head'][0](); return ob_get_clean(); };
ok( false !== strpos( $head(), 'name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"' ), 'canvas page: early viewport' );
$S['tpl'] = ''; ok( '' === $head(), 'theme page: no extra viewport' ); $S['tpl'] = 'elementor_canvas';
$S['singular'] = false; ok( '' === $head(), 'archive/404: no extra viewport' ); $S['singular'] = true;
$_GET['elementor-preview'] = 1; ok( '' === $head(), 'editor preview: untouched' ); unset( $_GET['elementor-preview'] );
$st = $H['style_loader_tag'][0];
ok( '' === $st( '<link roboto>', 'elementor-gf-roboto' ) && '' === $st( '<link slab>', 'elementor-gf-robotoslab' ), 'roboto + slab dropped' );
ok( '<link inter>' === $st( '<link inter>', 'elementor-gf-inter' ) && '<link m>' === $st( '<link m>', 'elementor-gf-manrope' ), 'inter + manrope kept' );
$S['admin'] = true; ok( '<link roboto>' === $st( '<link roboto>', 'elementor-gf-roboto' ), 'admin: roboto kept' ); $S['admin'] = false;
$rh = $H['wp_resource_hints'][0]; $u = $rh( array(), 'preconnect' ); ok( 'https://fonts.gstatic.com' === $u[0]['href'] && 'anonymous' === $u[0]['crossorigin'], 'preconnect gstatic' );
ok( array( 'x' ) === $rh( array( 'x' ), 'dns-prefetch' ), 'other hints untouched' );
$H['wp_enqueue_scripts'][0](); ok( in_array( 's:woocommerce-general', $GLOBALS['DQ'], true ) && in_array( 'j:wc-order-attribution', $GLOBALS['DQ'], true ) && ! preg_grep( '/gtag|googlesitekit|jquery-core|jetpack|leadconnector/', $GLOBALS['DQ'] ), 'non-store page: woo assets dequeued, tracking/jquery/jetpack not' );
$GLOBALS['DQ'] = array(); $S['woo'] = true; $H['wp_print_footer_scripts'][0](); ok( array() === $GLOBALS['DQ'], 'store page: nothing dequeued' );
echo $f ? "\n$f FAILED\n" : "\nALL PASSED\n"; exit( $f ? 1 : 0 ); }
