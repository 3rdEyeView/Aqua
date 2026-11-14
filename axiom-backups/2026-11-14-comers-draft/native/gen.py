"""Elementor V4 build payloads for the Comer's Landscaping demo (axiomsystems.systems page 1996, DRAFT).
Ported from the v3 local concept (../../2026-11-13-comers-landscaping/src.html), same content, palette and photos,
with the review fixes:
 - hero: normal-height hero instead of the ~3-screen scroll-pinned scrub; short H1; both CTAs on the first phone screen;
   the hydroseed -> grown-in pair is a one-time crossfade (CSS in the page snippet), grown-in shows without it;
 - gallery: same 31 photos, filters and lightbox (snippet), but only 8 shown until "Show all";
 - quote: every quote link targets the form card itself (#quote-form); the card comes first on phones; service cards
   preselect their service; the form itself (snippet, demo-only) asks for name, phone, optional email, service,
   optional city/ZIP and details.
Content rules: Comer's own wording/contact details (archived comerslandscaping.com, see the v3 README); written-for-demo
captions and blurbs only describe the photos. No reviews, ratings, years, licence or warranty claims.
Reuses the build helpers (N, payload, L) from the Branham generator, like the Fence It Up and Arroyo's demos."""
import importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("bgen", os.path.join(HERE, "..", "..", "2026-11-08-branham-demo", "native", "gen.py"))
bgen = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(bgen)
N, payload, L = bgen.N, bgen.payload, bgen.L
MEDIA = json.load(open(os.path.join(HERE, "media-ids.json")))
def mid(name): return MEDIA[name]["id"]

INK, PANEL, PANEL2, GREEN, LIME, LIME_B = "#060a07", "#0d130e", "#141c15", "#72be45", "#c4d82e", "#d6ea3c"
PAPER, PAPER2, CARD, TEXT, MUTED, LINE, DGREEN = "#f3f5ec", "#e7ebdc", "#ffffff", "#10160f", "#59635a", "#d9dfcc", "#3f7d1c"
ONDARK, ONDARK_M, DLINE = "#ffffff", "rgba(255,255,255,0.78)", "rgba(255,255,255,0.14)"
DISP, BODY = '"Anton"', '"Figtree"'
PHONE, TEL, MAIL = "803.422.8031", "tel:+18034228031", "comerslandscaping@gmail.com"
FB, IGM = "https://www.facebook.com/comerslandscaping", "https://www.instagram.com/comerslandscapingllc/"
QUOTE = "#quote-form"
FOCUS = f"&:focus {{ outline-width: 3px; outline-color: {LIME}; outline-style: solid; outline-offset: 3px; }}"

def P(cid, text, css="", tag="p", link=None):
    c = {"paragraph": text, "tag": tag}
    if link: c["link"] = link
    return N("e-paragraph", cid, c, "display: block; margin: 0px; " + css)
def H(cid, text, tag, css=""):
    return N("e-heading", cid, {"title": text, "tag": tag},
             f"display: block; margin: 0px; font-family: {DISP}; font-weight: 400; line-height: 0.95; letter-spacing: 0.01em; text-transform: uppercase; color: {TEXT}; " + css)
def BTN(cid, text, dest, kind="lime", css="", blank=False, anchor=None):
    base = (f"font-family: {BODY}; font-weight: 800; font-size: 0.94rem; line-height: 1; letter-spacing: 0.06em; text-transform: uppercase; text-decoration: none; text-align: center; "
            f"min-height: 52px; padding-block-start: 0.9rem; padding-block-end: 0.9rem; padding-inline-start: 1.6rem; padding-inline-end: 1.6rem; "
            f"border-radius: 999px; border-width: 2px; border-style: solid; display: inline-flex; align-items: center; justify-content: center; transition: background-color 0.2s, color 0.2s, border-color 0.2s; {FOCUS} ")
    base += {
        "lime": f"color: #0a1005; background-color: {LIME}; border-color: {LIME}; &:hover {{ background-color: {LIME_B}; border-color: {LIME_B}; color: #0a1005; }} ",
        "dark": f"color: {ONDARK}; background-color: {INK}; border-color: {INK}; &:hover {{ background-color: #1b271c; border-color: #1b271c; color: {ONDARK}; }} ",
        "ghost": f"color: {ONDARK}; background-color: rgba(0,0,0,0.28); border-color: rgba(255,255,255,0.6); &:hover {{ background-color: {ONDARK}; border-color: {ONDARK}; color: {INK}; }} ",
    }[kind]
    cfg = {"text": text, "link": L(dest, blank)}
    if anchor: cfg["_cssid"] = anchor
    return N("e-button", cid, cfg, base + css)
def FX(cid, kids, css="", **cfg): return N("e-flexbox", cid, cfg or None, "padding: 0px; " + css, kids)
def DV(cid, kids, css="", **cfg): return N("e-div-block", cid, cfg or None, "padding: 0px; min-width: 0px; " + css, kids)
def GR(cid, kids, css="", **cfg): return N("e-grid", cid, cfg or None, "padding: 0px; " + css, kids)
def IMG(cid, name, css="", size="full"):
    return N("e-image", cid, {"image": {"src": {"id": mid(name)}, "size": size}}, css)
FILL = "position: absolute; inset: 0px; width: 100%; height: 100%; object-fit: cover; display: block;"

