# crawl.py <out.json> [url ...]: status, redirect hops and SEO head data for each URL (no cache: unique query arg)
import json, re, sys, html, urllib.request, urllib.error, random
from html.parser import HTMLParser
UA = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NoRedir)
def fetch(u):
    try:
        r = op.open(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=30)
        return r.status, dict(r.headers), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode('utf-8', 'replace')
class P(HTMLParser):
    def __init__(s): super().__init__(); s.h=[]; s.cur=None; s.links=[]; s.imgs=[]; s.ld=[]; s.inld=False; s.meta={}; s.canon=None; s.title=''; s.intitle=False
    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ('h1','h2','h3'): s.cur=[t,'']
        if t=='a' and a.get('href'): s.links.append(a['href'])
        if t=='img': s.imgs.append((a.get('src') or a.get('data-src'), a.get('alt')))
        if t=='script' and a.get('type')=='application/ld+json': s.inld=True; s.ld.append('')
        if t=='meta': k=a.get('name') or a.get('property'); 
        if t=='meta' and (a.get('name') or a.get('property')): s.meta[a.get('name') or a.get('property')]=a.get('content')
        if t=='link' and a.get('rel')=='canonical': s.canon=a.get('href')
        if t=='title': s.intitle=True
    def handle_endtag(s, t):
        if s.cur and t==s.cur[0]: s.h.append((s.cur[0], ' '.join(s.cur[1].split()))); s.cur=None
        if t=='script': s.inld=False
        if t=='title': s.intitle=False
    def handle_data(s, d):
        if s.cur: s.cur[1]+=d
        if s.inld: s.ld[-1]+=d
        if s.intitle: s.title+=d
out = {}
for url in sys.argv[2:]:
    hops=[]; u=url
    for _ in range(6):
        sep = '&' if '?' in u else '?'
        code, hd, body = fetch(u)
        hops.append([u, code, hd.get('Location') or hd.get('location')])
        if code in (301,302,307,308) and hops[-1][2]: u = urllib.parse.urljoin(u, hops[-1][2]); continue
        break
    p=P(); p.feed(body)
    types=[]
    for blob in p.ld:
        try:
            j=json.loads(blob); g=j.get('@graph',[j]) if isinstance(j,dict) else j
            types += [x.get('@type') for x in g]
        except Exception as e: types.append('PARSE-ERR')
    out[url] = dict(hops=hops, final=u, status=code, x_robots=hd.get('X-Robots-Tag') or hd.get('x-robots-tag'),
        title=html.unescape(p.title.strip()), desc=p.meta.get('description'), robots=p.meta.get('robots'), canonical=p.canon,
        og_title=p.meta.get('og:title'), og_desc=p.meta.get('og:description'), og_image=p.meta.get('og:image'), og_url=p.meta.get('og:url'),
        headings=p.h, h1=[t for h,t in p.h if h=='h1'], ld_types=types, ld=p.ld,
        links=sorted(set(p.links)), imgs=p.imgs, body_len=len(body),
        body_text_sample=' '.join(re.sub(r'<[^>]+>',' ',re.sub(r'(?s)<(script|style).*?</\1>','',body)).split())[:4000])
json.dump(out, open(sys.argv[1],'w'), indent=1)
for k,v in out.items():
    print(f"{v['status']} {k} -> {v['final'] if v['final']!=k else ''} | robots={v['robots']} xr={v['x_robots']} | canon={v['canonical']}\n   T: {v['title']}\n   D: {v['desc']}\n   H1: {v['h1']} | LD: {v['ld_types']}")
