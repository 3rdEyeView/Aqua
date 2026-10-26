import json,sys,re
# Dump every text-bearing setting from an Elementor page in document order.
def walk(els, depth, out, sec):
    for el in els:
        s=el.get('settings',{})
        if el.get('elType')!='widget' and depth==0:
            sec=(s.get('_cssid') or {}).get('value') if isinstance(s.get('_cssid'),dict) else None
            sec=sec or el['id']
        for k,v in s.items():
            if isinstance(v,dict) and v.get('$$type') in ('escaped-html','html','html-v2','html-v3') and k not in ('tag','_cssid','link','classes','attributes'):
                val=v.get('value')
                if isinstance(val,dict): val=val.get('content') or json.dumps(val)
                if isinstance(val,str) and re.search('[A-Za-z]{2}',val): out.append((sec,el['id'],el.get('widgetType') or el.get('elType'),k,val))
            elif isinstance(v,dict) and v.get('$$type')=='link':
                href=((v.get('value') or {}).get('destination') or {}).get('value')
                out.append((sec,el['id'],el.get('widgetType'),'href',str(href)))
        walk(el.get('elements',[]),depth+1,out,sec)
for pid in sys.argv[1:]:
    d=json.load(open(f'before/pages/{pid}.json'))
    data=json.loads(d['meta']['_elementor_data'])
    out=[];walk(data,0,out,None)
    with open(f'audit/{pid}-{d["slug"]}.txt','w') as f:
        for r in out: f.write(' | '.join(map(str,r))+'\n')
    print(pid,d['slug'],len(out))
