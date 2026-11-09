import json, subprocess, sys, urllib.parse, time
UA = 'AxiomSystemsDemoBuild/1.0 (https://axiomsystems.systems/)'
res = []
for q in sys.argv[1:]:
    u = 'https://api.openverse.org/v1/images/?' + urllib.parse.urlencode({'q': q, 'license': 'cc0,by', 'page_size': 20})
    d = json.loads(subprocess.run(['curl', '-sS', '-A', UA, u], capture_output=True, text=True).stdout)
    for r in d.get('results', []):
        res.append({'q': q, 'id': r['id'], 'title': r.get('title'), 'creator': r.get('creator'), 'lic': f"{r['license']} {r.get('license_version') or ''}".strip(),
                    'url': r['url'], 'thumb': r.get('thumbnail'), 'w': r.get('width'), 'h': r.get('height'), 'landing': r.get('foreign_landing_url'), 'lic_url': r.get('license_url')})
    time.sleep(2)
seen = set(); res = [r for r in res if not (r['url'] in seen or seen.add(r['url']))]
json.dump(res, open('ov.json', 'w'), indent=1)
for i, r in enumerate(res): print(i, r['lic'].ljust(8), f"{r['w']}x{r['h']}".ljust(10), (r['title'] or '')[:60], '|', (r['creator'] or '')[:20], r['url'].split('/')[2])
