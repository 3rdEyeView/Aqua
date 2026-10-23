<?php
/** Axiom CRM Sync: admin page (Tools > Axiom CRM Sync) (loaded by main.php). */
namespace AngieSnippets\AxiomCrmSync_1398;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
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

/** Form fields that can be mapped to GoHighLevel custom fields. */
function mapped_labels() {
	return array( 'Business name', 'Current website', 'Plan interest', 'Tell us about your business' );
}

function posted_field_map() {
	$posted = isset( $_POST['field_map'] ) && is_array( $_POST['field_map'] ) ? wp_unslash( $_POST['field_map'] ) : array();
	$map    = array();
	foreach ( mapped_labels() as $i => $label ) {
		$map[ $label ] = isset( $posted[ $i ] ) ? sanitize_text_field( $posted[ $i ] ) : '';
	}
	return $map;
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
						'field_map'        => posted_field_map(),
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
	foreach ( mapped_labels() as $i => $label ) {
		$id = isset( $s['field_map'][ $label ] ) ? $s['field_map'][ $label ] : '';
		echo '<tr><th>Custom field ID for &ldquo;' . esc_html( $label ) . '&rdquo;</th><td><input name="field_map[' . (int) $i . ']" class="regular-text" value="' . esc_attr( $id ) . '"> <span class="description">Empty: not mapped (still in the note).</span></td></tr>';
	}
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
