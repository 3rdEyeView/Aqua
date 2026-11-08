"""Generate Elementor V4 build-composition payloads for the Branham demo (page 1532)."""
import json, os, sys
OUT = os.path.dirname(os.path.abspath(__file__))
U = "https://axiomsystems.systems/wp-content/uploads/2026/11/branham-demo-"
GROUND, SURFACE, INK, MUTED, LINE, TIMBER, TINK, STEEL, BAND = "#141210","#1D1A17","#EEE8DF","#A99F94","#3A332C","#C68D55","#170F08","#BDB9B2","#0D0B0A"
DISP, BODY, TAG = '"Big Shoulders Display"', '"Libre Franklin"', '"DM Mono"'
FOCUS = f"&:focus {{ outline-width: 3px; outline-color: {TIMBER}; outline-style: solid; outline-offset: 3px; }}"

class N:
    def __init__(s, t, cid, cfg=None, css="", kids=None, cls=None):
        s.t, s.cid, s.cfg, s.css, s.kids, s.cls = t, cid, cfg, css, kids or [], cls
import re as _re
SIDES = ["block-start", "block-end", "inline-start", "inline-end"]
def _fix(d):
    lh = [f"border-{x}-width" for x in SIDES]
    if any(k in d for k in lh):
        base = d.pop("border-width", None)
        v = {x: d.pop(f"border-{x}-width", base or "0px") for x in SIDES}
        d["border-width"] = f'{v["block-start"]} {v["inline-end"]} {v["block-end"]} {v["inline-start"]}' 
    if "inset" in d:
        v = d.pop("inset")
        for x in SIDES: d.setdefault(f"inset-{x}", v)
    if "row-gap" in d or "column-gap" in d:
        r = d.pop("row-gap", None); c = d.pop("column-gap", None)
        d["gap"] = r or c
        if c and r and c != r: d["column-gap"] = c
    d.pop("overflow-x", None)
def norm(css):
    """Merge declarations: top-level and per nested block (&:hover, @media...), later wins; emit compactly."""
    blocks = {"": {}}; order = [""]
    i = 0; css = " ".join(css.split())
    def decls(body, into):
        for d in body.split(";"):
            d = d.strip()
            if not d: continue
            k, v = d.split(":", 1)
            into.pop(k.strip(), None); into[k.strip()] = v.strip()
    buf = ""
    while i < len(css):
        m = _re.match(r"(&:[a-z-]+|@media\s*\([^)]*\))\s*\{([^}]*)\}", css[i:])
        if m:
            sel = m.group(1).replace(" ", "")
            if sel not in blocks: blocks[sel] = {}; order.append(sel)
            decls(m.group(2), blocks[sel]); i += m.end(); continue
        j = css.find(";", i); nxt = _re.search(r"(&:|@media)", css[i:])
        if nxt and (j == -1 or i + nxt.start() < j):
            buf_end = i + nxt.start(); decls(css[i:buf_end], blocks[""]); i = buf_end; continue
        if j == -1: decls(css[i:], blocks[""]); break
        decls(css[i:j+1], blocks[""]); i = j + 1
    for b in blocks.values(): _fix(b)
    out = " ".join(f"{k}: {v};" for k, v in blocks[""].items())
    for sel in order[1:]:
        body = " ".join(f"{k}: {v};" for k, v in blocks[sel].items())
        out += f" {sel} {{ {body} }}"
    return out.strip()
def flat(n, xml, cfg, sty, cl):
    xml.append(f'<{n.t} configuration-id="{n.cid}">')
    for k in n.kids: flat(k, xml, cfg, sty, cl)
    xml.append(f'</{n.t}>')
    if n.cfg: cfg[n.cid] = n.cfg
    if n.css: sty[n.cid] = norm(n.css)
    if n.cls: cl[n.cid] = n.cls
def payload(root):
    xml, cfg, sty, cl = [], {}, {}, {}
    flat(root, xml, cfg, sty, cl)
    out = {"xml_structure": "".join(xml), "element_config": cfg, "style": sty}
    if cl: out["classes"] = cl
    return out

# ---------- helpers ----------
def P(cid, text, css="", tag="p", link=None):
    c = {"paragraph": text, "tag": tag}
    if link: c["link"] = link
    return N("e-paragraph", cid, c, "display: block; margin: 0px; " + css)
def H(cid, text, tag, css=""):
    return N("e-heading", cid, {"title": text, "tag": tag},
             f"display: block; margin: 0px; font-family: {DISP}; font-weight: 800; line-height: 0.95; text-transform: uppercase; color: {INK}; " + css)
def L(dest, blank=False): return {"destination": dest, "isTargetBlank": blank, "tag": "a"}
def BTN(cid, text, dest, ghost=False, css="", blank=False):
    base = (f"font-family: {BODY}; font-weight: 600; font-size: 1rem; line-height: 1; text-decoration: none; text-align: center; "
            f"min-height: 48px; padding-block-start: 0.85rem; padding-block-end: 0.85rem; padding-inline-start: 1.35rem; padding-inline-end: 1.35rem; "
            f"border-radius: 2px; border-width: 2px; border-style: solid; display: inline-flex; align-items: center; justify-content: center; {FOCUS} ")
    if ghost: base += f"color: {INK}; border-color: {INK}; background-color: transparent; &:hover {{ color: {GROUND}; background-color: {INK}; }} "
    else: base += f"color: {TINK}; border-color: {TIMBER}; background-color: {TIMBER}; &:hover {{ color: {TIMBER}; background-color: transparent; }} "
    return N("e-button", cid, {"text": text, "link": L(dest, blank)}, base + css)
