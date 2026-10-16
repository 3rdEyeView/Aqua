#!/usr/bin/env python3
"""Build the temporary CDN 'bridge' CSS: exact Elementor-generated rules for selected style classes,
read from origin (uncached) Elementor CSS files, in Elementor's own order (global class rule first,
then local rules, desktop -> tablet -> mobile).
Usage: tools/bridge_css.py <page_id> <global_class_label|-> <local_class> [<local_class> ...]
Prints CSS to stdout. Read-only."""
import re, sys, urllib.request
pid, glob_label, locs = sys.argv[1], sys.argv[2], sys.argv[3:]
UA = {"User-Agent": "Mozilla/5.0 Chrome/128.0 XtremeAudit-Claude/1.0"}
BP = {"desktop": None, "tablet": "(max-width:1024px)", "mobile": "(max-width:767px)"}
def fetch(kind, bp):
    u = f"https://xtremestpete.com/wp-content/uploads/elementor/css/{kind}-{pid}-frontend-{bp}.css"
    try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode()
    except Exception: return ""
def rules(css, cls):
    # top-level rules and rules inside @media blocks whose selector mentions the class
    out = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css):
        sel = m.group(1).strip().lstrip('}').strip()
        if re.search(r'\.' + re.escape(cls) + r'(?![\w-])', sel) and not sel.startswith('@'):
            body = m.group(2).replace('\\n', '').strip()
            out.append(f"{sel}{{{body}}}")
    return out
for bp, mq in BP.items():
    chunk = []
    if glob_label != "-":
        g = fetch("global", bp); chunk += rules(g, glob_label)
    l = fetch("local", bp)
    for c in locs: chunk += rules(l, c)
    if not chunk: continue
    body = "\n".join(dict.fromkeys(chunk))
    print(body if not mq else f"@media {mq}{{\n{body}\n}}")
