# Axiom Systems — backup before pricing & add-on expansion

Taken 2026-10-20 (UTC) from https://axiomsystems.systems before any pricing changes.
Pages had not been modified since late September; contents verified identical to live at backup time.

## Contents
- `pages/<id>.json` — full REST export (context=edit): title, slug, status, template, raw content and
  Elementor meta (`_elementor_data`, `_elementor_page_settings`, edit mode, template type).
  952 Home · 1068 Pricing · 1074 Add-Ons · 1085 FAQ · 1095 Get Started · 1013 How It Works · 1031 Our Work · 107 Services (legacy)
- `snippets/` — original source of Angie snippets 1099 (Get Started form), 1134 (front page), 1135 (mobile menu).
- `seo/` — Yoast data per page (no custom titles/descriptions were set; 107 Services was indexable).
- `global/` — Elementor global class and variable lists (not modified by this work).
- `restore.py` — writes a page's saved Elementor data/settings/template back via REST.

Restore was tested: the Pricing backup written into a temporary draft rendered text-identical to the
live Pricing page at the same height (the draft was then deleted). WordPress/Elementor revisions also exist.

## Original pricing & CTAs
| Location | Offer | CTA → destination |
|---|---|---|
| Pricing | Premium Managed Website $299/mo, $0 setup, cancel anytime | Get Started → /get-started/ |
| Add-Ons | Review Automation +$99/mo | /get-started/?plan=review-automation |
| Add-Ons | Lead Response +$149/mo | /get-started/?plan=lead-response |
| Add-Ons | Follow-Up Automation +$199/mo | /get-started/?plan=follow-up-automation |
| Add-Ons | Axiom Growth System $597/mo ($746 individually, save $149, $0 setup) | /get-started/?plan=growth-system |
| Home, How It Works, Our Work, FAQ, Get Started | $299/month · $0 setup fee · Cancel anytime | /get-started/ |

Snippet 1099 plan keys: growth-system, review-automation, lead-response, follow-up-automation.
No checkout/payment links existed on these pages. Tracking: GA4 GT-55XGH597, Google Ads AW-17878870459.

## Staging (2026-10-20)
All page changes are staged on draft copies, not on the live pages:
1309 Pricing · 1310 Add-Ons · 1311 Home · 1312 Our Work · 1313 FAQ · 1314 Get Started · 1315 How It Works.
`proposed-snippets/` holds the reviewed new source for snippets 1099 (plan keys + legacy aliases) and
1135 (mobile-menu copy). Snippets go live when saved, so they are applied only at publish time.

### Publish procedure (after approval)
1. Re-verify each live page still matches `pages/<id>.json` (no edits since backup).
2. Copy each staging draft's `_elementor_data` and page settings into its live page via REST,
   re-apply the `elementor_canvas` template, regenerate Elementor CSS, and confirm the render.
3. Save `proposed-snippets/` into snippets 1099 and 1135.
4. Set Services (107) to noindex in Yoast (this also removes it from the XML sitemap).
5. Clear the Kinsta cache, re-run QA on the live URLs, then delete the staging drafts.
Rollback: `restore.py <ids>` plus the original `snippets/` sources; set 107 back to index.

## Published 2026-10-20/21 (UTC)
Approved changes are live on 952, 1068, 1074, 1085, 1095, 1013, 1031; snippets 1099 and 1135 are
updated and published; Services (107) is noindex (out of the sitemap) and its Primary Menu item 205
was removed (`menu3-before.json` has the original menu). `after-publish/` holds the live state after
publication. Staging drafts 1309–1315 were deleted after verification.

Rollback notes learned during publish:
- After writing `_elementor_data` via REST, Elementor keeps serving cached HTML. Save the page once
  through Elementor (any element update via the Elementor MCP, then `elementor-publish-document`),
  then re-apply the `elementor_canvas` template.
- Snippet file changes only go live after `angie-publish-snippet`.
- Yoast descriptions come from post_content; regenerate it from the rendered page after a restore.
- To restore the menu item: add a Primary Menu item for page 107 at position 3.
- To re-index Services: set Yoast noindex back to null for page 107.
