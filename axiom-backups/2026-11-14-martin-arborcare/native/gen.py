"""Elementor V4 build payloads for the Martin Arborcare demo (axiomsystems.systems page 2057).
Native port of the approved local draft (../site/index.html): same copy, palette, photos and sections.
The page snippet (../snippet/main.php) adds the demo estimate form (#ma-form), service preselect, heading accents,
the header colour, the sticky fix and the phone bar logic.
Reuses the build helpers (N, payload, L) from the Branham generator, like every demo since Fence It Up."""
import importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("bgen", os.path.join(HERE, "..", "..", "2026-11-08-branham-demo", "native", "gen.py"))
bgen = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(bgen)
N, payload, L = bgen.N, bgen.payload, bgen.L
MEDIA = json.load(open(os.path.join(HERE, "media-ids.json")))
def mid(slug): return MEDIA[f"martin-demo-{slug}.jpg"]["id"]

FOREST, FOREST2, DEEP, LEAF, LEAF_B, LEAF_INK = "#123b24", "#1b5232", "#0b2416", "#7cc142", "#8fd352", "#2f6b12"
CREAM, PAPER, INK, MUTED, LINE, GOLD = "#f7f5ee", "#ffffff", "#18241c", "#56635a", "#dfe3d8", "#e8b44a"
ONDARK, ONDARK_M = "#ffffff", "#cfe0c8"
DISP, BODY = '"Barlow Condensed"', '"Figtree"'
PHONE, TEL, MAIL = "(727) 455-2245", "tel:+17274552245", "martinarborcare@gmail.com"
FB = "https://www.facebook.com/MartinArborcareLLC"
EST = "#estimate-form"
FOCUS = f"&:focus {{ outline-width: 3px; outline-color: {LEAF}; outline-style: solid; outline-offset: 3px; }}"
SHADOW = "box-shadow: 0px 10px 30px 0px rgba(18,59,36,0.12);"

def P(cid, text, css="", tag="p", link=None):
    c = {"paragraph": text, "tag": tag}
    if link: c["link"] = link
    return N("e-paragraph", cid, c, "display: block; margin: 0px; " + css)
def H(cid, text, tag, css=""):
    return N("e-heading", cid, {"title": text, "tag": tag},
             f"display: block; margin: 0px; font-family: {DISP}; font-weight: 700; line-height: 1.02; letter-spacing: 0.01em; color: {FOREST}; " + css)
def BTN(cid, text, dest, kind="leaf", css="", blank=False):
    base = (f"font-family: {BODY}; font-weight: 600; font-size: 1rem; line-height: 1; text-decoration: none; text-align: center; "
            f"min-height: 52px; padding-block-start: 0.9rem; padding-block-end: 0.9rem; padding-inline-start: 1.5rem; padding-inline-end: 1.5rem; "
            f"border-radius: 999px; border-width: 2px; border-style: solid; display: inline-flex; align-items: center; justify-content: center; transition: background-color 0.15s, color 0.15s; {FOCUS} ")
    base += {
        "leaf": f"color: #0e2a17; background-color: {LEAF}; border-color: {LEAF}; &:hover {{ background-color: {LEAF_B}; border-color: {LEAF_B}; color: #0e2a17; }} ",
        "ghost": f"color: {ONDARK}; background-color: rgba(0,0,0,0.15); border-color: rgba(255,255,255,0.7); &:hover {{ background-color: rgba(255,255,255,0.14); color: {ONDARK}; }} ",
        "white": f"color: {FOREST}; background-color: #ffffff; border-color: #ffffff; &:hover {{ background-color: #eef3ea; color: {FOREST}; }} ",
    }[kind]
    return N("e-button", cid, {"text": text, "link": L(dest, blank)}, base + css)
def FX(cid, kids, css="", **cfg): return N("e-flexbox", cid, cfg or None, "padding: 0px; " + css, kids)
def DV(cid, kids, css="", **cfg): return N("e-div-block", cid, cfg or None, "padding: 0px; min-width: 0px; " + css, kids)
def GR(cid, kids, css="", **cfg): return N("e-grid", cid, cfg or None, "padding: 0px; " + css, kids)
def IMG(cid, slug, css="", size="full"):
    return N("e-image", cid, {"image": {"src": {"id": mid(slug)}, "size": size}}, css)
