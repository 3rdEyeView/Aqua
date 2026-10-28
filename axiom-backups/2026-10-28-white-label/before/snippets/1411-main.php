<?php
/**
 * Axiom Form Protection
 * Cloudflare Turnstile + light rate limiting for the Get Started form (Jetpack form on page 1095).
 *
 * - Hooks Jetpack's own spam check (`jetpack_contact_form_is_spam`). Returning true saves the entry as spam
 *   (no email, not synced to GHL, no Ads conversion); a WP_Error rejects the submission so the visitor can retry.
 * - Modes: "log" (default) records what would happen and never changes the outcome; "enforce" applies the rules.
 *   Enforcement is switched on only from Tools > Axiom Form Protection or the admin REST route, with confirmation.
 * - Keys live in the site configuration file: AXIOM_TURNSTILE_SITE_KEY (public) and AXIOM_TURNSTILE_SECRET (server only; never
 *   output, stored or logged). Without keys the widget isn't shown and nothing is ever blocked.
 * - Cloudflare unreachable or misconfigured: fail open (submission accepted, result logged).
 * - Logs hold no names, emails, phones, tokens or raw IPs (IP and identity counters use salted hashes).
 * Rollback: unpublish this snippet; the form behaves exactly as before.
 */
namespace AngieSnippets\AxiomFormProtection;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const FORM_PAGE  = 1095; // contact-form-id posted by the Get Started form.
const OPT        = 'axiom_form_protection';
const LOG_OPT    = 'axiom_form_protection_log';
const META       = '_axiom_form_protection';
const VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
const API_JS     = 'https://challenges.cloudflare.com/turnstile/v0/api.js';
const ACTION     = 'get-started';
const IP_LIMIT   = 10;   // submissions per IP per IP_WINDOW (high: offices and mobile carriers share IPs).
const IP_WINDOW  = 600;
const ID_LIMIT   = 3;    // submissions per email or phone per ID_WINDOW.
const ID_WINDOW  = 3600;
const LOG_MAX    = 200;
const ALERT_TO   = 'axiom.systems.co@gmail.com';
const MESSAGE    = 'Please confirm you are not a robot and try again. You can also call us at (727) 591-7527.';

function site_key() {
	return defined( 'AXIOM_TURNSTILE_SITE_KEY' ) ? trim( (string) AXIOM_TURNSTILE_SITE_KEY ) : '';
}

function secret() {
	return defined( 'AXIOM_TURNSTILE_SECRET' ) ? trim( (string) AXIOM_TURNSTILE_SECRET ) : '';
}

function configured() {
	return '' !== site_key() && '' !== secret();
}

function mode() {
	$s = get_option( OPT, array() );
	return is_array( $s ) && isset( $s['mode'] ) && 'enforce' === $s['mode'] && configured() ? 'enforce' : 'log';
}

/* ------------------------------------------------------------ widget */

function script() {
	// Single-use tokens: after a failed submission, get a fresh token so the visitor can retry.
	return '<script src="' . esc_url( API_JS ) . '" async defer></script>'
		. '<script id="axfp-js">(function(){if(!window.fetch||window.axfpWrapped)return;window.axfpWrapped=1;var of=window.fetch;'
		. 'window.fetch=function(i,o){var p=of.apply(this,arguments);try{var u=typeof i==="string"?i:(i&&i.url)||"";'
		. 'if(u.indexOf("action=grunion-contact-form")!==-1){p.then(function(r){if(!r.ok&&window.turnstile){var w=document.querySelector(".axfp-turnstile");'
		. 'try{if(w)window.turnstile.reset(w);}catch(e){}}}).catch(function(){});}}catch(e){}return p;};})();</script>';
}

function add_widget( $content ) {
	if ( ! is_string( $content ) || '' === site_key() || false !== strpos( $content, 'axfp-turnstile' ) ) {
		return $content;
	}
	$form = strpos( $content, 'class="axgs"' );
	if ( false === $form ) {
		return $content;
	}
	$pos = strpos( $content, '<div class="wp-block-jetpack-button', $form );
	if ( false === $pos ) {
		return $content;
	}
	$widget = '<div class="axfp-turnstile cf-turnstile" style="margin:0 0 4px" data-sitekey="' . esc_attr( site_key() )
		. '" data-action="' . ACTION . '" data-appearance="interaction-only" data-size="flexible"></div>';
	return substr_replace( $content, $widget, $pos, 0 ) . script();
}
// After snippet 1099 has rendered the form (priority 20 / 999).
add_filter( 'elementor/frontend/the_content', __NAMESPACE__ . '\\add_widget', 25 );
add_filter( 'the_content', __NAMESPACE__ . '\\add_widget', 1000 );

