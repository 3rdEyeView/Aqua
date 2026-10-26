# Add-Ons refinement: Axiom Lead Automation consolidation (2026-10-26)

## Backups (taken before any change)
- `before/pages/<id>.json` — full REST export (context=edit) of the 7 live pages (952, 1068, 1074, 1085, 1095, 1013, 1031).
- `snippets/1099-main.before.php` — Get Started form snippet, verified byte-identical to live before editing.
- `audit/` — every text/link on the 7 pages before the change (`extract.py`).
- Yoast before-values for 1074 are in `seo_spec.py`.

## Changes
Copy edits: `copy_spec.py` (element ID, exact old text, new text). Applied with Elementor's manage-elements
(staged autosave -> preview -> publish); `build_ops.py` checked every old text against live first and
`diff_staged.py` confirmed only those elements changed.

Add-Ons (1074), same layout, sections in order Free -> Optional automation -> Recommended -> Premium advertising:
- Follow-Up Automation card (185b87e7) deleted; Lead Response card became **Axiom Lead Automation +$349/month**
  (headline "Never Miss an Opportunity.", six features, CTA "Add Lead Automation" -> /get-started/?plan=lead-automation).
  Card grid 39b068c4 now 2 columns on desktop (tablet/mobile stacking unchanged).
- Google Review Requests card: headline "Turn Great Service Into a Stronger Reputation.", new description, "Neutral Google
  review invitations" (no "after completed services" claim), CTA "Explore Website Plans" -> /pricing/.
- New tagline paragraphs 1173c05d / 466a0739 (inserted fresh; duplicating an element reuses its local style ID).
- Fine print: Lead Automation is a managed service, +$349 on top of Essential $299, included with Growth; usage/consent
  limits; reviews never guaranteed.
- Growth: new headline/description, "Axiom Essential ($299) + Axiom Lead Automation ($349) = $648/month ... Save $49/month",
  Plus list reworded to the requested items. Terms, price, CTA "Grow My Business", dark featured styling unchanged.
- Marketing: eyebrow "Premium advertising · Axiom Marketing", headline "More Leads. Better Opportunities. Real Growth.",
  new description, list = Google Ads strategy & management / Continuous campaign monitoring & optimization /
  Conversion-focused landing pages / Lead tracking & performance reporting (item 601ac531 removed); CRM lead tracking +
  automated follow-up kept; terms add Growth-vs-Marketing line, scope note and a no-guarantee line. $1,500 unchanged.
- "What's included where." map: Lead Automation row (+$349), Follow-Up row 787e8fa deleted, CRM row
  "Included with Lead Automation, Growth and Marketing", "Ongoing campaign management".
- Hero intro and the free-reviews notice reworded.
Pricing (1068): review blurb (no "each completed job" claim), fine print "neutral invitations", "Need automation, not the
full system?" block now describes Lead Automation at $349. FAQ (1085): one sentence now names Axiom Lead Automation ($349/month).
Snippet 1099: plan `lead-automation` = "Axiom Lead Automation — +$349/month"; `lead-response` and `follow-up-automation`
are now aliases of it (old links keep working, the original key is still recorded). Conversion tracking untouched.
post_content of 1074/1068/1085 re-synced (`sync_content.py`). Yoast title/description of 1074 (`seo_spec.py`).
Not changed: URLs, menus, header/footer, forms, Jetpack form 1096, GHL sync 1398, Site Kit/Ads/GA4, other pages.

## Rollback
- Pages: WordPress/Elementor revisions, or restore `before/pages/<id>.json` (see 2026-10-20 restore.py notes: write data,
  save once through Elementor, re-apply elementor_canvas, regenerate post_content).
- Snippet: save `snippets/1099-main.before.php` into 1099 with angie-update-snippet-files, then angie-publish-snippet.
- Yoast: set the before-values in `seo_spec.py`.

## Verification (live, after publish) — `tests/live-results.json`
- 7 pages x 4 widths (1440/1024/768/390): HTTP 200, no horizontal overflow, no JS errors.
- No public page text contains $149, $199, $647, $48, "Lead Response", "Follow-Up Automation" or "each completed job".
- Add-Ons shows $299, $349, $599, $648, Save $49 and $1,500. All internal links on the 7 pages return 200.
- Get Started form: ?plan=lead-automation, lead-response and follow-up-automation all show
  "Axiom Lead Automation — +$349/month" (hidden field records the original key); growth/essential/marketing unchanged.
  Empty submit blocked client-side (no AJAX). Lead-tracking script present with send_to AW-17889231515/C8k6CJn4q6YdEJuFoNJC.
- Google tag GT-55XGH597 and tel:+17275917527 present on all 7 pages.
- Screenshots: `tests/shots/before-*`, `staged2-*` (preview; uses the theme header, not elementor_canvas), `after-*`.

## Open items
- Legacy pages /services/ (107), /about-us/ (109), /elementor-9/ (9), noindexed post 393 and draft WooCommerce
  products still mention old offers; all are 301-redirected, noindex or unpublished, so they were left unchanged.
- No GoHighLevel workflow was checked for the old "Lead Response"/"Follow-Up Automation" plan text (GHL access is
  not available here). New leads now arrive with "Axiom Lead Automation — +$349/month (plan=...)" in Plan interest.