def FX(cid, kids, css="", **cfg): return N("e-flexbox", cid, cfg or None, "padding: 0px; " + css, kids)
def DV(cid, kids, css="", **cfg): return N("e-div-block", cid, cfg or None, "padding: 0px; " + css, kids)
def GR(cid, kids, css="", **cfg): return N("e-grid", cid, cfg or None, "padding: 0px; " + css, kids)
def IMG(cid, name, alt, css=""):
    return N("e-image", cid, {"image": {"src": {"url": U + name, "alt": alt}, "size": "full"}}, css)
def PH(cid, name, alt, css="", pos=None):
    """Photo box: relative div, image absolutely fills it (object-fit cover)."""
    op = f"object-position: {pos};" if pos else ""
    return DV(cid, [IMG(cid + "-i", name, alt, f"position: absolute; inset: 0px; width: 100%; height: 100%; object-fit: cover; display: block; {op}")],
              f"position: relative; overflow: hidden; background-color: {SURFACE}; " + css)
EYEBROW = f"font-family: {TAG}; font-weight: 500; font-size: 0.75rem; line-height: 1.2; letter-spacing: 0.16em; text-transform: uppercase; color: {TIMBER};"
LEDE = f"font-family: {BODY}; font-size: 1.2rem; line-height: 1.6; color: {MUTED}; max-width: 62ch; @media(--mobile) {{ font-size: 1.1rem; }}"
BODYTXT = f"font-family: {BODY}; font-size: 1.0625rem; line-height: 1.6; color: {INK}; max-width: 62ch;"
H2 = "font-size: 3.8rem; @media(--tablet) { font-size: 3rem; } @media(--mobile) { font-size: 2.3rem; }"
WRAP = "width: 100%; max-width: 1240px; margin-inline-start: auto; margin-inline-end: auto; padding-inline-start: 40px; padding-inline-end: 40px; @media(--mobile) { padding-inline-start: 16px; padding-inline-end: 16px; }"
SECTION = f"width: 100%; background-color: {GROUND}; padding-block-start: 6.5rem; padding-block-end: 6.5rem; display: flex; flex-direction: column; @media(--mobile) {{ padding-block-start: 4rem; padding-block-end: 4rem; }}"
SECID = {"ft": "featured", "ty": "types", "gl": "work", "ab": "about", "es": "estimate"}
def SEC(cid, kids, css="", tag="section"):
    if "padding-block-start: 0px" in css: css += " @media(--mobile) { padding-block-start: 0px; }"
    n = FX(cid, [FX(cid + "-w", kids, WRAP + " flex-direction: column; gap: 0px;")], SECTION + " scroll-margin-top: 74px; " + css, tag=tag)
    n.cfg["_cssid"] = SECID[cid]; return n
def HEAD(cid, eyebrow, title, lede=None, right=None):
    left = [P(cid + "-eb", eyebrow, EYEBROW), H(cid + "-h", title, "h2", H2)]
    if lede: left.append(P(cid + "-ld", lede, LEDE))
    kids = [FX(cid + "-l", left, "flex-direction: column; gap: 1rem; flex: 1 1 auto; min-width: 0px;")]
    if right: kids.append(right)
    return FX(cid, kids, "flex-direction: row; gap: 1.5rem; align-items: flex-end; justify-content: space-between; margin-block-end: 2.5rem; @media(--mobile) { flex-direction: column; align-items: flex-start; }")
def TICKET(cid, pairs):
    k = []
    for i, (a, b) in enumerate(pairs):
        k += [P(f"{cid}-k{i}", a, f"font-family: {TAG}; font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase; color: {MUTED}; padding-block-start: 0.1rem;"),
              P(f"{cid}-v{i}", b, f"font-family: {TAG}; font-size: 0.8rem; line-height: 1.4; color: {INK}; min-width: 0px;")]
    return GR(cid, k, f"grid-template-columns: max-content minmax(0,1fr); grid-template-rows: repeat({len(pairs)}, auto); column-gap: 1rem; row-gap: 0.3rem; "
              f"padding-block-start: 1rem; border-block-start-width: 1px; border-block-end-width: 0px; border-inline-start-width: 0px; border-inline-end-width: 0px; border-style: dashed; border-color: {LINE};")

def BRAND(cid):
    return FX(cid, [P(cid + "1", "Branham", f"font-family: {DISP}; font-weight: 900; font-size: 1.45rem; line-height: 0.9; letter-spacing: 0.02em; text-transform: uppercase; color: {STEEL};", tag="span"),
                    P(cid + "2", "Fencing Co.", f"font-family: {DISP}; font-weight: 600; font-size: 0.78rem; line-height: 1.1; letter-spacing: 0.28em; text-transform: uppercase; color: {MUTED};", tag="span")],
              "width: auto; flex-direction: column; gap: 0px;")
