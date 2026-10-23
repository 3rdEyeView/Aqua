<?php
/** Axiom CRM Sync: API client and delivery job (loaded by main.php). */
namespace AngieSnippets\AxiomCrmSync_1398;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
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

	// 1b. Lead source only for contacts this entry created, so an existing
	//     contact's original source (e.g. an ad campaign) is never overwritten.
	if ( ! empty( $state['contact_new'] ) && empty( $state['source_set'] ) ) {
		$r = api( 'PUT', '/contacts/' . rawurlencode( $state['contact_id'] ), array( 'source' => SOURCE ), true );
		if ( is_wp_error( $r ) ) {
			return fail_or_retry( $post_id, $r );
		}
		$state = set_state( $post_id, array( 'source_set' => true ), 'source set on new contact' );
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