LEDE = f"font-family: {BODY}; font-size: 1.12rem; line-height: 1.65; color: {MUTED}; max-width: 60ch; @media(--mobile) {{ font-size: 1.02rem; }}"
H2 = "font-size: 3.6rem; @media(--tablet) { font-size: 3rem; } @media(--mobile) { font-size: 2.35rem; }"
WRAP = "width: 100%; max-width: 1200px; margin-inline-start: auto; margin-inline-end: auto; padding-inline-start: 40px; padding-inline-end: 40px; @media(--mobile) { padding-inline-start: 16px; padding-inline-end: 16px; }"
SECTION = f"width: 100%; background-color: {PAPER}; padding-block-start: 6rem; padding-block-end: 6rem; display: flex; flex-direction: column; scroll-margin-top: 72px; @media(--tablet) {{ padding-block-start: 4.5rem; padding-block-end: 4.5rem; }} @media(--mobile) {{ padding-block-start: 3.5rem; padding-block-end: 3.5rem; scroll-margin-top: 64px; }}"
def SEC(cid, anchor, kids, css=""):
    n = FX(cid, [FX(cid + "-w", kids, WRAP + " flex-direction: column; gap: 0px;")], SECTION + " " + css, tag="section")
    if anchor: n.cfg["_cssid"] = anchor
    return n
def EYEBROW(cid, text, dark=False):
    return FX(cid, [DV(cid + "-d", [], "width: 28px; height: 2px; background-color: currentColor; flex: none;"),
                    P(cid + "-t", text, "color: inherit;", tag="span")],
              f"width: auto; align-items: center; gap: 10px; font-family: {BODY}; font-weight: 700; font-size: 0.8rem; line-height: 1; letter-spacing: 0.18em; text-transform: uppercase; color: {LIME if dark else DGREEN};")
def HEAD(cid, eb, title, lede=None, dark=False):
    left = [EYEBROW(cid + "-eb", eb, dark), H(cid + "-h", title, "h2", H2 + (f" color: {ONDARK};" if dark else ""))]
    kids = [FX(cid + "-l", left, "flex-direction: column; gap: 1rem; flex: 1 1 auto; min-width: 0px;")]
    if lede: kids.append(P(cid + "-ld", lede, LEDE + (f" color: {ONDARK_M};" if dark else "") + " max-width: 40ch; flex: 0 1 auto;"))
    return FX(cid, kids, "flex-direction: row; gap: 2rem; align-items: flex-end; justify-content: space-between; margin-block-end: 2.75rem; @media(--tablet) { flex-direction: column; align-items: flex-start; gap: 1rem; margin-block-end: 1.75rem; }")
def CHIP(cid, text, css=""):
    return FX(cid, [DV(cid + "-d", [], f"width: 7px; height: 7px; border-radius: 50%; background-color: {LIME}; flex: none;"),
                    P(cid + "-t", text, "color: inherit;", tag="span")],
              f"width: auto; align-items: center; gap: 6px; padding-block-start: 6px; padding-block-end: 6px; padding-inline-start: 10px; padding-inline-end: 10px; border-radius: 999px; background-color: rgba(0,0,0,0.62); border-width: 1px; border-style: solid; border-color: rgba(255,255,255,0.22); font-family: {BODY}; font-weight: 700; font-size: 0.7rem; line-height: 1; letter-spacing: 0.08em; text-transform: uppercase; color: {ONDARK}; " + css)

# ---------- 0. demo ribbon ----------
def ribbon():
    RB = f"font-family: {BODY}; font-size: 0.82rem; line-height: 1.4; color: #1a1000; text-align: center; max-width: 1100px;"
    return FX("rb", [P("rb-t", "<strong>Website concept by Axiom Systems, not Comer’s live site.</strong> Logo, wording, contact details and every photo are Comer’s own. The quote form is a demo and sends nothing.",
                       RB + " @media(--mobile) { display: none; }"),
                     P("rb-m", "<strong>Website concept by Axiom Systems.</strong> Not Comer’s live site.", RB + " display: none; font-size: 0.76rem; @media(--mobile) { display: block; }")],
              "width: 100%; justify-content: center; background-color: #ff9f2e; padding-block-start: 8px; padding-block-end: 8px; padding-inline-start: 16px; padding-inline-end: 16px; @media(--mobile) { padding-block-start: 6px; padding-block-end: 6px; }")

