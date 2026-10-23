# Builds manage-elements operations from copy_spec.py after checking that each
# element's current live text is exactly the expected "before" text.
import json, sys, urllib.request, os
from copy_spec import SPEC, NEW_FAQ
KEY = {'e-paragraph': 'paragraph', 'e-heading': 'title', 'e-button': 'text'}
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
def live(pid):
    req = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit', headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})
    return json.load(urllib.request.urlopen(req))
def index(els, out):
    for e in els:
        out[e['id']] = e; index(e.get('elements', []), out)
    return out
os.makedirs('ops', exist_ok=True)
ok = True
for pid, edits in SPEC.items():
    page = live(pid); backup = json.load(open(f'before/pages/{pid}.json'))
    if page['meta']['_elementor_data'] != backup['meta']['_elementor_data']:
        print(pid, 'CHANGED SINCE BACKUP'); ok = False
    els = index(json.loads(page['meta']['_elementor_data']), {})
    ops = []
    for eid, (old, new) in edits.items():
        el = els.get(eid)
        key = KEY.get(el and el.get('widgetType'))
        cur = el and key and el['settings'][key]['value']
        if cur != old:
            print(pid, eid, 'MISMATCH', repr(cur)[:120]); ok = False; continue
        ops.append({'action': 'update', 'element_id': eid, 'settings': {key: new}})
    json.dump(ops, open(f'ops/{pid}.json', 'w'), indent=1)
    print(pid, page['slug'], len(ops), 'ops')
print('ALL OK' if ok else 'PROBLEMS')
