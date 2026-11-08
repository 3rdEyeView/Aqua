"""Elementor V4 build payloads for the Advanced Fence Service demo.
Reuses the build helpers (N, norm, payload) from the Branham demo generator; palette, fonts and content are new."""
import importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("bgen", os.path.join(HERE, "..", "..", "2026-11-08-branham-demo", "native", "gen.py"))
bgen = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(bgen)
N, payload, L = bgen.N, bgen.payload, bgen.L

U = "https://axiomsystems.systems/wp-content/uploads/2026/11/advanced-demo-"
FB = "https://www.facebook.com/p/Advanced-Fence-Service-LLC-100067595773677/"
# Palette from the logo: copper/wood on charcoal, with warm light content sections.
NIGHT, NIGHT2, PAPER, CARD, INK, MUTED, LINE, COPPER, COPPER_D, ONDARK, ONDARK_M = (
    "#161412", "#211E1B", "#F4F1EC", "#FFFFFF", "#1B1A18", "#5E5A54", "#DDD6CC", "#C9803F", "#9A5420", "#F4F1EC", "#B8B0A6")
DISP, BODY, TAG = '"Oswald"', '"Archivo"', '"IBM Plex Mono"'
FOCUS = f"&:focus {{ outline-width: 3px; outline-color: {COPPER}; outline-style: solid; outline-offset: 3px; }}"

def P(cid, text, css="", tag="p", link=None, cls=None):
    c = {"paragraph": text, "tag": tag}
    if link: c["link"] = link
    return N("e-paragraph", cid, c, "display: block; margin: 0px; " + css, cls=cls)
def H(cid, text, tag, css=""):
    return N("e-heading", cid, {"title": text, "tag": tag},
             f"display: block; margin: 0px; font-family: {DISP}; font-weight: 600; line-height: 1.02; text-transform: uppercase; letter-spacing: 0.01em; color: {INK}; " + css)
def BTN(cid, text, dest, kind="solid", css="", blank=False):
    base = (f"font-family: {BODY}; font-weight: 600; font-size: 1rem; line-height: 1; text-decoration: none; text-align: center; "
            f"min-height: 48px; padding-block-start: 0.85rem; padding-block-end: 0.85rem; padding-inline-start: 1.4rem; padding-inline-end: 1.4rem; "
            f"border-radius: 3px; border-width: 2px; border-style: solid; display: inline-flex; align-items: center; justify-content: center; flex: 0 0 auto; {FOCUS} ")
    if kind == "solid": base += f"color: #FFFFFF; border-color: {COPPER_D}; background-color: {COPPER_D}; &:hover {{ color: #FFFFFF; background-color: {INK}; border-color: {INK}; }} "
    elif kind == "ghost-dark": base += f"color: {ONDARK}; border-color: {ONDARK}; background-color: transparent; &:hover {{ color: {NIGHT}; background-color: {ONDARK}; }} "
    else: base += f"color: {INK}; border-color: {INK}; background-color: transparent; &:hover {{ color: #FFFFFF; background-color: {INK}; }} "
    return N("e-button", cid, {"text": text, "link": L(dest, blank)}, base + css)
def FX(cid, kids, css="", **cfg): return N("e-flexbox", cid, cfg or None, "padding: 0px; " + css, kids)
def DV(cid, kids, css="", **cfg): return N("e-div-block", cid, cfg or None, "padding: 0px; " + css, kids)
def GR(cid, kids, css="", **cfg): return N("e-grid", cid, cfg or None, "padding: 0px; " + css, kids)
def IMG(cid, name, alt, css=""):
    return N("e-image", cid, {"image": {"src": {"url": U + name, "alt": alt}, "size": "full"}}, css)
FILL = "position: absolute; inset: 0px; width: 100%; height: 100%; object-fit: cover; display: block;"
def PH(cid, name, alt, css=""):
    return DV(cid, [IMG(cid + "-i", name, alt, FILL)], f"position: relative; overflow: hidden; background-color: {LINE}; " + css)

EYEBROW = f"font-family: {TAG}; font-weight: 500; font-size: 0.75rem; line-height: 1.2; letter-spacing: 0.14em; text-transform: uppercase; color: {COPPER_D};"
LEDE = f"font-family: {BODY}; font-size: 1.2rem; line-height: 1.6; color: {MUTED}; max-width: 62ch; @media(--mobile) {{ font-size: 1.08rem; }}"
H2 = "font-size: 3.2rem; @media(--tablet) { font-size: 2.6rem; } @media(--mobile) { font-size: 2.1rem; }"
WRAP = "width: 100%; max-width: 1200px; margin-inline-start: auto; margin-inline-end: auto; padding-inline-start: 40px; padding-inline-end: 40px; @media(--mobile) { padding-inline-start: 16px; padding-inline-end: 16px; }"
SECTION = f"width: 100%; background-color: {PAPER}; padding-block-start: 6rem; padding-block-end: 6rem; display: flex; flex-direction: column; scroll-margin-top: 76px; @media(--mobile) {{ padding-block-start: 4rem; padding-block-end: 4rem; }}"
def SEC(cid, anchor, kids, css=""):
    n = FX(cid, [FX(cid + "-w", kids, WRAP + " flex-direction: column; gap: 0px;")], SECTION + " " + css, tag="section")
    if anchor: n.cfg["_cssid"] = anchor
    return n
