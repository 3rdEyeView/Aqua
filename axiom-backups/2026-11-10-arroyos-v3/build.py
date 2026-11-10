"""Arroyo V3 sales demo. Assembles src.html from the V2 page (../2026-11-10-arroyos-v2/src.html) plus parts/, then inlines
every asset into one self-contained file: arroyo-v3-sales-demo.html (opens offline, makes no network requests)."""
import base64, mimetypes, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda *p: open(os.path.join(HERE, *p), encoding="utf8").read()
s = rd("..", "2026-11-10-arroyos-v2", "src.html")
def sub(pattern, repl, flags=re.S):
    global s
    s, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags); assert n == 1, pattern
sub(r"<title>.*?</title>", "<title>Arroyo’s Lawn Care — V3 sales demo (not live)</title>")
sub(r"</style>\n</head>", rd("parts", "v3.css") + "</style>\n</head>")
sub(r"<body>\n<div class=\"ribbon\".*?</div>\n",
    '<body data-view="home">\n<div class="pbar" role="toolbar" aria-label="Presenter"><span>Arroyo V3 demo · not published</span>'
    '<button type="button" data-view="home" aria-pressed="true">Homeowner page</button>'
    '<button type="button" data-view="lead" aria-pressed="false">See What Happens to a Lead</button></div>\n<div class="view-home">\n')
sub(r"<section class=\"hero\".*?</section>\n", rd("parts", "reveal.html"))
sub(r"(?<=</nav>\n)\n<script>", "</div>\n\n" + rd("parts", "lead.html") + "\n<script>")
for a, b in [("hero=document.querySelector('.hero'), ", ""), (" mbar.classList.toggle('is-on', y>hero.offsetHeight*0.6);", ""),
             ("document.querySelector('.hero video')", "document.querySelector('.rv video')"), ("V2 preview, not published", "V3 sales demo, not published")]:
    assert a in s, a; s = s.replace(a, b)
sub(r"</script>\n</body>", "</script>\n<script>\n" + rd("parts", "v3.js") + "</script>\n</body>")
open(os.path.join(HERE, "src.html"), "w", encoding="utf8").write(s)

def uri(rel):
    mime = {".woff2": "font/woff2", ".webp": "image/webp"}.get(os.path.splitext(rel)[1]) or mimetypes.guess_type(rel)[0]
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(HERE, rel), "rb").read()).decode()
css = re.sub(r"url\((fonts/[^)]+)\)", lambda m: f"url({uri(m.group(1))})", rd("fonts", "fonts.css"))
html = s.replace('<link rel="stylesheet" href="fonts/fonts.css">', "<style>" + css + "</style>")
cache = {}
html = re.sub(r'"(assets/[^"]+)"', lambda m: '"' + cache.setdefault(m.group(1), uri(m.group(1))) + '"', html)
assert '"assets/' not in html and "url(fonts/" not in html
out = os.path.join(HERE, "arroyo-v3-sales-demo.html")
open(out, "w", encoding="utf8").write(html)
print(out, round(os.path.getsize(out) / 1e6, 2), "MB")
