"""Elementor V4 build payloads for the Miracle Painting demo (axiomsystems.systems page 2118).
Native port of the approved local draft (../site/index.html): same copy, palette, photos and sections.
The page snippet (../snippet/main.php) adds the demo estimate form (#mp-form), service preselect, heading accents,
the header colour, the sticky fix and the phone bar logic.
Reuses the build helpers (N, payload, L) from the Branham generator, like every demo since Fence It Up."""
import importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("bgen", os.path.join(HERE, "..", "..", "2026-11-08-branham-demo", "native", "gen.py"))
bgen = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(bgen)
N, payload, L = bgen.N, bgen.payload, bgen.L
MEDIA = json.load(open(os.path.join(HERE, "media-ids.json")))
def mid(slug): return MEDIA[f"miracle-demo-{slug}.jpg"]["id"]

FOREST, FOREST2, DEEP, LEAF, LEAF_B, LEAF_INK = "#10263f", "#1a3b5e", "#0a1b2e", "#f4a62a", "#ffb940", "#94560a"
CREAM, PAPER, INK, MUTED, LINE, GOLD = "#faf7f1", "#ffffff", "#16202c", "#58626e", "#e2dfd6", "#f4a62a"
ONDARK, ONDARK_M = "#ffffff", "#cbd8e8"
DISP, BODY = '"Barlow Condensed"', '"Figtree"'
PHONE, TEL = "(727) 555-0100", "tel:+17275550100"
EST = "#estimate-form"
FOCUS = f"&:focus {{ outline-width: 3px; outline-color: {LEAF}; outline-style: solid; outline-offset: 3px; }}"
SHADOW = "box-shadow: 0px 10px 30px 0px rgba(16,38,63,0.12);"

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
        "leaf": f"color: #241500; background-color: {LEAF}; border-color: {LEAF}; &:hover {{ background-color: {LEAF_B}; border-color: {LEAF_B}; color: #241500; }} ",
        "ghost": f"color: {ONDARK}; background-color: rgba(0,0,0,0.15); border-color: rgba(255,255,255,0.7); &:hover {{ background-color: rgba(255,255,255,0.14); color: {ONDARK}; }} ",
        "white": f"color: {FOREST}; background-color: #ffffff; border-color: #ffffff; &:hover {{ background-color: #fdf1dc; color: {FOREST}; }} ",
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
    T = f"font-family: {BODY}; font-size: 0.82rem; line-height: 1.35; color: #c9d6e6; text-align: center;"
    return FX("rb", [P("rb-t", "<strong>Website concept by Axiom Systems</strong>, prepared for Miracle Painting LLC. Not their live site; photos are from their Google Business listing and the phone number is a placeholder.", T + " @media(--mobile) { display: none; }"),
                     P("rb-m", "<strong>Website concept by Axiom Systems.</strong> Not Miracle Painting’s live site.", T + " display: none; font-size: 0.76rem; @media(--mobile) { display: block; }")],
              f"width: 100%; justify-content: center; background-color: {DEEP}; padding-block-start: 8px; padding-block-end: 8px; padding-inline-start: 16px; padding-inline-end: 16px;", _cssid="mp-ribbon")

