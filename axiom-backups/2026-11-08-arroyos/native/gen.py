"""Elementor V4 build payloads for the Arroyo's Lawn Care demo (axiomsystems.systems page 1716).
Reuses the build helpers (N, payload, L) from the Branham generator. Section order, copy, palette and fonts follow
arroyoslawncare.com (home page); nothing is invented: claims, services, FAQ and contact details are theirs."""
import importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("bgen", os.path.join(HERE, "..", "..", "2026-11-08-branham-demo", "native", "gen.py"))
bgen = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(bgen)
N, payload, L = bgen.N, bgen.payload, bgen.L
MEDIA = json.load(open(os.path.join(HERE, "media-ids.json")))
def mid(name): return MEDIA["arroyos-demo-" + name]["id"]
def murl(name): return MEDIA["arroyos-demo-" + name]["url"]

# Their tokens (assets/css/styles.css)
INK, FOREST, GREEN, LIME, LIME_B, SUN, PAPER, TINT, CARD, MUTED, LINE = (
    "#0c1509", "#12300f", "#23751a", "#8edc1e", "#a8f032", "#f8981d", "#f4f5ef", "#e8eddf", "#ffffff", "#55604f", "#dde2d3")
ONDARK, ONDARK_M, DLINE = "#f4f5ef", "#c3cbbb", "rgba(244,245,239,0.16)"
DISP, BODY = '"Barlow Condensed"', '"Figtree"'
PHONE, TEL, EMAIL = "(941) 962-1124", "tel:+19419621124", "info@arroyoslawncare.com"
FB, IG = "https://www.facebook.com/profile.php?id=61595224107237", "https://www.instagram.com/arroyoslawncare/"
FOCUS = f"&:focus {{ outline-width: 3px; outline-color: {LIME}; outline-style: solid; outline-offset: 3px; }}"
QUOTE = "#estimate"

def P(cid, text, css="", tag="p", link=None):
    c = {"paragraph": text, "tag": tag}
    if link: c["link"] = link
    return N("e-paragraph", cid, c, "display: block; margin: 0px; " + css)
def H(cid, text, tag, css=""):
    return N("e-heading", cid, {"title": text, "tag": tag},
             f"display: block; margin: 0px; font-family: {DISP}; font-weight: 700; line-height: 1; text-transform: uppercase; letter-spacing: 0.005em; color: {INK}; " + css)
def BTN(cid, text, dest, kind="lime", css="", blank=False):
    base = (f"font-family: {BODY}; font-weight: 600; font-size: 1rem; line-height: 1; text-decoration: none; text-align: center; "
            f"min-height: 52px; padding-block-start: 0.9rem; padding-block-end: 0.9rem; padding-inline-start: 1.6rem; padding-inline-end: 1.6rem; "
            f"border-radius: 999px; border-width: 2px; border-style: solid; display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; transition: background-color 0.2s, color 0.2s, border-color 0.2s; {FOCUS} ")
    base += {
        "lime": f"color: {INK}; background-color: {LIME}; border-color: {LIME}; box-shadow: 0px 10px 28px -10px rgba(142,220,30,0.7); &:hover {{ background-color: {LIME_B}; border-color: {LIME_B}; color: {INK}; }} ",
        "dark": f"color: {ONDARK}; background-color: {INK}; border-color: {INK}; &:hover {{ background-color: {FOREST}; border-color: {FOREST}; color: {ONDARK}; }} ",
        "white": f"color: {INK}; background-color: #ffffff; border-color: #ffffff; &:hover {{ background-color: #eef3e4; border-color: #eef3e4; color: {INK}; }} ",
        "ghost": f"color: {ONDARK}; background-color: rgba(12,21,9,0.35); border-color: rgba(244,245,239,0.7); &:hover {{ background-color: {ONDARK}; border-color: {ONDARK}; color: {INK}; }} ",
        "line": f"color: {INK}; background-color: transparent; border-color: {INK}; &:hover {{ background-color: {INK}; color: {ONDARK}; }} ",
    }[kind]
    return N("e-button", cid, {"text": text, "link": L(dest, blank)}, base + css)
def FX(cid, kids, css="", **cfg): return N("e-flexbox", cid, cfg or None, "padding: 0px; " + css, kids)
def DV(cid, kids, css="", **cfg): return N("e-div-block", cid, cfg or None, "padding: 0px; min-width: 0px; " + css, kids)
def GR(cid, kids, css="", **cfg): return N("e-grid", cid, cfg or None, "padding: 0px; " + css, kids)
def IMG(cid, name, alt, css="", size="full"):
    return N("e-image", cid, {"image": {"src": {"id": mid(name)}, "size": size}}, css)
FILL = "position: absolute; inset: 0px; width: 100%; height: 100%; object-fit: cover; display: block;"

EYEBROW_CSS = (f"display: inline-flex; width: auto; align-self: flex-start; align-items: center; gap: 0.5rem; font-family: {BODY}; font-weight: 600; font-size: 0.82rem; line-height: 1; "
               f"color: {INK}; background-color: {CARD}; border-radius: 999px; padding-block-start: 0.45rem; padding-block-end: 0.45rem; padding-inline-start: 0.6rem; padding-inline-end: 0.85rem; "
               f"box-shadow: 0px 1px 2px rgba(12,21,9,0.06), 0px 6px 18px -10px rgba(12,21,9,0.25);")
def EYEBROW(cid, text, dark=False, center=False):
    dot = DV(cid + "-d", [], f"width: 10px; height: 10px; border-radius: 50%; background-color: {SUN}; flex: none;")
    css = EYEBROW_CSS + (f" color: {ONDARK}; background-color: rgba(244,245,239,0.08); box-shadow: 0px 0px 0px 0px rgba(0,0,0,0); border-width: 1px; border-style: solid; border-color: {DLINE};" if dark else "")
    if center: css += " align-self: center;"
    return FX(cid, [dot, P(cid + "-t", text, "color: inherit;", tag="span")], css)
