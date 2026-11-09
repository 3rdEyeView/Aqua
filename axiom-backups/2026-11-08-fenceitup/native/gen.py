"""Elementor V4 build payloads for the Fence It Up LLC demo (axiomsystems.systems page 1764, /fence-it-up-demo/).
Reuses the build helpers (N, payload, L) from the Branham generator, the same as the Arroyo's demo.

Content rules (from the brief):
 - Every photo is one of Jenny's Instagram posts (see ../sources.tsv), used once. Labels give the fence type plus the
   location tag of that post (Orlando / Kissimmee / Altamonte Springs). No dates.
 - No phone number until it's confirmed. No reviews, ratings, years in business, licensing or warranty claims. The
   "why" points paraphrase Fence It Up's own captions.
 - The estimate form is rendered by the page snippet (../snippet/main.php) into #fiu-form. It is demo-only and sends nothing.
Palette: navy + sky blue + gold, from the Fence It Up logo watermark (IMG_0353 post)."""
import importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("bgen", os.path.join(HERE, "..", "..", "2026-11-08-branham-demo", "native", "gen.py"))
bgen = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(bgen)
N, payload, L = bgen.N, bgen.payload, bgen.L
MEDIA = json.load(open(os.path.join(HERE, "media-ids.json")))
def mid(name): return MEDIA["fenceitup-demo-" + name]["id"]

INK, NAVY, NAVY2, SKY, SKY_D, GOLD, GOLD_B = "#0f1c2e", "#13243a", "#1a3150", "#5bb4ec", "#1d6fa5", "#e8b931", "#f3c94e"
PAPER, TINT, CARD, MUTED, LINE = "#f6f8fa", "#eaf1f7", "#ffffff", "#53647a", "#dbe3ec"
ONDARK, ONDARK_M, DLINE = "#f3f6f9", "#b9c6d4", "rgba(243,246,249,0.14)"
DISP, BODY = '"Archivo"', '"Figtree"'
IG = "https://www.instagram.com/fenceitupllc/"
QUOTE = "#estimate"
FOCUS = f"&:focus {{ outline-width: 3px; outline-color: {GOLD}; outline-style: solid; outline-offset: 3px; }}"

def P(cid, text, css="", tag="p", link=None):
    c = {"paragraph": text, "tag": tag}
    if link: c["link"] = link
    return N("e-paragraph", cid, c, "display: block; margin: 0px; " + css)
def H(cid, text, tag, css=""):
    return N("e-heading", cid, {"title": text, "tag": tag},
             f"display: block; margin: 0px; font-family: {DISP}; font-weight: 800; line-height: 1.02; letter-spacing: -0.015em; color: {INK}; " + css)
def BTN(cid, text, dest, kind="gold", css="", blank=False, anchor=None):
    base = (f"font-family: {BODY}; font-weight: 700; font-size: 1rem; line-height: 1; text-decoration: none; text-align: center; "
            f"min-height: 52px; padding-block-start: 0.9rem; padding-block-end: 0.9rem; padding-inline-start: 1.6rem; padding-inline-end: 1.6rem; "
            f"border-radius: 12px; border-width: 2px; border-style: solid; display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; transition: background-color 0.2s, color 0.2s, border-color 0.2s; {FOCUS} ")
    base += {
        "gold": f"color: {INK}; background-color: {GOLD}; border-color: {GOLD}; box-shadow: 0px 12px 28px -12px rgba(232,185,49,0.75); &:hover {{ background-color: {GOLD_B}; border-color: {GOLD_B}; color: {INK}; }} ",
        "navy": f"color: {ONDARK}; background-color: {INK}; border-color: {INK}; &:hover {{ background-color: {NAVY2}; border-color: {NAVY2}; color: {ONDARK}; }} ",
        "ghost": f"color: {ONDARK}; background-color: transparent; border-color: rgba(243,246,249,0.55); &:hover {{ background-color: {ONDARK}; border-color: {ONDARK}; color: {INK}; }} ",
        "line": f"color: {INK}; background-color: transparent; border-color: {INK}; &:hover {{ background-color: {INK}; color: {ONDARK}; }} ",
    }[kind]
    cfg = {"text": text, "link": L(dest, blank)}
    if anchor: cfg["_cssid"] = anchor
    return N("e-button", cid, cfg, base + css)
