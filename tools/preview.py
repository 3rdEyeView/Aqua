#!/usr/bin/env python3
"""Build a local, faithful preview of an Elementor V4 draft page (read-only).

Why: the Elementor MCP preview-link tool cannot snapshot drafts on this site, and
V4 CSS is only generated when a published page is viewed. This script:
  1. GETs the draft's rendered HTML + _elementor_data via the WP REST API
     (Authorization comes from the XTREME_WP_BASIC_AUTH env var; never printed).
  2. Converts the stored V4 style props to CSS (local styles).
  3. Compiles design/classes.css (global classes) + kit variables.
  4. Injects it all into a snapshot of the live site shell (real header, footer,
     WaveRez loader, tracking) so the page renders like production.

Usage: tools/preview.py <page_id> <out.html> [shell.html]
Nothing is written to WordPress.
"""
import html, json, os, re, sys, urllib.request

BASE = "https://xtremestpete.com"
UA = "XtremeAudit-Claude/1.0 (Mozilla/5.0 Chrome/128.0)"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BP = {"tablet": "(max-width:1024px)", "mobile": "(max-width:767px)"}


def get(path, auth=True):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
    if auth:
        req.add_header("Authorization", "Basic " + os.environ["XTREME_WP_BASIC_AUTH"])
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


# ---------- V4 prop -> CSS ----------
def val(p):
    if p is None:
        return None
    t, v = p.get("$$type"), p.get("value")
    if t == "size":
        if v is None:
            return None
        u, s = v.get("unit"), v.get("size")
        if u == "custom":
            return str(s)
        if u == "auto":
            return "auto"
        return f"{s}{u}"
    if t in ("string", "number", "color", "url"):
        return str(v)
    if t in ("global-color-variable", "global-font-variable"):
        return f"var(--{v})"
    if t == "image-src":
        return (v.get("url") or {}).get("value")
    return None


def box(prop, v, fmt):
    out = []
    for k, sub in v.items():
        s = val(sub)
        if s is not None:
            out.append((fmt(prop, k), s))
    return out


def radius_key(prop, k):
    return {"start-start": "border-start-start-radius", "start-end": "border-start-end-radius",
            "end-start": "border-end-start-radius", "end-end": "border-end-end-radius"}[k]


def background(v):
    out, layers = [], []
    if v.get("color"):
        out.append(("background-color", val(v["color"])))
    for ov in (v.get("background-overlay") or {}).get("value", []):
        t, o = ov["$$type"], ov["value"]
        if t == "background-image-overlay":
            img = o["image"]["value"]["src"]["value"]
            url = (img.get("url") or {}).get("value")
            layers.append((f'url("{url}")', o))
        elif t == "background-gradient-overlay":
            stops = ",".join(f"{val(s['value']['color'])} {s['value']['offset']['value']}%" for s in o["stops"]["value"])
            if val(o.get("type")) == "radial":
                layers.append((f"radial-gradient(circle at {val(o.get('positions')) or 'center center'},{stops})", o))
            else:
                layers.append((f"linear-gradient({(o.get('angle') or {}).get('value', 180)}deg,{stops})", o))
        elif t == "background-color-overlay":
            c = val(o.get("color"))
            layers.append((f"linear-gradient({c},{c})", o))
        else:
            print("WARN unknown bg overlay", t, file=sys.stderr)
    if layers:
        out.append(("background-image", ",".join(str(l[0]) for l in layers)))
        for key in ("size", "position", "repeat", "attachment"):
            vals = [val(l[1].get(key)) for l in layers]
            if any(vals):
                out.append((f"background-{key}", ",".join(x or {"size": "auto", "position": "0% 0%", "repeat": "repeat", "attachment": "scroll"}[key] for x in vals)))
    return out


