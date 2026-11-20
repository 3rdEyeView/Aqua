"""Elementor V4 build payloads for the Dave's Plumbing demo (axiomsystems.systems page 2164).
Native port of the approved local draft (../site/index.html): same copy, palette, photos and sections.
The page snippet (../snippet/main.php) adds the demo estimate form (#dp-form), service preselect, heading accents,
the header colour, the sticky fix and the phone bar logic.
Reuses the build helpers (N, payload, L) from the Branham generator, like every demo since Fence It Up."""
import importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("bgen", os.path.join(HERE, "..", "..", "2026-11-08-branham-demo", "native", "gen.py"))
bgen = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(bgen)
N, payload, L = bgen.N, bgen.payload, bgen.L
MEDIA = json.load(open(os.path.join(HERE, "media-ids.json")))
def mid(slug): return MEDIA[f"daves-demo-{slug}.jpg"]["id"]

FOREST, FOREST2, DEEP, LEAF, LEAF_B, LEAF_INK = "#0b2a4a", "#12507f", "#06182b", "#35c3e8", "#6fd8f2", "#0b6b8a"
CREAM, PAPER, INK, MUTED, LINE, GOLD = "#f4f8fb", "#ffffff", "#12202e", "#566574", "#dbe4ec", "#35c3e8"
ONDARK, ONDARK_M = "#ffffff", "#c4d7ea"
DISP, BODY = '"Barlow Condensed"', '"Figtree"'
PHONE, TEL = "(973) 294-2238", "tel:+19732942238"
EST = "#estimate-form"
FOCUS = f"&:focus {{ outline-width: 3px; outline-color: {LEAF}; outline-style: solid; outline-offset: 3px; }}"
SHADOW = "box-shadow: 0px 10px 30px 0px rgba(11,42,74,0.12);"

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
        "leaf": f"color: #062033; background-color: {LEAF}; border-color: {LEAF}; &:hover {{ background-color: {LEAF_B}; border-color: {LEAF_B}; color: #062033; }} ",
        "ghost": f"color: {ONDARK}; background-color: rgba(0,0,0,0.15); border-color: rgba(255,255,255,0.7); &:hover {{ background-color: rgba(255,255,255,0.14); color: {ONDARK}; }} ",
        "white": f"color: {FOREST}; background-color: #ffffff; border-color: #ffffff; &:hover {{ background-color: #e6f7fc; color: {FOREST}; }} ",
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
    T = f"font-family: {BODY}; font-size: 0.82rem; line-height: 1.35; color: #c4d7ea; text-align: center;"
    return FX("rb", [P("rb-t", "<strong>Website concept by Axiom Systems</strong>, prepared for Dave’s Plumbing and Mechanical LLC. Not their live site; phone, license and service area are theirs. Two photos are theirs; other images are AI-generated illustrations.", T + " @media(--mobile) { display: none; }"),
                     P("rb-m", "<strong>Website concept by Axiom Systems.</strong> Not Dave’s Plumbing’s live site.", T + " display: none; font-size: 0.76rem; @media(--mobile) { display: block; }")],
              f"width: 100%; justify-content: center; background-color: {DEEP}; padding-block-start: 8px; padding-block-end: 8px; padding-inline-start: 16px; padding-inline-end: 16px;", _cssid="dp-ribbon")

