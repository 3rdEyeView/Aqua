# End-to-end automation audit (2026-10-26)

Phase 1 was read-only toward GoHighLevel and the site. One exception, disclosed: the integration's
"Run verification (read-only)" action was run once. It makes only GET requests to GHL, but it refreshes the
stored verification snapshot in WordPress (`live/verify-7.json`). Nothing else was changed.

Evidence key: **V** = verified from real events/logs · **C** = configuration/code inspection · **N** = not yet tested ·
**X** = cannot be seen from this session (owner must check in GHL / Google Ads).

## Access available to this session
- WordPress REST (admin): pages, snippets, form 1096, form entries, CRM Sync status/verify, Site Kit settings, plugins.
- GHL: only through snippet 1398's fixed GET checks (location, contacts read, pipelines, tags, custom fields,
  workflow names + status). **No access to workflow triggers/actions/delays, calendars, phone numbers, conversations,
  opportunities by contact, A2P/10DLC status, or message logs.** PHP execution on the site is denied.
- Google Ads / GA4 UIs: no access. Gmail inbox: no access.

## Revision 1 (2026-10-26, after owner review) — supersedes "Findings" and the T0/T1 expectations below
The first pass mixed Axiom's production workflows with the CLIENT TEMPLATE library and checked the wrong pipeline.
Owner-supplied facts (not visible to this session): Axiom's "Instant New Lead Response" is published; its Create
Opportunity action targets **Axiom Sales & Client Acquisition / New Lead / Open**; duplicate opportunities are off; initial
email + SMS and Day 1 / Day 2 follow-up emails were received in an earlier test.

### Workflow classification (by name and status only; triggers are not visible here)
| Group | Workflows (status) |
|---|---|
| Axiom production | Instant New Lead Response (pub), Lead Follow-Up Sequence (pub), Missed Call Auto Text Back (pub), Appointment Confirmation Workflow (pub), Appointment Reminder Workflow (pub), Google Review Request Automation (pub) |
| CLIENT TEMPLATE | Appointment Cancellation Handler, Appointment Confirmation, Appointment Reminder, Google Review Request, Instant New Lead Response, Lead Follow-Up Sequence, Missed Call Text Back, Stop Lead Follow-Ups (all pub); Copy - … Facebook & Instagram DM Auto Response (draft) |
| Other / unclear | "\| Facebook & Instagram DM Auto Response" (pub; name looks like a template copy with the prefix removed); drafts: 1. New Lead Nurture (Fast 5), 2. Appointment Confirmation + Reminders, 3. Appt No Show, 4. New Sale - Send Review Request, 5. Long-Term Nurture, 6. Stale Leads, New Workflow - 2026-10-22…, Post-Appointment Follow-Up |

### Do CLIENT TEMPLATE workflows fire on Axiom production leads?
**No evidence either way is available to this session.** The API used here returns workflow names/status only; it
cannot show triggers, filters, enrollment history or messages. The first audit's "overlap" was an inference from names
and publish status and is **withdrawn** as a finding. Relevant fact: the snapshots show the templates did not exist at
2026-10-24 01:55 UTC (14 workflows, 0 templates) and existed by 2026-10-26 17:01 UTC (24, 9). Entry #1402 synced at
2026-10-24 03:48 UTC, so the earlier successful test may pre-date the templates and does not show whether they react
to production leads today. Deciding evidence (owner, read-only): contact `MWWqo11piJdDiATUmsze` → Workflows/Activity
(which workflows enrolled it), each template's created date, and each template's trigger + filters.

### Confirmed (verified from logs/code/settings)
| # | Item | Impact |
|---|---|---|
| C1 | Integration mode is **live**; repo docs said dry-run (docs corrected here). | Docs only |
| C2 | #1402 delivered end-to-end to GHL: contact created, source set, note added, `axiom-new-lead` tag added, 0 retries. | Working |
| C3 | The integration's **post-delivery opportunity check looks in the wrong pipeline**: `PIPELINE_NAME` = "AXIOM Standard Client Pipeline", stored pipeline `gWBaXOSSXt70oOgBlvXN`. Its "0 open / 0 total" for #1402 says nothing about Axiom Sales & Client Acquisition. It only logs; lead delivery does not use the pipeline. | Misleading status log; no lead impact |
| C4 | Site: no SMS-consent wording on form 1096; no privacy/terms page (404). Akismet active without a key. Site Kit Ads module AW-17878870459 vs lead conversion AW-17889231515. No Google Tag Manager. | Facts; impact listed under risks |
| C5 | Code on site = repo; offline harness 45/45; GHL read scopes OK; duplicate contact/opportunity settings off. | Working |