FILL = "position: absolute; inset: 0px; width: 100%; height: 100%; object-fit: cover; display: block;"

WRAP = "width: 100%; max-width: 1180px; margin-inline-start: auto; margin-inline-end: auto; padding-inline-start: 32px; padding-inline-end: 32px; @media(--mobile) { padding-inline-start: 16px; padding-inline-end: 16px; }"
LEDE = f"font-family: {BODY}; font-size: 1.06rem; line-height: 1.6; color: {MUTED}; max-width: 640px;"
H2 = "font-size: 3.2rem; @media(--tablet) { font-size: 2.7rem; } @media(--mobile) { font-size: 2.15rem; }"
EB = f"font-family: {BODY}; font-weight: 600; font-size: 0.86rem; line-height: 1; letter-spacing: 0.14em; text-transform: uppercase; color: {LEAF_INK};"
def SEC(cid, anchor, kids, css=""):
    n = FX(cid, [FX(cid + "-w", kids, WRAP + " flex-direction: column; gap: 0px;")],
           f"width: 100%; background-color: {CREAM}; padding-block-start: 6.5rem; padding-block-end: 6.5rem; flex-direction: column; scroll-margin-top: 80px; @media(--tablet) {{ padding-block-start: 4.5rem; padding-block-end: 4.5rem; }} @media(--mobile) {{ padding-block-start: 3.75rem; padding-block-end: 3.75rem; }} " + css, tag="section")
    if anchor: n.cfg["_cssid"] = anchor
    return n
def HEAD(cid, eb, title, lede=None, dark=False, right=None):
    left = [P(cid + "-eb", eb, EB + (f" color: {LEAF};" if dark else "")), H(cid + "-h", title, "h2", H2 + (f" color: {ONDARK};" if dark else ""))]
    if lede: left.append(P(cid + "-ld", lede, LEDE + (f" color: {ONDARK_M};" if dark else "") + " margin-block-start: 0.4rem;"))
    kids = [FX(cid + "-l", left, "flex-direction: column; gap: 0.75rem; min-width: 0px; flex: 1 1 auto;")]
    if right: kids.append(right)
    return FX(cid, kids, "flex-direction: row; gap: 1.5rem; align-items: flex-end; justify-content: space-between; flex-wrap: wrap; margin-block-end: 2.5rem; @media(--mobile) { margin-block-end: 1.75rem; }")

# ---------- ribbon + header ----------
def ribbon():
    T = f"font-family: {BODY}; font-size: 0.82rem; line-height: 1.35; color: #cfe3c4; text-align: center;"
    return FX("rb", [P("rb-t", f"<strong>Website concept by Axiom Systems</strong>, prepared for Martin Arborcare. Not their live site; photos are from the Martin Arborcare Facebook page.", T + " @media(--mobile) { display: none; }"),
                     P("rb-m", f"<strong>Website concept by Axiom Systems.</strong> Not Martin Arborcare’s live site.", T + " display: none; font-size: 0.76rem; @media(--mobile) { display: block; }")],
              f"width: 100%; justify-content: center; background-color: {DEEP}; padding-block-start: 8px; padding-block-end: 8px; padding-inline-start: 16px; padding-inline-end: 16px;", _cssid="ma-ribbon")