LEDE = f"font-family: {BODY}; font-size: 1.125rem; line-height: 1.6; color: {MUTED}; max-width: 60ch; @media(--mobile) {{ font-size: 1.04rem; }}"
H2 = "font-size: 3.4rem; @media(--tablet) { font-size: 2.8rem; } @media(--mobile) { font-size: 2.25rem; }"
WRAP = "width: 100%; max-width: 1200px; margin-inline-start: auto; margin-inline-end: auto; padding-inline-start: 40px; padding-inline-end: 40px; @media(--mobile) { padding-inline-start: 16px; padding-inline-end: 16px; }"
SECTION = f"width: 100%; background-color: {PAPER}; padding-block-start: 6rem; padding-block-end: 6rem; display: flex; flex-direction: column; scroll-margin-top: 80px; @media(--tablet) {{ padding-block-start: 4.5rem; padding-block-end: 4.5rem; }} @media(--mobile) {{ padding-block-start: 3.5rem; padding-block-end: 3.5rem; }}"
def SEC(cid, anchor, kids, css=""):
    n = FX(cid, [FX(cid + "-w", kids, WRAP + " flex-direction: column; gap: 0px;")], SECTION + " " + css, tag="section")
    if anchor: n.cfg["_cssid"] = anchor
    return n
def HL(cid, plain, accent, tag="h2", css="", dark=False, after=""):
    """Their two-tone headings as one real heading; the accent words sit in <em>, styled by the page snippet
    (lime underline on light sections, lime text on dark ones, like arroyoslawncare.com)."""
    col = ONDARK if dark else INK
    return H(cid, f"{plain}<em>{accent}</em>{after}", tag, f"color: {col}; " + css)
def HEAD(cid, eb, plain, accent, lede=None, right=None, dark=False, center=False):
    left = [EYEBROW(cid + "-eb", eb, dark, center), HL(cid + "-h", plain, accent, css=H2, dark=dark)]
    if lede: left.append(P(cid + "-ld", lede, LEDE + (f" color: {ONDARK_M};" if dark else "") + (" margin-inline-start: auto; margin-inline-end: auto;" if center else "")))
    kids = [FX(cid + "-l", left, "flex-direction: column; gap: 1rem; flex: 1 1 auto; min-width: 0px;" + (" align-items: center; text-align: center;" if center else ""))]
    if right: kids.append(right)
    return FX(cid, kids, "flex-direction: row; gap: 1.5rem; align-items: flex-end; justify-content: space-between; margin-block-end: 3rem; @media(--mobile) { flex-direction: column; align-items: flex-start; margin-block-end: 2rem; }")

# ---------- 0. announcement + utility bar ----------
def topbar():
    ann = FX("an", [P("an-t", "Now booking fall landscape projects", f"font-family: {BODY}; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; color: {INK};", tag="span"),
                    P("an-l", "Request a free estimate", f"font-family: {BODY}; font-weight: 700; font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; color: {INK}; text-decoration: underline; {FOCUS}", tag="span", link=L(QUOTE))],
              f"width: 100%; justify-content: center; align-items: center; flex-wrap: wrap; gap: 0.25rem; column-gap: 0.9rem; background-color: {LIME}; padding-block-start: 0.6rem; padding-block-end: 0.6rem; padding-inline-start: 16px; padding-inline-end: 16px; text-align: center;")
    U = f"font-family: {BODY}; font-size: 0.9rem; color: {ONDARK}; text-decoration: none; &:hover {{ color: {LIME}; }}"
    util = FX("ut", [FX("ut-w", [
        FX("ut-l", [P("ut-p", f"Call or text {PHONE}", U, link=L(TEL)), P("ut-e", EMAIL, U, link=L("mailto:" + EMAIL))], "width: auto; gap: 1.75rem; align-items: center;"),
        FX("ut-r", [P("ut-h", "Mon–Sat 8 AM – 5 PM", f"font-family: {BODY}; font-size: 0.9rem; color: {ONDARK_M};"),
                    P("ut-fb", "Facebook", U, link=L(FB, True)), P("ut-ig", "Instagram", U, link=L(IG, True))], "width: auto; gap: 1.5rem; align-items: center;"),
    ], WRAP + " justify-content: space-between; align-items: center; min-height: 44px;")],
        f"width: 100%; background-color: {INK}; border-width: 0px 0px 1px 0px; border-style: solid; border-color: {DLINE}; @media(--tablet) {{ display: none; }}")
    return [ann, util]

# ---------- 1. header ----------
NAV = [("About", "#about"), ("Services", "#services"), ("Process", "#process"), ("Results", "#results"), ("Gallery", "#work"), ("Areas", "#areas"), ("FAQ", "#faq")]
def header():
    logo = DV("hd-brand", [IMG("hd-logo", "logo.webp", "Arroyo’s Lawn Care LLC", "width: 150px; height: auto; display: block; @media(--mobile) { width: 118px; }")],
              f"width: auto; flex: none; margin-inline-end: auto; text-decoration: none; {FOCUS}", tag="a", link=L("#top"))
    navlinks = [BTN(f"hd-n{i}", t, d, kind="ghost", css=f"min-height: 0px; padding-inline-start: 0px; padding-inline-end: 0px; padding-block-start: 0.4rem; padding-block-end: 0.4rem; font-weight: 500; font-size: 0.98rem; color: {ONDARK}; background-color: transparent; border-radius: 0px; border-width: 0px 0px 2px 0px; border-color: transparent; box-shadow: 0px 0px 0px 0px rgba(0,0,0,0); &:hover {{ color: {LIME}; background-color: transparent; border-color: {LIME}; }}") for i, (t, d) in enumerate(NAV)]
    nav = FX("hd-nav", navlinks, "width: auto; gap: 1.6rem; align-items: center; @media(--tablet) { display: none; }", tag="nav")
    cta = BTN("hd-cta", "Request Free Estimate", QUOTE, css="min-height: 48px; @media(--tablet) { display: none; }")
    call = BTN("hd-call", "Call", TEL, kind="ghost", css="display: none; min-height: 44px; padding-inline-start: 1rem; padding-inline-end: 1rem; @media(--tablet) { display: inline-flex; }")
    mlinks = [BTN(f"hd-m{i}", t, d, kind="ghost", css=f"width: 100%; justify-content: flex-start; font-weight: 500; font-size: 1.1rem; color: {ONDARK}; background-color: transparent; border-radius: 0px; border-width: 0px 0px 1px 0px; border-color: {DLINE}; padding-inline-start: 0px; &:hover {{ color: {LIME}; background-color: transparent; border-color: {DLINE}; }}") for i, (t, d) in enumerate(NAV)]
    mlinks.append(BTN("hd-mcta", "Request Free Estimate", QUOTE, css="width: 100%; margin-block-start: 1.25rem;"))
    mlinks.append(BTN("hd-mtel", f"Call {PHONE}", TEL, kind="ghost", css="width: 100%; margin-block-start: 0.6rem;"))
    menu = N("e-accordion", "hd-menu", {"default_state": "all_collapsed", "max_expanded": "one", "show_icon": False, "faq_schema": False},
             "width: auto; position: static; padding: 0px; display: none; flex: 0 0 auto; @media(--tablet) { display: flex; }", [
        N("e-accordion-item", "hd-mi", None, "width: auto; position: static; padding: 0px; border-width: 0px;", [
            N("e-accordion-item-header", "hd-mh", None, f"min-height: 44px; cursor: pointer; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 1rem; padding-inline-end: 1rem; border-width: 1.5px; border-style: solid; border-color: rgba(244,245,239,0.7); border-radius: 999px; display: flex; gap: 0.5rem; align-items: center; {FOCUS}", [
                N("e-accordion-item-title", "hd-mt", None, "min-width: 0px; padding: 0px;", [P("hd-ml", "Menu", f"font-family: {BODY}; font-weight: 600; font-size: 0.95rem; color: {ONDARK};", tag="span")]),
                N("e-accordion-item-icon", "hd-mic", None, "display: none;")]),
            N("e-accordion-item-content", "hd-mp", None, f"position: absolute; inset-block-start: 100%; inset-inline-start: 0px; inset-inline-end: 0px; z-index: 60; padding-block-start: 0.5rem; padding-block-end: 1.25rem; padding-inline-start: 16px; padding-inline-end: 16px; background-color: {INK}; border-width: 0px 0px 1px 0px; border-style: solid; border-color: {DLINE}; box-shadow: 0px 30px 60px 0px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 0px;", mlinks)])])
    inner = FX("hd-in", [logo, nav, cta, call, menu], WRAP + " position: static; gap: 1.5rem; align-items: center; min-height: 80px; @media(--tablet) { gap: 0.6rem; min-height: 68px; }")
    h = FX("hd", [inner], f"width: 100%; position: sticky; inset-block-start: 0px; z-index: 50; background-color: rgba(12,21,9,0.92); backdrop-filter: blur(10px); border-width: 0px 0px 1px 0px; border-style: solid; border-color: {DLINE}; justify-content: center;", tag="header")
    h.cfg["_cssid"] = "top"; return h

