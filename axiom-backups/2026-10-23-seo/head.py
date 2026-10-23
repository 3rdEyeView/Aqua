# Extracts the SEO-relevant head tags of each live page into a JSON snapshot.
import json, re, sys, html, urllib.request
PAGES = {952: '/', 1068: '/pricing/', 1074: '/add-ons/', 1085: '/faq/', 1095: '/get-started/', 1013: '/how-it-works/', 1031: '/our-work/'}
out = {}
for pid, path in PAGES.items():
    h = urllib.request.urlopen(urllib.request.Request('https://axiomsystems.systems' + path + sys.argv[2], headers={'User-Agent': 'Mozilla/5.0'})).read().decode()
    head = h[:h.find('</head>')]
    meta = lambda attr, name: [html.unescape(m) for m in re.findall(r'<meta (?:%s)=[\'"]%s[\'"] content=[\'"]([^\'"]*)[\'"]' % (attr, re.escape(name)), head)]
    graph = [json.loads(s) for s in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S)]
    out[path] = {
        'title': [html.unescape(t) for t in re.findall(r'<title>(.*?)</title>', head, re.S)],
        'description': meta('name', 'description'), 'robots': meta('name', 'robots'),
        'canonical': re.findall(r'<link rel="canonical" href="([^"]*)"', head),
        'og:title': meta('property', 'og:title'), 'og:description': meta('property', 'og:description'),
        'og:site_name': meta('property', 'og:site_name'), 'og:url': meta('property', 'og:url'),
        'twitter': meta('name', 'twitter:card'),
        'schema_types': [[n.get('@type') for n in g.get('@graph', [g])] for g in graph],
        'schema_names': {n.get('@type') if isinstance(n.get('@type'), str) else str(n.get('@type')): n.get('name') for g in graph for n in g.get('@graph', [g]) if n.get('@type') in ('WebPage', 'WebSite', 'Organization', 'FAQPage')},
        'org_telephone': [n.get('telephone') for g in graph for n in g.get('@graph', [g]) if n.get('@type') == 'Organization'],
        'gtag': h.count('GT-55XGH597'), 'tel_links': h.count('href="tel:+17275917527"'), 'form': h.count('axgs-lead-js'),
    }
json.dump(out, open(sys.argv[1], 'w'), indent=1, ensure_ascii=False)
for p, v in out.items(): print(p, v['title'], v['description'], v['robots'], v['canonical'])
