# Rebuilds post_content (plain HTML copy read by search/excerpts/Yoast) from the published Elementor data and
# sets the featured (share) image. Elementor data is never sent; the script checks it is unchanged afterwards.
# usage: sync_content.py [--write] pid...
import json, os, sys, urllib.request
auth = os.environ['AXIOM_ELEMENTOR_MCP_AUTH']
MEDIA = int(open('og/media-id.txt').read())
def call(pid, body=None):
    req = urllib.request.Request(f'https://axiomsystems.systems/wp-json/wp/v2/pages/{pid}?context=edit',
        data=json.dumps(body).encode() if body else None, method='POST' if body else 'GET',
        headers={'Authorization': 'Basic ' + auth, 'User-Agent': 'curl/8.5.0', 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req))
def val(v):
    v = v.get('value') if isinstance(v, dict) else v
    return v.get('content') if isinstance(v, dict) else v
def build(els, out):
    for e in els:
        s, w = e.get('settings', {}), e.get('widgetType')
        if w == 'e-heading':
            tag = val(s.get('tag')) or 'h2'
            out.append(f'<{tag}>{val(s["title"]).replace("<br>", " ")}</{tag}>')
        elif w == 'e-paragraph':
            t = (val(s.get('paragraph')) or '').strip()
            if t and t not in ('✓', '—', '&nbsp;', '↓') and 'AXIOM_GS_FORM_SLOT' not in t:
                out.append(f'<p>{t.replace("<br>", " ")}</p>')
            elif 'AXIOM_GS_FORM_SLOT' in t:
                out.append(f'<p>{t}</p>')
        elif w == 'e-button':
            dest = ((s.get('link') or {}).get('value') or {}).get('destination')
            href = dest.get('value') if isinstance(dest, dict) else dest
            out.append(f'<a href="{href or ""}">{val(s.get("text"))}</a>')
        build(e.get('elements', []), out)
    return out
write = '--write' in sys.argv
for pid in [int(a) for a in sys.argv[1:] if a.isdigit()]:
    page = call(pid)
    html = '\n'.join(build(json.loads(page['meta']['_elementor_data']), []))
    os.makedirs('after/content', exist_ok=True); open(f'after/content/{pid}.html', 'w').write(html)
    body = {'content': html}
    if pid != 1413: body['featured_media'] = MEDIA
    print(pid, 'chars', len(page['content']['raw']), '->', len(html), 'featured', page['featured_media'], '->', body.get('featured_media'))
    if write:
        r = call(pid, body)
        print('   written; elementor unchanged:', r['meta']['_elementor_data'] == page['meta']['_elementor_data'], r['template'], r['status'], r['featured_media'])
