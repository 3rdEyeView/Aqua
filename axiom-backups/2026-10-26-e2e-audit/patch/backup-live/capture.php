<?php
/** Axiom CRM Sync: settings, form capture, queue, payload (loaded by main.php). */
namespace AngieSnippets\AxiomCrmSync_1398;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/* ------------------------------------------------------------ settings */

function defaults() {
	return array(
		'mode'             => 'dry-run',
		'location_id'      => defined( 'AXIOM_GHL_LOCATION_ID' ) ? AXIOM_GHL_LOCATION_ID : DEFAULT_LOCATION,
		'pipeline_id'      => '',
		'stage_id'         => '',
		// Form label => GoHighLevel custom field ID (contact model). Empty = not mapped.
		'field_map'        => array(),
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
	);
	$custom = array();
	foreach ( (array) $s['field_map'] as $label => $field_id ) {
		$value = 'Current website' === $label ? $site : field( $snap, $label );
		if ( $field_id && '' !== $value ) {
			$custom[] = array( 'id' => $field_id, 'field_value' => $value );
		}
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
		'opportunity'    => 'created by the GoHighLevel workflow',
		'source'         => 'set only if the contact is new',
	);
}
