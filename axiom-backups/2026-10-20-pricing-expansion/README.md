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
