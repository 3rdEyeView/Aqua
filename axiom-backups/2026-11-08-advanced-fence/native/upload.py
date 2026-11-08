# Uploads the Advanced Fence demo JPGs to the Axiom media library via the WordPress REST API
# (same method as ../2026-11-01-xtreme-flagship/upload.py); writes native/media-ids.json. Skips files already uploaded.
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
H = {'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'}
here = os.path.dirname(os.path.abspath(__file__)); img = os.path.join(here, '..', 'img')
out = os.path.join(here, 'media-ids.json')
ids = json.load(open(out)) if os.path.exists(out) else {}
names = sys.argv[1:] or sorted(os.listdir(img))
for fn in names:
    if fn in ids: continue
    data = open(os.path.join(img, fn), 'rb').read()
    r = urllib.request.Request('https://axiomsystems.systems/wp-json/wp/v2/media', data=data, method='POST',
        headers={**H, 'Content-Type': 'image/jpeg', 'Content-Disposition': f'attachment; filename="{fn}"'})
    m = json.load(urllib.request.urlopen(r))
    title = 'Advanced Fence demo – ' + fn[len('advanced-demo-'):-4]
    alt = 'Advanced Fence Service logo' if 'logo' in fn else 'Fence by Advanced Fence Service'
    r2 = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/media/{m["id"]}', method='POST',
        data=json.dumps({'title': title, 'alt_text': alt}).encode(), headers={**H, 'Content-Type': 'application/json'})
    m2 = json.load(urllib.request.urlopen(r2))
    ids[fn] = {'id': m2['id'], 'url': m2['source_url'], 'w': m2['media_details'].get('width'), 'h': m2['media_details'].get('height')}
    print(fn, ids[fn]); json.dump(ids, open(out, 'w'), indent=1)
