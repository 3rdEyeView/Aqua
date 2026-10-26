<?php
/** Axiom CRM Sync: read-only verification and status REST (loaded by main.php). */
namespace AngieSnippets\AxiomCrmSync_1398;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/* ------------------------------------------------------------ verification (GET only) */

/** Compares names ignoring case, spaces and punctuation ("AXIOM | Standard Client Pipeline"). */
function name_key( $name ) {
	return preg_replace( '/[^a-z0-9]/', '', strtolower( (string) $name ) );
}

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
			$l   = isset( $r['location'] ) ? $r['location'] : $r;
			$set = isset( $l['settings'] ) && is_array( $l['settings'] ) ? $l['settings'] : array();
			$dup = array();
			foreach ( array( 'allowDuplicateContact', 'allowDuplicateOpportunity', 'allowFacebookNameMerge' ) as $k ) {
				$dup[ $k ] = array_key_exists( $k, $set ) ? $set[ $k ] : 'not returned';
			}
			return array( 'name' => isset( $l['name'] ) ? $l['name'] : '', 'id_matches' => isset( $l['id'] ) && $l['id'] === $s['location_id'], 'duplicate_settings' => $dup );
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
			$ids   = array();
			foreach ( isset( $r['pipelines'] ) ? $r['pipelines'] : array() as $p ) {
				$names[]         = $p['name'];
				$ids[ $p['id'] ] = $p['name'] . ' (' . implode( ', ', wp_list_pluck( $p['stages'], 'name' ) ) . ')';
				if ( name_key( $p['name'] ) === name_key( PIPELINE_NAME ) ) {
					$pipeline = array( 'pipeline_id' => $p['id'], 'stage_id' => '' );
					foreach ( $p['stages'] as $st ) {
						if ( name_key( $st['name'] ) === name_key( STAGE_NAME ) ) {
							$pipeline['stage_id'] = $st['id'];
						}
					}
				}
			}
			return array( 'pipelines' => $names, 'pipeline_ids' => $ids, 'axiom_pipeline' => $pipeline );
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
	if ( $pipeline ) {
		$changes['pipeline_id'] = $pipeline['pipeline_id'];
		$changes['stage_id']    = $pipeline['stage_id'];
	}
	save_settings( $changes );
	return $out;
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
						if ( 'check' === $request['action'] ) {
							$id = (int) $request['entry'];
							if ( ! is_form_entry( $id ) ) {
								return new \WP_Error( 'axiom_entry', 'Not a Get Started entry.', array( 'status' => 400 ) );
							}
							check_opportunity( $id );
							$st = get_state( $id );
							return rest_ensure_response( array( 'entry' => $id, 'opportunity_check' => isset( $st['opportunity_check'] ) ? $st['opportunity_check'] : null ) );
						}
						if ( 'settings' === $request['action'] ) {
							$changes = array();
							if ( isset( $request['mode'] ) ) {
								// Live can only be switched on from the admin page, with confirmation.
								if ( ! in_array( $request['mode'], array( 'off', 'dry-run', 'test' ), true ) ) {
									return new \WP_Error( 'axiom_mode', 'Mode must be off, dry-run or test here.', array( 'status' => 400 ) );
								}
								$changes['mode'] = $request['mode'];
							}
							if ( isset( $request['field_map'] ) && is_array( $request['field_map'] ) ) {
								$changes['field_map'] = array_map( 'sanitize_text_field', array_intersect_key( $request['field_map'], array_flip( mapped_labels() ) ) );
							}
							if ( isset( $request['test_emails'] ) ) {
								$changes['test_emails'] = sanitize_textarea_field( $request['test_emails'] );
							}
							$s = save_settings( $changes );
							unset( $s['verified'] );
							return rest_ensure_response( $s );
						}
						return new \WP_Error( 'axiom_bad_action', 'Unknown action.', array( 'status' => 400 ) );
					},
				),
			)
		);
	}
);
