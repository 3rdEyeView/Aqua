# Legacy WooCommerce & archive cleanup (2026-10-23)

## Dependency check (before any change)
- WooCommerce orders: 0. No subscriptions plugin. Enabled gateways: WooPayments (card, Apple/Google Pay, Affirm,
  Afterpay, Klarna); PayPal and offline methods disabled. Not changed.
- Cart (305), Checkout (307), My account (309) and Shop (303) pages were already unpublished.
- No link to shop/cart/checkout/product from the 7 current pages or snippets 1099/1135/1377/1390; the Get Started
  form is Jetpack (not WooCommerce). Primary menu has no shop item.
- Google Listings & Ads: Merchant Center and Ads disconnected. Pinterest product sync disabled. Nothing syncing.
- Before cleanup all 9 products were purchasable (Store API is_purchasable true; product pages with add-to-cart,
  including the malformed /https:/axiomsystems.systems/shop/sample-product/... URLs).

## Backups (`before/`)
products.json (full product data), product-categories/tags, orders (empty), payment-gateways, WooCommerce
general/products/advanced settings, system status, plugins, menus/menu items, posts, pages, categories, users,
yoast-archive-settings.json (old Yoast values: all "show in search results"; also kept in the
axiom_seo_archives_backup option).

## Changes
- Products 360, 363, 364, 366, 368, 371, 374, 418, 424 -> Draft (WooCommerce batch API; nothing else changed).
- Blog post 393 "How Axiom Systems Builds Revenue Maps That Actually Convert": Yoast noindex (no genuine
  replacement page, so no redirect). Still published.
- Shop page 303 (draft, assigned WooCommerce Shop page): Yoast noindex; /shop/ now noindex, empty catalog.
- Yoast settings via one-time snippet 1392 (deleted after applying, `snippets/1392-main.php`): Show in search results
  = No for product archive, categories, product categories, product tags and author archives.
- WooCommerce configuration, payment gateways, plugins: unchanged. Nothing deleted.

## Verification
- Store API: 0 products; /wp-json/wc/store/v1/products/418 -> invalid ID. Adding each of the 9 products via
  ?add-to-cart and via the old product URL POST leaves the cart empty. Old product URLs 404 at origin.
- Sitemap index: page-sitemap (7 current pages) + an empty post-sitemap. Category, product_cat and author sitemaps 404;
  product sitemap empty and not listed.
- 7 pages: SEO head tags identical to the post-SEO state; redirects one hop; form, lead tracking, GT-55XGH597,
  click-to-call OK (`functional-live.json`).
- Edge cache: /shop/ and the malformed audit product URL were still served from Kinsta's cache (s-maxage 24h) at
  completion; origin is noindex / 404 and purchases are impossible either way.

## Rollback
Products: set status back to publish (wc/v3/products/batch). Post 393 / page 303: clear Yoast noindex. Archives:
Yoast SEO > Settings > Content types / Categories & tags / Author archives > Show in search results (old values above).
