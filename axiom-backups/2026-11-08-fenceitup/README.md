# Fence It Up LLC demo (2026-11-08) — not started, waiting on photos

Requested source: https://www.instagram.com/fenceitupllc/ (FL fence company).

## Scrape attempt (no photos retrieved)
- `scrape/ig1.js` (copy of `../2026-11-08-advanced-fence/scrape/fb1.js`): `net::ERR_TUNNEL_CONNECTION_FAILED`.
  The agent proxy answered 403 to CONNECT www.instagram.com:443 because the host isn't on this environment's network allowlist.
- Instagram's internal `web_profile_info` API was refused by the session's safety check as access circumvention, so it wasn't used.
- Also unreachable from here: www.homeadvisor.com. The only exact-name listing is
  https://www.homeadvisor.com/rated.fenceitupllc.148798084.html (vinyl/PVC, 5.0; the search entry doesn't name a state).
  "Fence It LLC" in Navarre, FL (Angi 6308753) is probably a different company.

## Needed to proceed
Original photo files (an Instagram data export or camera-roll originals, not screenshots), the logo, and the
city/service area, phone, owner's name and services. The build then follows Advanced Fence v2: native Elementor V4,
originals only, one tab per fence type, published noindex at `/fence-it-up-demo/`.
