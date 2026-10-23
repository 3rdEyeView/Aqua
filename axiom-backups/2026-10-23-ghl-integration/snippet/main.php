<?php
/**
 * Axiom CRM Sync (GoHighLevel)
 * Sends saved, non-spam Get Started form entries (Jetpack form 1096) to the
 * Axiom GoHighLevel sub-account: contact upsert (email/phone), one note per
 * entry, then the axiom-new-lead tag that starts the existing workflow.
 *
 * - The submission hook only saves a field snapshot and queues a background
 *   job (Action Scheduler); no API call happens in the visitor's request.
 * - The Jetpack entry, the Gmail notification and Google Ads tracking are not
 *   touched. If the CRM is unreachable, the job retries, then emails an alert.
 * - Token: AXIOM_GHL_PRIVATE_TOKEN (site configuration file). Only placed in the
 *   Authorization header of server-side requests; never stored, shown or logged.
 * - Modes (Tools > Axiom CRM Sync): off, dry-run (default: builds the payload,
 *   no GoHighLevel requests), test (writes only for listed test emails, with a
 *   test tag), live. Verification makes GET requests only. Write requests are
 *   refused unless the mode is test or live.
 * Rollback: unpublish this snippet. Entries keep their sync status meta.
 */
namespace AngieSnippets\AxiomCrmSync_1398;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const FORM_ID          = 1096;
const DEFAULT_LOCATION = 'WSbB7bUher6I1M2VNlZz';
const API_BASE         = 'https://services.leadconnectorhq.com';
const API_VERSION      = '2021-07-28';
const LEAD_TAG         = 'axiom-new-lead';
const TEST_TAG         = 'axiom-integration-test';
const PIPELINE_NAME    = 'AXIOM Standard Client Pipeline';
const STAGE_NAME       = 'New Lead';
const ALERT_TO         = 'axiom.systems.co@gmail.com';
const SOURCE           = 'Website: Get Started form';
const OPT              = 'axiom_ghl_sync_settings';
const META_STATE       = '_axiom_ghl_state';
const META_SNAPSHOT    = '_axiom_ghl_snapshot';
const META_LOCK        = '_axiom_ghl_lock';
const JOB              = 'axiom_ghl_sync_entry';
const CHECK_JOB        = 'axiom_ghl_check_opportunity';
const GROUP            = 'axiom-ghl';
const RETRY_DELAYS     = array( 60, 300, 1800, 7200, 43200 );

/* ------------------------------------------------------------ settings */

function defaults() {
	return array(
		'mode'             => 'dry-run',
		'location_id'      => defined( 'AXIOM_GHL_LOCATION_ID' ) ? AXIOM_GHL_LOCATION_ID : DEFAULT_LOCATION,
		'pipeline_id'      => '',
		'stage_id'         => '',
		'opportunity_mode' => 'workflow',
		'field_message'    => '',
		'field_plan'       => '',
		'test_emails'      => '',
		'verified'         => array(),
	);
}

function settings() {
	$s = get_option( OPT, array() );
	return array_merge( defaults(), is_array( $s ) ? $s : array() );
}

function save_settings( $changes ) {
	$s = array_merge( settings(), $changes );
	if ( ! in_array( $s['mode'], array( 'off', 'dry-run', 'test', 'live' ), true ) ) {
		$s['mode'] = 'dry-run';
	}
	if ( ! in_array( $s['opportunity_mode'], array( 'workflow', 'api' ), true ) ) {
		$s['opportunity_mode'] = 'workflow';
	}
	update_option( OPT, $s, false );
	return $s;
}

function token() {
	return defined( 'AXIOM_GHL_PRIVATE_TOKEN' ) ? (string) AXIOM_GHL_PRIVATE_TOKEN : '';
}

function test_emails() {
	$list = preg_split( '/[\s,]+/', strtolower( (string) settings()['test_emails'] ) );
	return array_values( array_filter( array_map( 'trim', $list ) ) );
}

/* ------------------------------------------------------------ capture */

/**
 * Field label => value. Labels are the form's own labels (Name, Email, ...).
 */
function snapshot_from_fields( $fields ) {
	$out = array();
	foreach ( (array) $fields as $field ) {
		if ( ! is_object( $field ) ) {
			continue;
		}
		$label = method_exists( $field, 'get_attribute' ) ? (string) $field->get_attribute( 'label' ) : '';
		$vars  = get_object_vars( $field ); // public properties only; never throws
		$value = isset( $vars['value'] ) ? $vars['value'] : '';
		if ( is_array( $value ) ) {
			$value = implode( ', ', $value );
		}
		if ( '' !== $label ) {
			$out[ $label ] = trim( (string) $value );
		}
	}
	return $out;
}

/** Jetpack's email values are keyed "1_Name", "2_Business name", ... */
function snapshot_from_values( $values ) {
	$out = array();
	foreach ( (array) $values as $key => $value ) {
		if ( preg_match( '/^\d+_(.+)$/', (string) $key, $m ) && ! is_array( $value ) ) {
			$out[ $m[1] ] = trim( (string) $value );
		}
	}
	return $out;
}