NAV = [("Services", "#services"), ("Our Work", "#work"), ("Reviews", "#reviews"), ("About", "#about")]
def header():
    brand = FX("hd-brand", [IMG("hd-logo", "logo", "width: 48px; height: 48px; border-radius: 50%; object-fit: cover; flex: none; box-shadow: 0px 0px 0px 2px rgba(255,255,255,0.25);"),
                            FX("hd-bt", [P("hd-b1", "MARTIN ARBORCARE", f"font-family: {DISP}; font-weight: 700; font-size: 1.55rem; line-height: 1; letter-spacing: 0.02em; color: {ONDARK}; @media(--mobile) {{ font-size: 1.35rem; }}", tag="span"),
                                         P("hd-b2", "Tree &amp; Landscape", f"font-family: {BODY}; font-weight: 500; font-size: 0.68rem; line-height: 1.2; letter-spacing: 0.16em; text-transform: uppercase; color: {LEAF};", tag="span")],
                               "flex-direction: column; gap: 3px;")],
                f"width: auto; align-items: center; gap: 12px; text-decoration: none; margin-inline-end: auto; {FOCUS}", tag="a", link=L("#top"))
    links = [P(f"hd-n{i}", t, f"font-family: {BODY}; font-weight: 500; font-size: 0.95rem; color: #e2ecdc; text-decoration: none; &:hover {{ color: {ONDARK}; }} {FOCUS}", tag="span", link=L(d)) for i, (t, d) in enumerate(NAV)]
    nav = FX("hd-nav", links, "width: auto; gap: 1.6rem; align-items: center; @media(--tablet) { display: none; }", tag="nav")
    call = P("hd-call", PHONE, f"font-family: {BODY}; font-weight: 600; font-size: 1rem; color: {ONDARK}; text-decoration: none; white-space: nowrap; {FOCUS} @media(--tablet) {{ display: none; }}", tag="span", link=L(TEL))
    cta = BTN("hd-cta", "Free Estimate", EST, css="min-height: 44px; padding-inline-start: 1.1rem; padding-inline-end: 1.1rem; font-size: 0.95rem; flex: none; @media(--mobile) { display: none; }")
    inner = FX("hd-in", [brand, nav, call, cta], WRAP + " gap: 1.4rem; align-items: center; min-height: 72px; @media(--mobile) { min-height: 64px; }")
    h = FX("hd", [inner], f"width: 100%; position: sticky; inset-block-start: 0px; z-index: 50; background-color: rgba(18,59,36,0.96); backdrop-filter: blur(8px); justify-content: center;", tag="header")
    h.cfg["_cssid"] = "top"; return h

# ---------- hero ----------
CHECK = "✓"
def hero():
    shade = DV("hr-sh", [], "position: absolute; inset: 0px; z-index: 1; background-image: linear-gradient(180deg, rgba(8,28,16,0.45) 0%, rgba(8,28,16,0.35) 35%, rgba(8,28,16,0.9) 100%), linear-gradient(90deg, rgba(8,28,16,0.6) 0%, rgba(8,28,16,0) 75%); @media(--mobile) { background-image: linear-gradient(180deg, rgba(8,28,16,0.62) 0%, rgba(8,28,16,0.72) 50%, rgba(8,28,16,0.92) 100%); }")
    h1 = H("hr-h1", "Tree care &amp; landscapes, <em>done right.</em>", "h1",
           f"color: {ONDARK}; font-size: 5.6rem; line-height: 0.98; text-transform: uppercase; max-width: 880px; @media(--tablet) {{ font-size: 4.4rem; }} @media(--mobile) {{ font-size: 3rem; }}")
    sub = P("hr-ld", "Trimming, removals and storm cleanup led by an ISA Certified Arborist, plus pavers, turf, lighting and landscaping that make the whole yard come together.",
            f"font-family: {BODY}; font-size: 1.2rem; line-height: 1.55; color: #e6efe1; max-width: 620px; @media(--mobile) {{ font-size: 1.04rem; }}")
    act = FX("hr-act", [BTN("hr-b1", "Get a Free Estimate", EST, css="@media(--mobile) { width: 100%; }"),
                        BTN("hr-b2", f"Call {PHONE}", TEL, kind="ghost", css="@media(--mobile) { width: 100%; }")],
             "flex-wrap: wrap; gap: 0.75rem; margin-block-start: 0.6rem; @media(--mobile) { flex-direction: column; gap: 0.6rem; }")
    act.cfg = {"_cssid": "hero-ctas"}
    chips = FX("hr-chips", [P(f"hr-c{i}", f"<b>{CHECK}</b>&nbsp; {t}", f"font-family: {BODY}; font-size: 0.95rem; color: #e6efe1;", tag="span")
                            for i, t in enumerate(["ISA Certified Arborist", "Licensed &amp; insured", "Family owned since 2017", "100% recommend · 37 Facebook reviews"])],
               "flex-wrap: wrap; gap: 0.9rem; margin-block-start: 1.6rem;")
    copy = FX("hr-copy", [P("hr-eb", "St. Petersburg · Pinellas County, FL", EB + f" color: {LEAF};"), h1, sub, act, chips], "flex-direction: column; gap: 1.1rem;")
    wrap = FX("hr-w", [copy], WRAP + " position: relative; z-index: 2; flex-direction: column; padding-block-start: 8rem; padding-block-end: 4rem; @media(--mobile) { padding-block-start: 4.5rem; padding-block-end: 3rem; }")
    n = FX("hr", [IMG("hr-img", "waterfront-paver-garden", FILL + " object-position: 50% 60%; z-index: 0;"), shade, wrap],
           f"position: relative; width: 100%; min-height: 760px; overflow: hidden; flex-direction: column; justify-content: flex-end; background-color: {FOREST}; @media(--tablet) {{ min-height: 640px; }} @media(--mobile) {{ min-height: 0px; }}", tag="section")
    n.cfg["_cssid"] = "hero"; return n

