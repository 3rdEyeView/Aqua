# SEO audit, cleanup & optimization (2026-10-27)

Source of truth for offers = the live Pricing/Add-Ons pages (verified 2026-10-27): Axiom Essential $299/mo, $0 setup;
Axiom Growth $599/mo; Axiom Lead Automation **+$349/mo add-on to Essential** (owner brief says $350 standalone — not changed,
needs owner decision); Axiom Marketing (Google Ads management) from $1,500/mo, ad spend separate, custom setup fee may apply,
initial three-month agreement.

## Inventory (before → action)
| ID | URL | Status | Index | H1 | Relevance | Action |
|---|---|---|---|---|---|---|
| 952 | / | 200 publish | index, self-canonical | Websites that turn leads into customers. | Current | **Optimized** (title, description, eyebrow, H1, intro, location FAQ, OG image) |
| 1013 | /how-it-works/ | 200 publish | index | We build it. We launch it. | Current | **Optimized** (title, description, OG image) |
| 1031 | /our-work/ | 200 publish | index | The work is the pitch. | Current | **Optimized** (title, description, eyebrow, OG image) |
| 1068 | /pricing/ | 200 publish | index | Plans that grow with your business. | Current | **Optimized** (title, description, eyebrow, OG image) |
| 1074 | /add-ons/ | 200 publish | index | Build the system your business needs. | Current | **Optimized** (title, description, OG image) |
| 1085 | /faq/ | 200 publish | index | Questions? We've got answers. | Current | **Optimized** (title, description, single FAQPage schema, OG image) |
| 1095 | /get-started/ | 200 publish | index | Let's grow your business. | Current (conversion) | **Optimized** (title, description, OG image) |
| 1413 | /privacy-policy/ | 200 publish | index | Privacy Policy | Current (legal) | Keep |
| 1247 | /myrtle-beach-ink-demo/ | 200 publish | noindex,nofollow | Your story. Wear it. | Client concept | Keep noindex; hidden from site search |
| 1184 | /pierce-it-or-ink-it-demo/ | 200 publish | noindex,nofollow | Your story. Wear it. | Client concept | Keep noindex; hidden from site search |
| 9 | /elementor-9/ | 301 → / | — | — | Legacy homepage (AI Automation) | Keep 301 (snippet 1390); hidden from site search |
| 107 | /services/ | 301 → /pricing/ | — | — | Legacy paid audit | Keep 301; hidden from site search |
| 109 | /about-us/ | 301 → /#about | — | — | Legacy about | Keep 301; hidden from site search |
| 230 | /contact-axiom-systems/ | 301 → /get-started/ | — | — | Legacy contact ($175 audit) | Keep 301; hidden from site search |
| 393 | /how-axiom-systems-builds-revenue-maps-that-actually-convert/ | 200 publish | noindex,follow | (post title) | Discontinued (Revenue Maps) | Hidden from site search. **Proposed: 410** (approval) |
| 943 | ?page_id=943 | 404 draft | — | — | Old homepage draft | **Proposed: trash** (approval) |
| 303 | /shop/ (Woo archive) | 200 | noindex | Shop (empty) | Discontinued store | **Proposed: 410** (approval) |
| 360–424 | 9 Woo products (Axiom Launch, Axiom Platinum, Revenue Systems Audit, …) | draft, URLs 404 | — | — | Discontinued | **Proposed: trash** (0 orders; approval) |
| — | /category/uncategorized/, /2026/, /author/axiomsystems/, /product-category/uncategorized/ | 200 | noindex | archive | None | Keep noindex; **proposed: disable author/date archives** (approval) |
| — | /?s= search | 200 | noindex | — | — | Legacy/demo pages now excluded |

Sitemap: https://axiomsystems.systems/sitemap_index.xml → page-sitemap (the 8 current pages) + an empty post-sitemap.
robots.txt: allows everything except WooCommerce internals and wp-admin; nothing legacy is blocked (correct — Google must
see the 301s / noindex). Two `User-agent: *` groups (WooCommerce + Yoast); Google merges them — harmless.
HTTP → HTTPS 301, no-slash → slash 301, /index.php and /home/ → / (one hop each). www did not resolve from this environment.

