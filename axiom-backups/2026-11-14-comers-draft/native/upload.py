# Uploads the Comer's demo media (logo, hero stills, job photos from ../2026-11-13-comers-landscaping/assets/) to the
# Axiom media library via the WordPress REST API, the same method as the earlier demos. Writes native/media-ids.json
# and skips files already uploaded. Published name: comers-demo-<asset name>.
import json, os, sys, urllib.request
H = {'Authorization': 'Basic ' + os.environ['AXIOM_ELEMENTOR_MCP_AUTH'], 'User-Agent': 'curl/8.5.0'}
here = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(here, '..', '..', '2026-11-13-comers-landscaping', 'assets')
out = os.path.join(here, 'media-ids.json')
ids = json.load(open(out)) if os.path.exists(out) else {}
ALT = json.load(open(os.path.join(here, 'alts.json')))
for fn in sys.argv[1:] or sorted(ALT):
    if fn in ids: continue
    pub = 'comers-demo-' + fn
    ctype = 'image/png' if fn.endswith('.png') else 'image/jpeg'
    data = open(os.path.join(src, fn), 'rb').read()
    r = urllib.request.Request('https://axiomsystems.systems/wp-json/wp/v2/media', data=data, method='POST',
        headers={**H, 'Content-Type': ctype, 'Content-Disposition': f'attachment; filename="{pub}"'})
    m = json.load(urllib.request.urlopen(r, timeout=300))
    body = {'title': "Comer's demo – " + fn.rsplit('.', 1)[0], 'alt_text': ALT[fn]}
    r2 = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/media/{m["id"]}', method='POST',
        data=json.dumps(body).encode(), headers={**H, 'Content-Type': 'application/json'})
    m2 = json.load(urllib.request.urlopen(r2, timeout=120)); md = m2.get('media_details', {})
    ids[fn] = {'id': m2['id'], 'url': m2['source_url'], 'w': md.get('width'), 'h': md.get('height'),
               'sizes': sorted(md.get('sizes', {}))}
    print(fn, ids[fn]['id'], ids[fn]['w'], ids[fn]['h'], flush=True); json.dump(ids, open(out, 'w'), indent=1)