# ---------- services ----------
SERVICES = [("Tree Trimming &amp; Removal", "Pruning, crown work and safe removals of big trees in tight spaces, by climb, lift or crane.", "norfolk-pine-climb", "50% 30%", "Tree service estimate"),
            ("Tree Health &amp; Cabling", "Certified-arborist care: cabling and bracing, insect and disease management, and honest advice on what to save.", "bucket-lift-pine", "50% 35%", "Arborist visit"),
            ("Storm &amp; Emergency Cleanup", "When storms hit, we stay in town for our neighbors. Downed trees, roof and fence hits, and full debris haul-off.", "storm-tree-on-cars", "50% 50%", "Storm help"),
            ("Pavers &amp; Paver Sealing", "Walkways, patios and driveways, pitched to drain, plus cleaning, re-sanding and sealing.", "paver-side-walk", "50% 55%", "Paver estimate"),
            ("Artificial Turf", "Green all year, pet and kid friendly, no mowing and no watering. Side yards, backyards and putting greens.", "artificial-turf-side-yard", "50% 60%", "Turf estimate"),
            ("Landscaping &amp; Lighting", "New beds, sod, palms and plants, finished with path lights and uplighting that shows it all off at night.", "night-landscape-lighting", "50% 45%", "Landscape estimate")]
def services():
    cards = []
    for i, (t, d, img, pos, cta) in enumerate(SERVICES):
        ph = DV(f"sv{i}-ph", [IMG(f"sv{i}-i", img, FILL + f" object-position: {pos}; transition: transform 0.5s; &:hover {{ transform: scale(1.04); }}", size="large")],
                "position: relative; overflow: hidden; aspect-ratio: 4 / 3; width: 100%; background-color: #dfe6da; flex: none;")
        q = P(f"sv{i}-q", cta + " →", f"font-family: {BODY}; font-weight: 600; font-size: 0.98rem; color: {LEAF_INK}; text-decoration: none; margin-block-start: auto; padding-block-start: 0.5rem; align-self: flex-start; width: auto; &:hover {{ text-decoration: underline; }} {FOCUS}", tag="span", link=L(EST))
        q.cfg["_cssid"] = f"q-{i + 1}"
        body = FX(f"sv{i}-b", [H(f"sv{i}-h", t, "h3", "font-size: 1.9rem;"),
                               P(f"sv{i}-p", d, f"font-family: {BODY}; font-size: 1rem; line-height: 1.55; color: {MUTED};"), q],
                  "flex-direction: column; gap: 0.5rem; padding: 1.4rem; padding-block-end: 1.5rem; flex: 1 1 auto;")
        cards.append(FX(f"sv{i}", [ph, body], f"flex-direction: column; background-color: {PAPER}; border-radius: 14px; overflow: hidden; {SHADOW} min-width: 0px;"))
    g = GR("sv-g", cards, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto auto; gap: 1.4rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(3, auto); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(6, auto); gap: 1rem; }")
    also = P("sv-also", f"<strong>Also:</strong> stump grinding · lot clearing · lawn care · pressure washing · solar-panel tree clearance.", f"font-family: {BODY}; font-size: 1rem; color: {MUTED}; margin-block-start: 1.75rem;")
    return SEC("sv", "services", [HEAD("sv-hd", "What we do", "From the canopy to <em>the curb</em>", "One local crew for the trees and everything under them, so you’re not juggling three contractors."), g, also])