# ---------- 1. header ----------
NAV = [("Our Work", "#work"), ("Fence Types", "#types"), ("About", "#about"), ("Estimates", "#estimate")]
def header():
    brand = FX("hd-brand", [
        IMG("hd-logo", "logo.jpg", "Branham Fencing Co. logo", f"width: 46px; height: 46px; object-fit: cover; object-position: 50% 30%; border-radius: 50%; border-width: 1px; border-style: solid; border-color: {LINE}; display: block;"),
        BRAND("hd-nm"),
    ], f"width: auto; flex: 0 1 auto; gap: 0.75rem; align-items: center; text-decoration: none; margin-inline-end: auto; {FOCUS}", tag="a", link=L("#top"))
    navlinks = [BTN(f"hd-n{i}", t, d, css=f"min-height: 0px; padding-inline-start: 0px; padding-inline-end: 0px; padding-block-start: 0.4rem; padding-block-end: 0.4rem; font-weight: 500; font-size: 0.98rem; color: {INK}; background-color: transparent; border-width: 0px; border-block-end-width: 2px; border-color: transparent; border-radius: 0px; &:hover {{ color: {INK}; background-color: transparent; border-color: {TIMBER}; }}") for i, (t, d) in enumerate(NAV)]
    nav = FX("hd-nav", navlinks, "width: auto; gap: 1.5rem; align-items: center; @media(--tablet) { display: none; }", tag="nav")
    cta = BTN("hd-cta", "Get a free estimate", "#estimate", css="@media(--tablet) { display: none; }")
    mlinks = [BTN(f"hd-m{i}", t, d, css=f"width: 100%; justify-content: flex-start; font-weight: 500; font-size: 1.05rem; color: {INK}; background-color: transparent; border-radius: 0px; border-width: 0px; border-block-end-width: 1px; border-color: {LINE}; padding-inline-start: 0px; padding-block-start: 0.85rem; padding-block-end: 0.85rem; &:hover {{ color: {TIMBER}; background-color: transparent; }}") for i, (t, d) in enumerate(NAV)]
    mlinks.append(BTN("hd-mcta", "Get a free estimate", "#estimate", css="width: 100%; margin-block-start: 1rem;"))
    menu = N("e-accordion", "hd-menu", {"default_state": "all_collapsed", "max_expanded": "one", "show_icon": False, "faq_schema": False},
             "width: auto; position: static; padding: 0px; display: none; flex: 0 0 auto; @media(--tablet) { display: flex; }", [
        N("e-accordion-item", "hd-mi", None, "width: auto; position: static; padding: 0px; border-width: 0px;", [
            N("e-accordion-item-header", "hd-mh", None, f"min-height: 44px; cursor: pointer; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 0.9rem; padding-inline-end: 0.9rem; border-width: 1.5px; border-style: solid; border-color: {INK}; border-radius: 2px; display: flex; gap: 0.5rem; align-items: center; {FOCUS}", [
                N("e-accordion-item-title", "hd-mt", None, "min-width: 0px; padding: 0px;", [P("hd-ml", "Menu", f"font-family: {BODY}; font-weight: 600; font-size: 0.95rem; color: {INK};", tag="span")]),
                N("e-accordion-item-icon", "hd-mic", None, "display: none;"),
            ]),
            N("e-accordion-item-content", "hd-mp", None, f"position: absolute; inset-block-start: 100%; inset-inline-start: 0px; inset-inline-end: 0px; z-index: 60; padding-block-start: 0.5rem; padding-block-end: 1rem; padding-inline-start: 16px; padding-inline-end: 16px; background-color: {GROUND}; border-width: 0px; border-block-end-width: 1px; border-style: solid; border-color: {LINE}; box-shadow: 0px 30px 60px 0px rgba(0,0,0,0.6); display: flex; flex-direction: column; gap: 0px;", mlinks),
        ]),
    ])
    inner = FX("hd-in", [brand, nav, cta, menu], WRAP + " position: static; gap: 1.5rem; align-items: center; min-height: 74px;")
    hdr = FX("hd", [inner], f"width: 100%; position: sticky; inset-block-start: 0px; z-index: 50; background-color: rgba(20,18,16,0.94); border-width: 0px; border-block-end-width: 1px; border-style: solid; border-color: {LINE}; justify-content: center; @media(--tablet) {{ position: relative; }}", tag="header"); hdr.cfg["_cssid"] = "top"; return hdr