function is_form_entry( $post_id ) {
	$post = get_post( $post_id );
	return $post && 'feedback' === $post->post_type && FORM_ID === (int) $post->post_parent;
}

function get_state( $post_id ) {
	$s = get_post_meta( $post_id, META_STATE, true );
	return is_array( $s ) ? $s : array();
}

function set_state( $post_id, $changes, $event = '' ) {
	$s            = array_merge( get_state( $post_id ), $changes );
	$s['updated'] = time();
	if ( $event ) {
		$s['history']   = isset( $s['history'] ) ? array_slice( $s['history'], -14 ) : array();
		$s['history'][] = gmdate( 'Y-m-d H:i:s' ) . ' ' . $event;
	}
	update_post_meta( $post_id, META_STATE, $s );
	return $s;
}

// Saved entry: snapshot + queue. Runs inside Jetpack's submission request, so
// it only writes post meta and inserts a queued job.
add_action(
	'grunion_after_feedback_post_inserted',
	function ( $post_id, $fields = array(), $is_spam = false ) {
		try {
			$post_id = (int) $post_id;
			if ( $is_spam || ! is_form_entry( $post_id ) || 'publish' !== get_post_status( $post_id ) ) {
				return;
			}
			try {
				$snap = snapshot_from_fields( $fields );
				if ( $snap ) {
					update_post_meta( $post_id, META_SNAPSHOT, $snap );
				}
			} catch ( \Throwable $e ) {
				// The grunion_pre_message_sent fallback below fills the snapshot.
				unset( $e );
			}
			$mode = settings()['mode'];
			if ( 'off' === $mode ) {
				set_state( $post_id, array( 'status' => 'held' ), 'saved while sync was off' );
				return;
			}
			set_state( $post_id, array( 'status' => 'queued', 'attempts' => 0 ), 'queued (' . $mode . ')' );
			queue( $post_id, 0 );
		} catch ( \Throwable $e ) {
			// Never interfere with the form submission.
			return;
		}
	},
	20,
	3
);

// Fallback field capture from the values Jetpack uses for its email.
add_action(
	'grunion_pre_message_sent',
	function ( $post_id, $all_values = array() ) {
		try {
			$post_id = (int) $post_id;
			if ( ! is_form_entry( $post_id ) ) {
				return;
			}
			$have = get_post_meta( $post_id, META_SNAPSHOT, true );
			$from = snapshot_from_values( $all_values );
			if ( $from && ( ! is_array( $have ) || ! array_filter( $have ) ) ) {
				update_post_meta( $post_id, META_SNAPSHOT, $from );
			} elseif ( $from && is_array( $have ) ) {
				foreach ( $from as $k => $v ) {
					if ( ( ! isset( $have[ $k ] ) || '' === $have[ $k ] ) && '' !== $v ) {
						$have[ $k ] = $v;
					}
				}
				update_post_meta( $post_id, META_SNAPSHOT, $have );
			}
		} catch ( \Throwable $e ) {
			return;
		}
	},
	5,
	2
);

function queue( $post_id, $delay ) {
	if ( ! function_exists( 'as_enqueue_async_action' ) ) {
		// WooCommerce/Action Scheduler missing: fall back to WP-Cron.
		wp_schedule_single_event( time() + max( 30, $delay ), JOB, array( $post_id ) );
		return;
	}
	if ( $delay > 0 ) {
		as_schedule_single_action( time() + $delay, JOB, array( $post_id ), GROUP );
	} else {
		as_enqueue_async_action( JOB, array( $post_id ), GROUP, true );
	}
}

/* ------------------------------------------------------------ payload */

function field( $snap, $label ) {
	return isset( $snap[ $label ] ) ? trim( (string) $snap[ $label ] ) : '';
}

function normalize_phone( $raw ) {
	$raw    = trim( (string) $raw );
	$digits = preg_replace( '/\D+/', '', $raw );
	if ( '' === $digits ) {
		return '';
	}
	if ( 10 === strlen( $digits ) ) {
		return '+1' . $digits;
	}
	if ( 11 === strlen( $digits ) && '1' === $digits[0] ) {
		return '+' . $digits;
	}
	return 0 === strpos( $raw, '+' ) ? '+' . $digits : $digits;
}

