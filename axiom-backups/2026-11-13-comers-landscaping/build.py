"""Comer's Landscaping concept. Inlines fonts and assets from src.html into ONE self-contained file
(comers-landscaping-demo.html) that opens offline and makes no network requests.
Each image is embedded once (window.__A map) and every <img>/<source> that uses it is filled from that map at load,
so a photo shown in the services, gallery and lightbox costs its bytes only once."""
import base64, json, mimetypes, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda *p: open(os.path.join(HERE, *p), encoding="utf8").read()
def uri(rel):
    mime = {".woff2": "font/woff2", ".mp4": "video/mp4"}.get(os.path.splitext(rel)[1]) or mimetypes.guess_type(rel)[0]
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(HERE, rel), "rb").read()).decode()
s = rd("src.html")
css = re.sub(r"url\((fonts/[^)]+)\)", lambda m: f"url({uri(m.group(1))})", rd("fonts", "fonts.css"))
s = s.replace('<link rel="stylesheet" href="fonts/fonts.css">', "<style>" + css + "</style>")
PIX = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
used = []
def note(p):
    if p not in used: used.append(p)
    return p
# <img src="assets/x"> -> placeholder pixel + data-a ; <source srcset="assets/x"> -> data-a ; data-src stays a path (lightbox reads the map)
s = re.sub(r'(?<![-\w])src="(assets/[^"]+)"', lambda m: f'src="{PIX}" data-a="{note(m.group(1))}"', s)
s = re.sub(r'(?<![-\w])srcset="(assets/[^"]+)"', lambda m: f'data-a="{note(m.group(1))}"', s)
for m in re.finditer(r'data-src="(assets/[^"]+)"', s): note(m.group(1))
assert not re.search(r'(?<![-\w])(?:src|srcset|href)="assets/', s) and "url(fonts/" not in s
amap = {p: uri(p) for p in used}
boot = ('<script>window.__A=' + json.dumps(amap, separators=(",", ":")) + ';'
        '(function(){var A=window.__A;[].forEach.call(document.querySelectorAll("[data-a]"),function(e){var u=A[e.getAttribute("data-a")];'
        'if(!u)return;if(e.tagName==="SOURCE")e.srcset=u;else e.src=u;});})();</script>\n')
i = s.index("<script>\n(function(){")
s = s[:i] + boot + s[i:]
out = os.path.join(HERE, "comers-landscaping-demo.html")
open(out, "w", encoding="utf8").write(s)
print(out, round(os.path.getsize(out) / 1e6, 2), "MB,", len(amap), "unique assets")