# ---------- 2. hero ----------
def hero():
    copy = FX("hr-copy", [
        P("hr-eb", "Fence contractor · Lugoff, SC", EYEBROW),
        H("hr-h1", "Built to last.", "h1", "font-weight: 900; font-size: 6.2rem; @media(--tablet) { font-size: 4.6rem; } @media(--mobile) { font-size: 3rem; }"),
        P("hr-h1b", "Crafted with integrity.", f"font-family: {DISP}; font-weight: 900; line-height: 0.95; text-transform: uppercase; color: {TIMBER}; font-size: 6.2rem; margin-block-start: -1.5rem; @media(--tablet) {{ font-size: 4.6rem; }} @media(--mobile) {{ font-size: 3rem; }}"),
        P("hr-ld", "Wood privacy, arch top, vinyl and aluminum fences, plus decks and steps. Timothy Branham and his crew build every job start to finish.", LEDE),
        FX("hr-act", [BTN("hr-b1", "Get a free estimate", "#estimate"), BTN("hr-b2", "See finished fences", "#work", ghost=True)], "flex-wrap: wrap; gap: 0.75rem;"),
        P("hr-vs", "Whatever you do, work at it with all your heart, as working for the Lord, not for human masters.<br>— Colossians 3:23",
          f"font-family: {BODY}; font-style: italic; font-size: 0.98rem; line-height: 1.5; color: {MUTED}; max-width: 62ch; padding-inline-start: 1rem; border-width: 0px; border-inline-start-width: 2px; border-style: solid; border-color: {TIMBER};"),
    ], "flex-direction: column; gap: 1.5rem; min-width: 0px;")
    tiles = [("150", "Arch top wood privacy fence with capped posts"), ("012", "Black aluminum fence around a backyard pool"), ("027", "Vinyl privacy fence along a side yard"),
             ("017", "Wood ranch rail fence casting long shadows"), ("131", "Charleston style wood privacy fence running down a slope")]
    place = ["grid-column: 1 / 5; grid-row: 1 / 5;", "grid-column: 5 / 7; grid-row: 1 / 3;", "grid-column: 5 / 7; grid-row: 3 / 5;", "grid-column: 1 / 3; grid-row: 5 / 7;", "grid-column: 3 / 7; grid-row: 5 / 7;"]
    mob = ["grid-column: 1 / 7; grid-row: 1 / 5;", "grid-column: 1 / 4; grid-row: 5 / 7;", "grid-column: 4 / 7; grid-row: 5 / 7;", "grid-column: 1 / 3; grid-row: 7 / 9;", "grid-column: 3 / 7; grid-row: 7 / 9;"]
    mos = GR("hr-mos", [PH(f"hr-m{i}", f"fence-{n}.jpg", a, f"{place[i]} min-height: 0px; @media(--mobile) {{ {mob[i]} }}") for i, (n, a) in enumerate(tiles)],
             f"grid-template-columns: repeat(6, minmax(0,1fr)); grid-template-rows: repeat(6, minmax(0,1fr)); column-gap: 6px; row-gap: 6px; padding: 6px; background-color: {LINE}; aspect-ratio: 1 / 1; @media(--mobile) {{ aspect-ratio: 4 / 5; grid-template-rows: repeat(8, minmax(0,1fr)); }}")
    grid = GR("hr-g", [copy, mos], "grid-template-columns: minmax(0,5fr) minmax(0,6fr); grid-template-rows: auto; column-gap: 4rem; row-gap: 2.5rem; align-items: center; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; }")
    return FX("hr", [FX("hr-w", [grid], WRAP + " flex-direction: column;")], SECTION + " padding-block-start: 4rem; padding-block-end: 4rem;", tag="section")

# ---------- 3. spec strip ----------
def spec():
    items = [("Who builds it", "Timothy Branham and his crew"), ("Based in", "Lugoff, South Carolina"), ("What we build", "Wood, vinyl &amp; aluminum fences, decks &amp; steps")]
    cells = []
    for i, (a, b) in enumerate(items):
        sep = f"border-width: 0px; border-inline-start-width: 1px; border-style: solid; border-color: {LINE}; padding-inline-start: 1.5rem; @media(--mobile) {{ border-inline-start-width: 0px; border-block-start-width: 1px; padding-inline-start: 0px; }}" if i else ""
        cells.append(FX(f"sp{i}", [P(f"sp{i}-k", a, f"font-family: {TAG}; font-weight: 500; font-size: 0.72rem; line-height: 1.2; letter-spacing: 0.12em; text-transform: uppercase; color: {MUTED};"),
                                    P(f"sp{i}-v", b, f"font-family: {BODY}; font-weight: 600; font-size: 1.1rem; line-height: 1.35; color: {INK};")],
                       f"flex-direction: column; gap: 0.35rem; padding-block-start: 1.5rem; padding-block-end: 1.5rem; padding-inline-end: 1.5rem; min-width: 0px; @media(--mobile) {{ padding-block-start: 1rem; padding-block-end: 1rem; }} {sep}"))
    g = GR("sp-g", cells, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; column-gap: 0px; row-gap: 0px; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); }")
    return FX("sp", [FX("sp-w", [g], WRAP + " flex-direction: column;")], f"width: 100%; background-color: {SURFACE}; border-width: 0px; border-block-start-width: 1px; border-block-end-width: 1px; border-style: solid; border-color: {LINE}; flex-direction: column;")

# ---------- 4. featured ----------
def featured():
    cards = [("151", "Arch top privacy fence with a double gate between two houses", "Arch top privacy with double gate", [("Style", "Arch top privacy"), ("Material", "Pressure-treated pine"), ("Extras", "Double drive gate, post caps")]),
             ("130", "Charleston style privacy fence along a driveway", "Charleston style privacy", [("Style", "Charleston privacy"), ("Material", "Pressure-treated pine"), ("Site", "Sloped lot along a driveway")]),
             ("160", "Black aluminum pool enclosure on an open lot", "Aluminum pool enclosure", [("Style", "Flat-top picket"), ("Material", "Black aluminum"), ("Use", "Pool enclosure")])]
    k = []
    for i, (n, alt, t, pairs) in enumerate(cards):
        hide = "@media(--tablet) { display: none; } @media(--mobile) { display: flex; }" if i == 2 else ""
        k.append(FX(f"ft{i}", [PH(f"ft{i}-ph", f"fence-{n}.jpg", alt, "aspect-ratio: 4 / 5; width: 100%;"),
                               FX(f"ft{i}-b", [H(f"ft{i}-h", t, "h3", "font-size: 1.55rem; line-height: 1.05;"), TICKET(f"ft{i}-t", pairs)], "flex-direction: column; gap: 1rem; padding: 1.5rem;")],
                    f"flex-direction: column; background-color: {SURFACE}; border-width: 1px; border-style: solid; border-color: {LINE}; text-decoration: none; min-width: 0px; {FOCUS} &:hover {{ border-color: {TIMBER}; }} {hide}", tag="a", link=L("#work")))
    g = GR("ft-g", k, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; column-gap: 1.5rem; row-gap: 1.5rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); }")
    return SEC("ft", [HEAD("ft-hd", "Featured jobs", "Recent fences", right=BTN("ft-all", "View all 40 photos", "#work", ghost=True)), g])

