# Branham Fencing Co. demo page (2026-11-08) — prepared, not yet on the site

Target: new page on axiomsystems.systems set up like `/myrtle-beach-ink-demo/` (page 1247):
title `Branham Fencing Co. — Website Concept`, slug `branham-fencing-demo`, Elementor Canvas, Yoast noindex + nofollow, published.

## Files
- `branham-demo.html`: the whole page (styles, markup, script scoped under `#bfc`) for one Elementor HTML widget.
  `IMG` = `https://axiomsystems.systems/wp-content/uploads/2026/11/branham-demo-` (change if uploads land elsewhere).
- `img/`: the 41 Media Library files, already named `branham-demo-*.jpg`. Resized to 1200px on the long side (JPEG q82).
  `branham-demo-logo.jpg` is cropped from the 1179×1778 source at (30,360)–(1150,1440): emblem, wordmark, tagline, verse.
- `sources.tsv`: name → Facebook CDN URL (links expire around 2026-11-12).

## Local verification (Playwright, images served from `img/`)
Desktop 1440×900 and iPhone 13: no horizontal scroll (scrollWidth = clientWidth); 40/40 gallery tiles load;
filters give All 40 · Wood privacy 17 · Arch & Charleston 7 · Vinyl 2 · Aluminum & metal 9 · Ranch rail 2 · Decks & steps 3;
lightbox opens at "3 of 40", next → 4, prev ×2 → 2, Escape closes; form shows "Demo only. Your request has not been sent.";
no JS errors.

## Blocked from this session
- Media upload: the Elementor/Angie MCP has no upload ability; `angie/execute-php` needs Angie super admin (off).
- HTML widget: the MCP can only place V4 atomic widgets; the classic HTML widget can't be created through it.
- Chat-widget overlap check: leadconnectorhq.com isn't reachable from this environment, so do it after publishing.
