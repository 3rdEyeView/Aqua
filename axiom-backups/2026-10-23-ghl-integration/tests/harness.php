<?php
// Offline tests for the Axiom CRM Sync snippet: stubbed WordPress + fake GoHighLevel API.
namespace {
define( 'ABSPATH', '/' );
define( 'AXIOM_GHL_PRIVATE_TOKEN', 'pit-test-token-123' );
class WP_Error { public $c; public $m; public $d; function __construct( $c = '', $m = '', $d = null ) { $this->c = $c; $this->m = $m; $this->d = $d; } function get_error_message() { return $this->m; } function get_error_data() { return $this->d; } function get_error_code() { return $this->c; } }
$GLOBALS['H'] = array(); $GLOBALS['OPT'] = array(); $GLOBALS['META'] = array(); $GLOBALS['POSTS'] = array(); $GLOBALS['Q'] = array(); $GLOBALS['CALLS'] = array(); $GLOBALS['MAIL'] = array(); $GLOBALS['FAKE'] = null;
function add_action( $h, $cb, $p = 10, $n = 1 ) { $GLOBALS['H'][ $h ][] = array( $cb, $n ); }
function add_filter( $h, $cb, $p = 10, $n = 1 ) { add_action( $h, $cb, $p, $n ); }
function do_action_test( $h, ...$args ) { foreach ( $GLOBALS['H'][ $h ] ?? array() as $x ) { call_user_func_array( $x[0], array_slice( $args, 0, $x[1] ) ); } }
function get_option( $k, $d = false ) { return $GLOBALS['OPT'][ $k ] ?? $d; }
function update_option( $k, $v, $a = null ) { $GLOBALS['OPT'][ $k ] = $v; return true; }
function get_post( $id ) { return $GLOBALS['POSTS'][ $id ] ?? null; }
function get_post_status( $id ) { return isset( $GLOBALS['POSTS'][ $id ] ) ? $GLOBALS['POSTS'][ $id ]->post_status : false; }
function get_post_meta( $id, $k, $single = false ) { return $GLOBALS['META'][ $id ][ $k ] ?? ''; }
function update_post_meta( $id, $k, $v ) { $GLOBALS['META'][ $id ][ $k ] = $v; return true; }
function add_post_meta( $id, $k, $v, $unique = false ) { if ( $unique && isset( $GLOBALS['META'][ $id ][ $k ] ) ) return false; $GLOBALS['META'][ $id ][ $k ] = $v; return true; }
function delete_post_meta( $id, $k ) { unset( $GLOBALS['META'][ $id ][ $k ] ); }
function get_post_time( $f, $gmt, $p ) { return '2026-10-23 05:00'; }
function as_enqueue_async_action( $h, $a, $g, $u = false ) { $GLOBALS['Q'][] = array( 0, $h, $a ); return 1; }
function as_schedule_single_action( $t, $h, $a, $g ) { $GLOBALS['Q'][] = array( $t - time(), $h, $a ); return 1; }
function wp_schedule_single_event( $t, $h, $a ) { $GLOBALS['Q'][] = array( $t - time(), $h, $a ); }
function is_email( $e ) { return (bool) filter_var( $e, FILTER_VALIDATE_EMAIL ); }
function esc_url_raw( $u ) { return $u; }
function sanitize_text_field( $s ) { return trim( strip_tags( $s ) ); }
function wp_json_encode( $v, $f = 0 ) { return json_encode( $v, $f ); }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
function wp_remote_retrieve_response_code( $r ) { return $r['code']; }
function wp_remote_retrieve_body( $r ) { return $r['body']; }
function wp_mail( $to, $s, $m ) { $GLOBALS['MAIL'][] = array( $to, $s, $m ); return true; }
function admin_url( $p ) { return 'https://axiomsystems.systems/wp-admin/' . $p; }
function wp_list_pluck( $l, $f ) { return array_map( function ( $x ) use ( $f ) { return $x[ $f ]; }, $l ); }
function http_build_query_( $a ) { return http_build_query( $a ); }
function wp_remote_request( $url, $args ) {
	$GLOBALS['CALLS'][] = array( $args['method'], str_replace( 'https://services.leadconnectorhq.com', '', $url ), isset( $args['body'] ) ? json_decode( $args['body'], true ) : null, $args['headers'] );
	return call_user_func( $GLOBALS['FAKE'], $args['method'], $url, $args );
}
require $argv[1];
}
namespace T {
use AngieSnippets\AxiomCrmSync_1398 as S;
class Field { public $value; private $label; function __construct( $l, $v ) { $this->label = $l; $this->value = $v; } function get_attribute( $k ) { return 'label' === $k ? $this->label : ''; } }
class PrivField { protected $value; private $label; function __construct( $l, $v ) { $this->label = $l; $this->value = $v; } function get_attribute( $k ) { return 'label' === $k ? $this->label : ''; } }
$fails = 0;
function ok( $cond, $msg ) { global $fails; echo ( $cond ? 'PASS ' : 'FAIL ' ) . $msg . "\n"; if ( ! $cond ) $fails++; }
function entry( $id, $status = 'publish', $parent = 1096 ) { $GLOBALS['POSTS'][ $id ] = (object) array( 'ID' => $id, 'post_type' => 'feedback', 'post_parent' => $parent, 'post_status' => $status ); }
function fields( $over = array(), $cls = Field::class ) {
	$d = array( 'Name' => 'Jane Q Doe', 'Business name' => 'Doe Plumbing', 'Email' => 'Jane@Example.com', 'Phone' => '(727) 555-0100', 'Current website' => '', 'Tell us about your business' => 'We fix pipes.', 'Plan interest' => 'Axiom Growth — $599/month (plan=growth)' );
	$d = array_merge( $d, $over ); $out = array(); $i = 0;
	foreach ( $d as $l => $v ) { $out[ 'g1095-' . $i++ ] = new $cls( $l, $v ); }
	return $out;
}
function values( $over = array() ) { $d = array( 'Name' => 'Jane Q Doe', 'Business name' => 'Doe Plumbing', 'Email' => 'Jane@Example.com', 'Phone' => '(727) 555-0100', 'Current website' => '', 'Tell us about your business' => 'We fix pipes.', 'Plan interest' => 'Axiom Growth — $599/month (plan=growth)' ); $d = array_merge( $d, $over ); $o = array(); $i = 1; foreach ( $d as $l => $v ) { $o[ $i++ . '_' . $l ] = $v; } return $o; }
function run_queue() { $n = 0; while ( $GLOBALS['Q'] && $n++ < 30 ) { $job = array_shift( $GLOBALS['Q'] ); do_action_test( $job[1], ...$job[2] ); } }
function fake_ok() {
	$GLOBALS['NOTES'] = array();
	return function ( $m, $url, $a ) {
		$path = parse_url( $url, PHP_URL_PATH );
		if ( 'POST' === $m && '/contacts/upsert' === $path ) return array( 'code' => 200, 'body' => json_encode( array( 'new' => true, 'contact' => array( 'id' => 'C1' ) ) ) );
		if ( 'POST' === $m && '/contacts/C1/notes' === $path ) { $b = json_decode( $a['body'], true )['body']; $GLOBALS['NOTES'][] = $b; return array( 'code' => 201, 'body' => json_encode( array( 'note' => array( 'id' => 'N' . count( $GLOBALS['NOTES'] ) ) ) ) ); }
		if ( 'GET' === $m && '/contacts/C1/notes' === $path ) return array( 'code' => 200, 'body' => json_encode( array( 'notes' => array_map( function ( $b, $i ) { return array( 'id' => 'N' . ( $i + 1 ), 'body' => $b ); }, $GLOBALS['NOTES'], array_keys( $GLOBALS['NOTES'] ) ) ) ) );
		if ( 'POST' === $m && '/contacts/C1/tags' === $path ) return array( 'code' => 201, 'body' => '{"tags":["x"]}' );
		if ( 'PUT' === $m && '/contacts/C1' === $path ) return array( 'code' => 200, 'body' => '{"succeded":true}' );
		if ( 'GET' === $m && '/opportunities/search' === $path ) return array( 'code' => 200, 'body' => json_encode( array( 'opportunities' => array() ) ) );
		if ( 'POST' === $m && '/opportunities/' === $path ) return array( 'code' => 201, 'body' => json_encode( array( 'opportunity' => array( 'id' => 'O1' ) ) ) );
		return array( 'code' => 404, 'body' => '{"message":"not found"}' );
	};
}
function reset_all( $mode, $extra = array() ) { $GLOBALS['OPT'] = array(); $GLOBALS['META'] = array(); $GLOBALS['Q'] = array(); $GLOBALS['CALLS'] = array(); $GLOBALS['MAIL'] = array(); S\save_settings( array_merge( array( 'mode' => $mode ), $extra ) ); $GLOBALS['FAKE'] = fake_ok(); }
function submit( $id, $over = array(), $spam = false, $cls = Field::class ) { entry( $id, $spam ? 'spam' : 'publish' ); do_action_test( 'grunion_after_feedback_post_inserted', $id, fields( $over, $cls ), $spam, array() ); do_action_test( 'grunion_pre_message_sent', $id, values( $over ), array() ); }
function writes() { return array_values( array_filter( $GLOBALS['CALLS'], function ( $c ) { return 'GET' !== $c[0]; } ) ); }

// --- helpers
ok( '+17275550100' === S\normalize_phone( '(727) 555-0100' ), 'phone 10 digits -> +1' );
ok( '+17275550100' === S\normalize_phone( '1-727-555-0100' ), 'phone 11 digits -> +1' );
ok( '+447700900123' === S\normalize_phone( '+44 7700 900123' ), 'intl phone kept' );
ok( '' === S\normalize_phone( 'n/a' ), 'no digits -> empty' );
$c = S\build_contact( array( 'Name' => 'Jane', 'Email' => 'x@y.co', 'Phone' => '', 'Business name' => '' ), S\settings() );
ok( ! isset( $c['phone'] ) && ! isset( $c['companyName'] ) && ! isset( $c['lastName'] ) && ! isset( $c['website'] ), 'empty values are omitted (no blanking)' );
ok( 'Jane' === $c['firstName'] && 'x@y.co' === $c['email'], 'name/email mapped' );

// --- dry-run: no GHL requests at all
reset_all( 'dry-run' );
submit( 101 );
ok( 1 === count( $GLOBALS['Q'] ), 'dry-run: one job queued in submission request' );
ok( 0 === count( $GLOBALS['CALLS'] ), 'dry-run: no HTTP during submission' );
run_queue();
ok( 0 === count( $GLOBALS['CALLS'] ), 'dry-run: worker made no HTTP requests' );
$st = S\get_state( 101 );
ok( 'dry-run' === $st['status'], 'dry-run: status recorded' );
ok( in_array( 'companyName', $st['preview']['contact_fields'], true ) && in_array( 'phone', $st['preview']['contact_fields'], true ) && ! in_array( 'website', $st['preview']['contact_fields'], true ), 'dry-run preview lists mapped fields, skips empty website' );
ok( false === strpos( json_encode( $st ), 'Jane' ), 'state/preview contains no lead values' );

// --- spam and other forms are not queued
reset_all( 'live' );
submit( 102, array(), true );
ok( 0 === count( $GLOBALS['Q'] ) && array() === S\get_state( 102 ), 'spam entry not queued' );
entry( 103, 'publish', 999 ); do_action_test( 'grunion_after_feedback_post_inserted', 103, fields(), false, array() );
ok( 0 === count( $GLOBALS['Q'] ), 'other form not queued' );

// --- verify-style guard: write blocked without allow flag
$r = S\api( 'POST', '/contacts/upsert', array( 'x' => 1 ) );
ok( $r instanceof \WP_Error && 'axiom_write_blocked' === $r->get_error_code() && 0 === count( $GLOBALS['CALLS'] ), 'api() refuses writes unless explicitly allowed' );

// --- live: upsert -> note -> tag, in that order, token only in header
reset_all( 'live' );
submit( 104 );
run_queue();
$w = writes();
ok( array( '/contacts/upsert', '/contacts/C1', '/contacts/C1/notes', '/contacts/C1/tags' ) === array_column( $w, 1 ), 'live: upsert, source (new contact), note, tag (tag last)' );
ok( array( 'axiom-new-lead' ) === $w[3][2]['tags'], 'live: axiom-new-lead tag' );
ok( ! isset( $w[0][2]['source'] ) && 'Website: Get Started form' === $w[1][2]['source'] && 'PUT' === $w[1][0], 'source not in upsert; set separately on new contact' );
ok( 'WSbB7bUher6I1M2VNlZz' === $w[0][2]['locationId'] && '+17275550100' === $w[0][2]['phone'] && 'jane@example.com' === $w[0][2]['email'] && 'Doe Plumbing' === $w[0][2]['companyName'] && ! isset( $w[0][2]['website'] ), 'live: upsert payload mapped, empty website omitted' );
ok( 'Bearer pit-test-token-123' === $w[0][3]['Authorization'] && '2021-07-28' === $w[0][3]['Version'], 'token only sent in Authorization header' );
$st = S\get_state( 104 );
ok( 'sent' === $st['status'] && false === strpos( json_encode( array( $st, $GLOBALS['OPT'] ) ), 'pit-test' ), 'live: sent; token not stored anywhere' );
ok( false !== strpos( $GLOBALS['NOTES'][0], 'Axiom website entry #104' ) && false !== strpos( $GLOBALS['NOTES'][0], 'We fix pipes.' ), 'note has marker and message' );
ok( ! in_array( '/opportunities/', array_column( $w, 1 ), true ), 'workflow mode: no opportunity created by the snippet' );
// re-running the same job does nothing
$GLOBALS['CALLS'] = array(); do_action_test( 'axiom_ghl_sync_entry', 104 );
ok( 0 === count( $GLOBALS['CALLS'] ), 'already-sent entry is never re-sent' );

// --- existing contact: source never touched
reset_all( 'live' );
$base = fake_ok();
$GLOBALS['FAKE'] = function ( $m, $url, $a ) use ( $base ) { if ( false !== strpos( $url, '/contacts/upsert' ) ) return array( 'code' => 200, 'body' => json_encode( array( 'new' => false, 'contact' => array( 'id' => 'C1' ) ) ) ); return $base( $m, $url, $a ); };
submit( 120 ); run_queue();
ok( 'sent' === S\get_state( 120 )['status'] && ! in_array( 'PUT', array_column( writes(), 0 ), true ), 'existing contact: no source overwrite' );

// --- custom field map: only non-empty values, website normalised
reset_all( 'live', array( 'field_map' => array( 'Business name' => 'F_BIZ', 'Current website' => 'F_WEB', 'Plan interest' => 'F_PLAN', 'Tell us about your business' => '' ) ) );
submit( 121, array( 'Current website' => 'doeplumbing.com' ) ); run_queue();
$cf = writes()[0][2]['customFields'];
ok( array( 'F_BIZ', 'F_WEB', 'F_PLAN' ) === array_column( $cf, 'id' ) && 'https://doeplumbing.com' === $cf[1]['field_value'], 'field map: mapped fields sent, unmapped skipped, website normalised' );
reset_all( 'live', array( 'field_map' => array( 'Current website' => 'F_WEB' ) ) );
submit( 122 ); run_queue();
ok( ! isset( writes()[0][2]['customFields'] ), 'field map: empty value not sent (no blanking)' );

// --- note step fails after being sent (timeout) -> retry finds note, no duplicate
reset_all( 'live' );
$base = fake_ok(); $first = true;
$GLOBALS['FAKE'] = function ( $m, $url, $a ) use ( $base, &$first ) { $r = $base( $m, $url, $a ); if ( $first && 'POST' === $m && false !== strpos( $url, '/notes' ) ) { $first = false; return new \WP_Error( 'http_request_failed', 'cURL error 28: timed out' ); } return $r; };
submit( 105 );
run_queue();
ok( 1 === count( $GLOBALS['NOTES'] ), 'timeout after note was saved: retry finds it, exactly one note' );
ok( 'sent' === S\get_state( 105 )['status'] && 1 === S\get_state( 105 )['attempts'], 'retried once then sent' );
ok( 1 === count( array_filter( writes(), function ( $c ) { return '/contacts/upsert' === $c[1]; } ) ), 'contact upserted once across retries' );

// --- 5xx retries with backoff, then fails and alerts; 401 fails immediately
reset_all( 'live' );
$GLOBALS['FAKE'] = function () { return array( 'code' => 503, 'body' => '{"message":"down"}' ); };
submit( 106 );
$delays = array(); $n = 0;
while ( $GLOBALS['Q'] && $n++ < 20 ) { $job = array_shift( $GLOBALS['Q'] ); $delays[] = $job[0]; do_action_test( $job[1], ...$job[2] ); }
ok( array( 0, 60, 300, 1800, 7200, 43200 ) === $delays, 'retry schedule 1m, 5m, 30m, 2h, 12h' );
ok( 'failed' === S\get_state( 106 )['status'] && 1 === count( $GLOBALS['MAIL'] ), 'after final retry: failed + one alert email' );
ok( false === strpos( $GLOBALS['MAIL'][0][2], 'Jane' ) && false === strpos( $GLOBALS['MAIL'][0][2], 'pit-' ), 'alert email has no lead data or token' );
reset_all( 'live' );
$GLOBALS['FAKE'] = function () { return array( 'code' => 401, 'body' => '{"message":"Invalid JWT"}' ); };
submit( 107 ); run_queue();
ok( 'failed' === S\get_state( 107 )['status'] && 1 === count( $GLOBALS['CALLS'] ) && 1 === count( $GLOBALS['MAIL'] ), '401: no retry, failed + alert' );

// --- test mode: only listed emails, test tag; others held
reset_all( 'test', array( 'test_emails' => 'qa-test@example.com' ) );
submit( 108 ); run_queue();
ok( 'held' === S\get_state( 108 )['status'] && 0 === count( $GLOBALS['CALLS'] ), 'test mode: real lead held, no requests' );
submit( 109, array( 'Email' => 'QA-Test@example.com' ) ); run_queue();
$w = writes();
ok( 'sent' === S\get_state( 109 )['status'] && array( 'axiom-integration-test' ) === end( $w )[2]['tags'], 'test mode: listed email sent with test tag' );
ok( ! in_array( '/opportunities/', array_column( $w, 1 ), true ), 'test mode never creates opportunities' );

// --- api opportunity mode: existing open one reused, otherwise created once
reset_all( 'live', array( 'opportunity_mode' => 'api', 'pipeline_id' => 'P1', 'stage_id' => 'S1' ) );
submit( 110 ); run_queue();
$opp = array_values( array_filter( writes(), function ( $c ) { return '/opportunities/' === $c[1]; } ) );
ok( 1 === count( $opp ) && 'S1' === $opp[0][2]['pipelineStageId'] && 'open' === $opp[0][2]['status'], 'api mode: creates one opportunity at New Lead' );
reset_all( 'live', array( 'opportunity_mode' => 'api', 'pipeline_id' => 'P1', 'stage_id' => 'S1' ) );
$base = fake_ok();
$GLOBALS['FAKE'] = function ( $m, $url, $a ) use ( $base ) { if ( false !== strpos( $url, '/opportunities/search' ) ) return array( 'code' => 200, 'body' => json_encode( array( 'opportunities' => array( array( 'id' => 'OLD', 'status' => 'open' ) ) ) ) ); return $base( $m, $url, $a ); };
submit( 111 ); run_queue();
ok( 0 === count( array_filter( writes(), function ( $c ) { return '/opportunities/' === $c[1]; } ) ) && 'OLD' === S\get_state( 111 )['opportunity_id'], 'api mode: existing open opportunity reused, none created' );

// --- protected field values: fallback snapshot from email values still works
reset_all( 'live' );
submit( 112, array(), false, PrivField::class ); run_queue();
ok( 'sent' === S\get_state( 112 )['status'] && 'Doe Plumbing' === writes()[0][2]['companyName'], 'non-public field values: fallback capture still maps fields' );

// --- no email and no phone -> skipped, no requests
reset_all( 'live' );
submit( 113, array( 'Email' => 'not-an-email', 'Phone' => '' ) ); run_queue();
ok( 'skipped' === S\get_state( 113 )['status'] && 0 === count( $GLOBALS['CALLS'] ), 'no valid email/phone: skipped, nothing sent' );

// --- verify: GET only
reset_all( 'dry-run' );
$GLOBALS['FAKE'] = function ( $m, $url ) {
	$p = parse_url( $url, PHP_URL_PATH );
	$map = array(
		'/locations/WSbB7bUher6I1M2VNlZz' => array( 'location' => array( 'id' => 'WSbB7bUher6I1M2VNlZz', 'name' => 'AxiomSystems' ) ),
		'/contacts/' => array( 'contacts' => array() ),
		'/opportunities/pipelines' => array( 'pipelines' => array( array( 'id' => 'P1', 'name' => 'AXIOM | Standard Client Pipeline', 'stages' => array( array( 'id' => 'S0', 'name' => 'Inbox' ), array( 'id' => 'S1', 'name' => 'New Lead' ) ) ) ) ),
		'/locations/WSbB7bUher6I1M2VNlZz/tags' => array( 'tags' => array( array( 'name' => 'axiom-new-lead' ) ) ),
		'/locations/WSbB7bUher6I1M2VNlZz/customFields' => array( 'customFields' => array( array( 'id' => 'F1', 'name' => 'Message', 'fieldKey' => 'contact.message', 'dataType' => 'LARGE_TEXT', 'model' => 'contact' ) ) ),
		'/workflows/' => array( 'workflows' => array( array( 'name' => 'New Lead', 'status' => 'published' ) ) ),
	);
	return isset( $map[ $p ] ) ? array( 'code' => 200, 'body' => json_encode( $map[ $p ] ) ) : array( 'code' => 403, 'body' => '{"message":"The token is not authorized for this scope."}' );
};
$v = S\verify();
ok( 6 === count( $GLOBALS['CALLS'] ) && 0 === count( writes() ), 'verify: 6 requests, all GET' );
ok( $v['checks']['location (locations.readonly)']['id_matches'] && 'P1' === S\settings()['pipeline_id'] && 'S1' === S\settings()['stage_id'], 'verify: location matched; "AXIOM | Standard Client Pipeline" / New Lead stored' );
ok( true === $v['checks']['tags (locations/tags.readonly)']['axiom-new-lead_exists'], 'verify: tag found' );
ok( false === strpos( json_encode( $GLOBALS['OPT'] ), 'pit-test' ), 'verify results do not contain the token' );

echo $fails ? "\n$fails FAILED\n" : "\nALL PASSED\n";
exit( $fails ? 1 : 0 );
}