NAV = [("Services", "#services"), ("Our Work", "#work"), ("How It Works", "#process"), ("About", "#about")]
def header():
    mono = FX("hd-mono", [P("hd-m", "D", f"font-family: {DISP}; font-weight: 700; font-size: 1.9rem; line-height: 1; color: #062033;", tag="span")],
              f"width: 48px; height: 48px; flex: none; border-radius: 50%; background-color: {LEAF}; align-items: center; justify-content: center; box-shadow: 0px 0px 0px 2px rgba(255,255,255,0.25);")
    brand = FX("hd-brand", [mono,
                            FX("hd-bt", [P("hd-b1", "DAVE’S PLUMBING", f"font-family: {DISP}; font-weight: 700; font-size: 1.55rem; line-height: 1; letter-spacing: 0.02em; color: {ONDARK}; @media(--mobile) {{ font-size: 1.35rem; }}", tag="span"),
                                         P("hd-b2", "&amp; Mechanical · Venice, FL", f"font-family: {BODY}; font-weight: 500; font-size: 0.68rem; line-height: 1.2; letter-spacing: 0.16em; text-transform: uppercase; color: {LEAF};", tag="span")],
                               "flex-direction: column; gap: 3px;")],
                f"width: auto; align-items: center; gap: 12px; text-decoration: none; margin-inline-end: auto; {FOCUS}", tag="a", link=L("#top"))
    links = [P(f"hd-n{i}", t, f"font-family: {BODY}; font-weight: 500; font-size: 0.95rem; color: #dbe8f4; text-decoration: none; &:hover {{ color: {ONDARK}; }} {FOCUS}", tag="span", link=L(d)) for i, (t, d) in enumerate(NAV)]
    nav = FX("hd-nav", links, "width: auto; gap: 1.6rem; align-items: center; @media(--tablet) { display: none; }", tag="nav")
    call = P("hd-call", PHONE, f"font-family: {BODY}; font-weight: 600; font-size: 1rem; color: {ONDARK}; text-decoration: none; white-space: nowrap; {FOCUS} @media(--tablet) {{ display: none; }}", tag="span", link=L(TEL))
    cta = BTN("hd-cta", "Request Service", EST, css="min-height: 44px; padding-inline-start: 1.1rem; padding-inline-end: 1.1rem; font-size: 0.95rem; flex: none; @media(--mobile) { display: none; }")
    inner = FX("hd-in", [brand, nav, call, cta], WRAP + " gap: 1.4rem; align-items: center; min-height: 72px; @media(--mobile) { min-height: 64px; }")
    h = FX("hd", [inner], "width: 100%; position: sticky; inset-block-start: 0px; z-index: 50; background-color: rgba(11,42,74,0.96); backdrop-filter: blur(8px); justify-content: center;", tag="header")
    h.cfg["_cssid"] = "top"; return h

