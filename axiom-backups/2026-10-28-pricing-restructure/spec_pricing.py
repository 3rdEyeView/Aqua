# Pricing (1068) copy, 2026-10-28. element id -> new text. Old text is checked against the backup by build_ops.py.
ADS_NOTE = ("Google Ads advertising spend is not included in the $597 subscription. You pay your advertising budget "
            "directly to Google. 3-month minimum commitment; cancellation terms are set out in your service agreement.")

FINE = ("Advertising spend is billed separately and paid directly by you through Google Ads. Growth includes management of "
        "one standard Google Search advertising program; additional campaigns, other advertising platforms, extensive "
        "creative work and custom marketing requirements are quoted separately. Advanced marketing solutions available by "
        "custom quote. Usage-based charges for SMS, calls, and applicable communication services may be billed separately, "
        "as disclosed in the service agreement. SMS automations are activated after the required carrier registration, "
        "approval and successful configuration, so timing varies by business. Website updates and support are provided "
        "within our standard service scope. Review requests are neutral invitations; reviews and ratings are never "
        "guaranteed. We do not guarantee leads, sales, revenue or specific advertising results.")

SPEC = {
    # hero
    '2fde0e1e': 'Simple monthly plans',
    '1196128b': 'Two plans.<br>Everything managed.',
    '4eb97eec': ('Choose Essentials for a professional website with essential business automations built in, or Growth '
                 'for a complete customer acquisition system with Google Ads management. Both plans have a $0 setup fee; '
                 'your first month is due at signup.'),
    # "included with every plan" strip
    '6800ff3b': 'Included with every plan',
    '28ad0480': 'Your website plus essential automations',
    '2bca7cb3': ('Every Axiom plan includes automated Google review requests, instant new-lead response and missed-call '
                 'text-back, so you respond faster without extra software.'),
    '4eba32ac': 'Automations go live after registration, approval and setup are complete.',
    # Essentials card
    '76353f67': 'Axiom Essentials',
    '5630fa9f': '$297',
    '4b7a09e2': 'Your professional website and essential business automations, all in one affordable monthly package.',
    '16108913': 'Professionally designed, mobile-responsive website',
    '2caced19': 'Website hosting, SSL &amp; ongoing maintenance',
    '7ce7c2e3': 'Website updates &amp; technical support',
    '4b43aee9': 'Foundational on-page SEO',
    '28c1eeb5': 'Contact forms &amp; lead capture',
    '7449181f': 'Included automations · Upon activation',
    '4a87d996': 'Automated Google review requests',
    '1a7aaa11': 'Instant new-lead response',
    # Growth card
    '794b76b3': '$597',
    '20099b6f': '3-month minimum',
    '3359b2ba': ('Your complete customer acquisition and business growth system: Google Ads brings in new inquiries, '
                 'and your CRM and automations follow up on every one.'),
    '4f288362': 'Everything in Essentials, plus',
    '1d2346d3': 'GoHighLevel CRM &amp; lead management pipeline',
    '1b73ded9': 'Advanced automated SMS &amp; email follow-up sequences',
    '5e162213': 'Appointment scheduling &amp; reminders',
    'f10a255':  'Lead nurturing workflows',
    '42df896f': 'Seven standardized business automations in total',
    '6ec3518e': 'Google Search Ads campaign setup &amp; ongoing management',
    '569b83c2': 'Campaign performance monitoring &amp; optimization',
    '4aa219b8': ADS_NOTE,
    '2c4b03c9': 'Get Started',
    # fine print
    '3f79b119': FINE,
    # why section
    '20d9252e': ('Custom websites usually start with a large invoice. With Axiom, your website is part of a monthly plan '
                 'instead: $297 a month for Essentials or $597 a month for Growth, with no setup fee. Your first month is '
                 'due at signup.'),
    '51a2234a': 'Need more than the standard plans?',
    '5a597acc': ('Additional ad campaigns, other advertising platforms, advanced automations and custom website work are '
                 'available as optional add-ons. Advanced marketing solutions available by custom quote.'),
    # closing CTA
    '361ed3f8': 'Essentials $297/month · Growth $597/month · $0 setup fee · First month due at signup',
}
DELETE = ['5384ebbd']  # Axiom Marketing card ($1,500)
# Phase 1 duplicates (new IDs are read back from the autosave and filled in phase 2):
#   1a7aaa11 -> Missed-call text-back automation
#   4f288362 -> Google Ads group label;  569b83c2 x2 -> reporting, priority support
DUPLICATE = ['1a7aaa11', '4f288362', '569b83c2', '569b83c2']
PHASE2 = {
    'after:1a7aaa11': 'Missed-call text-back automation',
    'label-ads': 'Customer acquisition · Google Ads',
    'report': 'Monthly advertising &amp; lead performance reporting',
    'priority': 'Priority support',
}
