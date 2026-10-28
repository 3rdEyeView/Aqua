# get <id> <file> <out>  : saves a snippet file's current content
# diff <id> <file> <local>: reports whether the live file equals a local file
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})))
cmd, sid, name, path = sys.argv[1:5]
r = get(f'https://axiomsystems.systems/wp-json/angie/v1/snippets/{sid}/files?include_content=true')
files = r.get('files', r) if isinstance(r, dict) else r
content = next((f.get('content') for f in files if f.get('name') == name), None)
if content is None: print(json.dumps(r)[:500]); sys.exit(1)
if cmd == 'get': open(path, 'w').write(content); print('saved', len(content))
else: print('IDENTICAL' if content == open(path).read() else 'DIFFERENT', len(content))
