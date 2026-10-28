# Writes ops/<pid>.json: price swap for every text containing $297/$597, plus EDITS (substring replace, asserted).
import json, os, sys, urllib.request
from spec import price, EDITS, KEY
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
os.makedirs('ops', exist_ok=True)
for pid in [952, 1068, 1074, 1085, 1095, 1013, 1031]:
    live = json.load(urllib.request.urlopen(urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit',
        headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})))
    assert live['meta']['_elementor_data'] == json.load(open(f'before/pages/{pid}.json'))['meta']['_elementor_data'], 'LIVE CHANGED'
    idx = {}
    def walk(els):
        for e in els: idx[e['id']] = e; walk(e.get('elements', []))
    walk(json.loads(live['meta']['_elementor_data']))
    ops, edits = [], dict(EDITS.get(pid, {}))
    for eid, e in idx.items():
        k = KEY.get(e.get('widgetType'))
        if not k or k not in e['settings']: continue
        old = e['settings'][k]['value']; new = price(old)
        if eid in edits:
            o, n = edits.pop(eid); assert o in new, (pid, eid, new); new = new.replace(o, n)
        if new != old:
            ops.append({'action': 'update', 'element_id': eid, 'settings': {k: new}}); print(pid, eid, '|', new[:110])
    assert not edits, edits
    json.dump(ops, open(f'ops/{pid}.json', 'w'), indent=1, ensure_ascii=False)
