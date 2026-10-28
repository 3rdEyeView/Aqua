# usage: build_ops.py <pid> <spec_module>  -> ops/<pid>-p1.json
# Refuses if the live page changed since the backup or an element id is unknown.
import json, os, sys, importlib, urllib.request
KEY = {'e-paragraph': 'paragraph', 'e-heading': 'title', 'e-button': 'text'}
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
pid, mod = int(sys.argv[1]), importlib.import_module(sys.argv[2])
live = json.load(urllib.request.urlopen(urllib.request.Request(
    f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit',
    headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})))
backup = json.load(open(f'before/pages/{pid}.json'))
assert live['meta']['_elementor_data'] == backup['meta']['_elementor_data'], 'LIVE CHANGED SINCE BACKUP'
idx = {}
def walk(els):
    for e in els: idx[e['id']] = e; walk(e.get('elements', []))
walk(json.loads(live['meta']['_elementor_data']))
ops = [{'action': 'duplicate', 'element_id': e} for e in getattr(mod, 'DUPLICATE', [])]
for eid, new in mod.SPEC.items():
    el = idx[eid]; key = KEY[el['widgetType']]
    cur = el['settings'][key]['value']
    cur = cur.get('content') if isinstance(cur, dict) else cur
    if cur == new: print('  unchanged', eid); continue
    print(f'  {eid}: {str(cur)[:60]!r} -> {new[:60]!r}')
    ops.append({'action': 'update', 'element_id': eid, 'settings': {key: new}})
for e in getattr(mod, 'DELETE', []):
    assert e in idx; ops.append({'action': 'delete', 'element_id': e})
ops += getattr(mod, 'EXTRA', [])
os.makedirs('ops', exist_ok=True)
json.dump(ops, open(f'ops/{pid}-p1.json', 'w'), indent=1)
print(pid, len(ops), 'ops')
