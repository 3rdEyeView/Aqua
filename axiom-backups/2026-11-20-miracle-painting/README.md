# Miracle Painting LLC — website demo (2026-11-20) — https://axiomsystems.systems/miracle-painting-demo/

**Published 2026-11-20 on the user's go-ahead.** Page **2118** "Miracle Painting — Website Concept": Elementor Canvas, title hidden,
Yoast noindex + nofollow, slug `miracle-painting-demo`, not linked from any menu (same as the other demos).
Rollback: set page 2118 back to draft (and unpublish snippet 2120 if wanted).

## Live build (native Elementor V4, same pipeline as Martin Arborcare)
- **Media 2101–2117**: the 17 `site/img/` photos, names `miracle-demo-*` (`native/upload.py`, `native/alts.json`, ids in `native/media-ids.json`).
- **Generator**: `python3 -I native/gen.py` -> `native/ALL.json`; `python3 -I native/build.py` (one replace call into 2118).
  Reuses the Branham build helpers. The gallery is 9 tiles in a 3x3 grid, three before/after pairs, a "How it works" section instead of reviews.
  If you rebuild and the CSS looks stale, check `native/csscheck.sh <url>` and build into a new draft (`MP_PID=<id>`, update `$pid` in the snippet).
- **Snippet 2120** "Axiom Demo – Miracle Painting Page Enhancements" (`snippet/main.php`), published, read back identical, scoped to page 2118
  only (`is_page(2118)` + its previews; nothing output on the home page). Adds the demo estimate form (no `<form>`, no field names, no requests),
  service-card preselect (#q-1..6 -> Exterior / Interior / Commercial / Stucco-coastal / Decks / Doors), heading accents, header colour,
  the `overflow-x: clip` sticky fix and the phone bar (hidden over the hero buttons, at the form and while chat is open).
- Draft preview (signed link) passed 57/60 (the 3 were noindex, not yet set); **live, logged out: 60 passed, 0 failed**
  (`preview/verify-live-log.txt`; desktop 1440, iPhone 13, Pixel 7). CSS file matches the page (198/198). Screenshots in `preview/`.
- Footer and ribbon state it is a concept by Axiom Systems, that the phone is a placeholder and that the form sends nothing.

## Still placeholders (live page too): phone (727) 555-0100, services/descriptions, service-area towns, no logo, no reviews. Replace
once the owner's real details are known. See the list below.

## Local draft (what the live page was ported from)
Deliverable: **`miracle-painting-demo.html`** (one self-contained file, 6.2 MB, opens offline, makes no network requests).
Source in `site/` (`index.html`, `img/`, `fonts/`); `python3 -I build.py` inlines it; `node check.js` runs desktop 1440 + iPhone 13
checks (all pass: no horizontal scroll, 24 images / 0 broken / alt on all, fonts, empty submit → 4 errors, sample → confirmation,
0 requests, no JS errors). Screenshots in `shots/`.

## Photos
Google blocks the egress proxy, so the user saved the images from the business's Google listing and sent them in chat.
The first ~20 were 101 px **thumbnails** (unusable; decided not to upscale them). The user then sent **15 full-size originals**
(`originals/16–30.webp`, 481–1360 px wide), which this page uses. One more thumbnail (yellow art-deco building) came with no file; unused.
`tools/optimize.py` → `site/img/miracle-demo-*.jpg` (hero 2000 px, rest ≤1400 px, never upscaled). The three before/after composites
(16, 27, 29) are split into separate frames (baked-in "Before/After" bars cropped out). #19 is cropped to drop the "Abstract Electronics"
sign; #21 (Awning Works / Patio Lane / reFueled signage) is not used.

## What is a placeholder — confirm before this goes anywhere
Nothing was available about the business except its name and city, so **all of this is generic demo copy**:
- **Phone `(727) 555-0100`** (fake; tel link too). Email: none. Owner name: none, so no names appear.
- **No reviews, no license/insurance/years-in-business claims** (none known). The "How it works" steps, service descriptions,
  "Also ask about" list and service-area towns are generic; verify with the owner.
- Search found no clear match for the business (nearest: Miracle Painters LLC, Largo; Miracle Method of Pinellas, Clearwater). Exact
  business details unconfirmed.
- Logo: none found, so a CSS "M" monogram stands in. Palette navy + sun-gold, Barlow Condensed + Figtree (same fonts as Martin Arborcare).
- Small yellow caution tape is visible on the sage ranch photo; house numbers are legible on a few photos.

## Sections
Draft ribbon → sticky header → hero (tan stucco home) → 6 service cards → 3 before/after pairs → 9-tile gallery → how-it-works →
about → estimate form (demo only, sends nothing) → footer; phone/tablet Call + Free Estimate bar.

## Environment change this session
Added `upload.higgsfield.ai` and `d2ol7oe51mr4n9.cloudfront.net` to the **Cyrus** environment allowlist for an upscale test that was
not run. Remove them if unwanted.

## Next
Get real contact details/reviews from the owner (or their Facebook/website) and more full-size photos, then update `native/gen.py` + the snippet and rebuild.