/** Contact fields for the upsert; empty values are left out so nothing is blanked. */
function build_contact( $snap, $s ) {
	$name  = preg_replace( '/\s+/', ' ', field( $snap, 'Name' ) );
	$parts = '' === $name ? array() : explode( ' ', $name, 2 );
	$email = strtolower( field( $snap, 'Email' ) );
	$site  = field( $snap, 'Current website' );
	if ( '' !== $site && ! preg_match( '#^https?://#i', $site ) ) {
		$site = 'https://' . $site;
	}
	$c = array(
		'locationId'  => $s['location_id'],
		'name'        => $name,
		'firstName'   => isset( $parts[0] ) ? $parts[0] : '',
		'lastName'    => isset( $parts[1] ) ? $parts[1] : '',
		'email'       => is_email( $email ) ? $email : '',
		'phone'       => normalize_phone( field( $snap, 'Phone' ) ),
		'companyName' => field( $snap, 'Business name' ),
		'website'     => '' !== $site ? esc_url_raw( $site ) : '',
		'source'      => SOURCE,
	);
	$custom = array();
	if ( $s['field_message'] && '' !== field( $snap, 'Tell us about your business' ) ) {
		$custom[] = array( 'id' => $s['field_message'], 'field_value' => field( $snap, 'Tell us about your business' ) );
	}
	if ( $s['field_plan'] && '' !== field( $snap, 'Plan interest' ) ) {
		$custom[] = array( 'id' => $s['field_plan'], 'field_value' => field( $snap, 'Plan interest' ) );
	}
	if ( $custom ) {
		$c['customFields'] = $custom;
	}
	return array_filter(
		$c,
		function ( $v ) {
			return '' !== $v && array() !== $v;
		}
	);
}

function note_marker( $post_id ) {
	return 'Axiom website entry #' . (int) $post_id;
}

function build_note( $post_id, $snap ) {
	$lines = array( 'New Get Started form submission (' . note_marker( $post_id ) . ')', '' );
	foreach ( array( 'Name', 'Business name', 'Email', 'Phone', 'Current website', 'Plan interest', 'Tell us about your business' ) as $label ) {
		$v = field( $snap, $label );
		if ( '' !== $v ) {
			$lines[] = $label . ': ' . $v;
		}
	}
	$post = get_post( $post_id );
	if ( $post ) {
		$lines[] = 'Submitted: ' . get_post_time( 'Y-m-d H:i', true, $post ) . ' UTC';
	}
	return implode( "\n", $lines );
}

/** Summary for dry-run/status screens: which fields would be sent, never their values. */
function preview( $post_id, $snap, $s ) {
	$c = build_contact( $snap, $s );
	unset( $c['locationId'] );
	$fields = array_keys( $c );
	if ( isset( $c['customFields'] ) ) {
		$fields = array_diff( $fields, array( 'customFields' ) );
		foreach ( $c['customFields'] as $cf ) {
			$fields[] = 'custom:' . $cf['id'];
		}
	}
	return array(
		'contact_fields' => array_values( $fields ),
		'note_chars'     => strlen( build_note( $post_id, $snap ) ),
		'tag'            => 'test' === $s['mode'] ? TEST_TAG : LEAD_TAG,
		'opportunity'    => $s['opportunity_mode'],
	);
}

/* ------------------------------------------------------------ API */

/**
 * The only place that talks to GoHighLevel. Non-GET requests are refused
 * unless $allow_write is true (set only by the delivery job in test/live mode).
 */
function api( $method, $path, $body = null, $allow_write = false ) {
	$method = strtoupper( $method );
	if ( 'GET' !== $method && ! $allow_write ) {
		return new \WP_Error( 'axiom_write_blocked', 'Write request blocked in this mode.' );
	}
	if ( '' === token() ) {
		return new \WP_Error( 'axiom_no_token', 'AXIOM_GHL_PRIVATE_TOKEN is not defined.' );
	}
	$args = array(
		'method'      => $method,
		'timeout'     => 15,
		'redirection' => 0,
		'headers'     => array(
			'Authorization' => 'Bearer ' . token(),
			'Version'       => API_VERSION,
			'Accept'        => 'application/json',
		),
	);
	if ( null !== $body ) {
		$args['headers']['Content-Type'] = 'application/json';
		$args['body']                    = wp_json_encode( $body );
	}
	$resp = wp_remote_request( API_BASE . $path, $args );
	if ( is_wp_error( $resp ) ) {
		return new \WP_Error( 'axiom_http', 'Connection error: ' . $resp->get_error_message(), array( 'retry' => true ) );
	}
	$code = (int) wp_remote_retrieve_response_code( $resp );
	$json = json_decode( wp_remote_retrieve_body( $resp ), true );
	if ( $code >= 200 && $code < 300 ) {
		return is_array( $json ) ? $json : array();
	}
	$msg = is_array( $json ) && isset( $json['message'] ) ? ( is_array( $json['message'] ) ? implode( '; ', $json['message'] ) : $json['message'] ) : 'HTTP ' . $code;
	return new \WP_Error(
		'axiom_api_' . $code,
		'HTTP ' . $code . ': ' . substr( sanitize_text_field( (string) $msg ), 0, 200 ),
		array( 'retry' => ( 429 === $code || $code >= 500 ), 'code' => $code )
	);
}

/* ------------------------------------------------------------ delivery job */

add_action( JOB, __NAMESPACE__ . '\\process', 10, 1 );

