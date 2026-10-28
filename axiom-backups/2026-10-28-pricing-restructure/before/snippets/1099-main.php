<?php
/**
 * Axiom Get Started Form
 * Replaces the AXIOM_GS_FORM_SLOT marker on the Get Started page with
 * Jetpack form 1096, records the ?plan= interest in the hidden field,
 * and styles the form to match the Axiom design system.
 */
namespace AngieSnippets\AxiomGetStartedForm_1099;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const FORM_ID      = 1096;
const MARKER       = 'AXIOM_GS_FORM_SLOT';
const DEFAULT_PLAN = 'Website (no plan selected)';
// Approved scheduling link. Leave empty until one is provided.
const CALENDLY_URL = '';
// Google Ads "Submit lead form" conversion (send_to). Leave empty until the
// owner confirms the value from Google Ads; while empty nothing is sent to Google.
const LEAD_CONVERSION_SEND_TO = 'AW-17889231515/C8k6CJn4q6YdEJuFoNJC';
// Entries older than this are never counted (guards against replays).
const LEAD_MAX_AGE = 600;

function plans() {
	return array(
		'essential'            => array( 'Axiom Essential', '$299/month' ),
		'growth'               => array( 'Axiom Growth', '$599/month' ),
		'marketing'            => array( 'Axiom Marketing', 'Starting at $1,500/month' ),
		'lead-automation'      => array( 'Axiom Lead Automation', '+$349/month' ),
	);
}

// Legacy ?plan= values from older links. Review Automation is now free
// with every website plan, so it maps to Axiom Essential. Lead Response and
// Follow-Up Automation were consolidated into Axiom Lead Automation.
function aliases() {
	return array(
		'growth-system'        => 'growth',
		'review-automation'    => 'essential',
		'lead-response'        => 'lead-automation',
		'follow-up-automation' => 'lead-automation',
	);
}

function current_plan() {
	if ( empty( $_GET['plan'] ) ) {
		return null;
	}
	$key     = sanitize_key( wp_unslash( $_GET['plan'] ) );
	$aliases = aliases();
	$plans   = plans();
	$target  = isset( $aliases[ $key ] ) ? $aliases[ $key ] : $key;
	// The recorded key keeps the original parameter so legacy links stay traceable.
	return isset( $plans[ $target ] ) ? array( $key, $plans[ $target ][0], $plans[ $target ][1] ) : null;
}

