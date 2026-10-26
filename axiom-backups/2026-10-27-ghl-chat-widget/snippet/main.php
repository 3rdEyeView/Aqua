<?php
/**
 * Axiom GHL Chat Widget
 * Loads the official LeadConnector (GoHighLevel) chat widget once, in the footer of every public page.
 * WIDGET_TAG is the exact code supplied by GoHighLevel (widget 6adfdfee388cb81c668e729a); do not edit it.
 * Not loaded in wp-admin, the Elementor editor preview, feeds, embeds, REST or AJAX responses.
 * Touches nothing else: no form, tracking, CRM sync or consent settings.
 * Rollback: unpublish this snippet.
 */
namespace AngieSnippets\AxiomGhlChatWidget;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const WIDGET_TAG = '<script src="https://widgets.leadconnectorhq.com/loader.js" data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" data-widget-id="6adfdfee388cb81c668e729a" data-source="WEB_USER"></script>';

function is_editor_preview() {
	// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- read-only check.
	if ( isset( $_GET['elementor-preview'] ) ) {
		return true;
	}
	return class_exists( '\Elementor\Plugin' ) && isset( \Elementor\Plugin::$instance->preview )
		&& \Elementor\Plugin::$instance->preview && \Elementor\Plugin::$instance->preview->is_preview_mode();
}

add_action(
	'wp_footer',
	function () {
		static $done = false;
		if ( $done || is_admin() || is_feed() || is_embed() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) || is_editor_preview() ) {
			return;
		}
		$done = true;
		echo "\n" . WIDGET_TAG . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput -- exact vendor tag, static.
	},
	100
);