# ---------- before / after ----------
def beforeafter():
    figs = []
    for i, (slug, lab, alt_bg) in enumerate([("front-yard-before", "Before", "rgba(8,28,16,0.82)"), ("front-yard-after-lighting", "After", LEAF)]):
        figs.append(DV(f"ba{i}", [IMG(f"ba{i}-i", slug, FILL, size="large"),
                                  P(f"ba{i}-l", lab, f"position: absolute; inset-block-start: 14px; inset-inline-start: 14px; font-family: {DISP}; font-weight: 700; font-size: 1.1rem; line-height: 1; letter-spacing: 0.12em; text-transform: uppercase; color: {'#0e2a17' if i else ONDARK}; background-color: {alt_bg}; padding-block-start: 9px; padding-block-end: 9px; padding-inline-start: 14px; padding-inline-end: 14px; border-radius: 999px;", tag="span")],
                       f"position: relative; overflow: hidden; border-radius: 14px; aspect-ratio: 4 / 3; background-color: {FOREST2};"))
    g = GR("ba-g", figs, "grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto; gap: 1.1rem; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; }")
    return SEC("ba", "before-after", [HEAD("ba-hd", "Before &amp; after · St. Pete", "Same house. <em>One project.</em>", "A bare front yard turned into planted beds, a lit walkway and an uplit palm.", dark=True), g],
               f"background-color: {FOREST};")

# ---------- gallery ----------
GAL = [("waterfront-paver-path", "Waterfront paver path &amp; plantings", "50% 60%"), ("pine-lift-work", "Pine trimming from the lift", "50% 40%"),
       ("paver-courtyard-plants", "Paver courtyard", "50% 60%"), ("turf-backyard", "Artificial turf backyard", "50% 60%"),
       ("storm-damaged-oak", "Storm-damaged tree, Sept 2024", "50% 35%"), ("paver-driveway", "Paver driveway", "50% 70%"),
       ("paver-garden-walk", "Garden walk", "50% 60%"), ("crane-truck-palm", "Crane work on a tall palm", "50% 45%"),
       ("paver-patio", "Paver patio", "50% 60%")]
def gallery():
    tiles = []
    for i, (slug, cap, pos) in enumerate(GAL):
        span = " grid-column: span 2; grid-row: span 2; @media(--mobile) { grid-column: span 2; grid-row: auto; }" if i in (0,) else ""
        tiles.append(DV(f"g{i:02d}", [IMG(f"g{i:02d}-i", slug, FILL + f" object-position: {pos}; transition: transform 0.4s; &:hover {{ transform: scale(1.04); }}", size="large"),
                                      P(f"g{i:02d}-c", cap, f"position: absolute; inset-inline-start: 0px; inset-inline-end: 0px; inset-block-end: 0px; padding-block-start: 2rem; padding-block-end: 0.7rem; padding-inline-start: 0.85rem; padding-inline-end: 0.85rem; font-family: {BODY}; font-weight: 600; font-size: 0.88rem; line-height: 1.25; color: {ONDARK}; background-image: linear-gradient(180deg, rgba(8,28,16,0) 0%, rgba(8,28,16,0.85) 100%); @media(--mobile) {{ font-size: 0.78rem; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; }}")],
                        f"position: relative; overflow: hidden; border-radius: 12px; aspect-ratio: 1 / 1; background-color: #dfe6da;{span}"))
    tiles[0].css = tiles[0].css.replace("aspect-ratio: 1 / 1;", "aspect-ratio: auto; min-height: 100%; @media(--mobile) { aspect-ratio: 4 / 3; }")
    g = GR("gl-g", tiles, "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: repeat(3, auto); gap: 0.9rem; @media(--tablet) { grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: repeat(4, auto); } @media(--mobile) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(5, auto); gap: 0.55rem; }")
    return SEC("gl", "work", [HEAD("gl-hd", "Our work", "Recent projects around <em>Pinellas</em>", right=BTN("gl-b", "Start your project", EST)), g])

