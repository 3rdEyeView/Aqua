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

## Slider v2 (2026-11-09): demo visualization on a real Arroyo photo — `ba2/`
v1's after was a grass edit on their original before, which itself looks AI-generated, and the result read as AI. Replaced:
- **After = their own photo `clean-1008` (circular-driveway home), unedited.** It's the clearest real photo they have with a large, simple lawn.
- **Before = the same photo; only the lawn is changed** (`ba2/mask1008.png`). Check: 0 pixels differ outside the lawn mask
  (house, beds, shrubs, pavers, sky, framing identical) → both frames align exactly.
- **Grass texture with permission:** “Unmowed lawn!” by Rhian de Kerhiec, CC BY 2.0
  (https://www.flickr.com/photos/34764035@N00/50001408903), modified. It was found via Openverse with a CC0/CC BY filter (`ba2/ov.py`,
  `ba2/ov.json`). The credit with links is in the slider caption, as CC BY requires.
  Wikimedia Commons was tried first, but it rate-limits this cloud IP (429). Share-alike (BY-SA) photos were skipped.
- Method:
  - `ba2/quilt.py`: image quilting (overlap-SSD patch choice + min-error cut) of the texture's lawn rows into a seamless
    2600×1900 sheet. The source light is flattened and the dead leaves are excluded, so nothing visibly repeats.
  - `ba2/compose.py`: the sheet is laid on this yard's ground plane (horizon y≈536, from the front door's height). It's rendered in
    overlapping bands so blades stay upright, with distance-matched anti-aliasing.
  - Tone and colour are mapped per distance band to the photo's sunlit lawn. The photo's own broad light and tree shadows are re-applied,
    plus soft natural colour variation and a ragged edge spill at pavers and beds.
  - Command: `python3 -I quilt.py ovfull/21_b.jpg 60,330,1024,600 sheet.png 2600 1900 72 24` then
    `python3 -I compose.py sheet.png 0.9 bv-b.png "536,800"`.
- Media **1749** (after) and **1750** (before visualization). Labels: "Before · Demo visualization" and "After". The caption states that
  only the lawn was edited.
- Frame: aspect 1597:760 on desktop, 16:9 on tablet, 4:3 on phone; images anchored to the bottom. On phones both images get the same 1.32× zoom
  toward the lawn, so they stay aligned.
- Page changes: only the slider elements, via `manage-elements` (images, aspect, labels, hint, caption). `gen.py` is synced.
- Snippet 1733 is now closure-only, because named functions made the validator fail while the live copy was loaded. It also adds readable
  caption link colours. Read back identical.
- Live checks (desktop 1440, iPhone 13, Pixel 7):
  - no horizontal scroll, 0 broken images;
  - both frames at identical rects;
  - mouse drag 50→20%, keyboard arrows move the divider, touch swipe 50→86%, tap 50→20→75%;
  - a vertical swipe on the slider scrolls the page and leaves the divider where it was;
  - credit links visible; video still playing; noindex, nofollow.
- `preview/ba2-before-vs-after.jpg`: the full frames compared.

## About photo lawn (2026-11-09) — `ab2/`
The "15+ years" About image (their `project-2001`) had AI-looking turf. Only its lawn was replaced; 0 pixels changed outside
`ab2/mask.png` (house, palms, bed, rocks, lake and sky are identical).
- Texture: “starr-090922-5230 Stenotaphrum secundatum, habit in lawn, Oakwood Lakes, Boynton Beach, Florida” by Forest & Kim Starr
  (Starr Environmental), CC BY 2.0 (https://www.flickr.com/photos/97499887@N06/24343142244), modified: a top-down photo of a
  mowed St. Augustine lawn in Florida. Credit with links is in the footer fine print.
- `ab2/quilt2.py`: fallen leaves inpainted, then large-patch quilting with all 8 rotations/flips into a seamless 2600×1900 sheet
  (no visible repetition). `ab2/compose.py` (variant of `ba2/compose.py`): ground-plane projection (horizon y≈1165), tone and colour
  matched to the original lawn, and the original palm shadows re-applied.
  Command: `python3 -I quilt2.py ../ba2/ovfull/m5_b.jpg sheet.png 2600 1900 280 70 20` then `python3 -I compose.py sheet.png 0.75 out.png "1165,800"`.
- Media **1781** (`arroyos-demo-lakeside-palm-bed-v2.jpg`, 1000×1250) replaces 1711 in element `ab-img`. Live on desktop, iPhone 13
  and Pixel 7: loads, no horizontal scroll, 0 broken images, slider and video unchanged. Screenshots: `preview/about-v2-*.png`.
