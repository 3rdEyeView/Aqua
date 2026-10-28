<?php
/**
 * Axiom Performance
 * - Canvas pages: prints the viewport meta tag first in <head>. Elementor Canvas
 *   prints it after the stylesheets, so phones laid the page out at the default
 *   980px width, painted the tablet layout and then shifted (mobile CLS 0.1-0.3).
 *   The later tag is identical, so it changes nothing.
 * - Drops the Roboto and Roboto Slab stylesheets (Elementor kit defaults; no text
 *   on the site uses them). Inter and Manrope are unchanged.
 * - Preconnects to fonts.gstatic.com so the Inter/Manrope files start sooner.
 * - Outside WooCommerce store pages, skips WooCommerce's front-end CSS/JS
 *   (store retired; WooCommerce itself stays active and Action Scheduler,
 *   used by Axiom CRM Sync, is not affected).
 * Not touched: Google tag / Ads / Site Kit, Jetpack forms, GHL chat widget, jQuery.
 * Rollback: unpublish or delete this snippet.
 */
namespace AngieSnippets\AxiomPerformance_1442;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const UNUSED_STYLES = array( 'elementor-gf-roboto', 'elementor-gf-robotoslab' );

const WOO_STYLES  = array( 'woocommerce-general', 'woocommerce-layout', 'woocommerce-smallscreen', 'woocommerce-inline', 'wc-ppcp-mini-cart-buttons' );
const WOO_SCRIPTS = array( 'wc-add-to-cart', 'woocommerce', 'wc-jquery-blockui', 'jquery-blockui', 'wc-js-cookie', 'js-cookie', 'sourcebuster-js', 'wc-order-attribution', 'woocommerce-analytics', 'woocommerce-analytics-client' );

function is_frontend() {
	return ! is_admin() && ! wp_doing_ajax() && ! isset( $_GET['elementor-preview'] ) && ! ( function_exists( 'is_customize_preview' ) && is_customize_preview() );
}

function is_store_page() {
	return ( function_exists( 'is_woocommerce' ) && is_woocommerce() )
		|| ( function_exists( 'is_cart' ) && is_cart() )
		|| ( function_exists( 'is_checkout' ) && is_checkout() )
		|| ( function_exists( 'is_account_page' ) && is_account_page() );
}

add_action(
	'wp_head',
	function () {
		if ( is_frontend() && is_singular() && 'elementor_canvas' === get_page_template_slug() ) {
			echo '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />' . "\n";
		}
	},
	-1000
);

add_filter(
	'style_loader_tag',
	function ( $tag, $handle ) {
		return is_frontend() && in_array( $handle, UNUSED_STYLES, true ) ? '' : $tag;
	},
	10,
	2
);

add_filter(
	'wp_resource_hints',
	function ( $urls, $relation ) {
		if ( 'preconnect' === $relation && is_frontend() ) {
			$urls[] = array(
				'href'        => 'https://fonts.gstatic.com',
				'crossorigin' => 'anonymous',
			);
		}
		return $urls;
	},
	10,
	2
);

function dequeue_woo_assets() {
	if ( ! is_frontend() || is_store_page() ) {
		return;
	}
	foreach ( WOO_STYLES as $h ) {
		wp_dequeue_style( $h );
	}
	foreach ( WOO_SCRIPTS as $h ) {
		wp_dequeue_script( $h );
	}
}

add_action( 'wp_enqueue_scripts', __NAMESPACE__ . '\\dequeue_woo_assets', 999 );
// Some of these are enqueued late (footer); dequeue again before footer scripts print.
add_action( 'wp_print_footer_scripts', __NAMESPACE__ . '\\dequeue_woo_assets', 1 );