**Withdrawn:** the first pass's F2 (missing opportunity) and F3 (template overlap). **No confirmed failure in lead handling.**

### Not verifiable from this session (needs the GHL UI)
- U1 Opportunity for `MWWqo11piJdDiATUmsze` in Axiom Sales & Client Acquisition / New Lead. The available reads cannot query
  that pipeline (the check is hard-wired to the Standard Client Pipeline; arbitrary GET calls aren't possible).
- U2 Production workflow triggers (e.g. tag `axiom-new-lead` vs contact created), re-entry, stop-on-response.
- U3 Whether any template/other workflow enrolled production contacts (see above).
- U4 Missed-call number routing, calendars, reminders, review trigger and duplicate protection, A2P 10DLC status.
- U5 Google Ads receiving the conversions; which Ads account runs campaigns.
- U6 Whether anything in GHL reads Service Interest text (old "Lead Response"/"Follow-Up Automation" values).

### Potential risks (not failures)
| # | Risk | Why | How to settle |
|---|---|---|---|
| R1 | Templates enrolling production contacts | Same account; published; triggers unknown; created after the last production test | U3 checks; T1 workflow-history check |
| R2 | SMS compliance | No consent wording/privacy page while workflows text web leads | Owner/legal decision; A2P status in GHL |
| R3 | Spam reaching GHL and SMS | Akismet has no key; spam would sync live | Add key; T14 |
| R4 | Ads attribution | Two AW IDs | Confirm account (U5) |
| R5 | Repeat inquiries silent | Tag already present → depends on production trigger (U2) | T2 |
| R6 | Misleading opportunity-check log | C3 | Optional read-only fix below |

### Revised expectations for the test plan
- T0 (owner, read-only): U1–U4 above, especially the #1402 contact's workflow history and opportunity.
- T1: opportunity expected in **Axiom Sales & Client Acquisition / New Lead / Open**; workflow history should list only
  production workflows; integration log will still say "0 … in pipeline" until C3 is fixed — ignore that line.
- T10: review request expectations follow the production "Google Review Request Automation" trigger only.

### Optional fix (needs approval; changes snippet 1398 only, no GHL change)
Point the post-delivery check at Axiom Sales & Client Acquisition / New Lead and make it read-only report all open
opportunities for the contact across pipelines, so the integration log can confirm U1 by itself.

## Findings (original pass, superseded by Revision 1)
| # | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | High | **Integration mode is LIVE** (repo docs still said dry-run). Every non-spam Get Started entry now creates/updates a real GHL contact and adds `axiom-new-lead`. | V `live/crm-sync-status.json` |
| F2 | High | **Last live lead (#1402, 2026-10-24 03:48 UTC, message "test") reached GHL** (contact `MWWqo11piJdDiATUmsze` created, source set, note, tag) **but no opportunity existed in "AXIOM \| Standard Client Pipeline" ~10 min later** ("0 open / 0 total"). The integration relies on the Instant New Lead Response workflow to create it, so that step is broken or creates the opportunity elsewhere (another pipeline, or after a wait). The check does not alert anyone. | V entry log |
| F3 | High | **Overlapping published workflows.** 24 workflows (was 14 on 10-24). Nine `CLIENT TEMPLATE \| ...` workflows are **published in Axiom's own sub-account** next to Axiom's own: Instant New Lead Response, Lead Follow-Up Sequence, Missed Call Text Back, Appointment Confirmation, Appointment Reminder, Google Review Request, plus Appointment Cancellation Handler and Stop Lead Follow-Ups. Also `\| Facebook & Instagram DM Auto Response` is published. If triggers overlap, leads get duplicate texts/emails, and a second workflow could create a second opportunity or a conflicting one. | C names/status `live/verify-7.json`; triggers X |
| F4 | High | **No SMS consent or privacy disclosure on the form/site.** Form 1096 has no consent checkbox or wording; no privacy policy, terms or SMS policy page exists (404). Workflows text web leads automatically, and the `SMS Consent` custom field exists but is never set. Carrier A2P 10DLC rules and TCPA expect opt-in language at the point of collection. | C form 1096, site scan |
| F5 | High | **No spam filtering.** Akismet is active but has no API key, so bot submissions are treated as real, synced live to GHL and could trigger automated SMS to numbers bots typed in. | C akismet key empty |
| F6 | Medium | Two Google Ads IDs: Site Kit's Ads module loads **AW-17878870459**, while the lead conversion is sent to **AW-17889231515** (conversion "C8k6…", also a destination of GT-55XGH597). If campaigns run in 17878870459, form conversions aren't attributed there. No Google Tag Manager is installed (it's listed in the brief, but it isn't on the site). | C live HTML + Site Kit |
| F7 | Medium | Package mapping. Plan interest → GHL "Service Interest" (TEXT) works for all plans. New value `Axiom Lead Automation — +$349/month (plan=lead-automation)`; old links `lead-response`/`follow-up-automation` map to it. Any GHL workflow, opportunity name/value or smart list that matches the old "Lead Response"/"Follow-Up Automation" text is now stale. | C code + V form labels; GHL side X |
| F8 | Medium | Repeat inquiries from an existing contact are silent by design: the tag is already present, so no workflow restarts and no new opportunity is created; only a GHL note + the Gmail notification. The owner should confirm that's wanted (a "returning lead" internal notification is common). | C delivery.php |
| F9 | Medium | No booking path from the website (no calendar link; CALENDLY_URL empty). Appointments can only start from links sent by GHL messages or manual booking. | C snippet 1099, pages |
| F10 | Low | Opportunity check runs 5 min after delivery (it actually ran at +10 min) and only logs. A missing opportunity raises no alert. | C/V |
| F11 | Low | Test mode uses `axiom-integration-test`, which (correctly) starts no workflow, so Test mode can't exercise workflows. End-to-end tests must use Live with owner-controlled test identities. | C |
| F12 | Info | Code on the site is byte-identical to `../2026-10-23-ghl-integration/split/`; offline harness 45/45 pass; token defined; Action Scheduler present; duplicate contact/opportunity settings off; pipeline + "New Lead" stage IDs resolved; all 6 read scopes OK; GA4/Ads/consent-mode settings unchanged since 10-23. | V |

## Integration / workflow table
| Component | Current configuration | Evidence | Test method | Expected result | Pass / fail criteria |
|---|---|---|---|---|---|
| Get Started form (Jetpack 1096) | 7 fields; hidden Plan interest set from `?plan=`; email notice to axiom.systems.co@gmail.com | C; V (10-26 label test) | T1 | Entry saved (publish), Gmail notice | Entry visible in Feedback; 1 email |
| WP→GHL sync (snippet 1398) | **live**; upsert by email/phone, source on new contacts only, 1 note/entry, tag `axiom-new-lead` last; retries 1m/5m/30m/2h/12h, then alert email | V #1402; C | T1, T2, T11 | Log: contact created/updated → note → tag → sent | Log "sent", 0 retries; GHL contact has fields, note, tag |
| Field mapping | Business name, Current website, Plan interest→Service Interest, message→Primary Business Challenge | C; V (1400/1402 sent) | T1, T12 | Custom fields filled | Values match form |
| Opportunity | Created by GHL workflow (not the snippet); expected "AXIOM \| Standard Client Pipeline" / New Lead | **V broken (#1402)** | T0, T1 | 1 open opportunity, New Lead | Opp check log "1 open"; none in other pipelines |
| Instant New Lead Response (+ CLIENT TEMPLATE twin) | published ×2; trigger unknown | C names; X | T0, T1, T6 | Exactly 1 SMS + 1 email | Count = 1 each; sent from the right number/sender |
| Lead Follow-Up Sequence (+ twin) + Stop Lead Follow-Ups | published ×3 | C; X | T1, T3 | Follow-ups on schedule; stop on reply | No message after reply; no duplicates |
| Unsubscribe / DND | GHL standard STOP handling | X | T4 | DND set for SMS; nothing further | No SMS after STOP |
| Missed Call Auto Text Back (+ twin) | published ×2 | C; X (number routing unknown) | T5 | 1 text-back within ~1 min | Count = 1; only when call unanswered |
| Appointment confirmation / reminders / cancellation (+ twins) | Appointment Confirmation, Appointment Reminder, 3 CLIENT TEMPLATE versions published; "2. Appointment Confirmation + Reminders" draft | C; X | T7–T9 | 1 confirmation; reminders at set times; cancel stops reminders | No duplicate confirmations/reminders |
| Google Review Request (+ twin) | published ×2; trigger unknown | C; X | T10 | 1 neutral request after the completion trigger; never twice | Count = 1; no re-send on re-trigger |
| Google Ads conversion | snippet 1099: after Jetpack success + server check, `AW-17889231515/C8k6CJn4q6YdEJuFoNJC`, transaction_id `axiom-lead-<id>`; GT-55XGH597; consent mode on (EEA) | V (10-23 tests, Google blocked); C live HTML | T13 | 1 conversion per real entry | Tag Assistant shows the event; Ads shows 1 conversion after delay |
| Spam protection | Akismet without key | C | T14 (offline/owner) | Spam entries not synced | — currently fails by config |

## Test plan (Phase 2) — none executed yet (N)
Rules: owner-controlled identities only, e.g. email `axiom.systems.co+e2e01@gmail.com` (Gmail plus-addressing) and the
owner's own mobile; Name "E2E TEST 01"; message starting "E2E TEST – do not contact". After each test the owner adds tag
`axiom-e2e-test` in GHL. Clean-up at the end: mark test opportunities Lost/delete, delete test contacts, trash Jetpack entries.
Live mode is already on, so no mode change is needed. Each form test may record 1 Google Ads conversion (see T13).

| ID | Journey step | Steps | Expected | Where to verify |
|---|---|---|---|---|
| T0 | Pre-flight (owner, read-only) | In GHL open every published workflow; note trigger, filters, first actions, re-entry, "stop on response"; check contact `MWWqo11piJdDiATUmsze` opportunities in all pipelines + workflow history | Exactly one workflow per trigger; a known reason for F2 | GHL Automation, contact Activity |
| T1 | Inquiry → contact → opportunity → instant response | Submit `/get-started/?plan=lead-automation` | Entry, Gmail, sync "sent", contact + 4 fields + note + tag, 1 opportunity New Lead, 1 SMS + 1 email | WP Feedback, Tools → Axiom CRM Sync, GHL, phone, inbox |
| T2 | Duplicate submission | Same email/phone, submit again after 2 min | Same contact, 2nd note, no 2nd opportunity, no 2nd instant response | Same |
| T3 | Customer reply | Reply "Yes" to the instant SMS | Conversation in inbox, owner notified, follow-ups stop | GHL Conversations, workflow history |
| T4 | Unsubscribe / DND | New test lead, reply STOP | DND on SMS, no further SMS; email unsubscribe link works | Contact DND, workflow history |
| T5 | Missed call | From test phone call the advertised number, let it ring out | 1 text-back | Phone, Conversations |
| T6 | After-hours inquiry | Submit outside business hours | Behaviour matches the owner's rule (immediate vs next morning) | Phone, workflow history |
| T7 | Appointment booking | Book through the calendar link the workflow sends | 1 confirmation, reminders scheduled, opportunity stage → booked | Calendar, Conversations, pipeline |
| T8 | Reschedule | Move the appointment | Reminders re-timed, 1 reschedule notice | Same |
| T9 | Cancellation | Cancel | Cancellation handler runs once; reminders stop | Same |
| T10 | Completion → review request | Move the test opportunity to the completion stage; then move it again | 1 neutral review request; none on the repeat | Conversations, workflow history |
| T11 | Failed integration | Offline harness (done, 45/45). Live option needs approval: set mode Off → submit → "held" → back to Live → "Send held entries" | Entry held, then sent once; alert email path checked offline | CRM Sync log |
| T12 | Package mapping | Submit `?plan=lead-response`, `?plan=bogus`, no plan | Service Interest = Lead Automation (+ original key) / "Website (no plan selected)" ×2; no workflow branch misroutes | GHL contact fields |
| T13 | Ads conversion | During T1 use Google Tag Assistant | One `conversion` event with `axiom-lead-<id>`; appears in Ads (hours) | Tag Assistant, Google Ads Goals |
| T14 | Spam | After an Akismet key is added: Akismet test author "akismet-guaranteed-spam" | Entry = spam, CRM Sync not queued, no conversion | WP Feedback, CRM Sync |

## Recommended fixes (none applied; each needs owner approval)
1. F2/F3: in GHL, unpublish (set to draft) the nine `CLIENT TEMPLATE | …` workflows and the `| Facebook & Instagram DM Auto Response`
   in Axiom's own account, or confirm their triggers can't overlap; fix the opportunity step in Instant New Lead Response
   (pipeline "AXIOM | Standard Client Pipeline", stage "New Lead"); then re-run T1.
2. F4: add SMS/email consent wording (+ optional checkbox mapped to the `SMS Consent` field), and publish Privacy Policy and
   Terms pages before sending automated texts to new leads; check A2P 10DLC campaign approval in GHL (LC Phone).
3. F5: add an Akismet key (or enable Jetpack's anti-spam) before ad traffic; spam is already excluded from sync and conversions.
4. F6: confirm which Google Ads account runs campaigns; remove or align the unused AW ID in Site Kit.
5. F10: optional code change: email an alert when the 5-minute opportunity check finds none.
6. F7/F8: update any GHL references to the old add-on names; decide on a returning-lead notification.