def HEAD(cid, eyebrow, title, lede=None, right=None):
    left = [P(cid + "-eb", eyebrow, EYEBROW), H(cid + "-h", title, "h2", H2)]
    if lede: left.append(P(cid + "-ld", lede, LEDE))
    kids = [FX(cid + "-l", left, "flex-direction: column; gap: 0.9rem; flex: 1 1 auto; min-width: 0px;")]
    if right: kids.append(right)
    return FX(cid, kids, "flex-direction: row; gap: 1.5rem; align-items: flex-end; justify-content: space-between; margin-block-end: 2.5rem; @media(--mobile) { flex-direction: column; align-items: flex-start; }")

NAV = [("Our Work", "#work"), ("Fence Types", "#types"), ("About", "#about"), ("Estimates", "#estimate")]
def BRAND(cid, dark=True):
    c1, c2 = (ONDARK, COPPER) if dark else (INK, COPPER_D)
    return FX(cid, [P(cid + "1", "Advanced", f"font-family: {DISP}; font-weight: 600; font-size: 1.35rem; line-height: 0.95; letter-spacing: 0.04em; text-transform: uppercase; color: {c1};", tag="span"),
                    P(cid + "2", "Fence Service", f"font-family: {DISP}; font-weight: 500; font-size: 0.78rem; line-height: 1.2; letter-spacing: 0.24em; text-transform: uppercase; color: {c2};", tag="span")],
              "width: auto; flex-direction: column; gap: 0.1rem;")

def header():
    brand = FX("hd-brand", [IMG("hd-logo", "logo-facebook.jpg", "Advanced Fence Service logo", f"width: 52px; height: 52px; object-fit: cover; border-radius: 50%; border-width: 1px; border-style: solid; border-color: #3A342E; display: block;"),
                            BRAND("hd-nm")], f"width: auto; flex: 0 1 auto; gap: 0.75rem; align-items: center; text-decoration: none; margin-inline-end: auto; {FOCUS}", tag="a", link=L("#top"))
    navlinks = [BTN(f"hd-n{i}", t, d, css=f"min-height: 0px; padding-inline-start: 0px; padding-inline-end: 0px; padding-block-start: 0.4rem; padding-block-end: 0.4rem; font-weight: 500; font-size: 0.98rem; color: {ONDARK}; background-color: transparent; border-radius: 0px; border-width: 0px 0px 2px 0px; border-color: transparent; &:hover {{ color: {ONDARK}; background-color: transparent; border-color: {COPPER}; }}") for i, (t, d) in enumerate(NAV)]
    nav = FX("hd-nav", navlinks, "width: auto; gap: 1.75rem; align-items: center; @media(--tablet) { display: none; }", tag="nav")
    cta = BTN("hd-cta", "Get a free estimate", "#estimate", css="@media(--tablet) { display: none; }")
    mlinks = [BTN(f"hd-m{i}", t, d, css=f"width: 100%; justify-content: flex-start; font-weight: 500; font-size: 1.05rem; color: {ONDARK}; background-color: transparent; border-radius: 0px; border-width: 0px 0px 1px 0px; border-color: #3A342E; padding-inline-start: 0px; &:hover {{ color: {COPPER}; background-color: transparent; border-color: #3A342E; }}") for i, (t, d) in enumerate(NAV)]
    mlinks.append(BTN("hd-mcta", "Get a free estimate", "#estimate", css="width: 100%; margin-block-start: 1rem;"))
    menu = N("e-accordion", "hd-menu", {"default_state": "all_collapsed", "max_expanded": "one", "show_icon": False, "faq_schema": False},
             "width: auto; position: static; padding: 0px; display: none; flex: 0 0 auto; @media(--tablet) { display: flex; }", [
        N("e-accordion-item", "hd-mi", None, "width: auto; position: static; padding: 0px; border-width: 0px;", [
            N("e-accordion-item-header", "hd-mh", None, f"min-height: 44px; cursor: pointer; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 0.9rem; padding-inline-end: 0.9rem; border-width: 1.5px; border-style: solid; border-color: {ONDARK}; border-radius: 3px; display: flex; gap: 0.5rem; align-items: center; {FOCUS}", [
                N("e-accordion-item-title", "hd-mt", None, "min-width: 0px; padding: 0px;", [P("hd-ml", "Menu", f"font-family: {BODY}; font-weight: 600; font-size: 0.95rem; color: {ONDARK};", tag="span")]),
                N("e-accordion-item-icon", "hd-mic", None, "display: none;")]),
            N("e-accordion-item-content", "hd-mp", None, f"position: absolute; inset-block-start: 100%; inset-inline-start: 0px; inset-inline-end: 0px; z-index: 60; padding-block-start: 0.5rem; padding-block-end: 1rem; padding-inline-start: 16px; padding-inline-end: 16px; background-color: {NIGHT}; border-width: 0px 0px 1px 0px; border-style: solid; border-color: #3A342E; box-shadow: 0px 30px 60px 0px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 0px;", mlinks)])])
    inner = FX("hd-in", [brand, nav, cta, menu], WRAP + " position: static; gap: 1.5rem; align-items: center; min-height: 76px;")
    h = FX("hd", [inner], f"width: 100%; position: sticky; inset-block-start: 0px; z-index: 50; background-color: rgba(22,20,18,0.96); border-width: 0px 0px 1px 0px; border-style: solid; border-color: #3A342E; justify-content: center; @media(--tablet) {{ position: relative; }}", tag="header")
    h.cfg["_cssid"] = "top"; return h