function styles() {
	return '<style id="axgs-form-css">
.axgs{width:100%}
.axgs-plan{margin:0 0 20px;padding:12px 16px;border-radius:10px;background:var(--ax-blue-soft,#EAF1FD);color:var(--ax-ink,#0A1628);font-family:var(--ax-body,Inter),sans-serif;font-size:15px;line-height:1.4}
.axgs-plan span{display:block;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ax-blue,#1D6CE2);margin-bottom:2px}
.axgs .wp-block-jetpack-contact-form{display:flex;flex-direction:column;gap:18px;padding:0;margin:0}
.axgs .wp-block-jetpack-contact-form>*{width:100%!important;flex:0 0 100%!important;max-width:100%!important;margin:0!important}
.axgs .grunion-field-wrap,.axgs .contact-form__input-wrap{width:100%}
.axgs label,.axgs .grunion-field-label{display:block;font-family:var(--ax-body,Inter),sans-serif;font-size:14px;font-weight:600;color:var(--ax-ink,#0A1628);margin:0 0 6px;line-height:1.3}
.axgs .grunion-label-required{font-weight:500;color:var(--ax-muted,#5B6778);font-size:12px;margin-left:4px}
.axgs input[type=text],.axgs input[type=email],.axgs input[type=tel],.axgs input[type=url],.axgs textarea{width:100%!important;max-width:100%;box-sizing:border-box;min-height:52px;padding:13px 15px;border:1px solid var(--ax-line,#E2E7EE)!important;border-radius:10px!important;background:#fff!important;color:var(--ax-ink,#0A1628);font-family:var(--ax-body,Inter),sans-serif;font-size:16px;line-height:1.4;box-shadow:none;transition:border-color .15s,box-shadow .15s}
.axgs textarea{min-height:132px;resize:vertical}
.axgs input:focus,.axgs textarea:focus{outline:none;border-color:var(--ax-blue,#1D6CE2)!important;box-shadow:0 0 0 3px rgba(29,108,226,.18)}
.axgs input::placeholder,.axgs textarea::placeholder,.axgs .grunion-field::placeholder{color:#8A94A3!important;opacity:1!important}
.axgs .wp-block-jetpack-button,.axgs .wp-block-button{margin-top:4px!important}
.axgs button[type=submit],.axgs .wp-block-button__link{display:block;width:100%!important;min-height:56px;padding:16px 24px;border:0!important;border-radius:10px!important;background:var(--ax-blue,#1D6CE2)!important;color:#fff!important;font-family:var(--ax-display,Manrope),sans-serif;font-size:15px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;transition:background .15s}
.axgs button[type=submit]:hover,.axgs button[type=submit]:focus-visible{background:var(--ax-blue-deep,#1553B4)!important}
.axgs .contact-form__input-error{color:#B42318;font-size:14px}
.axgs .contact-form__error.show-errors{background:#FEF3F2!important;color:#B42318!important;border:1px solid #FECDCA;border-radius:10px;padding:12px 16px;font-family:var(--ax-body,Inter),sans-serif;font-size:14px;line-height:1.5}
.axgs .contact-form__error.show-errors *{color:inherit!important}
.axgs .contact-form-submission{font-family:var(--ax-body,Inter),sans-serif;color:var(--ax-ink,#0A1628);padding:8px 0}
.axgs .contact-form-submission .go-back-message{display:none}
.axgs .contact-form-submission h4{margin:0 0 10px;font-family:var(--ax-display,Manrope),sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-.02em;line-height:1.15;color:var(--ax-ink,#0A1628)}
.axgs .jetpack_forms_contact-form-custom-success-message{font-size:1rem;line-height:1.6;color:var(--ax-muted,#5B6778)}
.axgs-cal-wrap{display:none;margin:14px 0 0}
.axgs:has(.submission-success) .axgs-cal-wrap{display:block}
.axgs-cal{color:var(--ax-blue,#1D6CE2);font-weight:700;text-decoration:none}
</style>';
}

function script( $label ) {
	$data = wp_json_encode(
		array(
			'def'   => DEFAULT_PLAN,
			'label' => $label,
		)
	);
	// Mobile keyboards and autofill hints; keep the plan label in the hidden field.
	return '<script id="axgs-form-js">(function(){var d=' . $data . ',f=document.querySelector(".axgs form");if(!f)return;'
		. 'var h={name:"name",businessname:"organization",email:"email",phone:"tel",currentwebsite:"url"};'
		. 'Object.keys(h).forEach(function(k){var el=f.querySelector("[name$=\'-"+k+"\']");if(el){el.setAttribute("autocomplete",h[k]);}});'
		. 'var u=f.querySelector("[name$=\'-currentwebsite\']");if(u){u.setAttribute("inputmode","url");}'
		. 'if(d.label){f.querySelectorAll("input[type=hidden]").forEach(function(el){if(el.value===d.def){el.value=d.label;}});}})();</script>';
}

function render_form() {
	$plan  = current_plan();
	$label = $plan ? $plan[1] . ' — ' . $plan[2] . ' (plan=' . $plan[0] . ')' : '';

	$form = do_blocks( '<!-- wp:jetpack/contact-form {"ref":' . FORM_ID . '} /-->' );
	if ( $label ) {
		// Server-side: set the hidden field's value (input value and the
		// interactivity context). Labels come from the allowlist above and
		// contain no quote, backslash or markup characters.
		$form = str_replace( DEFAULT_PLAN, $label, $form );
	}

	$html = styles() . '<div class="axgs">';
	if ( $plan ) {
		$html .= '<p class="axgs-plan"><span>Interested in</span>' . esc_html( $plan[1] ) . ' — ' . esc_html( $plan[2] ) . '</p>';
	}
	$html .= $form;
	if ( '' !== CALENDLY_URL ) {
		// Hidden by CSS until the form reports a successful submission.
		$html .= '<p class="axgs-cal-wrap"><a class="axgs-cal" href="' . esc_url( CALENDLY_URL ) . '" target="_blank" rel="noopener">Want to talk sooner? Schedule a Call →</a></p>';
	}
	$html .= '</div>';
	$html .= script( $label );
	$html .= lead_tracking_script();
	return $html;
}

/**
 * True only for a recent, non-spam entry from the Get Started form.
 * Jetpack reports success for Akismet spam too, so the stored status decides.
 */
function lead_is_countable( $entry_id ) {
	$post = get_post( $entry_id );
	if ( ! $post || 'feedback' !== $post->post_type || 'publish' !== $post->post_status ) {
		return false;
	}
	if ( FORM_ID !== (int) $post->post_parent ) {
		return false;
	}
	return ( time() - (int) get_post_time( 'U', true, $post ) ) <= LEAD_MAX_AGE;
}

add_action(
	'rest_api_init',
	function () {
		register_rest_route(
			'axiom/v1',
			'/lead-check',
			array(
				'methods'             => 'POST',
				'permission_callback' => '__return_true',
				'args'                => array(
					'id' => array(
						'type'     => 'integer',
						'required' => true,
						'minimum'  => 1,
					),
				),
				'callback'            => function ( $request ) {
					$response = rest_ensure_response( array( 'countable' => lead_is_countable( (int) $request['id'] ) ) );
					$response->header( 'Cache-Control', 'no-store' );
					return $response;
				},
			)
		);
	}
);

/**
 * Fires the lead conversion once per accepted, non-spam submission. It reads
 * Jetpack's own AJAX response (success + entry ID), confirms the entry
 * server-side, then sends only send_to and a non-personal transaction ID.
 */
function lead_tracking_script() {
	$cfg = wp_json_encode(
		array(
			'dest'  => LEAD_CONVERSION_SEND_TO,
			'check' => esc_url_raw( rest_url( 'axiom/v1/lead-check' ) ),
		)
	);
	return '<script id="axgs-lead-js">(function(){var c=' . $cfg . ';if(!window.fetch||window.axiomLeadTracking)return;'
		. 'var st=window.axiomLeadTracking={fired:[],skipped:[]},seen={},of=window.fetch;'
		. 'function has(k){if(seen[k])return true;try{return !!localStorage.getItem(k);}catch(e){return false;}}'
		. 'function mark(k){seen[k]=1;try{localStorage.setItem(k,"1");}catch(e){}}'
		. 'function handle(j){if(!j||j.success!==true||!j.refreshArgs)return;var id=parseInt(j.refreshArgs["contact-form-sent"],10);if(!(id>0))return;'
		. 'var k="axiomLead:"+id;if(has(k)){st.skipped.push({id:id,reason:"duplicate"});return;}mark(k);'
		. 'of(c.check,{method:"POST",credentials:"omit",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:id})})'
		. '.then(function(r){return r.ok?r.json():null;}).then(function(v){'
		. 'if(!v||v.countable!==true){st.skipped.push({id:id,reason:"not-countable"});return;}'
		. 'if(c.dest&&typeof window.gtag==="function"){window.gtag("event","conversion",{send_to:c.dest,transaction_id:"axiom-lead-"+id});st.fired.push(id);}'
		. 'else{st.skipped.push({id:id,reason:"no-destination"});}}).catch(function(){st.skipped.push({id:id,reason:"check-failed"});});}'
		. 'window.fetch=function(input,init){var p=of.apply(this,arguments);try{var u=typeof input==="string"?input:(input&&input.url)||"";'
		. 'var m=((init&&init.method)||(input&&input.method)||"GET").toUpperCase();'
		. 'if(m==="POST"&&u.indexOf("action=grunion-contact-form")!==-1){p.then(function(r){if(r.ok)return r.clone().json().then(handle);}).catch(function(){});}}catch(e){}return p;};'
		. '})();</script>';
}

function replace_marker( $content ) {
	if ( ! is_string( $content ) || false === strpos( $content, MARKER ) ) {
		return $content;
	}
	return preg_replace_callback(
		'#<p\b[^>]*>\s*' . MARKER . '\s*</p>#',
		function () {
			return render_form();
		},
		$content,
		1
	);
}

add_filter( 'elementor/frontend/the_content', __NAMESPACE__ . '\\replace_marker', 20 );
add_filter( 'the_content', __NAMESPACE__ . '\\replace_marker', 999 );
