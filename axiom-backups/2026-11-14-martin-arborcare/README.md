# Martin Arborcare — website demo (2026-11-14) — https://axiomsystems.systems/martin-arborcare-demo/

**Published 2026-11-14 on the user's go-ahead** (to send to Joe). Page **2057** "Martin Arborcare — Website Concept":
Elementor Canvas, title hidden, Yoast noindex + nofollow, slug `martin-arborcare-demo`, not linked from any menu
(same as the Branham, Advanced Fence, Arroyo's, Fence It Up and Comer's demos).
Rollback: set page 2057 back to draft (and unpublish snippet 2049 if wanted).

## Live build (native Elementor V4, same pipeline as Comer's)
- **Media 2025–2045**: the 20 `site/img/` photos + logo, names `martin-demo-*` (`native/upload.py`, `native/alts.json`,
  ids in `native/media-ids.json`).
- **Generator**: `python3 -I native/gen.py` → `native/ALL.json`; `python3 -I native/build.py` (one replace call into 2057).
  Same copy, palette and photos as the approved local draft; the gallery shows 9 (one large + 8), so the grid has no gap.
- **Page 2023** (trashed): the first build. After a rebuild its V4 CSS file stayed stale (0 of 189 classes), the same
  Elementor issue as Comer's 1972, so the build moved to a fresh page. **If you rebuild via the API, build into a new
  draft** (`MA_PID=<id> python3 -I native/build.py`, update `$pid` in the snippet), or edit in the Elementor editor.
  `native/csscheck.sh <url>` shows whether the CSS matches.
- **Snippet 2049** "Axiom Demo – Martin Arborcare Page Enhancements" (`snippet/main.php`), published, read back identical,
  scoped to page 2057 only (`is_page(2057)` + its previews). Checked: no output on the home page, Comer's or Fence It Up.
  Adds the demo estimate form (no `<form>`, no field names, no requests), service-card preselect (#q-1..6 → Tree
  trimming / Tree health / Storm cleanup / Pavers / Artificial turf / Landscaping), heading accents, header colour,
  the `overflow-x: clip` sticky fix, and the phone bar (hidden over the hero buttons, at the form, and while chat is open).

## Live verification — 60 passed, 0 failed (`preview/verify-live-log.txt`)
`node native/verify.js https://axiomsystems.systems/martin-arborcare-demo/` (or `auto` for a signed draft preview),
desktop 1440, iPhone 13, Pixel 7, logged out: no horizontal scroll; `noindex, nofollow`; snippet + form present; all
anchors; 20 images, 0 broken, alt on all; Barlow Condensed + Figtree loaded; hero accent and header colour; tel links;
sticky header; phone bar shown mid-page / hidden over hero buttons / hidden at the form; Pavers card preselects and lands
on the form card; empty send → 4 errors; sample → confirmation ("nothing was sent"); reset; 0 requests during the form
flow; no page errors. CSS file matches the page (182/182). Screenshots: `preview/*-fold.png`, `*-confirmation.png`,
`*-overview.jpg`. Known, site-wide (not this page): the Axiom chat greeting covers part of the phone hero until dismissed.
Known soft spot: WordPress serves the gallery's large tile at 600 px (≈0.9× on desktop at 1×); fine on phones.

## Local draft (the approved concept the live page was ported from)

Business: **Martin Arborcare, LLC** ("Tree & Landscape"), St. Petersburg FL 33714. Facebook `MartinArborcareLLC`
(page ID 1117986794999567, created 2017-10-05, 762 followers, Landscape Company).
Owners per their own flyer: **Joseph (Joe) and Stephanie Martin**. Joe is an ISA Certified Arborist **#FL-9184A** (on their graphics).
Contact from the FB About tab: **(727) 455-2245**, martinarborcare@gmail.com. Website listed: martinarborcare.com (**does not resolve**,
DNS fails, so Facebook was the only source). Service area: Clearwater, Palm Harbor, Gulfport, Pinellas Park, Shore Acres,
Pinellas County, Tarpon Springs, St. Petersburg, Tampa. FB rating: 100% recommend (37 reviews). Accepts Affirm financing.
HomeGuide also lists them (St. Pete, founded 2017). A 2020 BBB accreditation certificate is in their photos, not checked or used.

