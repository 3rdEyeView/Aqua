# Arroyo's Lawn Care LLC demo (2026-11-08) — https://axiomsystems.systems/arroyos-lawn-care-demo/

Page **1716** "Arroyo’s Lawn Care — Website Concept": Elementor Canvas, Yoast noindex + nofollow, published.
Reference: https://arroyoslawncare.com/ (home page). Their live site was only read, never changed.
Built the same way as the Branham and Advanced Fence demos: native Elementor V4 widgets, with media uploaded via REST.
New this time: `native/axmcp.py` calls the same Elementor MCP endpoint over JSON-RPC, so large payloads don't have to be pasted.

## Source
- `scrape/`: their HTML pages, `styles.css` (tokens: ink #0c1509, forest #12300f, green #23751a, lime #8edc1e, sun #f8981d;
  Barlow Condensed + Figtree), and screenshots of the original (`orig-*`).
- `src/assets/`: their full-size media. The original `hero.mp4` (18 MB) is not committed; it's on their site at `/assets/video/hero.mp4`.
- Their site has **no customer reviews** anywhere, so the demo has none. All copy, claims, services, FAQ, hours and contact
  details are theirs, verbatim or lightly trimmed.

## Section order (same as theirs)
Announcement bar → utility bar → header → **drone-video hero** → Why Us → Services (10) → 5-step process →
**Before & After** → Recent projects → Service areas → FAQ → CTA band (`#estimate`) → footer → phone bar.
Every quote button (9) goes to `#estimate`, which has call/text, email and hours. There are 8 tel: links.

## Hero video
- Same footage: all 361 frames, 15.04 s, 1920×1080, 24 fps. Re-encoded only for size (H.264 CRF 23, faststart, no audio track,
  18.1 MB → 8.6 MB). Media 1710.
- Poster = the video's own first frame (`hero-poster.jpg`, media 1709). It's set as the section background (CSS) and as
  `<video poster>` (snippet), so nothing jumps when playback starts.
- Phone framing: the cover crop is centered. Checked across the clip (`ba/frames/sheet.jpg`): the house, palms and driveway stay in a portrait frame.
- Overlay: left-to-right shade on desktop, bottom-weighted on tablet/phone. The pause control sits top-right, clear of the chat bubble.

## Before & After
- Their original before (`ba-before.webp`) and after (`ba-after.webp`) are **different camera positions**: a SIFT match finds
  only 2 matching points, and no other photo of that lawn exists in their gallery. A real matching "after" isn't available.
- So the after is a **visualization** (`ba/turf.py` → `arroyos-demo-ba-after-visualization.jpg`, media 1704). It starts
  from the before photo itself, so it lines up exactly. Only the lawn mask (`ba/mask.png`) is replaced, with real mowed turf
  texture warped from their existing after photo into the before's ground plane. Tone and colour are matched per distance
  band to the before's sunlit grass. The before's own tree shadows (from the bright-blade-tip envelope) are re-applied, and soft
  low-frequency colour variation is added. The beds, plants, hedges, house and sky are the original pixels.
  Comparison: `preview/ba-before-vs-visualization.jpg`.
- It's labelled "After · Visualization" on the image, plus a caption that says only the grass was edited.
- Slider = Elementor elements (`#ba`, `#ba-before` clipped with `clip-path`, `#ba-handle`). Without the snippet it shows a 50/50 split.

## Snippet 1733 "Axiom Demo – Arroyos Page Enhancements" (`snippet/main.php`)
Outputs only on page 1716 and its Elementor previews. It provides:
- the heading accents (`<em>` → lime underline on light sections, lime text on dark);
- slider drag, with `touch-action: pan-y` so vertical swipes still scroll; tap to jump; a keyboard range input; one intro nudge
  (skipped with reduced motion);
- the video poster, plus a pause under prefers-reduced-motion;
- `sizes` on the gallery and slider images.
Uploaded bytes were read back identical. Rollback: unpublish 1733.

## Media (ids in `native/media-ids.json`, files in `img/`)
1704–1715. Photos below the fold are 1200 px JPEG q80 (about photo 1000 px). WordPress generates the srcset sizes, and the
gallery serves 600 px files on desktop. The logo is their original WebP. Gallery photos are their `clean-*` (logo-free) versions.

## Build
`python3 -I native/gen.py` writes `A..E.json`, then `python3 -I native/build.py` replaces the document; then publish,
`native/set_slug.py`, and save page settings (`template: elementor_canvas`) to clear Elementor's render cache.

## Live verification (`native/verify.js`, `native/tap.js`, `native/hit.js`) — desktop 1440, iPhone 13, Pixel 7
- No horizontal scroll. 0 broken images. All anchors present. `noindex, nofollow`. Canvas template.
- Video is playing, with the poster set and `object-fit: cover`. The H1 accent renders lime.
- Slider: both images have identical rects (aligned). Mouse drag 50→20%. Arrow keys move the divider. Touch swipe 50→86%.
  A vertical swipe on the slider scrolls the page (165–205 px) and leaves the divider where it was. Tap jumps 50→20→75%.
- Mobile menu shows 9 links; the phone bar is fixed at the bottom.
- The only console error is the chat widget's phone-input script, which this environment's network blocks (same as earlier demos).
- Note: on phones the Axiom chat widget's greeting bubble covers the right edge of the hero buttons until it's dismissed. It's
  site-wide and set in GHL, not part of the demo.
Screenshots: `preview/final-*`, `preview/live-*`.
