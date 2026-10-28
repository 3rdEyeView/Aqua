# Google Ads conversion tracking audit — Get Started (2026-10-28, read-only, nothing changed)

## Tag configuration (Site Kit 1.190; no GTM)
- Page loads one Google tag: `gtag/js?id=GT-55XGH597`, then `config GT-55XGH597` and `config AW-17878870459`.
- GT-55XGH597 destinations (Site Kit, last synced 2026-02-07): **G-T8J1CRQRH6** (GA4) and **AW-17889231515** — this is
  the "base Ads tag" Tag Assistant shows.
- Site Kit Ads module conversion ID: **AW-17878870459** (a different Ads account/ID; no conversion is sent to it).
- Tag Manager: not connected. Consent Mode: on, denied by default only for EEA/UK/CH. GA4 not output for logged-in users.
- Site Kit conversion tracking: on, but its providers only send engagement events (contact_link_click,
  outbound_link_click, read_article…) and WooCommerce events — no lead conversion.

## Conversion source (only one): snippet 1099 "Axiom Get Started Form"
`LEAD_CONVERSION_SEND_TO = 'AW-17889231515/C8k6CJn4q6YdEJuFoNJC'`. Label 6i7MCMaIsqYdEJuFoNJC appears nowhere on the site.
History (`../2026-10-23-lead-conversion/README.md`): activated 2026-10-23 with **6i7M…** ("Submit lead form", owner-confirmed),
then replaced the same day with **C8k6…** (owner-supplied "manual lead conversion").
→ They are two separate conversion actions in the same account (a conversion label identifies one conversion action).
   Since 2026-10-23 the site sends only to C8k6, so Tag Assistant cannot detect 6i7M.

Flow: Jetpack 16.3.1 form submits via `fetch POST admin-ajax.php?action=grunion-contact-form` (unchanged from 10-23); the
tracker wraps `fetch`, reads Jetpack's JSON (`success:true`, `refreshArgs['contact-form-sent']` = entry ID), asks
`/wp-json/axiom/v1/lead-check` (true only for a non-spam form-1096 entry < 10 min old), then
`gtag('event','conversion',{send_to, transaction_id:'axiom-lead-<entry>'})`; dedup by localStorage + transaction_id.
Snippet 1411 (form protection, log mode, no Turnstile keys) and 1398 (GHL sync, server-side hooks) don't touch this path.

## Behaviour test (`tests/conversion-flow.js`, results `tests/conversion-flow-results.json`)
Form POST fulfilled inside the browser — nothing reached WordPress, GHL or Google.
| Scenario | Conversions |
|---|---|
| Page load | 0 |
| Submit clicked, empty form (no request sent) | 0 |
| Submit clicked, response pending 2 s | 0 |
| Success for an entry that doesn't exist (real server check → countable:false) | 0 |
| Successful, countable submission | **1** — send_to AW-17889231515/C8k6CJn4q6YdEJuFoNJC, transaction_id axiom-lead-990002 |
| Same entry again | 0 (skipped: duplicate) |
| Reload of the success URL | 0 |
| Failed submission (success:false) | 0 |

## Recommended minimal fix (pending owner decision in Google Ads)
Check Google Ads → Goals → Conversions → Summary for both actions: status, Primary/Secondary, goal, and which one the
campaigns optimise for. Then choose one:
- **A — campaigns use "Submit lead form (axiomsystems.systems/)" (6i7M):** change only the constant in snippet 1099 to
  `AW-17889231515/6i7MCMaIsqYdEJuFoNJC`; set C8k6 to Secondary (or remove it). One-line change; GHL sync, GA4, form untouched.
- **B — keep C8k6:** no site change; make C8k6 Primary in the lead goal and set 6i7M to Secondary/remove it so the goal
  doesn't show an inactive action.
Don't send to both while both are Primary in the same goal (double counting). If campaigns run in AW-17878870459, neither
label reaches them — confirm which account runs the ads.
Test after: logged out of WordPress, Tag Assistant on /get-started/, one real test submission with a test email (it will
sync to GHL as a contact), look for the `conversion` event after the success message. Conversions to an action can take
up to ~3 hours to show as recorded in Google Ads.

## Label → conversion action mapping (2026-10-28, read-only)
Owner confirmed in Google Ads: Primary "Submit lead form" = conversion type ID 7865039897 (Website, Manual event);
"Submit lead form (axiomsystems.systems/)" set to Secondary (page loads).
No prior record contains 7865039897. Decoding the labels (base64url → protobuf varints, 3-byte prefix skipped):
| Label | field 1 (conversion action ID) | field 2 (conversion ID) |
|---|---|---|
| C8k6CJn4q6YdEJuFoNJC (live tracker) | **7865039897** | 17889231515 |
| 6i7MCMaIsqYdEJuFoNJC (old) | 7865140294 | 17889231515 |
→ The live label belongs to the Primary manual-event action 7865039897. The label format is undocumented by Google, so
confirm once in the UI: Goals → Conversions → Summary → "Submit lead form" (URL shows ctId=7865039897) → Tag setup →
"Use Google Tag Manager": Conversion ID 17889231515, Conversion label C8k6CJn4q6YdEJuFoNJC.
