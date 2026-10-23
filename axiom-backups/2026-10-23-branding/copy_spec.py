# Copy changes for the Axiom branding & conversion pass (2026-10-23).
# Each entry: page ID -> {element ID: (current text, new text)}. apply.py refuses
# to write a page if any current text differs from what is live.

CRM_LINE = 'Axiom CRM: leads, conversations &amp; pipeline in one place'
GROWTH_PITCH = ('Our complete business system. Your website, Axiom CRM, missed-call recovery and automated '
                'follow-up work together, so fewer leads slip away and more inquiries become paying customers.')
REVIEW_PITCH = ('Every Axiom website plan includes automated Google review requests, so each completed job gets a '
                'timely, neutral invitation to leave a review and your online reputation keeps growing.')

SPEC = {
    # ---------------------------------------------------------------- Home
    952: {
        '46921639': ('Website as a Service for local businesses',
                     'Websites, CRM &amp; automation for local businesses'),
        '356e689d': ('Professional websites for local businesses.',
                     'Websites that turn leads into customers.'),
        '1b220467': ("Axiom designs and builds a custom website for your business, then hosts it, maintains it and keeps it up to date, with free automated Google review follow-ups included. When you're ready, we can automate your follow-up and run your Google Ads too.",
                     "Axiom builds and manages the systems local businesses need to grow: a custom website we host and maintain, free Google review requests, and, when you're ready, Axiom CRM, automated follow-up and Google Ads. One connected system. Less manual work. More leads turned into paying customers."),
        '4d6f36aa': ("Here's what $299 a month covers, from the first design to every update after launch. Want automated follow-up or Google Ads? Our Growth and Marketing plans take it further.",
                     "Here's what $299 a month covers, from the first design to every update after launch. Ready for more? Axiom Growth adds Axiom CRM, missed-call text-back and automated follow-up, and Axiom Marketing brings in new leads with Google Ads."),
        '9abfe10': ("Let's build a website you never have to worry about.",
                    "Let's build the system behind your next customer."),
        '5daf889c': ("Tell us a little about your business. We'll talk through what your website needs, answer every question and show you what's possible before you commit to anything.",
                     "Tell us a little about your business and how leads reach you today. We'll recommend the right setup, answer every question and show you what's possible before you commit to anything."),
        '1f98832b': ('We talk through what your site needs', 'We recommend the right plan for your goals'),
    },
    # ---------------------------------------------------------------- Pricing
    1068: {
        '4eb97eec': ('Start with a professionally managed website. Add automated follow-up or full lead generation when your business is ready.',
                     'Start with a professionally managed website. Add Axiom CRM and automated follow-up, or bring in new leads with Google Ads, when your business is ready. Every plan builds on the same connected system.'),
        '2bca7cb3': ('Your website does more than look good. Every Axiom website includes automated Google review follow-ups to help you build your online reputation.',
                     REVIEW_PITCH),
        '4b7a09e2': ('A professional website, built and managed for you, with essential automation included.',
                     'A conversion-focused website, built and managed for you, with Google review requests and instant inquiry replies included.'),
        '3359b2ba': ('Turn more inquiries into booked customers with automated systems that follow up even when you\'re busy.',
                     GROWTH_PITCH),
        '1d2346d3': ('GoHighLevel CRM', CRM_LINE),
        '1b73ded9': ('Missed-call text-back', 'Missed-call text-back to recover lost calls'),
        '5e162213': ('Multi-step SMS &amp; email lead follow-up', 'Automated multi-step SMS &amp; email follow-up'),
        'f10a255': ('Lead management pipeline', 'Pipeline from new lead to paying customer'),
        '4aa219b8': ("For businesses that already get leads and want help responding, organizing and converting them. No long-term contract: cancel anytime with 30 days' written notice.",
                     "Built for businesses that already get calls and inquiries and want to respond faster, follow up consistently and win more of them. No long-term contract: cancel anytime with 30 days' written notice."),
        '2c4b03c9': ('Automate My Business', 'Grow My Business'),
        '3b853f8a': ('Generate more qualified opportunities, capture every inquiry, and turn more advertising clicks into real business conversations.',
                     'Bring in new leads with Google Ads, then capture and follow up with them automatically, so more of your ad spend turns into real customer conversations.'),
        '3044bf61': ('GoHighLevel CRM integration', 'Axiom CRM lead tracking'),
        '3f79b119': ('Review requests are neutral and sent after completed services; reviews and ratings are never guaranteed. All automated messaging is subject to reasonable usage limits and applicable consent requirements. Custom booking-software integrations and high-volume messaging are not included. Questions first? Email axiom.systems.co@gmail.com',
                     'Review requests are neutral and sent after completed services; reviews and ratings are never guaranteed. All automated messaging is subject to reasonable usage limits and applicable consent requirements. Custom booking-software integrations and high-volume messaging are not included. Axiom CRM is our branded, managed setup of an established third-party CRM platform. Questions first? Email axiom.systems.co@gmail.com'),
        '369aee85': ("Tell us about your business and what you want your website and marketing to do. We'll recommend a plan and answer every question before you sign up.",
                     "Tell us about your business and what you want your website, follow-up and marketing to do. We'll recommend a plan and answer every question before you sign up."),
    },
    # ---------------------------------------------------------------- Add-Ons
    1074: {
        '6e146e8': ('Add what your<br>business needs.', 'Build the system<br>your business needs.'),
        '4961b413': ('Add individual automations to Axiom Essential, or get them all together with Axiom Growth.',
                     'Respond faster, follow up consistently and win more of the leads you already get. Add individual automations to Axiom Essential, or get everything working together with Axiom Growth.'),
        '1574deff': ('Your website does more than look good. Every Axiom website includes automated Google review follow-ups to help you build your online reputation.',
                     REVIEW_PITCH),
        '3f549d91': ("Reply to new customers quickly, even when you're busy on a job.",
                     "Reply to new leads right away, even when you're busy on a job, so fewer opportunities go to the next business on the list."),
        '631392d6': ('New lead notifications', 'Instant new-lead notifications'),
        '5e295794': ('Automated first response', 'Automated first reply to every new inquiry'),
        '12a96998': ('Keep following up with new leads after the first conversation.',
                     'Stay in front of every lead until they\'re ready to book, without having to remember who to call back.'),
        '13eb522c': ('Lead nurturing', 'Lead nurturing until they\'re ready to buy'),
        '5bed5140': ('Everything working together.', 'One connected system.'),
        '4c7dd1a6': ('Turn more inquiries into booked customers with automated systems that follow up even when you\'re busy.',
                     'Axiom Growth is our complete business system: your website, Axiom CRM, missed-call recovery and automated follow-up working together, so fewer leads slip away and more inquiries become paying customers.'),
        'be5cdd': ('Automate My Business', 'Grow My Business'),
        '65851d63': ('GoHighLevel CRM', CRM_LINE),
        '1b8712fe': ('Missed-call text-back', 'Missed-call text-back to recover lost calls'),
        '7181ca8b': ('Multi-step SMS &amp; email follow-up', 'Automated multi-step SMS &amp; email follow-up'),
        '79f0f036': ('Lead management pipeline', 'Pipeline from new lead to paying customer'),
        '36b98ca1': ('GoHighLevel CRM integration', 'Axiom CRM lead tracking'),
        '6147a1c9': ('Business Automation', 'Axiom Business Automation'),
        '76a206c1': ('CRM integration', 'Axiom CRM'),
        '1a720fb3': ("Add-on prices are in addition to your $299/month Axiom Essential plan. Both are included with Axiom Growth, so you're never charged twice. Automation features are available upon activation and subject to reasonable usage limits and applicable consent requirements.",
                     "Add-on prices are in addition to your $299/month Axiom Essential plan. Both are included with Axiom Growth, so you're never charged twice. Automation features are available upon activation and subject to reasonable usage limits and applicable consent requirements. Axiom CRM is our branded, managed setup of an established third-party CRM platform."),
    },
    # ---------------------------------------------------------------- FAQ
    1085: {
        '25f6be41': ('Do you offer anything besides websites?', 'Do you offer more than websites?'),
        '6317b72a': ('Yes. Axiom Growth ($599/month) adds automated lead follow-up, missed-call text-back, a CRM pipeline and appointment reminders. Axiom Marketing (from $1,500/month) adds Google Ads management and landing pages, and works with your existing website. Lead Response and Follow-Up Automation can also be added to Axiom Essential. See the Pricing and Add-Ons pages for details.',
                     'Yes. Axiom Growth ($599/month) is our complete business system: your website plus Axiom CRM, missed-call text-back, automated lead follow-up, a sales pipeline and appointment reminders. Axiom Marketing (from $1,500/month) adds Google Ads management and landing pages, and works with your existing website. Lead Response and Follow-Up Automation can also be added to Axiom Essential. See the Pricing and Add-Ons pages for details.'),
    },
    # ---------------------------------------------------------------- How It Works
    1013: {
        '4bd43adc': ('That\'s it. No logins to remember, no dashboards to learn.',
                     'That\'s it. No website logins to remember, no software to learn.'),
    },
}

# New FAQ item, cloned from the "Do you offer more than websites?" item and
# inserted right after it (page 1085, accordion 45f84265).
NEW_FAQ = {
    'page': 1085,
    'after_item': '76c8c320',
    'question': 'What is Axiom CRM?',
    'answer': ('Axiom CRM is the customer management system we set up and manage for Axiom Growth and Axiom Marketing '
               'clients. It brings your leads, conversations, appointments and sales pipeline into one place, with '
               'automated follow-up running in the background. It\'s our branded, managed setup of an established '
               'third-party CRM platform, so you get proven software without having to configure it yourself.'),
}
