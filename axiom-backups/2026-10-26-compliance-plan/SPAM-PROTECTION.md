# Spam protection for the Get Started form — options and recommendation (DRAFT, nothing applied)

## How the form works today (verified)
- Jetpack form 1096, rendered on /get-started/ by snippet 1099, submitted by AJAX (`admin-ajax.php?action=grunion-contact-form`).
- Jetpack runs `apply_filters( 'jetpack_contact_form_is_spam', false, $akismet_values )` before saving (Jetpack forms source):
  `true` → entry saved with status **spam**, no notification email; a `WP_Error` → submission **rejected** (nothing saved).
- Spam-status entries are already ignored by the GHL integration (snippet 1398) and by the Ads conversion check
  (`lead-check` returns countable:false), so anything flagged spam never reaches GHL or Google Ads.
- Akismet 5.7.2 is active with no key, so the filter currently never flags anything.

## Options
| Option | Stops | Cost | Fit with our form / integration | Downsides |
|---|---|---|---|---|
| Cloudflare Turnstile | Bots and scripted posts (must solve a browser challenge; token verified server-side, single use, 5-min validity) | Free plan: up to 20 widgets, unlimited challenges; works without moving DNS to Cloudflare | Needs a small snippet: widget in the form + Siteverify check in `jetpack_contact_form_is_spam`. No change to 1398 or the conversion code | Loads a Cloudflare script on /get-started/ (privacy-policy mention); visitors blocking scripts can't submit (show call/email fallback) |
| Akismet (paid) | Content spam incl. human-typed spam, learned from network data | Free "Personal" key is not allowed for business sites; paid plans reported from about $9.95/month (confirm at akismet.com/pricing) | Zero code: add key; Jetpack already calls it | Ongoing cost; occasional false positives land in Spam (lead silently not synced → review Spam weekly) |
| Server-side rate limiting | Floods/repeats from one IP, email or phone | Free (our code) | Same snippet as Turnstile, same filter; marks excess entries as spam (kept for review) | Doesn't stop low-volume bots alone; IP must be the real client IP behind Kinsta's edge (verify in staging) |
| Honeypot / time-trap | Naive bots | Free | Same snippet | Weak against modern bots; Turnstile covers it |

## Recommendation (lowest cost that covers the risk)
**Turnstile + light rate limiting in one new snippet ("Axiom Form Protection"), $0/month.** Add paid Akismet later only if
human-typed spam appears. Keeps the GHL integration (1398) and the Ads conversion snippet (1099) untouched.

Rules:
1. Applies only to form 1096 submissions.
2. Missing/invalid Turnstile token → `WP_Error` ("Please confirm you're not a robot and try again, or call (727) 591-7527.")
   → nothing saved, no GHL contact, no conversion; the visitor can retry.
3. Cloudflare unreachable (timeout/5xx) → **fail open**: accept, note "turnstile unavailable" on the entry, so real leads aren't lost.
4. Rate limit: more than 3 submissions per IP in 10 minutes, or more than 3 per email/phone in 1 hour → flagged **spam**
   (kept in Feedback → Spam for review). Legitimate duplicate inquiries (test T2) stay within the limit.
5. Secret key in `wp-config.php` constant `AXIOM_TURNSTILE_SECRET` (owner adds it, like the GHL token); site key is public.
   Secret never logged or output.

Rollout without risking leads:
1. **Shadow mode** (1 week): widget shown, token verified and the result logged on each entry, nothing blocked.
2. Review: real leads all "pass"? Then **enforce mode**.
3. Rollback at any time: unpublish the snippet (form returns to today's behaviour).

Google Ads: no change to tags or the conversion script. The conversion still fires only after Jetpack reports success
for a non-spam entry; rejected or spam submissions don't fire (same as today). Verified in tests with Tag Assistant.

Tests (test contacts only): normal submission (entry, GHL contact, 1 conversion); no token / forged token (rejected, no
entry, no conversion); 4 quick submissions from one browser (4th → Spam, not synced); Turnstile script blocked (error
message with phone/email); IP logging check behind Kinsta; mobile + desktop layout; existing workflows unaffected.

Costs: Turnstile $0 · rate limiting $0 · Akismet optional, ~$9.95/month reported (confirm) · implementation: one snippet.