def pickets():
    bar = DV("pk-bar", [], f"height: 26px; opacity: 0.9; background-image: repeating-linear-gradient(90deg, {TIMBER} 0px 16px, transparent 16px 21px);")
    return FX("pk", [FX("pk-w", [bar], WRAP + " flex-direction: column;")], f"width: 100%; background-color: {GROUND}; flex-direction: column;")

# ---------- 6. types ----------
def types():
    items = [("019", "Wood privacy fence on top of a block retaining wall", "Wood privacy", "Pressure-treated pine with post caps and trim, including runs set on retaining walls and down slopes.", "50% 60%"),
             ("148", "Arch top wood fence along a backyard", "Arch top &amp; Charleston", "Curved arch tops and Charleston style privacy for a more finished look.", None),
             ("113", "White vinyl privacy fence along a wooded property line", "Vinyl privacy", "Low-maintenance vinyl panels in white and tan.", "50% 40%"),
             ("014", "Black aluminum fence near a lake", "Aluminum &amp; pool", "Black aluminum for pools, lake lots and front yards, racked to follow the ground.", "50% 35%"),
             ("030", "White ranch rail fence across a field", "Ranch rail", "Wood and white rail fencing for open lots and property lines.", "50% 65%"),
             ("023", "New wood deck platform with steps", "Decks &amp; steps", "Wood steps, landings and small decks.", "50% 55%")]
    k = [FX(f"ty{i}", [PH(f"ty{i}-ph", f"fence-{n}.jpg", alt, "aspect-ratio: 16 / 10; width: 100%;", pos),
                       FX(f"ty{i}-b", [H(f"ty{i}-h", t, "h3", "font-size: 1.55rem; line-height: 1.05;"), P(f"ty{i}-p", d, f"font-family: {BODY}; font-size: 0.98rem; line-height: 1.6; color: {MUTED};")], "flex-direction: column; gap: 0.6rem; padding: 1.5rem;")],
            f"flex-direction: column; background-color: {GROUND}; text-decoration: none; min-width: 0px; {FOCUS}", tag="a", link=L("#work"))
         for i, (n, alt, t, d, pos) in enumerate(items)]
    g = GR("ty-g", k, f"grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: repeat(2, auto); column-gap: 6px; row-gap: 6px; background-color: {LINE}; border-width: 6px; border-style: solid; border-color: {LINE}; @media(--tablet) {{ grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(3, auto); }} @media(--mobile) {{ grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(6, auto); }}")
    return SEC("ty", [HEAD("ty-hd", "What we build", "Fence types", "Every photo on this page is a finished job by Timothy's crew."), g], tag="section")

# ---------- 7. gallery ----------
CATS = ["Wood privacy", "Arch & Charleston", "Vinyl", "Aluminum & metal", "Ranch rail", "Decks & steps"]
PHOTOS = [("150","Arch & Charleston","Arch top privacy, side yard",1),("013","Wood privacy","Capped privacy fence along a tree line",0),("012","Aluminum & metal","Pool fence on a sloped yard",0),
("131","Arch & Charleston","Charleston privacy down a slope",0),("027","Vinyl","Vinyl privacy, side yard",0),("019","Wood privacy","Privacy fence on a retaining wall",0),("017","Ranch rail","Ranch rail along a property line",0),
("151","Arch & Charleston","Arch top with double gate",1),("014","Aluminum & metal","Aluminum fence on a lake lot",0),("022","Wood privacy","Retaining wall job, second angle",0),("113","Vinyl","White vinyl privacy along the woods",0),
("130","Arch & Charleston","Charleston privacy along a driveway",0),("029","Aluminum & metal","Aluminum racked down a wooded slope",0),("035","Wood privacy","Capped privacy behind a two-story home",0),
("020","Decks & steps","Back steps and landing",0),("148","Arch & Charleston","Arch top privacy, full run",1),("155","Wood privacy","Privacy fence along a sidewalk",0),("026","Aluminum & metal","Aluminum backyard enclosure",0),
("094","Wood privacy","New-build backyard enclosure",0),("030","Ranch rail","White rail across an open lot",0),("158","Aluminum & metal","Pool enclosure on a gravel pad",0),("129","Arch & Charleston","Charleston privacy, backyard",0),
("095","Wood privacy","Privacy fence with walk gate",0),("023","Decks & steps","Deck platform with steps",0),("033","Aluminum & metal","Aluminum front and side yard",0),("097","Wood privacy","Backyard privacy, new subdivision",0),
("153","Arch & Charleston","Arch top detail at the post",1),("018","Wood privacy","Privacy fence, side yard",0),("160","Aluminum & metal","Aluminum pool enclosure",0),("098","Wood privacy","Capped privacy, long run",0),
("099","Wood privacy","Privacy fence through the pines",0),("036","Aluminum & metal","Aluminum with landscaped beds",0),("028","Decks & steps","Screened porch",0),("135","Wood privacy","Backyard privacy, open lot",0),
("156","Wood privacy","Privacy along a sidewalk, second angle",0),("141","Aluminum & metal","Black wire field fence",0),("032","Wood privacy","Side yard privacy at dusk",0),("137","Wood privacy","Long backyard run",0),
("096","Wood privacy","Backyard enclosure, new build",0),("157","Wood privacy","Privacy fence beside a walkway",0)]
assert len(PHOTOS) == 40 and len({p[0] for p in PHOTOS}) == 40
CLASSES = {
 "bfc-tile": f"position: relative; overflow: hidden; cursor: zoom-in; padding: 0px; background-color: {SURFACE}; grid-row: span 2; min-height: 0px; {FOCUS}",
 "bfc-tile-wide": "grid-column: span 2;",
 "bfc-tile-img": "position: absolute; inset: 0px; width: 100%; height: 100%; object-fit: cover; display: block;",
 "bfc-tile-cat": f"display: block; margin: 0px; position: absolute; inset-block-start: 0.5rem; inset-inline-start: 0.5rem; padding-block-start: 0.2rem; padding-block-end: 0.2rem; padding-inline-start: 0.45rem; padding-inline-end: 0.45rem; font-family: {TAG}; font-weight: 500; font-size: 0.64rem; line-height: 1.2; letter-spacing: 0.08em; text-transform: uppercase; background-color: rgba(13,11,10,0.78); color: {INK};",
 "bfc-gallery": f"padding: 0px; grid-template-columns: repeat(4, minmax(0,1fr)); grid-auto-rows: 140px; grid-auto-flow: dense; column-gap: 6px; row-gap: 6px; background-color: {LINE}; border-width: 6px; border-style: solid; border-color: {LINE}; @media(--tablet) {{ grid-template-columns: repeat(3, minmax(0,1fr)); }} @media(--mobile) {{ grid-template-columns: repeat(2, minmax(0,1fr)); grid-auto-rows: 110px; }}",
}
def tile(cid, p, label):
    n, cat, title, wide = p
    kids = [N("e-image", cid + "i", {"image": {"src": {"url": U + f"fence-{n}.jpg", "alt": title}, "size": "full"}}, cls=["bfc-tile-img"])]
    if label:
        kids.append(N("e-paragraph", cid + "c", {"paragraph": cat.replace("&", "&amp;"), "tag": "span"}, cls=["bfc-tile-cat"]))
    return N("e-div-block", cid, {"tag": "a", "link": L(U + f"fence-{n}.jpg", True)}, "", kids, cls=["bfc-tile-wide", "bfc-tile"] if wide else ["bfc-tile"])