# ---------- hero ----------
CHECK = "✓"
def hero():
    h1 = H("hr-h1", "Plumbing done right, <em>the first time.</em>", "h1",
           f"color: {ONDARK}; font-size: 5.4rem; line-height: 0.98; text-transform: uppercase; max-width: 760px; @media(--tablet) {{ font-size: 4.2rem; }} @media(--mobile) {{ font-size: 3rem; }}")
    sub = P("hr-ld", "Water heaters, drain cleaning, repairs and installs from a licensed Master Plumber. Honest answers, clean work and a call back when you need one.",
            f"font-family: {BODY}; font-size: 1.2rem; line-height: 1.55; color: #dbe8f4; max-width: 600px; @media(--mobile) {{ font-size: 1.04rem; }}")
    act = FX("hr-act", [BTN("hr-b1", "Request Service", EST, css="@media(--mobile) { width: 100%; }"),
                        BTN("hr-b2", f"Call {PHONE}", TEL, kind="ghost", css="@media(--mobile) { width: 100%; }")],
             "flex-wrap: wrap; gap: 0.75rem; margin-block-start: 0.6rem; @media(--mobile) { flex-direction: column; gap: 0.6rem; }")
    act.cfg = {"_cssid": "hero-ctas"}
    lic = P("hr-lic", f"<b>{CHECK}</b>&nbsp; Master Plumber · <strong>License # CFC1434195</strong>",
            f"font-family: {BODY}; font-size: 0.92rem; color: #e8f2fa; background-color: rgba(255,255,255,0.1); border-width: 1px; border-style: solid; border-color: rgba(255,255,255,0.25); border-radius: 999px; padding-block-start: 9px; padding-block-end: 9px; padding-inline-start: 16px; padding-inline-end: 16px; margin-block-start: 1.2rem; align-self: flex-start; width: auto;", tag="span")
    copy = FX("hr-copy", [P("hr-eb", "Venice · Sarasota · Bradenton · Englewood", EB + f" color: {LEAF};"), h1, sub, act, lic], "flex-direction: column; gap: 1.1rem; min-width: 0px;")
    PH = f"position: absolute; overflow: hidden; border-radius: 16px; border-width: 3px; border-style: solid; border-color: rgba(255,255,255,0.9); box-shadow: 0px 24px 50px 0px rgba(0,0,0,0.4); "
    c1 = DV("hr-c1", [IMG("hr-i1", "water-heater-install", FILL, size="large")], PH + "inset-inline-start: 0px; inset-block-start: 0px; width: 66%; height: 84%;")
    c2 = DV("hr-c2", [IMG("hr-i2", "drain-machine", FILL, size="large")], PH + "inset-inline-end: 0px; inset-block-end: 0px; width: 52%; height: 56%;")
    badge = FX("hr-bd", [P("hr-bd1", "LICENSED", f"font-family: {BODY}; font-weight: 600; font-size: 0.68rem; letter-spacing: 0.08em; color: #062033; opacity: 0.8;", tag="span"),
                         P("hr-bd2", "Master Plumber", f"font-family: {BODY}; font-weight: 700; font-size: 0.95rem; color: #062033;", tag="span")],
              f"position: absolute; inset-inline-start: 0px; inset-block-end: 6%; z-index: 3; width: auto; flex-direction: column; gap: 2px; background-color: {LEAF}; border-radius: 12px; padding-block-start: 12px; padding-block-end: 12px; padding-inline-start: 16px; padding-inline-end: 16px; box-shadow: 0px 10px 24px 0px rgba(0,0,0,0.3);")
    collage = DV("hr-col", [c1, c2, badge], "position: relative; width: 100%; max-width: 460px; aspect-ratio: 1 / 1.12; margin-inline-start: auto; margin-inline-end: auto; @media(--tablet) { max-width: 420px; }")
    g = GR("hr-g", [copy, collage], WRAP + " position: relative; z-index: 2; grid-template-columns: minmax(0,1.1fr) minmax(0,0.9fr); grid-template-rows: auto; gap: 3rem; align-items: center; padding-block-start: 5.25rem; padding-block-end: 4.5rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2.25rem; padding-block-start: 3.25rem; padding-block-end: 3rem; }")
    shade = DV("hr-sh", [], "position: absolute; inset: 0px; z-index: 1; background-image: linear-gradient(100deg, rgba(4,22,40,0.94) 0%, rgba(6,32,58,0.86) 55%, rgba(6,32,58,0.7) 100%); @media(--tablet) { background-image: linear-gradient(180deg, rgba(4,22,40,0.9) 0%, rgba(4,22,40,0.88) 100%); }")
    n = FX("hr", [IMG("hr-bg", "hero-copper-manifold", FILL + " object-position: 50% 50%; z-index: 0;"), shade, g], f"position: relative; width: 100%; overflow: hidden; flex-direction: column; background-color: {FOREST};", tag="section")
    n.cfg["_cssid"] = "hero"; return n

# ---------- services (icon cards; the icons are drawn by the page snippet on #ic-1..6) ----------
SERVICES = [("Water Heaters", "Tank and tankless installs and replacements, recirculation pumps and expansion tanks, done to code.", "Water heater estimate"),
            ("Drain Cleaning", "Slow or clogged sinks, tubs and floor drains cleared with professional drain machines.", "Drain service"),
            ("Leaks &amp; Repairs", "Dripping, running or leaking? We find the cause and fix it, not just the symptom.", "Repair visit"),
            ("Fixtures &amp; Faucets", "Faucets, toilets, tubs, sinks and disposals installed and connected cleanly.", "Fixture install"),
            ("Repipes &amp; Water Lines", "Re-plumbs, new lines and water-system upgrades for homes and renovations.", "Repipe estimate"),
            ("Mechanical &amp; Commercial", "Plumbing and mechanical work for businesses, offices and light commercial spaces.", "Commercial estimate")]
