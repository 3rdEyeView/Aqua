# Admin POST to axiom/v1/crm-sync: post.py '<json body>' <out.json>
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
req = urllib.request.Request('https://axiomsystems.systems/wp-json/axiom/v1/crm-sync', data=sys.argv[1].encode(), method='POST',
    headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0', 'Content-Type': 'application/json'})
try:
    r = json.load(urllib.request.urlopen(req))
except urllib.error.HTTPError as e:
    r = {'http_error': e.code, 'body': e.read().decode()[:300]}
json.dump(r, open(sys.argv[2], 'w'), indent=1); print(json.dumps(r, indent=1)[:2500])
