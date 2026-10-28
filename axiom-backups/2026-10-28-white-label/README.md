# White-label branding cleanup (2026-10-28)

Goal: no customer-facing references to the third-party software behind Axiom's services. Technology unchanged.

## Backups (before any change)
`before/pages/` (952, 1068, 1074, 1085, 1095, 1013, 1031, 1413), `before/snippets/` (all 15 snippet files),
`before/form-1096.json`. No pending Elementor drafts existed. Rendered audit before/after: `tests/audit-*.json`.

## Audit (tests/audit.js: visible text, title/meta, JSON-LD, alt/title/aria/placeholder, form markup; 9 URLs × 1440/390)
| Where | Finding | Action |
|---|---|---|
| Home, Pricing (card + table), Add-Ons, FAQ (2 answers) | "GoHighLevel CRM …" (visible + FAQ JSON-LD + post_content) | Replaced (below) |
| How It Works, Our Work, Get Started, 404, header/footer, mobile menu | none | — |
| Form 1096 labels, placeholders, thank-you message | none | — |
| Yoast titles/descriptions, share image | none | — |
| Privacy Policy 1413 (elements a871dff, 91782a4, c02aede) | Names GoHighLevel/LeadConnector, Kinsta, Cloudflare, WordPress, Jetpack, WooCommerce as service providers / cookie sources | **Not changed**: legal disclosure; owner/attorney decision |
| `<meta name="generator">` on every page | WordPress, WooCommerce, Site Kit, Elementor (page source only, not displayed) | Not changed (would need a code change); optional follow-up |
| CSS classes, script URLs, hooks in snippets (jetpack, elementor, cloudflare) | internal code | Not changed (per brief) |
| GHL chat widget (LeadConnector) | widget UI/branding is configured in GHL and not visible from here | Owner check |

## Changes (Elementor, staged → diff showed only these elements → published; post_content regenerated)
| Page | Element | New text |
|---|---|---|
| Home 952 | 3df2dc9f "Growth adds" list | Axiom CRM & Lead Management Pipeline |
| Home 952 | 515a1ed2 home FAQ answer | "…Growth ($597/month) adds access to the Axiom CRM, advanced lead follow-up automations, appointment scheduling and Google Search Ads…" |
| Home 952 | 121a7a6e Growth card | "Your complete customer acquisition and business growth system. Includes access to the Axiom CRM, advanced lead follow-up automations, and Google Ads management." |
| Pricing 1068 | 1d2346d3 Growth card, 55fc4587 comparison row | Axiom CRM & Lead Management Pipeline |
| Add-Ons 1074 | 78df7460 Growth list | Axiom CRM & Lead Management Pipeline |
| Add-Ons 1074 | 3f549d91 Growth card | "Everything in Essentials, plus access to the Axiom CRM, advanced lead follow-up automations, and Google Ads management, …" |
| FAQ 1085 | 6317b72a "What's included in Growth?" | "…plus the Axiom CRM & Lead Management Pipeline, …" |
| FAQ 1085 | 790f840d / 16efd0f6 | "What is the Axiom CRM?" — preferred CRM description; "runs on established, proven business software" (no proprietary claim) |
| FAQ 1085 | 2cb69bc4 "How do the automations work?" | "…in the Axiom Automation Platform…", "…your Axiom CRM pipeline…" |

Not touched: snippets (all byte-identical), CRM Sync, form, tracking/conversions, plugins, GHL workflows, Yoast, Privacy Policy.

## Verification (tests/)
- Provider audit after: all public pages clean except the Privacy Policy disclosures (and invisible generator meta).
- `live.js`: 8 pages × 4 widths 200 / no overflow / no JS errors; $297 / $597; GT-55XGH597 ×1, AW config ×1, chat widget ×1;
  lead send_to unchanged; every ?plan= label/hidden field correct; empty submit blocked; links 200.
- `look.js`: Growth still lists Google Search Ads setup & management; "not included in the $597 subscription" ad-spend note present.

Rollback: WordPress revisions, or restore `before/pages/<id>.json`.
