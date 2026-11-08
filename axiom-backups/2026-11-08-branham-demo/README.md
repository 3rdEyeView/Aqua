# Branham Fencing Co. demo page (2026-11-08)

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

## Native Elementor build (page 1532, draft) — Elementor MCP only, no Angie
Built from `branham-demo.html` as V4 atomic widgets (generator: `native/gen.py`, `native/calls.py`; ids in `native/ids.json`).
- Page 1532 "Branham Fencing Co. — Website Concept": template `elementor_canvas`, Yoast noindex + nofollow. **Status: draft**
  (images not uploaded yet). Slug requested via page settings (`post_name: branham-fencing-demo`); confirm after publish.
- Sections with anchors (`_cssid`): `#top` header (sticky; accordion "Menu" ≤ tablet, like Myrtle Beach Ink), hero (mosaic),
  spec strip, `#featured`, picket divider, `#types`, `#work` gallery, `#about`, `#estimate`, CTA band, footer, fixed mobile bar.
- Gallery: native e-tabs — All 40 · Wood privacy 17 · Arch & Charleston 7 · Vinyl 2 · Aluminum & metal 9 · Ranch rail 2 ·
  Decks & steps 3. Each tile links to the full-size JPG in a new tab (no lightbox). Each panel starts with "Showing: … · N photos".
- Estimate form: static preview (styled paragraphs, no inputs, no submit), labelled "Form preview · nothing here is sent or saved".
- Footer: "Website concept by Axiom Systems. Demo only."
- New global classes (kit): `bfc-tile`, `bfc-tile-wide`, `bfc-tile-img`, `bfc-tile-cat`, `bfc-gallery`, `bfc-picket`.
- Images are referenced by URL at `wp-content/uploads/2026/11/branham-demo-*.jpg` (the names in `img/`).

### MCP style-parser limits found (and workarounds)
- Inline `style=""` in text is stripped → coloured second hero line / "Fencing Co." / citation are separate elements.
- Rejected: `border-*-width` longhands (use `border-width: T R B L`), `inset` (use the four `inset-*`), `row-gap` and two-value
  `gap` (use `gap` + `column-gap`), `overflow-x`, `white-space`, `cursor: not-allowed`, `background-size/repeat`,
  `repeating-linear-gradient` (picket bar is 60 small divs instead), `e-grid` with tag `nav`.
- Tab "selected" state can't be styled (`&:selected`, `&.e--selected` dropped); tabs show filled timber on hover/focus only.

### Verification of the draft (preview link, images served from `img/` via request routing)
`node native/verify-live.js <url> <outdir> img` — desktop 1440×900 and iPhone 13: scrollWidth = clientWidth; 97 image refs,
0 broken, logo loads; 7 tabs with counts 40/17/7/2/9/2/3 and each panel shows that many photos; first tile → full-size JPG,
`target=_blank`; section ids present; robots `noindex, nofollow`; mobile menu opens with 5 links; mobile bar fixed at bottom;
no JS errors. Screenshots in `preview/`.

## Published 2026-11-08 — https://axiomsystems.systems/branham-fencing-demo/ (page 1532)
- Upload method (same as earlier sessions, e.g. `../2026-11-01-xtreme-flagship/upload.py`): WordPress REST
  `POST /wp-json/wp/v2/media` with the `AXIOM_ELEMENTOR_MCP_AUTH` application password — `native/upload.py`.
  The `mbi-demo-*` files match that pattern (batch of uploads by user 1 on 2026-10-07, unattached). 41 files → media
  **1571–1611**, all at `wp-content/uploads/2026/11/<exact name>` (no renames); ids in `native/media-ids.json`.
- Published with the Elementor MCP (`publish-document`). The page-settings `post_name` didn't apply (slug came out
  `branham-fencing-co-website-concept`), so the slug was set via REST `POST /wp/v2/pages/1532 {slug}` (`native/set_slug.py`).
- Mobile bar: right padding 84px at ≤ tablet so the GHL chat bubble (58px, 20px from the edge) sits beside the buttons.
- `branham-demo-images.zip`: all 41 prepared JPGs (fallback for manual upload).

### Live verification (desktop 1440 + iPhone 13, real image loading)
No horizontal scroll; 97 image refs, 0 broken, logo 1120px; All tab 40/40 loaded; tabs 40/17/7/2/9/2/3 each showing that
many photos; tiles → full-size JPG in a new tab; anchors present; robots `noindex, nofollow`; Canvas template; mobile menu
opens; no JS errors. Chat bubble vs mobile bar (iPhone 13, Pixel 7, iPad Mini): no overlap with either button
(`preview/live-mobile-bar-chat.png`). Environment allowlist gained widgets/services.leadconnectorhq.com for this check.