def FX(cid, kids, css="", **cfg): return N("e-flexbox", cid, cfg or None, "padding: 0px; " + css, kids)
def DV(cid, kids, css="", **cfg): return N("e-div-block", cid, cfg or None, "padding: 0px; min-width: 0px; " + css, kids)
def GR(cid, kids, css="", **cfg): return N("e-grid", cid, cfg or None, "padding: 0px; " + css, kids)
def IMG(cid, name, css=""):
    return N("e-image", cid, {"image": {"src": {"id": mid(name)}, "size": "full"}}, css)
FILL = "position: absolute; inset: 0px; width: 100%; height: 100%; object-fit: cover; display: block;"

LEDE = f"font-family: {BODY}; font-size: 1.125rem; line-height: 1.6; color: {MUTED}; max-width: 58ch; @media(--mobile) {{ font-size: 1.03rem; }}"
H2 = "font-size: 3rem; @media(--tablet) { font-size: 2.5rem; } @media(--mobile) { font-size: 2.05rem; }"
WRAP = "width: 100%; max-width: 1200px; margin-inline-start: auto; margin-inline-end: auto; padding-inline-start: 40px; padding-inline-end: 40px; @media(--mobile) { padding-inline-start: 16px; padding-inline-end: 16px; }"
SECTION = f"width: 100%; background-color: {PAPER}; padding-block-start: 6rem; padding-block-end: 6rem; display: flex; flex-direction: column; scroll-margin-top: 72px; @media(--tablet) {{ padding-block-start: 4.5rem; padding-block-end: 4.5rem; }} @media(--mobile) {{ padding-block-start: 3.5rem; padding-block-end: 3.5rem; }}"
def SEC(cid, anchor, kids, css=""):
    n = FX(cid, [FX(cid + "-w", kids, WRAP + " flex-direction: column; gap: 0px;")], SECTION + " " + css, tag="section")
    if anchor: n.cfg["_cssid"] = anchor
    return n
def EYEBROW(cid, text, dark=False):
    return P(cid, text, f"font-family: {BODY}; font-weight: 700; font-size: 0.8rem; line-height: 1.2; letter-spacing: 0.14em; text-transform: uppercase; color: {SKY if dark else SKY_D};")
def HEAD(cid, eb, title, lede=None, right=None, dark=False):
    left = [EYEBROW(cid + "-eb", eb, dark), H(cid + "-h", title, "h2", H2 + (f" color: {ONDARK};" if dark else ""))]
    if lede: left.append(P(cid + "-ld", lede, LEDE + (f" color: {ONDARK_M};" if dark else "")))
    kids = [FX(cid + "-l", left, "flex-direction: column; gap: 0.9rem; flex: 1 1 auto; min-width: 0px;")]
    if right: kids.append(right)
    return FX(cid, kids, "flex-direction: row; gap: 1.5rem; align-items: flex-end; justify-content: space-between; margin-block-end: 2.75rem; @media(--mobile) { flex-direction: column; align-items: flex-start; margin-block-end: 1.75rem; }")

# ---------- 1. header ----------
def wordmark(cid, dark=True, small=False):
    col = ONDARK if dark else INK
    pick = lambda i, h: DV(f"{cid}-k{i}", [], f"width: 6px; height: {h}px; border-radius: 3px 3px 1px 1px; background-color: {GOLD}; flex: none;")
    icon = FX(cid + "-ic", [pick(0, 14), pick(1, 20), pick(2, 14)], "width: auto; gap: 3px; align-items: flex-end; flex: none; padding-block-end: 3px;")
    name = FX(cid + "-nm", [P(cid + "-a", "FENCE IT UP", f"font-family: {DISP}; font-weight: 800; font-size: {'1.15rem' if small else '1.3rem'}; line-height: 1; letter-spacing: 0.02em; color: {col}; @media(--mobile) {{ font-size: 1.08rem; letter-spacing: 0.01em; }}", tag="span"),
                            P(cid + "-b", "LLC · ORLANDO, FL", f"font-family: {BODY}; font-weight: 600; font-size: 0.62rem; line-height: 1; letter-spacing: 0.2em; color: {ONDARK_M if dark else MUTED}; @media(--mobile) {{ font-size: 0.56rem; letter-spacing: 0.14em; }}", tag="span")],
              "width: auto; flex-direction: column; gap: 0.3rem;")
    return DV(cid, [icon, name], f"display: flex; width: auto; flex: none; align-items: center; gap: 0.6rem; text-decoration: none; {FOCUS}", tag="a", link=L("#top"))

