# Yoast SEO, 2026-10-28. BEFORE = values live before this change (rollback). AFTER = new values.
BEFORE = {
 952: ('Axiom Systems | Website Design & Digital Marketing',
       'Axiom Systems builds and manages professional websites for small businesses. Plans start at $299/month with $0 setup. Explore websites, marketing and automation.'),
 1068: ('Website Plans & Pricing from $299/month | Axiom Systems',
        'Managed website plans for small businesses: Axiom Essential $299/month with $0 setup, Axiom Growth $599/month, and Google Ads management from $1,500/month.'),
 1074: ('Lead Automation & Google Ads Management | Axiom Systems',
        'Add Axiom Lead Automation for $349/month: instant lead response, missed-call text-back and automated follow-up. Plus Axiom Growth and managed Google Ads.'),
 1085: ('FAQ: Managed Website Plans & Pricing | Axiom Systems',
        'Answers about Axiom Systems website plans: what $299/month includes, setup fees, cancellation, ownership, Axiom CRM, lead automation and Google Ads.'),
 1095: ('Get Started with Axiom Systems | Request Your Website Plan',
        "Tell us about your business in a short form and we'll recommend the right plan. Nothing is charged to submit. Website plans start at $299/month."),
}
AFTER = {
 952: ('Axiom Systems | Small Business Websites, Google Ads & Automation',
       'Managed websites, Google Ads and automated follow-up for small businesses. Essentials $297/month; Growth $597/month with Google Ads management. $0 setup.'),
 1068: ('Pricing: Essentials $297/mo & Growth $597/mo | Axiom Systems',
        'Compare Axiom Essentials ($297/month) and Growth ($597/month, includes Google Ads management). $0 setup fee, first month due at signup, ad spend separate.'),
 1074: ('Optional Add-Ons & Custom Solutions | Axiom Systems',
        'Optional enhancements beyond Essentials and Growth: extra Google Ads campaigns, social ads, custom automations and website development, by custom quote.'),
 1085: ('FAQ: Managed Website Plans & Pricing | Axiom Systems',
        "Answers about Axiom Essentials ($297/month) and Growth ($597/month): what's included, Google Ads management and budget, setup fees, SMS charges and cancellation."),
 1095: ('Get Started with Axiom Systems | Request Your Website Plan',
        "Tell us about your business in a short form and we'll recommend the right plan. Nothing is charged to submit. Essentials $297/month, Growth $597/month."),
}
if __name__ == '__main__':
    for k, (t, d) in AFTER.items(): print(k, len(t), len(d))
