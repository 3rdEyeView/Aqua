<?php
// Offline tests for the GHL chat widget snippet.
namespace { define( 'ABSPATH', '/' ); $GLOBALS['H'] = array(); $GLOBALS['F'] = array( 'admin' => false, 'feed' => false, 'embed' => false, 'ajax' => false );
function add_action( $h, $cb, $p = 10 ) { $GLOBALS['H'][ $h ][] = $cb; }
function is_admin() { return $GLOBALS['F']['admin']; } function is_feed() { return $GLOBALS['F']['feed']; } function is_embed() { return $GLOBALS['F']['embed']; } function wp_doing_ajax() { return $GLOBALS['F']['ajax']; }
require $argv[1]; }
namespace T { $fails = 0;
function ok( $c, $m ) { global $fails; echo ( $c ? 'PASS ' : 'FAIL ' ) . $m . "\n"; if ( ! $c ) $fails++; }
function footer() { ob_start(); foreach ( $GLOBALS['H']['wp_footer'] as $cb ) { $cb(); } return ob_get_clean(); }
$exact = '<script src="https://widgets.leadconnectorhq.com/loader.js" data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" data-widget-id="6adf9aa5388cb81c665a7bda" data-source="WEB_USER"></script>';
$o = footer();
ok( 1 === substr_count( $o, $exact ) && trim( $o ) === $exact, 'public page: exact vendor tag, once' );
ok( '' === footer(), 'second wp_footer call in the same request: no duplicate' );
$_GET['elementor-preview'] = '1095';
ok( \AngieSnippets\AxiomGhlChatWidget\is_editor_preview(), 'Elementor editor preview detected (widget skipped)' );
unset( $_GET['elementor-preview'] );
ok( ! \AngieSnippets\AxiomGhlChatWidget\is_editor_preview(), 'normal page is not a preview' );
echo $fails ? "\n$fails FAILED\n" : "\nALL PASSED\n"; exit( $fails ? 1 : 0 ); }
