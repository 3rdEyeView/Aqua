# Xtreme Jetski Watersports — Rebuild Status & Go-Live Runbook

Last updated 2026-09-27. **Nothing below is live.** Every rebuilt page is an unpublished
WordPress draft. The live site, its URLs, WaveRez code, tracking and forms are untouched.

## 1. What was built (drafts)

| Draft | ID | Replaces live URL | Editor link |
|---|---|---|---|
| Home | 10108 | `/` | https://xtremestpete.com/wp-admin/post.php?post=10108&action=elementor |
| Egmont Key & St. Pete Jet Ski Tours | 10109 | `/egmont-key-st-petersburg-jet-ski-tours/` | https://xtremestpete.com/wp-admin/post.php?post=10109&action=elementor |
| Book Now | 10118 | `/jet-ski-rentals-st-petersburg/` | https://xtremestpete.com/wp-admin/post.php?post=10118&action=elementor |
| Fort De Soto Jet Ski Tours | 10119 | `/6161-2/` (new slug proposed) | https://xtremestpete.com/wp-admin/post.php?post=10119&action=elementor |
| Jet Ski Rentals Tampa Bay | 10120 | `/tampa-bay-jet-ski-rentals/` | https://xtremestpete.com/wp-admin/post.php?post=10120&action=elementor |
| FAQ | 10121 | `/faq/` | https://xtremestpete.com/wp-admin/post.php?post=10121&action=elementor |
| About Us | 10129 | `/about-us/` | https://xtremestpete.com/wp-admin/post.php?post=10129&action=elementor |

Screenshots (desktop + mobile, full page): `docs/rebuild/screens/`.

Not rebuilt on purpose: **Contact** (its JetFormBuilder form + email delivery must not be
disturbed), Shop/Cart/Checkout (live WooCommerce merch), legal pages, blog posts.

## 2. Design system (Elementor kit, additive)

- Global variables: `xj-orange #FF6123` (existing brand primary), `xj-navy #04293A` and
  `xj-navy-2 #0A3D62` (existing kit accents), `xj-ink`, `xj-sand`, `xj-gulf`, `xj-slate`;
  fonts `Barlow Condensed` (display) + `Manrope` (body; already used by the header/footer).
- Global classes `xj-*` (layout, type scale, buttons, cards, accordion). Source of truth:
  `design/classes.css`. These only affect elements that use them — no existing page changed.

## 3. WaveRez booking (revenue-critical) — how the rebuild uses it

Existing WaveRez code on live pages is **not modified**. The new pages use WaveRez's own,
built-in "simple link" trigger from `_trip_book_widget.js` (the loader that already runs
sitewide from the theme):

- `https://reservations.waverez.com/1273279` → opens the same lightframe as the existing
  `data-waverez-id="1273279"` buttons (`/lightframe1273279`).
- Product deep links open that product directly in the lightframe:
  `…/1273279/details/5918` Jet Ski Rental · `5919` Egmont Key Jet Ski Adventure ·
  `5920` St Petersburg Guided Jet Ski Tour · `5967` Ultimate Island Hop.
- Verified in a real browser on every draft (desktop, tablet, mobile): click → lightframe
  iframe opens in-page; no navigation away. If JS fails, links fall back to the real
  WaveRez booking page. The `_gl` cross-domain param is still forwarded by WaveRez's script.

**Re-test after go-live:** click every Book button once on the live URL and confirm the
lightframe opens; complete one test booking end to end.

## 4. Facts used, and their sources

| Fact | Source |
|---|---|
| Products, durations, descriptions | WaveRez listing (live) |
| From prices: Rental $125, St Pete Guided $125, Egmont Key $210, Island Hop $650 (5 hrs) | WaveRez product pages (live, 2026-09-27) |
| 5.0 on Google, 600+ reviews | WaveRez header shows "5 · 607 Google reviews" |
| Phone (813) 538-4802, Open 7 days | Live site |
| 18+ renter, photo ID/passport, boater card if born on/after 1/1/1988, 2 riders/400 lb, arrive 30 min (groups 5+: 1 hr), no deposit, fuel included, no passenger fees, weather refund/reschedule | Live FAQ / Book Now / About / pricing post |
| Destinations, wildlife, Captain Mike | Live Home / Tours / Fort De Soto page / WaveRez |

## 5. Needs your confirmation (flagged, not guessed)