function process( $post_id ) {
	$post_id = (int) $post_id;
	if ( ! is_form_entry( $post_id ) || 'publish' !== get_post_status( $post_id ) ) {
		return;
	}
	$state = get_state( $post_id );
	if ( isset( $state['status'] ) && in_array( $state['status'], array( 'sent', 'skipped' ), true ) ) {
		return;
	}
	// One worker per entry; a stale lock (crashed run) expires after 10 minutes.
	if ( ! add_post_meta( $post_id, META_LOCK, time(), true ) ) {
		$since = (int) get_post_meta( $post_id, META_LOCK, true );
		if ( time() - $since < 600 ) {
			return;
		}
		update_post_meta( $post_id, META_LOCK, time() );
	}
	try {
		deliver( $post_id );
	} catch ( \Throwable $e ) {
		fail_or_retry( $post_id, new \WP_Error( 'axiom_exception', get_class( $e ) . ': ' . substr( $e->getMessage(), 0, 200 ), array( 'retry' => true ) ) );
	} finally {
		delete_post_meta( $post_id, META_LOCK );
	}
}

function deliver( $post_id ) {
	$s    = settings();
	$snap = get_post_meta( $post_id, META_SNAPSHOT, true );
	if ( ! is_array( $snap ) || ! array_filter( $snap ) ) {
		fail_or_retry( $post_id, new \WP_Error( 'axiom_no_data', 'No field data captured for this entry.', array( 'retry' => false ) ) );
		return;
	}
	$contact = build_contact( $snap, $s );
	if ( empty( $contact['email'] ) && empty( $contact['phone'] ) ) {
		set_state( $post_id, array( 'status' => 'skipped' ), 'skipped: no valid email or phone' );
		return;
	}
	$mode = $s['mode'];
	if ( 'dry-run' === $mode ) {
		set_state( $post_id, array( 'status' => 'dry-run', 'preview' => preview( $post_id, $snap, $s ) ), 'dry-run: payload built, nothing sent' );
		return;
	}
	if ( 'off' === $mode ) {
		set_state( $post_id, array( 'status' => 'held' ), 'held: sync is off' );
		return;
	}
	if ( 'test' === $mode && ! in_array( isset( $contact['email'] ) ? $contact['email'] : '', test_emails(), true ) ) {
		set_state( $post_id, array( 'status' => 'held' ), 'held: test mode, not a listed test email' );
		return;
	}
	if ( '' === token() ) {
		set_state( $post_id, array( 'status' => 'held', 'last_error' => 'Token not configured' ), 'held: token not configured' );
		return;
	}
	$state = set_state( $post_id, array( 'status' => 'sending', 'mode' => $mode ) );
	$tag   = 'test' === $mode ? TEST_TAG : LEAD_TAG;

	// 1. Contact upsert (GoHighLevel matches on email/phone per the location's duplicate settings).
	if ( empty( $state['contact_id'] ) ) {
		$r = api( 'POST', '/contacts/upsert', $contact, true );
		if ( is_wp_error( $r ) ) {
			return fail_or_retry( $post_id, $r );
		}
		$id = isset( $r['contact']['id'] ) ? (string) $r['contact']['id'] : '';
		if ( '' === $id ) {
			return fail_or_retry( $post_id, new \WP_Error( 'axiom_no_contact', 'Upsert returned no contact ID.', array( 'retry' => true ) ) );
		}
		$state = set_state( $post_id, array( 'contact_id' => $id, 'contact_new' => ! empty( $r['new'] ) ), ( ! empty( $r['new'] ) ? 'contact created ' : 'contact updated ' ) . $id );
	}
	$cid = rawurlencode( $state['contact_id'] );

	// 2. One note per entry. If an earlier attempt may have created it, look first.
	if ( empty( $state['note_id'] ) ) {
		if ( ! empty( $state['note_attempted'] ) ) {
			$existing = api( 'GET', '/contacts/' . $cid . '/notes' );
			if ( is_wp_error( $existing ) ) {
				return fail_or_retry( $post_id, $existing );
			}
			foreach ( isset( $existing['notes'] ) ? $existing['notes'] : array() as $n ) {
				if ( isset( $n['body'] ) && false !== strpos( $n['body'], note_marker( $post_id ) ) ) {
					$state = set_state( $post_id, array( 'note_id' => (string) $n['id'] ), 'note found from earlier attempt' );
					break;
				}
			}
		}
		if ( empty( $state['note_id'] ) ) {
			$state = set_state( $post_id, array( 'note_attempted' => true ) );
			$r     = api( 'POST', '/contacts/' . $cid . '/notes', array( 'body' => build_note( $post_id, $snap ) ), true );
			if ( is_wp_error( $r ) ) {
				return fail_or_retry( $post_id, $r );
			}
			$nid   = isset( $r['note']['id'] ) ? (string) $r['note']['id'] : 'created';
			$state = set_state( $post_id, array( 'note_id' => $nid ), 'note added' );
		}
	}

	// 3. Opportunity via API only if chosen; default leaves it to the workflow.
	if ( 'api' === $s['opportunity_mode'] && empty( $state['opportunity_id'] ) && 'live' === $mode ) {
		$opp = ensure_opportunity( $state['contact_id'], $snap, $s );
		if ( is_wp_error( $opp ) ) {
			return fail_or_retry( $post_id, $opp );
		}
		$state = set_state( $post_id, array( 'opportunity_id' => $opp['id'] ), $opp['created'] ? 'opportunity created ' . $opp['id'] : 'open opportunity already exists ' . $opp['id'] );
	}

	// 4. Tag last, so the workflow starts with the contact and note in place.
	//    Adding a tag the contact already has does not restart a tag-added trigger.
	if ( empty( $state['tagged'] ) ) {
		$r = api( 'POST', '/contacts/' . $cid . '/tags', array( 'tags' => array( $tag ) ), true );
		if ( is_wp_error( $r ) ) {
			return fail_or_retry( $post_id, $r );
		}
		$state = set_state( $post_id, array( 'tagged' => $tag ), 'tag added: ' . $tag );
	}

	set_state( $post_id, array( 'status' => 'sent', 'last_error' => '' ), 'sent' );
	if ( function_exists( 'as_schedule_single_action' ) && $s['pipeline_id'] ) {
		as_schedule_single_action( time() + 300, CHECK_JOB, array( $post_id ), GROUP );
	}
}

