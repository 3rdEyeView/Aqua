# fix_template.py <id...>: ensure pages use elementor_canvas (REST); prints before/after
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']; H = {'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0', 'Content-Type': 'application/json'}
for pid in sys.argv[1:]:
    u = f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit&_fields=id,template'
    t = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H)))['template']
    if t != 'elementor_canvas':
        t2 = json.load(urllib.request.urlopen(urllib.request.Request(u, data=b'{"template":"elementor_canvas"}', method='POST', headers=H)))['template']
        print(pid, repr(t), '->', t2)
    else: print(pid, 'ok', t)
