# usage: build_ops.py -> ops/952.json, ops/1031.json. Refuses if live page changed since backup or an id is unknown.
import json, os, urllib.request, spec
KEY = {'e-paragraph': 'paragraph', 'e-heading': 'title', 'e-button': 'text'}
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
os.makedirs('ops', exist_ok=True)
for pid, text, other in [(952, spec.HOME_TEXT, spec.HOME_OTHER), (1031, spec.OW_TEXT, spec.OW_OTHER)]:
    live = json.load(urllib.request.urlopen(urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit',
        headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})))
    assert live['meta']['_elementor_data'] == json.load(open(f'before/pages/{pid}.json'))['meta']['_elementor_data'], 'LIVE CHANGED'
    idx = {}
    def walk(els):
        for e in els: idx[e['id']] = e; walk(e.get('elements', []))
    walk(json.loads(live['meta']['_elementor_data']))
    ops = []
    for eid, new in text.items():
        el = idx[eid]; key = KEY[el['widgetType']]
        cur = el['settings'][key]['value']; cur = cur.get('content') if isinstance(cur, dict) else cur
        if cur == new: print('  unchanged', eid); continue
        print(f'  {eid}: {cur[:50]!r} -> {new[:50]!r}')
        ops.append({'action': 'update', 'element_id': eid, 'settings': {key: new}})
    for o in other:
        assert o['element_id'] in idx, o['element_id']
        if o['action'] == 'update':  # merge with a text op on the same element
            prev = next((p for p in ops if p['element_id'] == o['element_id'] and p['action'] == 'update'), None)
            if prev: prev['settings'].update(o.get('settings', {})); prev.update({k: v for k, v in o.items() if k not in ('settings',)}); continue
        ops.append(o)
    json.dump(ops, open(f'ops/{pid}.json', 'w'), indent=1, ensure_ascii=False)
    print(pid, len(ops), 'ops')
