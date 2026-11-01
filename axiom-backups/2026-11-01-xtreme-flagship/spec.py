# Content for the Xtreme-flagship change. TEXT: element id -> new text. Other ops listed per page.
import json
IDS = json.load(open('media/ids.json'))  # mobile 1490, desktop 1491, detail1 1492, detail2 1493
X, AQ, BR = 'https://xtremestpete.com/', 'https://jetskiadventureclearwater.com/', 'https://bragspressurewashing.com/'
def img(i): return {'image': {'src': {'id': i}, 'size': 'full'}}
def link(u): return {'destination': u, 'isTargetBlank': True, 'tag': 'a'}

HOME_TEXT = {
 # section intro
 '6476ebf': "Every Axiom site is designed from scratch around the business it belongs to. We start with our own: the business our founder owns and runs on the same systems we offer you. Every site here is live. Click through and see for yourself.",
 # large feature card -> Xtreme (flagship)
 '6f3ff5d5': 'xtremestpete.com',
 '4f8335fe': 'Founder-owned · Jet ski rentals &amp; guided tours · St. Petersburg, FL',
 '5173da27': 'Xtreme Jet Ski Watersports',
 '5196d46b': "Our flagship. Xtreme is owned and run by Axiom's founder, and it runs on the same website, marketing and follow-up systems we offer through Axiom. The site is built to turn visitors into booked tours, and inquiries get followed up instead of sitting in an inbox.",
 '4b398afe': 'Check Availability and a call button on the very first screen',
 'ebe72f': 'Every tour shows its length, its price and a Book button',
 'd158e38': 'Inquiries captured and followed up with the same automations Axiom plans include',
 '3d2e5045': 'View Website ↗',
 # second row: Aqua Safari (2nd) + Brags
 '5c6e1eeb': 'Every business gets its own website.',
 '3970fb67': "Aqua Safari sells guided jet ski tours on the same Gulf Coast as Xtreme, yet its website looks nothing like it. Brags Global needed six services to make sense at a glance. Your website should look like your business, not like a template.",
 '7372f1c7': 'Client website · Guided jet ski tours · Tarpon Springs, FL',
 '19482278': 'View Website ↗',
 '52d1635e': 'bragspressurewashing.com',
 '50a26dbb': 'Client website · Pressure washing &amp; coatings · Pinellas County, FL',
 '77fe7d1e': 'Brags Global',
 '6d2314de': 'A clean, confident website for a pressure washing and coatings company. Six services are easy to understand at a glance, and a free quote or a phone call is always one tap away.',
 '5d1a23b6': 'Visit the website ↗',
 # CTA band under the work
 '486d10a5': 'Get the same website, marketing and follow-up systems we run Xtreme on, with plans from $299 a month.',
 # founder section + FAQ
 '45bba0fb': "That's why Axiom works the way it does. Xtreme runs on the same website, marketing and follow-up systems we offer you, so we use everything we recommend. We build your site, we take care of it, and when you need something, you talk to a real person who already knows your business.",
 '48d59077': 'No. Every site is designed for the business it belongs to. Compare Xtreme and Aqua Safari above: same industry, same coastline, completely different websites.',
}
HOME_OTHER = [
 {'action': 'update', 'element_id': '68295952', 'settings': img(IDS['mobile'])},           # hero phone: Aqua -> Xtreme mobile
 {'action': 'update', 'element_id': '5be028aa', 'settings': {**img(IDS['desktop']), 'link': link(X)},
  'style': 'object-position: 50% 100%;'},                                                       # feature card image -> Xtreme
 {'action': 'update', 'element_id': '3d2e5045', 'settings': {'link': link(X)}},
 {'action': 'update', 'element_id': '429526b9', 'settings': {**img(945), 'link': link(BR)}, 'style': 'object-position: 50% 0%;'},
 {'action': 'update', 'element_id': '5d1a23b6', 'settings': {'link': link(BR)}},
]