# ---------- 2. hero: their drone video, untouched, with a first-frame poster ----------
BADGES = [("Licensed &amp; Insured", "Fully covered"), ("Free Estimates", "On every project"), ("Same-Day Reply", "On every request"), ("Owner-Operated", "You deal with the owner")]
def hero():
    shade = DV("hr-shade", [], "position: absolute; inset: 0px; z-index: 0; background-image: linear-gradient(90deg, rgba(12,21,9,0.86) 0%, rgba(12,21,9,0.62) 42%, rgba(12,21,9,0.12) 78%), linear-gradient(0deg, rgba(12,21,9,0.55) 0%, rgba(12,21,9,0) 35%); @media(--tablet) { background-image: linear-gradient(180deg, rgba(12,21,9,0.30) 0%, rgba(12,21,9,0.55) 40%, rgba(12,21,9,0.90) 100%); }")
    pill = FX("hr-pill", [DV("hr-pill-d", [], f"width: 8px; height: 8px; border-radius: 50%; background-color: {LIME}; flex: none;"),
                          P("hr-pill-t", "15+ years of experience · Commercial &amp; Residential", "color: inherit;", tag="span")],
              f"display: inline-flex; width: auto; align-self: flex-start; align-items: center; gap: 0.55rem; font-family: {BODY}; font-weight: 500; font-size: 0.9rem; line-height: 1.2; color: {ONDARK}; "
              f"background-color: rgba(12,21,9,0.55); backdrop-filter: blur(6px); border-width: 1px; border-style: solid; border-color: rgba(248,152,29,0.55); border-radius: 999px; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 0.85rem; padding-inline-end: 1rem; @media(--mobile) {{ font-size: 0.8rem; }}")
    h1 = HL("hr-h1", "Complete landscape service for ", "Manatee &amp; Sarasota Counties", tag="h1", dark=True,
            css="font-size: 4.6rem; line-height: 0.98; max-width: 760px; @media(--tablet) { font-size: 3.8rem; max-width: 620px; } @media(--mobile) { font-size: 2.55rem; line-height: 1; max-width: 100%; }")
    lede = P("hr-ld", "One experienced team to design, build, and maintain your property.", f"font-family: {BODY}; font-size: 1.3rem; line-height: 1.5; color: {ONDARK}; max-width: 40ch; @media(--mobile) {{ font-size: 1.1rem; }}")
    act = FX("hr-act", [BTN("hr-b1", "Request a Free Estimate", QUOTE, css="min-height: 56px; font-size: 1.08rem; padding-inline-start: 1.9rem; padding-inline-end: 1.9rem; @media(--mobile) { width: 100%; }"),
                        BTN("hr-b2", f"Call {PHONE}", TEL, kind="ghost", css="min-height: 56px; font-size: 1.08rem; @media(--mobile) { width: 100%; }")],
             "flex-wrap: wrap; gap: 0.75rem; @media(--mobile) { flex-direction: column; }")
    badges = GR("hr-bd", [FX(f"hr-bd{i}", [P(f"hr-bd{i}-a", a, f"font-family: {DISP}; font-weight: 700; font-size: 1.1rem; line-height: 1.05; letter-spacing: 0.02em; text-transform: uppercase; color: {ONDARK};"),
                                            P(f"hr-bd{i}-b", b, f"font-family: {BODY}; font-size: 0.85rem; line-height: 1.35; color: {ONDARK_M};")],
                             f"flex-direction: column; gap: 0.25rem; padding-block-start: 0.85rem; padding-block-end: 0.85rem; padding-inline-start: 1rem; padding-inline-end: 1rem; border-width: 0px 0px 0px 3px; border-style: solid; border-color: {LIME}; background-color: rgba(12,21,9,0.5); backdrop-filter: blur(6px); border-radius: 0px 10px 10px 0px; min-width: 0px;")
                          for i, (a, b) in enumerate(BADGES)],
                "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: auto; gap: 0.75rem; max-width: 780px; margin-block-start: 0.75rem; @media(--mobile) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; gap: 0.5rem; }")
    copy = FX("hr-copy", [pill, h1, lede, act, badges], "position: relative; z-index: 1; flex-direction: column; gap: 1.4rem; min-width: 0px; @media(--mobile) { gap: 1.1rem; }")
    w = FX("hr-w", [copy], WRAP + " position: relative; z-index: 1; flex-direction: column; justify-content: center; min-height: calc(100vh - 160px); padding-block-start: 5rem; padding-block-end: 5.5rem; @media(--tablet) { justify-content: flex-end; min-height: 760px; padding-block-start: 9rem; padding-block-end: 3rem; } @media(--mobile) { min-height: 0px; padding-block-start: 5.5rem; padding-block-end: 2.25rem; }")
    content = N("e-background-video-content", "hr-c", None, "position: relative; z-index: 1; padding: 0px; width: 100%;", [shade, w])
    lbl = lambda cid, t: N(cid, cid, None, f"padding: 0px; display: flex; align-items: center; justify-content: center; min-width: 44px; min-height: 44px; border-radius: 999px; background-color: rgba(12,21,9,0.55); border-width: 1px; border-style: solid; border-color: rgba(244,245,239,0.45); color: {ONDARK}; cursor: pointer; {FOCUS}",
                           [P(cid + "-t", t, f"font-family: {BODY}; font-weight: 600; font-size: 0.8rem; color: {ONDARK}; padding-inline-start: 0.8rem; padding-inline-end: 0.8rem;", tag="span")])
    controls = N("e-background-video-controls", "hr-k", None, "position: absolute; z-index: 2; inset-block-start: 1.25rem; inset-block-end: auto; inset-inline-end: 1.25rem; height: auto; padding: 0px; @media(--tablet) { inset-block-start: 1rem; inset-block-end: auto; inset-inline-end: 1rem; }",
                 [lbl("e-background-video-play", "Play video"), lbl("e-background-video-pause", "Pause video")])
    # controls cids must be unique: rename
    controls.kids[0].cid, controls.kids[1].cid = "hr-play", "hr-pause"
    controls.kids[0].kids[0].cid, controls.kids[1].kids[0].cid = "hr-play-t", "hr-pause-t"
    v = N("e-background-video", "hr", {"_cssid": "hero", "tag": "section", "source": {"id": mid("hero.mp4")}, "autoplay": True, "mute": True, "loop": True, "show_controls": True},
          f"width: 100%; padding: 0px; position: relative; overflow: hidden; background-color: {INK}; background-image: url({murl('hero-poster.jpg')}); background-size: cover; background-position: 50% 50%;",
          [content, controls])
    return v