def hero():
    bg = IMG("hr-bg", "hero-wood-privacy.jpg", "New wood privacy fence along a backyard tree line", FILL + " object-position: 50% 55%;")
    shade = DV("hr-shade", [], "position: absolute; inset: 0px; background-image: linear-gradient(90deg, rgba(22,20,18,0.92) 0%, rgba(22,20,18,0.78) 45%, rgba(22,20,18,0.35) 100%); @media(--mobile) { background-image: linear-gradient(180deg, rgba(22,20,18,0.70) 0%, rgba(22,20,18,0.88) 100%); }")
    copy = FX("hr-copy", [
        P("hr-eb", "Fence contractor · Columbia, SC", EYEBROW + f" color: {COPPER};"),
        H("hr-h1", "Fences done right,", "h1", f"color: {ONDARK}; font-weight: 600; font-size: 5rem; @media(--tablet) {{ font-size: 4rem; }} @media(--mobile) {{ font-size: 2.7rem; }}"),
        P("hr-h1b", "gate to post.", f"font-family: {DISP}; font-weight: 600; line-height: 1.02; text-transform: uppercase; color: {COPPER}; font-size: 5rem; margin-block-start: -1.2rem; @media(--tablet) {{ font-size: 4rem; }} @media(--mobile) {{ font-size: 2.7rem; margin-block-start: -0.9rem; }}"),
        P("hr-ld", "Wood privacy, vinyl, black metal, chain link and split rail fences, plus custom gates and arbors, for homes and businesses around Columbia.",
          f"font-family: {BODY}; font-size: 1.2rem; line-height: 1.6; color: {ONDARK}; opacity: 0.9; max-width: 54ch; @media(--mobile) {{ font-size: 1.08rem; }}"),
        FX("hr-act", [BTN("hr-b1", "Get a free estimate", "#estimate"), BTN("hr-b2", "See our work", "#work", kind="ghost-dark")], "flex-wrap: wrap; gap: 0.75rem;"),
    ], "position: relative; flex-direction: column; gap: 1.4rem; max-width: 640px; min-width: 0px;")
    w = FX("hr-w", [copy], WRAP + " position: relative; flex-direction: column; justify-content: center; min-height: 600px; padding-block-start: 5rem; padding-block-end: 5rem; @media(--mobile) { min-height: 520px; padding-block-start: 3.5rem; padding-block-end: 3.5rem; }")
    return FX("hr", [bg, shade, w], f"width: 100%; position: relative; overflow: hidden; background-color: {NIGHT}; flex-direction: column;", tag="section")

