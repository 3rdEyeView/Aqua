# Branding, messaging & conversion pass (2026-10-23)

Positioning: Axiom Systems as one connected business system (website, Axiom CRM, automated
follow-up, Google review requests, lead generation), with no customer-facing GoHighLevel/GHL wording.
Brand casing kept as "Axiom" (owner's choice).

## Audit findings
- "GoHighLevel CRM" appeared on Pricing (Growth card) and Add-Ons (Growth card); "GoHighLevel CRM integration"
  on both Marketing cards. No other GHL wording on the 7 current pages, snippets or the form.
- The stored post_content (used by Yoast for auto descriptions/og:description) also contained "GoHighLevel".
- Four pages from the previous "Revenue Systems" site were still published and in the sitemap:
  /elementor-9/ (old homepage: "AI Automation", "+47% conversion rate"), /services/ (paid audit offer),
  /about-us/, /contact-axiom-systems/ ($175 audit; "Book a Free Booking Breakdown" -> app.gohighlevel.com).
- Traffic (Jetpack Stats, 2026 / last 60 days): elementor-9 890 / 40 (mostly from when it was the homepage),
  services 128 / 6, contact 82 / 4, about-us 76 / 7. Backlinks could not be checked: Site Kit's Search Console
  connection lacks the webmasters scope, and no backlink tool is connected. Saved in `traffic/`.

## Changes
Copy: `copy_spec.py` lists every edit (element ID, exact old text, new text). Applied with Elementor's own
manage-elements tool (staged autosave -> preview -> publish), so layout, styles, links and settings are untouched;
`diff_staged.py` confirmed only those elements changed. Pricing, inclusions, billing terms and disclosures unchanged.
- Home: eyebrow, H1 ("Websites that turn leads into customers."), hero intro (connected-system positioning),
  Essential section close (introduces Growth/Marketing), closing CTA heading/intro, one step line.
- Pricing: intro, review-request blurb, Essential/Growth/Marketing descriptions, Growth list (Axiom CRM line,
  outcome wording), Growth CTA "Grow My Business", Marketing "Axiom CRM lead tracking", fine print adds
  "Axiom CRM is our branded, managed setup of an established third-party CRM platform.", closing intro.
- Add-Ons: H1 "Build the system your business needs.", intro, review blurb, Lead Response and Follow-Up
  descriptions/bullets, Growth block ("One connected system."), CRM lines, "Axiom Business Automation"
  heading, "Axiom CRM" row, fine-print CRM disclosure, CTA "Grow My Business".
- FAQ: "Do you offer more than websites?" answer reworded; new question "What is Axiom CRM?" (duplicated
  accordion item, included automatically in the FAQ schema).
- How It Works: "No website logins to remember, no software to learn." (Growth clients do get a CRM login).
- post_content regenerated with the same replacements (`sync_content.py`), so search snippets match.
Legacy pages: snippet 1390 "Axiom Legacy Redirects" (`live-snippets/1390-main.php`), single-hop 301s:
  /contact-axiom-systems/ -> /get-started/, /about-us/ -> /#about (founder section), /elementor-9/ -> /,
  /services/ -> /pricing/; also excludes those IDs from the Yoast sitemap. Old page content left unchanged.
Menu 3 (theme menu shown on 404/search pages): removed items 135, 114, 231 (old pages). `before/menu3-items.json`.

## Rollback
- Copy: restore a page's `before/pages/<id>.json` Elementor data (see 2026-10-20 restore.py notes), or
  re-run manage-elements with the old texts from `copy_spec.py`; WordPress revisions also exist.
- Redirects: unpublish/delete snippet 1390. Menu: re-add the three items from `before/menu3-items.json`.

## Tests
- `tests/live/results.json`: 7 pages x 10 widths, header/CTA geometry identical to the previous release, no
  overflow/overlap/JS errors, mobile menu OK, phone links intact.
- `tests/functional-live.json`: Get Started form + ?plan label, empty submit blocked (no AJAX, no conversion),
  lead-tracking script and GT-55XGH597 present, click-to-call, schema.
- Redirects 301 in one hop, no loops; sitemap lists only the 7 current pages; no GHL text on any public page.
