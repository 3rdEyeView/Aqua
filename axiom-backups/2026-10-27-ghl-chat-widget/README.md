# GoHighLevel (LeadConnector) chat widget — snippet 1412 (2026-10-27)

## Method
New standalone Angie code snippet **1412 "Axiom GHL Chat Widget"** (`snippet/main.php`): prints the exact vendor tag once
on `wp_footer` (priority 100) on every public page. Same mechanism as the existing mobile-menu snippet 1135; survives theme
updates; no plugin. Skipped in wp-admin, the Elementor editor preview, feeds, embeds, REST and AJAX. No other file, page,
form, tracking, CRM or consent setting was changed.

Exact tag (unchanged):
`<script src="https://widgets.leadconnectorhq.com/loader.js" data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" data-widget-id="6adf9aa5388cb81c665a7bda" data-source="WEB_USER"></script>`

## Before
- No LeadConnector widget on any page (7 pages + 404) or in any snippet (1398 only calls the GHL API server-side).
- Backup: `before/` — all 7 snippet sources, page baselines (scripts, Google tag configs, lead send_to, form inputs,
  plan label, phone links, nav), CRM Sync settings, Form Protection settings, page 1095 export.

## Deployment
Uploaded file read back = `snippet/main.php`; offline tests (`harness.php`) pass; published.
Kinsta served a cached /get-started/ without the tag; an empty REST save of page 1095 (content verified identical
before/after) purged it; within ~15 s the cached page carried the tag.

## Verification (`after/`, `tests/regression.json`)
| Check | Result |
|---|---|
| Exact tag on /, /pricing/, /add-ons/, /faq/, /get-started/ (also ?plan=), /how-it-works/, /our-work/, 404 | exactly 1 per page, widget ID 6adf9aa5388cb81c665a7bda; also on plain cached URLs |
| Duplicates | none (one tag per page; static guard per request) |
| Feed | no tag |
| Everything else on each page | identical to baseline (script list differs only by the loader; GT-55XGH597 / AW-17878870459 config; lead send_to AW-17889231515/C8k6…; form inputs; plan label; tel links; nav) |
| Other snippets (1099, 1134, 1135, 1377, 1390, 1398, 1411) | byte-identical |
| CRM Sync (live, pipeline 29sSMvlcvPPuSxaEzoVb, field map) / Form Protection (log, no keys) | unchanged |
| Desktop 1440 + mobile 390, 7 pages | 200, no overflow, **0 JS errors** (with the widget host blocked), mobile menu opens, Get Started label "Axiom Lead Automation — +$349/month", empty submit blocked client-side (no AJAX) |
| Fixed elements | only the top header; nothing fixed in the bottom-right corner where the bubble sits |

Not verifiable from this environment: the widget itself rendering (widgets.leadconnectorhq.com is blocked here) and its
consent text. Owner checks below.

## Owner checks (desktop + phone)
1. Open the site: chat bubble appears once, bottom corner, on several pages.
2. On a phone at /get-started/, scroll so the "Get Started" button is near the bottom: the bubble should not block tapping it
   (if it does, adjust the widget position/offset in GHL — no site change needed).
3. Open the widget: read the consent/legal text and links.
4. One test chat with a test name/phone/email → GHL Conversations; note which workflows enrol the new contact.
5. GHL: re-run the chat widget / compliance verification.

## SMS compliance notes (no settings changed)
- The website still has no Privacy Policy or Terms page (404) and the Get Started form has no SMS disclosure; drafts are in
  `../2026-10-26-compliance-plan/`. A2P reviewers usually check the consent text at every phone-collection point (form and
  chat widget) and the privacy/terms links.
- The chat widget is a second phone-collection point. Its consent text and links are configured in GHL; if they point to
  /privacy-policy/ or /terms/ they will 404 until those drafts are published.
- Chat contacts don't pass through the Get Started form, Turnstile or the Ads lead conversion. Any GHL workflow triggered by
  contact creation or live-chat replies may enrol them (owner check 4).

Rollback: unpublish snippet 1412 (and let the page cache refresh).
