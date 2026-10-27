# Builds the Privacy Policy page's Elementor data from the live site's own sections:
# header + footer from Get Started (1095, no active nav item), hero + two-column section layout from FAQ (1085).
# New element/style IDs are generated; global classes are reused so typography matches the site.
import copy, json, random, sys
sys.path.insert(0, 'build')
import policy_content as P
random.seed(20261027)
gs = json.loads(json.load(open('before/1095.json'))['meta']['_elementor_data'])
faq = json.loads(json.load(open('before/page-1085.json'))['meta']['_elementor_data'])
used = set()
def collect(e):
    used.add(e['id']); [collect(c) for c in e.get('elements', [])]
for e in gs + faq: collect(e)
def nid():
    while True:
        x = '%07x' % random.getrandbits(28)
        if x not in used: used.add(x); return x
def find(e, i):
    if e['id'] == i: return e
    for c in e.get('elements', []):
        r = find(c, i)
        if r: return r
def restyle(el, new_id):
    """Copy an element's local style under a new element id (style ids embed the element id)."""
    el['id'] = new_id
    styles = el.get('styles') or {}
    if not styles: return el
    (old_sid, st), = styles.items()
    sid = 'e-%s-%04x' % (new_id, random.getrandbits(16))
    st = copy.deepcopy(st); st['id'] = sid
    el['styles'] = {sid: st}
    el['settings']['classes']['value'] = [sid if c == old_sid else c for c in el['settings']['classes']['value']]
    return el
def size(v, u='rem'): return {'$$type': 'size', 'value': {'size': v, 'unit': u}}
def variant(bp, props): return {'meta': {'breakpoint': bp, 'state': None}, 'props': props, 'custom_css': None}

header, footer = copy.deepcopy(gs[0]), copy.deepcopy(gs[-1])
assert footer['settings'].get('tag', {}).get('value') == 'footer'

# Footer: add a "Privacy Policy" link styled like the other footer links, right after FAQ.
def add_privacy_link(ft):
    def walk(e):
        kids = e.get('elements', [])
        for i, c in enumerate(kids):
            if c.get('widgetType') == 'e-button' and c['settings'].get('text', {}).get('value') == 'FAQ':
                link = restyle(copy.deepcopy(c), nid())
                link['settings']['text']['value'] = 'Privacy Policy'
                link['settings']['link']['value']['destination'] = {'$$type': 'url', 'value': '/privacy-policy/'}
                link['editor_settings'] = {'title': 'fl-privacy'}
                kids.insert(i + 1, link); return True
            if walk(c): return True
    assert walk(ft), 'footer FAQ link not found'
add_privacy_link(footer)

# Hero (FAQ "top" section) with new text.
hero = copy.deepcopy(faq[1])
eyebrow, title, lead = find(hero, '4c4889be'), find(hero, '21bc7ba1'), find(hero, '3931f4e9')
eyebrow['settings']['paragraph']['value'] = P.HERO_EYEBROW
title['settings']['title']['value'] = P.HERO_TITLE
lead['settings']['paragraph']['value'] = P.HERO_LEAD
def renew(e):
    restyle(e, nid()); [renew(c) for c in e.get('elements', [])]
renew(hero)
hero['settings']['_cssid'] = {'$$type': 'string', 'value': 'top'}

# Content section: FAQ "questions" section and container, then one FAQ-style grid per policy section.
section = copy.deepcopy(faq[2]); container = section['elements'][0]
grid_tpl, h2_tpl = find(faq[2], '278beb87'), find(faq[2], '4af02706')
para_tpl = find(faq[2], '5bd9860e')
grids = []
for label, paras in P.SECTIONS:
    g = restyle(copy.deepcopy({k: v for k, v in grid_tpl.items() if k != 'elements'}), nid())
    h = restyle(copy.deepcopy(h2_tpl), nid()); h['settings']['title']['value'] = label
    bid = nid(); bsid = 'e-%s-%04x' % (bid, random.getrandbits(16))
    body = {'id': bid, 'elType': 'e-flexbox', 'settings': {'classes': {'$$type': 'classes', 'value': [bsid]}},
            'elements': [], 'isInner': False, 'editor_settings': {'title': 'policy-body'}, 'version': '0.0',
            'styles': {bsid: {'id': bsid, 'label': 'local', 'type': 'class', 'variants': [
                variant('desktop', {'min-width': size(0, 'px'), 'padding': {'$$type': 'dimensions', 'value': {'block-start': size(1.6), 'inline-end': size(0, 'px'), 'block-end': size(0, 'px'), 'inline-start': size(0, 'px')}},
                                    'display': {'$$type': 'string', 'value': 'flex'}, 'flex-direction': {'$$type': 'string', 'value': 'column'}, 'gap': size(1),
                                    'border-width': {'$$type': 'border-width-v2', 'value': {'block-start': size(1, 'px'), 'inline-end': size(0, 'px'), 'block-end': size(0, 'px'), 'inline-start': size(0, 'px')}},
                                    'border-color': {'$$type': 'color', 'value': '#E2E7EE'}, 'border-style': {'$$type': 'string', 'value': 'solid'}}),
                variant('mobile', {'padding': {'$$type': 'dimensions', 'value': {'block-start': size(1), 'inline-end': size(0, 'px'), 'block-end': size(0, 'px'), 'inline-start': size(0, 'px')}}, 'gap': size(0.85)}),
            ]}}}
    for t in paras:
        p = copy.deepcopy(para_tpl); p['id'] = nid(); p['settings']['paragraph']['value'] = t
        p['editor_settings'] = {'title': 'policy-text'}; body['elements'].append(p)
    g['elements'] = [h, body]; g['editor_settings'] = {'title': 'policy-section'}
    grids.append(g)
container['elements'] = grids
restyle(container, nid()); restyle(section, nid())
section['settings']['_cssid'] = {'$$type': 'string', 'value': 'policy'}

data = [header, hero, section, footer]
ids = []
def allids(e): ids.append(e['id']); [allids(c) for c in e.get('elements', [])]
for e in data: allids(e)
assert len(ids) == len(set(ids)), 'duplicate element ids'
json.dump(data, open('build/elementor_data.json', 'w'))
print('elements:', len(ids), '| sections:', len(grids), '| bytes:', len(json.dumps(data)))