NAV = [("Services", "#services"), ("Before &amp; After", "#before-after"), ("Our Work", "#work"), ("About", "#about")]
def header():
    mono = FX("hd-mono", [P("hd-m", "M", f"font-family: {DISP}; font-weight: 700; font-size: 1.9rem; line-height: 1; color: #241500;", tag="span")],
              f"width: 48px; height: 48px; flex: none; border-radius: 50%; background-color: {LEAF}; align-items: center; justify-content: center; box-shadow: 0px 0px 0px 2px rgba(255,255,255,0.25);")
    brand = FX("hd-brand", [mono,
                            FX("hd-bt", [P("hd-b1", "MIRACLE PAINTING", f"font-family: {DISP}; font-weight: 700; font-size: 1.55rem; line-height: 1; letter-spacing: 0.02em; color: {ONDARK}; @media(--mobile) {{ font-size: 1.35rem; }}", tag="span"),
                                         P("hd-b2", "Clearwater, FL", f"font-family: {BODY}; font-weight: 500; font-size: 0.68rem; line-height: 1.2; letter-spacing: 0.16em; text-transform: uppercase; color: {LEAF};", tag="span")],
                               "flex-direction: column; gap: 3px;")],
                f"width: auto; align-items: center; gap: 12px; text-decoration: none; margin-inline-end: auto; {FOCUS}", tag="a", link=L("#top"))
    links = [P(f"hd-n{i}", t, f"font-family: {BODY}; font-weight: 500; font-size: 0.95rem; color: #dde6f1; text-decoration: none; &:hover {{ color: {ONDARK}; }} {FOCUS}", tag="span", link=L(d)) for i, (t, d) in enumerate(NAV)]
    nav = FX("hd-nav", links, "width: auto; gap: 1.6rem; align-items: center; @media(--tablet) { display: none; }", tag="nav")
    call = P("hd-call", PHONE, f"font-family: {BODY}; font-weight: 600; font-size: 1rem; color: {ONDARK}; text-decoration: none; white-space: nowrap; {FOCUS} @media(--tablet) {{ display: none; }}", tag="span", link=L(TEL))
    cta = BTN("hd-cta", "Free Estimate", EST, css="min-height: 44px; padding-inline-start: 1.1rem; padding-inline-end: 1.1rem; font-size: 0.95rem; flex: none; @media(--mobile) { display: none; }")
    inner = FX("hd-in", [brand, nav, call, cta], WRAP + " gap: 1.4rem; align-items: center; min-height: 72px; @media(--mobile) { min-height: 64px; }")
    h = FX("hd", [inner], "width: 100%; position: sticky; inset-block-start: 0px; z-index: 50; background-color: rgba(16,38,63,0.96); backdrop-filter: blur(8px); justify-content: center;", tag="header")
    h.cfg["_cssid"] = "top"; return h

# ---------- hero ----------
CHECK = "✓"
def hero():
    shade = DV("hr-sh", [], "position: absolute; inset: 0px; z-index: 1; background-image: linear-gradient(180deg, rgba(7,20,36,0.5) 0%, rgba(7,20,36,0.4) 35%, rgba(7,20,36,0.9) 100%), linear-gradient(90deg, rgba(7,20,36,0.6) 0%, rgba(7,20,36,0) 75%); @media(--mobile) { background-image: linear-gradient(180deg, rgba(7,20,36,0.66) 0%, rgba(7,20,36,0.76) 50%, rgba(7,20,36,0.93) 100%); }")
    h1 = H("hr-h1", "Paint that makes it look <em>brand new.</em>", "h1",
           f"color: {ONDARK}; font-size: 5.6rem; line-height: 0.98; text-transform: uppercase; max-width: 880px; @media(--tablet) {{ font-size: 4.4rem; }} @media(--mobile) {{ font-size: 3rem; }}")
    sub = P("hr-ld", "Interior and exterior painting for homes and commercial buildings across the Clearwater area: careful prep, clean lines and a finish that holds up to Florida sun.",
            f"font-family: {BODY}; font-size: 1.2rem; line-height: 1.55; color: #e8eef6; max-width: 620px; @media(--mobile) {{ font-size: 1.04rem; }}")
    act = FX("hr-act", [BTN("hr-b1", "Get a Free Estimate", EST, css="@media(--mobile) { width: 100%; }"),
                        BTN("hr-b2", f"Call {PHONE}", TEL, kind="ghost", css="@media(--mobile) { width: 100%; }")],
             "flex-wrap: wrap; gap: 0.75rem; margin-block-start: 0.6rem; @media(--mobile) { flex-direction: column; gap: 0.6rem; }")
    act.cfg = {"_cssid": "hero-ctas"}
    chips = FX("hr-chips", [P(f"hr-c{i}", f"<b>{CHECK}</b>&nbsp; {t}", f"font-family: {BODY}; font-size: 0.95rem; color: #e8eef6;", tag="span")
                            for i, t in enumerate(["Interior &amp; exterior", "Homes &amp; commercial", "Free estimates", "Locally owned in Clearwater"])],
               "flex-wrap: wrap; gap: 0.9rem; margin-block-start: 1.6rem;")
    copy = FX("hr-copy", [P("hr-eb", "Clearwater · Pinellas County, FL", EB + f" color: {LEAF};"), h1, sub, act, chips], "flex-direction: column; gap: 1.1rem;")
    wrap = FX("hr-w", [copy], WRAP + " position: relative; z-index: 2; flex-direction: column; padding-block-start: 8rem; padding-block-end: 4rem; @media(--mobile) { padding-block-start: 4.5rem; padding-block-end: 3rem; }")
    n = FX("hr", [IMG("hr-img", "hero-tan-stucco-home", FILL + " object-position: 50% 55%; z-index: 0;"), shade, wrap],
           f"position: relative; width: 100%; min-height: 760px; overflow: hidden; flex-direction: column; justify-content: flex-end; background-color: {FOREST}; @media(--tablet) {{ min-height: 640px; }} @media(--mobile) {{ min-height: 0px; }}", tag="section")
    n.cfg["_cssid"] = "hero"; return n