- **`martin-arborcare-demo.html`**: the deliverable. One self-contained file (8.6 MB), opens offline, makes no network requests.
- `site/`: the source (`index.html`, `img/`, `fonts/`). `python3 -I build.py` inlines it into the single file.
- `node check.js`: browser checks on desktop 1440 and iPhone 13, writes `shots/`. **All passed**: no horizontal scroll,
  21 images / 0 broken / alt on all, fonts load, empty submit → 4 errors, sample → confirmation, 0 network requests, no JS errors.

## Page sections
Draft ribbon → sticky header (round logo, nav, phone, Free Estimate) → hero (waterfront paver garden, "Tree care & landscapes,
done right.", trust chips) → Services (6 cards: trimming/removal, tree health/cabling, storm cleanup, pavers, turf,
landscaping/lighting; each "estimate →" link preselects the service) → **Before & After** (same St. Pete house, posted
July 6 2026) → Our Work (10-photo masonry) → Reviews (4 real FB recommendations, first name + last initial) → About
(Joe & Stephanie, ISA cert, since 2017, service area) → Estimate (demo form, sends nothing; "Fill in sample details" uses
a fictional 555 number) → footer. Phone/tablet: Call / Free Estimate bar, hidden over the hero buttons and the form.

Palette forest / leaf green from their logo; Barlow Condensed + Figtree (same font files as Arroyo V3).
Copy claims are only what their own page says (ISA certified, licensed & insured, family owned, free estimates, Affirm).
**Confirm with Joe before going live:** the ISA number, "licensed & insured", the 2017 start year, and permission to quote reviewers.

## How the photos were scraped
Logged-out Facebook works for the photos grid once these hosts are allowed (added to the **Cyrus** environment this session):
`static.xx.fbcdn.net`, `scontent-ord5-1.xx.fbcdn.net`, `scontent-ord5-2.xx.fbcdn.net`.
Opening `photo.php?fbid=…` directly hits the login wall, but **clicking a grid thumbnail opens the viewer**, and
"Next photo" walks the whole stream. `scrape/harvest.js` does that and saves the full-size image plus date, caption and
Facebook's **"AI content"** label for each (curl downloads it, because Playwright's request API bypasses the proxy).

- **378 photos harvested** (Oct 2026 back to May 2019) → `harvest.json`; files in `originals/` (97 MB, gitignored).
  Stopped there: everything before ~2021 is 720 px. 112 photos are ≥1500 px.
- **5 are labelled "AI content"** by Facebook (recent promo graphics). None are used.
- Many are promo flyers, repeats of the profile photo (lift in an oak, ×20+), memes, or event photos. Not used.
- Contact sheets: `review/sheet-01..13.jpg` (AI-labelled in red); candidates at large size: `review/pick-a.jpg`, `pick-b.jpg`.

## Shortlist → `site/img/` (`shortlist.tsv`, `tools/optimize.py`: hero 2000 px q80, rest ≤1200 px q82, no upscaling)
| Role | Harvest # | Photo | Source size |
|---|---|---|---|
| Hero | 128 | waterfront paver garden (Nov 2021) | 2048×1542 |
| Before / After | 8 / 7 | same front yard, bare → beds + path lights + uplit palm (Jul 2026) | 1320×986 / 2048×1536 |
| Tree trimming & removal | 96 | climber on a Norfolk pine removal (Dec 2022) | 1536×2048 |
| Tree health & cabling | 53 | spider lift on a tall pine (Nov 2024) | 1290×1716 |
| Storm cleanup | 66 | tree across a driveway (posted Oct 13 2024, days after Hurricane Milton) | 2048×1536 |
| Pavers | 17 | gray paver side walk (Jan 2026) | 1536×2048 |
| Artificial turf | 42 | turf side yard, bottom 14% cropped to drop the "Galaxy S20 FE 5G" stamp (Feb 2025) | 1536×2048 |
| Landscaping & lighting | 21 | lit paver path at night (Dec 2025) | **640×960**: the weakest file, fine at card size |
| Our Work | 129, 52, 127, 41, 80, 120, 131, 169, 16, 37 | pavers, turf, lift and crane work, storm job | 1290–2048 px |
| About | 199 | lift and truck at a large banyan (Jul 2020) | 1511×2015 |
| Logo | 20 | round "Martin Arborcare" badge from their posts | 1024×1024 |

## Next steps
- Ask Joe for camera-roll originals (the FB copies are recompressed), especially the night-lighting jobs and more storm work.
- Optional: build it natively in Elementor on axiomsystems.systems like the Fence It Up / Arroyo demos (noindex, `/martin-arborcare-demo/`).
