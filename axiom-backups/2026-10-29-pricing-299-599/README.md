# Public pricing: Essentials $299 / Growth $599 + Growth ad-spend disclaimer (2026-10-29)

## Backups (before any change)
`before/pages/` (952, 1068, 1074, 1085, 1095, 1013, 1031, 1413), `before/snippets/` (all 15 files), `before/wc-products.json`
(read-only listing). No pending Elementor drafts. Yoast before-values: below.

## Changes (staged → `diff_staged.py` showed only these → published)
Price swap $297→$299 / $597→$599 in every text element (`build.py`, asserted against the backup) plus wording in `spec.py`:
| Page | Changed |
|---|---|
| Pricing 1068 | Card prices; comparison header; **new disclaimer element 1afb9582 under "Google Search Ads campaign setup & ongoing management"**; Growth note 4aa219b8 → "The $599 subscription covers setup and standard management only. 3-month minimum…"; table row "Google Ads advertising spend" Growth = "Not included · paid separately"; fine print opens with the disclaimer; why-monthly + CTA facts |
| Add-Ons 1074 | Card prices; **disclaimer 41f33541 under "Google Search Ads setup & ongoing management"**; note 1a720fb3 drops the old "paid directly through Google Ads" sentence; CTA facts |
| Home 952 | Hero badge, work line, both plan cards, Growth card line "…Advertising spend not included"; **disclaimer 78176b8b under "Google Search Ads setup & ongoing management" in "Growth adds"**; home FAQ answer |
| FAQ 1085 | Prices in 4 answers; "Is the advertising budget included?" and "Does Growth include Google Ads management?" contain the exact disclaimer; cost answer "…paid separately to Google and/or Meta"; CTA facts |
| Get Started 1095 | "Essentials $299/mo · Growth $599/mo (includes Google Ads management; ad spend paid separately) · $0 setup fee" |
| How It Works 1013, Our Work 1031 | Prices |
| Snippet 1099 | Labels "$299/month" / "$599/month" (keys, aliases, tracking unchanged) |
| Snippet 1135 | Mobile-menu note $299 / $599 |
| Yoast | 952/1085/1095 descriptions, 1068 title+description ($297/$597 → $299/$599) |
| Share image | Featured image back to media 1439 ("From $299/month", identical render of `og/card.html`); media 1454 ($297) now unused |
| post_content | Regenerated from Elementor (`sync_content.py`) |

Disclaimer (exact): "Advertising spend is not included. We recommend considering approximately $500/month to start, but your
advertising budget is flexible and paid separately to Google and/or Meta." Style: 0.8125rem, line-height 1.5, aligned with
the list text (1.85rem), padding 0.55/0.75rem, radius 8px; dark card #C9D3E3 on rgba(255,255,255,.07), light cards #566174 on #F5F7FA.

Yoast before: 952 desc "…Essentials $297/month; Growth $597/month…"; 1068 "Pricing: Essentials $297/mo & Growth $597/mo | Axiom
Systems" / "Compare Axiom Essentials ($297/month) and Growth ($597/month…"; 1085, 1095 same text with $297/$597.

## $1,500 Marketing Management
Not on the public site (no public price since 2026-10-28). No WordPress/WooCommerce product exists for it (only legacy items
trashed 2026-10-27). Stripe is not reachable from this session: nothing in Stripe was viewed or changed. The Get Started
`?plan=marketing` link still records "Advanced Marketing — Custom quote" for private proposals.

## Verification (`tests/live.js` → `tests/live-results.json`)
8 pages × 1440/1024/768/390: 200, no overflow, 0 JS errors. No $297/$597/$1,500/$349 in text or HTML; $299 and $599 present;
exact disclaimer visible on Pricing (card + fine print), Add-Ons, Home; in FAQ answers (FAQPage JSON-LD). Mobile menu note
$299/$599. Each page: GT-55XGH597 ×1, AW config ×1, chat widget ×1, lead send_to C8k6… unchanged; every ?plan= label/hidden
field correct; utm/gclid preserved; empty submit sends nothing; all links 200. Snippets other than 1099/1135 byte-identical.
No CRM Sync, GHL workflow, conversion or Google Ads campaign was touched.

Rollback: WordPress revisions or `before/pages/`; PATCH `before/snippets/1099-main.php` / `1135-main.php` + publish; Yoast values above.
