# Advanced Fence Service LLC demo (2026-11-08) — https://axiomsystems.systems/advanced-fence-demo/

Page **1632** "Advanced Fence Service — Website Concept": Elementor Canvas, Yoast noindex + nofollow, published.
Built the same way as the Branham demo (`../2026-11-08-branham-demo/`): Elementor MCP with native V4 widgets, no Angie.

## v3 (current): 26 job photos from the owner's own uploads, photo hero
The user uploaded 84 photos straight from Advanced Fence's own files (Facebook still blocks logged-out access,
so nothing was scraped). Selection, in `native/photos_v3.py`:
- **Dropped 10 exact duplicates** found by pixel hash: #16, #21, #22, #41–46, #56.
- **Dropped as too dark or backlit:** #25, #26. **Dropped as AI-smoothed (wood-and-wire job):** #58, #59.
- **Dropped as off-subject:** #28 (core drilling), #57 (pool is the subject), #81 (cluttered deck railing).
- Kept one strong shot per job plus workmanship details, and checked each at its 4:3 card crop.
  #2 and #66 were swapped for #3 and #68, where the fence fills the frame.
- 10 more photos the user sent came through as previews only, not files, so they couldn't be uploaded.

**27 gallery photos** (26 + #89, a scalloped-top run added from a later upload; #85–88 were repeats of #81–84), each used once, plus the hero (#83, 2000×1500 scalloped privacy) and an owner photo of Chris
(#84) in About. Uploaded as media 1674–1701 and 1717 (`advanced-demo-<slug>.jpg`, long edge ≤1600px; hero 2000px; q80).

| Tab | Photos |
|---|---|
| Wood privacy | 12 |
| Gates & arbors | 4 |
| Vinyl | 3 |
| Aluminum & pool | 3 |
| Rail & farm | 2 |
| Chain link & commercial | 3 |

The 8 Angi photos from v2 (700px) were dropped in favor of these higher-resolution originals.

**Build.** `native/gen3.py` → `v3-*.json`. Only the hero, gallery, fence types and About were rebuilt (appended, then
moved into place with manage-elements). Cards reuse the `afs-card*` kit classes, with only a per-card `object-position`
inline, which keeps the payloads small. Header, spec, estimate, band, footer and mobile bar are unchanged from v2.
After publishing, page settings were re-saved to clear Elementor's element cache (see the v2 gotcha below).

### Live verification (`native/verify-v3.js`)
Desktop 1440, iPhone 13, Pixel 7 and iPad Mini:
- no horizontal scroll;
- 29 photos, all unique, 0 broken, 0 screenshot or Angi images;
- tabs 12/4/3/3/2/3, all loaded; links open in a new tab;
- `noindex, nofollow`; Canvas; the chat bubble doesn't overlap the mobile bar.

Sharpness is source pixels over device pixels:

| Device | Cards | Hero |
|---|---|---|
| Desktop | ≥2.0 | 1.39 |
| iPad | ≥1.09 | 1.25 |
| Phones (3× screens) | ≥0.67 | 0.96–1.1 |

On phones, the 720px originals still give 2× density. Screenshots: `preview/v3-*`.

## v2 (superseded): originals only, Branham as the quality bar
All screenshot-sourced photos were removed: the 14 Facebook crops and the Angi "hero" (enhanced/upscaled).
The 17 Angi originals in `src/` (all 700×700) were reviewed at card size (≈330–380 CSS px) and hero size.

**Kept: 8 photos, each used once** (media 1654–1661, exact names in `2026/11/`):

| Tab | Photos |
|---|---|
| Wood privacy · 3 | wood-fence-corner, wood-privacy-fence, wood-fence-backyard |
| Metal & pool · 4 | black-pool-fence, black-fence-stone-columns, metal-fence-poolside, metal-fence-garden |
| Vinyl · 1 | white-vinyl-yard |

Rejected: wood-fence-roadside, wood-double-gate, wood-privacy-corner, hero-wood-privacy (soft or visibly enhanced);
black-metal-gate (branch across the frame), wood-rail-fence (tilted, hard shadow); white-vinyl-detail and
white-vinyl-privacy (catalog-looking, may not be his work); all `advanced-demo-fb-*` crops (screenshots).

**Hero is text-led.** No original holds up full-width (700px source), so the hero is the headline and CTAs, with the AFS
logo emblem (720px, crisp) at 320/240/160px.

The gallery has no "All" tab, so every photo appears exactly once. The empty categories Chain link, Rail & farm,
Gates & arbors and Metal & gates were removed. The "Featured" cards and the photo band were folded into the gallery cards,
which are 4:3, at most 400px wide, and open the full photo in a new tab. Fence Types is text-only.

Generator: `native/gen2.py` → `v2-A..E.json`, plus `native/split2.py` for the work shell and the card grids.
New kit classes: `afs-card*`. The v1 classes `afs-gallery` and `afs-tile*` are now unused, and the FB and hero media
1616–1630 are still in the library, unused.

**Gotcha.** After publish-document the front end kept serving v1, even with Kinsta's cache bypassed, because of
Elementor's rendered-element cache. Saving page settings (`template: elementor_canvas`) cleared it.

### Live verification (`native/verify-v2.js`)
Desktop 1440, iPhone 13, Pixel 7 and iPad Mini:
- no horizontal scroll;
- 8 photos, 8 unique, 0 FB/hero crops, 0 broken; 3 logo instances;
- tabs 3/4/1, all loaded; largest card image 355–378px; links open in a new tab;
- anchors present; `noindex, nofollow`; Canvas;
- chat bubble beside the mobile bar buttons with no overlap.

The only console error is the chat widget's phone-input script, which this environment's network blocks.
Screenshots: `preview/v2-*`.

## v1 (superseded)
Used the 14 Facebook crops (408×408) plus the Angi hero, with a 6-tab gallery (All 14). `native/gen.py`, `split.py`,
`verify-live.js` and the `preview/*.png` screenshots without the v2 prefix belong to v1.