/* ------------------------------------------------------------ checks */

function is_our_form() {
	// phpcs:ignore WordPress.Security.NonceVerification.Missing -- read-only check inside Jetpack's own (JWT-signed) submission.
	return isset( $_POST['contact-form-id'] ) && FORM_PAGE === (int) $_POST['contact-form-id'];
}

function client_ip() {
	// Same source Jetpack uses for the entry's IP.
	return isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
}

function hash_value( $v ) {
	return hash_hmac( 'sha256', (string) $v, wp_salt( 'nonce' ) );
}

/** Verifies the token with Cloudflare (server-side, single call). Never logs the token or secret. */
function turnstile( $token ) {
	if ( '' === secret() ) {
		return array( 'result' => 'not-configured', 'codes' => array() );
	}
	if ( '' === $token ) {
		return array( 'result' => 'missing', 'codes' => array() );
	}
	$resp = wp_remote_post(
		VERIFY_URL,
		array(
			'timeout' => 5,
			'body'    => array(
				'secret'          => secret(),
				'response'        => $token,
				'idempotency_key' => wp_generate_uuid4(),
			),
		)
	);
	if ( is_wp_error( $resp ) ) {
		return array( 'result' => 'unavailable', 'codes' => array( 'connection-error' ) );
	}
	$code = (int) wp_remote_retrieve_response_code( $resp );
	$json = json_decode( (string) wp_remote_retrieve_body( $resp ), true );
	if ( $code >= 500 || ! is_array( $json ) ) {
		return array( 'result' => 'unavailable', 'codes' => array( 'http-' . $code ) );
	}
	$codes = isset( $json['error-codes'] ) && is_array( $json['error-codes'] ) ? array_values( array_map( 'sanitize_key', $json['error-codes'] ) ) : array();
	if ( ! empty( $json['success'] ) ) {
		$host = strtolower( (string) wp_parse_url( home_url(), PHP_URL_HOST ) );
		if ( ! empty( $json['hostname'] ) && strtolower( (string) $json['hostname'] ) !== $host ) {
			return array( 'result' => 'invalid', 'codes' => array( 'hostname-mismatch' ) );
		}
		if ( ! empty( $json['action'] ) && ACTION !== $json['action'] ) {
			return array( 'result' => 'invalid', 'codes' => array( 'action-mismatch' ) );
		}
		return array( 'result' => 'pass', 'codes' => array() );
	}
	// Our own configuration or Cloudflare problems must never block real visitors.
	if ( array_intersect( $codes, array( 'missing-input-secret', 'invalid-input-secret', 'internal-error', 'bad-request' ) ) ) {
		return array( 'result' => 'unavailable', 'codes' => $codes );
	}
	return array( 'result' => 'invalid', 'codes' => $codes ? $codes : array( 'not-successful' ) );
}

/** Fixed-window counter in a transient. */
function bump( $key, $window ) {
	$now = time();
	$v   = get_transient( $key );
	if ( ! is_array( $v ) || (int) $v[1] + $window <= $now ) {
		$v = array( 0, $now );
	}
	$v[0] = (int) $v[0] + 1;
	set_transient( $key, $v, max( 1, (int) $v[1] + $window - $now ) );
	return $v[0];
}

/** Hashed email and phone of this submission (field names end in -email / -phone). */
function identities() {
	$ids = array();
	// phpcs:ignore WordPress.Security.NonceVerification.Missing
	foreach ( (array) $_POST as $name => $value ) {
		if ( ! is_string( $value ) || ! is_string( $name ) ) {
			continue;
		}
		if ( preg_match( '/-email$/', $name ) && '' !== trim( $value ) ) {
			$ids[] = 'e' . hash_value( strtolower( trim( wp_unslash( $value ) ) ) );
		} elseif ( preg_match( '/-phone$/', $name ) ) {
			$digits = substr( preg_replace( '/\D+/', '', $value ), -10 );
			if ( strlen( $digits ) >= 7 ) {
				$ids[] = 'p' . hash_value( $digits );
			}
		}
	}
	return $ids;
}

function decide( $r ) {
	if ( in_array( $r['turnstile'], array( 'missing', 'invalid' ), true ) ) {
		$d = 'reject';
	} elseif ( $r['rate_limited'] ) {
		$d = 'flag-spam';
	} elseif ( 'pass' === $r['turnstile'] ) {
		$d = 'allow';
	} else {
		$d = 'allow-fail-open';
	}
	return ( 'enforce' === $r['mode'] || 0 === strpos( $d, 'allow' ) ) ? $d : 'would-' . $d;
}

