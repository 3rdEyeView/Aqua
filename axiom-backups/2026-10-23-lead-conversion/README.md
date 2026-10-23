# Google Ads lead conversion — Get Started form (2026-10-23)

## Findings
- Tags come from Google Site Kit 1.190: Google tag GT-55XGH597 (container destinations G-T8J1CRQRH6 and
  AW-17889231515) plus Site Kit's Ads module ID AW-17878870459. No GTM. Consent Mode on (EEA regions denied by default).
- Site Kit conversion tracking is on but has no Jetpack-form provider, so there was no existing lead event.
- Jetpack form 1096 submits by fetch to admin-ajax.php?action=grunion-contact-form; success JSON contains
  refreshArgs['contact-form-sent'] = the feedback entry ID.
- Akismet has no API key, so no submission is currently marked spam.

## Change (snippet 1099)
- `LEAD_CONVERSION_SEND_TO` — empty = dormant (nothing sent to Google). Set to the confirmed send_to value to enable.
- POST /wp-json/axiom/v1/lead-check {id} → {countable} true only for a feedback entry with status publish,
  parent = form 1096, created within 600 s. Response is no-store.
- Browser script observes Jetpack's own AJAX reply; on success:true it asks lead-check, then calls
  gtag('event','conversion',{send_to, transaction_id:'axiom-lead-<entryID>'}) once. Dedup: in-memory + localStorage key
  axiomLead:<id>, plus transaction_id for Google-side dedup. No form data is sent.

## Rollback
Save `snippet-1099-main.php` (original) back into snippet 1099 with angie-update-snippet-files, then angie-publish-snippet.
To pause conversions only, set LEAD_CONVERSION_SEND_TO back to ''.

## Tests (tests/)
t.php / t.js — offline unit tests; live-test.js / spam-sim.js — live browser tests (Google domains blocked, dummy send_to).
