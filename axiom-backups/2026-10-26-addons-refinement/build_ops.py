# Phase 1: verifies each element's live text equals the expected "before" text, then
# writes manage-elements operations to ops/<id>.json. Texts for 1574deff/3f549d91 go to
# their duplicates in phase 2; the originals become the short taglines.
import json, os, urllib.request
from copy_spec import SPEC, DELETE
KEY = {'e-paragraph': 'paragraph', 'e-heading': 'title', 'e-button': 'text'}
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
TAGLINE = {'1574deff': 'Turn Great Service Into a Stronger Reputation.', '3f549d91': 'Never Miss an Opportunity.'}
TAG_CSS = "color: var(--ax-ink, #0A1628); font-family: var(--ax-display, Manrope), sans-serif; font-weight: 700; font-size: 1.05rem; line-height: 1.35; letter-spacing: -0.01em;"
def live(pid):
    req = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit', headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})
    return json.load(urllib.request.urlopen(req))
def index(els, out):
    for e in els:
        out[e['id']] = e; index(e.get('elements', []), out)
    return out
os.makedirs('ops', exist_ok=True); ok = True
for pid, edits in SPEC.items():
    page = live(pid); backup = json.load(open(f'before/pages/{pid}.json'))
    if page['meta']['_elementor_data'] != backup['meta']['_elementor_data']:
        print(pid, 'CHANGED SINCE BACKUP'); ok = False
    els = index(json.loads(page['meta']['_elementor_data']), {})
    ops = []
    if pid == 1074:
        ops += [{'action': 'duplicate', 'element_id': e} for e in ('1574deff', '3f549d91', '5e295794', '5e295794', '5e295794')]
    for eid, (old, new) in edits.items():
        el = els.get(eid); key = KEY.get(el and el.get('widgetType'))
        cur = el and key and el['settings'][key]['value']
        if isinstance(cur, dict): cur = cur.get('content')
        if cur != old:
            print(pid, eid, 'MISMATCH', repr(cur)[:120]); ok = False; continue
        if eid in TAGLINE:
            ops.append({'action': 'update', 'element_id': eid, 'settings': {key: TAGLINE[eid]}, 'style': TAG_CSS})
        else:
            ops.append({'action': 'update', 'element_id': eid, 'settings': {key: new}})
    if pid == 1074:
        ops.append({'action': 'update', 'element_id': '5cd41bfc', 'settings': {'link': {'destination': '/get-started/?plan=lead-automation', 'isTargetBlank': False, 'tag': 'a'}}})
        ops.append({'action': 'update', 'element_id': '39b068c4', 'style': 'grid-template-columns: 1fr 1fr;'})
    for e in DELETE.get(pid, []):
        assert e in els; ops.append({'action': 'delete', 'element_id': e})
    json.dump(ops, open(f'ops/{pid}.json', 'w'), indent=1)
    print(pid, page['slug'], len(ops), 'ops')
print('ALL OK' if ok else 'PROBLEMS')
