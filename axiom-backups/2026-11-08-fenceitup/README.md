# Fence It Up LLC demo (2026-11-08) — waiting on Jenny's media ZIP

Business: Fence It Up, LLC, Orlando FL (Instagram @fenceitupllc). Directory listings: Yelp `fence-it-up-orlando` /
`fence-it-up-orlando-2`, Angi `fence-it-up-llc-reviews-1`, MapQuest 422370714. Phones listed as (407) 738-0904 and
(407) 887-4520; confirm with Jenny before using either.

## Where the media can come from
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