def spec():
    items = [("Based in", "Columbia, South Carolina"), ("What we build", "Wood, vinyl, metal &amp; chain link fences"), ("Also", "Custom gates, arbors &amp; split rail")]
    cells = []
    for i, (a, b) in enumerate(items):
        sep = f"border-style: solid; border-color: {LINE}; border-width: 0px 0px 0px 1px; padding-inline-start: 1.5rem; @media(--mobile) {{ border-width: 1px 0px 0px 0px; padding-inline-start: 0px; }}" if i else ""
        cells.append(FX(f"sp{i}", [P(f"sp{i}-k", a, f"font-family: {TAG}; font-weight: 500; font-size: 0.72rem; line-height: 1.2; letter-spacing: 0.12em; text-transform: uppercase; color: {MUTED};"),
                                    P(f"sp{i}-v", b, f"font-family: {BODY}; font-weight: 600; font-size: 1.1rem; line-height: 1.35; color: {INK};")],
                       f"flex-direction: column; gap: 0.35rem; padding-block-start: 1.5rem; padding-block-end: 1.5rem; padding-inline-end: 1.5rem; min-width: 0px; @media(--mobile) {{ padding-block-start: 1rem; padding-block-end: 1rem; }} {sep}"))
    g = GR("sp-g", cells, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; gap: 0px; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); }")
    return FX("sp", [FX("sp-w", [g], WRAP + " flex-direction: column;")], f"width: 100%; background-color: {CARD}; border-style: solid; border-color: {LINE}; border-width: 0px 0px 1px 0px; flex-direction: column;")

def TICKET(cid, pairs):
    k = []
    for i, (a, b) in enumerate(pairs):
        k += [P(f"{cid}-k{i}", a, f"font-family: {TAG}; font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase; color: {MUTED}; padding-block-start: 0.1rem;"),
              P(f"{cid}-v{i}", b, f"font-family: {TAG}; font-size: 0.8rem; line-height: 1.4; color: {INK}; min-width: 0px;")]
    return GR(cid, k, f"grid-template-columns: max-content minmax(0,1fr); grid-template-rows: repeat({len(pairs)}, auto); gap: 0.3rem; column-gap: 1rem; padding-block-start: 1rem; border-style: dashed; border-color: {LINE}; border-width: 1px 0px 0px 0px;")

def featured():
    cards = [("fb-black-driveway-gate.jpg", "Black metal driveway gate between brick columns", "Black metal driveway gate", [("Style", "Arched double drive gate"), ("Material", "Black metal"), ("Set", "Brick columns, gravel drive")]),
             ("fb-white-vinyl-gate.jpg", "White vinyl privacy gate beside a brick house", "White vinyl privacy gate", [("Style", "Privacy with X-brace gate"), ("Material", "White vinyl"), ("Use", "Side-yard access")]),
             ("fb-arbor-gate.jpg", "Wood privacy fence with a lattice arbor over the gate", "Arbor gate &amp; privacy", [("Style", "Privacy with lattice arbor"), ("Material", "Pressure-treated pine"), ("Extras", "Arbor over walk gate")])]
    k = []
    for i, (n, alt, t, pairs) in enumerate(cards):
        hide = "@media(--tablet) { display: none; } @media(--mobile) { display: flex; }" if i == 2 else ""
        k.append(FX(f"ft{i}", [PH(f"ft{i}-ph", n, alt, "aspect-ratio: 1 / 1; width: 100%;"),
                               FX(f"ft{i}-b", [H(f"ft{i}-h", t, "h3", "font-size: 1.45rem; line-height: 1.1;"), TICKET(f"ft{i}-t", pairs)], "flex-direction: column; gap: 1rem; padding: 1.5rem;")],
                    f"flex-direction: column; background-color: {CARD}; border-width: 1px; border-style: solid; border-color: {LINE}; text-decoration: none; min-width: 0px; max-width: 408px; {FOCUS} &:hover {{ border-color: {COPPER_D}; }} {hide}", tag="a", link=L("#work")))
    g = GR("ft-g", k, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; gap: 1.5rem; justify-items: center; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); }")
    return SEC("ft", "featured", [HEAD("ft-hd", "Recent projects", "From the job site", right=BTN("ft-all", "View all 14 photos", "#work", kind="ghost")), g])