# ---------- services ----------
SERVICES = [("Exterior Painting", "Full house repaints with pressure-clean, scrape, caulk and prime, then a coating built for coastal weather.", "exterior-bungalow", "50% 50%", "Exterior estimate"),
            ("Interior Painting", "Walls, ceilings, trim and accent walls, with floors and furniture protected and clean, crisp edges.", "interior-navy-room", "50% 50%", "Interior estimate"),
            ("Commercial Painting", "Offices, warehouses and storefronts, scheduled around your business hours.", "commercial-building", "50% 55%", "Commercial estimate"),
            ("Coastal &amp; Stucco Homes", "Salt, sun and humidity are hard on paint. We prep stucco and wood so the new coat lasts.", "teal-coastal-home", "50% 40%", "Stucco estimate"),
            ("Decks &amp; Outdoor Structures", "Deck staining, railings, pavilions and pergolas, finished to stand up to rain and UV.", "deck-pavilion", "50% 45%", "Deck estimate"),
            ("Doors, Trim &amp; Details", "Front doors, shutters, railings and trim, the small details that make a house pop.", "arched-iron-door", "50% 45%", "Door &amp; trim estimate")]
def services():
    cards = []
    for i, (t, d, img, pos, cta) in enumerate(SERVICES):
        ph = DV(f"sv{i}-ph", [IMG(f"sv{i}-i", img, FILL + f" object-position: {pos}; transition: transform 0.5s; &:hover {{ transform: scale(1.04); }}", size="large")],
                "position: relative; overflow: hidden; aspect-ratio: 4 / 3; width: 100%; background-color: #e3e8ee; flex: none;")
        q = P(f"sv{i}-q", cta + " →", f"font-family: {BODY}; font-weight: 600; font-size: 0.98rem; color: {LEAF_INK}; text-decoration: none; margin-block-start: auto; padding-block-start: 0.5rem; align-self: flex-start; width: auto; &:hover {{ text-decoration: underline; }} {FOCUS}", tag="span", link=L(EST))
        q.cfg["_cssid"] = f"q-{i + 1}"
        body = FX(f"sv{i}-b", [H(f"sv{i}-h", t, "h3", "font-size: 1.9rem;"),
                               P(f"sv{i}-p", d, f"font-family: {BODY}; font-size: 1rem; line-height: 1.55; color: {MUTED};"), q],
                  "flex-direction: column; gap: 0.5rem; padding: 1.4rem; padding-block-end: 1.5rem; flex: 1 1 auto;")
        cards.append(FX(f"sv{i}", [ph, body], f"flex-direction: column; background-color: {PAPER}; border-radius: 14px; overflow: hidden; {SHADOW} min-width: 0px;"))
    g = GR("sv-g", cards, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto auto; gap: 1.4rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(3, auto); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(6, auto); gap: 1rem; }")
    also = P("sv-also", "<strong>Also ask about:</strong> cabinet painting · pressure washing · drywall &amp; popcorn-ceiling repair · floor coatings.", f"font-family: {BODY}; font-size: 1rem; color: {MUTED}; margin-block-start: 1.75rem;")
    return SEC("sv", "services", [HEAD("sv-hd", "What we paint", "Every surface, <em>done properly</em>", "One crew from the first walkthrough to the final touch-up, so the color you picked is the color you get."), g, also])

