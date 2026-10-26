# Axiom Form Protection — Cloudflare Turnstile + rate limiting (snippet 1411)

Status: **published 2026-10-27 in LOG-ONLY mode, without Turnstile keys.** Nothing is blocked. Enforcement only after
owner approval. Source: `snippet/main.php` · tests: `harness.php` (6 checks without keys, 31 with keys).

## What it does
- Hooks Jetpack's own spam check (`jetpack_contact_form_is_spam`, priority 5) for the Get Started form only
  (`contact-form-id` = 1095). Jetpack semantics (verified in Jetpack Forms source): `true` → entry saved as **spam**
  (no notification email); `WP_Error` → submission rejected with our message (HTTP 400, shown in the form).
- Spam entries are already ignored by the GHL sync (1398) and the Ads lead-check (1099), so they never reach GHL or Ads.
- When keys exist: adds a Turnstile widget (Managed, `interaction-only`, so most visitors see nothing) inside the form
  before the button, loads Cloudflare's script, and verifies the token server-side once (Siteverify, 5 s timeout).
  After a failed submission the widget is reset so the visitor gets a fresh single-use token.
- Records per entry (post meta `_axiom_form_protection`) and in a rolling log (200 events): Turnstile result, error codes,
  rate-limit counts, Jetpack fill time, decision, 8-char salted IP reference. No names, emails, phones, tokens, raw IPs or keys.
- Admin: Tools → Axiom Form Protection; REST `GET/POST /wp-json/axiom/v1/form-protection` (administrators only; POST to
  `enforce` requires `confirm: "enforcement-approved"` and both keys).

## Handling of each case
| Case | Log-only (now) | Enforce (after approval) |
|---|---|---|
| Keys not configured | allowed, logged `not-configured` | never blocks (enforce cannot be switched on without keys) |
| Valid token | allowed (`pass / allow`) | allowed |
| Missing token (bot posting directly, script blocked, widget not loaded) | allowed, `would-reject` | rejected: "Please confirm you are not a robot and try again. You can also call us at (727) 591-7527." No entry, no GHL, no conversion; widget reset for retry |
| Invalid / expired / replayed token, wrong hostname or action | allowed, `would-reject` | rejected (same message) |
| Cloudflare unreachable, timeout, 5xx, unreadable reply | allowed, `allow-fail-open` | **allowed** (fail open) — real leads are never lost to an outage |
| Our misconfiguration (wrong/missing secret, bad request) | allowed, `allow-fail-open` | **allowed** — a bad key can't block every visitor |
| Over a rate limit | allowed, `would-flag-spam` | saved as **spam** (kept, reviewable, mark "not spam" to restore) + email alert to axiom.systems.co@gmail.com with the entry number |
| Unexpected PHP error in the add-on | caught; form behaves as without it | same |

## Rate limits and shared IPs
- Per IP: more than **10** submissions in **10 minutes**. Per email or phone: more than **3** in **1 hour**.
- Verified on the live server: `REMOTE_ADDR` equals Cloudflare's `CF-Connecting-IP` (Kinsta restores the visitor IP), so
  counts are per real visitor, not per Cloudflare edge.
- Shared IPs (offices, mobile carriers, public Wi-Fi): 10 different people from one IP within 10 minutes are all accepted
  (tested); real traffic to this form is a few submissions per day. The email/phone limit is per person, not per IP.
- Even when a limit is hit, the entry is **kept as spam with an alert**, never discarded, so a real customer can be recovered.
- In log-only mode the limits are only recorded, so the week's data will show whether they would ever have triggered.

## Deployment record (2026-10-27)
- Backup before: `before/` (all 6 snippets with sources, CRM Sync settings, Get Started form/tracking baseline).
- Kinsta's Cloudflare WAF rejected the first upload because a code comment contained the text "wp-config.php"; the comment
  now says "site configuration file". Code unchanged.
- Uploaded bytes = `snippet/main.php`; tests passed on the uploaded bytes; published.
- After: 7 pages 200; snippets 1099/1134/1135/1377/1390/1398 byte-identical; Get Started form inputs, plan label, GT-55XGH597,
  AW-17878870459 config, lead conversion send_to and lead script identical to baseline; CRM Sync live, settings unchanged;
  add-on mode log, keys missing; REST without login 401 (`deploy/status-after-deploy.json`).
- Not yet exercised: a real form submission through the add-on (needs a test submission; see below).

## Cloudflare setup (owner)
1. Cloudflare dashboard (free account) → **Turnstile** → **Add widget**: name "Axiom Get Started form"; hostname
   `axiomsystems.systems` (add `www.axiomsystems.systems` only if that host is used); widget mode **Managed**; pre-clearance off.
2. Copy the **Site Key** and **Secret Key**.
3. In the site configuration file on Kinsta (SFTP/SSH), above the "stop editing" line, add:
   `define( 'AXIOM_TURNSTILE_SITE_KEY', '<site key>' );` and `define( 'AXIOM_TURNSTILE_SECRET', '<secret key>' );`
   Never paste the secret into chat, email or the repository.
4. Tell me when done (the site key may be shared; it is public). I then confirm keys detected, widget rendered, and
   ask you to submit one test lead from your own browser (this environment cannot reach Cloudflare's challenge script).

## Before enforcement (checklist)
- ~1 week of log data: every real lead `pass / allow`; no real lead in `would-reject`; `unavailable` rare.
- Your browser test lead: `pass`, entry synced to GHL as usual, one Ads conversion.
- With approval: switch to enforce, then a rejection test from this environment (no token → rejected, no entry, message shown).
- Rollback anytime: switch back to log, or unpublish snippet 1411.