def types():
    items = [("fb-wood-privacy-woods.jpg", "Wood privacy fence along a wooded lot", "Wood privacy", "Pressure-treated pine privacy fences, including lattice tops and runs along wooded lots."),
             ("fb-white-vinyl-between-houses.jpg", "White vinyl privacy fence between two houses", "Vinyl", "Low-maintenance white vinyl privacy fencing and matching gates."),
             ("fb-black-metal-double-gate.jpg", "Black metal fence with a double gate", "Black metal &amp; gates", "Black metal fencing for pools, lake lots and drives, with walk and double gates."),
             ("fb-commercial-chain-link-gate.jpg", "Galvanized chain link fence and gate at a commercial lot", "Chain link", "Galvanized and green-coated chain link for yards, businesses and commercial lots."),
             ("fb-split-rail-lawn.jpg", "Split rail fence across a lawn", "Rail &amp; farm", "Split rail and wood-and-wire fencing for open lots and property lines."),
             ("fb-arbor-gate.jpg", "Lattice arbor over a wood gate", "Custom gates &amp; arbors", "Walk gates, drive gates and arbors built to match the fence.")]
    k = [FX(f"ty{i}", [PH(f"ty{i}-ph", n, alt, "aspect-ratio: 4 / 3; width: 100%;"),
                       FX(f"ty{i}-b", [H(f"ty{i}-h", t, "h3", "font-size: 1.45rem; line-height: 1.1;"), P(f"ty{i}-p", d, f"font-family: {BODY}; font-size: 0.98rem; line-height: 1.6; color: {MUTED};")], "flex-direction: column; gap: 0.6rem; padding: 1.5rem;")],
            f"flex-direction: column; background-color: {CARD}; text-decoration: none; min-width: 0px; {FOCUS}", tag="a", link=L("#work"))
         for i, (n, alt, t, d) in enumerate(items)]
    g = GR("ty-g", k, f"grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: repeat(2, auto); gap: 1px; background-color: {LINE}; border-width: 1px; border-style: solid; border-color: {LINE}; @media(--tablet) {{ grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(3, auto); }} @media(--mobile) {{ grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(6, auto); }}")
    return SEC("ty", "types", [HEAD("ty-hd", "What we build", "Fence types", "Every photo on this page is a finished Advanced Fence Service job."), g], "padding-block-start: 0px; @media(--mobile) { padding-block-start: 0px; }")

CATS = ["Wood privacy", "Vinyl", "Metal & gates", "Chain link", "Rail & farm"]
PHOTOS = [("wood-privacy-lawn", "Wood privacy", "Wood privacy fence around an open backyard"),
          ("black-driveway-gate", "Metal & gates", "Black metal driveway gate between brick columns"),
          ("white-vinyl-between-houses", "Vinyl", "White vinyl privacy fence between two houses"),
          ("split-rail-lawn", "Rail & farm", "Split rail fence across a shaded lawn"),
          ("poolside-privacy", "Wood privacy", "Wood privacy fence around a backyard pool"),
          ("commercial-chain-link-gate", "Chain link", "Galvanized chain link gate at a commercial lot"),
          ("black-metal-lake", "Metal & gates", "Black metal fence on a lake lot"),
          ("arbor-gate", "Wood privacy", "Lattice arbor over a wood privacy gate"),
          ("wood-and-wire", "Rail & farm", "Wood post and wire fence along a wooded line"),
          ("white-vinyl-gate", "Vinyl", "White vinyl privacy gate beside a brick house"),
          ("wood-lattice-detail", "Wood privacy", "Wood privacy fence with a lattice top"),
          ("green-chain-link", "Chain link", "Green-coated chain link enclosure at a business"),
          ("black-metal-double-gate", "Metal & gates", "Black metal fence with a double gate"),
          ("wood-privacy-woods", "Wood privacy", "Wood privacy fence along a wooded lot")]
assert len(PHOTOS) == 14 and all(os.path.exists(os.path.join(HERE, "..", "img", f"advanced-demo-fb-{p[0]}.jpg")) for p in PHOTOS)
CLASSES = {
    "afs-gallery": f"padding: 0px; grid-template-columns: repeat(4, minmax(0,1fr)); grid-auto-rows: auto; gap: 10px; @media(--tablet) {{ grid-template-columns: repeat(3, minmax(0,1fr)); }} @media(--mobile) {{ grid-template-columns: repeat(2, minmax(0,1fr)); gap: 8px; }}",
    "afs-tile": f"position: relative; overflow: hidden; display: block; aspect-ratio: 1 / 1; max-width: 408px; width: 100%; padding: 0px; cursor: zoom-in; background-color: {LINE}; border-radius: 3px; {FOCUS}",
    "afs-tile-img": "position: absolute; width: 100%; height: 100%; object-fit: cover; display: block; inset-block-start: 0px; inset-block-end: 0px; inset-inline-start: 0px; inset-inline-end: 0px;",
    "afs-tile-cat": f"display: block; margin: 0px; position: absolute; inset-block-start: 0.5rem; inset-inline-start: 0.5rem; padding-block-start: 0.2rem; padding-block-end: 0.2rem; padding-inline-start: 0.45rem; padding-inline-end: 0.45rem; font-family: {TAG}; font-weight: 500; font-size: 0.64rem; line-height: 1.2; letter-spacing: 0.06em; text-transform: uppercase; background-color: rgba(22,20,18,0.8); color: {ONDARK};",
}
def tile(cid, p, label):
    n, cat, title = p
    kids = [N("e-image", cid + "i", {"image": {"src": {"url": U + f"fb-{n}.jpg", "alt": title}, "size": "full"}}, cls=["afs-tile-img"])]
    if label: kids.append(N("e-paragraph", cid + "c", {"paragraph": cat.replace("&", "&amp;"), "tag": "span"}, cls=["afs-tile-cat"]))
    return N("e-div-block", cid, {"tag": "a", "link": L(U + f"fb-{n}.jpg", True)}, "", kids, cls=["afs-tile"])
