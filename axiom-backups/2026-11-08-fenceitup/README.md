# Fence It Up LLC demo (2026-11-08) — https://axiomsystems.systems/fence-it-up-demo/

Business: Fence It Up, LLC, Orlando FL (Instagram @fenceitupllc; posts tagged Orlando, Kissimmee and Altamonte Springs).
Directory listings: Yelp `fence-it-up-orlando` / `fence-it-up-orlando-2`, Angi `fence-it-up-llc-reviews-1`, MapQuest 422370714.
Phones listed as (407) 738-0904 and (407) 887-4520; confirm with Jenny before using either.

## Page build (2026-11-09) — page 1764, published, noindex
"Fence It Up LLC — Website Concept": Elementor Canvas, Yoast noindex + nofollow, slug `fence-it-up-demo`.
Built like Branham / Advanced Fence / Arroyo's: native Elementor V4 widgets via the Elementor MCP (`native/axmcp.py`
JSON-RPC), media via WordPress REST, plus one page-scoped snippet.

- **Media 1755–1763**: the 9 `site/` JPEGs at their exact names (`native/upload.py`, `native/alts.json`, ids in `native/media-ids.json`).
- **Generator**: `python3 -I native/gen.py` → `A..D.json`, then `python3 -I native/build.py` (replaces the document), publish,
  `native/set_slug.py`, then re-save page settings (`template: elementor_canvas`) to clear Elementor's render cache.
