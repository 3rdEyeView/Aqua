<?php
/**
 * Axiom Legacy Redirects
 * Permanently redirects pages from the previous site to their current
 * equivalents and keeps them out of the Yoast XML sitemap. The old pages
 * are left in place (unchanged), so removing this snippet restores them.
 * Rollback: unpublish or delete this snippet.
 */
namespace AngieSnippets\AxiomLegacyRedirects_1390;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Old page ID => current path.
function targets() {
	return array(
		230 => '/get-started/',  // Contact Axiom Systems
		109 => '/#about',        // About Us -> founder section on Home
		9   => '/',              // previous homepage (elementor-9)
		107 => '/pricing/',      // Services
	);
}

add_action(
	'template_redirect',
	function () {
		if ( is_admin() || is_preview() || isset( $_GET['elementor-preview'] ) ) {
			return;
		}
		$id      = get_queried_object_id();
		$targets = targets();
		if ( $id && is_page() && isset( $targets[ $id ] ) ) {
			wp_safe_redirect( home_url( $targets[ $id ] ), 301, 'Axiom Systems' );
			exit;
		}
	},
	1
);

add_filter(
	'wpseo_exclude_from_sitemap_by_post_ids',
	function ( $ids ) {
		return array_values( array_unique( array_merge( (array) $ids, array_keys( targets() ) ) ) );
	}
);
