# Miracle Painting LLC — website demo, rough draft 1 (2026-11-20) — local only, NOT published

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
1. Get real contact details/reviews from the owner (or their Facebook/website) and the rest of their full-size photos.
2. On go-ahead: native Elementor port at `/miracle-painting-demo/` (noindex, Canvas), same pipeline as Martin Arborcare (`../2026-11-14-martin-arborcare/native/`).
