<?php
namespace { define( 'ABSPATH', '/' ); function add_action() {} function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); } require $argv[1]; }
namespace T { use function AngieSnippets\AxiomRetiredUrls_1441\decide; $f = 0;
function ok( $got, $want, $m ) { global $f; $p = $got === $want; echo ( $p ? 'PASS ' : 'FAIL ' ) . $m . ( $p ? '' : ' got ' . json_encode( $got ) ) . "\n"; if ( ! $p ) $f++; }
$d = function ( $u, $q = array(), $a = false, $dt = false ) { return decide( $u, $q, $a, $dt ); };
ok( $d( '/how-axiom-systems-builds-revenue-maps-that-actually-convert/' ), array( 410 ), 'revenue maps post 410' );
ok( $d( '/how-axiom-systems-builds-revenue-maps-that-actually-convert' ), array( 410 ), 'no trailing slash 410' );
ok( $d( '/How-Axiom-Systems-Builds-Revenue-Maps-That-Actually-Convert/?utm=x' ), array( 410 ), 'case + query 410' );
ok( $d( '/https:/axiomsystems.systems/shop/sample-product/axiom-platinum/' ), array( 410 ), 'malformed product platinum 410' );
ok( $d( '/https://axiomsystems.systems/shop/sample-product/axiom-revenue-systems-audit/' ), array( 410 ), 'double-slash variant 410' );
ok( $d( '/https:/axiomsystems.systems/shop/sample-product/website-builder/' ), array( 301, '/pricing/' ), 'website product -> pricing' );
ok( $d( '/https:/axiomsystems.systems/shop/sample-product/google-ppc-ads/' ), array( 301, '/add-ons/' ), 'ppc product -> add-ons' );
ok( $d( '/https:/axiomsystems.systems/shop/sample-product/%f0%9f%a7%a0-crm-automation/' ), array( 301, '/add-ons/' ), 'emoji crm product -> add-ons' );
ok( $d( '/https:/axiomsystems.systems/shop/sample-product/%F0%9F%93%B1-meta-ads-facebook-instagram/' ), array( 410 ), 'emoji meta ads 410' );
ok( $d( '/product/axiom-launch/' ), array( 410 ), 'standard product base 410' );
ok( $d( '/product/unknown-thing/' ), array( 410 ), 'unknown product 410' );
ok( $d( '/shop/' ), array( 301, '/pricing/' ), 'shop -> pricing' );
ok( $d( '/shop/page/2/' ), array( 301, '/pricing/' ), 'shop page 2 -> pricing' );
ok( $d( '/https:/axiomsystems.systems/shop/' ), array( 301, '/pricing/' ), 'malformed shop -> pricing' );
ok( $d( '/product-category/uncategorized/' ), array( 410 ), 'product category 410' );
ok( $d( '/product-tag/x/' ), array( 410 ), 'product tag 410' );
ok( $d( '/', array( 'post_type' => 'product' ) ), array( 301, '/pricing/' ), '?post_type=product -> pricing' );
ok( $d( '/', array( 'post_type' => 'product', 'p' => '371' ) ), array( 410 ), '?post_type=product&p= 410' );
ok( $d( '/author/axiomsystems/', array(), true ), array( 404 ), 'author archive 404' );
ok( $d( '/2026/', array(), false, true ), array( 404 ), 'date archive 404' );
foreach ( array( '/', '/pricing/', '/add-ons/', '/our-work/', '/how-it-works/', '/faq/', '/get-started/', '/privacy-policy/', '/myrtle-beach-ink-demo/', '/services/', '/about-us/', '/elementor-9/', '/contact-axiom-systems/', '/category/uncategorized/', '/shopping-guide/', '/feed/', '/wp-json/', '/sitemap_index.xml' ) as $u ) {
	ok( $d( $u ), null, 'untouched ' . $u );
}
ok( $d( '/get-started/', array( 'plan' => 'growth' ) ), null, 'get-started with plan untouched' );
echo $f ? "\n$f FAILED\n" : "\nALL PASSED\n"; exit( $f ? 1 : 0 ); }