# ---------- before / after (three pairs) ----------
PAIRS = [("ba1", "Gray stucco ranch", "to crisp white"), ("ba2", "Coastal stilt home", "from faded pink to white &amp; seafoam"), ("ba3", "Historic two-story", "from worn to fresh")]
def beforeafter():
    rows = []
    for k, (key, title, sub) in enumerate(PAIRS):
        figs = []
        for i, (suffix, lab, bg) in enumerate([("before", "Before", "rgba(7,20,36,0.82)"), ("after", "After", LEAF)]):
            figs.append(DV(f"{key}-{suffix}", [IMG(f"{key}-{suffix}-i", f"{key}-{suffix}", FILL + " object-position: 50% 40%;", size="large"),
                                      P(f"{key}-{suffix}-l", lab, f"position: absolute; inset-block-start: 14px; inset-inline-start: 14px; font-family: {DISP}; font-weight: 700; font-size: 1.1rem; line-height: 1; letter-spacing: 0.12em; text-transform: uppercase; color: {'#241500' if i else ONDARK}; background-color: {bg}; padding-block-start: 9px; padding-block-end: 9px; padding-inline-start: 14px; padding-inline-end: 14px; border-radius: 999px; @media(--mobile) {{ inset-block-start: 8px; inset-inline-start: 8px; font-size: 0.9rem; padding-block-start: 7px; padding-block-end: 7px; padding-inline-start: 10px; padding-inline-end: 10px; }}", tag="span")],
                           f"position: relative; overflow: hidden; border-radius: 14px; aspect-ratio: 5 / 4; background-color: {FOREST2};"))
        g = GR(f"{key}-g", figs, "grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto; gap: 1.1rem; @media(--mobile) { gap: 0.6rem; }")
        rows.append(FX(f"{key}-row", [H(f"{key}-h", f"{title} <em>· {sub}</em>", "h3", f"font-size: 1.7rem; letter-spacing: 0.04em; text-transform: uppercase; color: {ONDARK}; @media(--mobile) {{ font-size: 1.35rem; }}"), g], "flex-direction: column; gap: 0.8rem;"))
    stack = FX("ba-st", rows, "flex-direction: column; gap: 2.2rem;")
    return SEC("ba", "before-after", [HEAD("ba-hd", "Before &amp; after", "Same house. <em>New life.</em>", "Real jobs from our Google listing. Tired, faded exteriors turned fresh and clean.", dark=True), stack],
               f"background-color: {FOREST};")

# ---------- gallery (3 x 3) ----------
GAL = [("sage-ranch-metal-roof", "Ranch home, exterior repaint", "50% 55%"), ("interior-navy-room", "Navy walls &amp; glossy floor", "50% 55%"),
       ("teal-coastal-home", "Coastal teal &amp; white", "50% 40%"), ("deck-pavilion", "Pavilion &amp; deck", "50% 45%"),
       ("white-ranch-clouds", "Brick &amp; stucco refresh", "50% 60%"), ("arched-iron-door", "Arched entry door", "50% 45%"),
       ("commercial-building", "Commercial building", "50% 55%"), ("deck-stained", "Deck stain &amp; white rail", "50% 55%"),
       ("exterior-bungalow", "Bungalow with a bold door", "50% 55%")]
