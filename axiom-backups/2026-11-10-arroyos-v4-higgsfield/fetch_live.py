"""Read-only: downloads the stylesheets, the few Elementor scripts and the images the live page (live.html) uses."""
import re, os, json, hashlib, urllib.request, html
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36", "Accept": "*/*"}
s = open("live.html", encoding="utf8").read(); idx = {}
def get(u):
    u = html.unescape(u)
    if u.startswith("//"): u = "https:" + u
    fn = hashlib.md5(u.encode()).hexdigest()[:10] + os.path.splitext(u.split("?")[0])[1]
    p = os.path.join("live-assets", fn)
    if not os.path.exists(p):
        open(p, "wb").write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())
    idx[u] = fn; return fn
css = [u for u in re.findall(r'<link[^>]+rel=.stylesheet.[^>]+href=.([^"\']+)', s) if "axiomsystems.systems" in u]
js = [u for u in re.findall(r'<script[^>]+src=.([^"\']+)', s) if re.search(r"plugins/elementor/|hello-frontend", u)]
imgs = sorted(set(re.findall(r'<img[^>]+src=.([^"\']+)', s)))
for u in css + js + imgs:
    try: print(get(u), os.path.getsize("live-assets/" + idx[html.unescape(u)]), u[-70:])
    except Exception as e: print("FAIL", u, e)
json.dump(idx, open("live-assets/index.json", "w"), indent=1)