def props_to_css(props):
    decl = []
    for k, p in (props or {}).items():
        t, v = p.get("$$type"), p.get("value")
        if t == "dimensions":
            decl += box(k, v, lambda pr, kk: f"{pr}-{kk}")
        elif t == "border-width-v2" or t == "border-width":
            decl += box(k, v, lambda pr, kk: f"border-{kk}-width")
        elif t == "border-radius":
            decl += box(k, v, radius_key)
        elif t == "background":
            decl += background(v)
        elif t == "box-shadow":
            parts = []
            for sh in v:
                s = sh["value"]
                parts.append(" ".join(filter(None, [val(s.get("position")) if s.get("position") else None, val(s["hOffset"]), val(s["vOffset"]), val(s["blur"]), val(s["spread"]), val(s["color"])])))
            decl.append(("box-shadow", ",".join(parts)))
        elif t == "transform":
            fns = []
            for f in (v.get("transform-functions") or {}).get("value", []):
                ft, fv = f["$$type"], f["value"]
                if ft == "transform-move":
                    fns.append(f"translate3d({val(fv['x'])},{val(fv['y'])},{val(fv['z'])})")
                elif ft == "transform-scale":
                    fns.append(f"scale3d({val(fv['x'])},{val(fv['y'])},{val(fv['z'])})")
                elif ft == "transform-rotate":
                    fns.append(f"rotateX({val(fv['x'])}) rotateY({val(fv['y'])}) rotateZ({val(fv['z'])})")
            if fns:
                decl.append(("transform", " ".join(fns)))
        elif t in ("backdrop-filter", "filter"):
            fs = []
            for f in v:
                fv = f["value"]
                arg = fv["args"]["value"]
                a = val(arg.get("size") or arg.get("amount") or next(iter(arg.values())))
                fs.append(f"{fv['func']['value']}({a})")
            decl.append((k, " ".join(fs)))
        elif t == "transition":
            ts = []
            for tr in v:
                tv = tr["value"]
                ts.append(f"{tv['selection']['value']['value']['value']} {val(tv['size'])}")
            decl.append(("transition", ",".join(ts)))
        elif t == "object-position":
            decl.append((k, f"{val(v.get('x')) or '50%'} {val(v.get('y')) or '50%'}"))
        elif t == "flex":
            decl.append(("flex", f"{(v.get('flexGrow') or {}).get('value', 0)} {(v.get('flexShrink') or {}).get('value', 1)} {val(v.get('flexBasis')) or 'auto'}"))
        else:
            s = val(p)
            if s is None:
                print("WARN unhandled", k, t, file=sys.stderr)
            else:
                decl.append((k, s))
    return ";".join(f"{a}:{b}" for a, b in decl)


def local_css(elements):
    rules = {"desktop": [], "tablet": [], "mobile": []}

    def walk(e):
        for sid, st in (e.get("styles") or {}).items():
            for var in st["variants"]:
                css = props_to_css(var["props"])
                if var.get("custom_css"):
                    css += ";" + str(var["custom_css"])
                if not css:
                    continue
                state = var["meta"].get("state")
                sel = f".elementor .{sid}" + (f":{state}" if state else "")
                rules[var["meta"].get("breakpoint") or "desktop"].append(f"{sel}{{{css}}}")
        for c in e.get("elements", []):
            walk(c)

    for e in elements:
        walk(e)
    out = rules["desktop"]
    for bp in ("tablet", "mobile"):
        if rules[bp]:
            out.append(f"@media {BP[bp]}{{" + "".join(rules[bp]) + "}")
    return "\n".join(out)