NAV = [("Services", "#services"), ("Our Work", "#work"), ("Why Us", "#why")]
def header():
    navlinks = [P(f"hd-n{i}", t, f"font-family: {BODY}; font-weight: 600; font-size: 0.98rem; color: {ONDARK}; text-decoration: none; padding-block-start: 0.4rem; padding-block-end: 0.4rem; border-width: 0px 0px 2px 0px; border-style: solid; border-color: transparent; &:hover {{ color: {GOLD}; border-color: {GOLD}; }} {FOCUS}", tag="span", link=L(d))
                for i, (t, d) in enumerate(NAV)]
    nav = FX("hd-nav", navlinks, "width: auto; gap: 1.8rem; align-items: center; margin-inline-start: auto; @media(--tablet) { display: none; }", tag="nav")
    cta = BTN("hd-cta", "Request a Free Estimate", QUOTE, css="min-height: 46px; padding-inline-start: 1.2rem; padding-inline-end: 1.2rem; font-size: 0.95rem; @media(--tablet) { margin-inline-start: auto; } @media(--mobile) { display: none; }")
    cta_m = BTN("hd-ctam", "Free Estimate", QUOTE, css="display: none; flex: none; min-height: 42px; padding-inline-start: 0.9rem; padding-inline-end: 0.9rem; font-size: 0.9rem; margin-inline-start: auto; @media(--mobile) { display: inline-flex; }")
    inner = FX("hd-in", [wordmark("hd-wm"), nav, cta, cta_m], WRAP + " gap: 1.75rem; align-items: center; min-height: 72px; @media(--mobile) { gap: 0.75rem; min-height: 64px; }")
    h = FX("hd", [inner], f"width: 100%; position: sticky; inset-block-start: 0px; z-index: 50; background-color: {INK}; border-width: 0px 0px 1px 0px; border-style: solid; border-color: {DLINE}; justify-content: center;", tag="header")
    h.cfg["_cssid"] = "top"; return h

