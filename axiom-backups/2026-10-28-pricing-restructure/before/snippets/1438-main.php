<?php
/**
 * Axiom SEO Signals
 * - Adds verified business facts (description, email, founder, area served)
 *   to Yoast's existing Organization schema. Telephone stays with the
 *   Axiom Business Phone snippet.
 * - Merges the separate FAQPage JSON-LD blocks that Elementor prints for each
 *   accordion into one FAQPage per page (Google expects a single FAQPage).
 * - Keeps retired pages (already 301-redirected or noindexed) and client demo
 *   pages out of the site's own search results.
 * Rollback: unpublish or delete this snippet.
 */
namespace AngieSnippets\AxiomSeoSignals_1438;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const ORG_DESCRIPTION = 'Axiom Systems designs, builds and manages professional websites for small businesses, with digital marketing, Google Ads management and lead automation. Based in St. Petersburg, Florida, serving businesses across the United States.';
const ORG_EMAIL       = 'axiom.systems.co@gmail.com';
const FOUNDER         = 'Michael Hinkle';

// Retired pages (see Axiom Legacy Redirects), the retired Revenue Maps post and client demo pages.
const HIDDEN_FROM_SEARCH = array( 9, 107, 109, 230, 393, 1184, 1247 );

add_filter(
	'wpseo_schema_organization',
	function ( $data ) {
		if ( ! is_array( $data ) ) {
			return $data;
		}
		$data['description'] = ORG_DESCRIPTION;
		$data['email']       = ORG_EMAIL;
		$data['founder']     = array(
			'@type' => 'Person',
			'name'  => FOUNDER,
		);
		$data['areaServed']  = array(
			'@type' => 'Country',
			'name'  => 'United States',
		);
		return $data;
	},
	20
);

function merge_faq_schema( $content ) {
	if ( ! is_string( $content ) || false === strpos( $content, 'FAQPage' ) ) {
		return $content;
	}
	$pattern = '#<script type="application/ld\+json">(\{"@context":"https:\\\\/\\\\/schema.org","@type":"FAQPage".*?\})</script>#s';
	if ( preg_match_all( $pattern, $content, $m ) < 2 ) {
		return $content;
	}
	$questions = array();
	foreach ( $m[1] as $json ) {
		$block = json_decode( $json, true );
		if ( ! is_array( $block ) || empty( $block['mainEntity'] ) || ! is_array( $block['mainEntity'] ) ) {
			return $content; // Unexpected shape: leave the page as it is.
		}
		$questions = array_merge( $questions, $block['mainEntity'] );
	}
	$merged = '<script type="application/ld+json">' . wp_json_encode(
		array(
			'@context'   => 'https://schema.org',
			'@type'      => 'FAQPage',
			'mainEntity' => $questions,
		)
	) . '</script>';
	$first = true;
	return preg_replace_callback(
		$pattern,
		function () use ( &$first, $merged ) {
			$out   = $first ? $merged : '';
			$first = false;
			return $out;
		},
		$content
	);
}

add_filter( 'elementor/frontend/the_content', __NAMESPACE__ . '\\merge_faq_schema', 40 );

add_action(
	'pre_get_posts',
	function ( $query ) {
		if ( is_admin() || ! $query->is_main_query() || ! $query->is_search() ) {
			return;
		}
		$query->set( 'post__not_in', array_merge( array_filter( (array) $query->get( 'post__not_in' ) ), HIDDEN_FROM_SEARCH ) );
	}
);
