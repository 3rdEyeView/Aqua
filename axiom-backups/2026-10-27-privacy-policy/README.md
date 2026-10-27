# Privacy Policy page + footer links (2026-10-27)

Live: https://axiomsystems.systems/privacy-policy/ (page 1413, Elementor, `elementor_canvas`, effective date October 27, 2026).

## Basis (verified before drafting — `inventory/site-inventory.json`)
- Get Started form (Jetpack 1096): name, business name, email, phone, current website (optional), message, hidden plan
  interest; entry stores IP + user agent; email notification to the team; synced live to GHL (snippet 1398).
- Google tag GT-55XGH597 (GA4 G-T8J1CRQRH6 + Ads), Site Kit Ads AW-17878870459, lead conversion AW-17889231515 with
  transaction ID only; Consent Mode for EEA/UK/CH.
- Jetpack Stats (stats.wp.com) + WooCommerce Analytics (`tk_ai`), WooCommerce order-attribution cookies (`sbjs_*`),
  Cloudflare `__cf_bm` (Kinsta edge), Google Fonts, LeadConnector chat widget (6adfdfee388cb81c668e729a).
- Not loading: Klaviyo, TikTok, Pinterest. Not active: Turnstile (no keys), Akismet (no key) — not named in the policy.

## Page
Built from the site's own sections (`build/build_page.py`): header + footer from Get Started (no active nav item),
hero and two-column section layout from FAQ, global classes ax-eyebrow / ax-body, new IDs. Text: `build/policy_content.py`
(14 sections). Plain-HTML copy in post_content. Yoast: "Privacy Policy | Axiom Systems" + description; index, follow;
canonical; in page sitemap.

## Footer link
"Privacy Policy" added after FAQ in the footer of all 8 pages (952, 1068, 1074, 1085, 1095, 1013, 1031, 1413): new
`e-button` with class ax-link and the footer link style (#AAB5C8, 0.875rem, 500, hover white). Staged → diff showed one
added element per page, nothing changed → published. Backups: `before/pages/`.

## Verification (`after/`, `tests/`)
HTTP 200 (direct and via footer click), renders desktop/mobile, no overflow/JS errors, links underlined; all pages:
only change = the new link; snippets 1099/1134/1135/1377/1390/1398/1411/1412, CRM Sync and Form Protection settings
unchanged; Get Started label and empty-submit block intact; templates still elementor_canvas.

## Owner review items
See the final report: legal entity name/address, payment processor, Google lead form → CRM confirmation, SMS consent at
collection points (form has no disclosure; chat widget wording), A2P campaign match, marketing SMS existence, update the
policy when Turnstile/Akismet keys are added, WordPress Settings → Privacy page selection, attorney review.
Rollback: unpublish page 1413; delete the fl-privacy buttons (IDs in this README's commit) or restore `before/pages/`.