GAL = f"grid-template-columns: repeat(4, minmax(0,1fr)); grid-auto-rows: 140px; grid-auto-flow: dense; column-gap: 6px; row-gap: 6px; background-color: {LINE}; border-width: 6px; border-style: solid; border-color: {LINE}; @media(--tablet) {{ grid-template-columns: repeat(3, minmax(0,1fr)); }} @media(--mobile) {{ grid-template-columns: repeat(2, minmax(0,1fr)); grid-auto-rows: 110px; }}"
TAB = (f"width: auto; flex: none; min-height: 44px; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 1rem; padding-inline-end: 1rem; "
       f"font-family: {BODY}; font-weight: 500; font-size: 0.95rem; white-space: nowrap; color: {INK}; background-color: transparent; border-width: 2px; border-style: solid; border-color: {TIMBER}; border-radius: 2px; "
       f"&:hover {{ color: {TINK}; background-color: {TIMBER}; }} &:focus {{ color: {TINK}; background-color: {TIMBER}; outline-width: 3px; outline-color: {INK}; outline-style: solid; outline-offset: 2px; }}")
def gallery():
    groups = [("All", PHOTOS)] + [(c, [p for p in PHOTOS if p[1] == c]) for c in CATS]
    menu, panels = [], []
    for gi, (name, ps) in enumerate(groups):
        nm = name.replace("&", "&amp;")
        menu.append(N("e-tab", f"gl-t{gi}", None, TAB, [P(f"gl-t{gi}-l", f"{nm} · {len(ps)}", "color: inherit;", tag="span")]))
        note = f"Showing all {len(ps)} photos." if name == "All" else f"Showing: {nm} · {len(ps)} {'photo' if len(ps) == 1 else 'photos'}."
        panels.append(N("e-tab-content", f"gl-c{gi}", None, "padding: 0px; width: 100%;", [
            P(f"gl-c{gi}-n", note, EYEBROW + " margin-block-end: 1rem;"),
            N("e-grid", f"gl-c{gi}-g", None, "", [tile(f"g{gi}{j}", p, name == "All") for j, p in enumerate(ps)], cls=["bfc-gallery"])]))
    tabs = N("e-tabs", "gl-tabs", {"default-active-tab": 0}, "gap: 1.5rem; padding: 0px;", [
        N("e-tabs-menu", "gl-menu", None, "justify-content: flex-start; flex-wrap: wrap; gap: 0.5rem; padding-block-end: 0.5rem;", menu),
        N("e-tabs-content-area", "gl-area", None, "padding: 0px;", panels)])
    note = P("gl-note", "Tap any photo to open it full size.", f"font-family: {BODY}; font-size: 0.95rem; color: {MUTED}; margin-block-start: 1.5rem;")
    return SEC("gl", [HEAD("gl-hd", "Our work", "Fences we've built", "Finished jobs around Lugoff and the Midlands. Tap a photo to see it full size."), tabs, note], "padding-block-start: 0px;")

