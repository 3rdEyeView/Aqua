# Xtreme Jetski Watersports — Rebuild Published (2026-09-27)

Live screenshots: `docs/rebuild/live/`. Pre-change backups: `docs/backup/`.

## Live pages (same URLs as before)

| URL | Page ID | Status |
|---|---|---|
| `/` | 10108 (new front page) | Rebuilt |
| `/egmont-key-st-petersburg-jet-ski-tours/` | 554 | Rebuilt |
| `/jet-ski-rentals-st-petersburg/` (Book Now) | 477 | Rebuilt |
| `/6161-2/` (Fort De Soto) | 6161 | Rebuilt, titled |
| `/tampa-bay-jet-ski-rentals/` | 2205 | Rebuilt |
| `/faq/` | 21 | Rebuilt (FAQPage schema) |
| `/about-us/` | 12 | Rebuilt |
| `/contact/` | 14 | New intro band + quick Call/Text/Book; original form and map kept |

Page IDs, slugs, menus and canonicals were kept. The homepage moved from page 9 to page
10108 because the edge CDN had permanently cached a stale stylesheet for page 9 (`/home/`
still 301s to `/`; page 9 is a draft now).

## How to roll back
- One page: `python3 tools/swap_content.py --restore <id>` then open the page in Elementor and click Update.
- Homepage: Settings → Reading → Homepage = "Home" (ID 9), restore page 9 as above and publish it.
- Media alt text originals: `docs/backup/media-alt-before.json`. Menus: `docs/backup/menu-5.json`, `menu-6.json`.

## Verified after publishing (public site, desktop 1440 + mobile 390)
- HTTP 200, one H1, no horizontal overflow, brand fonts loaded, no broken images on all 8 pages.
- WaveRez: the in-page booking button opens `reservations.waverez.com/lightframe1273279` on every
  rebuilt page without leaving the page; product deep links (5918/5919/5920/5967) open the right
  product; all fallback URLs return 200.
- Tracking present on every page: GTM-KG694DXC, GA4 (Site Kit GT-M3V5VSCC), Google Ads AW-16472149836,
  ClickCease, Fraud Blocker, Complianz consent, WaveRez loader.
- Titles and meta descriptions: clean on 14 URLs. 36 internal links: all 200. `/home/` → 301 → `/`.
- Contact form (JetFormBuilder) and map untouched.

## Could not verify / change safely
- A real WaveRez test booking end to end (don't create fake bookings).
- GTM trigger configuration (googletagmanager.com blocked by this environment's network policy).
- takemyboattest.com link target (blocked by network policy; link unchanged).
- Kinsta CDN cache purge — no access; worked around for the homepage.
