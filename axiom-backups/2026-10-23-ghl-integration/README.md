# Get Started form → GoHighLevel (Axiom CRM Sync)

Snippet **1398** (`AngieSnippets\AxiomCrmSync_1398`), published 2026-10-23, **mode: dry-run**.
Source of truth: `split/` (main, capture, delivery, verify, admin). Offline tests:
`php tests/harness.php split/main.php` (45 pass).

## Existing behaviour (inspected, unchanged)

| Piece | Where | Status |
|---|---|---|
| Form fields, validation, design | Jetpack form 1096 on page 1095 (`before/form-1096.json`) | untouched |
| Saved entries | Jetpack `feedback` posts (spam flagged by Akismet/Jetpack) | untouched |
| Email notification | Jetpack `wp_mail` to axiom.systems.co@gmail.com | untouched |
| Ads conversion | Snippet 1099: client-side `AW-17889231515/C8k6CJn4q6YdEJuFoNJC` after POST `/axiom/v1/lead-check`; Google tag GT-55XGH597 | untouched |
| Site config | `AXIOM_GHL_PRIVATE_TOKEN` constant | read only, not edited |

## Flow

1. `grunion_after_feedback_post_inserted` (priority 20): skips spam, other forms and
   non-published entries; saves a field snapshot to post meta and enqueues an Action
   Scheduler async job. No HTTP call here, all wrapped in try/catch, so the form,
   email and conversion are never slowed or broken.
   `grunion_pre_message_sent` (priority 5) only fills in missing snapshot fields.
2. The job (`axiom_ghl_sync_entry`) runs in the background with a per-entry lock:
   - **off**: holds the entry. **dry-run**: records a preview of the field names it would send; no
     HTTP request at all. **test**: only entries whose email is listed; uses the
     `axiom-integration-test` tag. **live**: all valid entries.
   - Upsert the contact (`POST /contacts/upsert`, matched on email/phone by GHL's
     duplicate rules); empty values are never sent, so nothing gets blanked.
   - Set `source` only if the contact was newly created.
   - Add one note per entry, marked "Axiom website entry #ID" and checked before a
     retry so it isn't duplicated.
   - Opportunity: default `workflow` (the GHL workflow creates it). An optional `api` mode
     creates one in "AXIOM | Standard Client Pipeline" / New Lead only if the contact
     has no open opportunity there.
   - Add the `axiom-new-lead` tag **last**, so a workflow fires once, after the data is
     in place.
3. Failures: 429/5xx/network errors retry at 1m, 5m, 30m, 2h and 12h, then the entry is marked
   failed and an alert goes to axiom.systems.co@gmail.com (entry ID and error only).
   4xx errors fail without retrying. Status for each entry: Tools → Axiom CRM Sync.

Token handling: used only in the server-side `Authorization` header; never stored in options,
meta, logs, REST output, alerts or the page source. Errors are sanitized. Writes are refused
by the HTTP wrapper unless they come from the delivery step in test or live mode.
SMS Consent field is never set; the snippet sends no messages itself.

## Live verification (read-only, `verify-2.json`)

Location WSbB7bUher6I1M2VNlZz = "AxiomSystems". All six read scopes OK. Pipeline
gWBaXOSSXt70oOgBlvXN, stage eb77750e-edd9-49b1-8186-a4bde1481599 stored. Tag
`axiom-new-lead` exists; the test tag will be created on the first test-mode delivery.
Write scopes (contacts.write, opportunities.write) can only be confirmed by the first
test-mode delivery.

## Field mapping (approved by owner 2026-10-23)

| Form field | GHL contact custom field |
|---|---|
| Business name | Business Name `4ZYDZGWO0Z3TUuZIgWqX` (also sent as companyName) |
| Current website | Current Website URL `HUtHUw3TbnQn9ZZD864k` (also sent as website) |
| Plan interest | Service Interest `o8EzFOVQrRoWE1OWqA5H` |
| Tell us about your business | Primary Business Challenge `EB63uFUp0FROWGBS2QGG` |

Name, email and phone go to the standard contact fields. An empty answer is never sent.

## Rollback

Set mode to Off (Tools → Axiom CRM Sync), or unpublish/delete snippet 1398. The form,
email and Ads conversion don't depend on it. Option `axiom_ghl_sync_settings`, meta
`_axiom_ghl_*`, and Action Scheduler group `axiom-ghl` can be removed afterwards.
