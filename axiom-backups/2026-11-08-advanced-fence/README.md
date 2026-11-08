# Advanced Fence Service LLC demo (2026-11-08) — https://axiomsystems.systems/advanced-fence-demo/

Page **1632** "Advanced Fence Service — Website Concept": Elementor Canvas, Yoast noindex + nofollow, published.
Built the same way as the Branham demo (`../2026-11-08-branham-demo/`): Elementor MCP with native V4 widgets, no Angie.

## Photos (`src/` = the supplied ZIP; `img/` = the 16 files uploaded)
- Facebook could not be scraped from here (logged-out visitors get the login wall; `scrape/`), so the owner supplied the ZIP.
- Uploaded via WordPress REST (`native/upload.py`, same method as Branham) → media **1616–1631**, exact names in `2026/11/`.
  14 Facebook crops `advanced-demo-fb-*.jpg` (408×408, kept at card size — never rendered wider than 408 CSS px),
  logo `advanced-demo-logo-facebook.jpg` (720×720), hero `advanced-demo-hero-wood-privacy.jpg` (Angi, 700×700).
  The other Angi photos and `advanced-demo-logo.png` in `src/` were not used.
- Slug set via REST (`native/set_slug.py`) — the publish created `advanced-fence-service-website-concept` first.

## Page (`native/gen.py` → `native/split.py` batches; reuses Branham's builder helpers)
Header (`#top`, sticky, logo + "Menu" accordion ≤ tablet) · full-width hero (Angi photo + dark gradient) · spec strip ·
`#featured` 3 project cards · `#types` 6 fence types · `#work` gallery tabs All 14 · Wood privacy 5 · Vinyl 2 ·
Metal & gates 3 · Chain link 2 · Rail & farm 2 (tiles open the photo in a new tab) · `#about` ("Call Chris") ·
`#estimate` steps + preview-only form · CTA band · footer "Website concept by Axiom Systems. Demo only." · fixed mobile bar
(84px right padding so the site chat bubble sits beside the buttons). Copy uses only what the photos and the ZIP README
support (Columbia, SC; fence types seen in the photos; Chris as the contact) — no phone number, years or licence claims.
Kit classes added: `afs-gallery`, `afs-tile`, `afs-tile-img`, `afs-tile-cat`.

## Live verification (`native/verify-live.js`, `native/chat-check.js`)
Desktop 1440 + iPhone 13: no horizontal scroll; 42 image refs, 0 broken; logo loads; All tab 14/14; tabs 14/5/2/3/2/2;
tiles → photo in new tab; anchors present; robots `noindex, nofollow`; Canvas; mobile menu opens (5 links); largest
Facebook crop on screen 408px (desktop) / 358px (phone). Chat bubble vs mobile bar: no overlap on iPhone 13, Pixel 7,
iPad Mini. Only console error: chat widget's `stcdn.leadconnectorhq.com` phone-input script, blocked by this
environment's network rules (same on the other demos). Screenshots in `preview/`.
