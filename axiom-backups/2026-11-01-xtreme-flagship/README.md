# Xtreme Jet Ski Watersports as the flagship showcase (2026-11-01)

Goal: Xtreme (founder-owned) becomes the primary portfolio example on axiomsystems.systems; Aqua Safari is second.
Only Home (952) and Our Work (1031) mention either business; no other page, snippet or Yoast field referenced them.

## Backups (before any change)
`before/pages/952.json`, `1031.json` (REST context=edit) + `109.json` (legacy About, untouched); element trees `before/*-tree.txt`;
screenshots `before/shots/`. Live pages were checked to be identical to the backups before the ops were built (`build_ops.py`).

## New media (captured from the live sites on 2026-11-01, `xcap.js`)
Xtreme redesigned its site after the Sept portfolio images, so the old Xtreme images (949, 1443) no longer matched it.
Only change made to the captures: the floating "Sound On" video control was hidden.
| ID | File | Use |
|---|---|---|
| 1490 | axiom-portfolio-xtreme-jet-ski-mobile.webp (780×1560, same size as Aqua's 948) | Home hero phone mockup |
| 1491 | axiom-portfolio-xtreme-jet-ski-desktop-2026-11.webp (1920×1200) | Home feature card, Our Work Xtreme frame + comparison |
| 1492 | xtreme-detail-first-screen.webp | Our Work Xtreme detail 1 |
| 1493 | xtreme-detail-tours.webp | Our Work Xtreme detail 2 |
Aqua Safari's live site still matches its images (947/948) and copy (checked via its WordPress data; its front end blocks headless browsers).

## Changes (`spec.py` → `ops/*.json`, staged, previewed at 1440/390, `diff_staged.py`, published ~17:10 UTC)
**Home 952**
- Hero phone: Aqua Safari mobile (948) → Xtreme mobile (1490). Desktop frame (Brags) unchanged.
- "Our work": the large feature card is now Xtreme: "Founder-owned · Jet ski tours · St. Petersburg, FL", flagship copy (owned by Axiom's founder,
  runs on the same website/marketing/follow-up systems), 3 checklist points, "View Website ↗" → https://xtremestpete.com/ (image links there too).
- Second row: Aqua Safari (left, "Client website ·…", "View Website ↗") + Brags Global (right, moved from the feature slot, image 945).
  Heading "Two jet ski companies…" → "Every business gets its own website." + new intro.
- Section intro, CTA band line ("Get the same website, marketing and follow-up systems we run Xtreme on…"), founder paragraph 45bba0fb,
  FAQ answer 48d59077 ("Compare Xtreme and Aqua Safari above").
**Our Work 1031**
- Section order: hero → **01 Xtreme** → **02 Aqua Safari** → comparison → 03 Brags → 04 Tile Father (showroom index reordered/renumbered the same).
- Hero paragraph leads with Xtreme as the founder-owned business, then Aqua Safari.
- Xtreme section: eyebrow "Founder-owned · Our flagship", business/what mattered/what we built rewritten for the current site and the
  ownership relationship; new desktop + 2 detail images (detail frames' aspect ratios set to the new crops); captions; footer
  "Founder-owned · Online booking · Inquiry follow-up"; "View Website ↗" (xtremestpete.com, new tab); note "Our founder's own business…".
- Comparison: Xtreme image and column refreshed (headline, palette #FF6123/#04293A/#F7F2EA/#00B5A6, first words, what it sells, trust).
- Aqua Safari: eyebrow "Client website · Tours & experiences", number 02, "View Website ↗".
- post_content regenerated for both (`sync_content.py`, Elementor data untouched; featured images unchanged).
No metrics, revenue or results claims were added. Primary CTAs (Get Started / Start my website → /get-started/) unchanged; project links
stay as text links/secondary buttons opening in a new tab.

## Verification (`tests/live.js` → `tests/live-results.json`, `after/shots/`)
Both pages × 1440/1024/768/390: HTTP 200, no horizontal overflow, 0 JS errors, 0 broken images; Xtreme appears before Aqua Safari before
Brags in page text; every Xtreme/Aqua/Brags link and image points to the right business; no stale Xtreme copy left; Get Started links intact.

## Rollback
WordPress revisions, or restore `before/pages/<id>.json` `_elementor_data`. Old media 947/948/949/1443 remain in the library.
