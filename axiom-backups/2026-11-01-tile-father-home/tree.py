# prints element tree with text/links/images for a saved page export
import json, sys
d = json.load(open(sys.argv[1]))
data = json.loads(d['meta']['_elementor_data'])
def val(v):
    v = v.get('value') if isinstance(v, dict) else v
    return v.get('content') if isinstance(v, dict) else v
def walk(els, depth):
    for e in els:
        s = e.get('settings', {})
        w = e.get('widgetType') or e['elType']
        t = ''
        for k in ('title','paragraph','text','html','editor'):
            if k in s: t = str(val(s[k]))
        extra = ''
        if 'link' in s:
            try: extra += ' LINK=' + json.dumps(s['link'])[:160]
            except: pass
        if 'image' in s: extra += ' IMG=' + json.dumps(s['image'])[:200]
        cls = s.get('classes', {})
        print('  '*depth + e['id'], w, repr(t[:110]), extra, json.dumps(cls)[:80] if cls else '')
        walk(e.get('elements', []), depth+1)
walk(data, 0)
