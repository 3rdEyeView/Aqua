# ability.py <name> '<json input>' : run a WordPress Ability over REST (GET for readonly, POST otherwise via --post)
import json, os, sys, urllib.request, urllib.parse
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']; name, inp = sys.argv[1], json.loads(sys.argv[2])
base = 'https://axiomsystems.systems/wp-json/wp-abilities/v1/abilities/' + name + '/run'
h = {'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0', 'Content-Type': 'application/json'}
if '--post' in sys.argv:
    req = urllib.request.Request(base, data=json.dumps({'input': inp}).encode(), headers=h, method='POST')
else:
    req = urllib.request.Request(base + '?' + urllib.parse.urlencode({f'input[{k}]': v for k, v in inp.items()}), headers=h)
try: print(json.dumps(json.load(urllib.request.urlopen(req)), indent=1))
except urllib.error.HTTPError as e: print(e.code, e.read().decode()[:800]); sys.exit(1)
