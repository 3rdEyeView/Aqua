# Implementation plan: privacy policy, SMS consent, spam protection (DRAFT — nothing applied)

Status: for owner and legal/compliance review. No legal wording is published and the live form is unchanged until approved.
All wording below is a starting draft, not legal advice.

## Current state (verified 2026-10-26)
- No privacy policy, terms or SMS policy page (all 404); no footer links to them.
- Form 1096 (Get Started): Name, Business name, Email, Phone (all required), Current website, message, hidden Plan interest.
  No consent text or checkbox. Jetpack stores each entry (with IP and user agent) and emails it.
- Snippet 1398 sends Name/Email/Phone + 4 mapped fields to GHL; GHL field "SMS Consent" (`xBX0lq8bwM9v08uGmrG9`,
  single option) exists but is never set.
- Production messaging (owner-verified): instant email + SMS, Day 1/Day 2 follow-up emails; appointment messages.
- Spam: Akismet 5.7.2 active with no API key; Jetpack marks nothing as spam; the integration already skips entries marked spam.

## Phase 1 — Spam protection (lowest risk, do first)
1. Connect Akismet or Jetpack anti-spam. Akismet's free plan is for personal sites; a business site needs a paid
   (commercial) plan, so the owner picks the plan. Settings → Akismet → enter key. No code change.
2. Verify (test contacts only): Name "akismet-guaranteed-spam" (Akismet's documented test value) + owner test email →
   entry marked spam, Tools → Axiom CRM Sync shows "spam (not sent)", no GHL contact, no Ads conversion
   (lead-check returns countable:false for spam). Then one normal test lead → still delivered.
3. Optional later (code change, separate approval): server-side guards in snippet 1398 before queueing — e.g. skip
   entries with an invalid phone or a URL-stuffed message — logged as "held: suspected spam" for manual release.
Rollback: disconnect the key.

## Phase 2 — Privacy policy and terms pages (drafts as WordPress drafts, not published)
1. Create two draft pages: /privacy-policy/ and /terms/ (owner/legal edit the text). Set the privacy page in
   Settings → Privacy only at publish time.
2. Privacy policy must cover (outline): who we are + contact (axiom.systems.co@gmail.com, (727) 591-7527, postal address);
   data collected (form fields, phone, email, IP/user agent, cookies); uses (respond to inquiries, scheduling, service
   delivery, marketing with consent); service providers (GoHighLevel/LeadConnector CRM and messaging, Google Analytics 4,
   Google Ads incl. conversion tracking and consent mode, Kinsta hosting, Jetpack/Akismet, email delivery); retention;
   choices (STOP, unsubscribe, access/deletion requests); children; changes.
   SMS clause required by carriers for A2P 10DLC (draft): "We do not sell, rent or share mobile phone numbers or SMS
   opt-in consent with third parties or affiliates for their marketing purposes. Text messaging originator opt-in data
   and consent are not shared with any third parties."
3. Terms (outline): services and plan terms already published (Essential: cancel anytime; Growth: no long-term contract,
   30 days' written notice; Marketing: initial three-month agreement, ad spend separate), billing, ownership (as on Pricing),
   and an "SMS terms" section: program name (Axiom Systems), message types, "Message frequency varies", "Msg & data rates
   may apply", "Reply STOP to cancel, HELP for help", carriers not liable for delayed or undelivered messages, link to privacy policy.
4. After approval: publish, add Privacy · Terms links to the footer of the 7 pages (Elementor edit, staged + previewed),
   and to the form disclosure.

## Phase 3 — SMS consent collection and recording (form + integration; legal review first)
Transactional vs marketing (for the reviewer):
- Inquiry-related (the person asked to be contacted): acknowledgment, questions about the inquiry, scheduling, appointment
  confirmations/reminders. Plan: a clear disclosure at the submit button.
- Marketing: promotional follow-ups, nurture, offers, re-engagement; review requests should be classified by the reviewer.
  Under TCPA and Florida's FTSA, automated marketing texts generally require prior express written consent, which must
  not be a condition of purchase; FTSA also restricts hours and frequency. Plan: a separate, optional, unticked checkbox.

Draft wording (DRAFT — for legal review):
- Disclosure under the button: "By submitting this form, you agree that Axiom Systems may contact you by phone, text
  message and email about your inquiry. Message frequency varies. Msg & data rates may apply. Reply STOP to opt out or
  HELP for help. See our Privacy Policy and Terms."
- Optional checkbox (unticked, not required): "Yes, send me occasional marketing text messages from Axiom Systems at the
  number above. Consent is not a condition of purchase. Msg frequency varies; Msg & data rates may apply. Reply STOP to cancel."

Recording (so consent can be proven):
1. Form 1096: add the checkbox field (label e.g. "Marketing texts") and a hidden field "Consent version" (e.g.
   "sms-v1-2026-11") set by snippet 1099 the same way it sets Plan interest. Jetpack stores value, time, IP, user agent.
2. Snippet 1398 (code change): include both fields in the GHL note; map the checkbox to "SMS Consent" using the field's
   exact option value (read via verification first); never send "no" over an existing "yes" from another source unless
   the reviewer wants that. Offline tests + test-mode run before live.
3. GHL (separate approval, owner-made): marketing SMS steps check SMS Consent; transactional steps unchanged; STOP keeps
   working via GHL DND. Emails: unsubscribe link + postal address in commercial emails (CAN-SPAM).
4. A2P 10DLC: confirm brand/campaign status in GHL; campaign description, sample messages and opt-in description should
   match the final form wording and privacy URL.

Tests (test contacts only): consent ticked / unticked → entry values, GHL note + field; marketing SMS only when ticked;
STOP → DND; existing lead path (instant email/SMS, follow-ups, opportunity) unchanged; Ads conversion still fires once.
Rollback: remove the new fields (entries keep their stored values) and restore snippet backups.

## Order and approvals
1. Phase 1 (key) → 2. Phase 2 drafts reviewed → 3. Phase 3 wording reviewed → publish pages + form change + snippet change
together, staged and tested → 4. GHL gating of marketing SMS. Each step needs explicit approval.
