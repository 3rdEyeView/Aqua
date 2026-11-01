# Home: Tile Father replaces Aqua Safari; Our Work: Aqua Safari moves to last (2026-11-01)

Backups taken before any change: `before/pages/952.json`, `1031.json` (+ element trees). No pending autosaves existed.
Live pages matched the backups when the ops were built. Ops in `spec.py` / `ops/`. Staged, previewed at 1440/390, published ~18:30 UTC.

## Home (952)
- Supporting card that showed Aqua Safari is now **The Tile Father**, using the approved assets and wording from Our Work:
  image 1146 (tile-father-site-desktop.webp), browser bar "thetilefather.com", label "Client website · Custom tile · Tampa Bay, FL",
  description based on the Our Work "What we built" text, image + "View Website ↗" link to https://thetilefather.com/ (new tab).
  Same element, so its styling is unchanged. Layout: Xtreme large feature, then The Tile Father (left) + Brags Global (right).
- Row intro 3970fb67 rewritten (tile contractor / pressure washing company / Xtreme) – the Aqua comparison is gone.
- FAQ answer 48d59077: "Compare Xtreme, The Tile Father and Brags Global above…".
- Rendered Home page now has zero mentions of Aqua Safari / jetskiadventureclearwater.com (text and HTML). The only remaining "Aqua"
  strings are Elementor navigator labels on that card's containers (e.g. "Aqua Card"), visible only in the editor.

## Our Work (1031)
- Sections: 01 Xtreme → 02 Brags Global → 03 The Tile Father → 04 Aqua Safari → "Same industry. Same coast." (Xtreme vs Aqua comparison,
  kept directly after Aqua Safari so it still follows both businesses). Backgrounds still alternate dark/light.
- "In this showroom" list reordered and renumbered the same way; Aqua's "04 · jetskiadventureclearwater.com" label updated.
- Hero paragraph lists the businesses in the new order.

## Verification (`tests/live.js` → `tests/live-results.json`, `after/shots/`)
Both pages × 1440/1024/768/390: HTTP 200, no horizontal overflow, 0 JS errors, 0 broken images. Home: no Aqua Safari text/HTML; order
Xtreme → Tile Father → Brags; links go to xtremestpete.com, thetilefather.com and bragspressurewashing.com. Our Work: order and numbers
01–04 correct in both the list and the sections; all project links point to the right sites.

## Rollback
WordPress revisions, or restore `before/pages/<id>.json` `_elementor_data`.