def services():
    cards = []
    for i, (t, d, cta) in enumerate(SERVICES):
        ic = DV(f"sv{i}-ic", [], "width: 56px; height: 56px; border-radius: 14px; background-color: #e1f3fa; flex: none; margin-block-end: 0.4rem;")
        ic.cfg = {"_cssid": f"ic-{i + 1}"}
        q = P(f"sv{i}-q", cta + " →", f"font-family: {BODY}; font-weight: 600; font-size: 0.98rem; color: {LEAF_INK}; text-decoration: none; margin-block-start: auto; padding-block-start: 0.5rem; align-self: flex-start; width: auto; &:hover {{ text-decoration: underline; }} {FOCUS}", tag="span", link=L(EST))
        q.cfg["_cssid"] = f"q-{i + 1}"
        cards.append(FX(f"sv{i}", [ic, H(f"sv{i}-h", t, "h3", "font-size: 1.9rem;"), P(f"sv{i}-p", d, f"font-family: {BODY}; font-size: 1rem; line-height: 1.55; color: {MUTED};"), q],
                        f"flex-direction: column; gap: 0.5rem; padding: 1.6rem 1.5rem; background-color: {PAPER}; border-radius: 14px; {SHADOW} min-width: 0px;"))
    g = GR("sv-g", cards, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto auto; gap: 1.4rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(3, auto); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(6, auto); gap: 1rem; }")
    also = P("sv-also", "<strong>Also ask about:</strong> new construction rough-ins · remodels · water pressure problems · gas and mechanical work.", f"font-family: {BODY}; font-size: 1rem; color: {MUTED}; margin-block-start: 1.75rem;")
    return SEC("sv", "services", [HEAD("sv-hd", "What we do", "Plumbing and mechanical, <em>handled</em>", "From a clogged drain to a full water heater install, one licensed team across Sarasota and Manatee counties."), g, also])

# ---------- showcase (generated, illustrative images) ----------
SHOW = [("gen-bathroom-tub", "Bathroom fixtures", "50% 50%", "grid-column: 1; grid-row: 1 / span 2;"), ("gen-tankless-heater", "Tankless water heaters", "50% 30%", "grid-column: 2; grid-row: 1;"),
        ("gen-under-sink", "Under-sink repairs", "50% 50%", "grid-column: 3; grid-row: 1;"), ("gen-pipe-wrench-hands", "Copper &amp; brass fittings", "50% 50%", "grid-column: 2; grid-row: 2;"),
        ("gen-florida-home-hose-bib", "Outdoor &amp; irrigation lines", "50% 50%", "grid-column: 3; grid-row: 2;")]
def showcase():
    tiles = []
    for i, (slug, cap, pos, place) in enumerate(SHOW):
        tablet = " @media(--tablet) { grid-column: auto; grid-row: auto; aspect-ratio: 4 / 3; }" if i else " @media(--tablet) { grid-column: span 2; grid-row: auto; aspect-ratio: 16 / 10; }"
        tiles.append(DV(f"sh{i}", [IMG(f"sh{i}-i", slug, FILL + f" object-position: {pos}; transition: transform 0.4s; &:hover {{ transform: scale(1.04); }}", size="large"),
                                   P(f"sh{i}-t", "Illustrative image", f"position: absolute; inset-block-start: 10px; inset-inline-start: 10px; font-family: {BODY}; font-weight: 600; font-size: 0.7rem; letter-spacing: 0.06em; text-transform: uppercase; color: #ffffff; background-color: rgba(4,22,40,0.7); border-radius: 999px; padding-block-start: 5px; padding-block-end: 5px; padding-inline-start: 10px; padding-inline-end: 10px;", tag="span"),
                                   P(f"sh{i}-c", cap, f"position: absolute; inset-inline-start: 0px; inset-inline-end: 0px; inset-block-end: 0px; padding-block-start: 2rem; padding-block-end: 0.8rem; padding-inline-start: 0.95rem; padding-inline-end: 0.95rem; font-family: {BODY}; font-weight: 600; font-size: 0.95rem; line-height: 1.25; color: {ONDARK}; background-image: linear-gradient(180deg, rgba(4,22,40,0) 0%, rgba(4,22,40,0.85) 100%);")],
                        f"position: relative; overflow: hidden; border-radius: 14px; min-height: 240px; background-color: #e1eaf2; {place}{tablet}"))
    g = GR("sh-g", tiles, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: repeat(2, minmax(260px, auto)); gap: 1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto; } @media(--mobile) { grid-template-columns: minmax(0,1fr); gap: 0.7rem; }")
    note = P("sh-note", "Illustrative images of the kinds of work we handle; they are not photos of specific jobs. See Recent work below for jobs from the field.", f"font-family: {BODY}; font-size: 0.92rem; color: {MUTED}; margin-block-start: 1rem;")
    return SEC("sh", "showcase", [HEAD("sh-hd", "Plumbing, start to finish", "From the water heater <em>to the faucet</em>", "The fixtures, fittings and systems we install, repair and replace every day."), g, note], f"background-color: {PAPER};")

