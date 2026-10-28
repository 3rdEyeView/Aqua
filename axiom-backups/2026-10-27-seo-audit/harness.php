<?php
// Offline tests for snippet/main.php (Axiom SEO Signals).
namespace { define( 'ABSPATH', '/' ); $GLOBALS['F'] = array(); $GLOBALS['A'] = array(); $GLOBALS['admin'] = false;
function add_filter( $h, $cb, $p = 10 ) { $GLOBALS['F'][ $h ][] = $cb; } function add_action( $h, $cb, $p = 10 ) { $GLOBALS['A'][ $h ][] = $cb; }
function is_admin() { return $GLOBALS['admin']; } function wp_json_encode( $d ) { return json_encode( $d ); }
class Q { public $v = array(); public $main = true; public $search = true; function is_main_query() { return $this->main; } function is_search() { return $this->search; } function get( $k ) { return $this->v[ $k ] ?? ''; } function set( $k, $x ) { $this->v[ $k ] = $x; } }
require $argv[1]; }
namespace T { $fails = 0; function ok( $c, $m ) { global $fails; echo ( $c ? 'PASS ' : 'FAIL ' ) . $m . "\n"; if ( ! $c ) $fails++; }
$org = $GLOBALS['F']['wpseo_schema_organization'][0]( array( '@type' => 'Organization', 'name' => 'Axiom Systems', 'telephone' => '+1-727-591-7527' ) );
ok( 'Axiom Systems' === $org['name'] && '+1-727-591-7527' === $org['telephone'], 'org: existing keys kept' );
ok( 'axiom.systems.co@gmail.com' === $org['email'] && 'Michael Hinkle' === $org['founder']['name'] && 'United States' === $org['areaServed']['name'] && strlen( $org['description'] ) > 50, 'org: facts added' );
$merge = $GLOBALS['F']['elementor/frontend/the_content'][0];
$q = function ( $n ) { return '{"@type":"Question","name":"Q' . $n . ' it’s","acceptedAnswer":{"@type":"Answer","text":"A' . $n . ' <b>"}}'; };
$blk = function ( ...$ns ) use ( $q ) { return '<script type="application/ld+json">{"@context":"https:\/\/schema.org","@type":"FAQPage","mainEntity":[' . implode( ',', array_map( $q, $ns ) ) . ']}</script>'; };
$yoast = '<script type="application/ld+json" class="yoast-schema-graph">{"@graph":[{"@type":"WebPage"}]}</script>';
$html = $yoast . '<div>a</div>' . $blk( 1, 2 ) . '<div>b</div>' . $blk( 3 ) . '<p>c</p>' . $blk( 4, 5 ) . '<p>d</p>';
$out = $merge( $html );
ok( 1 === substr_count( $out, '"FAQPage"' ), 'faq: one FAQPage left' );
preg_match( '#<script type="application/ld\+json">(.*?)</script>#', $out, $mm ); $d = json_decode( $mm[1], true );
ok( 5 === count( $d['mainEntity'] ) && 'Q1 it’s' === $d['mainEntity'][0]['name'] && 'Q5 it’s' === $d['mainEntity'][4]['name'], 'faq: all 5 questions, in order, decoded intact' );
ok( false !== strpos( $out, $yoast ) && false !== strpos( $out, '<div>a</div>' ) && false !== strpos( $out, '<p>d</p>' ), 'faq: yoast graph and page HTML untouched' );
ok( strip_tags( preg_replace( '#<script.*?</script>#s', '', $out ) ) === strip_tags( preg_replace( '#<script.*?</script>#s', '', $html ) ), 'faq: visible text identical' );
$single = $yoast . $blk( 1, 2 ) . '<p>x</p>'; ok( $single === $merge( $single ), 'faq: single block page unchanged (home)' );
ok( '<p>none</p>' === $merge( '<p>none</p>' ), 'faq: page without FAQ unchanged' );
$bad = $blk( 1 ) . '<script type="application/ld+json">{"@type":"FAQPage","mainEntity":"x"}</script>'; ok( $bad === $merge( $bad ), 'faq: unexpected shape -> unchanged' );
$pg = $GLOBALS['A']['pre_get_posts'][0];
$s = new \Q(); $pg( $s ); ok( array( 9, 107, 109, 230, 393, 1184, 1247 ) === $s->get( 'post__not_in' ), 'search: retired + demo IDs excluded' );
$s = new \Q(); $s->search = false; $pg( $s ); ok( '' === $s->get( 'post__not_in' ), 'non-search query untouched' );
$s = new \Q(); $s->main = false; $pg( $s ); ok( '' === $s->get( 'post__not_in' ), 'secondary query untouched' );
$GLOBALS['admin'] = true; $s = new \Q(); $pg( $s ); ok( '' === $s->get( 'post__not_in' ), 'admin search untouched' );
echo $fails ? "\n$fails FAILED\n" : "\nALL PASSED\n"; exit( $fails ? 1 : 0 ); }
