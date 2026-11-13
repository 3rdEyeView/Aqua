# Comer's Landscaping, LLC — website concept (2026-11-13), local preview, NOT published

Requested from https://www.facebook.com/comerslandscaping. Business: Comer's Landscaping, LLC, Columbia / Cayce SC, owned and
operated by Colin Comer. Nothing was created or changed in WordPress; no media was uploaded to Axiom.

- `comers-landscaping-demo.html`: the deliverable. One self-contained file (12.9 MB), opens offline, makes no network requests.
- `src.html` + `assets/` + `fonts/` → `python3 -I build.py` → the file above. `node check.js` → 31 passed, 0 failed
  (desktop 1440, iPhone 13, reduced motion); screenshots in `shots/`.

## What is real and what is generated
**Real (Comer's own, from the archived copy of comerslandscaping.com, Wayback snapshot 2026-06-07):** logo, tagline
"Design • Install • Maintain", H1 "Your Commercial & Residential Landscaping Partner", the About paragraph, the seven service names,
the Request a Quote paragraph, 803.422.8031, comerslandscaping@gmail.com, hours Mon–Sat 7 AM – 7 PM, "We accept Venmo and CashApp",
Facebook and Instagram (@comerslandscapingllc) links. Brand colours sampled from the logo (#72BE45, #C4D82E, black, white).

**Written for the demo:** the one-line description under each service, the three process blurbs and section headings. No reviews,
ratings, years in business, licence, warranty or job-count claims anywhere.

**AI-generated with Higgsfield (every photo and the hero video):** labelled on the page three ways: an orange ribbon at the top,
an "AI-generated visualization" / "AI concept image" chip on each image, and the footer notice. They are not Comer's projects.
- 11 stills, `gpt_image_2_6`, 2K: hero end frame (high), commercial, lawn, rock, hardscape, irrigation, lighting, erosion, sod,
  pine straw, aerial (medium). Plus the hero "before" frame, an edit of the end frame (high). Originals in `source/`.
- Hero video: `minimax_h3`, 8 s, 2560×1440, start frame = bare yard, end frame = finished yard at dusk
  (job `ac72f042-27ca-4228-b85e-50fc7ed839f1`). The 29 MB original is gitignored; the page uses a 1280×720 all-keyframe
  re-encode (`assets/hero-grow.mp4`, 5.2 MB, no audio) so it can be scrubbed frame by frame.
- Credits: balance read 98 before. Quoted cost 10 + 2 × 2.75 + 16 for the video ≈ 31.5; the balance was not re-read afterwards
  because the Higgsfield connector dropped.

## Why there are no real job photos
| Source | Result |
|---|---|
| facebook.com/comerslandscaping | Not scraped. Fetching it with a browser identity was refused by the session's safety check (bot-check circumvention), and a plain fetch returns only the page name behind the login wall. |
| comerslandscaping.com | Dead: Cloudflare error 1001 on HTTP, TLS handshake failure on HTTPS. |
| Wayback Machine | Has the page HTML and logo files. Their one hero photo (`IMG_7701-scaled.jpeg`) was never archived, and "Our Work" was an Instagram feed embed with no stored images. |
| instagram.com/comerslandscapingllc | Host not on the environment allowlist; logged-out Instagram is a login wall anyway (same as Fence It Up). |

So "Our Work" on the page is six dashed "Comer's photo" slots plus Facebook / Instagram buttons, not generated images posing as jobs.
**Next step for real photos:** a ZIP of Colin's job photos (or a Facebook/Instagram data export); `../2026-11-08-fenceitup/tools/` has the intake pipeline.

## The logo file
`assets/logo.png` / `logo-mark.png` were rebuilt from a full-resolution (806×514) preview of Comer's own
`cromerslandscaping_logo-2.png` flattened on grey (`source/logo-preview-on-grey.png`): the grey was removed and edge pixels
un-blended. Pixel-identical inside the badge; only the outer anti-aliased edge is reconstructed. Swap in the original PNG when convenient.

## Page
Ribbon → header → **scroll-driven hero** (pinned for 340vh; scroll position sets the video's current time, so the bare clay yard
is sodded, paved, planted and lit as you scroll; the headline fades out after the first few percent so the yard is unobstructed;
a Design / Install / Maintain rail fills in thirds) → service marquee → About (their paragraph + facts) → Services (7; hover or
focus swaps the photo on desktop, swipe cards on phones) → Process (Design / Install / Maintain) → Our Work → Request a Quote
(demo form: validates, shows a confirmation, sends nothing; no `<form>` element, no fetch) → footer → phone call bar.
Reduced motion: no pinning or video, the finished still is shown. If the video fails to load, the two stills cross-fade instead.

## Not done: publishing to axiomsystems.systems
The Axiom Elementor/WordPress credentials are environment variables on the **Default** cloud environment. This session was moved
to the repo's **Aqua** environment (needed to download Higgsfield results), which has no variables, so the Elementor MCP answers 401
and `AXIOM_ELEMENTOR_MCP_AUTH` is unset. To publish like the other demos: run a session on an environment that has both the Axiom
variables and `d8j0ntlcm91z4.cloudfront.net`, then port `src.html` (sections map 1:1 to Elementor containers; the hero scrub and
form go in a page-scoped snippet as on Arroyo's 1733 / Fence It Up 1774), upload `assets/`, set Canvas + noindex.
Also changed on Aqua this session: `comerslandscaping.com` and `www.comerslandscaping.com` were added to its allowed hosts (the site turned out to be dead).
