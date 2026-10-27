<?php
/**
 * Axiom Retired URLs
 * Answers URLs from discontinued offers so search engines drop them cleanly:
 * - 301 to the current page when one replaces the old offer (shop -> Pricing,
 *   website/Google Ads/CRM products -> Pricing or Add-Ons);
 * - 410 Gone for discontinued content with no replacement (Revenue Maps post,
 *   old packages and audits, product categories/tags);
 * - 404 for author and date archives (they only listed the retired post).
 * Gone/not-found responses use the theme's normal 404 page.
 * Old page redirects stay in Axiom Legacy Redirects (snippet 1390).
 * Rollback: unpublish or delete this snippet.
 */
namespace AngieSnippets\AxiomRetiredUrls_1441;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Product slug (without emoji prefix) => current path, or null for 410 Gone.
function products() {
	return array(
		'website-builder'               => '/pricing/',
		'google-ppc-ads'                => '/add-ons/',
		'crm-automation'                => '/add-ons/',
		'axiom-launch'                  => null,
		'axiom-platinum'                => null,
		'axiom-revenue-systems-audit'   => null,
		'funnels-conversion-systems'    => null,
		'meta-ads-facebook-instagram'   => null,
		'digital-graphic-design'        => null,
	);
}

const GONE_PATHS = array(
	'/how-axiom-systems-builds-revenue-maps-that-actually-convert/',
);

/**
 * Decides the response for a request.
 * Returns null (leave alone), array( 301, path ), array( 410 ) or array( 404 ).
 */
function decide( $request_uri, $query, $is_author, $is_date ) {
	$path = strtolower( rawurldecode( (string) wp_parse_url( $request_uri, PHP_URL_PATH ) ) );
	$path = preg_replace( '#/+#', '/', $path );
	$path = rtrim( $path, '/' ) . '/';

	if ( in_array( $path, GONE_PATHS, true ) ) {
		return array( 410 );
	}
	// Products, including the malformed /https:/axiomsystems.systems/shop/sample-product/... permalinks.
	if ( preg_match( '#^/(?:https?:/axiomsystems\.systems/)?(?:shop/sample-product|product)/([^/]+)/$#u', $path, $m ) ) {
		$slug = preg_replace( '/^[^a-z0-9]+/', '', $m[1] );
		$map  = products();
		return isset( $map[ $slug ] ) ? array( 301, $map[ $slug ] ) : array( 410 );
	}
	if ( preg_match( '#^/(?:https?:/axiomsystems\.systems/)?(?:product-category|product-tag)/#', $path ) ) {
		return array( 410 );
	}
	if ( preg_match( '#^/(?:https?:/axiomsystems\.systems/)?shop/(?:page/\d+/)?$#', $path ) ) {
		return array( 301, '/pricing/' );
	}
	if ( isset( $query['post_type'] ) && 'product' === $query['post_type'] ) {
		return ( isset( $query['p'] ) || isset( $query['product'] ) ) ? array( 410 ) : array( 301, '/pricing/' );
	}
	if ( $is_author || $is_date ) {
		return array( 404 );
	}
	return null;
}

function respond_missing( $code ) {
	global $wp_query;
	$wp_query->set_404();
	status_header( $code );
	nocache_headers();
	$template = get_query_template( '404' );
	if ( ! $template ) {
		$template = get_index_template();
	}
	include $template;
	exit;
}

add_action(
	'template_redirect',
	function () {
		if ( is_admin() || is_preview() || isset( $_GET['elementor-preview'] ) ) {
			return;
		}
		$query  = array_map( 'sanitize_key', wp_unslash( array_intersect_key( $_GET, array_flip( array( 'post_type', 'p', 'product' ) ) ) ) );
		$action = decide( isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '/', $query, is_author(), is_date() );
		if ( ! $action ) {
			return;
		}
		if ( 301 === $action[0] ) {
			wp_safe_redirect( home_url( $action[1] ), 301, 'Axiom Systems' );
			exit;
		}
		respond_missing( $action[0] );
	},
	0
);