## Changes made (all reversible)
1. **Yoast titles/descriptions** on 952, 1013, 1031, 1068, 1074, 1085, 1095 (`seo_spec.py`; before-values `before/yoast/`).
   Robots, canonicals, cornerstone flags unchanged.
2. **Copy** (`copy_spec.py`, Elementor manage-elements → publish; Elementor data diff = exactly these fields):
   home eyebrow "Website design & marketing for small businesses", H1 "Small business websites that turn leads into
   customers.", hero intro (Axiom Systems, website design, lead automation, Google Ads management, St. Petersburg FL,
   nationwide), FAQ "Do you only work with businesses in Florida?" answer (based in St. Petersburg / Tampa Bay, U.S.-wide);
   Our Work eyebrow "Website design portfolio"; Pricing eyebrow "Website plans & pricing". post_content synced.
3. **Site tagline** (was empty): "Website design, digital marketing and lead automation for small businesses" (WebSite schema, feed).
4. **Share image** `og/axiom-systems-share.jpg` (1200×630, media 1439) set as featured image on the 7 pages → og:image /
   twitter large card. Privacy Policy keeps its own.
5. **Snippet 1438 "Axiom SEO Signals"** (`snippet/main.php`, offline tests `harness.php`, real-page test `tests/real-faq.php`):
   Organization schema + description, email, founder (Michael Hinkle), areaServed United States; merges the 4 FAQPage blocks on
   /faq/ into one (16 questions); excludes IDs 9, 107, 109, 230, 393, 1184, 1247 from site search.
6. Elementor page setting `template = elementor_canvas` saved on 952, 1031, 1068 (see incident).

## Incident (resolved)
The first staging of the copy edits (manage-elements, autosave) reset `_wp_page_template` on 952/1031/1068 to the theme default
for ~10 min (≈20:15–20:25 UTC): live pages showed the theme header/menu and an extra "Home" H1. Fixed by restoring
`elementor_canvas` via REST (live Elementor data verified identical to backup; cache MISS afterwards). Root cause: Elementor's
own page setting `template` was empty; setting it via elementor-update-page-settings before editing kept the template through the
later edit + publish. Future sessions: set that page setting first, and check templates after every Elementor save.

## Verification (`audit/crawl-after.json`, `tests/regression-after.json`)
8 pages 200, one H1 each, robots/canonical unchanged, one FAQPage max, og:image present; 1440 + 390: no overflow, no JS errors,
mobile menu opens, tel links, GT-55XGH597, chat widget 6adfdfee… exactly once; Get Started: 7 fields, plan labels for
essential/growth/lead-automation/marketing, empty submit blocked (no POST), lead conversion script present. Redirects one hop.
No lead was submitted.

## Rollback
Yoast: `before/yoast/<id>.json` values. Copy: old texts in `copy_spec.py` (manage-elements + publish; then check template) or
WordPress revisions. Tagline: Settings → General (empty). Share image: remove featured image (media 1439). Snippet: unpublish 1438.

## Awaiting approval (not applied)
A1 Post 393 → HTTP 410 Gone (discontinued Revenue Maps; no replacement) — or keep noindex.
A2 /shop/ and /product-category/* → 410 (store discontinued). Alternative: 301 /shop/ → /pricing/.
A3 Trash the 9 draft legacy products (0 orders) and draft page 943.
A4 Yoast: disable author and date archives (thin noindex archives; Yoast redirects them to the homepage).
A5 Performance: mobile CLS 0.10–0.29 from late font swap (preload/self-host Manrope + Inter, drop unused Roboto set loaded by
   Elementor); XtremeStpete.png 1.28 MB on /our-work/ → WebP ~150 KB; WooCommerce CSS/JS (≈90 KB CSS) and Klaviyo / Pinterest /
   TikTok / Google Listings & Ads plugins load on every page although the store is retired (privacy policy names some — update together).
A6 LocalBusiness / ProfessionalService schema: needs the GBP setup (address shown or service-area only) and verified social URLs (sameAs).
A7 Lead Automation price: site $349 vs brief $350.
A8 Optional landing pages with original content: Google Ads Management, Lead Automation (website design is covered by Home).
A9 Mobile menu sub-label "Lead response & follow-up automation" (snippet 1135) → "Axiom Lead Automation" wording.