OW_TEXT = {
 '1daf17a9': "Xtreme Jet Ski Watersports, the St. Petersburg tour company our founder owns and runs on Axiom's own systems. Aqua Safari, a guided jet ski tour operator in Tarpon Springs. A pressure washing and coatings company in Pinellas County. A custom tile contractor in Tampa Bay. Real businesses with real customers, and websites you can open and use right now.",
 # showroom index numbers (after reorder: Xtreme, Aqua, Brags, Tile)
 '48db5478': '01', '64e1e13b': '02', '25e865fc': '03',
 '603f2be9': 'Founder-owned · St. Petersburg',
 # Xtreme section
 '4a7f63e': '01',
 '3ed383c7': 'Founder-owned · Our flagship',
 '53f14a1b': 'Jet ski rentals and guided Gulf tours',
 '482868c0': "Xtreme is owned and run by Axiom's founder. It takes riders from St. Petersburg into open Gulf water: Egmont Key, Shell Key, Fort De Soto, sandbars and dolphins, with a local guide out front. It's where we use the website, marketing and follow-up systems we offer through Axiom, on a business we run ourselves.",
 '293c0285': "Someone looking at a jet ski tour wants three answers fast: where does it go, is there a spot, and how do I book? The site had to answer all three before anyone scrolls, and every inquiry needed a reply, even on a busy day on the water.",
 '13a5b560': "A bold site over real ride footage. Where the ride goes, Check Availability and a call button come first. Every tour has its length, its price and a Book button that opens online booking. Behind the site, inquiries are captured and followed up with the same automations Axiom plans include.",
 '348f779a': 'Where the ride goes, Check Availability and a call button, all on the first screen.',
 '62a68eb0': 'Every tour shows its length and price, with a Book button that goes straight to online booking.',
 '797a0426': 'Founder-owned · Online booking · Inquiry follow-up',
 '14528d89': 'View Website ↗',
 '6d8cc71f': "Our founder's own business: xtremestpete.com. Opens in a new tab.",
 # comparison (Xtreme column refreshed to the current site)
 '52a33ec4': "Xtreme and Aqua Safari both take people out on guided jet ski tours along Florida's Gulf Coast. On paper, they're the same kind of business. Here's how differently their websites introduce them.",
 '5546f2f6': 'A short, punchy promise over live ride footage',
 '66dc241': '“Jet Ski the Gulf. Land on an Island.”',
 '96af186': 'Guided tours to Egmont Key, Shell Key and open Gulf water',
 '5afa51cf': 'Google reviews and an owner-operated guide, up front',
 # Aqua Safari section (second)
 '457f916f': '02',
 '70e36183': 'Client website · Tours &amp; experiences',
 '1657e95': '02 · jetskiadventureclearwater.com',
 '71408d5a': 'View Website ↗',
 # Brags (third)
 '3d71995d': '03',
}
OW_OTHER = [
 {'action': 'update', 'element_id': '1df5542', 'settings': img(IDS['desktop']),
  'style': 'object-position: 50% 100%; @media(--mobile){ object-position: 50% 60%; }'},
 {'action': 'update', 'element_id': '7fb1be76', 'settings': img(IDS['detail1']), 'style_apply_mode': 'replace',
  'style': 'width: 100%; inset-block-start: 0; inset-inline-start: 0;'},
 {'action': 'update', 'element_id': '688cbb05', 'style': 'aspect-ratio: 2460 / 1008;'},
 {'action': 'update', 'element_id': '6eff2b7b', 'settings': img(IDS['detail2']), 'style_apply_mode': 'replace',
  'style': 'width: 100%; inset-block-start: 0; inset-inline-start: 0;'},
 {'action': 'update', 'element_id': '307e53e0', 'style': 'aspect-ratio: 2304 / 1008;'},
 {'action': 'update', 'element_id': '5f52cbc2', 'settings': {'image': {'src': {'id': IDS['desktop']}, 'size': 'large'}},
  'style': 'object-position: 50% 100%;'},
 {'action': 'update', 'element_id': '6017435c', 'style': 'background: #FF6123;'},
 {'action': 'update', 'element_id': '574dcc8c', 'style': 'background: #04293A;'},
 {'action': 'update', 'element_id': '1577e326', 'style': 'background: #F7F2EA; border: 1px solid rgba(10,22,40,0.12);'},
 {'action': 'update', 'element_id': '75e7d067', 'style': 'background: #00B5A6;'},
 # reorder showroom index: Xtreme, Aqua, Brags, Tile (parent 254508ff; index 0 is the "In this showroom" label)
 {'action': 'move', 'element_id': '1525b0a7', 'new_parent_id': '254508ff', 'index': 1},
 {'action': 'move', 'element_id': '122c827b', 'new_parent_id': '254508ff', 'index': 2},
 # reorder sections: hero, Xtreme, Aqua, comparison, Brags, Tile
 {'action': 'move', 'element_id': '1257a6db', 'new_parent_id': 'document', 'index': 2},
 {'action': 'move', 'element_id': '4a2a2cc', 'new_parent_id': 'document', 'index': 3},
 {'action': 'move', 'element_id': '69b631c5', 'new_parent_id': 'document', 'index': 4},
]
