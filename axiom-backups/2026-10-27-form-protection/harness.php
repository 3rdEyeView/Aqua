<?php
// Offline tests for Axiom Form Protection: stubbed WordPress, fake Cloudflare Siteverify.
namespace {
define( 'ABSPATH', '/' ); define( 'DAY_IN_SECONDS', 86400 );
class WP_Error { public $c; public $m; public $d; function __construct( $c = '', $m = '', $d = null ) { $this->c = $c; $this->m = $m; $this->d = $d; } function get_error_message() { return $this->m; } function get_error_code() { return $this->c; } }
$GLOBALS['H'] = array(); $GLOBALS['OPT'] = array(); $GLOBALS['TR'] = array(); $GLOBALS['META'] = array(); $GLOBALS['HTTP'] = array(); $GLOBALS['MAIL'] = array(); $GLOBALS['FAKE'] = null; $GLOBALS['CAN'] = true;
function add_filter( $h, $cb, $p = 10, $n = 1 ) { $GLOBALS['H'][ $h ][] = array( $cb, $n ); }
function add_action( $h, $cb, $p = 10, $n = 1 ) { add_filter( $h, $cb, $p, $n ); }
function apply_test( $h, ...$a ) { $v = $a[0]; foreach ( $GLOBALS['H'][ $h ] ?? array() as $x ) { $a[0] = $v; $v = call_user_func_array( $x[0], array_slice( $a, 0, $x[1] ) ); } return $v; }
function do_test( $h, ...$a ) { foreach ( $GLOBALS['H'][ $h ] ?? array() as $x ) { call_user_func_array( $x[0], array_slice( $a, 0, $x[1] ) ); } }
function get_option( $k, $d = false ) { return $GLOBALS['OPT'][ $k ] ?? $d; }
function update_option( $k, $v, $a = null ) { $GLOBALS['OPT'][ $k ] = $v; return true; }
function get_transient( $k ) { return $GLOBALS['TR'][ $k ] ?? false; }
function set_transient( $k, $v, $t ) { $GLOBALS['TR'][ $k ] = $v; return true; }
function update_post_meta( $id, $k, $v ) { $GLOBALS['META'][ $id ][ $k ] = $v; }
function wp_salt( $s ) { return 'salt-xyz'; }
function home_url() { return 'https://axiomsystems.systems'; }
function wp_parse_url( $u, $c ) { return parse_url( $u, $c ); }
function sanitize_text_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function sanitize_key( $s ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( $s ) ); }
function wp_unslash( $s ) { return $s; }
function esc_attr( $s ) { return htmlspecialchars( $s, ENT_QUOTES ); }
function esc_url( $s ) { return $s; }
function wp_generate_uuid4() { return '00000000-0000-4000-8000-000000000000'; }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
function wp_remote_post( $u, $a ) { $GLOBALS['HTTP'][] = array( $u, $a ); return call_user_func( $GLOBALS['FAKE'], $a ); }
function wp_remote_retrieve_response_code( $r ) { return $r['code']; }
function wp_remote_retrieve_body( $r ) { return $r['body']; }
function wp_mail( $to, $s, $m ) { $GLOBALS['MAIL'][] = array( $to, $s, $m ); return true; }
function admin_url( $p ) { return 'https://axiomsystems.systems/wp-admin/' . $p; }
function current_user_can( $c ) { return $GLOBALS['CAN']; }
function get_current_user_id() { return 1; }
function wp_json_encode( $v, $f = 0 ) { return json_encode( $v, $f ); }
if ( getenv( 'AXFP_KEYS' ) ) { define( 'AXIOM_TURNSTILE_SITE_KEY', '0x4AAAAAAAsitekey' ); define( 'AXIOM_TURNSTILE_SECRET', '0x4AAAAAAAsecret-DO-NOT-LEAK' ); }
require $argv[1];
}
namespace T {
use AngieSnippets\AxiomFormProtection as P;
$fails = 0;
function ok( $c, $m ) { global $fails; echo ( $c ? 'PASS ' : 'FAIL ' ) . $m . "\n"; if ( ! $c ) $fails++; }
function cf( $json, $code = 200 ) { return function () use ( $json, $code ) { return array( 'code' => $code, 'body' => is_string( $json ) ? $json : json_encode( $json ) ); }; }
function post( $over = array() ) { $_POST = array_merge( array( 'contact-form-id' => '1095', 'g1095-email' => 'Jane@Example.com', 'g1095-phone' => '(727) 555-0100', 'jetpack_form_fill_duration' => '42', 'cf-turnstile-response' => 'tok' ), $over ); }
function reset( $mode = 'log', $ip = '203.0.113.5' ) { $GLOBALS['OPT'] = $mode === 'enforce' ? array( 'axiom_form_protection' => array( 'mode' => 'enforce' ) ) : array(); $GLOBALS['TR'] = array(); $GLOBALS['META'] = array(); $GLOBALS['HTTP'] = array(); $GLOBALS['MAIL'] = array(); $_SERVER = array( 'REMOTE_ADDR' => $ip ); $GLOBALS['FAKE'] = cf( array( 'success' => true, 'hostname' => 'axiomsystems.systems', 'action' => 'get-started' ) ); }
function submit( $id = 500 ) { $r = apply_test( 'jetpack_contact_form_is_spam', false, array() ); if ( ! is_wp_error( $r ) ) { do_test( 'grunion_after_feedback_post_inserted', $id ); } return $r; }
$keys = (bool) getenv( 'AXFP_KEYS' );
$html = '<div class="axgs"><form><input name="x"><div class="wp-block-jetpack-button wp-block-button"><button type="submit">Get Started</button></div></form></div>';

if ( ! $keys ) {
	reset( 'log' ); post();
	ok( $html === apply_test( 'elementor/frontend/the_content', $html ), 'no keys: form HTML unchanged (no widget)' );
	$r = submit( 501 );
	ok( false === $r && 0 === count( $GLOBALS['HTTP'] ), 'no keys: submission allowed, no Cloudflare call' );
	ok( 'not-configured' === $GLOBALS['META'][501]['_axiom_form_protection']['turnstile'] && 'allow-fail-open' === $GLOBALS['META'][501]['_axiom_form_protection']['decision'], 'no keys: entry logged as not-configured / allowed' );
	ok( 'log' === P\mode(), 'no keys: mode stays log' );
	$GLOBALS['OPT']['axiom_form_protection'] = array( 'mode' => 'enforce' );
	ok( 'log' === P\mode(), 'no keys: stored enforce is ignored (never blocks without keys)' );
	ok( is_wp_error( P\set_mode( 'enforce', true ) ), 'no keys: cannot switch to enforce' );
	echo $fails ? "\n$fails FAILED\n" : "\nALL PASSED (no keys)\n"; exit( $fails ? 1 : 0 );
}

// ---- widget
$out = apply_test( 'elementor/frontend/the_content', $html );
ok( 1 === substr_count( $out, 'class="axfp-turnstile cf-turnstile"' ) && strpos( $out, 'axfp-turnstile' ) < strpos( $out, 'wp-block-jetpack-button' ), 'widget inserted once, inside the form before the button' );
ok( false !== strpos( $out, 'challenges.cloudflare.com/turnstile/v0/api.js' ) && false !== strpos( $out, 'data-sitekey="0x4AAAAAAAsitekey"' ), 'Turnstile script and public site key present' );
ok( false === strpos( $out, 'secret' ), 'secret never in page output' );
ok( $out === apply_test( 'elementor/frontend/the_content', $out ), 'idempotent (no second widget)' );
ok( '<p>Other page</p>' === apply_test( 'elementor/frontend/the_content', '<p>Other page</p>' ), 'other pages unchanged' );

// ---- other forms and earlier spam decisions pass straight through
reset( 'enforce' ); post( array( 'contact-form-id' => '999', 'cf-turnstile-response' => '' ) );
ok( false === submit() && 0 === count( $GLOBALS['HTTP'] ), 'other forms untouched' );
reset( 'enforce' ); post();
ok( true === apply_test( 'jetpack_contact_form_is_spam', true, array() ), 'already-spam stays spam' );

// ---- log mode never changes the outcome
foreach ( array(
	array( 'missing token', array( 'cf-turnstile-response' => '' ), cf( array( 'success' => true ) ), 'missing', 'would-reject' ),
	array( 'invalid token', array(), cf( array( 'success' => false, 'error-codes' => array( 'invalid-input-response' ) ) ), 'invalid', 'would-reject' ),
	array( 'replayed token', array(), cf( array( 'success' => false, 'error-codes' => array( 'timeout-or-duplicate' ) ) ), 'invalid', 'would-reject' ),
	array( 'wrong hostname', array(), cf( array( 'success' => true, 'hostname' => 'evil.example' ) ), 'invalid', 'would-reject' ),
	array( 'Cloudflare 5xx', array(), cf( 'oops', 503 ), 'unavailable', 'allow-fail-open' ),
	array( 'bad secret config', array(), cf( array( 'success' => false, 'error-codes' => array( 'invalid-input-secret' ) ) ), 'unavailable', 'allow-fail-open' ),
	array( 'valid token', array(), cf( array( 'success' => true, 'hostname' => 'axiomsystems.systems', 'action' => 'get-started' ) ), 'pass', 'allow' ),
) as $c ) {
	reset( 'log' ); post( $c[1] ); $GLOBALS['FAKE'] = $c[2];
	$r = submit( 600 ); $m = $GLOBALS['META'][600]['_axiom_form_protection'];
	ok( false === $r && $c[3] === $m['turnstile'] && $c[4] === $m['decision'], "log mode, $c[0]: allowed, recorded {$c[3]} / {$c[4]}" );
}
reset( 'log' ); post(); $GLOBALS['FAKE'] = function () { return new \WP_Error( 'http_request_failed', 'timeout' ); };
ok( false === submit( 601 ) && 'unavailable' === $GLOBALS['META'][601]['_axiom_form_protection']['turnstile'], 'log mode, Cloudflare timeout: allowed, recorded unavailable' );

// ---- enforce mode
reset( 'enforce' ); post( array( 'cf-turnstile-response' => '' ) );
$r = submit( 700 );
ok( is_wp_error( $r ) && 'axiom_form_protection' === $r->get_error_code() && ! isset( $GLOBALS['META'][700] ), 'enforce, missing token: rejected with message, no entry' );
reset( 'enforce' ); post(); $GLOBALS['FAKE'] = cf( array( 'success' => false, 'error-codes' => array( 'invalid-input-response' ) ) );
ok( is_wp_error( submit( 701 ) ), 'enforce, invalid token: rejected' );
reset( 'enforce' ); post();
ok( false === submit( 702 ) && 'allow' === $GLOBALS['META'][702]['_axiom_form_protection']['decision'], 'enforce, valid token: allowed' );
reset( 'enforce' ); post(); $GLOBALS['FAKE'] = function () { return new \WP_Error( 'x', 'down' ); };
ok( false === submit( 703 ), 'enforce, Cloudflare down: fail open (allowed)' );
reset( 'enforce' ); post(); $GLOBALS['FAKE'] = cf( array( 'success' => false, 'error-codes' => array( 'invalid-input-secret' ) ) );
ok( false === submit( 704 ), 'enforce, wrong secret configured: fail open (never blocks everyone)' );
$sent = $GLOBALS['HTTP'][0][1]['body'];
ok( 'tok' === $sent['response'] && ! isset( $sent['remoteip'] ) && 5 === $GLOBALS['HTTP'][0][1]['timeout'], 'Siteverify: token sent server-side, 5 s timeout, no IP binding' );

// ---- rate limits
reset( 'enforce' );
$res = array(); for ( $i = 1; $i <= 10; $i++ ) { post( array( 'g1095-email' => "person$i@example.com", 'g1095-phone' => '72755501' . sprintf( '%02d', $i ) ) ); $res[] = submit( 800 + $i ); }
ok( array( false ) === array_unique( $res, SORT_REGULAR ), 'shared IP: 10 different people in 10 min all accepted' );
post( array( 'g1095-email' => 'person11@example.com', 'g1095-phone' => '7275550111' ) );
ok( true === submit( 811 ) && 'flag-spam' === $GLOBALS['META'][811]['_axiom_form_protection']['decision'], 'shared IP: 11th submission in 10 min saved as spam (kept for review)' );
ok( 1 === count( $GLOBALS['MAIL'] ) && false !== strpos( $GLOBALS['MAIL'][0][2], '#811' ) && false === strpos( $GLOBALS['MAIL'][0][2], 'example.com' ), 'rate-limited entry: owner alerted (entry number only)' );
reset( 'enforce' );
$res = array(); foreach ( array( '198.51.100.1', '198.51.100.2', '198.51.100.3', '198.51.100.4' ) as $n => $ip ) { $_SERVER['REMOTE_ADDR'] = $ip; post(); $res[] = submit( 900 + $n ); }
ok( array( false, false, false, true ) === $res, 'same email/phone: 3 per hour accepted, 4th saved as spam' );
reset( 'log' );
for ( $i = 1; $i <= 11; $i++ ) { post( array( 'g1095-email' => "p$i@example.com", 'g1095-phone' => '72755502' . sprintf( '%02d', $i ) ) ); $r = submit( 950 + $i ); }
ok( false === $r && 'would-flag-spam' === $GLOBALS['META'][961]['_axiom_form_protection']['decision'] && 0 === count( $GLOBALS['MAIL'] ), 'log mode: rate limit only recorded (would-flag-spam), no alert' );

// ---- privacy of logs and options
$all = json_encode( array( $GLOBALS['OPT'], $GLOBALS['META'], $GLOBALS['TR'] ) );
ok( false === strpos( $all, 'DO-NOT-LEAK' ) && false === strpos( $all, 'tok"' ) && false === strpos( $all, 'example.com' ) && false === strpos( $all, '203.0.113' ) && false === strpos( $all, '7275550' ), 'logs/options/meta/transients: no secret, token, email, phone or raw IP' );
$st = json_encode( P\status() );
ok( false === strpos( $st, 'DO-NOT-LEAK' ) && false === strpos( $st, 'sitekey' ), 'status output: no keys, only set/missing flags' );

// ---- mode switching
reset( 'log' );
ok( is_wp_error( P\set_mode( 'enforce', false ) ) && 'log' === P\mode(), 'enforce needs explicit confirmation' );
ok( ! is_wp_error( P\set_mode( 'enforce', true ) ) && 'enforce' === P\mode(), 'enforce with confirmation + keys' );
ok( is_wp_error( P\set_mode( 'off', true ) ), 'unknown mode rejected' );

echo $fails ? "\n$fails FAILED\n" : "\nALL PASSED (keys)\n"; exit( $fails ? 1 : 0 );
}
