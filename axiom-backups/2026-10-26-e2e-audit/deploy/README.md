# A1 deployment: snippet 1398 opportunity check → production pipeline (2026-10-26)

Approved by owner: A1 only. A2–A7 not touched.

## Pre-deploy
- Backup: `pre-deploy-snippet-1398.json` (all 5 live files) = `../patch/backup-live/` byte-for-byte; settings in `pre-deploy-status.json`
  (mode live, test_emails empty, field map ×4, pipeline gWBaXOSSXt70oOgBlvXN).
- Change scope (`../patch/snippet-1398.patch`): main.php constant; verify.php pipeline reporting + admin `check` action;
  delivery.php opportunity-check function. capture.php and admin.php unchanged; contact upsert, source, note, tag, retries,
  alerts, modes and field map untouched. The check calls `api('GET', …)` without write permission.
- Security review of `check`:
  - Authentication/authorization: same route as the existing verify/settings actions; `permission_callback` =
    `current_user_can('manage_options')` (administrators only, application password or logged-in admin).
  - CSRF: WordPress REST cookie auth requires a valid `X-WP-Nonce`; without it the request is treated as logged out
    (core `rest_cookie_check_errors`), so a cross-site POST fails the permission check. Application-password requests
    are not cookie-based. POST only; GET on the route returns status and never runs a check.
  - Input: `entry` cast to int and must be a Get Started (form 1096) entry, else 400. Entries never synced make no request.
  - Output: `{entry, opportunity_check}`; the line holds counts and GHL pipeline IDs only — no contact data, token or headers.
    API errors are sanitised and truncated by the existing `api()`.
  - Side effects: one GET to GHL; updates that entry's sync log meta.

## Deploy
Files uploaded via the snippet REST endpoint (exact bytes), read back = `../patch/split/` for all 5 files; offline harness
on the uploaded bytes 54/54 (`harness-uploaded.txt`); then published.

## Post-deploy results
| Check | Result |
|---|---|
| Home / Get Started / Add-Ons | 200 |
| Live files = patch | yes (`post-deploy-snippet-1398.json`) |
| Token / Action Scheduler / mode | defined / available / **live** |
| Field map, test emails | unchanged |
| Verification (`verify-8.json`, GET only) | all 6 checks OK; production pipeline **29sSMvlcvPPuSxaEzoVb** "Axiom Sales & Client Acquisition" (New Lead, Appointment Booked, Follow Up, Won), New Lead stage `14423499-01c7-4ca3-91b2-d10ea619186a`, now stored |
| Re-check #1402 (`check-1402.json`) | **1 open / 1 total in Axiom Sales & Client Acquisition**; no opportunities in any other pipeline |
| Security (`security-tests.txt`) | no auth 401; forged cookie without nonce 401; wrong password 401; non-entry / bad / missing id 400; unsynced spam entry → no request; response has no PII/token |

Contact creation/update, notes and tags: code unchanged (diff) and covered by the offline tests (upsert → source on new
contact → note → tag, tag last; existing contact keeps its source; retries; no opportunity writes). A live confirmation
needs a new test submission, which wasn't part of A1.

## Rollback
Upload `../patch/backup-live/{main,verify,delivery}.php` to snippet 1398 and publish. The stored pipeline_id
then points at the production pipeline; to restore the old value too, run verification with the old code.