# ---------- 2. hero: copy + contained photo (706px source, so never full-bleed) ----------
TYPES_CHIPS = ["Vinyl privacy", "Wood", "Chain link", "Gates"]
def hero():
    eb = P("hr-eb", "Orlando · Kissimmee · Altamonte Springs", f"display: inline-flex; width: auto; align-self: flex-start; font-family: {BODY}; font-weight: 600; font-size: 0.88rem; line-height: 1.2; color: {ONDARK}; background-color: rgba(91,180,236,0.12); border-width: 1px; border-style: solid; border-color: rgba(91,180,236,0.45); border-radius: 999px; padding-block-start: 0.45rem; padding-block-end: 0.45rem; padding-inline-start: 0.9rem; padding-inline-end: 0.9rem; @media(--mobile) {{ font-size: 0.78rem; }}")
    h1 = H("hr-h1", "Fence Installation <em>in Orlando</em>", "h1",
           f"color: {ONDARK}; font-size: 4.25rem; line-height: 0.98; max-width: 11ch; @media(--tablet) {{ font-size: 3.6rem; }} @media(--mobile) {{ font-size: 2.6rem; line-height: 1.02; }}")
    lede = P("hr-ld", "Vinyl privacy, wood and chain-link fencing, plus single and double gates, for homes across Orlando, Kissimmee and Altamonte Springs.",
             f"font-family: {BODY}; font-size: 1.2rem; line-height: 1.55; color: {ONDARK_M}; max-width: 44ch; @media(--mobile) {{ font-size: 1.05rem; }}")
    act = FX("hr-act", [BTN("hr-b1", "Request a Free Estimate", QUOTE, css="min-height: 58px; font-size: 1.08rem; padding-inline-start: 2rem; padding-inline-end: 2rem; @media(--mobile) { width: 100%; }"),
                        BTN("hr-b2", "See Our Work", "#work", kind="ghost", css="min-height: 58px; font-size: 1.08rem; @media(--mobile) { width: 100%; }")],
             "flex-wrap: wrap; gap: 0.75rem; margin-block-start: 0.4rem; @media(--mobile) { flex-direction: column; }")
    chips = FX("hr-ch", [P(f"hr-ch{i}", t, f"font-family: {BODY}; font-weight: 600; font-size: 0.85rem; line-height: 1; color: {ONDARK}; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 0.75rem; padding-inline-end: 0.75rem; border-radius: 8px; background-color: rgba(243,246,249,0.07); border-width: 1px; border-style: solid; border-color: {DLINE};", tag="span")
                         for i, t in enumerate(TYPES_CHIPS)], "flex-wrap: wrap; gap: 0.5rem; margin-block-start: 0.5rem;")
    copy = FX("hr-copy", [eb, h1, lede, act, chips], "flex-direction: column; gap: 1.25rem; min-width: 0px; @media(--mobile) { gap: 1rem; }")
    # photo: capped at 440 CSS px wide on desktop (706px source → ≥1.6 px per CSS px), full column width when stacked
    tag = FX("hr-tag", [DV("hr-tag-d", [], f"width: 8px; height: 8px; border-radius: 50%; background-color: {GOLD}; flex: none;"),
                        P("hr-tag-t", "Vinyl privacy · Orlando", "color: inherit;", tag="span")],
             f"position: absolute; width: auto; inset-inline-start: 14px; inset-block-end: 14px; align-items: center; gap: 0.5rem; font-family: {BODY}; font-weight: 600; font-size: 0.85rem; line-height: 1; color: {INK}; background-color: rgba(255,255,255,0.94); border-radius: 999px; padding-block-start: 0.5rem; padding-block-end: 0.5rem; padding-inline-start: 0.75rem; padding-inline-end: 0.9rem; box-shadow: 0px 6px 18px -8px rgba(15,28,46,0.5);")
    frame = DV("hr-ph", [IMG("Hero photo - Jenny vinyl corner", "vinyl-privacy-corner.jpg", FILL + " object-position: 50% 50%;"), tag],
               f"position: relative; width: 100%; max-width: 440px; aspect-ratio: 706 / 840; border-radius: 22px; overflow: hidden; background-color: {NAVY2}; box-shadow: 0px 40px 80px -30px rgba(0,0,0,0.65); border-width: 1px; border-style: solid; border-color: {DLINE}; margin-inline-start: auto; @media(--tablet) {{ max-width: 520px; margin-inline-start: 0px; }} @media(--mobile) {{ max-width: 100%; border-radius: 18px; }}")
    g = GR("hr-g", [copy, frame], "grid-template-columns: minmax(0,1.25fr) minmax(0,1fr); grid-template-rows: auto; gap: 4rem; align-items: center; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2.5rem; }")
    n = FX("hr", [FX("hr-w", [g], WRAP + " flex-direction: column; padding-block-start: 5rem; padding-block-end: 5.5rem; @media(--tablet) { padding-block-start: 3.5rem; padding-block-end: 4rem; } @media(--mobile) { padding-block-start: 2.25rem; padding-block-end: 2.75rem; }")],
           f"width: 100%; flex-direction: column; background-color: {INK}; background-image: radial-gradient(circle at 85% 20%, rgba(91,180,236,0.22) 0%, rgba(91,180,236,0) 45%), radial-gradient(circle at 0% 100%, rgba(232,185,49,0.12) 0%, rgba(232,185,49,0) 35%);", tag="section")
    n.cfg["_cssid"] = "hero"; return n

# ---------- 3. services: one photo per fence style ----------
# Three cards borrow sharp photos from the Branham Fencing demo (TJ OK'd it for this mockup). They carry an
# "Example fence style" chip, and their Navigator titles start with "SWAP" so they're easy to find and replace in
# Elementor when Jenny sends originals: click the image → choose the new photo, then delete the "Example label" element.
# Chain link has no Branham equivalent, so it uses Jenny's own chain-link job (labelled as her work).
BRANHAM = json.load(open(os.path.join(HERE, "..", "..", "2026-11-08-branham-demo", "native", "media-ids.json")))
def bmid(num): return BRANHAM[f"branham-demo-fence-{num}.jpg"]["id"]
SERVICES = [("vinyl", "01", "Vinyl privacy", "White and tan PVC privacy fencing with clean lines, for backyards, side yards and pool areas.", "Vinyl estimate",
             ("branham", "027", "50% 62%"), None),
            ("wood", "02", "Wood", "Pine privacy fencing with capped posts and matching walk gates, for a classic backyard look.", "Wood estimate",
             ("branham", "155", "50% 52%"), None),
            ("chain", "03", "Chain link", "Black chain-link fencing that marks the property line and keeps the view open.", "Chain-link estimate",
             ("jenny", "black-chain-link.jpg", "50% 42%"), "Our work · Orlando"),
            ("gates", "04", "Gates", "Single walk gates and wide double gates, on a new fence or added to one you have, so bigger items fit through.", "Gate estimate",
             ("branham", "151", "50% 60%"), None)]
