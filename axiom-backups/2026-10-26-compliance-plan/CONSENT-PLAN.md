# Get Started form consent wording, evidence and GHL enforcement (DRAFT — needs professional review)

Nothing here is live. Wording marked DRAFT must be reviewed by a qualified attorney or compliance professional before use.

## 1. Message categories (owner to confirm the list)
| Category | Examples in Axiom's system | Basis proposed | Review flag |
|---|---|---|---|
| Inquiry-related (informational) | Instant acknowledgment SMS/email; questions about the inquiry; scheduling; appointment confirmations, reminders, reschedule/cancel notices | Consent given by submitting the form with the disclosure below | Whether an automated *SMS* acknowledgment is covered by the submit-button disclosure under TCPA and Florida's FTSA |
| Marketing | Promotional follow-ups, offers, nurture/long-term, reactivation; any SMS whose purpose is selling services | Separate optional checkbox = prior express written consent | PEWC elements (clear disclosure, signature via checkbox, not a condition of purchase); FTSA hours/frequency limits |
| Review requests to Axiom's own clients | "Please review Axiom" | Classify with counsel | Commonly treated as marketing; also Google's review policies (no gating/incentives) |
| Email | Day 1 / Day 2 follow-ups, newsletters | CAN-SPAM: unsubscribe link + postal address in commercial emails | Footer content in GHL email templates |

## 2. Proposed form wording (DRAFT)
Under the Phone field (helper text):
> We'll use this number to reply to your inquiry.

Optional checkbox (unticked by default, not required to submit):
> ☐ Yes, Axiom Systems may send me occasional marketing text messages (offers and service updates) at the phone number
> above. Consent is not a condition of purchase. Message frequency varies. Msg & data rates may apply. Reply STOP to
> unsubscribe or HELP for help.

Disclosure directly above the submit button:
> By submitting this form, you agree that Axiom Systems may contact you by phone, text message and email about your
> inquiry, including automated messages. Message frequency varies. Msg & data rates may apply. Reply STOP to opt out or
> HELP for help. See our [Privacy Policy](/privacy-policy/) and [Terms of Service](/terms/).

Review flags: whether "including automated messages" in a submit disclosure is sufficient for the instant SMS; whether
the marketing checkbox wording satisfies TCPA/FTSA written-consent requirements (identity of seller, phone number,
automated technology); whether phone should remain a required field; carrier (A2P 10DLC) opt-in description must match this text.

## 3. Consent evidence (what gets recorded)
| Evidence | Where | Change needed |
|---|---|---|
| Checkbox value (yes/blank) | Jetpack entry (with timestamp, IP, user agent, page URL) | Add a checkbox field to form 1096 |
| Exact wording version | Hidden field "Consent version", fixed value e.g. `consent-v1-2026-11` (bump on every wording change; keep the wording archive in this repo) | Add hidden field to form 1096 (no code) |
| Same, in the CRM | GHL note (already lists form fields) + GHL "SMS Consent" field (`xBX0lq8bwM9v08uGmrG9`) | Snippet 1398: add the two labels to the note and map the checkbox to SMS Consent using the field's exact option value (read via verification first); never overwrite an existing "yes" with blank |
| Opt-outs | GHL DND (STOP) and email unsubscribe | None (GHL standard); confirm in test T4 |

Google Ads conversion and plan mapping are unaffected (snippet 1099 untouched; consent version is a static form value).

## 4. GHL enforcement (separate approval; owner makes or approves workflow edits)
1. In each production workflow, label every SMS step as inquiry-related or marketing.
2. Before each marketing SMS step: If/Else "SMS Consent is <yes option>" → send; else → skip (email path may continue if allowed).
3. Inquiry-related steps unchanged. DND/STOP continues to block all SMS automatically.
4. Commercial email templates: unsubscribe link + postal address.
5. A2P 10DLC: confirm brand/campaign status; campaign opt-in description, sample messages and privacy URL match the final wording.
Test: consent ticked vs unticked test leads → marketing SMS only for ticked; STOP → no SMS; instant response, Day 1/2
emails, opportunity creation unchanged.

## 5. Rollout order
Policies approved → wording approved → (staged) form fields + snippet 1398 mapping (offline tests, test-mode run) →
publish policies, footer links and form change together → GHL gating → tests.