- **Sections**: sticky header (`#top`) → hero (`#hero`: H1 "Fence Installation in Orlando", vinyl/wood/chain-link/gates line,
  "Request a Free Estimate"; Jan 3 vinyl corner beside the copy, capped at 440 CSS px, stacked on tablet/phone) →
  Services (`#services`: vinyl privacy, wood, chain link, gates; each card's "… estimate →" link preselects that type) →
  Recent projects (`#work`: 8 square cards, 4-up desktop / 2-up tablet and phone; each labelled with fence type + the post's
  location tag; no dates) → Why (`#why`: three points paraphrased from their captions: permits, quality materials / clean
  installation, the added double gate) → Estimate (`#estimate`, form mount `#fiu-form`) → footer → phone/tablet bar (`#fiu-bar`).
- **Content rules**: no phone number (unconfirmed, 0 `tel:` links), no reviews, ratings, years, licensing or warranty claims.
  Palette navy / sky / gold from the logo watermark; Archivo + Figtree.

### Snippet 1774 "Axiom Demo – Fence It Up Page Enhancements" (`snippet/main.php`)
Outputs only on page 1764 and its Elementor previews. Read back identical after every update. Rollback: unpublish 1774.
- **Demo estimate form**: name, phone, ZIP, fence type, optional description (400 chars). Inline validation (errors appear after
  a submit attempt or once something is typed); phone formatted to (xxx) xxx-xxxx; ZIP digits only; "Fill in sample details"
  for quick demos (fictional 555-01xx number). The confirmation repeats the entries, says "Demo preview … nothing was sent",
  and "Start a new request" resets it.
- **Sends nothing**: no `<form>` element, no submit event, no fetch/XHR/beacon. Field names avoid name/phone/email.
  Axiom CRM Sync (1398) and Form Protection (1411) only handle Jetpack form 1096 on page 1095, server-side. Verified: 0 network requests
  during the whole form flow, on every device.
- Smooth scroll to `#estimate` (72 px under the sticky header); desktop focuses the first empty field.
- Hero `<em>` accent in gold. `#top` is forced to navy because the site's Additional CSS paints every `<header>` charcoal with `!important`.
- **Phone/tablet bar vs. the site chat (GHL)**: the chat's invisible greeting box (fixed, z-index 99999999, 301×150) swallowed taps
  on a normal bottom bar. The bar now sits above it (z-index 100000000) and ends 84 px from the right edge, so the chat bubble
  keeps its corner, uncovered and on top. The snippet hides the bar while the estimate form is on screen and while the chat is
  open (`chat-widget[data-active]`), so it never covers the chat's input.

### Live verification (`node native/verify.js` → `preview/verify-log.txt`): 87 passed, 0 failed
Desktop 1440, iPhone 13, Pixel 7, iPad Mini:
- no horizontal scroll; `noindex, nofollow`; Canvas; fonts loaded; all anchors present;
- 9 photos, all unique, 0 broken, alt text on all; hero beside the copy on desktop, stacked elsewhere;
- every visible estimate link (8 desktop / 9 mobile, including a real tap on the bar) lands on `#estimate`; type preselect 4/4;
- empty submit → 4 errors and focus on name; no errors from tabbing past; short phone flagged; ZIP digits only;
  sample → confirmation; 0 network requests; reset works;
- bar: button receives taps at its center and corners, chat bubble clear, hidden at the form and while chat is open.

Image density (file px / device px): desktop cards 1.07–1.34, hero 0.81 at 2×; phones cards 1.2–1.47, hero 0.66–0.71
(706 px source; the same range accepted on Advanced v3).
The only console error is the chat's phone-input script. Failed loads are all site-wide third parties this sandbox blocks
(stcdn.leadconnectorhq.com, services.msgsndr.com, GTM, Facebook, ClickCease, stats.wp.com), not the page.
Screenshots: `preview/*-fold.png`, `*-confirmation.png`, `*-bar.png`, `desktop-overview.jpg`, `iphone13-overview.jpg`,
`confirmation-pair.jpg`.

Known, site-wide (not this page): on phones the Axiom chat greeting covers part of the hero buttons until it's dismissed
(same as the Arroyo's demo).

Later: a muted walkthrough clip can go in if Jenny sends the original Reel (pipeline in `tools/`).

## Jenny's ZIP (`Fence_It_Up_Demo_Media.zip`, 11 files) — what it actually is
`originals/Fence_It_Up_Demo_Media/IMG_0343–0353.jpeg` are **Instagram app screenshots** (706×1536, no camera EXIF,
status bar, like counts and captions in frame), not camera originals. **No video files.** 8 of the 11 posts are videos
(mute icon), but only a still frame of each was captured. The originals are kept untouched; the ZIP itself is gitignored
under `inbox/`.

Steps:
1. `tools/intake.py` → `inventory.tsv`, `review/photos-01.jpg`. No duplicates. Sharpness scores are inflated by UI text,
   so they weren't used for ranking.
2. `tools/crop_screens.py` → `crops/fenceitup-<slug>.png` (lossless) + **`sources.tsv`** (screenshot → post date,
   location, caption, video post y/n, overlays removed). The post photo is the full-width band from y=298
   (706×531 4:3, 706×708 square, 706×943 3:4). The per-file box then cuts out Instagram's mute icon, the repost badge,
   the "Want a Fence?" sticker, the "Work in progress" text and a Fence It Up watermark. Proof sheets: `review/captions-*.png`,
   `review/crops-final.jpg`.
3. Reviewed every crop; the hero was checked at 100%. They're sharp at native size, which is ≈706px wide, so the
   layout is limited to cards ≤ ~400 CSS px and a half-width hero, **not a full-bleed banner**.
4. `shortlist.tsv` → `tools/optimize.py` → `site/` (9 JPEGs, 1.1 MB total; q86 because the source has
   already been compressed by Instagram; no upscaling).

### Shortlist (9)
| Role | File (site/) | Post | Size |
|---|---|---|---|
| **Hero** | fenceitup-demo-vinyl-privacy-corner.jpg | 2026-01-03, Orlando: white vinyl privacy corner, big sky | 706×840 |
| Vinyl privacy | fenceitup-demo-pool-backyard-vinyl.jpg | 2026-10-30, Orlando: pool backyard | 706×555 |
| Vinyl privacy | fenceitup-demo-side-yard-walkway.jpg | 2026-01-20, Orlando: side yard and paver walk | 706×840 |
| Vinyl privacy | fenceitup-demo-pvc-side-yard.jpg | 2025-10-16, Kissimmee: side-yard run | 706×943 |
| Vinyl privacy | fenceitup-demo-new-build-backyard.jpg | 2025-12-09, Altamonte Springs: new build | 561×445 |
| Gates | fenceitup-demo-double-gate-sunset.jpg | 2025-10-18, Kissimmee: added double gate | 706×531 |
| Gates | fenceitup-demo-pvc-double-gate.jpg | 2025-07-20, Kissimmee: PVC double gate | 636×531 |
| Wood | fenceitup-demo-wood-privacy-gate.jpg | 2025-05-28, Orlando: pine privacy and walk gate | 706×490 |
| Chain link | fenceitup-demo-black-chain-link.jpg | 2025-12-07, Orlando: black chain link | 706×943 |

Not used: work-in-progress (2026-02-15 promo post, job-site mess) and vinyl-privacy-sunburst (2025-11-08, lens flare
washes out the fence). Their crops are kept in `crops/`.

### Video: not possible from this ZIP
The clip shortlist and the muted page clip need the actual Reel files. Video posts we'd want, by date:
2026-01-03 corner (hero post), 2026-10-30 pool backyard, 2025-12-09 new build, 2025-05-28 wood gate.
Once they arrive: `tools/intake.py <zip>` → `review/video-V##.jpg` → add `clip` / `video` rows to `shortlist.tsv`
→ `tools/optimize.py` (muted H.264, long side ≤1280, poster JPEG).

## Earlier: where the media could come from

| Source | Result |
|---|---|
| instagram.com/fenceitupllc | Blocked. The host isn't on this environment's network allowlist (proxy 403 on CONNECT). The internal `web_profile_info` API was refused by the safety check as access circumvention, and a logged-out browser gets a login wall anyway. The image CDNs (`scontent-*.cdninstagram.com`) vary per file and can't be wildcarded. |
| fenceitupllc.com (from MapQuest/Yelp) | Dead. Added `fenceitupllc.com` and `www.fenceitupllc.com` to the Default environment; the proxy still answers 502 and DNS doesn't resolve on https, http or www. The domain is lapsed or was never set up. |
| homeadvisor.com/rated.fenceitupllc.148798084 | Blocked host; the state isn't confirmed, so it may not be the same company. |

→ **Next step: Jenny's media ZIP.** An Instagram data export (Settings → Accounts Center → Your information and
permissions → Download your information → Media, format JSON, quality High) is best, because it includes
`posts_1.json` / `reels.json`, which map every file to its post, date, caption and carousel position.
Camera-roll originals in a plain ZIP also work (dates come from EXIF).

## Pipeline (tested on a synthetic IG export: carousel, near-duplicate, HEIC, Reel plus a low-res copy)
1. `python3 -I tools/intake.py <zip> [<zip> ...]`
   - unzips to `originals/<zip-name>/` (kept untouched; zip-slip and `__MACOSX` guarded; zip-in-zip handled)
   - photos: size, sharpness (Laplacian variance at 1024px), brightness, perceptual hash; HEIC supported
   - videos: ffprobe size/duration/fps/bitrate/audio, plus a middle-frame hash
   - dedupe: exact SHA-1, then pHash ≤6 for photos, or the same duration and frame hash ≤8 for videos. The highest-res /
     highest-bitrate copy is kept, and the posts its duplicates came from go in `also_in`.
   - `inventory.tsv` (one row per file with source post, date, caption and carousel position) and `review/` contact
     sheets: `photos-NN.jpg` (48 per sheet, ordered by sharpness, labelled `P###`) and `video-V##.jpg` (6 frames per clip).
2. Review the sheets → write `shortlist.tsv`: 8–12 photos (one marked `hero`), 2–3 videos (one marked `clip`, with start and length).
3. `python3 -I tools/optimize.py shortlist.tsv` → `site/fenceitup-demo-<slug>.*`
   - hero: 2000px JPEG q80 · photos: 1200px JPEG q82 (Branham spec)
   - video: H.264 MP4, audio removed, long side ≤1280, CRF 26 capped at 2.5 Mbps, faststart, plus a poster JPEG
4. Build: same as Advanced Fence v2 (native Elementor V4 on axiomsystems.systems, upload via REST, noindex,
   `/fence-it-up-demo/`), with the hero photo and a muted autoplay loop of the clip.

`scrape/ig1.js` is the blocked browser attempt (a copy of the Advanced Fence Facebook script).