def services():
    cards = []
    for i, (key, num, t, d, cta, (src, ref, pos), own) in enumerate(SERVICES):
        borrowed = src == "branham"
        img_cid = f"SWAP {t} photo - Branham example" if borrowed else f"{t} photo - Fence It Up"
        img = N("e-image", img_cid, {"image": {"src": {"id": bmid(ref) if borrowed else mid(ref)}, "size": "full"}}, FILL + f" object-position: {pos};")
        chip_text = "Example fence style" if borrowed else own
        chip = P(f"Example label - {t} - delete after swap" if borrowed else f"{t} label", chip_text,
                 f"position: absolute; width: auto; inset-inline-start: 10px; inset-block-end: 10px; font-family: {BODY}; font-weight: 600; font-size: 0.76rem; line-height: 1; letter-spacing: 0.01em; "
                 f"color: {INK if borrowed else ONDARK}; background-color: {'rgba(255,255,255,0.92)' if borrowed else 'rgba(15,28,46,0.85)'}; border-radius: 999px; padding-block-start: 0.4rem; padding-block-end: 0.4rem; padding-inline-start: 0.65rem; padding-inline-end: 0.65rem; box-shadow: 0px 4px 12px -6px rgba(15,28,46,0.5);", tag="span")
        ph = DV(f"sv{i}-ph", [img, chip], f"position: relative; overflow: hidden; aspect-ratio: 4 / 3; width: 100%; background-color: {LINE}; flex: none;")
        body = FX(f"sv{i}-b", [
            FX(f"sv{i}-top", [P(f"sv{i}-n", num, f"font-family: {DISP}; font-weight: 800; font-size: 0.95rem; color: {SKY_D};"),
                              DV(f"sv{i}-ln", [], f"flex: 1 1 auto; height: 2px; background-color: {LINE};")], "align-items: center; gap: 0.75rem;"),
            H(f"sv{i}-h", t, "h3", "font-size: 1.5rem;"),
            P(f"sv{i}-p", d, f"font-family: {BODY}; font-size: 0.97rem; line-height: 1.55; color: {MUTED}; flex: 1 1 auto;"),
            # _cssid q-<type> lets the page snippet preselect this fence type in the form
            P(f"sv{i}-q", cta + " →", f"font-family: {BODY}; font-weight: 700; font-size: 0.95rem; color: {SKY_D}; text-decoration: none; margin-block-start: 0.3rem; &:hover {{ color: {INK}; }} {FOCUS}", tag="span", link=L(QUOTE))],
            "flex-direction: column; gap: 0.7rem; padding: 1.3rem; padding-block-end: 1.4rem; flex: 1 1 auto;")
        body.kids[-1].cfg["_cssid"] = f"q-{key}"
        cards.append(FX(f"sv{i}", [ph, body],
            f"flex-direction: column; gap: 0px; background-color: {CARD}; border-radius: 16px; overflow: hidden; border-width: 1px; border-style: solid; border-color: {LINE}; min-width: 0px; transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s; &:hover {{ border-color: {SKY}; transform: translateY(-2px); box-shadow: 0px 18px 36px -24px rgba(15,28,46,0.45); }}"))
    g = GR("sv-g", cards, "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: auto; gap: 1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(4, auto); gap: 0.85rem; }")
    note = P("sv-note", "Photos marked “Example fence style” show the style only. Fence It Up’s own jobs are in Recent projects below.",
             f"font-family: {BODY}; font-size: 0.86rem; line-height: 1.5; color: {MUTED}; margin-block-start: 1.1rem;")
    return SEC("sv", "services", [HEAD("sv-hd", "What we install", "Fencing and gates for Central Florida homes",
                                       "Vinyl, wood, chain link and gates. Pick a style, or tell us about your yard and we’ll help you choose."), g, note])