# ---------- 8. owner ----------
def owner():
    g = GR("ow-g", [PH("ow-ph", "fence-099.jpg", "Capped wood privacy fence running through the pines", f"aspect-ratio: 4 / 5; width: 100%; border-width: 6px; border-style: solid; border-color: {LINE}; @media(--tablet) {{ max-width: 420px; }}"),
                    FX("ow-c", [P("ow-eb", "Owner on the job", EYEBROW), H("ow-h", "You talk to Timothy, not a call center.", "h2", H2),
                                P("ow-ld", "Branham Fencing Co. is Timothy Branham's company in Lugoff. He quotes the job, his crew builds it, and he's the one you call when it's done.", LEDE),
                                P("ow-p", "The name on the sign is the name on the work. Every post is set to stay put and every board is hung to stay straight, because that fence is going to be standing in your yard for a long time.", BODYTXT)],
                       "flex-direction: column; gap: 1.5rem; min-width: 0px;")],
           "grid-template-columns: minmax(0,4fr) minmax(0,6fr); grid-template-rows: auto; column-gap: 4rem; row-gap: 2.5rem; align-items: center; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; }")
    return SEC("ab", [g], "padding-block-start: 0px;")

# ---------- 9. estimate ----------
def estimate():
    steps = [("Tell us about the yard", "Send the form with your address, the fence style you want and rough footage if you know it."),
             ("We walk the line", "Timothy measures, checks the grade and gate spots, and talks through materials with you."),
             ("Get your price, then the build", "You get a written quote. Once you approve it, the crew gets your fence on the schedule.")]
    st = GR("es-st", [FX(f"es-s{i}", [P(f"es-s{i}-n", f"Step {i+1}", EYEBROW), H(f"es-s{i}-h", a, "h3", "font-size: 1.55rem; line-height: 1.05;"), P(f"es-s{i}-p", b, f"font-family: {BODY}; font-size: 1.0625rem; line-height: 1.6; color: {MUTED};")],
                            f"flex-direction: column; gap: 0.6rem; padding-block-start: 1.5rem; border-width: 0px; border-block-start-width: 2px; border-style: solid; border-color: {TIMBER}; min-width: 0px;") for i, (a, b) in enumerate(steps)],
            "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; column-gap: 2.5rem; row-gap: 1.5rem; margin-block-end: 4rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); }")
    copy = FX("es-copy", [H("es-h", "Get a free estimate", "h2", H2), P("es-ld", "A few details and a rough idea of the footage is all Timothy needs to get started.", LEDE),
                          FX("es-fbw", [BTN("es-fb", "Message Timothy on Facebook ↗", "https://www.facebook.com/tj.branham.92", ghost=True, blank=True)], "")],
              "flex-direction: column; gap: 1.5rem; min-width: 0px;")
    LBL = f"font-family: {TAG}; font-weight: 500; font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: {MUTED};"
    BOX = f"font-family: {BODY}; font-size: 1rem; line-height: 1.4; color: {MUTED}; opacity: 0.75; min-height: 48px; padding-block-start: 0.75rem; padding-block-end: 0.75rem; padding-inline-start: 0.85rem; padding-inline-end: 0.85rem; background-color: {GROUND}; border-width: 1.5px; border-style: solid; border-color: {LINE}; border-radius: 2px;"
    def field(cid, label, ph, tall=False):
        return FX(cid, [P(cid + "-l", label, LBL), P(cid + "-f", ph, BOX + (" min-height: 110px;" if tall else ""))], "flex-direction: column; gap: 0.35rem; min-width: 0px;")
    ROW2 = "grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto; column-gap: 1rem; row-gap: 1rem; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; }"
    form = FX("es-form", [
        P("es-tag", "Form preview · nothing here is sent or saved", f"font-family: {TAG}; font-weight: 500; font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: {MUTED}; padding-block-end: 1rem; border-width: 0px; border-block-end-width: 1px; border-style: dashed; border-color: {LINE};"),
        GR("es-r1", [field("es-name", "Name", "Your name"), field("es-phone", "Phone", "(803) 555-0100")], ROW2),
        field("es-addr", "Job address", "Street, town"),
        GR("es-r2", [field("es-type", "Fence type", "Wood privacy ▾"), field("es-feet", "Rough footage", "e.g. 180 ft")], ROW2),
        field("es-msg", "About the job", "Gates, height, slope, old fence to remove…", True),
        P("es-send", "Request my estimate", f"font-family: {BODY}; font-weight: 600; font-size: 1rem; line-height: 1; text-align: center; color: {TINK}; background-color: {TIMBER}; opacity: 0.55; min-height: 48px; padding-block-start: 1rem; padding-block-end: 1rem; border-radius: 2px; cursor: not-allowed;"),
        P("es-demo", "Demo only. This preview doesn't send anything.", f"font-family: {BODY}; font-size: 0.95rem; color: {TIMBER};"),
    ], f"flex-direction: column; gap: 1rem; background-color: {SURFACE}; border-width: 1px; border-style: solid; border-color: {LINE}; padding: 2.5rem; min-width: 0px; @media(--mobile) {{ padding: 1.5rem; }}")
    g = GR("es-g", [copy, form], "grid-template-columns: minmax(0,5fr) minmax(0,6fr); grid-template-rows: auto; column-gap: 4rem; row-gap: 2.5rem; align-items: start; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; }")
    return SEC("es", [HEAD("es-hd", "Getting an estimate", "How a job starts"), st, g], "padding-block-start: 0px;")

