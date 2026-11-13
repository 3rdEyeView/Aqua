"""Comer's Landscaping concept. Inlines fonts and assets from src.html into one self-contained file
(comers-landscaping-demo.html) that opens offline and makes no network requests."""
import base64, mimetypes, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda *p: open(os.path.join(HERE, *p), encoding="utf8").read()
def uri(rel):
    mime = {".woff2": "font/woff2", ".mp4": "video/mp4"}.get(os.path.splitext(rel)[1]) or mimetypes.guess_type(rel)[0]
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(HERE, rel), "rb").read()).decode()
s = rd("src.html")
css = re.sub(r"url\((fonts/[^)]+)\)", lambda m: f"url({uri(m.group(1))})", rd("fonts", "fonts.css"))
s = s.replace('<link rel="stylesheet" href="fonts/fonts.css">', "<style>" + css + "</style>")
cache = {}
s = re.sub(r'"(assets/[^"]+)"', lambda m: '"' + cache.setdefault(m.group(1), uri(m.group(1))) + '"', s)
assert '"assets/' not in s and "url(fonts/" not in s
out = os.path.join(HERE, "comers-landscaping-demo.html")
open(out, "w", encoding="utf8").write(s)
print(out, round(os.path.getsize(out) / 1e6, 2), "MB", len(cache), "assets")
