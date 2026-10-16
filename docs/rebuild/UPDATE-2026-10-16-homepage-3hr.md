# Homepage 3-hour Egmont option, tour-card fix, weight limit, pricing (2026-10-16)

## Rollback point
- **Backup:** `docs/backup/2026-10-16T0332Z-homepage-3hr/`, commit `cd9a3b4`.
  - Database content: all 29 pages, posts and theme templates (raw content, Elementor JSON, page
    settings), all 35 V4 global class styles, kit 7, Customizer CSS, WordPress settings, Yoast head meta.
  - Also: before-change screenshots (`screens-before/`) and `manifest.json` with sha256 hashes.
  - Verified: hashes match, and the stored data was byte-identical to live for every in-scope document.
  - WordPress returned no revision IDs (revisions appear to be disabled), so these files are the
    rollback source.
- **Extra snapshot:** `jet-theme-core/27-after-bridge-step1.json` (header after step 1 of the bridge).
- **Restore one document:** `python3 tools/restore_from_backup.py docs/backup/2026-10-16T0332Z-homepage-3hr pages <id>`,
  then clear the Elementor cache (`DELETE /wp-json/elementor/v1/cache`) and the Hummingbird page cache.
  - Don't run Elementor's publish step after a REST restore: it can promote a staged autosave.
  - Tested on draft 10120.
- **Restore `xj-hero-inner`:** add back custom CSS `background-size:cover;` on its desktop variant
  (stored base64 `YmFja2dyb3VuZC1zaXplOmNvdmVyOw==` in `elementor/global-classes-styles.json`).
- Customer data (orders, bookings, form entries) isn't touched by any of these restores.

## Changes (all live and verified on plain public URLs)

### 1. Homepage (10108): Egmont Key 2-hour and 3-hour options
- **Existing Egmont card (2-hour):**
  - `710a2273`: "1–3 hours · guided" → "2 hours · guided".
  - `42cb0e6b`: "From $220" → "$220".
  - `4e3b4a54`: "Book" → "Book Your Adventure".
  - Still "Most popular", with its orange border.
- **New card `50e56cec`** (full width, below the three cards, inside `119cd4b5`):
  - Content: "Extended adventure" badge, photo 3110 (couple on a WaveRunner near Egmont Key),
    "3 hours · guided", "3-Hour Egmont Key Adventure", short copy, **$350** "per jet ski · up to 2 riders",
    and a **Book Your Adventure** button.
  - Classes: existing `xj-card`, `xj-photo`, `xj-h3`, `xj-body`, `xj-btn`, plus its own local styles.
  - Layout: photo left on desktop and tablet, stacked on mobile.
- **Both buttons** link to `reservations.waverez.com/1273279/details/5919`, and WaveRez's widget opens the
  lightframe for product 5919 on top of the homepage.
  - Duration preselect isn't possible from a link: WaveRez only applies `duration` together with a
    specific `schedule` (time-slot) ID. The customer picks 2 or 3 hours in the lightframe.

### 2. Tour cards on Egmont Key (554) and Fort De Soto (6161)
- **Root cause:**
  1. Global class `xj-hero-inner` held `background-size:cover;` as custom CSS.
  2. Elementor prints custom CSS followed by a literal `\n`.
  3. Hummingbird's minifier moved that `\n` in front of the next rule, `.elementor .xj-panel`, which then
     never matched, so the cards rendered as squashed rows with clipped prices.
- **Permanent fix**, in its Elementor V4 locations:
  - Hero elements 554 `7be6fbdd`, 6161 `4e78419a`, About 12 `a974f1d` and Tampa 2205 `24c8a3c9` got
    `size: cover` on their own background-image layer.
  - `xj-hero-inner` custom CSS removed; its properties are otherwise identical.
  - Origin CSS now has no stray `\n`, and Elementor outputs `background-size:auto auto,cover` for each hero.

### 3. Weight limit (350 lb combined, max 2 riders)
- Homepage `1f5c61c3` and `4f22a6cf`, FAQ 21 `5b17bce4`, Egmont 554 `5dabdd51` and `3dbd7d61`,
  Fort De Soto 6161 `9f6577d`.
- Now reads "up to 2 riders per ski, 350 lb combined max". Search and feed fallback text was updated too.
- The FAQ structured data is generated from this text and now says 350 lb.
- No "400 lb" remains on any public URL.