# ---------- 10. band ----------
def band():
    bg = IMG("bd-bg", "fence-135.jpg", "", "position: absolute; inset: 0px; width: 100%; height: 100%; object-fit: cover; opacity: 0.28; display: block;")
    copy = FX("bd-c", [H("bd-h", "Need a fence up?", "h2", H2), P("bd-p", "Tell Timothy what you're after and he'll get back to you with a price.", f"font-family: {BODY}; font-size: 1.0625rem; line-height: 1.6; color: rgba(238,232,223,0.82);")],
              "flex-direction: column; gap: 1rem; min-width: 0px; flex: 1 1 auto;")
    w = FX("bd-w", [copy, BTN("bd-b", "Get a free estimate", "#estimate")], WRAP + " position: relative; gap: 2.5rem; align-items: center; justify-content: space-between; @media(--tablet) { flex-direction: column; align-items: flex-start; }")
    return FX("bd", [bg, w], f"width: 100%; position: relative; overflow: hidden; background-color: {BAND}; padding-block-start: 6.5rem; padding-block-end: 6.5rem; flex-direction: column; @media(--mobile) {{ padding-block-start: 4rem; padding-block-end: 4rem; }}", tag="section")

# ---------- 11. footer + mobile bar ----------
def footer():
    FL = f"font-family: {BODY}; font-size: 0.95rem; color: {INK}; text-decoration: none; &:hover {{ text-decoration: underline; }}"
    def lk(cid, t, d, blank=False): return P(cid, t, FL, link=L(d, blank))
    g = GR("fo-g", [
        FX("fo-a", [BRAND("fo-nm"),
                    P("fo-desc", "Wood, vinyl and aluminum fences built by Timothy Branham's crew. Based in Lugoff, South Carolina.", f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.6; color: {MUTED};")],
           "flex-direction: column; gap: 0.5rem; min-width: 0px; @media(--tablet) { grid-column: 1 / -1; }"),
        FX("fo-b", [P("fo-b-h", "On this page", EYEBROW), lk("fo-b1", "Our Work", "#work"), lk("fo-b2", "Fence Types", "#types"), lk("fo-b3", "About", "#about"), lk("fo-b4", "Free estimate", "#estimate")], "flex-direction: column; gap: 0.5rem; min-width: 0px;"),
        FX("fo-c", [P("fo-c-h", "Follow", EYEBROW), lk("fo-c1", "Facebook ↗", "https://www.facebook.com/tj.branham.92", True), lk("fo-c2", "Instagram ↗", "https://www.instagram.com/tj.branham.92/", True), lk("fo-c3", "Back to top ↑", "#top")], "flex-direction: column; gap: 0.5rem; min-width: 0px;"),
    ], "grid-template-columns: minmax(0,2fr) minmax(0,1fr) minmax(0,1fr); grid-template-rows: auto; column-gap: 2.5rem; row-gap: 2.5rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; }")
    fine = P("fo-fine", "Website concept by Axiom Systems. Demo only.", f"font-family: {TAG}; font-size: 0.78rem; color: {MUTED}; margin-block-start: 2.5rem; padding-block-start: 1.5rem; border-width: 0px; border-block-start-width: 1px; border-style: solid; border-color: {LINE};")
    return FX("fo", [FX("fo-w", [g, fine], WRAP + " flex-direction: column;")],
              f"width: 100%; background-color: {GROUND}; border-width: 0px; border-block-start-width: 1px; border-style: solid; border-color: {LINE}; padding-block-start: 4rem; padding-block-end: 4rem; flex-direction: column; @media(--tablet) {{ padding-block-end: calc(4rem + 72px); }}", tag="footer")
def mobilebar():
    A = f"min-height: 54px; display: flex; align-items: center; justify-content: center; font-family: {BODY}; font-weight: 600; font-size: 1rem; text-decoration: none; border-radius: 0px; border-width: 0px; padding: 0px; {FOCUS}"
    return GR("mb", [BTN("mb-1", "See our work", "#work", css=A + f" color: {INK}; background-color: {SURFACE}; &:hover {{ color: {TIMBER}; background-color: {SURFACE}; }}"),
                     BTN("mb-2", "Free estimate", "#estimate", css=A)],
              f"display: none; position: fixed; inset-inline-start: 0px; inset-inline-end: 0px; inset-block-end: 0px; z-index: 30; grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto; column-gap: 6px; row-gap: 0px; padding: 6px; background-color: {LINE}; @media(--tablet) {{ display: grid; }}",
              tag="nav")

def root():
    return FX("bfc", [header(), hero(), spec(), featured(), pickets(), types(), gallery(), owner(), estimate(), band(), footer(), mobilebar()],
              f"width: 100%; max-width: 100%; flex-direction: column; gap: 0px; background-color: {GROUND}; color: {INK}; overflow-x: clip;")

if __name__ == "__main__":
    r = root()
    # split: shell + per-section payloads appended under the shell's id later
    full = payload(r)
    json.dump(full, open(os.path.join(OUT, "full.json"), "w"), ensure_ascii=False)
    for n in r.kids:
        json.dump(payload(n), open(os.path.join(OUT, f"sec-{n.cid}.json"), "w"), ensure_ascii=False)
    json.dump(CLASSES, open(os.path.join(OUT, "classes.json"), "w"), ensure_ascii=False)
    print({n.cid: len(json.dumps(payload(n))) for n in r.kids}, "total", len(json.dumps(full)))