1. **Live site advertises "$100 per ski"** (Home, SEO post) — WaveRez shows Jet Ski Rental from **$125**. Drafts use $125.
2. **Live Tours page price table** (1 hr $125 / 2 hr $210 / 3 hr $350, names "Coastal Ride" etc.) doesn't match the WaveRez catalog (Egmont Key starts at $210). Drafts use WaveRez products + "from" prices only.
3. **Hours conflict:** 9–5 (Home hero, About) vs 9–6 (Home info, Contact). Drafts say "Open 7 days" only.
4. **Operator age conflict:** 14+ with parent (Home/FAQ) vs 16+ (Tampa page, SEO post). FAQ draft keeps the FAQ page's own wording; please confirm.
5. **Review count** on live pages says 610+ (Book Now) and 365+ (Tampa). Drafts say 600+ (WaveRez shows 607).
6. **Departure point:** map says "North Skyway Beach, St. Petersburg 33715"; WaveRez says "St. Pete Beach area". Drafts avoid a street-level claim; add the exact meeting point + parking notes if you want it shown.
7. **Most popular:** WaveRez says the 2-hour ride is most popular; the live Tours page says Egmont Key. Drafts show both claims in their own context.
8. **Review quotes:** none exist on the site. Send 4–6 real Google reviews (with first name/initial) and they'll be added as a quote row.

## 6. Things the Elementor MCP cannot do (manual, ~10 minutes each)

1. **Header/menu (JetThemeCore, V3):** menu labels include two full SEO titles and wrap to
   two lines (header is ~276px tall). Appearance → Menus: rename to "Home, Tours, Fort De Soto,
   Tampa Bay, FAQ, About, Contact" + a "Book Now" button. Keep "Boating License" if it earns
   affiliate value.
