# Comer's Landscaping demo (2026-11-14) — https://axiomsystems.systems/comers-landscaping-demo/

**Published 2026-11-14 on the user's go-ahead** after reviewing the draft: page **1996** published, slug
`comers-landscaping-demo` (`native/set_slug.py`), Elementor Canvas, Yoast noindex + nofollow, not linked from any menu or
from Our Work (same as the Branham, Advanced Fence, Arroyo's and Fence It Up demos). Snippet 2010 unchanged (it keys on
`is_page(1996)`). Live check on the public URL, logged out: **91 passed, 0 failed** (`preview/verify-log.txt`); the page's
CSS file matches its HTML (395/395 classes); the plain URL is served from the Kinsta cache and that copy is the
published page (snippet, form card and noindex present).
Rollback: set page 1996 back to draft (and unpublish snippet 2010 if wanted).

## Before publishing (kept for reference)

Page **1996** "Comer’s Landscaping — Website Concept" on axiomsystems.systems: **draft**, Elementor Canvas, title hidden,
Yoast noindex + nofollow. Review link (WordPress login as an editor needed):
https://axiomsystems.systems/?page_id=1996&preview_id=1996&preview=true · Editor: https://axiomsystems.systems/wp-admin/post.php?post=1996&action=elementor

Source: the v3 local concept in `../2026-11-13-comers-landscaping/` (`src.html`). The user's re-upload
`comers-landscaping-demo2.html` was byte-identical to v3's `comers-landscaping-demo.html`, so v3 is the latest version.
Before this session no Comer's page existed in WordPress (searched "Comer" and "Landscaping"; checked every page).

## What changed from v3 (review fixes)
- **Mobile hero.** v3 pinned a scroll-driven scrub over ~3 phone screens (1,992 px) before any content, with a 4-line H1,
  the photo chip under the logo and the header jumping out of place after a "Request a Quote" tap. Now: one normal-height
  hero, sticky header, H1 sized for phones, and the lede + both buttons on the first iPhone 13 screen. The hydroseed-day →
  grown-in pair is a one-time 2.6 s crossfade (snippet CSS; skipped with reduced motion; grown-in shows without it).
  The demo ribbon has a one-line phone version.
- **Gallery.** Same 31 photos, 7 filters and lightbox, but 8 photos (a mixed set) show until "Show all 31 photos", so the
  phone gallery is ~1/3 of v3's 2,920 px. Filter chips scroll sideways on phones with a fade edge that shows there's more.
  Tiles are keyboard-operable (Enter/Space), lightbox has arrows, swipe, Esc, focus trap and focus return.
- **Quote flow.** v3's buttons landed on the section heading with the form ~600 px further down on phones. Now every
  quote button (hero, header, menu, about, 7 service cards, call band, phone bar) lands on the form card itself, which
  comes first on phones/tablets; desktop focuses the first empty field. Each service card's "Get a quote for this →"
  preselects its service. Phone is required and email optional (v3 required email); added an optional "Property
  location (city or ZIP)" field and a "Not sure yet" service; "Send" became "Send quote request". Inline validation,
  sample-details button, on-page confirmation that repeats the entries and says nothing was sent, reset.
- **Services** are a 7-card grid with a photo each (v3: hover-to-swap list / swipe cards on phones).
- **Mobile menu** is Elementor's native accordion (closes when a link is tapped). Phone bar (Call + Request a Quote)
  stays hidden over the hero and at the form, sits clear of the site chat bubble.

## Content (unchanged from v3)
Comer's own wording and details from the archived comerslandscaping.com (Wayback, 2026-06-07; see the v3 README): tagline,
H1, About paragraph, seven service names, quote paragraph, phone 803.422.8031, comerslandscaping@gmail.com, hours
Mon–Sat 7 AM–7 PM, Venmo/CashApp, Facebook/Instagram links. Not re-checked this session: web.archive.org is blocked by
the Cyrus environment's network policy. Service one-liners, process blurbs and photo captions were written for the demo.
No reviews, ratings, years, licence or warranty claims. Photos: the same 35 of Comer's 39 as v3 (022, 031, 032, 036 left
out on purpose — see the v3 README), plus the logo. Still to confirm with Colin: photo permission, the three before/after
pairings, and the equipment captions.