# ---------- 1. header (sticky, so it never overlaps content) + native accordion menu ----------
NAV = [("About", "#about"), ("Services", "#services"), ("Results", "#results"), ("Equipment", "#equipment"), ("Our Work", "#gallery")]
def header():
    logo = DV("hd-brand", [IMG("Logo - Comers", "logo-mark.png", "height: 54px; width: auto; display: block; @media(--mobile) { height: 44px; }")],
              f"display: block; width: auto; flex: none; {FOCUS}", tag="a", link=L("#hero"))
    navlinks = [P(f"hd-n{i}", t, f"font-family: {BODY}; font-weight: 700; font-size: 0.84rem; letter-spacing: 0.08em; text-transform: uppercase; color: {ONDARK}; text-decoration: none; padding-block-start: 0.45rem; padding-block-end: 0.45rem; border-width: 0px 0px 2px 0px; border-style: solid; border-color: transparent; &:hover {{ border-color: {LIME}; }} {FOCUS}", tag="span", link=L(d))
                for i, (t, d) in enumerate(NAV)]
    nav = FX("hd-nav", navlinks, "width: auto; gap: 1.6rem; align-items: center; margin-inline-start: auto; @media(--tablet) { display: none; }", tag="nav")
    cta = BTN("hd-cta", "Request a Quote", QUOTE, css="min-height: 44px; padding-inline-start: 1.2rem; padding-inline-end: 1.2rem; font-size: 0.82rem; flex: none; @media(--tablet) { margin-inline-start: auto; } @media(--mobile) { display: none; }")
    mlinks = [P(f"hd-m{i}", t, f"font-family: {BODY}; font-weight: 700; font-size: 1.05rem; letter-spacing: 0.06em; text-transform: uppercase; color: {ONDARK}; text-decoration: none; padding-block-start: 0.9rem; padding-block-end: 0.9rem; border-width: 0px 0px 1px 0px; border-style: solid; border-color: {DLINE}; {FOCUS}", tag="span", link=L(d))
              for i, (t, d) in enumerate(NAV)]
    mlinks.append(BTN("hd-mq", "Request a Quote", QUOTE, css="width: 100%; margin-block-start: 1.25rem;"))
    mlinks.append(BTN("hd-mtel", f"Call {PHONE}", TEL, kind="ghost", css="width: 100%; margin-block-start: 0.6rem;"))
    menu = N("e-accordion", "hd-menu", {"default_state": "all_collapsed", "max_expanded": "one", "show_icon": False, "faq_schema": False},
             "width: auto; position: static; padding: 0px; display: none; flex: 0 0 auto; @media(--tablet) { display: flex; }", [
        N("e-accordion-item", "hd-mi", None, "width: auto; position: static; padding: 0px; border-width: 0px;", [
            N("e-accordion-item-header", "hd-mh", None, f"min-height: 44px; cursor: pointer; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 1rem; padding-inline-end: 1rem; border-width: 1.5px; border-style: solid; border-color: rgba(255,255,255,0.6); border-radius: 999px; display: flex; gap: 0.5rem; align-items: center; {FOCUS}", [
                N("e-accordion-item-title", "hd-mt", None, "min-width: 0px; padding: 0px;", [P("hd-ml", "Menu", f"font-family: {BODY}; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase; color: {ONDARK};", tag="span")]),
                N("e-accordion-item-icon", "hd-mic", None, "display: none;")]),
            N("e-accordion-item-content", "hd-mp", None, f"position: absolute; inset-block-start: 100%; inset-inline-start: 0px; inset-inline-end: 0px; z-index: 60; padding-block-start: 0.25rem; padding-block-end: 1.25rem; padding-inline-start: 16px; padding-inline-end: 16px; background-color: {INK}; border-width: 0px 0px 1px 0px; border-style: solid; border-color: {DLINE}; box-shadow: 0px 30px 60px 0px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 0px;", mlinks)])])
    inner = FX("hd-in", [logo, nav, cta, menu], WRAP + " position: static; gap: 1.5rem; align-items: center; min-height: 76px; @media(--tablet) { gap: 0.6rem; } @media(--mobile) { min-height: 64px; }")
    h = FX("hd", [inner], f"width: 100%; position: sticky; inset-block-start: 0px; z-index: 50; background-color: rgba(6,10,7,0.94); backdrop-filter: blur(10px); border-width: 0px 0px 1px 0px; border-style: solid; border-color: {DLINE}; justify-content: center;", tag="header")
    h.cfg["_cssid"] = "top"; return h

# ---------- 2. hero: one screen, grown-in basin with a one-time crossfade from hydroseed day ----------
def hero():
    before = IMG("Hero photo - hydroseed day", "hero-hydroseed.jpg", FILL + " object-position: 50% 60%; z-index: 0;")
    after = IMG("Hero photo - grown in", "hero-grown.jpg", FILL + " object-position: 50% 60%; z-index: 1;")
    after.cfg["_cssid"] = "hero-after"
    shade = DV("hr-shade", [], "position: absolute; inset: 0px; z-index: 2; background-image: linear-gradient(90deg, rgba(6,10,7,0.88) 0%, rgba(6,10,7,0.6) 45%, rgba(6,10,7,0.1) 80%), linear-gradient(0deg, rgba(6,10,7,0.6) 0%, rgba(6,10,7,0) 40%); @media(--tablet) { background-image: linear-gradient(180deg, rgba(6,10,7,0.15) 0%, rgba(6,10,7,0.45) 35%, rgba(6,10,7,0.92) 100%); }")
    # chip A ("hydroseed day") is hidden unless the page snippet runs the crossfade; chip B ("grown in") is the resting state
    chips = DV("hr-chips", [CHIP("hr-chip-a", "Comer’s job photo · hydroseed day", "display: none;"), CHIP("hr-chip-b", "Comer’s job photo · grown in", "position: absolute; inset-block-start: 0px; inset-inline-end: 0px;")],
               "position: absolute; z-index: 3; inset-block-start: 20px; inset-inline-end: 20px; width: auto; @media(--mobile) { inset-block-start: 12px; inset-inline-end: 12px; }")
    chips.kids[1].cfg = {"_cssid": "hero-chip-b"}
    chips.kids[0].cfg = {"_cssid": "hero-chip-a"}
    h1 = H("hr-h1", "Your Commercial &amp; Residential <em>Landscaping</em> Partner", "h1",
           f"color: {ONDARK}; font-size: 5rem; max-width: 12ch; @media(--tablet) {{ font-size: 4rem; }} @media(--mobile) {{ font-size: 2.45rem; max-width: 15ch; }}")
    sub = P("hr-ld", "Reliable year-round landscaping service in Columbia, SC. Owned and operated by Colin Comer.",
            f"font-family: {BODY}; font-size: 1.2rem; line-height: 1.55; color: {ONDARK_M}; max-width: 42ch; @media(--mobile) {{ font-size: 1.02rem; }}")
    act = FX("hr-act", [BTN("hr-b1", "Request a Quote", QUOTE, css="min-height: 56px; padding-inline-start: 2rem; padding-inline-end: 2rem; @media(--mobile) { width: 100%; }"),
                        BTN("hr-b2", f"Call {PHONE}", TEL, kind="ghost", css="min-height: 56px; @media(--mobile) { width: 100%; }")],
             "flex-wrap: wrap; gap: 0.75rem; margin-block-start: 0.5rem; @media(--mobile) { flex-direction: column; gap: 0.6rem; }")
    copy = FX("hr-copy", [h1, sub, act], "flex-direction: column; gap: 1.2rem; max-width: 720px; @media(--mobile) { gap: 0.9rem; }")
    wrap = FX("hr-w", [copy], WRAP + " position: relative; z-index: 3; flex-direction: column; justify-content: flex-end; padding-block-start: 7rem; padding-block-end: 4.5rem; @media(--tablet) { padding-block-start: 9rem; padding-block-end: 3rem; } @media(--mobile) { padding-block-start: 4rem; padding-block-end: 1.5rem; }")
    n = FX("hr", [before, after, shade, chips, wrap],
           f"position: relative; width: 100%; min-height: 680px; overflow: hidden; flex-direction: column; justify-content: flex-end; background-color: {PANEL}; @media(--tablet) {{ min-height: 620px; }} @media(--mobile) {{ min-height: 0px; }}", tag="section")
    n.cfg["_cssid"] = "hero"; return n