# ---------- 4. work: Jenny's own jobs, one photo per card, type + post location ----------
WORK = [("pool-backyard-vinyl.jpg", "Vinyl privacy", "Orlando", "50% 50%"),
        ("double-gate-sunset.jpg", "Double gate", "Kissimmee", "50% 55%"),
        ("wood-privacy-gate.jpg", "Wood privacy &amp; walk gate", "Orlando", "50% 50%"),
        ("side-yard-walkway.jpg", "Vinyl privacy", "Orlando", "50% 60%")]
def work():
    cards = []
    for i, (img, t, loc, pos) in enumerate(WORK):
        ph = DV(f"wk{i}-ph", [IMG(f"wk{i}-i", img, FILL + f" object-position: {pos}; transition: transform 0.4s; &:hover {{ transform: scale(1.03); }}")],
                f"position: relative; overflow: hidden; aspect-ratio: 1 / 1; width: 100%; background-color: {LINE};")
        cap = FX(f"wk{i}-b", [P(f"wk{i}-t", t, f"font-family: {BODY}; font-weight: 700; font-size: 0.98rem; line-height: 1.25; color: {INK}; @media(--mobile) {{ font-size: 0.9rem; }}"),
                              P(f"wk{i}-l", loc + ", FL", f"font-family: {BODY}; font-size: 0.86rem; line-height: 1.3; color: {MUTED}; @media(--mobile) {{ font-size: 0.8rem; }}")],
                 "flex-direction: column; gap: 0.2rem; padding-block-start: 0.85rem; padding-block-end: 1rem; padding-inline-start: 1rem; padding-inline-end: 1rem; @media(--mobile) { padding-inline-start: 0.75rem; padding-inline-end: 0.75rem; padding-block-start: 0.65rem; padding-block-end: 0.8rem; }")
        cards.append(FX(f"wk{i}", [ph, cap], f"flex-direction: column; background-color: {CARD}; border-radius: 14px; overflow: hidden; border-width: 1px; border-style: solid; border-color: {LINE}; min-width: 0px;"))
    g = GR("wk-g", cards, "grid-template-columns: repeat(4, minmax(0,1fr)); grid-template-rows: auto; gap: 1.25rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; gap: 1rem; } @media(--mobile) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: auto auto; gap: 0.65rem; }")
    foot = FX("wk-ft", [P("wk-ig", "See more on Instagram: @fenceitupllc ↗", f"font-family: {BODY}; font-weight: 700; font-size: 1rem; color: {SKY_D}; text-decoration: none; &:hover {{ color: {INK}; }} {FOCUS}", link=L(IG, True)),
                        BTN("wk-cta", "Request a Free Estimate", QUOTE, kind="navy", css="@media(--mobile) { width: 100%; }")],
               "justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-block-start: 2rem; @media(--mobile) { flex-direction: column; align-items: flex-start; }")
    return SEC("wk", "work", [HEAD("wk-hd", "Recent projects", "Fences we’ve put up around Orlando",
                                   "Real jobs from our Instagram, labelled by fence type and the area each project was posted from."), g, foot],
               f"background-color: {CARD};")

# ---------- 5. why: paraphrased from Fence It Up's own captions ----------
WHY = [("Permits done right", "Permits done the right way means no fines and no stress for you down the road."),
       ("Quality materials, clean installs", "Quality materials, clean installation and results you can trust, on vinyl, wood and chain link."),
       ("Built around your yard", "One client needed more room, so we added a double gate wide enough for bigger items.")]