function evaluate() {
	// phpcs:ignore WordPress.Security.NonceVerification.Missing
	$token = isset( $_POST['cf-turnstile-response'] ) ? sanitize_text_field( wp_unslash( $_POST['cf-turnstile-response'] ) ) : '';
	$ip    = client_ip();
	$ts    = turnstile( $token );
	$ipn   = '' !== $ip ? bump( 'axfp_i' . substr( hash_value( $ip ), 0, 32 ), IP_WINDOW ) : 0;
	$idn   = 0;
	foreach ( identities() as $id ) {
		$idn = max( $idn, bump( 'axfp_' . substr( $id, 0, 33 ), ID_WINDOW ) );
	}
	// phpcs:ignore WordPress.Security.NonceVerification.Missing
	$fill = isset( $_POST['jetpack_form_fill_duration'] ) && '' !== $_POST['jetpack_form_fill_duration'] ? (int) $_POST['jetpack_form_fill_duration'] : null;
	$r    = array(
		'time'         => time(),
		'mode'         => mode(),
		'turnstile'    => $ts['result'],
		'codes'        => $ts['codes'],
		'ip_count'     => $ipn,
		'id_count'     => $idn,
		'rate_limited' => $ipn > IP_LIMIT || $idn > ID_LIMIT,
		'fill_seconds' => $fill,
		'ip_ref'       => '' !== $ip ? substr( hash_value( $ip ), 0, 8 ) : '',
	);
	$r['decision'] = decide( $r );
	return $r;
}

function log_event( $r ) {
	$log   = get_option( LOG_OPT, array() );
	$log   = is_array( $log ) ? $log : array();
	$log[] = $r;
	update_option( LOG_OPT, array_slice( $log, -LOG_MAX ), false );
}

function last( $set = null ) {
	static $r = null;
	if ( null !== $set ) {
		$r = $set;
	}
	return $r;
}

function check( $is_spam, $form = array() ) {
	if ( true === $is_spam || is_wp_error( $is_spam ) || ! is_our_form() ) {
		return $is_spam;
	}
	try {
		$r = evaluate();
		last( $r );
		if ( 'reject' === $r['decision'] ) {
			$r['entry'] = null;
			log_event( $r );
			return new \WP_Error( 'axiom_form_protection', MESSAGE );
		}
		if ( 'flag-spam' === $r['decision'] ) {
			return true;
		}
	} catch ( \Throwable $e ) {
		unset( $e ); // Never break the form.
	}
	return $is_spam;
}
// Before Jetpack's blocklist and Akismet checks (priority 10).
add_filter( 'jetpack_contact_form_is_spam', __NAMESPACE__ . '\\check', 5, 2 );

// Attach the result to the saved entry (runs before the GHL sync hook at priority 20).
add_action(
	'grunion_after_feedback_post_inserted',
	function ( $post_id ) {
		try {
			$r = last();
			if ( is_array( $r ) ) {
				$r['entry'] = (int) $post_id;
				update_post_meta( (int) $post_id, META, $r );
				log_event( $r );
				last( false );
				if ( 'flag-spam' === $r['decision'] ) {
					// A real customer must never be lost silently: the entry is kept under Feedback > Spam.
					wp_mail(
						ALERT_TO,
						'Get Started entry held by rate limiting',
						'Entry #' . (int) $post_id . " was saved as spam because of the submission rate limit.\n"
						. "If it is a real customer, open Feedback > Spam and mark it as not spam.\n"
						. admin_url( 'edit.php?post_type=feedback&post_status=spam' ) . "\n"
					);
				}
			}
		} catch ( \Throwable $e ) {
			unset( $e );
		}
	},
	5,
	1
);

/* ------------------------------------------------------------ admin status (no secrets) */