def band():
    names = ["Commercial Grounds Maintenance", "Residential Lawn Care", "Decorative Rock", "Hardscaping", "Irrigation", "Landscape Design &amp; Lighting", "Erosion Control"]
    items = [P(f"bd{i}", t, f"font-family: {DISP}; font-size: 1.15rem; line-height: 1; letter-spacing: 0.04em; text-transform: uppercase; color: #0a1005; @media(--mobile) {{ font-size: 0.98rem; }}", tag="span") for i, t in enumerate(names)]
    return FX("bd", items, f"width: 100%; background-color: {LIME}; padding-block-start: 14px; padding-block-end: 14px; padding-inline-start: 20px; padding-inline-end: 20px; gap: 1.6rem; flex-wrap: wrap; justify-content: center; @media(--mobile) {{ gap: 0.7rem; }}")

# ---------- 3. about ----------
FACTS = [("Based in", "Columbia, SC"), ("We serve", "Commercial &amp; Residential"), ("Owner", "Colin Comer"), ("Hours", "Mon–Sat · 7 AM – 7 PM"), ("Call", PHONE)]
def about():
    copy = FX("ab-copy", [EYEBROW("ab-eb", "About Comer’s Landscaping"), H("ab-h", "Design. Install. <em>Maintain.</em>", "h2", H2),
        P("ab-p", "Comer’s Landscaping in Columbia, SC provides reliable year-round landscaping services. Owned and operated by Colin Comer, we provide services that meet both commercial and residential needs. Our landscaping services include commercial grounds maintenance, residential lawn care, installation of sod, mulch, and gravel, hardscaping, irrigation installation and repair, landscape design and lighting, and erosion control.", LEDE),
        P("ab-p2", "When it comes to quality work, we are the first you should call.", LEDE + f" font-weight: 700; color: {TEXT};"),
        FX("ab-act", [BTN("ab-b", "Get Started", QUOTE, kind="dark")], "margin-block-start: 0.5rem;")],
        "flex-direction: column; gap: 1.1rem; min-width: 0px;")
    rows = []
    for i, (k, v) in enumerate(FACTS):
        val = P(f"ab-f{i}-v", v, f"font-family: {BODY}; font-weight: 700; font-size: 1.05rem; line-height: 1.3; color: {TEXT}; text-align: end; text-decoration: none;" + (f" &:hover {{ color: {DGREEN}; }} {FOCUS}" if k == "Call" else ""), link=L(TEL) if k == "Call" else None)
        rows.append(FX(f"ab-f{i}", [P(f"ab-f{i}-k", k, f"font-family: {BODY}; font-weight: 700; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: {MUTED};"), val],
                       f"justify-content: space-between; align-items: center; gap: 1rem; padding-block-start: 1rem; padding-block-end: 1rem; border-width: 0px 0px 1px 0px; border-style: solid; border-color: {LINE};"))
    facts = FX("ab-facts", rows, f"flex-direction: column; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 1.75rem; padding-inline-end: 1.75rem; background-color: {CARD}; border-radius: 20px; border-width: 1px; border-style: solid; border-color: {LINE}; min-width: 0px; @media(--mobile) {{ padding-inline-start: 1.1rem; padding-inline-end: 1.1rem; }}")
    g = GR("ab-g", [copy, facts], "grid-template-columns: minmax(0,1.4fr) minmax(0,1fr); grid-template-rows: auto; gap: 4rem; align-items: center; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2.25rem; }")
    return SEC("ab", "about", [g])

# ---------- 4. services: 7 cards with Comer's photos; each card's link preselects the service in the form ----------
SERVICES = [("Commercial Grounds Maintenance", "Scheduled mowing, edging, beds and seasonal cleanups that keep a business looking cared for.", "p-009.jpg", "60% 55%"),
            ("Residential Lawn Care", "Regular mowing, trimming and clean edges, so the yard is ready whenever you are.", "p-034.jpg", "60% 55%"),
            ("Installation of Decorative Rock", "Sod, mulch, gravel and decorative rock installed for clean, low-upkeep beds and borders.", "p-028.jpg", "50% 50%"),
            ("Hardscaping", "Patios, walkways, walls and steps that give the yard structure and a place to gather.", "p-026c.jpg", "50% 50%"),
            ("Irrigation Installation &amp; Repair", "New systems put in and existing ones repaired, so the lawn gets water where it needs it.", "p-020.jpg", "50% 55%"),
            ("Landscape Design &amp; Lighting", "Planting plans and low-voltage lighting that make the property work after dark too.", "p-021.jpg", "50% 55%"),
            ("Erosion Control", "Grading, walls, stone and groundcover to hold a slope and move water where it should go.", "p-017.jpg", "50% 60%")]
