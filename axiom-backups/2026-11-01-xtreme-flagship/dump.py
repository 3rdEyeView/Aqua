import json, sys
d = json.load(open(sys.argv[1])); data = json.loads(d['meta']['_elementor_data'])
idx={}
def w(els):
    for e in els: idx[e['id']]=e; w(e.get('elements',[]))
w(data)
def val(v):
    v = v.get('value') if isinstance(v, dict) else v
    return v.get('content') if isinstance(v, dict) else v
for i in sys.argv[2:]:
    s = idx[i]['settings']
    for k in ('title','paragraph','text'):
        if k in s: print(i, idx[i]['widgetType'], '|', val(s[k]))
    if 'image' in s: print(i, 'IMG', json.dumps(s['image']))
    if 'link' in s: print(i, 'LINK', json.dumps(s['link']))