# ---------- 3. why us ----------
WHY = ["Licensed and fully insured", "Owner-operated, with over 15 years of experience", "Free estimates and same-day communication",
       "Commercial and residential properties", "Trees and palms trimmed for their health, not just their looks", "Craftsmanship you can count on"]
def about():
    photo = DV("ab-ph", [IMG("ab-img", "lakeside-palm-bed.jpg", "Lakeside palm bed: palm cluster with boulders and agave", FILL + " object-position: 50% 60%;"),
                         FX("ab-yr", [P("ab-yr-n", "15+", f"font-family: {DISP}; font-weight: 700; font-size: 3.2rem; line-height: 0.9; color: {LIME};"),
                                      P("ab-yr-t", "years of landscaping experience", f"font-family: {BODY}; font-size: 0.9rem; line-height: 1.4; color: {ONDARK}; max-width: 12ch;")],
                            f"position: absolute; width: auto; inset-block-end: -1.5rem; inset-inline-end: 1.5rem; flex-direction: column; gap: 0.4rem; background-color: {INK}; border-radius: 16px; padding: 1.25rem; box-shadow: 0px 20px 40px -16px rgba(12,21,9,0.6); @media(--mobile) {{ inset-inline-end: 1rem; inset-block-end: -1.25rem; padding: 1rem; }}")],
               f"position: relative; aspect-ratio: 4 / 5; border-radius: 28px; overflow: visible; background-color: {LINE}; @media(--tablet) {{ aspect-ratio: 4 / 3; }}")
    # rounded image: radius on the img itself since the box keeps overflow visible for the badge
    photo.kids[0].css += " border-radius: 28px;"
    checks = FX("ab-ck", [FX(f"ab-c{i}", [P(f"ab-c{i}-m", "✓", f"font-family: {BODY}; font-weight: 700; color: {GREEN}; flex: none; width: 1.2rem;", tag="span"),
                                         P(f"ab-c{i}-t", t, f"font-family: {BODY}; font-size: 1.02rem; line-height: 1.45; color: {INK};", tag="span")],
                             "gap: 0.5rem; align-items: flex-start;") for i, t in enumerate(WHY)], "flex-direction: column; gap: 0.6rem;")
    copy = FX("ab-copy", [EYEBROW("ab-eb", "Why Us?"), HL("ab-h", "Quality work from a team you can ", "count on", css=H2),
                          P("ab-p", "We are a licensed and insured, owner-operated landscaping company based in Bradenton. One team handles the design, the install, and the upkeep, so nothing gets lost between contractors.", LEDE),
                          checks, FX("ab-act", [BTN("ab-b", "Request a Free Estimate", QUOTE, kind="dark")], "margin-block-start: 0.5rem;")],
               "flex-direction: column; gap: 1.25rem; min-width: 0px;")
    g = GR("ab-g", [photo, copy], "grid-template-columns: minmax(0,5fr) minmax(0,6fr); grid-template-rows: auto; gap: 5rem; align-items: center; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 3.5rem; }")
    return SEC("ab", "about", [g])

# ---------- 4. services ----------
SERVICES = [("Landscape Design &amp; Installation", "Landscape design, grading, plant installation, sod, topsoil, mulch, decorative stone, and landscape edging."),
            ("Landscape Lighting Installation &amp; Repair", "Landscape lighting installation and repair for lanais, driveways, palms, beds, and other outdoor areas."),
            ("Tree &amp; Palm Services", "Tree and palm trimming, tree and palm removal, and stump grinding."),
            ("Pavers, Hardscapes &amp; Fencing", "Paver and hardscape installation, plus fence removal and installation."),
            ("Drainage Installation &amp; Repair", "Drain pipe and catch basin installation, plus gutter repair and installation."),
            ("Irrigation &amp; Sprinkler Services", "Irrigation system installation and expansion, Rain Bird programming, drip irrigation, and filter cleaning and maintenance."),
            ("Lawn Maintenance", "Basic to full-service lawn maintenance, including mowing, edging, trimming, and blowing, with weed control available."),
            ("Property &amp; Storm Cleanup", "Seasonal cleanups, one-time deep cleans, and hurricane and storm debris removal."),
            ("Shrub, Hedge &amp; Flower Bed Care", "Shrub and hedge trimming, pruning, shaping, and spot weeding in beds."),
            ("Pressure Washing &amp; Surface Sealing", "Pressure washing and exterior surface sealing.")]
