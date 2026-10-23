# Compares each page's staged Elementor autosave with the live page:
# reports every element whose settings/styles differ, and any added/removed elements.
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})))
def index(els, out, parent=None):
    for i, e in enumerate(els):
        out[e['id']] = (e, parent, i); index(e.get('elements', []), out, e['id'])
    return out
for pid in map(int, sys.argv[1:]):
    live = json.loads(get(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit')['meta']['_elementor_data'])
    auto = get(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}/autosaves?context=edit')
    staged = json.loads(auto[0]['meta']['_elementor_data'])
    a, b = index(live, {}), index(staged, {})
    strip = lambda e: {k: v for k, v in e.items() if k != 'elements'}
    changed = [k for k in a if k in b and strip(a[k][0]) != strip(b[k][0])]
    print(pid, 'changed', len(changed), 'added', [k for k in b if k not in a], 'removed', [k for k in a if k not in b])
    for k in changed:
        ka = {s for s in a[k][0]['settings'] if a[k][0]['settings'][s] != b[k][0]['settings'].get(s)}
        other = [x for x in strip(a[k][0]) if x != 'settings' and a[k][0][x] != b[k][0].get(x)]
        print('   ', k, sorted(ka), other or '')
