"""Inline every asset of src.html into one self-contained file: arroyo-v2-preview.html (opens offline, no server)."""
import base64, mimetypes, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
def uri(rel):
    mime = {".woff2": "font/woff2", ".webp": "image/webp"}.get(os.path.splitext(rel)[1]) or mimetypes.guess_type(rel)[0]
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(HERE, rel), "rb").read()).decode()
html = open(os.path.join(HERE, "src.html"), encoding="utf8").read()
css = open(os.path.join(HERE, "fonts", "fonts.css"), encoding="utf8").read()
css = re.sub(r"url\((fonts/[^)]+)\)", lambda m: f"url({uri(m.group(1))})", css)
html = html.replace('<link rel="stylesheet" href="fonts/fonts.css">', "<style>" + css + "</style>")
cache = {}
html = re.sub(r'"(assets/[^"]+)"', lambda m: '"' + cache.setdefault(m.group(1), uri(m.group(1))) + '"', html)
assert "assets/" not in html and "fonts/" not in html
out = os.path.join(HERE, "arroyo-v2-preview.html")
open(out, "w", encoding="utf8").write(html)
print(out, round(os.path.getsize(out) / 1e6, 2), "MB")
