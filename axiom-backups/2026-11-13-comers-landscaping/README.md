# Comer's Landscaping, LLC — website concept (2026-11-13), local preview, NOT published

Business: Comer's Landscaping, LLC, Columbia / Cayce SC, owned and operated by Colin Comer (facebook.com/comerslandscaping).
Nothing was created or changed in WordPress; no media was uploaded to Axiom.

## v3 (current): all 39 saved job photos, filterable gallery, lightbox, equipment and results sections
- `comers-landscaping-demo.html`: the deliverable, one self-contained file (14.3 MB), opens offline, no network requests.
  Each image is embedded once and filled into every place it appears at load (see `build.py`).
- `src.html` + `assets/` (`p-<photo number>.jpg` web copies, 4 hero stills, logos) + `fonts/` -> `python3 -I build.py`.
  `rebuild_v3.py` is the one-shot script that rewrote the v2 sections into v3 (kept for reference).
  `node check.js` -> 45 passed, 0 failed (desktop 1440, iPhone 13, reduced motion); screenshots in `shots/`.
- `originals/comers-001..039.jpg`: the photos, untouched. 001-023 were uploaded in chat; 024-039 came from the user's ZIP
  (`originals/zip-sources.tsv` maps them to the ZIP's `comer42..61` names; 4 ZIP files were duplicates and were skipped).

### Sections (nav: About, Services, Results, Equipment, Our Work)
Scroll-driven hero (basin: hydroseed day -> grown in) -> service marquee -> About -> Services (7, photo swaps on hover/focus,
swipe cards on phones) -> Process -> **Results** (3 before/after rows) -> **Equipment** (4 cards) -> **Our Work** gallery
(31 photos, 7 filter chips, lightbox with arrows, swipe, Esc, focus return) -> full-bleed call band using Comer's own line ->
Request a Quote (demo form, sends nothing) -> footer -> phone bar.

### Photo use (35 of 39)
| Place | Photos |
|---|---|
| Hero | 004 hydroseeded basin at sunset -> 005 grown in |
| Services 1-7 | 009 dealership mowing (aerial), 034 Walker mower, 028 river rock by a pool, 026 fire pit patio (cropped to the patio), 020 irrigation trench, 021 paver patio and beds, 017 silt fence |
| Process | 006 lawn and beds, 037 irrigation + sod, 030 striped lawn |
| Results | 001 -> 002 roadside slope, 010 -> 011 drainage crossing, 039 -> 035 backyard |
| Equipment | 024 truck + trailer, 025 CAT 259D3, 015 brush cutter, 013 compact excavator |
| Gallery | all of the above except the hero, plus 003, 007, 008, 012, 014, 016, 018, 019 (cropped), 023, 027, 029, 033, 038 |
Not used, on purpose: 022 (house number and another contractor's truck with a phone number), 031 (a customer's vintage truck),
032 (a dealership's logo sign with both mowers), 036 (two customers' faces). All four are in `originals/` if Colin okays them.

### Things to confirm with Colin
- Permission to use the photos, and whether client names may be shown (none are named on the page).
- The before/after pairings are my reading of the photos, not his captions: 001/002 (two roadside slopes), 010/011 (two views of a
  drainage crossing), 039/035 (I believe the same yard: same fence, crepe myrtles and house, but not verified).
- Equipment captions describe what the photos show (CAT 259D3 is printed on the machine); they make no ownership or capacity claims.
- 009 and 034 show a crew member on a mower, small or from behind. No other identifiable people are on the page.

## v2 (superseded): 23 real photos, scroll-hero, simple "Our Work" strip
### Text
Comer's own (archived comerslandscaping.com, Wayback 2026-06-07): logo, tagline, H1, About paragraph, seven service names, quote
paragraph, phone, email, hours, Venmo/CashApp line, social links. Written for the demo: service one-liners, process blurbs, photo
captions, section headings. No reviews, ratings, years, licence or warranty claims.

### Higgsfield
Not used in v2. The plan was a generated transition between the two real basin photos, but the account read 0 credits on a free
plan (98 on Plus earlier the same day), so nothing was generated. Two keyframe uploads were requested but never sent or confirmed.
`upload.higgsfield.ai` was added to the Aqua environment's allowed hosts for this.

## v1 (superseded): AI concept imagery — `ai-concept-v1/`
The first build, made before any real photos were available: 12 Higgsfield stills and an 8 s generated hero video, all labelled
as AI on the page. Kept for reference only (`ai-concept-v1/comers-landscaping-demo-ai-concept.html`).

## Sources tried before the photos were uploaded
Facebook: scraping refused by the session safety check, and logged-out fetches return only the page name. comerslandscaping.com: dead (Cloudflare 1001). Wayback: text and logo only. Instagram: host not allowed, login wall.

## The logo file
`assets/logo.png` / `logo-mark.png` were rebuilt from a full-resolution (806×514) preview of Comer's own
`cromerslandscaping_logo-2.png` flattened on grey (`source/logo-preview-on-grey.png`): the grey was removed and edge pixels
un-blended. Pixel-identical inside the badge; only the outer anti-aliased edge is reconstructed. Swap in the original PNG when convenient.

## Not done: publishing to axiomsystems.systems
The Axiom Elementor/WordPress credentials are environment variables on the **Default** cloud environment. This session was moved
to the repo's **Aqua** environment (needed to download Higgsfield results), which has no variables, so the Elementor MCP answers 401
and `AXIOM_ELEMENTOR_MCP_AUTH` is unset. To publish like the other demos: run a session on an environment that has both the Axiom
variables and `d8j0ntlcm91z4.cloudfront.net`, then port `src.html` (sections map 1:1 to Elementor containers; the hero scrub and
form go in a page-scoped snippet as on Arroyo's 1733 / Fence It Up 1774), upload `assets/`, set Canvas + noindex.
Also changed on Aqua this session: `comerslandscaping.com` and `www.comerslandscaping.com` were added to its allowed hosts (the site turned out to be dead).
