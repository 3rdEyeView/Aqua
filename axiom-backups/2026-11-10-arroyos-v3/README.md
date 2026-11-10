# Arroyo's Lawn Care — V3 sales demo (2026-11-10), NOT published

Local preview only, for a Zoom sales call. Built from the V2 page (`../2026-11-10-arroyos-v2/src.html`) plus `parts/`.
WordPress page 1716, snippet 1733, the media library, the CRM, messaging, ad accounts and tracking were not touched.

- `arroyo-v3-sales-demo.html`: the deliverable. One self-contained file, opens offline, makes no network requests.
- `python3 -I build.py` assembles `src.html` and the single file. `node check.js` runs the browser checks and writes `shots/`.

## Creative reference
https://www.instagram.com/p/Dd4LPGlxkz1/ could not be viewed: instagram.com is outside this session's allowed network.
The fallback concept from the brief was built instead.

## View 1 — Homeowner page: cinematic project reveal (replaces the V2 hero)
Desktop (≥900 px wide, motion allowed): a pinned, scroll-scrubbed scene.
1. Beginning: Arroyo's drone loop full bleed with the headline.
2. Reveal: DESIGNED. / BUILT. / MAINTAINED. cross the frame in alternating directions while the footage holds and pushes in.
3. Montage cut: a different Arroyo property (driveway island) opens from a centre slit, then the full-screen close-up
   (bottle palms and ti plants, their photo `clean-1011`) wipes up and settles from a tight crop.
4. Finish: project details and Request an Estimate arrive. The 01/02/03 rail on the right jumps between the three parts.
The footage and both photos are different properties, so the transition is cut as a montage, not a continuous move.
Phones: no scroll scrubbing. The footage stays put (CSS sticky) while the panels scroll over it, with one-shot fades.
Reduced motion: no video, no transitions, everything static in normal flow.
A Request an Estimate button is on screen at every point (header button on desktop, bottom bar on phones).

## View 2 — "See What Happens to a Lead" (presenter bar at the top switches views; `#lead-demo` opens it directly)
Start Sample Ad Visit → estimate form with a simulated Google Ads source → Send → the lead appears in an Axiom CRM-style
panel (service, contact details, ad source, timeline). Then: 2 No reply yet (clock jumps to Wed 9:00 AM, follow-up sent,
next one scheduled) → 3 Homeowner replies / books (stage moves, automation stops, pending message cancelled). Reset demo.
Texts only appear when the SMS opt-in box is ticked; unticked shows "Text not sent" and the email-only path.
All names, numbers, campaign, click ID, times and the follow-up cadence are sample values, not Axiom's real settings.