### 4. Pricing
- Site-wide scan of all 27 public URLs (text, meta, JSON-LD, attributes):
  - $125 (1-hour and "from" prices), $220 (2-hour Egmont: homepage, Egmont page, Book Now),
    $350 (3-hour Egmont: homepage), $650 (Island Hop), $50 (shop hoodie).
  - No $210 and no $375 anywhere. WaveRez now lists product 5919 "From $220".

### 5. Book Now (477)
- Inspected and left unchanged. It renders exactly as its saved Elementor design and the original
  draft: plain tiles at $125+ / $125+ / $220+. No defect.

## Temporary CDN bridge
**Why it's needed:**
- Hummingbird combines Elementor CSS into fixed-name files (`uploads/hummingbird-assets/*.css`), and its
  browser caching sets CSS to `max-age=315360000`.
- Kinsta's CDN caches those files and Elementor's own CSS files. Clearing Hummingbird regenerates
  them under the same names, so visitors keep the old copies until the Kinsta CDN is purged.
- The first homepage publish without a bridge showed the card unstyled, and I rolled it back.

**Where it is:**
- Header template 27 (`jet-theme-core`), container `ca4414b`, **HTML widget `7e5a1cb`**.
- It contains `<style id="xj-cdn-bridge">`, with a comment header marking it temporary.
- It sits next to the Turnstile widget `8883d2f` (untouched) and the mobile-menu fix `7e5a1c9`
  (separate and permanent).
- It's served inline in the page HTML, which isn't CDN-cached.

**What's in it** (sources in `design/bridge/`):
- `home-3hr-card.css`: the new card's own styles, scoped to `.elementor-10108`.
- `tour-cards-554-6161.css`: the `.xj-panel` rule followed by each card's own rules, in Elementor's
  order, scoped to `.elementor-554` / `.elementor-6161`. These are copied from Elementor's origin CSS
  by `tools/bridge_css.py`.
- `hero-sizes.css`: `background-size:auto auto,cover` for the four hero elements, scoped per page.
- Every rule is scoped to a single page and only repeats what Elementor already generates.
  No `!important` except on the widget's own wrapper.

**How to remove it safely:**
1. Purge in MyKinsta: Sites → xtremestpete → Caching → **Clear cache**, then CDN → **Clear CDN cache**.
2. Clear the Elementor and Hummingbird caches, then load each page once.
3. Prove the permanent styles load for ordinary visitors with the bridge hidden:
   ```
   NOBRIDGE=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt NODE_PATH=$(npm root -g) node tools/home_3hr_qa.cjs <out>
   NOBRIDGE=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt NODE_PATH=$(npm root -g) node tools/panel_qa.cjs <out> 1440,1024,768,430,375 https://xtremestpete.com/egmont-key-st-petersburg-jet-ski-tours/ https://xtremestpete.com/6161-2/
   ```
   Every panel must report `dir: column` with no problems, and the homepage card must be `row` on
   desktop and `column` on mobile. Also check the hero background size on 554, 6161, 12 and 2205
   (`tools/live_qa.cjs` with `PLAIN=1` reports `hero=auto, cover`).
4. `python3 tools/remove_bridge.py`. It saves the header first and keeps Turnstile and the menu fix.
5. Clear the caches again and re-run the QA without `NOBRIDGE`.

As of 2026-10-16 the CDN is still stale: a `NOBRIDGE=1` run on 554 shows the cards as rows. **Keep the bridge.**

## Verification (plain public URLs, no cache-busting, not logged in)
- **Homepage** at 1440, 1024, 768, 430 and 375:
  - Prices read From $125 · From $125 · $220 · $350; all photos load.
  - No horizontal overflow; header height is unchanged (276/226/161).
  - Both Egmont buttons open `reservations.waverez.com/lightframe1273279/details/5919` without leaving the page.
- **Egmont Key and Fort De Soto** at the same widths: all 5 and 4 cards stack correctly, nothing
  clipped, no overflow.
- **All 8 rebuilt pages** (desktop and mobile):
  - Status 200, no overflow, no broken images, brand fonts loaded.
  - The booking lightframe opens in place; hero images are `auto, cover`.
  - The mobile menu is still opaque navy with all 8 links.
- **JavaScript errors:** the same 3 as before today (Reddit/Snap pixel stubs and one tracker), none new.
- **Not verified here:** WaveRez per-duration rates on a future date. This environment's network policy
  blocks `api.waverez.com`, so the calendar can't load availability. Check that 2 h = $220 and
  3 h = $350 in WaveRez yourself, or allow that host in the environment's network settings.
- Screenshots: `docs/rebuild/live/2026-10-16-homepage-3hr/`.
