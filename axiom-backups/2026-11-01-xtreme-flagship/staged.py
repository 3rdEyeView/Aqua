# Prints the staged (autosave) subtree of an element: id, widget, text.
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})))
pid, root = int(sys.argv[1]), sys.argv[2]
auto = get(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}/autosaves?context=edit')
data = json.loads(auto[0]['meta']['_elementor_data'])
def walk(els, d, on):
    for e in els:
        o = on or e['id'] == root
        if o:
            s = e.get('settings', {}); t = (s.get('paragraph') or s.get('title') or s.get('text') or {}).get('value', '') if isinstance(s.get('paragraph') or s.get('title') or s.get('text'), dict) else ''
            print('  ' * d, e['id'], e.get('widgetType') or e['elType'], str(t)[:70])
        walk(e.get('elements', []), d + 1, o)
walk(data, 0, False)