# ---------- recent work (two photos) ----------
WORK = [("water-heater-install", "Water heater install", "Shelf-mounted tank with recirculation pump and expansion tank"),
        ("drain-machine", "Drain cleaning", "Clearing a stubborn floor drain with a power drain machine")]
def work():
    figs = [FX(f"wk{i}", [DV(f"wk{i}-ph", [IMG(f"wk{i}-i", slug, FILL + " object-position: 50% 45%;", size="large")], "position: relative; overflow: hidden; width: 100%; aspect-ratio: 4 / 5; background-color: #e1eaf2;"),
                          FX(f"wk{i}-cp", [P(f"wk{i}-t", t, f"font-family: {BODY}; font-weight: 600; font-size: 1.05rem; color: {FOREST};"), P(f"wk{i}-s", s, f"font-family: {BODY}; font-size: 0.95rem; color: {MUTED};")], "flex-direction: column; gap: 2px; padding: 1rem 1.25rem;")],
               f"flex-direction: column; background-color: {PAPER}; border-radius: 14px; overflow: hidden; {SHADOW} min-width: 0px;") for i, (slug, t, s) in enumerate(WORK)]
    g = GR("wk-g", figs, "grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto; gap: 1.4rem; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; }")
    return SEC("wk", "work", [HEAD("wk-hd", "Recent work", "Clean installs, <em>clear explanations</em>", right=BTN("wk-b", "Start your project", EST)), g])

# ---------- how it works ----------
STEPS = [("Call or request", "Tell us what is going on and we will set up a time that works."),
         ("Clear diagnosis", "We find the real cause and explain your options and the price up front."),
         ("Fixed right", "Licensed work to code, with floors protected and the area kept tidy."),
         ("Walkthrough", "We test everything with you and clean up before we leave.")]
def process():
    cards = [FX(f"pr{i}", [P(f"pr{i}-n", f"0{i + 1}", f"font-family: {DISP}; font-weight: 700; font-size: 2.5rem; line-height: 1; color: {FOREST2};"),
                           P(f"pr{i}-t", t, f"font-family: {DISP}; font-weight: 700; font-size: 1.5rem; line-height: 1.1; color: {FOREST};"),
                           P(f"pr{i}-d", d, f"font-family: {BODY}; font-size: 0.98rem; line-height: 1.55; color: {MUTED};")],
                f"flex-direction: column; gap: 0.5rem; padding: 1.5rem 1.4rem; background-color: {CREAM}; border-radius: 14px; border-width: 5px 0px 0px 0px; border-style: solid; border-color: {LEAF}; min-width: 0px;")
             for i, (t, d) in enumerate(STEPS)]
    g = GR("pr-g", cards, "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: auto; gap: 1.1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(4, auto); }")
    return SEC("pr", "process", [HEAD("pr-hd", "How it works", "Simple from <em>call to cleanup</em>"), g], f"background-color: {PAPER};")