/** Finds an open opportunity for the contact in the Axiom pipeline, or creates one at New Lead. */
function ensure_opportunity( $contact_id, $snap, $s ) {
	if ( ! $s['pipeline_id'] || ! $s['stage_id'] ) {
		return new \WP_Error( 'axiom_no_pipeline', 'Pipeline/stage not verified yet.', array( 'retry' => false ) );
	}
	$q = '/opportunities/search?' . http_build_query(
		array(
			'location_id' => $s['location_id'],
			'contact_id'  => $contact_id,
			'pipeline_id' => $s['pipeline_id'],
			'status'      => 'open',
		)
	);
	$r = api( 'GET', $q );
	if ( is_wp_error( $r ) ) {
		return $r;
	}
	if ( ! empty( $r['opportunities'][0]['id'] ) ) {
		return array( 'id' => (string) $r['opportunities'][0]['id'], 'created' => false );
	}
	$name = field( $snap, 'Business name' ) ? field( $snap, 'Business name' ) : field( $snap, 'Name' );
	$r    = api(
		'POST',
		'/opportunities/',
		array(
			'pipelineId'      => $s['pipeline_id'],
			'pipelineStageId' => $s['stage_id'],
			'locationId'      => $s['location_id'],
			'contactId'       => $contact_id,
			'name'            => $name . ' - Website lead',
			'status'          => 'open',
			'source'          => SOURCE,
		),
		true
	);
	if ( is_wp_error( $r ) ) {
		return $r;
	}
	return array( 'id' => isset( $r['opportunity']['id'] ) ? (string) $r['opportunity']['id'] : 'created', 'created' => true );
}

function fail_or_retry( $post_id, $error ) {
	$state    = get_state( $post_id );
	$attempts = isset( $state['attempts'] ) ? (int) $state['attempts'] + 1 : 1;
	$data     = $error->get_error_data();
	$retry    = is_array( $data ) && ! empty( $data['retry'] );
	$msg      = $error->get_error_message();
	if ( $retry && $attempts <= count( RETRY_DELAYS ) ) {
		$delay = RETRY_DELAYS[ $attempts - 1 ];
		set_state( $post_id, array( 'status' => 'retrying', 'attempts' => $attempts, 'last_error' => $msg ), 'attempt ' . $attempts . ' failed, retry in ' . $delay . 's: ' . $msg );
		queue( $post_id, $delay );
		return null;
	}
	set_state( $post_id, array( 'status' => 'failed', 'attempts' => $attempts, 'last_error' => $msg ), 'failed: ' . $msg );
	wp_mail(
		ALERT_TO,
		'Axiom CRM sync failed for a Get Started lead',
		"A Get Started form entry could not be sent to GoHighLevel.\n\n"
		. 'Entry: #' . (int) $post_id . "\n"
		. 'Error: ' . $msg . "\n\n"
		. "The lead is safe: it is saved in WordPress and was emailed as usual.\n"
		. 'Review and retry: ' . admin_url( 'tools.php?page=axiom-crm-sync' ) . "\n"
	);
	return null;
}

