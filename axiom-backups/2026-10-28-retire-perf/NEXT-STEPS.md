# Plugins, business details & landing pages (prepared 2026-10-28, nothing applied)

## A. Legacy plugin investigation
| Plugin | Front-end output now | Ties found | Verdict |
|---|---|---|---|
| WooCommerce 11.2.1 | 3 small deferred scripts (Site Kit dependency) | **Action Scheduler used by Axiom CRM Sync (1398)** for lead delivery/retries; WooPayments (card, Apple/Google Pay, Klarna, Affirm, Afterpay enabled), PayPal Payments, Stripe Tax, Shipping, Services, GLA, Pinterest, TikTok all depend on it; 0 orders | **Keep active for now.** Removal path below |
| Klaviyo 3.8.3 | none | no orders/customers to sync; its settings API is not readable from here | Safe to deactivate after you confirm Klaviyo isn't used (GHL sends your email) |
| Pinterest for WooCommerce 1.6.0 | none (no tag) | plugin reports health "approved", `ads_campaign_is_active: true`, no account ID, billing not set up, catalog 0 products, settings synced 2026-10-27 | Check Pinterest Business (campaigns/catalog), disconnect in the plugin, then deactivate |
| TikTok for WooCommerce 1.4.2 | none | no readable status | Check TikTok Business Center, disconnect, deactivate |
| Google Listings & Ads 3.10.0 | none | Merchant Center + Ads **disconnected** | Safe to deactivate now |
| WP Fastest Cache | — | Kinsta already caches at the edge | Usually redundant on Kinsta; review separately |

**Removing WooCommerce entirely** (when you want it): 1) confirm in WooPayments/Stripe that nothing is billed through the
site (client billing via Stripe payment links/GHL is separate and unaffected); 2) keep lead delivery reliable — either add
the standalone Action Scheduler plugin or switch snippet 1398 to WP-Cron with a Kinsta server cron; 3) deactivate GLA,
Pinterest, TikTok, Klaviyo, PayPal Payments, WooPayments, Stripe Tax, Shipping, Services, then WooCommerce; 4) update the
Privacy Policy (it names WooCommerce Analytics and order-attribution cookies); 5) re-run the regression. Snippets 1441/1442
keep working without WooCommerce. Deactivate first; delete plugins only after a quiet week.

## B. Business details needed for LocalBusiness/Organization schema and GBP (do not guess)
1. Legal business name/entity (e.g. "Axiom Systems LLC") — or confirm "Axiom Systems" is the trading name only.
2. Google Business Profile: link or Maps CID, primary category, and whether the address is **shown** or the profile is a
   **service-area business** (if hidden, schema gets areaServed only — no street address).
3. If shown: the exact address as on GBP. Service areas you list on GBP (e.g. Pinellas, Hillsborough, Pasco).
4. Business hours (as on GBP), or "by appointment".
5. Official profile URLs: Facebook page (Jetpack shows Facebook referral traffic, so one may exist), Instagram, LinkedIn,
   YouTube, X/TikTok — only ones you control and keep active.
6. Confirm contact details: (727) 591-7527 and axiom.systems.co@gmail.com (a domain email would look more established).
7. Optional: founding year, a square logo (≥ 512×512) for schema/GBP.
8. Pricing decision: Lead Automation is +$349/month on the site vs $350 in the brief.

## C. Recommended landing pages (draft plan — not built)
Both must carry original material; otherwise keep the content on Add-Ons.

### /google-ads-management/
- Target: "Google Ads management for small businesses", "Google Ads agency St. Petersburg/Tampa Bay", "PPC management".
- Title: `Google Ads Management for Small Businesses | Axiom Systems`; H1: "Google Ads management that turns clicks into calls."
- Sections: who it's for → what's included (from live Add-Ons: strategy & management, continuous monitoring & optimization,
  conversion-focused landing pages, lead tracking & reporting, CRM + automated follow-up) → how a campaign starts (audit,
  conversion tracking, launch, weekly optimization, monthly report) → pricing exactly as live ($1,500/month, ad spend paid
  directly, custom setup fee may apply, initial three-month agreement, no guaranteed results) → proof (needs you: an
  anonymized campaign example or report screenshot) → FAQ (min. budget, contracts, account ownership, tracking) → CTA
  `/get-started/?plan=marketing`.
- Schema: Service (provider = #organization, areaServed US). Links from Pricing/Add-Ons Marketing cards.

### /lead-automation/
- Target: "lead follow-up automation", "missed call text back", "speed to lead for small business".
- Title: `Lead Automation & Missed-Call Text Back | Axiom Systems`; H1: "Answer every lead in seconds — automatically."
- Sections: the problem (slow follow-up) → what it does (instant response, missed-call text-back, follow-up sequences,
  Axiom CRM pipeline) → a sample message timeline (needs your real workflow, compliant wording) → consent & opt-out (STOP/
  HELP, A2P) → pricing as live (+$349/month on Essential; included with Growth at $599) → FAQ → CTA
  `/get-started/?plan=lead-automation`.
- After launch: retitle Add-Ons around the comparison ("Add-Ons & Plan Comparison") so the pages don't compete.

## D. Follow-ups noticed
- The theme's 404/410 page (used for retired URLs) shows a very large logo with the message below the fold, and now also
  the site tagline. A simple branded 404 template would help visitors who arrive from old links.
- /category/uncategorized/ is empty and noindex; can return 404 the same way if you want.
