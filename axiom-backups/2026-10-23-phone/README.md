# Business phone number — (727) 591-7527 (2026-10-23)

## Findings
- No Elementor Pro theme-builder header/footer exists. All 7 live pages (952 Home, 1068 Pricing, 1074 Add-Ons,
  1085 FAQ, 1095 Get Started, 1013 How It Works, 1031 Our Work) use `elementor_canvas` with their own copy of
  the header and footer, so a per-page edit would have meant 7 header + 7 footer edits.
- The closest thing to a global component is the snippet layer (1099 form, 1135 mobile menu). The phone number
  is therefore added by one new snippet that filters the rendered Elementor HTML. No page content was edited.
- No phone number or `tel:` link existed anywhere. Yoast outputs one Organization schema piece (no telephone);
  no LocalBusiness schema exists.

## Changes
- **New snippet 1377 "Axiom Business Phone"** (`live-snippets/1377-main.php`), filter `elementor/frontend/the_content`:
  - Header: wraps the phone link and the header Get Started button in `.axm-group`. Desktop (≥1025px): phone icon +
    "(727) 591-7527" text link to the left of Get Started. Tablet (768–1024): 44×44 bordered icon button matching the
    menu button. Phones (385–767): compact borderless icon. Under 385px there is no room next to the full logo, so the
    header icon is hidden and the number is in the mobile menu instead.
  - Footer: phone link under the "Managed websites…" tagline.
  - Get Started/contact sections: "Prefer to speak directly? Call us at (727) 591-7527." added after
    "Or write to us directly at …" (Home, Pricing, Add-Ons, How It Works, Our Work), after "Prefer email? …" (FAQ),
    and after the form note on the Get Started page. It reuses that paragraph's classes, so typography matches.
  - Schema: `wpseo_schema_organization` sets `telephone: +1-727-591-7527` on Yoast's existing Organization piece.
  - All links use `tel:+17275917527`. Each insertion is skipped if its anchor text is not found.
- **Snippet 1135 Axiom Mobile Menu** (`live-snippets/1135-main.php`; before: `snippets/1135-main.before.php`):
  reuses an existing `.axm-group` around the header CTA (falls back to creating one as before), and adds a
  "Call (727) 591-7527" row to the mobile menu when the header has a phone link.
- Kinsta edge cache: purged per page by a no-op REST update (`POST /wp/v2/pages/<id>` with `{}`); Elementor data,
  settings, template, status and content were verified identical to `before/pages/` afterwards.

## Rollback
1. Unpublish or delete snippet 1377 — the site renders exactly as before (1135 handles both cases).
2. Optional: save `snippets/1135-main.before.php` into snippet 1135 and publish it. Do not do this while 1377 is
   active: the old menu script only finds a CTA that is a direct child of the header bar.
3. Purge the Kinsta cache (or no-op update each page as above).

## Tests (tests/)
- `render.php` — offline: applies the snippet to saved live HTML; each page got 1 header, 1 footer and 1 contact
  line, idempotent.
- `visual.js` — 7 pages × 10 widths (1440→320) before, offline-after and live: header height and CTA size unchanged,
  no overlap, no horizontal scroll, mobile menu opens/closes with the call row, no JS errors, email lines unchanged.
  `shots-live/` holds the key screenshots and `results.json`.
- `functional.js` — live: tel links keep the page in place and request `tel:+17275917527`; tab order nav → phone →
  Get Started with focus outline; Get Started form renders with `?plan=` label, empty submit blocked client-side
  (no AJAX, no conversion fired), lead tracking script and Google tag GT-55XGH597 present; schema has one
  Organization with the telephone. No form submission was sent.