def gallery():
    tiles = []
    for i, (slug, cap, pos) in enumerate(GAL):
        span = " @media(--tablet) { grid-column: span 2; }" if i == len(GAL) - 1 else ""
        tiles.append(DV(f"g{i:02d}", [IMG(f"g{i:02d}-i", slug, FILL + f" object-position: {pos}; transition: transform 0.4s; &:hover {{ transform: scale(1.04); }}", size="large"),
                                      P(f"g{i:02d}-c", cap, f"position: absolute; inset-inline-start: 0px; inset-inline-end: 0px; inset-block-end: 0px; padding-block-start: 2rem; padding-block-end: 0.7rem; padding-inline-start: 0.85rem; padding-inline-end: 0.85rem; font-family: {BODY}; font-weight: 600; font-size: 0.88rem; line-height: 1.25; color: {ONDARK}; background-image: linear-gradient(180deg, rgba(7,20,36,0) 0%, rgba(7,20,36,0.85) 100%); @media(--mobile) {{ font-size: 0.78rem; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; }}")],
                        f"position: relative; overflow: hidden; border-radius: 12px; aspect-ratio: 4 / 3; background-color: #e3e8ee;{span}"))
    g = GR("gl-g", tiles, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: repeat(3, auto); gap: 1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(5, auto); } @media(--mobile) { gap: 0.55rem; }")
    return SEC("gl", "work", [HEAD("gl-hd", "Our work", "Recent projects around <em>Clearwater</em>", right=BTN("gl-b", "Start your project", EST)), g])

# ---------- how it works ----------
STEPS = [("Free estimate", "We look at the job, talk colors and scope, and give you a clear written price."),
         ("Prep that lasts", "Washing, scraping, patching and priming. This is what keeps paint from peeling."),
         ("Clean, careful paint", "Sharp lines, tidy work and everything protected, inside and out."),
         ("Final walkthrough", "We check every detail with you and touch up before we call it done.")]
def process():
    cards = [FX(f"pr{i}", [P(f"pr{i}-n", f"0{i + 1}", f"font-family: {DISP}; font-weight: 700; font-size: 2.5rem; line-height: 1; color: {FOREST2};"),
                           P(f"pr{i}-t", t, f"font-family: {DISP}; font-weight: 700; font-size: 1.5rem; line-height: 1.1; color: {FOREST};"),
                           P(f"pr{i}-d", d, f"font-family: {BODY}; font-size: 0.98rem; line-height: 1.55; color: {MUTED};")],
                f"flex-direction: column; gap: 0.5rem; padding: 1.5rem 1.4rem; background-color: {CREAM}; border-radius: 14px; border-width: 5px 0px 0px 0px; border-style: solid; border-color: {LEAF}; min-width: 0px;")
             for i, (t, d) in enumerate(STEPS)]
    g = GR("pr-g", cards, "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: auto; gap: 1.1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(4, auto); }")
    return SEC("pr", "process", [HEAD("pr-hd", "How it works", "Simple from <em>start to finish</em>"), g], f"background-color: {PAPER};")

