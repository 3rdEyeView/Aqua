<?php
/**
 * Axiom Archive Noindex (one-time)
 * Sets Yoast "Show in search results" to No for the shop (product archive) and
 * the category, product category, product tag and author archives, which also
 * removes them from the Yoast XML sitemap. The previous values are saved once
 * in the axiom_seo_archives_backup option and can be read (admins only) at
 * GET /wp-json/axiom/v1/seo-archives. Delete this snippet once applied; the
 * settings stay in Yoast SEO > Settings.
 */
namespace AngieSnippets\AxiomArchiveNoindex_1392;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const BACKUP = 'axiom_seo_archives_backup';

function targets() {
	return array(
		'noindex-ptarchive-product' => true,
		'noindex-tax-category'      => true,
		'noindex-tax-product_cat'   => true,
		'noindex-tax-product_tag'   => true,
		'noindex-author-wpseo'      => true,
	);
}

function current_values() {
	$out = array();
	foreach ( array_keys( targets() ) as $key ) {
		$out[ $key ] = \WPSEO_Options::get( $key );
	}
	$out['disable-author'] = \WPSEO_Options::get( 'disable-author' );
	return $out;
}

add_action(
	'init',
	function () {
		if ( ! class_exists( '\WPSEO_Options' ) ) {
			return;
		}
		if ( false === get_option( BACKUP ) ) {
			add_option( BACKUP, current_values(), '', false );
		}
		foreach ( targets() as $key => $value ) {
			if ( \WPSEO_Options::get( $key ) !== $value ) {
				\WPSEO_Options::set( $key, $value );
			}
		}
	},
	20
);

add_action(
	'rest_api_init',
	function () {
		register_rest_route(
			'axiom/v1',
			'/seo-archives',
			array(
				'methods'             => 'GET',
				'permission_callback' => function () {
					return current_user_can( 'manage_options' );
				},
				'callback'            => function () {
					return array(
						'backup'  => get_option( BACKUP ),
						'current' => class_exists( '\WPSEO_Options' ) ? current_values() : null,
					);
				},
			)
		);
	}
);