function status() {
	$log    = get_option( LOG_OPT, array() );
	$log    = is_array( $log ) ? $log : array();
	$since  = time() - 7 * DAY_IN_SECONDS;
	$counts = array();
	foreach ( $log as $e ) {
		if ( isset( $e['time'] ) && $e['time'] >= $since ) {
			$k            = $e['turnstile'] . ' / ' . $e['decision'];
			$counts[ $k ] = isset( $counts[ $k ] ) ? $counts[ $k ] + 1 : 1;
		}
	}
	return array(
		'mode'            => mode(),
		'site_key_set'    => '' !== site_key(),
		'secret_set'      => '' !== secret(),
		'limits'          => array( 'ip' => IP_LIMIT . ' per ' . IP_WINDOW . 's', 'email_or_phone' => ID_LIMIT . ' per ' . ID_WINDOW . 's' ),
		'last_7_days'     => $counts,
		'recent'          => array_slice( array_reverse( $log ), 0, 50 ),
		// Diagnostic for the person viewing: is REMOTE_ADDR the visitor (same as Cloudflare's header)?
		'your_request_ip' => array(
			'remote_addr_set'         => '' !== client_ip(),
			'cf_connecting_ip_set'    => isset( $_SERVER['HTTP_CF_CONNECTING_IP'] ),
			'remote_addr_equals_cf'   => isset( $_SERVER['HTTP_CF_CONNECTING_IP'] ) && client_ip() === sanitize_text_field( wp_unslash( $_SERVER['HTTP_CF_CONNECTING_IP'] ) ),
			'x_forwarded_for_set'     => isset( $_SERVER['HTTP_X_FORWARDED_FOR'] ),
		),
	);
}

function set_mode( $mode, $confirmed ) {
	if ( 'enforce' === $mode && ( ! $confirmed || ! configured() ) ) {
		return new \WP_Error( 'axiom_mode', 'Enforcement needs both Turnstile keys and explicit confirmation.', array( 'status' => 400 ) );
	}
	if ( ! in_array( $mode, array( 'log', 'enforce' ), true ) ) {
		return new \WP_Error( 'axiom_mode', 'Mode must be log or enforce.', array( 'status' => 400 ) );
	}
	update_option( OPT, array( 'mode' => $mode, 'changed' => time(), 'by' => get_current_user_id() ), false );
	return status();
}

add_action(
	'rest_api_init',
	function () {
		register_rest_route(
			'axiom/v1',
			'/form-protection',
			array(
				array(
					'methods'             => 'GET',
					'permission_callback' => function () {
						return current_user_can( 'manage_options' );
					},
					'callback'            => function () {
						$r = rest_ensure_response( status() );
						$r->header( 'Cache-Control', 'no-store' );
						return $r;
					},
				),
				array(
					'methods'             => 'POST',
					'permission_callback' => function () {
						return current_user_can( 'manage_options' );
					},
					'callback'            => function ( $request ) {
						return rest_ensure_response( set_mode( (string) $request['mode'], 'enforcement-approved' === $request['confirm'] ) );
					},
				),
			)
		);
	}
);

add_action(
	'admin_menu',
	function () {
		add_management_page( 'Axiom Form Protection', 'Axiom Form Protection', 'manage_options', 'axiom-form-protection', __NAMESPACE__ . '\\admin_page' );
	}
);

function admin_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$notice = '';
	if ( isset( $_POST['axfp_mode'] ) && check_admin_referer( 'axfp_mode' ) ) {
		$r      = set_mode( sanitize_key( wp_unslash( $_POST['axfp_mode'] ) ), ! empty( $_POST['axfp_confirm'] ) );
		$notice = is_wp_error( $r ) ? $r->get_error_message() : 'Mode saved.';
	}
	$s = status();
	echo '<div class="wrap"><h1>Axiom Form Protection</h1>';
	if ( $notice ) {
		echo '<div class="notice notice-info"><p>' . esc_html( $notice ) . '</p></div>';
	}
	echo '<p>Mode: <strong>' . esc_html( $s['mode'] ) . '</strong> · Site key: ' . ( $s['site_key_set'] ? 'set' : 'missing' ) . ' · Secret: ' . ( $s['secret_set'] ? 'set' : 'missing' ) . '</p>';
	echo '<form method="post">';
	wp_nonce_field( 'axfp_mode' );
	echo '<select name="axfp_mode"><option value="log"' . selected( $s['mode'], 'log', false ) . '>Log only</option><option value="enforce"' . selected( $s['mode'], 'enforce', false ) . '>Enforce</option></select> ';
	echo '<label><input type="checkbox" name="axfp_confirm" value="1"> Enforcement is approved</label> <button class="button button-primary">Save</button></form>';
	echo '<h2>Last 7 days</h2><pre>' . esc_html( wp_json_encode( $s['last_7_days'], JSON_PRETTY_PRINT ) ) . '</pre>';
	echo '<h2>Recent submissions</h2><pre style="max-height:400px;overflow:auto;background:#fff;padding:8px">' . esc_html( wp_json_encode( $s['recent'], JSON_PRETTY_PRINT ) ) . '</pre></div>';
}
