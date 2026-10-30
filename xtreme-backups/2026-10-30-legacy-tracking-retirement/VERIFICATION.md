# Post-deactivation verification — HFCM #3, #6, #7 (xtremestpete.com)

Performed 2026-10-30, read-only, after the owner manually deactivated HFCM Snippets
#3 (honeypot link), #6 (Pipedrive Script) and #7 (FingerPrintJS) in WP Admin.
No website, Cloudflare, Pipedream or tracking settings were changed during verification.

Raw results in this folder:
- `post-scan-markers.txt` — 76 page loads (19 sitemap/WooCommerce pages × desktop/iPhone × cached/cache-busted), marker counts per page.
- `post-browser-check.json` — headless Chromium run of 10 main pages × desktop/iPhone: legacy requests, first-party failures, JS errors, hosts this sandbox could not reach. Contains no credentials.

## Result: legacy scripts removed — Verified

| Marker | Baseline (README) | After, all 76 loads |
|---|---|---|
| `fpjscdn` (Fingerprint, #7) | 1 | 0 |
| `pipedream` (#3/#6/#7) | 3 | 0 |
| `ipapi.co` (#6) | 1 | 0 |
| `honeypot-link` / `trap-link` (#3) | 2 / 1 | 0 / 0 |

- All 76 loads returned HTTP 200; cached and cache-busted copies matched (no stale cache).
- Headless browser: zero requests to `fpjscdn`, `fpjs.io`, `pipedream`, `ipapi.co`, `/honeypot-log`; zero failed first-party requests.

## Unchanged components — Verified (page source)

- Remaining HFCM snippets byte-identical to pre-change (SHA-256 compared): #1 ClickCease, #2 GTM, #4 Fraud Blocker, #5 bots/Ads code, #8 WaveRez.
- GTM `GTM-KG694DXC`; Google Ads `AW-16472149836` (3 refs); GA4 via Site Kit Google tag `GT-M3V5VSCC` plus Site Kit content/WooCommerce event providers; Complianz consent hooks — unchanged.
- WaveRez widget script and booking links (`reservations.waverez.com/1273279`, tour details 5918/5919/5920/5967) — identical per page on all 19 pages.
- Cloudflare Turnstile (`cf-turnstile`), ClickCease, Fraud Blocker — present.
- iPhone emulation: all 10 main pages including cart/checkout loaded (200), Turnstile present.

## Issues observed (not caused by this change)

1. **PayPal Payments 500** — `POST /?wc-ajax=ppc-sdk-v6-client-token` returns 500 on every cart/checkout load (desktop and iPhone); PayPal SDK eligibility check then fails. Server-side WooCommerce PayPal Payments plugin; the deactivated snippets were client-only. Likely pre-existing (no pre-change capture). PayPal buttons may not render for shop orders. Not touched.
2. **Cloudflare challenge for headless browsers** — `HeadlessChrome` UA receives 403 `cf-mitigated: challenge` on /cart/ and /checkout/; the same browser with a normal Chrome or iPhone UA receives 200. Bot protection working as intended; not customer-facing.
3. **Console errors in sandbox** — `rdt not implemented` (reddit-for-woocommerce), `snaptr not implemented` (snapchat-for-woocommerce), `n[e] is not a function` (Jetpack WooCommerce Analytics) on 18/20 loads. Originate in those plugins' own files; most likely caused by this sandbox blocking vendor scripts. Real-browser occurrence Unverified.

## Not tested from this sandbox (network policy blocks the hosts)

- Execution of GTM, Google Ads, GA4, WaveRez, ClickCease, Fraud Blocker and Turnstile scripts (presence verified, execution not).
- End-to-end WaveRez booking and WooPayments test checkout.
- Real Safari / real iPhone (Chromium iPhone emulation only).

Recommended owner checks: GTM Preview/Tag Assistant on homepage + a tour page (GA4 page_view, Ads tags);
one WaveRez booking on a phone to the payment screen; GA4 Realtime and Google Ads tag diagnostics over 24–72 h.

## Restore

See `README.md` → Restore: toggle the snippet's Status back on in WP Admin → HFCM, purge Kinsta /
WP Fastest Cache / Hummingbird caches, confirm markers return in page source. If a snippet were lost,
recreate it as HTML, footer, all pages, all devices, from the matching `hfcm-snippet-*.html` file.

## Still pending (separate, owner-approved later)

Rotate/revoke the exposed Cloudflare API token; pause then delete the Pipedream workflow; retire the
Fingerprint "My First App" workspace after 7–14 days with no production identifications.
