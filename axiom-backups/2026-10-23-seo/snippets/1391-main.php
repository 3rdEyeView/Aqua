<?php
/**
 * Axiom Yoast Names (one-time)
 * Renames Yoast's Organization name and Website name from "AxiomSystems" to
 * "Axiom Systems" (Yoast SEO > Settings > Site representation / Site basics).
 * Only changes a value that still reads "AxiomSystems", so repeat runs do
 * nothing. Delete this snippet once the names are updated.
 */
namespace AngieSnippets\AxiomYoastNames_1391;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action(
	'init',
	function () {
		if ( ! class_exists( '\WPSEO_Options' ) ) {
			return;
		}
		foreach ( array( 'website_name', 'company_name' ) as $key ) {
			if ( 'AxiomSystems' === \WPSEO_Options::get( $key ) ) {
				\WPSEO_Options::set( $key, 'Axiom Systems' );
			}
		}
	},
	20
);