# ---------- reviews (real Facebook recommendations, first name + last initial) ----------
REVIEWS = [("They gave me a reasonable quote, arrived on time, quickly removed my 45-foot Norfolk pine which had been struck by lightning. They were friendly, professional and hard working.", "Bit S.", "March 2026"),
           ("I have trusted Martin Arborcare for years across multiple homes, and their tree work is truly exceptional. Joe is a master of his craft… I wouldn’t trust anyone else with my trees!", "Heather M.", "January 2025"),
           ("This family-owned business is truly impressive. The team was professional, hardworking, and completed the tree service at my home quickly and efficiently.", "Nicole S.", "July 2025"),
           ("I had reached out to several companies for quotes on a tree removal and trimming. They were the only ones to respond right away… The pricing was great, would definitely recommend!", "Kaitlin P.", "May 2021")]
def reviews():
    score = FX("rv-score", [P("rv-sb", "100%", f"font-family: {DISP}; font-weight: 700; font-size: 3.3rem; line-height: 1; color: {FOREST};"),
                            P("rv-st", "recommend<br>37 reviews on Facebook", f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.35; color: {MUTED};")],
               "width: auto; align-items: center; gap: 0.9rem;")
    qs = [FX(f"rv{i}", [P(f"rv{i}-q", f"“{q}”", f"font-family: {BODY}; font-size: 1.06rem; line-height: 1.6; color: {INK};"),
                        P(f"rv{i}-a", f"<strong>{who}</strong> · {when}", f"font-family: {BODY}; font-size: 0.9rem; color: {MUTED};")],
             f"flex-direction: column; gap: 1rem; padding: 1.75rem; background-color: {CREAM}; border-radius: 14px; border-width: 0px 0px 0px 5px; border-style: solid; border-color: {LEAF}; min-width: 0px;")
          for i, (q, who, when) in enumerate(REVIEWS)]
    g = GR("rv-g", qs, "grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; gap: 1.4rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(4, auto); }")
    return SEC("rv", "reviews", [HEAD("rv-hd", "Reviews", "Neighbors who’d <em>hire us again</em>", right=score), g], f"background-color: {PAPER};")

# ---------- about ----------
CREDS = [("ISA Certified", "Arborist #FL-9184A, Joseph Martin"), ("Licensed &amp; Insured", "Tree service &amp; landscaping"), ("Since 2017", "Serving Pinellas County"), ("Free Estimates", "Call, text or request online")]
def about():
    ph = DV("ab-ph", [IMG("ab-i", "lift-banyan-truck", FILL + " object-position: 50% 50%;", size="large")],
            f"position: relative; overflow: hidden; border-radius: 14px; aspect-ratio: 4 / 5; {SHADOW} @media(--tablet) {{ aspect-ratio: 4 / 3; }}")
    creds = GR("ab-cr", [FX(f"ab-c{i}", [P(f"ab-c{i}-b", b, f"font-family: {DISP}; font-weight: 700; font-size: 1.45rem; line-height: 1.1; color: {FOREST};"),
                                         P(f"ab-c{i}-s", s, f"font-family: {BODY}; font-size: 0.9rem; color: {MUTED};")],
                            f"flex-direction: column; gap: 0.2rem; padding-block-start: 1rem; padding-block-end: 1rem; padding-inline-start: 1.1rem; padding-inline-end: 1.1rem; background-color: {PAPER}; border-width: 1px; border-style: solid; border-color: {LINE}; border-radius: 12px; min-width: 0px;")
                         for i, (b, s) in enumerate(CREDS)],
                 "grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; gap: 0.85rem; margin-block-start: 1.6rem; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(4, auto); }")
    copy = FX("ab-copy", [P("ab-eb", "About us", EB), H("ab-h", "A family business that treats your property <em>like our own</em>", "h2", H2),
                          P("ab-p", "Martin Arborcare is run by Joe and Stephanie Martin in St. Petersburg. Joe is an ISA Certified Arborist, so the decisions about your trees come from someone trained in tree health, not just a chainsaw. When hurricanes come through, we stay in town and help our neighbors dig out.", LEDE + " margin-block-start: 0.5rem;"),
                          creds,
                          P("ab-area", f"<strong>Service area:</strong> St. Petersburg · Gulfport · Shore Acres · Pinellas Park · Clearwater · Palm Harbor · Tarpon Springs · Tampa · all of Pinellas County", f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.6; color: {MUTED}; margin-block-start: 1.5rem;")],
              "flex-direction: column; gap: 0.75rem; min-width: 0px;")
    g = GR("ab-g", [ph, copy], "grid-template-columns: minmax(0,1fr) minmax(0,1.15fr); grid-template-rows: auto; gap: 3.5rem; align-items: center; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2rem; }")
    return SEC("ab", "about", [g])

# ---------- estimate (form mount #ma-form, rendered by the snippet) ----------
def estimate():
    LK = f"font-family: {BODY}; font-weight: 600; font-size: 1.2rem; color: {ONDARK}; text-decoration: none; &:hover {{ color: {LEAF}; }} {FOCUS}"
    SM = f"font-family: {BODY}; font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; color: {LEAF};"
    copy = FX("es-copy", [P("es-eb", "Free estimate", EB + f" color: {LEAF};"), H("es-h", "Tell us about <em>your yard</em>", "h2", H2 + f" color: {ONDARK};"),
                          P("es-p", "Send a few details and we’ll reach out to set up a time to look at it. Prefer to talk? Call or text Joe directly.", LEDE + f" color: {ONDARK_M};"),
                          FX("es-ct", [P("es-tk", "Call or text", SM), P("es-tel", PHONE, LK + " font-size: 1.5rem;", link=L(TEL)),
                                       P("es-mk", "Email", SM + " margin-block-start: 0.8rem;"), P("es-mail", MAIL, LK + " font-size: 1.1rem; overflow-wrap: anywhere;", link=L("mailto:" + MAIL))],
                             "flex-direction: column; gap: 0.3rem; margin-block-start: 1rem;"),
                          P("es-fin", "<strong>Financing available.</strong> Bigger landscape projects can be split into payments with Affirm (buy now, pay later).",
                            f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.55; color: #dbe8d4; margin-block-start: 1.4rem; padding-block-start: 1rem; padding-block-end: 1rem; padding-inline-start: 1.1rem; padding-inline-end: 1.1rem; border-width: 1px; border-style: dashed; border-color: rgba(255,255,255,0.35); border-radius: 12px;")],
              "flex-direction: column; gap: 0.75rem; min-width: 0px;")
    mount = DV("es-form", [P("es-fb", f"The estimate form is loading. You can also call {PHONE}.", f"font-family: {BODY}; font-size: 1rem; color: {MUTED};")], "min-height: 200px;")
    mount.cfg = {"_cssid": "ma-form"}
    card = FX("es-card", [H("es-ch", "Request an estimate", "h3", "font-size: 2rem;"),
                          P("es-cs", "Takes about a minute.", f"font-family: {BODY}; font-size: 0.95rem; color: {MUTED}; margin-block-end: 0.8rem;"), mount],
              f"flex-direction: column; gap: 0.3rem; padding: 1.9rem; background-color: {PAPER}; border-radius: 18px; box-shadow: 0px 20px 50px 0px rgba(0,0,0,0.25); min-width: 0px; scroll-margin-top: 88px; @media(--tablet) {{ order: -1; }} @media(--mobile) {{ padding: 1.25rem; scroll-margin-top: 76px; }}")
    card.cfg = {"_cssid": "estimate-form"}
    g = GR("es-g", [copy, card], "grid-template-columns: minmax(0,0.9fr) minmax(0,1.1fr); grid-template-rows: auto; gap: 3.5rem; align-items: start; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2.25rem; }")
    return SEC("es", "estimate", [g], f"background-image: linear-gradient(180deg, {FOREST} 0%, #0d2c1a 100%);")

# ---------- footer + phone bar ----------
def footer():
    T = f"font-family: {BODY}; font-size: 0.92rem; line-height: 1.6; color: #b9ccb1;"
    LK = f"font-family: {BODY}; font-size: 0.92rem; color: #e2ecdc; text-decoration: none; &:hover {{ color: {LEAF}; }} {FOCUS}"
    row = FX("fo-r", [P("fo-a", "<strong>Martin Arborcare, LLC</strong> · Tree &amp; Landscape · St. Petersburg, FL 33714", T),
                      FX("fo-l", [P("fo-tel", PHONE, LK, link=L(TEL)), P("fo-em", MAIL, LK, link=L("mailto:" + MAIL)), P("fo-fb", "Facebook ↗", LK, link=L(FB, True))],
                         "width: auto; gap: 1.2rem; flex-wrap: wrap;")],
             "flex-wrap: wrap; gap: 1.25rem; justify-content: space-between; align-items: center;")
    fine = P("fo-fine", "<strong>Demo notice.</strong> This page is a website concept prepared by Axiom Systems for Martin Arborcare, LLC and is not their official site. Contact details, services and reviews come from the Martin Arborcare Facebook page, and the photographs are from their own posts. The estimate form is a demonstration and sends nothing.",
             T + " font-size: 0.8rem; max-width: 110ch; margin-block-start: 1.5rem; padding-block-start: 1.25rem; border-width: 1px 0px 0px 0px; border-style: solid; border-color: rgba(255,255,255,0.14);")
    return FX("fo", [FX("fo-w", [row, fine], WRAP + " flex-direction: column;")],
              f"width: 100%; background-color: {DEEP}; padding-block-start: 2.75rem; padding-block-end: 2.5rem; flex-direction: column; @media(--tablet) {{ padding-block-end: 6.5rem; }}", tag="footer")

def mobilebar():
    # Ends 84px short of the right edge so the site chat bubble keeps its corner (same fix as Fence It Up / Comer's).
    return FX("mb", [BTN("mb-call", "Call", TEL, kind="white", css="flex: 1 1 0px; min-height: 50px; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; font-size: 0.95rem;"),
                     BTN("mb-q", "Free Estimate", EST, css="flex: 1.5 1 0px; min-height: 50px; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; font-size: 0.95rem;")],
              f"display: none; position: fixed; width: auto; inset-inline-start: 0px; inset-inline-end: 84px; inset-block-end: 0px; z-index: 100000000; flex-direction: row; gap: 8px; padding: 8px; background-color: rgba(11,36,22,0.96); backdrop-filter: blur(10px); border-radius: 0px 14px 0px 0px; @media(--tablet) {{ display: flex; }}", tag="nav", _cssid="ma-bar")

SECTIONS = [ribbon, header, hero, services, beforeafter, gallery, reviews, about, estimate, footer, mobilebar]
if __name__ == "__main__":
    kids = [f() for f in SECTIONS]
    root = N("e-flexbox", "ma", None, f"padding: 0px; width: 100%; max-width: 100%; flex-direction: column; gap: 0px; background-color: {CREAM}; color: {INK}; font-family: {BODY};", kids)
    p = payload(root)
    json.dump(p, open(os.path.join(HERE, "ALL.json"), "w"), ensure_ascii=False); print("ALL", len(json.dumps(p, ensure_ascii=False)))
