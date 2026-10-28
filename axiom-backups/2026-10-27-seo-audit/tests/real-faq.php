<?php
namespace { define( 'ABSPATH', '/' ); $GLOBALS['F'] = array();
function add_filter( $h, $cb, $p = 10 ) { $GLOBALS['F'][ $h ][] = $cb; } function add_action() {} function wp_json_encode( $d ) { return json_encode( $d ); }
require $argv[1]; $html = file_get_contents( $argv[2] ); $out = $GLOBALS['F']['elementor/frontend/the_content'][0]( $html );
preg_match_all( '#<script type="application/ld\+json">(.*?)</script>#s', $out, $m ); $faq = array_values( array_filter( $m[1], function ( $j ) { return false !== strpos( $j, '"FAQPage"' ); } ) );
$d = json_decode( $faq[0], true ); echo count( $faq ), " FAQPage block(s), ", count( $d['mainEntity'] ), " questions\n";
foreach ( $d['mainEntity'] as $q ) echo ' - ', $q['name'], "\n";
echo 'non-script HTML identical: ', var_export( preg_replace( '#<script.*?</script>#s', '', $out ) === preg_replace( '#<script.*?</script>#s', '', $html ), true ), "\n"; }