TAB = (f"width: auto; flex: none; min-height: 44px; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 1rem; padding-inline-end: 1rem; "
       f"font-family: {BODY}; font-weight: 500; font-size: 0.95rem; color: {INK}; background-color: {CARD}; border-width: 1.5px; border-style: solid; border-color: {INK}; border-radius: 3px; "
       f"&:hover {{ color: #FFFFFF; background-color: {COPPER_D}; border-color: {COPPER_D}; }} &:focus {{ color: #FFFFFF; background-color: {COPPER_D}; outline-width: 3px; outline-color: {INK}; outline-style: solid; outline-offset: 2px; }}")
def gallery():
    groups = [("All", PHOTOS)] + [(c, [p for p in PHOTOS if p[1] == c]) for c in CATS]
    menu, panels = [], []
    for gi, (name, ps) in enumerate(groups):
        nm = name.replace("&", "&amp;")
        menu.append(N("e-tab", f"gl-t{gi}", None, TAB, [P(f"gl-t{gi}-l", f"{nm} · {len(ps)}", "color: inherit;", tag="span")]))
        note = f"Showing all {len(ps)} photos." if name == "All" else f"Showing: {nm} · {len(ps)} photos."
        panels.append(N("e-tab-content", f"gl-c{gi}", None, "padding: 0px; width: 100%;", [
            P(f"gl-c{gi}-n", note, EYEBROW + " margin-block-end: 1rem;"),
            N("e-grid", f"gl-c{gi}-g", None, "", [tile(f"a{gi}{j}", p, name == "All") for j, p in enumerate(ps)], cls=["afs-gallery"])]))
    tabs = N("e-tabs", "gl-tabs", {"default-active-tab": 0}, "gap: 1.5rem; padding: 0px;", [
        N("e-tabs-menu", "gl-menu", None, "justify-content: flex-start; flex-wrap: wrap; gap: 0.5rem; padding-block-end: 0.5rem;", menu),
        N("e-tabs-content-area", "gl-area", None, "padding: 0px;", panels)])
    note = P("gl-note", "Tap any photo to open it on its own. These are from Advanced Fence Service's Facebook page.", f"font-family: {BODY}; font-size: 0.95rem; color: {MUTED}; margin-block-start: 1.5rem;")
    return SEC("gl", "work", [HEAD("gl-hd", "Our work", "Fences we've built", "Finished jobs around Columbia and the Midlands."), tabs, note], "padding-block-start: 0px; @media(--mobile) { padding-block-start: 0px; }")

def owner():
    g = GR("ow-g", [PH("ow-ph", "fb-wood-lattice-detail.jpg", "Wood privacy fence with a lattice top", f"aspect-ratio: 1 / 1; width: 100%; max-width: 408px; border-radius: 3px;"),
                    FX("ow-c", [P("ow-eb", "Talk to the owner", EYEBROW), H("ow-h", "Call Chris, not a call center.", "h2", H2),
                                P("ow-ld", "Advanced Fence Service is Chris's fence company in Columbia. You talk to him about the job, the materials and the price, and he's who you call when it's done.", LEDE),
                                P("ow-p", "Wood, vinyl, metal or chain link, the work is the same: posts set solid, lines straight and gates that close the way they should.", f"font-family: {BODY}; font-size: 1.0625rem; line-height: 1.6; color: {INK}; max-width: 62ch;")],
                       "flex-direction: column; gap: 1.4rem; min-width: 0px;")],
           "grid-template-columns: minmax(0,5fr) minmax(0,7fr); grid-template-rows: auto; align-items: center; gap: 2.5rem; column-gap: 4rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; }")
    return SEC("ab", "about", [g], f"background-color: {CARD}; border-style: solid; border-color: {LINE}; border-width: 1px 0px 1px 0px;")

