import json, os, urllib.request, urllib.parse
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0'})))
B='https://axiomsystems.systems/wp-json/wp/v2/'
for t in ['pages','posts','product','jetpack-form','elementor_library']:
    for q in ['149','199','647','Lead Response','Follow-Up Automation','lead-response','Save $48']:
        try:
            r = get(B+t+'?context=edit&status=publish,draft,private,pending&per_page=50&search='+urllib.parse.quote(q))
            hits=[(x['id'],x.get('slug'),x.get('status')) for x in r]
            if hits: print(t, repr(q), hits)
        except Exception as e:
            print(t, q, 'ERR', str(e)[:80]); break