2. **Yoast title template:** titles render duplicated (e.g. "Home - Xtreme Jetski Watersports
   Home Jet Ski Rentals…"). Yoast → Settings → Content types → Pages: set the SEO title
   template to `%%title%%` only where a custom title exists, or clear the prefix.
3. **Image alt text:** the V4 image widget renders the Media Library alt text, which is empty
   on ~29 images. Proposed alt text is in section 8 (Media Library → edit each image).
4. **Footer typo:** "garunteed" → "guaranteed" (footer template).
5. **Floating "Sound Off" button** overlaps page content on mobile; consider moving it or
   removing the ambience audio.
6. **Cloudflare:** re-enable "Block definitely automated traffic" (or add a narrow allow
   rule) — it was relaxed for this audit.

## 7. Go-live runbook (preserves URLs, SEO, tracking)

Do these one page at a time, starting with a low-risk page (FAQ), then Tours, Book Now, Home.

0. Backup (host snapshot or UpdraftPlus) + Elementor → export the live page as a template.
1. Open the draft in Elementor, preview it logged in, check desktop/tablet/mobile.
2. Copy SEO fields from the live page to the draft in Yoast (title, meta description,
   focus keyphrase, canonical left blank = self). Suggested titles/descriptions below.
3. Swap slugs: rename the live page slug to `<slug>-old` and set it to Draft; give the new
   page the original slug and Publish. (Home: Settings → Reading → Homepage = new page.)
4. Immediately test: page loads at the same URL, Book buttons open the lightframe, tap-to-call
   works, GTM/GA4 Realtime shows the visit, Google Ads tag present (Tag Assistant).
5. Fort De Soto: publish with slug `fort-de-soto-jet-ski-tours` and add a **301** from
   `/6161-2/` (Yoast Premium Redirects or the Redirection plugin).
6. Keep the old pages as drafts for 30 days as instant rollback.

### Suggested SEO titles / meta descriptions

| Page | Title | Meta description |
|---|---|---|
| Home | Jet Ski Tours & Rentals St. Petersburg FL \| Xtreme Jetski | Guided jet ski tours from St. Pete to Egmont Key, Shell Key and Fort De Soto on brand-new Yamaha WaveRunners. 5.0 on Google. Book online. |
| Tours | Egmont Key & St. Petersburg Jet Ski Tours \| Xtreme Jetski | Guided jet ski tours to Egmont Key's lighthouse and Fort Dade, or the St. Pete waterfront. 1–3 hours, from $125. Book online today. |
| Book Now | Book a Jet Ski in St. Petersburg FL \| Xtreme Jetski | Check live availability and book your St. Pete jet ski rental or guided tour in minutes. No deposit, no hidden fees. |
| Fort De Soto | Fort De Soto Jet Ski Tours \| Xtreme Jetski Watersports | Guided jet ski tours near Fort De Soto Park: Bunces Pass dolphins, Shell Key, Egmont Key and Skyway views. Beginners welcome. |
| Tampa Bay | Jet Ski Rentals Tampa Bay \| Xtreme Jetski Watersports | Tampa riders: skip the river traffic. Our St. Pete launch puts you on open Gulf water near Egmont Key and Shell Key. Book online. |
| FAQ | Jet Ski Rental FAQ St. Petersburg FL \| Xtreme Jetski | Age requirements, Florida boater card rules, what to bring, weather policy and what to expect before your ride. |
| About | About Xtreme Jetski Watersports \| St. Petersburg FL | Family-owned jet ski tours in Pinellas County. No passenger fees, unrestricted riding areas and new Yamaha WaveRunners. |

### Structured data
- FAQPage schema: emitted by the accordions on Tours, Fort De Soto and FAQ drafts.
- Recommended: LocalBusiness (TouristAttraction) schema via Yoast Local SEO or a code snippet
  with name, phone, address, geo, hours, `sameAs` (Instagram, Facebook, YouTube, Yelp) —
  once hours/address are confirmed (section 5).

## 8. Proposed Media Library alt text

| ID | File | Alt text |
|---|---|---|
| 3118 | UKTouristEgmont | Visitor from the UK on the beach at Egmont Key after a guided jet ski tour |
| 3117 | UKDadandMom | Couple celebrating on the beach at Egmont Key during a jet ski tour |
| 3116 | CoupleDonCesar | Couple riding a Yamaha WaveRunner in front of the Don CeSar on St. Pete Beach |
| 3111 | CoupleEgmont | Guests with their WaveRunners in shallow water at Egmont Key |
| 3110 | YoungCoupleEgmont | Young couple on a Yamaha WaveRunner near Egmont Key |
| 3108 | CoupleRetreat | Couple riding a brand-new Yamaha WaveRunner off St. Petersburg |
| 635 | JetSkiRentStPetebeach | Guests riding Yamaha WaveRunners through green Gulf water off St. Pete Beach |
| 624 | PassageGroup | Group of guests celebrating in shallow water beside their WaveRunners |
| 220 | IMG-5826 | Rider throwing spray on a Yamaha WaveRunner in open water near St. Petersburg |
| 219 | RentJetSkiGroup | Two guests in life jackets on a Yamaha WaveRunner near St. Pete Beach |
| 218 | JetSkiRentTreasureIsland | Rider on a Yamaha WaveRunner near Treasure Island waterfront homes |
| 217 | IMG-5872 | WaveRunner in open water with kiteboarders overhead near St. Petersburg |
| 216 | RentJetSkiBirthdaySisters | Sisters riding a WaveRunner together on a birthday jet ski tour |
| 215 | IMG-5849 | Wildlife surfacing in clear shallow water during a guided jet ski tour |
| 214 | CouplesTourYacht | Two WaveRunners near a sandbar with a sailboat anchored behind |
| 213 | JetSkiFamilyRetreat | Family riding WaveRunners together on a guided tour in Tampa Bay |
| 212 | IMG-3836 | Parent and child riding a Yamaha WaveRunner together |
| 211 | JetSkiRentTierraVerde | Rider on a WaveRunner near Tierra Verde waterfront homes |
| 210 | JetSkiRentStPetersburg | WaveRunners in calm bay water with kiteboarders near St. Petersburg |
| 209 | JetSkiRentStPetebeach | Guests riding WaveRunners side by side in green water near St. Pete Beach |
| 208 | CouplesJetSkiRetreat | Couples riding WaveRunners in clear shallow water |
| 207 | JetSkiCoupleCrystalClearWaters | Couple smiling on a Yamaha WaveRunner during a St. Petersburg jet ski tour |
| 206 | JetSkiBestFriends | Friends riding WaveRunners past waterfront homes and palm trees |
| 519 | JetSkiRentalLogo | Xtreme Jetski Watersports logo |

Do not use on the site: `399` (mountain lake, not Florida) and `382` (studio render, likely
a Yamaha press image).
