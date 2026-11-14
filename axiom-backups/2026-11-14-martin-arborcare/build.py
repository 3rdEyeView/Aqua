"""Inline site/index.html + fonts + images into one self-contained file: martin-arborcare-demo.html (offline, no network)."""
import base64, mimetypes, os, re
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
rd = lambda p: open(os.path.join(H, p), encoding='utf8').read()
def uri(rel):
    mime = {'.woff2': 'font/woff2'}.get(os.path.splitext(rel)[1]) or mimetypes.guess_type(rel)[0]
    return f'data:{mime};base64,' + base64.b64encode(open(os.path.join(H, rel), 'rb').read()).decode()
css = re.sub(r'url\((fonts/[^)]+)\)', lambda m: f'url({uri(m.group(1))})', rd('fonts/fonts.css'))
html = rd('index.html').replace('<link rel="stylesheet" href="fonts/fonts.css">', '<style>' + css + '</style>')
cache = {}
html = re.sub(r'"(img/[^"]+)"', lambda m: '"' + cache.setdefault(m.group(1), uri(m.group(1))) + '"', html)
assert '"img/' not in html and 'url(fonts/' not in html
out = os.path.join(os.path.dirname(H), 'martin-arborcare-demo.html'); open(out, 'w', encoding='utf8').write(html)
print(out, round(os.path.getsize(out) / 1e6, 2), 'MB,', len(cache), 'images')
