# Comer's Landscaping, LLC — website concept (2026-11-13), local preview, NOT published

Business: Comer's Landscaping, LLC, Columbia / Cayce SC, owned and operated by Colin Comer (facebook.com/comerslandscaping).
Nothing was created or changed in WordPress; no media was uploaded to Axiom.

## v2 (current): Comer's real photos, no AI imagery
- `comers-landscaping-demo.html`: the deliverable, one self-contained file (13.3 MB), opens offline, no network requests.
- `src.html` + `assets/` + `fonts/` -> `python3 -I build.py`. `node check.js` -> 29 passed, 0 failed (desktop 1440, iPhone 13,
  reduced motion). Screenshots in `shots/`.
- `originals/comers-001..023.jpg`: the 23 photos the user saved from Comer's Facebook page and uploaded in chat, untouched.
  About 38 more were sent while a reply was in progress and arrived as previews only, not files; they are NOT here
  (pond clearing set, field clearing set, Mashburn paver pad, highway right-of-way set, fire pit, pool rock border, paver walk,
  striped lawns, Walker mowers at a dealership sign, sod/irrigation job, Comer's flatbed truck, new CAT 259D3).

### Where each photo is used (each once)
| Place | Photo |
|---|---|
| Hero start / end (scroll cross-fades and eases a slight zoom) | 004 hydroseeded basin at sunset -> 005 basin grown in |
| Services 1-7 | 009 dealership lot mowing (aerial, Comer's box truck), 008 Walker mower lawn, 022 front beds (cropped: mailbox number and another contractor's truck removed), 021 paver patio, 020 irrigation trench, 006 lawn and beds, 017 silt fence |
| Process | 018 graded site, 013 excavator, 007 lawn |
| Our Work pair | 001 roadside hydroseed (cropped) -> 002 roadside grown in |
| Our Work grid | 015 Comer's trailer + skid steer, 003 basin grown in, 019 rip-rap basin (cropped: third-party trailer branding removed), 016 silt fence trench, 010 / 011 culvert before / after, 012 excavator + pipe, 023 pond bank |
Not used: 014.

### Things to confirm with Colin
- The before/after pairings (004->005 basin, 001->002 roadside, 010->011 culvert) are my reading of the photos, not captions from his posts.
- Permission to use the photos, and whether client sites may be named (none are named on the page).
- 009 shows a crew member on a mower (small, from above). No other identifiable people are on the page.

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