// Five minutes after delivery: confirm the contact has an opportunity in the pipeline (read-only).
add_action(
	CHECK_JOB,
	function ( $post_id ) {
		$s     = settings();
		$state = get_state( $post_id );
		if ( empty( $state['contact_id'] ) || ! $s['pipeline_id'] ) {
			return;
		}
		$r = api(
			'GET',
			'/opportunities/search?' . http_build_query(
				array(
					'location_id' => $s['location_id'],
					'contact_id'  => $state['contact_id'],
					'pipeline_id' => $s['pipeline_id'],
				)
			)
		);
		if ( is_wp_error( $r ) ) {
			set_state( $post_id, array( 'opportunity_check' => 'error: ' . $r->get_error_message() ), 'opportunity check error' );
			return;
		}
		$opps  = isset( $r['opportunities'] ) ? $r['opportunities'] : array();
		$open  = array_filter(
			$opps,
			function ( $o ) {
				return isset( $o['status'] ) && 'open' === $o['status'];
			}
		);
		$check = count( $open ) . ' open / ' . count( $opps ) . ' total in pipeline';
		set_state( $post_id, array( 'opportunity_check' => $check ), 'opportunity check: ' . $check );
	},
	10,
	1
);

/* ------------------------------------------------------------ verification (GET only) */

function verify() {
	$s   = settings();
	$loc = rawurlencode( $s['location_id'] );
	$out = array(
		'time'          => gmdate( 'Y-m-d H:i:s' ) . ' UTC',
		'token_defined' => '' !== token(),
		'location_id'   => $s['location_id'],
	);
	$check = function ( $label, $r, $ok ) use ( &$out ) {
		$out['checks'][ $label ] = is_wp_error( $r ) ? array( 'ok' => false, 'error' => $r->get_error_message() ) : array_merge( array( 'ok' => true ), $ok( $r ) );
	};

	$check(
		'location (locations.readonly)',
		api( 'GET', '/locations/' . $loc ),
		function ( $r ) use ( $s ) {
			$l = isset( $r['location'] ) ? $r['location'] : $r;
			return array( 'name' => isset( $l['name'] ) ? $l['name'] : '', 'id_matches' => isset( $l['id'] ) && $l['id'] === $s['location_id'] );
		}
	);
	$check(
		'contacts read (contacts.readonly)',
		api( 'GET', '/contacts/?' . http_build_query( array( 'locationId' => $s['location_id'], 'limit' => 1 ) ) ),
		function () {
			return array();
		}
	);
	$pipeline = null;
	$check(
		'pipelines (opportunities.readonly)',
		api( 'GET', '/opportunities/pipelines?' . http_build_query( array( 'locationId' => $s['location_id'] ) ) ),
		function ( $r ) use ( &$pipeline ) {
			$names = array();
			foreach ( isset( $r['pipelines'] ) ? $r['pipelines'] : array() as $p ) {
				$names[] = $p['name'];
				if ( 0 === strcasecmp( trim( $p['name'] ), PIPELINE_NAME ) ) {
					foreach ( $p['stages'] as $st ) {
						if ( 0 === strcasecmp( trim( $st['name'] ), STAGE_NAME ) ) {
							$pipeline = array( 'pipeline_id' => $p['id'], 'stage_id' => $st['id'] );
						}
					}
					$pipeline = $pipeline ? $pipeline : array( 'pipeline_id' => $p['id'], 'stage_id' => '', 'stages' => wp_list_pluck( $p['stages'], 'name' ) );
				}
			}
			return array( 'pipelines' => $names, 'axiom_pipeline' => $pipeline );
		}
	);
	$check(
		'tags (locations/tags.readonly)',
		api( 'GET', '/locations/' . $loc . '/tags' ),
		function ( $r ) {
			$names = array_map( 'strtolower', wp_list_pluck( isset( $r['tags'] ) ? $r['tags'] : array(), 'name' ) );
			return array( LEAD_TAG . '_exists' => in_array( LEAD_TAG, $names, true ), TEST_TAG . '_exists' => in_array( TEST_TAG, $names, true ), 'tag_count' => count( $names ) );
		}
	);
	$fields = array();
	$check(
		'custom fields (locations/customFields.readonly)',
		api( 'GET', '/locations/' . $loc . '/customFields' ),
		function ( $r ) use ( &$fields ) {
			foreach ( isset( $r['customFields'] ) ? $r['customFields'] : array() as $f ) {
				if ( isset( $f['model'] ) && 'contact' !== $f['model'] ) {
					continue;
				}
				$fields[] = array( 'id' => $f['id'], 'name' => $f['name'], 'key' => isset( $f['fieldKey'] ) ? $f['fieldKey'] : '', 'type' => isset( $f['dataType'] ) ? $f['dataType'] : '' );
			}
			return array( 'contact_fields' => $fields );
		}
	);
	$check(
		'workflows (workflows.readonly)',
		api( 'GET', '/workflows/?' . http_build_query( array( 'locationId' => $s['location_id'] ) ) ),
		function ( $r ) {
			$list = array();
			foreach ( isset( $r['workflows'] ) ? $r['workflows'] : array() as $w ) {
				$list[] = $w['name'] . ' [' . ( isset( $w['status'] ) ? $w['status'] : '?' ) . ']';
			}
			return array( 'workflows' => $list );
		}
	);

	$changes = array( 'verified' => $out );
	if ( $pipeline && ! empty( $pipeline['stage_id'] ) ) {
		$changes['pipeline_id'] = $pipeline['pipeline_id'];
		$changes['stage_id']    = $pipeline['stage_id'];
	}
	save_settings( $changes );
	return $out;
}