def services():
    cards = []
    for i, (t, d, img, pos) in enumerate(SERVICES):
        ph = DV(f"sv{i}-ph", [IMG(f"sv{i}-i", img, FILL + f" object-position: {pos}; transition: transform 0.5s; &:hover {{ transform: scale(1.04); }}", size="large"),
                              CHIP(f"sv{i}-c", "Comer’s work", "position: absolute; inset-inline-start: 10px; inset-block-end: 10px;")],
                f"position: relative; overflow: hidden; aspect-ratio: 4 / 3; width: 100%; background-color: {PAPER2}; flex: none;")
        q = P(f"sv{i}-q", "Get a quote for this →", f"font-family: {BODY}; font-weight: 800; font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; color: {DGREEN}; text-decoration: none; margin-block-start: auto; padding-block-start: 0.4rem; &:hover {{ color: {TEXT}; }} {FOCUS}", tag="span", link=L(QUOTE))
        q.cfg["_cssid"] = f"q-{i + 1}"
        body = FX(f"sv{i}-b", [P(f"sv{i}-n", f"0{i + 1}", f"font-family: {DISP}; font-size: 1rem; color: {DGREEN};"),
                               H(f"sv{i}-h", t, "h3", "font-size: 1.55rem; line-height: 1;"),
                               P(f"sv{i}-p", d, f"font-family: {BODY}; font-size: 0.97rem; line-height: 1.55; color: {MUTED};"), q],
                  "flex-direction: column; gap: 0.6rem; padding: 1.3rem; padding-block-end: 1.4rem; flex: 1 1 auto;")
        span = " grid-column: span 2; @media(--tablet) { grid-column: auto; }" if i == 0 else ""
        cards.append(FX(f"sv{i}", [ph, body], f"flex-direction: column; background-color: {CARD}; border-radius: 18px; overflow: hidden; border-width: 1px; border-style: solid; border-color: {LINE}; min-width: 0px;{span}"))
    g = GR("sv-g", cards, "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: auto auto; gap: 1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(4, auto); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(7, auto); gap: 0.85rem; }")
    return SEC("sv", "services", [HEAD("sv-hd", "Our Services", "One crew for the <em>whole property</em>", "Seven services, year-round, for homes and commercial sites across the Columbia area."), g],
               f"background-color: {PAPER2};")

# ---------- 5. process ----------
PROC = [("Design", "Tell us what you have in mind. We look at the site and lay out a plan and a quote.", "p-006.jpg"),
        ("Install", "Grading, drainage, sod, rock, hardscape and irrigation, installed by the same company that planned it.", "p-037.jpg"),
        ("Maintain", "Reliable, year-round care for lawns and commercial grounds, so the work keeps its shape.", "p-030.jpg")]
def process():
    cards = []
    for i, (t, d, img) in enumerate(PROC):
        cards.append(DV(f"pr{i}", [IMG(f"pr{i}-i", img, FILL + " object-position: 50% 55%;", size="large"),
                                    DV(f"pr{i}-sh", [], "position: absolute; inset: 0px; background-image: linear-gradient(180deg, rgba(6,10,7,0) 30%, rgba(6,10,7,0.9) 100%);"),
                                    FX(f"pr{i}-in", [P(f"pr{i}-n", f"0{i + 1}", f"font-family: {DISP}; font-size: 1rem; color: {LIME};"),
                                                     H(f"pr{i}-h", t, "h3", f"font-size: 2.2rem; color: {ONDARK};"),
                                                     P(f"pr{i}-p", d, f"font-family: {BODY}; font-size: 0.98rem; line-height: 1.55; color: {ONDARK_M};")],
                                       "position: absolute; inset-inline-start: 0px; inset-inline-end: 0px; inset-block-end: 0px; flex-direction: column; gap: 0.5rem; padding: 1.5rem;")],
                        f"position: relative; overflow: hidden; border-radius: 20px; aspect-ratio: 4 / 5; background-color: {PANEL}; @media(--tablet) {{ aspect-ratio: 16 / 11; }} @media(--mobile) {{ aspect-ratio: 4 / 4.4; }}"))
    g = GR("pr-g", cards, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; gap: 1rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); }")
    return SEC("pr", "process", [HEAD("pr-hd", "How it works", "Three words in the logo. <em>One plan</em> for your yard."), g])

# ---------- 6. results: three before/after pairs (pairings are a reading of the photos; see README) ----------
RESULTS = [("Roadside slope", "Hydroseed goes down, then the bank holds.", ("p-001c.jpg", "50% 100%", "Sprayed", "Hydroseed day"), ("p-002.jpg", "50% 100%", "Grown in", "Established cover")),
           ("Drainage crossing", "A washed-out crossing, then pipe and stone.", ("p-010.jpg", "50% 88%", "Washed out", "Pipe exposed, bank cut away"), ("p-011.jpg", "50% 88%", "Rebuilt", "Culvert set in gravel")),
           ("Backyard", "Graded to bare soil, then a lawn that is kept.", ("p-039.jpg", "50% 75%", "Graded", "Mini skid steer on site"), ("p-035.jpg", "50% 70%", "Finished", "Edged and maintained"))]
def results():
    rows = []
    for i, (t, d, a, b) in enumerate(RESULTS):
        figs = []
        for j, (img, pos, k, cap) in enumerate((a, b)):
            figs.append(DV(f"rs{i}-{j}", [IMG(f"rs{i}-{j}-i", img, FILL + f" object-position: {pos};", size="large"),
                                          FX(f"rs{i}-{j}-c", [P(f"rs{i}-{j}-k", k, f"font-family: {DISP}; font-size: 1.2rem; line-height: 1; text-transform: uppercase; color: {LIME if j else ONDARK};"),
                                                              P(f"rs{i}-{j}-t", cap, f"font-family: {BODY}; font-size: 0.85rem; line-height: 1.3; color: {ONDARK_M};")],
                                             "position: absolute; inset-inline-start: 0px; inset-inline-end: 0px; inset-block-end: 0px; flex-direction: column; gap: 0.3rem; padding: 1rem; background-image: linear-gradient(180deg, rgba(6,10,7,0) 0%, rgba(6,10,7,0.85) 100%);")],
                           f"position: relative; overflow: hidden; border-radius: 16px; aspect-ratio: 4 / 5; background-color: {PANEL};"))
        pair = GR(f"rs{i}-pair", figs, "grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto; gap: 0.75rem; @media(--mobile) { gap: 0.5rem; }")
        hd = FX(f"rs{i}-hd", [P(f"rs{i}-n", f"0{i + 1}", f"font-family: {DISP}; font-size: 1rem; color: {LIME};"),
                              H(f"rs{i}-h", t, "h3", f"font-size: 2.3rem; color: {ONDARK};"),
                              P(f"rs{i}-p", d, f"font-family: {BODY}; font-size: 1rem; line-height: 1.55; color: {ONDARK_M};")],
                "flex-direction: column; gap: 0.5rem; min-width: 0px;")
        rows.append(GR(f"rs{i}", [hd, pair], f"grid-template-columns: minmax(0,1fr) minmax(0,2fr); grid-template-rows: auto; gap: 2.5rem; align-items: center; padding-block-start: 2rem; padding-block-end: 2rem; border-width: 1px 0px 0px 0px; border-style: solid; border-color: {DLINE}; @media(--tablet) {{ grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 1.1rem; }}"))
    return SEC("rs", "results", [HEAD("rs-hd", "Results", "Bare ground to <em>finished work</em>", "Three jobs from Comer’s own photos, from the first pass to the result.", dark=True)] + rows,
               f"background-color: {INK};")

