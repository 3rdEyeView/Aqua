# Applies the copy_spec replacements to each page's post_content (the plain HTML
# copy Elementor keeps for excerpts/Yoast), and adds the new FAQ item text.
import json, os, sys, urllib.request
from copy_spec import SPEC, NEW_FAQ
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
def call(pid, body=None):
    req = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit',
        data=json.dumps(body).encode() if body else None, method='POST' if body else 'GET',
        headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0', 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req))
dry = '--write' not in sys.argv
for pid, edits in SPEC.items():
    page = call(pid); c = page['content']['raw']; orig = c; missing = []
    for eid, (old, new) in edits.items():
        for o, n in ((old, new), (old.replace('<br>', ' '), new.replace('<br>', ' ')), (old.upper().replace('&AMP;', '&amp;'), new.upper().replace('&AMP;', '&amp;')),
                     (old.replace("'", '&#8217;'), new.replace("'", '&#8217;'))):
            if f'>{o}<' in c:
                c = c.replace(f'>{o}<', f'>{n}<', 1); break
        else:
            missing.append(eid)
    if pid == NEW_FAQ['page']:
        ans = SPEC[1085]['6317b72a'][1]
        anchor = f'<p>{ans}</p>'
        if anchor in c:
            c = c.replace(anchor, anchor + f"\n<h3>{NEW_FAQ['question']}</h3>\n<p>{NEW_FAQ['answer']}</p>", 1)
        else:
            missing.append('new-faq')
    print(pid, 'replaced', len(edits) - len([m for m in missing if m != 'new-faq']), 'of', len(edits), 'missing', missing, 'GoHighLevel left:', 'GoHighLevel' in c)
    if not dry and c != orig:
        r = call(pid, {'content': c})
        print('   written; elementor data unchanged:', r['meta']['_elementor_data'] == page['meta']['_elementor_data'], r['template'], r['status'])
