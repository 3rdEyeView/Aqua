# Get Started form -> GoHighLevel: verification & plan (2026-10-23)

Status: prerequisites phase. No CRM delivery code is installed. Nothing on the site changed except a temporary,
read-only probe snippet (1393, now deleted) and two labeled test submissions (entries 1394, 1395, now in Trash;
each sent one Gmail notification; Google tags were blocked in the test browser, so no Ads conversion fired).

## Verified on the live site
- Form: Jetpack form 1096 on page 1095, fields Name, Business name, Email, Phone, Current website (optional),
  Tell us about your business, Plan interest (hidden, set by snippet 1099 from ?plan=). Notification: Jetpack email to
  axiom.systems.co@gmail.com, subject "New Axiom Get Started lead". Submits by AJAX (admin-ajax).
- Hook order in the AJAX request (`probe/after-submit.json`):
  1. feedback post inserted (status publish, parent 1096)
  2. `grunion_after_feedback_post_inserted( $post_id, $fields, $is_spam, $entry_values )`
     $fields keyed g1095-name, g1095-businessname, g1095-email, g1095-phone, g1095-currentwebsite,
     g1095-tellusaboutyourbusiness, g1095-planinterest (Contact_Form_Field objects); $is_spam bool
  3. `grunion_pre_message_sent` -> wp_mail (Gmail notification, ~1.4 s) -> `grunion_after_message_sent`
- Snippets do load during the AJAX submission.
- Server: PHP 8.2.35; Action Scheduler 4.1.0 available (WooCommerce); WP-Cron enabled (traffic-driven);
  fastcgi_finish_request available; services.leadconnectorhq.com reachable from the server (~0.1 s).
- Not verifiable from here: anything inside GoHighLevel (no GHL access from this session; no token yet).

## Integration design (to build after prerequisites)
- Hook `grunion_after_feedback_post_inserted`; act only when parent = 1096, $is_spam = false, not a test entry.
  It only enqueues an Action Scheduler job (DB-backed) - no HTTP in the visitor's request. The Jetpack entry and the
  Gmail email are unaffected and happen regardless of CRM status.
- Worker: POST /contacts/upsert (non-empty fields only), POST /contacts/{id}/tags (adds, never replaces),
  one note per entry (marker "Axiom web entry #ID"; on an uncertain retry, existing notes are checked first).
  No opportunity API calls: the existing workflow remains the only thing that creates/moves opportunities.
- Idempotency: per-entry state meta (pending/sent/failed, attempts, contact ID, note ID) + a unique lock meta.
  Repeat inquiries reuse the same contact; duplicate quick resubmits do not re-add the tag.
- Retries: 1 m, 5 m, 30 m, 2 h, 12 h for timeouts/429/5xx; 4xx (other than 429) fail at once. Final failure emails
  axiom.systems.co@gmail.com with the entry link. Status visible in an admin page (Tools > Axiom CRM Sync) and in
  Tools > Scheduled Actions (group axiom-ghl).
- Modes, set by the owner in wp-config.php: off | dry-run | verify | test | live. Token never printed, stored or logged.
- No SMS/consent fields are set; the integration sends no messages.
