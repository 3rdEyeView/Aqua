# Dave's Plumbing and Mechanical LLC — website demo (2026-11-20) — https://axiomsystems.systems/daves-plumbing-demo/

**Published 2026-11-20 on the user's go-ahead** (to send as a demo). Page **2146** "Dave's Plumbing and Mechanical — Website Concept":
Elementor Canvas, title hidden, Yoast noindex + nofollow, slug `daves-plumbing-demo`, not linked from any menu.
Rollback: set page 2146 to draft (and unpublish snippet 2134 if wanted).

## Live build (native Elementor V4, Miracle Painting pipeline)
- **Media 2130-2131** (`daves-demo-*`), `native/upload.py`, ids in `native/media-ids.json`. Generator `python3 -I native/gen.py`, build `python3 -I native/build.py`.
- **Snippet 2134** "Axiom Demo – Dave's Plumbing Page Enhancements" (`snippet/main.php`), read back identical, scoped to page 2146 only. Adds the demo
  form (no `<form>`, no requests), service preselect (#q-1..6), the six service icons (drawn as CSS backgrounds on #ic-1..6), accents, header colour,
  sticky fix, phone bar.
- **Stale-CSS gotcha hit again**: the first build (page 2132) was fine, but a rebuild of the same page left its V4 stylesheet stale (0/141 classes).
  Caught by the live check before sending; moved to a fresh page (2146) and trashed 2132. **Never rebuild into a published page: build into a new draft.**
- Elementor drops multi-layer gradients; the hero uses a single `linear-gradient`.
- Draft preview 57/60 (3 = noindex not yet set); **live, logged out: 60 passed, 0 failed** (`preview/verify-live-log.txt`; desktop, iPhone 13, Pixel 7).
  CSS file matches the page (142/142).

## Local draft (what the live page was ported from)
Deliverable: **`daves-plumbing-demo.html`** (one self-contained file, 0.8 MB, opens offline, no network requests). Source in `site/`;
`python3 -I build.py` inlines it; `node check.js` runs desktop 1440 + iPhone 13 checks (all pass). Screenshots in `shots/`.
Built from the Miracle Painting template (`../2026-11-20-miracle-painting/`), recoloured deep blue + aqua, same fonts.

## Facts supplied by the user (real)
Dave's Plumbing and Mechanical LLC · Venice, FL · **(973) 294-2238** · Master Plumber **License # CFC1434195** ·
serves Sarasota / Venice / Bradenton / Englewood "etc." (North Port, Osprey and Nokomis in the area line are my additions: confirm).
Instagram: `davesplumbingandmechanical.llc` (user-supplied). Not readable here: logged-out Instagram redirects then returns 429 to automated clients; not worked around.
Web search found no public listing, so nothing else is confirmed.

## Photos
Only **2 usable full-size photos** (765x1020 portraits, `originals/31, 32.webp`): a shelf-mounted water heater install with recirculation pump
and expansion tank, and a Milwaukee drain machine in a floor drain. Used in the hero collage and the "Recent work" section (so they appear twice).
Four more (33-36) were 101 px thumbnails (the owner at work; a tankless heater): unusable at that size, not on the page.
No wide hero photo exists, so the hero is a navy/aqua gradient with a two-photo collage instead of a full-bleed image.

## Placeholders / to confirm
Services and descriptions, "How it works" steps, the owner name (none used), no reviews and no years-in-business claims.
Wording about emergency/same-day service is deliberately absent. Logo: a CSS "D" monogram.

## Environment changes this session (Cyrus allowlist)
Added `upload.higgsfield.ai`, `d2ol7oe51mr4n9.cloudfront.net` (Higgsfield upscale test, not run) and `www.instagram.com` (reachable now but unusable). Remove if unwanted.

## Next
Get full-size photos (esp. the owner and a wide job shot) and confirm services/service-area towns, then rebuild into a NEW draft page (see gotcha above) and swap the slug.