/* ------------------------------------------------------------ admin page */

add_action(
	'admin_menu',
	function () {
		add_management_page( 'Axiom CRM Sync', 'Axiom CRM Sync', 'manage_options', 'axiom-crm-sync', __NAMESPACE__ . '\\admin_page' );
	}
);

function recent_entries( $limit = 30 ) {
	return get_posts(
		array(
			'post_type'      => 'feedback',
			'post_status'    => array( 'publish', 'spam' ),
			'post_parent'    => FORM_ID,
			'posts_per_page' => $limit,
			'orderby'        => 'date',
			'order'          => 'DESC',
		)
	);
}

function admin_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$notice = '';
	if ( isset( $_POST['axiom_ghl_action'] ) && check_admin_referer( 'axiom_ghl_sync' ) ) {
		$action = sanitize_key( wp_unslash( $_POST['axiom_ghl_action'] ) );
		if ( 'save' === $action ) {
			$mode = sanitize_key( wp_unslash( isset( $_POST['mode'] ) ? $_POST['mode'] : '' ) );
			if ( 'live' === $mode && empty( $_POST['confirm_live'] ) ) {
				$notice = 'Live mode not saved: tick the confirmation box.';
			} else {
				save_settings(
					array(
						'mode'             => $mode,
						'opportunity_mode' => sanitize_key( wp_unslash( isset( $_POST['opportunity_mode'] ) ? $_POST['opportunity_mode'] : 'workflow' ) ),
						'field_message'    => sanitize_text_field( wp_unslash( isset( $_POST['field_message'] ) ? $_POST['field_message'] : '' ) ),
						'field_plan'       => sanitize_text_field( wp_unslash( isset( $_POST['field_plan'] ) ? $_POST['field_plan'] : '' ) ),
						'test_emails'      => sanitize_textarea_field( wp_unslash( isset( $_POST['test_emails'] ) ? $_POST['test_emails'] : '' ) ),
					)
				);
				$notice = 'Settings saved.';
			}
		} elseif ( 'verify' === $action ) {
			verify();
			$notice = 'Verification finished (read-only requests).';
		} elseif ( 'retry' === $action && ! empty( $_POST['entry'] ) ) {
			$id = (int) $_POST['entry'];
			if ( is_form_entry( $id ) ) {
				set_state( $id, array( 'status' => 'queued', 'attempts' => 0 ), 'manually queued' );
				queue( $id, 0 );
				$notice = 'Entry #' . $id . ' queued.';
			}
		} elseif ( 'send_held' === $action && 'live' === settings()['mode'] ) {
			$n = 0;
			foreach ( recent_entries( 100 ) as $p ) {
				$st = get_state( $p->ID );
				if ( 'publish' === $p->post_status && isset( $st['status'] ) && in_array( $st['status'], array( 'held', 'dry-run' ), true ) ) {
					set_state( $p->ID, array( 'status' => 'queued', 'attempts' => 0 ), 'queued from held' );
					queue( $p->ID, 0 );
					$n++;
				}
			}
			$notice = $n . ' held entries queued.';
		}
	}
	$s = settings();
	echo '<div class="wrap"><h1>Axiom CRM Sync</h1>';
	if ( $notice ) {
		echo '<div class="notice notice-info"><p>' . esc_html( $notice ) . '</p></div>';
	}
	echo '<p>Get Started form (#' . (int) FORM_ID . ') to GoHighLevel. Token configured: <strong>' . ( token() ? 'yes' : 'no' ) . '</strong>. Location: <code>' . esc_html( $s['location_id'] ) . '</code>. Pipeline: <code>' . esc_html( $s['pipeline_id'] ? $s['pipeline_id'] : 'not verified' ) . '</code> / stage <code>' . esc_html( $s['stage_id'] ? $s['stage_id'] : '-' ) . '</code>.</p>';
	echo '<form method="post">';
	wp_nonce_field( 'axiom_ghl_sync' );
	echo '<table class="form-table"><tr><th>Mode</th><td><select name="mode">';
	foreach ( array( 'off' => 'Off', 'dry-run' => 'Dry run (no GoHighLevel requests)', 'test' => 'Test (listed test emails only, test tag)', 'live' => 'Live' ) as $k => $label ) {
		echo '<option value="' . esc_attr( $k ) . '"' . selected( $s['mode'], $k, false ) . '>' . esc_html( $label ) . '</option>';
	}
	echo '</select> <label><input type="checkbox" name="confirm_live" value="1"> I confirm live delivery is approved</label></td></tr>';
	echo '<tr><th>Opportunity</th><td><select name="opportunity_mode"><option value="workflow"' . selected( $s['opportunity_mode'], 'workflow', false ) . '>Created by the GoHighLevel workflow (tag only)</option><option value="api"' . selected( $s['opportunity_mode'], 'api', false ) . '>Created here if the contact has no open one</option></select></td></tr>';
	echo '<tr><th>Custom field ID: message</th><td><input name="field_message" class="regular-text" value="' . esc_attr( $s['field_message'] ) . '"> <span class="description">Empty: message goes in the note only.</span></td></tr>';
	echo '<tr><th>Custom field ID: plan</th><td><input name="field_plan" class="regular-text" value="' . esc_attr( $s['field_plan'] ) . '"></td></tr>';
	echo '<tr><th>Test emails</th><td><textarea name="test_emails" rows="2" class="large-text">' . esc_textarea( $s['test_emails'] ) . '</textarea></td></tr></table>';
	echo '<p><button class="button button-primary" name="axiom_ghl_action" value="save">Save</button> <button class="button" name="axiom_ghl_action" value="verify">Run verification (read-only)</button> ';
	if ( 'live' === $s['mode'] ) {
		echo '<button class="button" name="axiom_ghl_action" value="send_held">Send held entries</button>';
	}
	echo '</p></form>';
	if ( $s['verified'] ) {
		echo '<h2>Last verification</h2><pre style="background:#fff;padding:12px;max-height:320px;overflow:auto">' . esc_html( wp_json_encode( $s['verified'], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES ) ) . '</pre>';
	}
	echo '<h2>Recent entries</h2><table class="widefat striped"><thead><tr><th>Entry</th><th>Date</th><th>Status</th><th>Attempts</th><th>Contact</th><th>Details</th><th></th></tr></thead><tbody>';
	foreach ( recent_entries() as $p ) {
		$st     = get_state( $p->ID );
		$status = 'spam' === $p->post_status ? 'spam (not sent)' : ( isset( $st['status'] ) ? $st['status'] : 'before sync' );
		$link   = ! empty( $st['contact_id'] ) ? 'https://app.axiomsystems.systems/v2/location/' . rawurlencode( $s['location_id'] ) . '/contacts/detail/' . rawurlencode( $st['contact_id'] ) : '';
		echo '<tr><td>#' . (int) $p->ID . '</td><td>' . esc_html( get_the_date( 'Y-m-d H:i', $p ) ) . '</td><td>' . esc_html( $status ) . '</td><td>' . (int) ( isset( $st['attempts'] ) ? $st['attempts'] : 0 ) . '</td><td>' . ( $link ? '<a href="' . esc_url( $link ) . '" target="_blank" rel="noopener">open</a>' : '' ) . '</td><td><details><summary>log</summary><pre>' . esc_html( implode( "\n", isset( $st['history'] ) ? $st['history'] : array() ) ) . ( ! empty( $st['opportunity_check'] ) ? "\nOpportunity: " . esc_html( $st['opportunity_check'] ) : '' ) . '</pre></details></td><td>';
		if ( 'publish' === $p->post_status && isset( $st['status'] ) && in_array( $st['status'], array( 'failed', 'held' ), true ) && in_array( $s['mode'], array( 'test', 'live' ), true ) ) {
			echo '<form method="post" style="margin:0">';
			wp_nonce_field( 'axiom_ghl_sync' );
			echo '<input type="hidden" name="entry" value="' . (int) $p->ID . '"><button class="button button-small" name="axiom_ghl_action" value="retry">Retry</button></form>';
		}
		echo '</td></tr>';
	}
	echo '</tbody></table></div>';
}

