"""Polite Commons API client (curl, descriptive UA, backoff on 429)."""
import json, subprocess, time, urllib.parse, sys
UA = 'AxiomSystemsDemoBuild/1.0 (https://axiomsystems.systems/)'
def api(**params):
    u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({**params, 'format': 'json', 'maxlag': 5})
    for i in range(6):
        out = subprocess.run(['curl', '-sS', '-A', UA, u], capture_output=True, text=True).stdout
        if out.startswith('{'): time.sleep(2); return json.loads(out)
        time.sleep(8 * (i + 1))
    raise SystemExit('rate-limited: ' + out[:100])
def subcats(cat): return [m['title'] for m in api(action='query', list='categorymembers', cmtitle=cat, cmtype='subcat', cmlimit=200)['query']['categorymembers']]
def files(cat, n=200):
    r = api(action='query', generator='categorymembers', gcmtitle=cat, gcmtype='file', gcmlimit=min(n, 50), prop='imageinfo', iiprop='url|size|extmetadata', iiurlwidth=360)
    out = []
    for p in (r.get('query', {}).get('pages', {}) or {}).values():
        if 'imageinfo' not in p: continue
        ii = p['imageinfo'][0]; md = ii.get('extmetadata', {})
        out.append({'cat': cat, 'title': p['title'], 'w': ii['width'], 'h': ii['height'], 'lic': md.get('LicenseShortName', {}).get('value', ''),
                    'thumb': ii.get('thumburl'), 'url': ii['url'], 'artist': md.get('Artist', {}).get('value', '')[:300], 'page': ii.get('descriptionurl')})
    return out
if __name__ == '__main__':
    print(subcats(sys.argv[1]))
