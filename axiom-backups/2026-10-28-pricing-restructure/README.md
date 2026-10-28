# Pricing restructure: Essentials $297 / Growth $597 (2026-10-28)

New public pricing: **Axiom Essentials $297/month** and **Axiom Growth $597/month** (includes Google Search Ads
management), $0 setup fee, first month due at signup. The $1,500 Marketing package, the $349 Lead Automation add-on
and the $299/$599 prices are no longer published. Add-ons are by custom quote.

## Backups (taken before any change)
- `before/pages/<id>.json`: full REST export (context=edit) of 952, 1068, 1074, 1085, 1095, 1013, 1031, 1413, the
  legacy pages 9/107/109/230, demos 1184/1247 and post 393.
- `before/snippets/`: every snippet file (1099, 1134, 1135, 1377, 1390, 1398×5, 1411, 1412, 1438, 1441, 1442).
- `before/html/`: rendered live HTML of the 8 public pages. `before/media-1439.json` + `before/axiom-systems-share.jpg`.
- `audit/`: all text/links per page before the change (`extract.py`). Yoast before-values: `seo_spec.py` (BEFORE).
- No staging site is reachable from this session (environment = production only). Changes were staged as Elementor
  autosaves, checked with signed preview links + `diff_staged.py`, then published. Kinsta's own backups were not visible
  here (owner to confirm a current Kinsta backup exists).

## Changes (all published 2026-10-28 ~18:30 UTC)
| Page | What changed |
|---|---|
| Pricing 1068 | Hero; "included with every plan" strip; Essentials card ($297, new feature list incl. missed-call text-back); Growth card ($597, Recommended, 3-month minimum, CRM/automations + "Customer acquisition · Google Ads" group, reporting, priority support, ad-spend note, CTA "Get Started"); Marketing card deleted; grid 2 columns (desktop); new **comparison table** (`compare_table.py`, 15 rows incl. setup fee, first payment, ad spend, SMS usage, commitment; CTAs ?plan=essential / ?plan=growth); fine print (ad spend, one Search program, custom quote, SMS usage wording from owner, activation, no guarantees); why-monthly + add-on teaser + CTA facts |
| Add-Ons 1074 | Hero "Go further when you're ready."; two cards now show what Essentials / Growth already include; Growth price-math block ($648/Save $49) and Marketing card ($1,500) deleted; "What's included where" map → add-on catalogue: Advanced Advertising Services, Advanced Business Automations, Website Enhancements (Custom quote / Available by consultation), links → `/get-started/?plan=custom-quote`; CTA |
| Home 952 | Eyebrow, H1 "Attract More Customers. Capture More Leads. Automate Your Growth.", owner's supporting message, hero CTA "Get Started" → /get-started/, $297 badge naming Growth + Google Ads; pricing section = two cards (Essentials $297, Growth $597 "Recommended", Google Ads named) with "Included in every plan" / "Growth adds" lists below; 2 home FAQ answers |
| FAQ 1085 | All 12 required questions answered (8 new accordion items + rewrites); "What's included" group ordered Essentials → Growth → Google Ads → CRM → automations → phone number → results; CTA facts. FAQPage schema regenerates from the accordion (1 block, verified) |
| Get Started 1095 | Price line, intro (first month due at signup), "Every Axiom plan includes" list |
| How It Works 1013 | $297, "from $297", Growth/Google Ads mention |
| Our Work 1031 | Essentials card $297, CTA "Get Started" |
| Snippet 1099 | Plans: essential = "Axiom Essentials — $297/month", growth = "Axiom Growth — $597/month", new custom-quote = "Add-On or Custom Solution — Custom quote", marketing = "Advanced Marketing — Custom quote"; aliases essentials→essential, lead-automation/lead-response/follow-up-automation→growth (original key still recorded in the hidden field) |
| Snippet 1135 | Mobile-menu note: "Plans from $297/month with essential automations included. Growth ($597/month) adds Google Ads management." |
| SEO | Yoast title/description for 952, 1068, 1074; description for 1085, 1095 (`seo_spec.py` AFTER). New share image media **1454** (`og/`, "From $297/month") as featured image/og:image on the 7 pages; post_content regenerated from Elementor (`sync_content.py`) |

Not changed: header/nav/footer, Privacy Policy, forms (Jetpack 1096 fields), GA4/Ads tags, conversion label, Site Kit,
CRM Sync 1398, Form Protection 1411, chat widget 1412, SEO Signals 1438, redirects 1390/1441, performance 1442, menus,
URLs, ownership FAQ wording.

## Verification (`tests/live.js` → `tests/live-results.json`)
- 8 pages × 1440/1024/768/390: HTTP 200, no horizontal overflow, 0 JS errors.
- No $299, $599, $1,500, $349, $648, Save $49, $149, $199, "Lead Automation", "Axiom Marketing", "Axiom CRM",
  "No long-term contract" in page text or HTML (incl. JS-built mobile menu). $297/$597 present.
- Each page: exactly 1 GT-55XGH597 loader, 1 AW-17878870459 config, 1 GHL widget; tel link; lead tracker with
  send_to AW-17889231515/C8k6CJn4q6YdEJuFoNJC on /get-started/. All internal links 200.
- Get Started: every ?plan= value gives the right label + hidden field; utm_source/gclid stay in the URL; empty submit
  sends no AJAX. Snippets other than 1099/1135 byte-identical to `before/`.

## Rollback
- Pages: WordPress revisions, or restore `before/pages/<id>.json` (save through Elementor, keep elementor_canvas).
- Snippets: PATCH `before/snippets/1099-main.php` / `1135-main.php` back, then publish.
- Yoast: `seo_spec.py` BEFORE. Share image: set featured_media back to 1439 and re-save each page.

## Owner items (see final report)
- Growth 3-month minimum replaced the published "No long-term contract · 30 days' written notice"; existing service
  agreements must match. Essentials "Cancel anytime" kept.
- Confirm "Custom quote" vs "Available by consultation" labels on Add-Ons; FAQ phone-number answer.
- GHL: Service Interest values changed ("Axiom Essentials — $297/month …", "Axiom Growth — $597/month …",
  "Add-On or Custom Solution — Custom quote …"); update any workflow/smart list that matches the old text.
- Old share image 1439 (shows $299) remains in the media library, unused; social networks may cache it until re-scraped.