def estimate():
    steps = [("Tell us about the job", "Send the form with your address, the fence you want and rough footage if you know it."),
             ("We look at the site", "Chris checks the line, the grade and where the gates go, and goes over materials with you."),
             ("Get your price, then the build", "You get a written quote. Once you approve it, your fence goes on the schedule.")]
    st = GR("es-st", [FX(f"es-s{i}", [P(f"es-s{i}-n", f"Step {i+1}", EYEBROW), H(f"es-s{i}-h", a, "h3", "font-size: 1.45rem; line-height: 1.1;"), P(f"es-s{i}-p", b, f"font-family: {BODY}; font-size: 1.0625rem; line-height: 1.6; color: {MUTED};")],
                            f"flex-direction: column; gap: 0.6rem; padding-block-start: 1.5rem; border-style: solid; border-color: {COPPER_D}; border-width: 3px 0px 0px 0px; min-width: 0px;") for i, (a, b) in enumerate(steps)],
            "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; gap: 1.5rem; column-gap: 2.5rem; margin-block-end: 4rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); }")
    copy = FX("es-copy", [H("es-h", "Get a free estimate", "h2", H2), P("es-ld", "A few details and a rough idea of the footage is all Chris needs to get started.", LEDE),
                          FX("es-fbw", [BTN("es-fb", "Message on Facebook ↗", FB, kind="ghost", blank=True)], "")], "flex-direction: column; gap: 1.4rem; min-width: 0px;")
    LBL = f"font-family: {TAG}; font-weight: 500; font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: {MUTED};"
    BOX = f"font-family: {BODY}; font-size: 1rem; line-height: 1.4; color: #8A847C; min-height: 48px; padding-block-start: 0.75rem; padding-block-end: 0.75rem; padding-inline-start: 0.85rem; padding-inline-end: 0.85rem; background-color: {PAPER}; border-width: 1.5px; border-style: solid; border-color: {LINE}; border-radius: 3px;"
    def field(cid, label, ph, tall=False):
        return FX(cid, [P(cid + "-l", label, LBL), P(cid + "-f", ph, BOX + (" min-height: 110px;" if tall else ""))], "flex-direction: column; gap: 0.35rem; min-width: 0px;")
    ROW2 = "grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto; gap: 1rem; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; }"
    form = FX("es-form", [
        P("es-tag", "Form preview · nothing here is sent or saved", f"font-family: {TAG}; font-weight: 500; font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: {MUTED}; padding-block-end: 1rem; border-style: dashed; border-color: {LINE}; border-width: 0px 0px 1px 0px;"),
        GR("es-r1", [field("es-name", "Name", "Your name"), field("es-phone", "Phone", "(803) 555-0100")], ROW2),
        field("es-addr", "Job address", "Street, town"),
        GR("es-r2", [field("es-type", "Fence type", "Wood privacy ▾"), field("es-feet", "Rough footage", "e.g. 150 ft")], ROW2),
        field("es-msg", "About the job", "Gates, height, old fence to remove…", True),
        P("es-send", "Request my estimate", f"font-family: {BODY}; font-weight: 600; font-size: 1rem; line-height: 1; text-align: center; color: #FFFFFF; background-color: {COPPER_D}; opacity: 0.5; min-height: 48px; padding-block-start: 1rem; padding-block-end: 1rem; border-radius: 3px;"),
        P("es-demo", "Demo only. This preview doesn't send anything.", f"font-family: {BODY}; font-size: 0.95rem; color: {COPPER_D};"),
    ], f"flex-direction: column; gap: 1rem; background-color: {CARD}; border-width: 1px; border-style: solid; border-color: {LINE}; border-radius: 3px; padding: 2.5rem; min-width: 0px; @media(--mobile) {{ padding: 1.5rem; }}")
    g = GR("es-g", [copy, form], "grid-template-columns: minmax(0,5fr) minmax(0,6fr); grid-template-rows: auto; align-items: start; gap: 2.5rem; column-gap: 4rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; }")
    return SEC("es", "estimate", [HEAD("es-hd", "Getting an estimate", "How a job starts"), st, g])

def band():
    bg = IMG("bd-bg", "hero-wood-privacy.jpg", "", FILL + " opacity: 0.3; object-position: 50% 60%;")
    copy = FX("bd-c", [H("bd-h", "Need a fence up?", "h2", H2 + f" color: {ONDARK};"), P("bd-p", "Tell Chris what you're after and he'll get back to you with a price.", f"font-family: {BODY}; font-size: 1.0625rem; line-height: 1.6; color: {ONDARK_M};")],
              "flex-direction: column; gap: 1rem; min-width: 0px; flex: 1 1 auto;")
    w = FX("bd-w", [copy, BTN("bd-b", "Get a free estimate", "#estimate")], WRAP + " position: relative; gap: 2.5rem; align-items: center; justify-content: space-between; @media(--tablet) { flex-direction: column; align-items: flex-start; }")
    return FX("bd", [bg, w], f"width: 100%; position: relative; overflow: hidden; background-color: {NIGHT}; padding-block-start: 6rem; padding-block-end: 6rem; flex-direction: column; @media(--mobile) {{ padding-block-start: 4rem; padding-block-end: 4rem; }}", tag="section")