# ---------- 7. equipment ----------
EQUIP = [("Truck &amp; trailer", "Comer’s flatbed hauls a tracked skid steer from job to job.", "p-024.jpg", "22% 55%"),
         ("CAT 259D3", "A tracked skid steer for grading, loading and attachments.", "p-025.jpg", "50% 50%"),
         ("Brush cutter", "A mowing attachment for overgrown fields and highway right-of-way.", "p-015.jpg", "62% 72%"),
         ("Compact excavator", "For drainage pipe, culverts and cutting an access path.", "p-013.jpg", "50% 50%")]
def equipment():
    cards = [FX(f"eq{i}", [DV(f"eq{i}-ph", [IMG(f"eq{i}-i", img, FILL + f" object-position: {pos};", size="large")], f"position: relative; overflow: hidden; aspect-ratio: 1 / 1; width: 100%; background-color: {PANEL2};"),
                           FX(f"eq{i}-b", [H(f"eq{i}-h", t, "h3", f"font-size: 1.5rem; color: {ONDARK};"),
                                           P(f"eq{i}-p", d, f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.5; color: {ONDARK_M};")], "flex-direction: column; gap: 0.45rem; padding: 1.2rem;")],
                f"flex-direction: column; background-color: {PANEL2}; border-radius: 18px; overflow: hidden; border-width: 1px; border-style: solid; border-color: {DLINE}; min-width: 0px;")
             for i, (t, d, img, pos) in enumerate(EQUIP)]
    g = GR("eq-g", cards, "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: auto; gap: 1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; } @media(--mobile) { gap: 0.65rem; }")
    return SEC("eq", "equipment", [HEAD("eq-hd", "The equipment", "Real machines for <em>real ground</em>", "From residential beds to roadside right-of-way, the work calls for more than a push mower.", dark=True), g],
               f"background-color: {PANEL}; border-width: 1px 0px 0px 0px; border-style: solid; border-color: {DLINE};")

# ---------- 8. gallery: 31 photos; the snippet adds filter chips (#cmz-chips), "Show all" and the lightbox ----------
# (category, asset, caption, object-position). The first 8 are the varied set shown before "Show all".
GALLERY = [("hard", "p-026.jpg", "Paver fire pit patio", "50% 62%"), ("lawn", "p-009.jpg", "Commercial mowing", "60% 55%"),
           ("drain", "p-003.jpg", "Basin, grown in", "50% 50%"), ("hard", "p-021.jpg", "Paver patio and beds", "50% 55%"),
           ("equip", "p-024.jpg", "Truck and trailer", "30% 50%"), ("lawn", "p-030.jpg", "Striped lawn", "50% 55%"),
           ("drain", "p-019c.jpg", "Rip-rap and check dams", "50% 50%"), ("hard", "p-028.jpg", "River rock by the pool", "50% 50%"),
           ("site", "p-012.jpg", "Drainage pipe going in", "50% 70%"), ("irr", "p-037.jpg", "Irrigation and sod", "50% 60%"),
           ("lawn", "p-034.jpg", "Walker mower at work", "60% 55%"), ("drain", "p-017.jpg", "Silt fence along the road", "50% 60%"),
           ("hard", "p-029.jpg", "Paver walkway", "50% 50%"), ("site", "p-039.jpg", "Backyard graded", "50% 55%"),
           ("lawn", "p-007.jpg", "Backyard lawn", "50% 60%"), ("equip", "p-025.jpg", "CAT 259D3", "50% 50%"),
           ("drain", "p-016.jpg", "Silt fence trench", "50% 55%"), ("hard", "p-027.jpg", "Fire pit, close up", "50% 50%"),
           ("irr", "p-020.jpg", "Irrigation line", "50% 55%"), ("site", "p-038.jpg", "Pond edge, cleared", "50% 50%"),
           ("lawn", "p-035.jpg", "Edged lawn", "50% 60%"), ("drain", "p-010.jpg", "Crossing, washed out", "50% 70%"),
           ("drain", "p-011.jpg", "Crossing, rebuilt", "50% 70%"), ("equip", "p-015.jpg", "Brush cutter on site", "70% 55%"),
           ("lawn", "p-008.jpg", "Mowing", "60% 60%"), ("site", "p-023.jpg", "Pond bank", "50% 55%"),
           ("drain", "p-014.jpg", "Eroded bank", "50% 60%"), ("lawn", "p-033.jpg", "Backyard lawn", "50% 60%"),
           ("drain", "p-018.jpg", "Site graded behind silt fence", "50% 60%"), ("lawn", "p-006.jpg", "Lawn and beds", "50% 55%"),
           ("equip", "p-013.jpg", "Compact excavator", "50% 50%")]
def gallery():
    tiles = []
    for i, (cat, img, cap, pos) in enumerate(GALLERY):
        t = DV(f"g{i:02d}", [IMG(f"g{i:02d}-i", img, FILL + f" object-position: {pos}; transition: transform 0.4s;", size="large"),
                             P(f"g{i:02d}-c", cap, f"position: absolute; inset-inline-start: 0px; inset-inline-end: 0px; inset-block-end: 0px; padding-block-start: 2rem; padding-block-end: 0.7rem; padding-inline-start: 0.8rem; padding-inline-end: 0.8rem; font-family: {BODY}; font-weight: 700; font-size: 0.85rem; line-height: 1.25; color: {ONDARK}; background-image: linear-gradient(180deg, rgba(6,10,7,0) 0%, rgba(6,10,7,0.8) 100%); @media(--mobile) {{ font-size: 0.76rem; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; padding-block-end: 0.55rem; }}")],
               f"position: relative; overflow: hidden; border-radius: 14px; aspect-ratio: 1 / 1; background-color: {PAPER2}; {FOCUS}")
        t.cfg = {"_cssid": f"g-{cat}-{i:02d}"}
        tiles.append(t)
    chips = DV("gl-chips", [], "min-height: 0px; margin-block-end: 1.25rem;")
    chips.cfg = {"_cssid": "cmz-chips"}
    g = GR("gl-g", tiles, "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: repeat(8, auto); gap: 0.85rem; @media(--tablet) { grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: repeat(11, auto); } @media(--mobile) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(16, auto); gap: 0.5rem; }")
    g.cfg = {"_cssid": "cmz-gal"}
    return SEC("gl", "gallery", [HEAD("gl-hd", "Our Work", "Every kind of <em>job</em>", "Photos from Comer’s own jobs. Tap a photo to see it full size, or filter by the kind of work."), chips, g])

# ---------- 9. call band ----------
def callband():
    n = FX("cb", [IMG("cb-i", "hero-grown.jpg", FILL + " object-position: 50% 70%;", size="1536x1536"),
                  DV("cb-sh", [], "position: absolute; inset: 0px; background-color: rgba(6,10,7,0.72);"),
                  FX("cb-w", [EYEBROW("cb-eb", "Ready when you are", dark=True),
                              H("cb-h", "When it comes to quality work, we are the first you should call.", "h2", f"color: {ONDARK}; font-size: 3.4rem; max-width: 22ch; @media(--tablet) {{ font-size: 2.8rem; }} @media(--mobile) {{ font-size: 2.1rem; }}"),
                              FX("cb-act", [BTN("cb-b1", f"Call {PHONE}", TEL, css="@media(--mobile) { width: 100%; }"), BTN("cb-b2", "Request a Quote", QUOTE, kind="ghost", css="@media(--mobile) { width: 100%; }")],
                                 "flex-wrap: wrap; gap: 0.75rem; margin-block-start: 0.5rem; @media(--mobile) { flex-direction: column; }")],
                     WRAP + " position: relative; z-index: 1; flex-direction: column; gap: 1.1rem;")],
           "position: relative; width: 100%; overflow: hidden; flex-direction: column; padding-block-start: 6rem; padding-block-end: 6rem; @media(--mobile) { padding-block-start: 4rem; padding-block-end: 4rem; }", tag="section")
    return n

# ---------- 10. quote: form card first on phones; the snippet renders the demo form into #cmz-form ----------
def quote():
    LK = f"font-family: {BODY}; text-decoration: none; color: {TEXT}; &:hover {{ color: {DGREEN}; }} {FOCUS}"
    copy = FX("qt-copy", [EYEBROW("qt-eb", "Request a Quote"), H("qt-h", "Have a project <em>in mind?</em>", "h2", H2),
        P("qt-p", "If you have a creative project in mind, get in contact with Comer’s Landscaping today! When it comes to quality work, we are the first you should call. We are looking forward to hearing from you.", LEDE),
        FX("qt-ct", [P("qt-tel", PHONE, f"font-family: {DISP}; font-size: 3rem; line-height: 1; {LK} @media(--mobile) {{ font-size: 2.4rem; }}", link=L(TEL)),
                     P("qt-mail", MAIL, f"font-weight: 700; font-size: 1.08rem; text-decoration: underline; {LK}", link=L("mailto:" + MAIL)),
                     P("qt-hrs", "Hours: Monday–Saturday | 7 AM – 7 PM", f"font-family: {BODY}; font-size: 1rem; color: {MUTED};"),
                     P("qt-pay", "We accept Venmo and CashApp", f"display: inline-block; width: auto; align-self: flex-start; font-family: {BODY}; font-weight: 700; font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase; color: {DGREEN}; background-color: {PAPER2}; border-radius: 999px; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 0.9rem; padding-inline-end: 0.9rem; margin-block-start: 0.4rem;")],
           "flex-direction: column; gap: 0.6rem; margin-block-start: 0.75rem;")],
        "flex-direction: column; gap: 1.1rem; min-width: 0px;")
    mount = DV("qt-form", [P("qt-form-fb", f"The quote form is loading. You can also call {PHONE}.", f"font-family: {BODY}; font-size: 1rem; color: {MUTED};")], "min-height: 200px;")
    mount.cfg = {"_cssid": "cmz-form"}
    card = FX("qt-card", [H("qt-card-h", "Tell us about the job", "h3", "font-size: 2rem;"),
                          P("qt-card-s", "Takes about a minute. Demo form: nothing you type here is sent or stored.", f"font-family: {BODY}; font-size: 0.92rem; color: {MUTED}; margin-block-end: 0.6rem;"), mount],
              f"flex-direction: column; gap: 0.35rem; padding: 2rem; background-color: {CARD}; border-radius: 22px; border-width: 1px; border-style: solid; border-color: {LINE}; box-shadow: 0px 30px 60px -36px rgba(6,10,7,0.45); min-width: 0px; scroll-margin-top: 92px; @media(--tablet) {{ order: -1; }} @media(--mobile) {{ padding: 1.2rem; border-radius: 18px; scroll-margin-top: 76px; }}")
    card.cfg = {"_cssid": "quote-form"}
    g = GR("qt-g", [copy, card], "grid-template-columns: minmax(0,1fr) minmax(0,1.1fr); grid-template-rows: auto; gap: 4rem; align-items: start; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2.5rem; }")
    return SEC("qt", "quote", [g])

# ---------- 11. footer + phone bar ----------
def footer():
    T = f"font-family: {BODY}; font-size: 0.93rem; line-height: 1.6; color: {ONDARK_M};"
    LK = f"font-family: {BODY}; font-weight: 600; font-size: 0.95rem; color: {ONDARK}; text-decoration: none; &:hover {{ color: {LIME}; }} {FOCUS}"
    a = FX("fo-a", [IMG("fo-logo", "logo.png", "width: 190px; height: auto; display: block;"),
                    P("fo-d", "Design. Install. Maintain. Commercial and residential landscaping in Columbia, SC.", T + " max-width: 36ch;")],
           "flex-direction: column; gap: 1rem; min-width: 0px;")
    b = FX("fo-b", [P("fo-b-h", "Explore", T + f" font-weight: 700; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: {LIME};")] +
           [P(f"fo-l{i}", t, LK, link=L(d)) for i, (t, d) in enumerate(NAV + [("Request a Quote", QUOTE)])], "flex-direction: column; gap: 0.55rem; min-width: 0px;")
    c = FX("fo-c", [P("fo-c-h", "Contact", T + f" font-weight: 700; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: {LIME};"),
                    P("fo-tel", PHONE, LK, link=L(TEL)), P("fo-em", MAIL, LK + "", link=L("mailto:" + MAIL)),
                    P("fo-hrs", "Monday–Saturday, 7 AM – 7 PM", T), P("fo-pay", "We accept Venmo and CashApp", T),
                    FX("fo-so", [P("fo-fb", "Facebook ↗", LK, link=L(FB, True)), P("fo-ig", "Instagram ↗", LK, link=L(IGM, True))], "gap: 1.25rem; margin-block-start: 0.3rem;")],
           "flex-direction: column; gap: 0.55rem; min-width: 0px;")
    g = GR("fo-g", [a, b, c], "grid-template-columns: minmax(0,1.4fr) minmax(0,1fr) minmax(0,1.2fr); grid-template-rows: auto; gap: 2.5rem; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); gap: 2rem; }")
    fine = FX("fo-fine", [P("fo-cp", "<strong>Demo notice.</strong> This page is a website concept prepared by Axiom Systems for Comer’s Landscaping, LLC and is not Comer’s official site. The logo, wording, services, phone number, email and hours come from Comer’s own website, and the photographs are from Comer’s own job posts. The quote form is a demonstration and sends nothing.", T + " font-size: 0.82rem; max-width: 110ch;")],
              f"margin-block-start: 2.5rem; padding-block-start: 1.5rem; border-width: 1px 0px 0px 0px; border-style: solid; border-color: {DLINE};")
    return FX("fo", [FX("fo-w", [g, fine], WRAP + " flex-direction: column;")],
              f"width: 100%; background-color: {INK}; padding-block-start: 4rem; padding-block-end: 3rem; flex-direction: column; @media(--tablet) {{ padding-block-end: 7rem; }}", tag="footer")

def mobilebar():
    # Ends 84px short of the right edge so the site chat bubble keeps its corner; above the chat's invisible greeting box
    # (same fix as Fence It Up). The snippet hides it while the quote form is on screen or the chat is open.
    return FX("mb", [BTN("mb-call", "Call", TEL, kind="ghost", css="flex: 1 1 0px; min-height: 50px; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; font-size: 0.85rem;"),
                     BTN("mb-q", "Request a Quote", QUOTE, css="flex: 1.6 1 0px; min-height: 50px; padding-inline-start: 0.6rem; padding-inline-end: 0.6rem; font-size: 0.85rem;")],
              f"display: none; position: fixed; width: auto; inset-inline-start: 0px; inset-inline-end: 84px; inset-block-end: 0px; z-index: 100000000; flex-direction: row; gap: 8px; padding: 8px; background-color: rgba(6,10,7,0.95); backdrop-filter: blur(10px); border-width: 1px 1px 0px 0px; border-style: solid; border-color: {DLINE}; border-radius: 0px 14px 0px 0px; @media(--tablet) {{ display: flex; }}", tag="nav", _cssid="cmz-bar")

def root():
    return FX("cmz", [ribbon(), header(), hero(), band(), about(), services(), process(), results(), equipment(), gallery(), callband(), quote(), footer(), mobilebar()],
              f"width: 100%; max-width: 100%; flex-direction: column; gap: 0px; background-color: {PAPER}; color: {TEXT}; font-family: {BODY};")

if __name__ == "__main__":
    r = root(); k = {n.cid: n for n in r.kids}
    shell = N("e-flexbox", "cmz", None, r.css, [k["rb"], k["hd"], k["hr"], k["bd"]])
    batches = {"A": [shell], "B": [k["ab"], k["sv"]], "C": [k["pr"], k["rs"]], "D": [k["eq"], k["gl"]], "E": [k["cb"], k["qt"]], "F": [k["fo"], k["mb"]]}
    for name, nodes in batches.items():
        ps = [payload(n) for n in nodes]; out = {"xml_structure": "".join(p["xml_structure"] for p in ps), "element_config": {}, "style": {}}
        for p in ps: out["element_config"].update(p["element_config"]); out["style"].update(p["style"])
        json.dump(out, open(os.path.join(HERE, f"{name}.json"), "w"), ensure_ascii=False); print(name, len(json.dumps(out, ensure_ascii=False)))
