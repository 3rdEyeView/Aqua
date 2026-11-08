# Sets page 1632's slug via the WordPress REST API (same auth as upload.py)
import json, os, urllib.request
H = {'Authorization': 'Basic ' + os.environ['AXIOM_ELEMENTOR_MCP_AUTH'], 'User-Agent': 'curl/8.5.0', 'Content-Type': 'application/json'}
r = urllib.request.Request('https://axiomsystems.systems/wp-json/wp/v2/pages/1632', method='POST', headers=H,
                           data=json.dumps({'slug': 'advanced-fence-demo'}).encode())
p = json.load(urllib.request.urlopen(r)); print(p['id'], p['status'], p['slug'], p['link'], p['template'])