def footer():
    FL = f"font-family: {BODY}; font-size: 0.95rem; color: {ONDARK}; text-decoration: none; &:hover {{ color: {COPPER}; }}"
    def lk(cid, t, d, blank=False): return P(cid, t, FL, link=L(d, blank))
    EB = EYEBROW.replace(COPPER_D, COPPER)
    g = GR("fo-g", [
        FX("fo-a", [FX("fo-br", [IMG("fo-logo", "logo-facebook.jpg", "", "width: 64px; height: 64px; object-fit: cover; border-radius: 50%; display: block;"), BRAND("fo-nm")], "gap: 0.9rem; align-items: center;"),
                    P("fo-desc", "Wood, vinyl, metal and chain link fences, gates and arbors. Based in Columbia, South Carolina.", f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.6; color: {ONDARK_M}; max-width: 46ch;")],
           "flex-direction: column; gap: 1rem; min-width: 0px; @media(--tablet) { grid-column: 1 / -1; }"),
        FX("fo-b", [P("fo-b-h", "On this page", EB), lk("fo-b1", "Our Work", "#work"), lk("fo-b2", "Fence Types", "#types"), lk("fo-b3", "About", "#about"), lk("fo-b4", "Free estimate", "#estimate")], "flex-direction: column; gap: 0.5rem; min-width: 0px;"),
        FX("fo-c", [P("fo-c-h", "Follow", EB), lk("fo-c1", "Facebook ↗", FB, True), lk("fo-c3", "Back to top ↑", "#top")], "flex-direction: column; gap: 0.5rem; min-width: 0px;"),
    ], "grid-template-columns: minmax(0,2fr) minmax(0,1fr) minmax(0,1fr); grid-template-rows: auto; gap: 2.5rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; }")
    fine = P("fo-fine", "Website concept by Axiom Systems. Demo only.", f"font-family: {TAG}; font-size: 0.78rem; color: {ONDARK_M}; margin-block-start: 2.5rem; padding-block-start: 1.5rem; border-style: solid; border-color: #3A342E; border-width: 1px 0px 0px 0px;")
    return FX("fo", [FX("fo-w", [g, fine], WRAP + " flex-direction: column;")],
              f"width: 100%; background-color: {NIGHT2}; padding-block-start: 4rem; padding-block-end: 4rem; flex-direction: column; @media(--tablet) {{ padding-block-end: 8.5rem; }}", tag="footer")

def mobilebar():
    A = f"flex: 1 1 0px; min-height: 54px; display: flex; align-items: center; justify-content: center; font-family: {BODY}; font-weight: 600; font-size: 1rem; text-decoration: none; border-radius: 0px; border-width: 0px; padding: 0px; {FOCUS}"
    return FX("mb", [BTN("mb-1", "See our work", "#work", css=A + f" color: {ONDARK}; background-color: {NIGHT2}; &:hover {{ color: {COPPER}; background-color: {NIGHT2}; }}"),
                     BTN("mb-2", "Free estimate", "#estimate", css=A)],
              # right padding keeps the site chat bubble (58px, 20px from the edge) beside the buttons
              f"display: none; position: fixed; inset-inline-start: 0px; inset-inline-end: 0px; inset-block-end: 0px; z-index: 30; flex-direction: row; gap: 6px; padding: 6px; background-color: {NIGHT}; @media(--tablet) {{ display: flex; padding-inline-end: 84px; }}", tag="nav")

def root():
    return FX("afs", [header(), hero(), spec(), featured(), types(), gallery(), owner(), estimate(), band(), footer(), mobilebar()],
              f"width: 100%; max-width: 100%; flex-direction: column; gap: 0px; background-color: {PAPER}; color: {INK};")

if __name__ == "__main__":
    r = root()
    # gallery tiles go in separate calls: strip them from the skeleton
    tiles = {}
    def strip(n):
        for c in n.kids:
            if c.cls == ["afs-gallery"]: tiles[c.cid] = c.kids; c.kids = []
            else: strip(c)
    strip(r)
    json.dump(payload(r), open(os.path.join(HERE, "call-page.json"), "w"), ensure_ascii=False)
    for cid, ts in tiles.items():
        ps = [payload(t) for t in ts]; cfg, cl = {}, {}
        for p in ps: cfg.update(p["element_config"]); cl.update(p.get("classes", {}))
        json.dump({"xml_structure": "".join(p["xml_structure"] for p in ps), "element_config": cfg, "classes": cl}, open(os.path.join(HERE, f"call-{cid}.json"), "w"), ensure_ascii=False)
    json.dump({k: bgen.norm(v) for k, v in CLASSES.items()}, open(os.path.join(HERE, "classes.json"), "w"), ensure_ascii=False, indent=1)
    print("page", len(json.dumps(payload(r))), {k: len(v) for k, v in tiles.items()})