# ---------- about ----------
CREDS = [("Interior &amp; Exterior", "Residential and commercial"), ("Free Estimates", "Call, text or request online"), ("Clearwater, FL", "Serving Pinellas County"), ("Clean Job Sites", "Protected floors, tidy finish")]
def about():
    ph = DV("ab-ph", [IMG("ab-i", "white-ranch-clouds", FILL + " object-position: 30% 50%;", size="large")],
            f"position: relative; overflow: hidden; border-radius: 14px; aspect-ratio: 4 / 5; {SHADOW} @media(--tablet) {{ aspect-ratio: 4 / 3; }}")
    creds = GR("ab-cr", [FX(f"ab-c{i}", [P(f"ab-c{i}-b", b, f"font-family: {DISP}; font-weight: 700; font-size: 1.45rem; line-height: 1.1; color: {FOREST};"),
                                         P(f"ab-c{i}-s", s, f"font-family: {BODY}; font-size: 0.9rem; color: {MUTED};")],
                            f"flex-direction: column; gap: 0.2rem; padding-block-start: 1rem; padding-block-end: 1rem; padding-inline-start: 1.1rem; padding-inline-end: 1.1rem; background-color: {PAPER}; border-width: 1px; border-style: solid; border-color: {LINE}; border-radius: 12px; min-width: 0px;")
                         for i, (b, s) in enumerate(CREDS)],
                 "grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; gap: 0.85rem; margin-block-start: 1.6rem; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(4, auto); }")
    copy = FX("ab-copy", [P("ab-eb", "About us", EB), H("ab-h", "Locally owned, and we treat your home <em>like our own</em>", "h2", H2),
                          P("ab-p", "Miracle Painting LLC is a Clearwater painting company serving homeowners, landlords and local businesses. We keep the process simple: show up on time, prep right, paint clean and stand behind the finish.", LEDE + " margin-block-start: 0.5rem;"),
                          creds,
                          P("ab-area", "<strong>Service area:</strong> Clearwater · Largo · Dunedin · Safety Harbor · Oldsmar · Belleair · St. Petersburg · all of Pinellas County", f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.6; color: {MUTED}; margin-block-start: 1.5rem;")],
              "flex-direction: column; gap: 0.75rem; min-width: 0px;")
    g = GR("ab-g", [ph, copy], "grid-template-columns: minmax(0,1fr) minmax(0,1.15fr); grid-template-rows: auto; gap: 3.5rem; align-items: center; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2rem; }")
    return SEC("ab", "about", [g])

# ---------- estimate (form mount #mp-form, rendered by the snippet) ----------
def estimate():
    LK = f"font-family: {BODY}; font-weight: 600; font-size: 1.2rem; color: {ONDARK}; text-decoration: none; &:hover {{ color: {LEAF}; }} {FOCUS}"
    SM = f"font-family: {BODY}; font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; color: {LEAF};"
    copy = FX("es-copy", [P("es-eb", "Free estimate", EB + f" color: {LEAF};"), H("es-h", "Tell us about <em>your project</em>", "h2", H2 + f" color: {ONDARK};"),
                          P("es-p", "Send a few details and we’ll reach out to set up a time to look at it. Prefer to talk? Give us a call.", LEDE + f" color: {ONDARK_M};"),
                          FX("es-ct", [P("es-tk", "Call or text", SM), P("es-tel", PHONE, LK + " font-size: 1.5rem;", link=L(TEL)),
                                       P("es-mk", "Location", SM + " margin-block-start: 0.8rem;"), P("es-loc", "Clearwater, FL · Pinellas County", f"font-family: {BODY}; font-weight: 500; font-size: 1.1rem; color: {ONDARK};")],
                             "flex-direction: column; gap: 0.3rem; margin-block-start: 1rem;")],
              "flex-direction: column; gap: 0.75rem; min-width: 0px;")
    mount = DV("es-form", [P("es-fb", f"The estimate form is loading. You can also call {PHONE}.", f"font-family: {BODY}; font-size: 1rem; color: {MUTED};")], "min-height: 200px;")
    mount.cfg = {"_cssid": "mp-form"}
    card = FX("es-card", [H("es-ch", "Request an estimate", "h3", "font-size: 2rem;"),
                          P("es-cs", "Takes about a minute.", f"font-family: {BODY}; font-size: 0.95rem; color: {MUTED}; margin-block-end: 0.8rem;"), mount],
              f"flex-direction: column; gap: 0.3rem; padding: 1.9rem; background-color: {PAPER}; border-radius: 18px; box-shadow: 0px 20px 50px 0px rgba(0,0,0,0.25); min-width: 0px; scroll-margin-top: 88px; @media(--tablet) {{ order: -1; }} @media(--mobile) {{ padding: 1.25rem; scroll-margin-top: 76px; }}")
    card.cfg = {"_cssid": "estimate-form"}
    g = GR("es-g", [copy, card], "grid-template-columns: minmax(0,0.9fr) minmax(0,1.1fr); grid-template-rows: auto; gap: 3.5rem; align-items: start; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2.25rem; }")
    return SEC("es", "estimate", [g], f"background-image: linear-gradient(180deg, {FOREST} 0%, #0a1d31 100%);")

# ---------- footer + phone bar ----------
def footer():
    T = f"font-family: {BODY}; font-size: 0.92rem; line-height: 1.6; color: #b3c2d6;"
    LK = f"font-family: {BODY}; font-size: 0.92rem; color: #dde6f1; text-decoration: none; &:hover {{ color: {LEAF}; }} {FOCUS}"
    row = FX("fo-r", [P("fo-a", "<strong>Miracle Painting LLC</strong> · Painting · Clearwater, FL", T),
                      FX("fo-l", [P("fo-tel", PHONE, LK, link=L(TEL))], "width: auto; gap: 1.2rem; flex-wrap: wrap;")],
             "flex-wrap: wrap; gap: 1.25rem; justify-content: space-between; align-items: center;")
    fine = P("fo-fine", "<strong>Demo notice.</strong> This page is a website concept prepared by Axiom Systems for Miracle Painting LLC and is not their official site. The phone number is a placeholder, services and descriptions are illustrative, and the photographs are from their Google Business listing. The estimate form is a demonstration and sends nothing.",
             T + " font-size: 0.8rem; max-width: 110ch; margin-block-start: 1.5rem; padding-block-start: 1.25rem; border-width: 1px 0px 0px 0px; border-style: solid; border-color: rgba(255,255,255,0.14);")
    return FX("fo", [FX("fo-w", [row, fine], WRAP + " flex-direction: column;")],
              f"width: 100%; background-color: {DEEP}; padding-block-start: 2.75rem; padding-block-end: 2.5rem; flex-direction: column; @media(--tablet) {{ padding-block-end: 6.5rem; }}", tag="footer")

def mobilebar():
    # Ends 84px short of the right edge so the site chat bubble keeps its corner (same fix as Fence It Up / Comer's).
    return FX("mb", [BTN("mb-call", "Call", TEL, kind="white", css="flex: 1 1 0px; min-height: 50px; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; font-size: 0.95rem;"),
                     BTN("mb-q", "Free Estimate", EST, css="flex: 1.5 1 0px; min-height: 50px; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; font-size: 0.95rem;")],
              f"display: none; position: fixed; width: auto; inset-inline-start: 0px; inset-inline-end: 84px; inset-block-end: 0px; z-index: 100000000; flex-direction: row; gap: 8px; padding: 8px; background-color: rgba(10,27,46,0.96); backdrop-filter: blur(10px); border-radius: 0px 14px 0px 0px; @media(--tablet) {{ display: flex; }}", tag="nav", _cssid="mp-bar")

SECTIONS = [ribbon, header, hero, services, beforeafter, gallery, process, about, estimate, footer, mobilebar]
if __name__ == "__main__":
    kids = [f() for f in SECTIONS]
    root = N("e-flexbox", "mp", None, f"padding: 0px; width: 100%; max-width: 100%; flex-direction: column; gap: 0px; background-color: {CREAM}; color: {INK}; font-family: {BODY};", kids)
    p = payload(root)
    json.dump(p, open(os.path.join(HERE, "ALL.json"), "w"), ensure_ascii=False); print("ALL", len(json.dumps(p, ensure_ascii=False)))
