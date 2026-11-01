# Saves full REST exports (context=edit) of the given pages into before/pages/.
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})))
out = sys.argv[1]
for pid in sys.argv[2:]:
    d = get(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit')
    json.dump(d, open(f'{out}/{pid}.json', 'w'), indent=1)
    print(pid, d['slug'], d['status'], d['modified_gmt'], len(d['meta'].get('_elementor_data') or ''))
