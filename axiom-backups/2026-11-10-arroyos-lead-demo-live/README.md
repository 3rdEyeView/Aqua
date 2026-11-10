# Arroyo live page: "See What Happens to a Lead" walkthrough (2026-11-10) — LIVE

Approved live change: the V3 lead walkthrough was added to https://axiomsystems.systems/arroyos-lawn-care-demo/ (page 1716),
opened by `#lead-demo`. Nothing else was changed: the Elementor document, snippet 1733, media, forms and settings are untouched.

## What was published
New snippet **1818 "Axiom Demo – Arroyos Lead Walkthrough"** (`main.php`, built by `build.py` from `../2026-11-10-arroyos-v3/parts`).
Uploaded bytes were read back identical. Page 1716 only (not in Elementor previews). **Rollback: unpublish snippet 1818.**
- `wp_head`: one small style + one line that adds `axl-lead-open` to `<html>` when the hash is `#lead-demo`.
- `wp_footer`: an inert `<template>` and the script. On a normal visit nothing is mounted.
- With `#lead-demo` (fresh tab or hash change) the template is mounted in a shadow root as a full-screen layer, so its styles
  cannot reach the page and the page's styles cannot reach it. "Back to website" removes the hash.
- Simulation only: no `<form>`, no links, no `name` attributes, no fetch/XHR/beacon, no dataLayer/gtag calls, no storage.
  Demo events are stopped at the layer, so page-level listeners never receive them.

## Verification (logged out, Playwright; desktop 1440 and iPhone 13) — `snap.js`, `run.js`, `altcheck.js`, `cachestat.js`
- Normal URL before vs after: same page height, element count (452) and text; no demo host mounted; full-page pixel diff is
  confined to the hero video (different frame). `shots/before-*`, `shots/after-*`.
- Walkthrough on the live page: ad visit → sample request → New Lead + owner notification + acknowledgment (text only with opt-in)
  → follow-up at Wed 9:00 AM → booked / replied → automation stopped → reset. Second run without SMS opt-in. No network requests,
  no events seen by the page, dataLayer length unchanged during the run. `shots/live-*`.
- The only console errors are the site chat widget's scripts, which this environment's network blocks (same as earlier demos).

## Open issue: Kinsta edge cache on the plain URL (desktop variant)
A desktop cache entry for the plain URL was generated at 17:14:20 UTC, seconds before the snippet took effect, and is served
for up to 24 h (`s-maxage=86400`). At 17:21 UTC: phone loads of `…/#lead-demo` opened the demo 4/4; desktop loads 0/4 (one of
five earlier). Any query string bypasses that entry: `…/arroyos-lawn-care-demo/?walkthrough=1#lead-demo` opened and completed
the run 6/6. Fix: clear the Kinsta cache (WP admin bar or MyKinsta), or it expires by about 17:14 UTC on 2026-11-11.
A server-side purge was attempted through the MCP PHP tool and was denied; page 1716 was not re-saved to force a purge
because that is outside the approved change.
