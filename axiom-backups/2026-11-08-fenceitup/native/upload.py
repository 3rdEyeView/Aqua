# Uploads the Fence It Up demo photos (../site/) to the Axiom media library via the WordPress REST API, the same
# method as the Branham / Advanced Fence / Arroyo's demos. Writes native/media-ids.json and skips files already uploaded.
import json, os, sys, urllib.request
H = {'Authorization': 'Basic ' + os.environ['AXIOM_ELEMENTOR_MCP_AUTH'], 'User-Agent': 'curl/8.5.0'}
here = os.path.dirname(os.path.abspath(__file__)); img = os.path.join(here, '..', 'site')
out = os.path.join(here, 'media-ids.json')
ids = json.load(open(out)) if os.path.exists(out) else {}
ALT = json.load(open(os.path.join(here, 'alts.json')))
for fn in sys.argv[1:] or sorted(os.listdir(img)):
    if fn in ids or not fn.endswith('.jpg'): continue
    data = open(os.path.join(img, fn), 'rb').read()
    r = urllib.request.Request('https://axiomsystems.systems/wp-json/wp/v2/media', data=data, method='POST',
        headers={**H, 'Content-Type': 'image/jpeg', 'Content-Disposition': f'attachment; filename="{fn}"'})
    m = json.load(urllib.request.urlopen(r, timeout=300))
    body = {'title': 'Fence It Up demo – ' + fn[len('fenceitup-demo-'):-4], 'alt_text': ALT[fn]}
    r2 = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/media/{m["id"]}', method='POST',
        data=json.dumps(body).encode(), headers={**H, 'Content-Type': 'application/json'})
    m2 = json.load(urllib.request.urlopen(r2)); md = m2.get('media_details', {})
    ids[fn] = {'id': m2['id'], 'url': m2['source_url'], 'w': md.get('width'), 'h': md.get('height'),
               'sizes': sorted(md.get('sizes', {}))}
    print(fn, ids[fn]); json.dump(ids, open(out, 'w'), indent=1)
