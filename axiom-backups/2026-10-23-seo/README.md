# SEO titles, meta descriptions & site name (2026-10-23)

## Changes
- WordPress site title: "AxiomSystems" -> "Axiom Systems" (`before/settings.json`).
- Yoast Organization name and Website name: "AxiomSystems" -> "Axiom Systems", set by one-time snippet 1391
  (`snippets/1391-main.php`; only changed values that still read "AxiomSystems"), deleted after it ran.
- Yoast SEO title + meta description on the 7 pages (`seo_spec.py`; before: none set, Yoast defaults
  "<Page> - AxiomSystems" and an auto description starting with the menu text). Open Graph inherits them.
- Nothing else in Yoast changed: canonicals, robots (index, follow), schema graph, noindex/cornerstone flags.
- Cache purged with a no-op page re-save; Elementor data, template and status verified unchanged.

## Rollback
- Site title: set back to "AxiomSystems" in Settings > General.
- Yoast names: Yoast SEO > Settings > Site basics (Website name) and Site representation (Organization name).
- Page titles/descriptions: clear them in each page's Yoast box (or yoast-seo-update-post-seo-data with "").

## Verification
- `before/head.json` vs `after-head.json`: titles, descriptions, OG tags as specified; robots, canonical,
  schema types, Organization telephone, Google tag, phone links and form identical; schema names now "Axiom Systems".
- Legacy 301s (snippet 1390): one hop each to /get-started/, /#about, /, /pricing/. Page sitemap: the 7 pages only.
- `functional-live.json`: Get Started form + plan label, no AJAX/conversion on empty submit, lead tracking, GT tag,
  click-to-call, mobile menu call row.

## Open item (not changed, needs owner decision)
The sitemap index also lists other content types: 9 published, purchasable WooCommerce products from the old
offers (product IDs 360-424, malformed URLs under /https:/axiomsystems.systems/shop/...), the /shop/ archive,
blog post 393 "How Axiom Systems Builds Revenue Maps That Actually Convert", and category, product-category and
author archives. All are indexable. Snapshot: `before/products.json`, `before/sitemap_index.xml`.
