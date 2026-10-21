# Add-Ons Marketing card (2026-10-21)

`1074.json` is the live Add-Ons page before the Marketing card was added; `1074-after-publish.json` is the published result.
Rollback: run `../2026-10-20-pricing-expansion/restore.py` logic with `1074.json` (POST its Elementor data and settings), save the page once through Elementor, re-apply `elementor_canvas`, then regenerate post_content for the Yoast description.