def why():
    items = [FX(f"wy{i}", [P(f"wy{i}-n", f"0{i+1}", f"display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; flex: none; border-radius: 12px; background-color: rgba(232,185,49,0.14); border-width: 1px; border-style: solid; border-color: rgba(232,185,49,0.5); font-family: {DISP}; font-weight: 800; font-size: 0.95rem; color: {GOLD};"),
                           H(f"wy{i}-h", t, "h3", f"font-size: 1.45rem; color: {ONDARK};"),
                           P(f"wy{i}-p", d, f"font-family: {BODY}; font-size: 1rem; line-height: 1.6; color: {ONDARK_M};")],
                f"flex-direction: column; gap: 0.85rem; padding: 1.6rem; border-radius: 16px; background-color: rgba(243,246,249,0.04); border-width: 1px; border-style: solid; border-color: {DLINE}; min-width: 0px;")
             for i, (t, d) in enumerate(WHY)]
    g = GR("wy-g", items, "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; gap: 1rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(3, auto); gap: 0.75rem; }")
    return SEC("wy", "why", [HEAD("wy-hd", "Why Fence It Up", "Done right, from permit to final post", dark=True), g],
               f"background-color: {NAVY}; background-image: radial-gradient(circle at 100% 0%, rgba(91,180,236,0.16) 0%, rgba(91,180,236,0) 40%);")

# ---------- 6. estimate: copy + form mount (#fiu-form, filled by the page snippet) ----------
STEPS = [("Send your request", "Name, phone, ZIP code, fence type and a line or two about the project."),
         ("We follow up", "We get back to you to talk through the details of your project."),
         ("Get your free estimate", "A clear price for the fence and gates you want.")]
def estimate():
    steps = [FX(f"es{i}", [P(f"es{i}-n", str(i + 1), f"display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; flex: none; border-radius: 50%; background-color: {INK}; font-family: {DISP}; font-weight: 800; font-size: 0.9rem; color: {GOLD};"),
                           FX(f"es{i}-c", [P(f"es{i}-t", t, f"font-family: {BODY}; font-weight: 700; font-size: 1.02rem; color: {INK};"),
                                           P(f"es{i}-d", d, f"font-family: {BODY}; font-size: 0.95rem; line-height: 1.5; color: {MUTED};")], "flex-direction: column; gap: 0.2rem; min-width: 0px;")],
                f"gap: 0.9rem; align-items: flex-start;") for i, (t, d) in enumerate(STEPS)]
    note = FX("es-nt", [P("es-nt-k", "Demo", f"font-family: {BODY}; font-weight: 700; font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: {INK}; background-color: {GOLD}; border-radius: 6px; padding-block-start: 0.3rem; padding-block-end: 0.3rem; padding-inline-start: 0.5rem; padding-inline-end: 0.5rem; flex: none;", tag="span"),
                        P("es-nt-t", "This is a website concept. Requests sent from this page aren’t delivered anywhere.", f"font-family: {BODY}; font-size: 0.9rem; line-height: 1.45; color: {MUTED};", tag="span")],
              f"gap: 0.7rem; align-items: center; padding: 0.85rem; border-radius: 12px; background-color: {TINT}; margin-block-start: 0.5rem;")
    copy = FX("es-copy", [EYEBROW("es-eb", "Free estimate"), H("es-h", "Tell us about your fence project", "h2", H2),
                          P("es-ld", "Share a few details about your yard and the fence you have in mind, and we’ll follow up.", LEDE),
                          FX("es-st", steps, "flex-direction: column; gap: 1.1rem; margin-block-start: 0.5rem;"), note],
              "flex-direction: column; gap: 1rem; min-width: 0px;")
    mount = DV("es-form", [P("es-form-fb", "The estimate form is loading…", f"font-family: {BODY}; font-size: 1rem; color: {MUTED};")], "min-height: 200px;")
    mount.cfg = {"_cssid": "fiu-form"}
    card = FX("es-card", [H("es-card-h", "Request a free estimate", "h3", "font-size: 1.6rem;"),
                          P("es-card-s", "Takes about a minute.", f"font-family: {BODY}; font-size: 0.95rem; color: {MUTED}; margin-block-end: 0.5rem;"), mount],
              f"flex-direction: column; gap: 0.35rem; padding: 2rem; background-color: {CARD}; border-radius: 20px; border-width: 1px; border-style: solid; border-color: {LINE}; box-shadow: 0px 30px 60px -36px rgba(15,28,46,0.45); min-width: 0px; @media(--mobile) {{ padding: 1.25rem; border-radius: 16px; }}")
    g = GR("es-g", [copy, card], "grid-template-columns: minmax(0,1fr) minmax(0,1.1fr); grid-template-rows: auto; gap: 4rem; align-items: start; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2.25rem; }")
    return SEC("es", "estimate", [g], f"background-color: {TINT};")

