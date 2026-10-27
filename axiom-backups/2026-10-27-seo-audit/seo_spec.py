# SEO titles and meta descriptions (2026-10-27). Literal text, no Yoast variables.
# Before-values: before/yoast/<id>.json. Prices and plan names follow the live Pricing/Add-Ons pages.
SEO = {
    952: ('Axiom Systems | Website Design & Digital Marketing',
          'Axiom Systems builds and manages professional websites for small businesses. Plans start at $299/month '
          'with $0 setup. Explore websites, marketing and automation.'),
    1013: ('How It Works: Managed Website Design | Axiom Systems',
           'How Axiom Systems designs, builds and launches a custom website for your small business, then hosts, '
           'updates, backs up and supports it every month.'),
    1031: ('Our Work: Small Business Website Design | Axiom Systems',
           'Live websites Axiom Systems designed and built for small businesses around St. Petersburg and Tampa Bay. '
           'Every site is custom-designed, never a template.'),
    1068: ('Website Plans & Pricing from $299/month | Axiom Systems',
           'Managed website plans for small businesses: Axiom Essential $299/month with $0 setup, Axiom Growth '
           '$599/month, and Google Ads management from $1,500/month.'),
    1074: ('Lead Automation & Google Ads Management | Axiom Systems',
           'Add Axiom Lead Automation for $349/month: instant lead response, missed-call text-back and automated '
           'follow-up. Plus Axiom Growth and managed Google Ads.'),
    1085: ('FAQ: Managed Website Plans & Pricing | Axiom Systems',
           'Answers about Axiom Systems website plans: what $299/month includes, setup fees, cancellation, ownership, '
           'Axiom CRM, lead automation and Google Ads.'),
    1095: ('Get Started with Axiom Systems | Request Your Website Plan',
           "Tell us about your business in a short form and we'll recommend the right plan. Nothing is charged to "
           'submit. Website plans start at $299/month.'),
    1413: ('Privacy Policy | Axiom Systems', None),  # unchanged; listed for the inventory only
}
if __name__ == '__main__':
    for pid, (t, d) in SEO.items():
        print(pid, len(t), t); d and print('    ', len(d), d)
