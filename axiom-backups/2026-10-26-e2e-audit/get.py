# GET-only helper for the live site's authenticated REST API: get.py <path> [out.json]
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
r = json.load(urllib.request.urlopen(urllib.request.Request('https://axiomsystems.systems/wp-json/' + sys.argv[1].lstrip('/'),
    headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})))
if len(sys.argv) > 2: json.dump(r, open(sys.argv[2], 'w'), indent=1)
else: print(json.dumps(r, indent=1))
