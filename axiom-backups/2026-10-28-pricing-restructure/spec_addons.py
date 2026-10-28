# Add-Ons (1074), 2026-10-28. Plans first (what's already included), then optional add-ons by custom quote.
# "Custom quote" = services Axiom already delivers today (Google Ads, GHL/CRM work, custom web development).
# "Available by consultation" = not yet verified as a standard deliverable; owner to confirm (see README).
CQ, BC = 'Custom quote', 'Available by consultation'
QUOTE = {'destination': '/get-started/?plan=custom-quote', 'isTargetBlank': False, 'tag': 'a'}
SPEC = {
    # hero
    '5d1c3af9': 'Optional add-ons',
    '6e146e8': 'Go further<br>when you\'re ready.',
    '4961b413': ('Your Essentials or Growth plan already covers your website, hosting, support and the automations most '
                 'small businesses need. Add-ons are optional enhancements for businesses that want even more.'),
    '7d71cc2d': 'Most businesses don\'t need anything on this page.',
    '645c77ea': ('Essentials and Growth already include substantial value.<br>Everything else here is optional and '
                 'quoted to your needs.'),
    # plan card 1: Essentials
    '4e2c0804': 'Included in Essentials',
    '1747bf49': 'Axiom Essentials',
    '1d5f28a7': '$297',
    '61269a0a': '/month · $0 setup fee',
    '1173c05d': 'Your website and essential automations.',
    '1574deff': ('Your professional website and essential business automations, all in one affordable monthly package: '
                 'design, hosting, SSL, maintenance, updates, support and foundational on-page SEO.'),
    '16f6e08e': 'Automated Google review requests',
    '4d107e02': 'Instant new-lead response',
    '25cb0a2d': 'Missed-call text-back automation',
    '3f1d5914': 'Get Started →',
    # plan card 2: Growth
    '73d16fdc': 'Recommended · Includes Google Ads management',
    '799af7e9': 'Axiom Growth',
    '748dd511': '$597',
    '6da72b6e': '/month · $0 setup fee',
    '466a0739': 'Your complete customer acquisition system.',
    '3f549d91': ('Everything in Essentials, plus a CRM, advanced follow-up and Google Search Ads managed for you, so new '
                 'inquiries come in and every one gets a timely response.'),
    '78df7460': 'GoHighLevel CRM &amp; lead management pipeline',
    '631392d6': 'Advanced SMS &amp; email follow-up sequences',
    '5e295794': 'Appointment scheduling, reminders &amp; lead nurturing',
    '423ee687': 'Seven standardized business automations in total',
    '960b165': 'Google Search Ads setup &amp; ongoing management',
    '646c6719': 'Monthly advertising &amp; lead performance reporting',
    '5cd41bfc': 'Get Started →',
    '1a720fb3': ('Google Ads advertising spend is not included in the Growth subscription and is paid directly by you '
                 'through Google Ads. Growth includes management of one standard Google Search advertising program. '
                 'Usage-based charges for SMS, calls, and applicable communication services may be billed separately, '
                 'as disclosed in the service agreement. Automations are activated after the required registration, '
                 'approval and successful configuration. Results are not guaranteed.'),
    # catalogue (former "what's included where" map)
    '11911384': 'Optional add-ons',
    '3a2fef0b': 'Enhancements beyond the standard plans.',
    '6b108ad3': ('Pricing depends on your goals and scope. Tell us what you have in mind and we\'ll confirm what\'s '
                 'possible and quote it before any work begins. Advanced marketing solutions available by custom quote.'),
    # advertising column (moved first)
    '4652ceac': 'Advanced Advertising Services',
    '55faa04c': 'Additional Google Ads campaigns', '5b37d931': CQ,
    '22b38ced': 'Facebook &amp; Instagram advertising management', '525b16d3': BC,
    'd3aa34f': 'Multi-platform advertising', '7dba399d': BC,
    '3c6a6564': 'Advanced landing pages &amp; conversion optimization', '7d771d1': CQ,
    '37a5c064': 'Ask about advertising →',
    # automation column
    '6147a1c9': 'Advanced Business Automations',
    '2c8f448': 'Custom workflow development', '36ef9305': CQ,
    '2c8d98d2': 'AI receptionist &amp; advanced phone automation', '60031ca5': BC,
    '4d3204cf': 'Additional CRM integrations', '2945818': CQ,
    '76a206c1': 'Custom appointment &amp; sales processes', '1e5ba4c4': CQ,
    '3762d562': 'Ask about automations →',
    # website column
    '7938f864': 'Additional custom functionality', '39a48b78': CQ,
    '3f45be38': 'E-commerce integrations', '1f02f930': CQ,
    '5a1446d1': 'Advanced SEO services', '75fea50f': BC,
    '6d57485e': 'Ask about website work →',
    # closing CTA
    '594acca6': 'Let\'s find the<br>right fit.',
    '67214b41': ('Start with Essentials or Growth, and add enhancements whenever your business is ready. We\'ll '
                 'recommend what makes sense, and nothing you don\'t need.'),
    'df2995f': 'Essentials $297/month · Growth $597/month · Add-ons by custom quote',
}
DELETE = ['2689dc5b', '3c7a9f0d']  # Growth price-math block ($648 / Save $49) and Axiom Marketing card ($1,500)
DUPLICATE = ['67f757e6', '34a6e02e']  # 5th automation row, 4th website row (texts set in phase 2)
LINKS = {'3f1d5914': '/get-started/?plan=essential', '5cd41bfc': '/get-started/?plan=growth',
         '37a5c064': '/get-started/?plan=custom-quote', '3762d562': '/get-started/?plan=custom-quote',
         '6d57485e': '/get-started/?plan=custom-quote'}
EXTRA = [{'action': 'update', 'element_id': k, 'settings': {'link': {'destination': v, 'isTargetBlank': False, 'tag': 'a'}}}
         for k, v in LINKS.items()]
EXTRA.append({'action': 'move', 'element_id': '36424498', 'new_parent_id': '152f1e66', 'index': 0})