# ---------- about ----------
CREDS = [("Master Plumber", "License # CFC1434195"), ("Venice, FL", "Locally based"), ("Residential &amp; Commercial", "Plumbing and mechanical"), ("Call or Text", PHONE)]
def about():
    creds = GR("ab-cr", [FX(f"ab-c{i}", [P(f"ab-c{i}-b", b, f"font-family: {DISP}; font-weight: 700; font-size: 1.45rem; line-height: 1.1; color: {FOREST};"),
                                         P(f"ab-c{i}-s", s, f"font-family: {BODY}; font-size: 0.9rem; color: {MUTED};")],
                            f"flex-direction: column; gap: 0.2rem; padding-block-start: 1rem; padding-block-end: 1rem; padding-inline-start: 1.1rem; padding-inline-end: 1.1rem; background-color: {PAPER}; border-width: 1px; border-style: solid; border-color: {LINE}; border-radius: 12px; min-width: 0px;")
                         for i, (b, s) in enumerate(CREDS)],
                 "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: auto; gap: 0.85rem; margin-block-start: 1.6rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(4, auto); }")
    copy = FX("ab-copy", [P("ab-eb", "About us", EB), H("ab-h", "A licensed local plumber <em>you can call</em>", "h2", H2),
                          P("ab-p", "Dave’s Plumbing and Mechanical LLC is based in Venice, Florida and serves homeowners and businesses across Sarasota, Venice, Bradenton, Englewood and the surrounding area. Work is performed under a Florida Master Plumber license.", LEDE + " margin-block-start: 0.5rem; max-width: 760px;"),
                          creds,
                          P("ab-area", "<strong>Service area:</strong> Venice · Sarasota · Bradenton · Englewood · North Port · Osprey · Nokomis · surrounding areas", f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.6; color: {MUTED}; margin-block-start: 1.5rem;")],
              "flex-direction: column; gap: 0.75rem; min-width: 0px;")
    return SEC("ab", "about", [copy])

# ---------- estimate (form mount #dp-form, rendered by the snippet) ----------
def estimate():
    LK = f"font-family: {BODY}; font-weight: 600; font-size: 1.2rem; color: {ONDARK}; text-decoration: none; &:hover {{ color: {LEAF}; }} {FOCUS}"
    SM = f"font-family: {BODY}; font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; color: {LEAF};"
    copy = FX("es-copy", [P("es-eb", "Request service", EB + f" color: {LEAF};"), H("es-h", "Tell us <em>what you need</em>", "h2", H2 + f" color: {ONDARK};"),
                          P("es-p", "Send a few details and we’ll reach out to set up a time. Prefer to talk? Call or text anytime.", LEDE + f" color: {ONDARK_M};"),
                          FX("es-ct", [P("es-tk", "Call or text", SM), P("es-tel", PHONE, LK + " font-size: 1.5rem;", link=L(TEL)),
                                       P("es-mk", "Based in", SM + " margin-block-start: 0.8rem;"), P("es-loc", "Venice, FL · Sarasota &amp; Manatee counties", f"font-family: {BODY}; font-weight: 500; font-size: 1.1rem; color: {ONDARK};")],
                             "flex-direction: column; gap: 0.3rem; margin-block-start: 1rem;")],
              "flex-direction: column; gap: 0.75rem; min-width: 0px;")
    mount = DV("es-form", [P("es-fb", f"The estimate form is loading. You can also call {PHONE}.", f"font-family: {BODY}; font-size: 1rem; color: {MUTED};")], "min-height: 200px;")
    mount.cfg = {"_cssid": "dp-form"}
    card = FX("es-card", [H("es-ch", "Request service", "h3", "font-size: 2rem;"),
                          P("es-cs", "Takes about a minute.", f"font-family: {BODY}; font-size: 0.95rem; color: {MUTED}; margin-block-end: 0.8rem;"), mount],
              f"flex-direction: column; gap: 0.3rem; padding: 1.9rem; background-color: {PAPER}; border-radius: 18px; box-shadow: 0px 20px 50px 0px rgba(0,0,0,0.25); min-width: 0px; scroll-margin-top: 88px; @media(--tablet) {{ order: -1; }} @media(--mobile) {{ padding: 1.25rem; scroll-margin-top: 76px; }}")
    card.cfg = {"_cssid": "estimate-form"}
    g = GR("es-g", [copy, card], "grid-template-columns: minmax(0,0.9fr) minmax(0,1.1fr); grid-template-rows: auto; gap: 3.5rem; align-items: start; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2.25rem; }")
    return SEC("es", "estimate", [g], f"background-image: linear-gradient(180deg, {FOREST} 0%, #061c33 100%);")

# ---------- footer + phone bar ----------
def footer():
    T = f"font-family: {BODY}; font-size: 0.92rem; line-height: 1.6; color: #b3c6da;"
    LK = f"font-family: {BODY}; font-size: 0.92rem; color: #dbe8f4; text-decoration: none; &:hover {{ color: {LEAF}; }} {FOCUS}"
    row = FX("fo-r", [P("fo-a", "<strong>Dave’s Plumbing and Mechanical LLC</strong> · Master Plumber License # CFC1434195 · Venice, FL", T),
                      FX("fo-l", [P("fo-tel", PHONE, LK, link=L(TEL))], "width: auto; gap: 1.2rem; flex-wrap: wrap;")],
             "flex-wrap: wrap; gap: 1.25rem; justify-content: space-between; align-items: center;")
    fine = P("fo-fine", "<strong>Demo notice.</strong> This page is a website concept prepared by Axiom Systems for Dave’s Plumbing and Mechanical LLC and is not their official site. The phone number, license number and service area were supplied by the business; services and descriptions are illustrative. The two photos under Recent work are from their online listing; the other images are AI-generated illustrations and do not show specific jobs. The estimate form is a demonstration and sends nothing.",
             T + " font-size: 0.8rem; max-width: 110ch; margin-block-start: 1.5rem; padding-block-start: 1.25rem; border-width: 1px 0px 0px 0px; border-style: solid; border-color: rgba(255,255,255,0.14);")
    return FX("fo", [FX("fo-w", [row, fine], WRAP + " flex-direction: column;")],
              f"width: 100%; background-color: {DEEP}; padding-block-start: 2.75rem; padding-block-end: 2.5rem; flex-direction: column; @media(--tablet) {{ padding-block-end: 6.5rem; }}", tag="footer")

def mobilebar():
    # Ends 84px short of the right edge so the site chat bubble keeps its corner (same fix as Fence It Up / Comer's).
    return FX("mb", [BTN("mb-call", "Call", TEL, kind="white", css="flex: 1 1 0px; min-height: 50px; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; font-size: 0.95rem;"),
                     BTN("mb-q", "Request Service", EST, css="flex: 1.5 1 0px; min-height: 50px; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; font-size: 0.95rem;")],
              f"display: none; position: fixed; width: auto; inset-inline-start: 0px; inset-inline-end: 84px; inset-block-end: 0px; z-index: 100000000; flex-direction: row; gap: 8px; padding: 8px; background-color: rgba(6,24,43,0.96); backdrop-filter: blur(10px); border-radius: 0px 14px 0px 0px; @media(--tablet) {{ display: flex; }}", tag="nav", _cssid="dp-bar")

SECTIONS = [ribbon, header, hero, services, showcase, work, process, about, estimate, footer, mobilebar]
if __name__ == "__main__":
    kids = [f() for f in SECTIONS]
    root = N("e-flexbox", "dp", None, f"padding: 0px; width: 100%; max-width: 100%; flex-direction: column; gap: 0px; background-color: {CREAM}; color: {INK}; font-family: {BODY};", kids)
    p = payload(root)
    json.dump(p, open(os.path.join(HERE, "ALL.json"), "w"), ensure_ascii=False); print("ALL", len(json.dumps(p, ensure_ascii=False)))