def services():
    tiles = [FX(f"sv{i}", [P(f"sv{i}-n", f"{i+1:02d}", f"font-family: {DISP}; font-weight: 700; font-size: 1rem; color: {GREEN};"),
                           H(f"sv{i}-h", t, "h3", "font-size: 1.35rem; line-height: 1.05;"),
                           P(f"sv{i}-p", d, f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.55; color: {MUTED};")],
                f"flex-direction: column; gap: 0.6rem; padding: 1.4rem; background-color: {CARD}; border-radius: 16px; border-width: 1px; border-style: solid; border-color: {LINE}; min-width: 0px; transition: border-color 0.2s, transform 0.2s; &:hover {{ border-color: {GREEN}; transform: translateY(-2px); }}")
             for i, (t, d) in enumerate(SERVICES)]
    g = GR("sv-g", tiles, "grid-template-columns: repeat(5, minmax(0,1fr)); grid-template-rows: auto auto; gap: 1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(5, auto); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(10, auto); gap: 0.75rem; }")
    right = BTN("sv-cta", "Request a Free Estimate", QUOTE, kind="dark", css="flex: none; min-width: 240px;")
    return SEC("sv", "services", [HEAD("sv-hd", "Our Services", "Landscaping, hardscaping, and ", "everything in between",
                                       "From new landscapes and lighting to irrigation, drainage, tree work, and routine upkeep.", right=right), g],
               f"background-color: {TINT};")

# ---------- 5. process ----------
STEPS = [("Free Estimate Request", "Call, text, or send the estimate form and tell us about your property and what you would like done. You will hear back from us the same day. For a quicker response, call or text us."),
         ("On-Site Walkthrough", "We meet you at the property, look over the space together, take measurements, and listen to how you want it to look and function. Bring your questions and ideas."),
         ("Plan &amp; Proposal", "You receive a clear scope of the work that will be done, so there are no surprises. We go over it with you and adjust it until it fits."),
         ("Build &amp; Installation", "With the plan approved, you can leave the rest to us. Our crew follows it closely, treats your property with care, and delivers exactly what we agreed on."),
         ("Property Maintenance", "Once the work is finished, scheduled maintenance is available to keep your property looking the way it did on day one.")]
def process():
    st = [FX(f"pr{i}", [FX(f"pr{i}-top", [P(f"pr{i}-n", f"{i+1:02d}", f"display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; flex: none; border-radius: 50%; background-color: {LIME}; font-family: {DISP}; font-weight: 700; font-size: 1.05rem; color: {INK};"),
                                          DV(f"pr{i}-ln", [], f"flex: 1 1 auto; height: 2px; background-color: {LINE}; @media(--mobile) {{ display: none; }}")], "align-items: center; gap: 0.75rem;"),
                        H(f"pr{i}-h", t, "h3", "font-size: 1.3rem; line-height: 1.05; margin-block-start: 0.4rem;"),
                        P(f"pr{i}-p", d, f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.6; color: {MUTED};")],
             "flex-direction: column; gap: 0.6rem; min-width: 0px;") for i, (t, d) in enumerate(STEPS)]
    g = GR("pr-g", st, "grid-template-columns: repeat(5, minmax(0,1fr)); grid-template-rows: auto; gap: 1.5rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(3, auto); gap: 2rem; } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(5, auto); gap: 1.75rem; }")
    return SEC("pr", "process", [HEAD("pr-hd", "How It Works", "Our 5-step ", "approach", "A clear process from your first inquiry, so every step is clear before it starts.", center=True), g])

# ---------- 6. before & after (the standout) ----------
def results():
    BAIMG = FILL + " object-position: 50% 100%; @media(--mobile) { transform: scale(1.32); transform-origin: 46% 100%; }"
    after = IMG("ba-after", "ba2-after.jpg", "After", BAIMG)
    before = DV("ba-before", [IMG("ba-before-i", "ba2-before-visualization.jpg", "Before, demo visualization", BAIMG)],
                "position: absolute; inset: 0px; z-index: 1; clip-path: inset(0px 50% 0px 0px);")
    before.cfg = {"_cssid": "ba-before"}
    TAGCSS = f"position: absolute; z-index: 3; inset-block-start: 1rem; font-family: {BODY}; font-weight: 700; font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase; line-height: 1; padding-block-start: 0.55rem; padding-block-end: 0.55rem; padding-inline-start: 0.8rem; padding-inline-end: 0.8rem; border-radius: 999px; @media(--mobile) {{ font-size: 0.68rem; inset-block-start: 0.75rem; }}"
    t_before = P("ba-tb", "Before · Demo visualization", TAGCSS + f" inset-inline-start: 1rem; color: {ONDARK}; background-color: rgba(12,21,9,0.72); @media(--mobile) {{ inset-inline-start: 0.75rem; }}", tag="span")
    t_after = P("ba-ta", "After", TAGCSS + f" inset-inline-end: 1rem; color: {INK}; background-color: {LIME}; @media(--mobile) {{ inset-inline-end: 0.75rem; }}", tag="span")
    knob = FX("ba-knob", [P("ba-knob-t", "‹ ›", f"font-family: {BODY}; font-weight: 700; font-size: 1.15rem; line-height: 1; color: {INK}; letter-spacing: 0.1em;", tag="span")],
              f"position: absolute; inset-block-start: 50%; inset-inline-start: 50%; transform: translate(-50%, -50%); width: 56px; height: 56px; border-radius: 50%; background-color: #ffffff; align-items: center; justify-content: center; box-shadow: 0px 6px 24px rgba(0,0,0,0.45); border-width: 3px; border-style: solid; border-color: {LIME};")
    handle = DV("ba-handle", [knob], "position: absolute; z-index: 2; inset-block-start: 0px; inset-block-end: 0px; inset-inline-start: 50%; width: 3px; margin-inline-start: -1.5px; background-color: #ffffff; box-shadow: 0px 0px 12px rgba(0,0,0,0.35);")
    handle.cfg = {"_cssid": "ba-handle"}
    stage = DV("ba", [after, before, handle, t_before, t_after],
               f"position: relative; width: 100%; aspect-ratio: 1597 / 760; overflow: hidden; border-radius: 20px; background-color: {FOREST}; box-shadow: 0px 30px 80px -30px rgba(0,0,0,0.8); @media(--tablet) {{ aspect-ratio: 16 / 9; }} @media(--mobile) {{ aspect-ratio: 4 / 3; border-radius: 14px; }}")
    stage.cfg = {"_cssid": "ba"}
    CAPTION = ('<strong>Demo visualization.</strong> After: a real yard photo from Arroyo’s Lawn Care, unedited. '
               'Before: the same photo with only the lawn replaced by real overgrown-grass texture, to show a typical starting point. '
               'The house, beds, driveway, light and camera angle are identical. '
               'Grass texture: <a href="https://www.flickr.com/photos/34764035@N00/50001408903" target="_blank" rel="noopener">“Unmowed lawn!”</a> '
               'by Rhian de Kerhiec, <a href="https://creativecommons.org/licenses/by/2.0/" target="_blank" rel="noopener">CC BY 2.0</a>, modified.')
    note = FX("ba-nt", [P("ba-nt-t", CAPTION,
                          f"font-family: {BODY}; font-size: 0.92rem; line-height: 1.55; color: {ONDARK_M}; max-width: 70ch;"),
                        BTN("ba-cta", "Get an Estimate for Your Lawn", QUOTE, css="flex: none; @media(--mobile) { width: 100%; }")],
              "justify-content: space-between; align-items: center; gap: 1.5rem; margin-block-start: 1.5rem; @media(--mobile) { flex-direction: column; align-items: stretch; }")
    hint = P("ba-hint", "Drag the handle to compare an overgrown lawn with the same yard freshly maintained.", f"font-family: {BODY}; font-size: 1.05rem; line-height: 1.6; color: {ONDARK_M};")
    head = FX("ba-hd", [EYEBROW("ba-eb", "Before &amp; After", dark=True), HL("ba-h", "See the ", "difference", css=H2, dark=True), hint], "flex-direction: column; gap: 1rem; margin-block-start: 0px; margin-block-end: 2.5rem; @media(--mobile) { margin-block-end: 1.75rem; }")
    return SEC("ba-s", "results", [head, stage, note], f"background-color: {INK}; background-image: radial-gradient(circle at 85% 0%, rgba(35,117,26,0.38) 0%, rgba(12,21,9,0) 45%);")

# ---------- 7. recent projects ----------
WORK = [("paver-driveway-entry.jpg", "Front Yard", "Palms &amp; Planting Beds", "New planting beds and trimmed palms, kept sharp with full-service maintenance.", "Paver driveway entry: palms and planting beds"),
        ("driveway-island.jpg", "Driveway Entry", "Driveway Island Planting", "A circular driveway island planted with palms and agave, kept green with properly zoned irrigation and routine maintenance.", "Driveway island planting: palms, agave, and a hedge border"),
        ("royal-palm-entry.jpg", "Entry", "Royal Palm Entry", "Royal palms and planting beds.", "Royal palm entry: royal palms and planting beds"),
        ("layered-front-beds.jpg", "Front Yard", "Layered Front-Yard Beds", "Royal palms, boulders, and tropical plants.", "Layered front-yard beds: royal palms, boulders, and tropical plants"),
        ("bottle-palms-entry.jpg", "Entry", "Bottle Palms &amp; Ti Plants", "Bottle palms, red ti plants, and black rock.", "Entry bottle palms and ti plants: bottle palms, red ti plants, and black rock"),
        ("circular-driveway-lawn.jpg", "Lawn", "Circular Driveway Lawn", "A wide lawn and an island bed.", "Circular driveway lawn: wide lawn and an island bed")]
def work():
    cards = []
    for i, (img, cat, t, d, alt) in enumerate(WORK):
        ph = DV(f"wk{i}-ph", [IMG(f"wk{i}-i", img, alt, FILL + " transition: transform 0.4s; &:hover { transform: scale(1.03); }", size="large")], f"position: relative; overflow: hidden; aspect-ratio: 4 / 3; width: 100%; background-color: {LINE};")
        body = FX(f"wk{i}-b", [P(f"wk{i}-c", cat, f"font-family: {BODY}; font-weight: 600; font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase; color: {GREEN};"),
                               H(f"wk{i}-h", t, "h3", "font-size: 1.45rem;"), P(f"wk{i}-p", d, f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.55; color: {MUTED};")],
                  "flex-direction: column; gap: 0.45rem; padding: 1.25rem; padding-block-end: 1.5rem;")
        cards.append(FX(f"wk{i}", [ph, body], f"flex-direction: column; background-color: {CARD}; border-radius: 20px; overflow: hidden; border-width: 1px; border-style: solid; border-color: {LINE}; min-width: 0px;"))
    g = GR("wk-g", cards, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto auto; gap: 1.5rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(3, auto); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(6, auto); gap: 1rem; }")
    right = BTN("wk-cta", "Request a Free Estimate", QUOTE, kind="dark", css="flex: none; min-width: 240px;")
    return SEC("wk", "work", [HEAD("wk-hd", "Gallery", "Recent ", "projects", "A look at landscapes we have designed, installed, and maintained for homes and businesses in the area.", right=right), g])

# ---------- 8. service areas ----------
AREAS = [("Bradenton", "Our home base. Lawn maintenance, landscape installs, irrigation, and cleanups across Bradenton."),
         ("Lakewood Ranch", "Design, installation, and ongoing maintenance for homes and businesses in Lakewood Ranch."),
         ("Sarasota", "Full landscape service in Sarasota, from routine maintenance to complete installs.")]
def areas():
    cards = [FX(f"ar{i}", [P(f"ar{i}-k", "FL", f"font-family: {BODY}; font-weight: 600; font-size: 0.78rem; letter-spacing: 0.12em; color: {GREEN};"),
                           H(f"ar{i}-h", t, "h3", "font-size: 1.8rem;"), P(f"ar{i}-p", d, f"font-family: {BODY}; font-size: 0.98rem; line-height: 1.55; color: {MUTED};")],
                f"flex-direction: column; gap: 0.5rem; padding: 1.6rem; background-color: {CARD}; border-radius: 16px; border-width: 0px 0px 0px 4px; border-style: solid; border-color: {LIME}; min-width: 0px;")
             for i, (t, d) in enumerate(AREAS)]
    g = GR("ar-g", cards, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; gap: 1rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); }")
    note = P("ar-nt", f"Nearby and not listed? Call {PHONE} and ask.", f"font-family: {BODY}; font-weight: 600; font-size: 1rem; color: {INK}; margin-block-start: 1.5rem; text-decoration: none; &:hover {{ color: {GREEN}; }}", link=L(TEL))
    return SEC("ar", "areas", [HEAD("ar-hd", "Service Areas", "Serving Manatee &amp; ", "Sarasota counties", "Based in Bradenton and working across both counties. If you are nearby and not listed, call and ask."), g, note],
               f"background-color: {TINT};")

# ---------- 9. FAQ ----------
FAQ = [("How do I get an estimate, and is it free?", f"Estimates are free. Call or text {PHONE}, or send the request form with a few details about the property and the work you need. We reply the same day and set up a time that works for you to see the property in person before giving you a scope of work."),
       ("What areas do you serve?", "We serve Bradenton, Lakewood Ranch, Sarasota, and nearby communities across Manatee and Sarasota counties. If your property is close by and you are not sure, call us and we will let you know."),
       ("Do you work with HOAs and property managers?", "Yes. We maintain common areas, entrances, medians, and amenity areas for HOAs and property managers. We also handle irrigation repairs, palm and tree trimming, and storm cleanup, so the community works with one contractor instead of several."),
       ("Are you licensed and insured?", "Yes. Arroyo’s Lawn Care LLC is licensed and fully insured for both residential and commercial work."),
       ("What happens after I send a request?", "We reply the same day to confirm what you need and schedule a walkthrough at your property. After the walkthrough you receive a clear scope of the work, and once you approve it, we put the job on the schedule.")]
def faq():
    items = []
    for i, (q, a) in enumerate(FAQ):
        items.append(N("e-accordion-item", f"fq{i}", None, f"padding: 0px; background-color: {CARD}; border-width: 1px; border-style: solid; border-color: {LINE}; border-radius: 14px; overflow: hidden;", [
            N("e-accordion-item-header", f"fq{i}-hd", None, f"display: flex; align-items: center; justify-content: space-between; gap: 1rem; min-height: 60px; padding-block-start: 1rem; padding-block-end: 1rem; padding-inline-start: 1.25rem; padding-inline-end: 1.25rem; cursor: pointer; {FOCUS}", [
                N("e-accordion-item-title", f"fq{i}-t", None, "padding: 0px; min-width: 0px;", [H(f"fq{i}-q", q, "h3", f"font-family: {BODY}; font-weight: 600; font-size: 1.05rem; line-height: 1.4; text-transform: none; letter-spacing: 0px; color: {INK};")]),
                N("e-accordion-item-icon", f"fq{i}-ic", None, f"flex: none; display: flex; align-items: center; justify-content: center; width: 30px; height: 30px; min-width: 30px; border-radius: 50%; background-color: {LIME}; color: {INK}; padding: 0px;",
                  [P(f"fq{i}-ic-t", "+", f"font-family: {BODY}; font-weight: 600; font-size: 1.3rem; line-height: 1; color: {INK};", tag="span")])]),
            N("e-accordion-item-content", f"fq{i}-c", None, "padding-block-start: 0px; padding-block-end: 1.25rem; padding-inline-start: 1.25rem; padding-inline-end: 1.25rem;",
              [P(f"fq{i}-a", a, f"font-family: {BODY}; font-size: 1rem; line-height: 1.65; color: {MUTED}; max-width: 70ch;")])]))
    acc = N("e-accordion", "fq", {"default_state": "first_expanded", "max_expanded": "one", "show_icon": True, "faq_schema": False},
            "display: flex; flex-direction: column; gap: 0.6rem; padding: 0px; width: 100%; max-width: 820px; margin-inline-start: auto; margin-inline-end: auto;", items)
    return SEC("fq-s", "faq", [HEAD("fq-hd", "Questions", "Good to ", "know", "Straight answers to the questions customers ask us most.", center=True), acc])

# ---------- 10. CTA band = estimate destination ----------
def band():
    copy = FX("bd-c", [HL("bd-h", "Ready for a landscaper you can ", "count on", css=H2 + " max-width: 16ch;", dark=True, after="?"),
                       P("bd-p", "Estimates are free. Tell us what you need and we’ll answer the same day.", f"font-family: {BODY}; font-size: 1.15rem; line-height: 1.6; color: {ONDARK};")],
              "flex-direction: column; gap: 1rem; min-width: 0px;")
    C = f"font-family: {BODY}; font-size: 0.85rem; color: {ONDARK_M};"
    ways = GR("bd-ways", [
        BTN("bd-b1", f"Call or text {PHONE}", TEL, css="width: 100%; min-height: 58px; font-size: 1.1rem;"),
        BTN("bd-b2", f"Email {EMAIL}", "mailto:" + EMAIL + "?subject=Free%20estimate%20request", kind="white", css="width: 100%; min-height: 58px; @media(--mobile) { font-size: 0.92rem; }"),
        P("bd-hrs", "Mon–Sat 8 AM – 5 PM · Sunday closed · Same-day reply on every request", C + " text-align: center;"),
    ], "grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); gap: 0.75rem; min-width: 0px;")
    g = GR("bd-g", [copy, ways], "grid-template-columns: minmax(0,6fr) minmax(0,5fr); grid-template-rows: auto; gap: 3rem; align-items: center; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2rem; }")
    n = FX("bd", [FX("bd-w", [g], WRAP + " flex-direction: column;")],
           f"width: 100%; background-color: {FOREST}; background-image: radial-gradient(circle at 100% 0%, rgba(248,152,29,0.55) 0%, rgba(248,152,29,0) 28%); border-width: 0px 0px 3px 0px; border-style: solid; border-color: {LIME}; padding-block-start: 5.5rem; padding-block-end: 5.5rem; flex-direction: column; scroll-margin-top: 80px; @media(--mobile) {{ padding-block-start: 3.5rem; padding-block-end: 3.5rem; }}", tag="section")
    n.cfg = {"_cssid": "estimate"}; return n

# ---------- 11. footer ----------
SVC_LINKS = ["Landscape Design", "Landscape Lighting", "Tree &amp; Palm Services", "Pavers &amp; Hardscapes", "Drainage", "Irrigation &amp; Sprinklers", "Lawn Maintenance", "Property Cleanup", "Shrub &amp; Bed Care", "Pressure Washing"]
HOURS = [("Monday", "8 AM – 5 PM"), ("Tuesday", "8 AM – 5 PM"), ("Wednesday", "8 AM – 5 PM"), ("Thursday", "8 AM – 5 PM"), ("Friday", "8 AM – 5 PM"), ("Saturday", "8 AM – 5 PM"), ("Sunday", "Closed")]
def footer():
    EB = f"font-family: {BODY}; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.14em; text-transform: uppercase; color: {LIME}; margin-block-end: 0.4rem;"
    T = f"font-family: {BODY}; font-size: 0.93rem; line-height: 1.5; color: {ONDARK_M};"
    LK = f"font-family: {BODY}; font-size: 0.93rem; line-height: 1.5; color: {ONDARK}; text-decoration: none; &:hover {{ color: {LIME}; }}"
    a = FX("fo-a", [IMG("fo-logo", "logo.webp", "Arroyo’s Lawn Care LLC", "width: 150px; height: auto; display: block;"),
                    P("fo-d", "Licensed, insured, owner-operated landscaping company with over 15 years of experience serving homes and businesses across Manatee and Sarasota counties.", T + " max-width: 38ch;"),
                    FX("fo-so", [P("fo-fb", "Facebook ↗", LK, link=L(FB, True)), P("fo-ig", "Instagram ↗", LK, link=L(IG, True))], "gap: 1.25rem;")],
           "flex-direction: column; gap: 1rem; min-width: 0px; @media(--tablet) { grid-column: 1 / -1; }")
    b = FX("fo-b", [P("fo-b-h", "Services", EB)] + [P(f"fo-s{i}", s, T, link=L("#services")) for i, s in enumerate(SVC_LINKS)], "flex-direction: column; gap: 0.2rem; min-width: 0px;")
    c = FX("fo-c", [P("fo-c-h", "Service Areas", EB), P("fo-a1", "Bradenton, FL", T), P("fo-a2", "Lakewood Ranch, FL", T), P("fo-a3", "Sarasota, FL", T),
                    P("fo-c-h2", "Contact", EB + " margin-block-start: 1rem;"), P("fo-tel", PHONE, LK, link=L(TEL)), P("fo-em", EMAIL, LK + " overflow-wrap: anywhere;", link=L("mailto:" + EMAIL)), P("fo-loc", "Based in Bradenton, Florida", T)],
           "flex-direction: column; gap: 0.2rem; min-width: 0px;")
    hrs = [P("fo-h-h", "Hours", EB)] + [FX(f"fo-h{i}", [P(f"fo-h{i}-d", d, T, tag="span"), P(f"fo-h{i}-t", t, T + (f" color: {SUN};" if t == "Closed" else ""), tag="span")], "justify-content: space-between; gap: 1rem;") for i, (d, t) in enumerate(HOURS)]
    d = FX("fo-d4", hrs, "flex-direction: column; gap: 0.2rem; min-width: 0px;")
    g = GR("fo-g", [a, b, c, d], "grid-template-columns: minmax(0,1.4fr) minmax(0,1fr) minmax(0,1fr) minmax(0,1fr); grid-template-rows: auto; gap: 2.5rem; @media(--tablet) { grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto auto; } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(4, auto); gap: 2rem; }")
    fine = FX("fo-fine", [P("fo-cp", "Copyright © 2026 Arroyo’s Lawn Care LLC. All Rights Reserved.", T + " font-size: 0.82rem;"),
                          P("fo-ax", "Website concept by Axiom Systems. Demo only.", T + " font-size: 0.82rem;")],
              f"justify-content: space-between; gap: 1rem; flex-wrap: wrap; margin-block-start: 3rem; padding-block-start: 1.5rem; border-width: 1px 0px 0px 0px; border-style: solid; border-color: {DLINE};")
    return FX("fo", [FX("fo-w", [g, fine], WRAP + " flex-direction: column;")],
              f"width: 100%; background-color: {INK}; padding-block-start: 4.5rem; padding-block-end: 3rem; flex-direction: column; @media(--tablet) {{ padding-block-end: 7.5rem; }}", tag="footer")

# ---------- 12. phone bar ----------
def mobilebar():
    A = f"flex: 1 1 0px; min-height: 52px; font-size: 1rem; padding-inline-start: 0.5rem; padding-inline-end: 0.5rem; box-shadow: 0px 0px 0px 0px rgba(0,0,0,0);"
    return FX("mb", [BTN("mb-1", "Call now", TEL, kind="ghost", css=A + f" background-color: {FOREST}; border-color: {FOREST};"),
                     BTN("mb-2", "Free estimate", QUOTE, css=A)],
              # right padding keeps the site chat bubble (58px, 20px from the edge) beside the buttons
              f"display: none; position: fixed; inset-inline-start: 0px; inset-inline-end: 0px; inset-block-end: 0px; z-index: 40; flex-direction: row; gap: 8px; padding: 8px; background-color: rgba(12,21,9,0.94); backdrop-filter: blur(10px); border-width: 1px 0px 0px 0px; border-style: solid; border-color: {DLINE}; @media(--tablet) {{ display: flex; padding-inline-end: 84px; }}", tag="nav")

def root():
    return FX("arl", topbar() + [header(), hero(), about(), services(), process(), results(), work(), areas(), faq(), band(), footer(), mobilebar()],
              f"width: 100%; max-width: 100%; flex-direction: column; gap: 0px; background-color: {PAPER}; color: {INK}; font-family: {BODY};")

if __name__ == "__main__":
    r = root(); k = {n.cid: n for n in r.kids}
    shell = N("e-flexbox", "arl", None, r.css, [k["an"], k["ut"], k["hd"], k["hr"]])
    batches = {"A": [shell], "B": [k["ab"], k["sv"]], "C": [k["pr"], k["ba-s"]], "D": [k["wk"], k["ar"]], "E": [k["fq-s"], k["bd"], k["fo"], k["mb"]]}
    for name, nodes in batches.items():
        ps = [payload(n) for n in nodes]; out = {"xml_structure": "".join(p["xml_structure"] for p in ps), "element_config": {}, "style": {}}
        for p in ps: out["element_config"].update(p["element_config"]); out["style"].update(p["style"])
        json.dump(out, open(os.path.join(HERE, f"{name}.json"), "w"), ensure_ascii=False); print(name, len(json.dumps(out, ensure_ascii=False)))
