# Arroyo's Lawn Care demo — V2 preview (2026-11-10), NOT published

Local preview only. Nothing on axiomsystems.systems was read through the editor or changed: page 1716, snippet 1733 and the
media library are untouched. V2 was built from the 2026-11-08 backup (`../2026-11-08-arroyos/`: `native/gen.py`, `scrape/`, `img/`).

- `arroyo-v2-preview.html`: the deliverable. One self-contained file (fonts, photos and video inlined), opens offline, makes no network requests.
- `src.html` + `assets/` + `fonts/`: the source. `python3 -I build.py` rebuilds the single file.
- `check.js`: Playwright checks at desktop 1440 and iPhone 13 (plus reduced motion); writes `shots/`.

## Hero
- Loop = Arroyo's own drone footage (their `hero.mp4`), 0.75–7.5 s, with the first 0.75 s cross-faded onto the end so it loops
  without a jump. 6.75 s, 1920×1080, 24 fps, H.264 CRF 30, no audio, 3.2 MB. No generated video (the Higgsfield connector
  in this session can only browse and import, not generate, and the real footage is stronger anyway).
- Poster = the loop's first frame. The video is muted, inline, and only loaded after page load; with
  `prefers-reduced-motion` it is never loaded and the poster stays. Pause/Play control top right.

## Content rules
- All facts come from the existing demo / arroyoslawncare.com: 10 services, About copy, 3 service areas, phone, email, socials.
- No reviews section: their site has none. No hours and no map: no street address is published (owner-operated, "based in Bradenton").
- Gallery = six of their own unedited project photos. The before/after lawn visualizations from V1 are not used anywhere in V2.
- Estimate form: client-side validation and an on-page demo confirmation. No `action`, no fetch, no storage.

## To go live (needs explicit approval first)
Rebuild page 1716 from this layout with native Elementor widgets, upload `assets/hero-loop.mp4` + poster, wire the form.
