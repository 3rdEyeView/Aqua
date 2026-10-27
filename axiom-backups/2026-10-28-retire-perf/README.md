# Retire legacy URLs, archive cleanup & mobile performance (2026-10-28)

Owner-approved items 1–4 from `../2026-10-27-seo-audit/README.md`. Everything backed up in `before/` first.

## 1. Evidence before retiring URLs (`traffic/`)
- Jetpack Stats 2026: Revenue Maps post (393) **0 views**; all products together **1 view** (a `?post_type=product&p=371`
  preview link); /shop/ 0. Referrers/search terms (365 days): none point at these URLs (referrers are the homepage,
  Facebook, Google Ads/Syndicated search and spam domains).
- Backlinks: no backlink data is reachable from here (Site Kit's Search Console link is not authenticated for this
  account; no backlink tool). Public web search for the domain, the post title and the product names returns nothing.
  → No evidence of useful backlinks. Confirm in GSC → Links (see GSC section).
- Replacements: /shop/ listed the old service catalogue → Pricing; three products have direct current equivalents.

## 2. URL outcomes (snippet 1441 "Axiom Retired URLs", `snippets/retired-urls.php`, tests `harness-retired.php`)
| URL | Before | Now |
|---|---|---|
| /how-axiom-systems-builds-revenue-maps-that-actually-convert/ | 200 noindex | **410** (post 393 set to draft; content kept) |
| /shop/, /shop/page/N/, /?post_type=product | 200 noindex / 404 | **301 → /pricing/** |
| …/shop/sample-product/website-builder/ (Website / Landing Page) | 404 | **301 → /pricing/** |
| …/shop/sample-product/google-ppc-ads/ (Google PPC Ads $1,500) | 404 | **301 → /add-ons/** (Axiom Marketing) |
| …/shop/sample-product/🧠-crm-automation/ | 404 | **301 → /add-ons/** (Lead Automation / CRM) |
| …/sample-product/ axiom-launch, axiom-platinum, axiom-revenue-systems-audit, funnels-conversion-systems, 📱-meta-ads-facebook-instagram, digital-graphic-design; /product/* ; /?post_type=product&p=N | 404 | **410** |
| /product-category/*, /product-tag/* | 200 noindex | **410** |
| /author/axiomsystems/, /?author=1 | 200 noindex / 301 | **404** (also stops username enumeration) |
| /2026/ and other date archives | 200 noindex | **404** |
| /services/, /about-us/, /elementor-9/, /contact-axiom-systems/ | 301 | 301 (unchanged, snippet 1390) |
| /cart/, /checkout/, /my-account/, /?p=393 | 404 | 404 (unchanged) |
| /category/uncategorized/ | 200 noindex | unchanged (empty, noindex; category, not author/date) |
(`…` = `/https:/axiomsystems.systems` — the old malformed product permalinks; `/product/<slug>/` handled the same way.)
Full before/after tables: `audit/status-before.txt`, `audit/status-after-retire.txt`.

## 3. Content removed (backups in `before/`)
- 9 legacy products → **Trash** (restorable 30 days; full data `before/products-full.json`, images kept in the Media Library
  and copied to `before/media-*`). 0 orders ever; only category "uncategorized" (0 left).
- Page 943 "Home – New Draft" → **Trash** (`before/page-943.json`).
- Post 393 → **Draft** (`before/post-393.json`); URL answers 410.

## 4. Performance (snippet 1442 "Axiom Performance", `snippets/performance.php`, tests `harness-performance.php`)
Root cause of mobile CLS: Elementor Canvas prints `<meta name="viewport">` *after* all stylesheets, so phones evaluated the
mobile media queries at 980px, painted the tablet layout, then shifted. Proven by interception test before deploying.
- Viewport meta first on Canvas pages (identical tag; the later one is harmless).
- Removed unused Roboto + Roboto Slab stylesheets (verified no text renders in them on any page, incl. demos and 404).
- `preconnect` to fonts.gstatic.com.
- WooCommerce CSS, cart/order-attribution/sourcebuster/WooCommerce-Analytics JS skipped outside store pages.
  `woocommerce.js`, `blockUI`, `js-cookie` remain because Site Kit's WooCommerce event provider depends on them (Site Kit
  left untouched by design).
- Our Work: 1.28 MB PNG → 137 KB WebP (media 1443, same 1917×1196, PSNR 39.6 dB), now with responsive srcset.

| Mobile (Pixel 7, lab) | Before | After |
|---|---|---|
| CLS (7 pages, 3 runs) | 0.10–0.29 | **0.000** |
| LCP / | 4.4 s* | 1.8 s |
| Requests / weight — Home | 53 / 1,427 KB | 41 / 1,145 KB |
| Our Work | 52 / 2,700 KB | 40 / 1,140 KB |
| Pricing | 46 / 868 KB | 35 / 587 KB |
| CSS per page | ~470 KB | ~230 KB |
*before-run TTFB was uncached; LCP improvement also includes the CSS reduction.

## Verification
- Simulation before deploy (`tests/sim/`): 16 page/viewport full-page screenshots pixel-identical, 0 JS errors.
- After deploy (`tests/after/`): 15/16 pixel-identical to pre-change; desktop Our Work differs only inside the Xtreme
  image frame (WebP vs PNG; `tests/xtreme-before-after.png`). Templates still elementor_canvas; Elementor data diff = image only.
- Functional regression (`tests/regression-*.json`): identical before/after — 8 pages × 1440/390, no overflow, no JS errors,
  mobile menu, tel links, GT-55XGH597, GHL chat widget once, Get Started 7 fields + plan labels, empty submit blocked;
  lead conversion script (axgs-lead-js, AW-17889231515/C8k6…) present. No lead submitted.
- Sitemap: index → page-sitemap (8 current pages). post-sitemap now empty and no longer listed.

## Rollback
Snippets: unpublish 1441 / 1442. Products/page: restore from Trash. Post 393: publish (still noindex). Image: set element
6eff2b7b on page 1031 back to `/wp-content/uploads/2026/09/XtremeStpete.png` (media 946 kept).

## Plugin investigation (no plugin changed)
See `NEXT-STEPS.md` (plugins, business details, landing pages).