/* ------------------------------------------------------------ admin REST (status + verify) */

add_action(
	'rest_api_init',
	function () {
		$admin = function () {
			return current_user_can( 'manage_options' );
		};
		register_rest_route(
			'axiom/v1',
			'/crm-sync',
			array(
				array(
					'methods'             => 'GET',
					'permission_callback' => $admin,
					'callback'            => function () {
						$s       = settings();
						$entries = array();
						foreach ( recent_entries( 10 ) as $p ) {
							$st        = get_state( $p->ID );
							$entries[] = array(
								'id'      => $p->ID,
								'post'    => $p->post_status,
								'status'  => isset( $st['status'] ) ? $st['status'] : null,
								'preview' => isset( $st['preview'] ) ? $st['preview'] : null,
								'history' => isset( $st['history'] ) ? $st['history'] : array(),
							);
						}
						$response = rest_ensure_response(
							array(
								'token_defined'     => '' !== token(),
								'action_scheduler'  => function_exists( 'as_enqueue_async_action' ),
								'settings'          => $s,
								'entries'           => $entries,
							)
						);
						$response->header( 'Cache-Control', 'no-store' );
						return $response;
					},
				),
				array(
					'methods'             => 'POST',
					'permission_callback' => $admin,
					'callback'            => function ( $request ) {
						if ( 'verify' === $request['action'] ) {
							return rest_ensure_response( verify() );
						}
						return new \WP_Error( 'axiom_bad_action', 'Unknown action.', array( 'status' => 400 ) );
					},
				),
			)
		);
	}
);
