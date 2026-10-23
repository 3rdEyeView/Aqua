<?php
/**
 * Axiom GHL Hook Probe (temporary, read-only)
 * Records which Jetpack form submission hooks fire for the Get Started form,
 * their order and argument shapes (field labels only, never values), and reports
 * server capabilities for a background queue. Sends no lead data anywhere.
 * Read (admins only): GET /wp-json/axiom/v1/ghl-probe. Delete after testing.
 */
namespace AngieSnippets\AxiomGhlProbe_1393;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const OPT = 'axiom_ghl_probe_log';

function shape( $value ) {
	if ( is_array( $value ) ) {
		$out = array( 'type' => 'array', 'count' => count( $value ), 'keys' => array() );
		foreach ( array_slice( array_keys( $value ), 0, 20 ) as $k ) {
			$v                       = $value[ $k ];
			$out['keys'][ (string) $k ] = is_object( $v ) ? get_class( $v ) : gettype( $v );
		}
		return $out;
	}
	if ( is_object( $value ) ) {
		return array( 'type' => get_class( $value ) );
	}
	if ( is_int( $value ) || is_bool( $value ) || null === $value ) {
		return array( 'type' => gettype( $value ), 'value' => $value );
	}
	return array( 'type' => gettype( $value ) );
}

function record( $hook, $args ) {
	$log   = get_option( OPT, array() );
	$entry = array(
		'hook' => $hook,
		't'    => microtime( true ),
		'args' => array_map( __NAMESPACE__ . '\\shape', $args ),
	);
	if ( isset( $args[0] ) && is_int( $args[0] ) && $post = get_post( $args[0] ) ) {
		$entry['post'] = array( 'type' => $post->post_type, 'status' => $post->post_status, 'parent' => (int) $post->post_parent );
	}
	$log[] = $entry;
	update_option( OPT, array_slice( $log, -150 ), false );
}

// Every forms-related hook name that fires (names only), once per request.
add_action(
	'all',
	function ( $tag ) {
		static $seen = array();
		if ( isset( $seen[ $tag ] ) || count( $seen ) > 80 || ! preg_match( '/^(grunion|wp_insert_post$|save_post_feedback$|transition_post_status$|wp_mail$|pre_wp_mail$|wp_mail_succeeded$|wp_mail_failed$)|(response|submission|feedback)/i', $tag ) || preg_match( '/(register|registered|labels|rest_|_format|gettext|rewrite|wcpay|woocommerce_blocks|enable$)/i', $tag ) ) {
			return;
		}
		$seen[ $tag ] = true;
		$args         = func_get_args();
		array_shift( $args );
		$keep = preg_match( '/(grunion|feedback|jetpack|contact|insert_post)/i', $tag );
		record( 'ALL:' . $tag . ( wp_doing_ajax() ? ' [ajax]' : '' ), $keep ? $args : array() );
	}
);

add_action(
	'wp_footer',
	function () {
		record( 'selftest-footer', array() );
		echo "<!-- axiom-probe-1393 -->\n";
	}
);

foreach ( array( 'grunion_pre_message_sent', 'grunion_after_feedback_post_inserted', 'grunion_after_message_sent', 'jetpack_forms_response_created' ) as $hook ) {
	add_action(
		$hook,
		function () use ( $hook ) {
			record( $hook, func_get_args() );
		},
		999,
		10
	);
}

add_action(
	'rest_api_init',
	function () {
		register_rest_route(
			'axiom/v1',
			'/ghl-probe',
			array(
				'methods'             => 'GET',
				'permission_callback' => function () {
					return current_user_can( 'manage_options' );
				},
				'callback'            => function () {
					if ( isset( $_GET['reset'] ) ) {
						delete_option( OPT );
					}
					$err = null;
					try {
						record( 'selftest-rest', array( 1 ) );
					} catch ( \Throwable $e ) {
						$err = get_class( $e ) . ': ' . $e->getMessage() . ' line ' . $e->getLine();
					}
					$direct = update_option( 'axiom_ghl_probe_direct', time(), false );
					$t0   = microtime( true );
					$resp = wp_remote_head( 'https://services.leadconnectorhq.com/', array( 'timeout' => 10 ) );
					return array(
						'log' => get_option( OPT, array() ),
						'debug' => array( 'error' => $err, 'direct_update' => $direct, 'direct_read' => get_option( 'axiom_ghl_probe_direct' ), 'log_type' => gettype( get_option( OPT ) ) ),
						'env' => array(
							'php'                         => PHP_VERSION,
							'action_scheduler'            => function_exists( 'as_enqueue_async_action' ),
							'action_scheduler_version'    => class_exists( '\ActionScheduler_Versions' ) ? \ActionScheduler_Versions::instance()->latest_version() : null,
							'disable_wp_cron'             => defined( 'DISABLE_WP_CRON' ) && DISABLE_WP_CRON,
							'alternate_wp_cron'           => defined( 'ALTERNATE_WP_CRON' ) && ALTERNATE_WP_CRON,
							'fastcgi_finish_request'      => function_exists( 'fastcgi_finish_request' ),
							'ghl_constants_defined'       => array( defined( 'AXIOM_GHL_TOKEN' ), defined( 'AXIOM_GHL_LOCATION_ID' ) ),
							'ghl_host_reachable'          => is_wp_error( $resp ) ? $resp->get_error_message() : wp_remote_retrieve_response_code( $resp ),
							'ghl_host_ms'                 => (int) ( ( microtime( true ) - $t0 ) * 1000 ),
							'next_cron'                   => wp_next_scheduled( 'action_scheduler_run_queue' ),
						),
					);
				},
			)
		);
	}
);