## WordPress objects
- **Page 1996** (draft). Built by `native/gen.py` → `A..F.json` → `native/build.py` (one replace call, `ALL.json`).
- **Media 1934–1971** (38 files: logo, logo mark, 2 hero stills, 34 job photos), uploaded by `native/upload.py`,
  ids in `native/media-ids.json`, alt text in `native/alts.json`, file names `comers-demo-*`.
- **Page 1972** (trashed): the first draft. After a rebuild its V4 CSS file stayed on the previous build (none of the
  page's 390 style classes were in it; re-saving page settings and a full replace didn't regenerate it, and Elementor's
  site-wide "clear files" tool was not used because it can unstyle the published pages behind the CDN). A new page
  renders its CSS correctly on first view, so the build moved to 1996. **If you rebuild via the API, build into a new
  draft** (`CMZ_PID=<id> python3 -I native/build.py`, update `$pid` in the snippet) — or edit in the Elementor editor,
  whose saves regenerate CSS normally. `native/csscheck.sh <preview-url>` shows whether the CSS matches the HTML.
- **Snippet 2010** "Axiom Demo – Comer’s Landscaping Page Enhancements" (`snippet/main.php`), published (code active) but
  scoped to page 1996 only: see below. Checked after publishing: home, Pricing, Arroyo’s and Fence It Up pages have no
  snippet output.

## Snippet
Outputs only for page 1996: `is_page(1996)`, `?elementor-preview=1996`, or a signed Elementor preview token whose payload
names post 1996. Nothing on any other page. Adds the demo form, quote-link behaviour, gallery chips/Show all/lightbox,
hero crossfade, heading accents, the header colour (site Additional CSS repaints `<header>`), `overflow-x: clip` on
html/body for this page (the site's `overflow-x: hidden` on body breaks `position: sticky`), mobile-menu close and the
phone-bar logic. The form has no `<form>`, no field names, no submit event and makes no requests.
Uploaded bytes were read back identical; validated by `angie-validate-snippet` and `php -l`.
Rollback: unpublish snippet 2010 (the page still shows every section and all photos; the form card says to call).
When page 1996 is published later, the snippet needs no change (it keys on `is_page(1996)`).

## Verification — 91 passed, 0 failed (`preview/verify-log.txt`)
`node native/verify.js auto [inject]` (`auto` mints a fresh signed preview link per device via `native/plink.py`;
the links expire after ~10 minutes) — desktop 1440, iPhone 13, Pixel 7, logged out. `inject` splices the
snippet's CSS/JS into the HTML locally (used before the snippet existed on the site). Logs: `preview/verify-*.txt`,
screenshots `preview/v-*.jpg`.

Checked on the live draft (desktop 1440, iPhone 13, Pixel 7, logged out): snippet present; no horizontal scroll; Anton
+ Figtree loaded; all anchors; `noindex, nofollow`; 0 broken images (57); H1 and both hero buttons on the first screen
(phones: buttons end at 541 px of 664/839); sticky header; nav links (desktop nav and the phone menu, which closes)
land under the header; phone bar hidden over the hero and at the form, shown mid-page; 7 chips; 8 photos then 31 with
"Show all", back to 8; Equipment 4 / Drainage 8 filters; lightbox opens the full-size photo with focus on Close, next
arrow (desktop) / swipe (phones), Esc closes and returns focus; Close keeps its colour (the Hello theme paints
focused buttons pink); quote buttons land on the form card (hero, about, Hardscaping card, phone bar) and the card
preselects "Hardscaping"; empty send flags name, phone and service; short phone and bad email flagged; sample →
confirmation (6 rows, "nothing was sent"); reset; **0 non-asset network requests during the whole form flow** and no
`<form>` element. No page errors except the site chat's blocked third-party scripts.
Known, site-wide (not this page): the Axiom chat greeting bubble covers part of the phone hero until dismissed, as on
the Arroyo's and Fence It Up demos.

Fixes found while testing: the site's Additional CSS sets `overflow-x:hidden !important` on html/body (breaks sticky;
overridden with a higher-specificity `clip` for this page only); the Hello theme's pink button hover/focus.
