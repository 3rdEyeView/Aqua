# Decisions needed before implementation

| # | Decision | Needed for |
|---|---|---|
| 1 | Approve Turnstile + rate limiting ($0) as the spam solution; Akismet paid plan now or only if needed | Spam |
| 2 | Create a free Cloudflare account + Turnstile widget for axiomsystems.systems; send the site key; add the secret to wp-config.php as `AXIOM_TURNSTILE_SECRET` (Kinsta) | Spam |
| 3 | Legal entity name, business postal address, privacy/billing contact email | Policies, CAN-SPAM, A2P |
| 4 | Which messages are marketing vs inquiry-related (instant SMS, Day 1/Day 2 emails, any follow-up SMS, review requests) | Consent + GHL gating |
| 5 | Terms: Essential cancellation effective date, Lead Automation term, billing method/processor, refunds, late payment, price-change notice | Terms |
| 6 | Website/design on cancellation (export only, transfer fee, other) | Terms §8, must match Pricing |
| 7 | Liability cap, governing county, courts vs arbitration | Terms §13, §16 |
| 8 | Data retention periods | Privacy §8 |
| 9 | Keep Phone required? (marketing checkbox stays optional either way) | Form |
| 10 | Attorney/compliance reviewer and A2P 10DLC status in GHL | All legal wording |
| 11 | Review in repo only, or as unpublished WordPress draft pages | Review workflow |
