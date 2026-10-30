# Xtreme (xtremestpete.com) — legacy tracking retirement backup

Captured 2026-10-30 from the live production page source, before any change.
Scope: HFCM (Header Footer Code Manager 1.1.46) Snippets #3, #6, #7 — deactivate only, never delete.

## Snippet backups (exact code as rendered on the live site)

| # | HFCM name | File | Bytes | SHA-256 (first 16) |
|---|---|---|---|---|
| 3 | honeypot link | `hfcm-snippet-3-honeypot-link.html` | 3065 | e6ec8f466b8ef9ba |
| 6 | Pipedrive Script | `hfcm-snippet-6-pipedrive-script.html` | 1386 | b4deb368ef65938f |
| 7 | FingerPrintJS | `hfcm-snippet-7-fingerprintjs.html` | 862 | c864984e3f94007e |

The code is what HFCM output between its `<!-- HFCM by 99 Robots - Snippet # N -->` markers.
HFCM adds those markers itself; paste only the file contents back when restoring.

## Settings observed from outside (confirm in WP Admin before toggling)

| Setting | #3 | #6 | #7 | How observed |
|---|---|---|---|---|
| Status | Active | Active | Active | Rendered on every page |
| Site display | All pages | All pages | All pages | Present on all 19 sitemap pages + cart/checkout/my-account |
| Location | Footer | Footer | Footer | Rendered after page content, between #2 (head) and #8 (footer) |
| Device | All (desktop + mobile) | All | All | Present for desktop Chrome and iPhone Safari user agents |
| Snippet type | HTML | HTML | HTML | Raw `<script>`/`<a>` markup |

Not observable from outside (record from the HFCM edit screen before changing): exact
"Site Display" option name, exclusions, priority/order, and any "Lazy load" setting.

## Baseline marker counts on the homepage (pre-change)

```
GTM-KG694DXC 2 | AW-16472149836 3 | waverez 12 | clickcease 6 | fraudblocker 3
challenges.cloudflare.com 1 | fpjscdn 1 | pipedream 3 | ipapi.co 1 | honeypot-link 2
```

Expected after deactivating #3/#6/#7: `fpjscdn`, `pipedream`, `ipapi.co`, `honeypot-link` = 0;
every other count unchanged.

## Deactivate (WP Admin)

1. WP Admin → HFCM → All Snippets.
2. Toggle **Status** off for #3, #6, #7 only. Leave #1, #2, #4, #5, #8 untouched.
3. Purge caches: Kinsta (admin bar → Clear caches), WP Fastest Cache (Delete Cache),
   Hummingbird (Clear cache). Cloudflare is not caching HTML (`cf-cache-status: DYNAMIC`); no purge needed there.

## Restore

Toggle the same snippet's Status back on in HFCM, then purge the same caches.
If a snippet's code was ever lost, recreate it as HTML, footer, all pages, all devices, pasting the backup file.

## Verification

Post-deactivation results (2026-10-30): see `VERIFICATION.md`, `post-scan-markers.txt`, `post-browser-check.json`.