# ---------- 7. footer + mobile bar ----------
def footer():
    T = f"font-family: {BODY}; font-size: 0.93rem; line-height: 1.55; color: {ONDARK_M};"
    LK = f"font-family: {BODY}; font-weight: 600; font-size: 0.95rem; color: {ONDARK}; text-decoration: none; &:hover {{ color: {GOLD}; }} {FOCUS}"
    a = FX("fo-a", [wordmark("fo-wm"), P("fo-d", "Vinyl privacy, wood and chain-link fences and gates in Orlando, Kissimmee and Altamonte Springs, Florida.", T + " max-width: 40ch;")],
           "flex-direction: column; gap: 1rem; min-width: 0px;")
    b = FX("fo-b", [P("fo-ig", "Instagram: @fenceitupllc ↗", LK, link=L(IG, True)), P("fo-q", "Request a Free Estimate", LK, link=L(QUOTE)),
                    P("fo-w", "Recent projects", LK, link=L("#work"))], "flex-direction: column; gap: 0.6rem; min-width: 0px;")
    g = GR("fo-g", [a, b], "grid-template-columns: minmax(0,2fr) minmax(0,1fr); grid-template-rows: auto; gap: 2.5rem; @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 1.75rem; }")
    fine = FX("fo-fine", [P("fo-cp", "© 2026 Fence It Up LLC", T + " font-size: 0.82rem;"),
                          P("fo-ax", "Website concept by Axiom Systems. Demo only.", T + " font-size: 0.82rem;")],
              f"justify-content: space-between; gap: 0.5rem; flex-wrap: wrap; margin-block-start: 2.5rem; padding-block-start: 1.5rem; border-width: 1px 0px 0px 0px; border-style: solid; border-color: {DLINE};")
    return FX("fo", [FX("fo-w2", [g, fine], WRAP + " flex-direction: column;")],
              f"width: 100%; background-color: {INK}; padding-block-start: 4rem; padding-block-end: 3rem; flex-direction: column; @media(--tablet) {{ padding-block-end: 7rem; }}", tag="footer")

def mobilebar():
    return FX("mb", [BTN("mb-q", "Request a Free Estimate", QUOTE, css="flex: 1 1 auto; min-height: 52px; font-size: 1rem; box-shadow: 0px 0px 0px 0px rgba(0,0,0,0);")],
              # The bar stops 84px short of the right edge, so the site chat bubble (58px, 20px from the edge) keeps that corner.
              # z-index sits above the chat's invisible greeting box (z 99999999), which otherwise swallows taps on the button.
              # The page snippet hides the bar while the chat is open or the estimate form is on screen.
              f"display: none; position: fixed; width: auto; inset-inline-start: 0px; inset-inline-end: 84px; inset-block-end: 0px; z-index: 100000000; flex-direction: row; padding: 8px; background-color: rgba(15,28,46,0.95); backdrop-filter: blur(10px); border-width: 1px 1px 0px 0px; border-style: solid; border-color: {DLINE}; border-radius: 0px 14px 0px 0px; @media(--tablet) {{ display: flex; }}", tag="nav", _cssid="fiu-bar")

def root():
    return FX("fiu", [header(), hero(), services(), work(), why(), estimate(), footer(), mobilebar()],
              f"width: 100%; max-width: 100%; flex-direction: column; gap: 0px; background-color: {PAPER}; color: {INK}; font-family: {BODY};")

if __name__ == "__main__":
    r = root(); k = {n.cid: n for n in r.kids}
    shell = N("e-flexbox", "fiu", None, r.css, [k["hd"], k["hr"]])
    batches = {"A": [shell], "B": [k["sv"], k["wk"]], "C": [k["wy"], k["es"]], "D": [k["fo"], k["mb"]]}
    for name, nodes in batches.items():
        ps = [payload(n) for n in nodes]; out = {"xml_structure": "".join(p["xml_structure"] for p in ps), "element_config": {}, "style": {}}
        for p in ps: out["element_config"].update(p["element_config"]); out["style"].update(p["style"])
        json.dump(out, open(os.path.join(HERE, f"{name}.json"), "w"), ensure_ascii=False); print(name, len(json.dumps(out, ensure_ascii=False)))
