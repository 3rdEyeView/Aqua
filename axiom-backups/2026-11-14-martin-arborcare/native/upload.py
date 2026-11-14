# Uploads the Martin Arborcare demo photos (../site/img/martin-demo-*.jpg) to the Axiom media library via the WordPress
# REST API, same method as the earlier demos. Writes native/media-ids.json and skips files already uploaded.
import json, os, sys, urllib.request
H = {'Authorization': 'Basic ' + os.environ['AXIOM_ELEMENTOR_MCP_AUTH'], 'User-Agent': 'curl/8.5.0'}
here = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(here, '..', 'site', 'img')
out = os.path.join(here, 'media-ids.json'); ids = json.load(open(out)) if os.path.exists(out) else {}
ALT = json.load(open(os.path.join(here, 'alts.json')))
for fn in sys.argv[1:] or sorted(ALT):
    if fn in ids: continue
    r = urllib.request.Request('https://axiomsystems.systems/wp-json/wp/v2/media', data=open(os.path.join(src, fn), 'rb').read(), method='POST',
        headers={**H, 'Content-Type': 'image/jpeg', 'Content-Disposition': f'attachment; filename="{fn}"'})
    m = json.load(urllib.request.urlopen(r, timeout=300))
    r2 = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/media/{m["id"]}', method='POST',
        data=json.dumps({'title': 'Martin Arborcare demo – ' + fn[12:-4], 'alt_text': ALT[fn]}).encode(), headers={**H, 'Content-Type': 'application/json'})
    m2 = json.load(urllib.request.urlopen(r2, timeout=120)); md = m2.get('media_details', {})
    ids[fn] = {'id': m2['id'], 'url': m2['source_url'], 'w': md.get('width'), 'h': md.get('height'), 'sizes': sorted(md.get('sizes', {}))}
    print(fn, ids[fn]['id'], ids[fn]['w'], ids[fn]['h'], flush=True); json.dump(ids, open(out, 'w'), indent=1)