# ---------- global classes (design/classes.css) ----------
def compile_classes(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    blocks, i = [], 0
    for m in re.finditer(r"\.([a-z0-9-]+)\s*\{", src):
        if m.start() < i:
            continue
        depth, j = 1, m.end()
        while depth:
            depth += {"{": 1, "}": -1}.get(src[j], 0)
            j += 1
        blocks.append((m.group(1), src[m.end():j - 1]))
        i = j
    out_base, out_bp = [], {"tablet": [], "mobile": []}
    for name, body in reversed(blocks):  # first listed = highest priority -> emitted last
        body = re.sub(r"\d+(\.\d+)?(svh|dvh)", "", body)  # parser drops these
        nested = re.findall(r"(&:[a-z]+|@media\s*\(--(tablet|mobile)\))\s*\{([^{}]*)\}", body)
        plain = re.sub(r"(&:[a-z]+|@media\s*\(--(tablet|mobile)\))\s*\{[^{}]*\}", "", body)
        sel = f".elementor .{name}"
        out_base.append(f"{sel}{{{plain.strip()}}}")
        for head, bp, inner in nested:
            if head.startswith("&"):
                out_base.append(f"{sel}{head[1:]}{{{inner}}}")
            else:
                out_bp[bp].append(f"{sel}{{{inner}}}")
    css = "\n".join(out_base)
    for bp in ("tablet", "mobile"):
        if out_bp[bp]:
            css += f"\n@media {BP[bp]}{{" + "".join(out_bp[bp]) + "}"
    return css


BASE_CSS = """
.elementor .e-flexbox-base{padding:10px;display:flex;flex-direction:row}
.elementor .e-div-block-base{padding:10px}
.elementor .e-grid-base{padding:10px;display:grid}
.elementor .e-heading-base,.elementor .e-paragraph-base{margin:0}
.elementor .e-heading-link-base,.elementor .e-paragraph-link-base{all:unset;cursor:pointer}
.elementor .e-button-base{text-align:center;padding:12px 24px;border-radius:2px;border-width:0;background-color:#375EFB;display:inline-block;text-decoration:none}
.elementor .e-image-base{display:block}
.elementor .e-background-video-base{width:100%;overflow:hidden;position:relative;padding:10px;display:flex;flex-direction:column}
.elementor .e-background-video-content-base{width:100%;position:relative;z-index:1;padding:0;display:flex;flex-direction:column;flex:1 1 auto}
.elementor .e-background-video-controls-base{width:auto;position:absolute;inset-inline-end:20px;inset-block-end:20px;z-index:2;display:flex;gap:8px}
.elementor .e-background-video-play-base,.elementor .e-background-video-pause-base{cursor:pointer;padding:8px;border-style:none;background-color:transparent;display:inline-flex;justify-content:center;align-items:center}
.elementor .e-accordion-base{padding:0;display:flex;flex-direction:column}
.elementor .e-accordion-item-base{padding:0;display:block}
.elementor .e-accordion-item-header-base{cursor:pointer;padding:10px;display:flex;gap:8px;justify-content:space-between;align-items:center;list-style:none}
.elementor .e-accordion-item-header-base::-webkit-details-marker{display:none}
.elementor .e-accordion-item-title-base{padding:0}
.elementor .e-accordion-item-icon-base{width:200px;height:20px;padding:0;display:inline-flex;flex:0 0 auto;justify-content:flex-end;align-items:center}
details[open] > summary .e-accordion-item-icon-base{transform:rotate(180deg)}
.elementor .e-accordion-item-content-base{min-width:30px;padding:10px;display:block}
.e-background-video__media{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}
.e-background-video--playing .e-background-video__play{display:none}
.e-background-video__pause{display:inline-flex}
"""


def main():
    pid, out = sys.argv[1], sys.argv[2]
    shell_path = sys.argv[3] if len(sys.argv) > 3 else None
    page = json.loads(get(f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content,meta"))
    rendered = page["content"]["rendered"]
    data = json.loads(page["meta"]["_elementor_data"])
    variables = json.loads(get("/wp-json/elementor/v1/variables/list"))["data"]["variables"]
    vcss = []
    for vid, v in variables.items():
        value = f'"{v["value"]}"' if v["type"] == "global-font-variable" else v["value"]
        vcss += [f"--{vid}:{value}", f"--{v['label']}:{value}"]
    classes = compile_classes(open(os.path.join(ROOT, "design", "classes.css")).read())
    css = ":root{" + ";".join(vcss) + "}\n" + BASE_CSS + "\n" + classes + "\n" + local_css(data)
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap">'
    shell = open(shell_path, encoding="utf-8").read() if shell_path else get("/", auth=False)
    start = shell.find('<div data-elementor-type="wp-page"')
    end = shell.find("</main>", start)
    if start < 0 or end < 0:
        raise SystemExit("shell markers not found")
    # Hello theme: <main><div class="page-content">[elementor page div]</div></main>; keep page-content's close
    cut_end = shell.rfind("</div>", start, end)
    doc = shell[:start] + rendered + shell[cut_end:]
    doc = doc.replace("</head>", fonts + f"<style id='xj-preview'>{css}</style></head>", 1)
    open(out, "w", encoding="utf-8").write(doc)
    print("wrote", out, len(doc), "bytes; css", len(css))


if __name__ == "__main__":
    main()
