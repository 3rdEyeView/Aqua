"""v2 of the Advanced Fence demo: original photos only (8 kept from the Angi set), each used once; text-led hero.
Reuses header/spec/estimate/footer/mobile bar and helpers from gen.py."""
import json, os
import gen
from gen import (N, payload, L, P, H, BTN, FX, DV, GR, IMG, PH, SEC, HEAD, BRAND, TICKET, EYEBROW, LEDE, H2, WRAP, FOCUS,
                 NIGHT, NIGHT2, PAPER, CARD, INK, MUTED, LINE, COPPER, COPPER_D, ONDARK, ONDARK_M, DISP, BODY, TAG, FILL)
HERE = os.path.dirname(os.path.abspath(__file__))

# name, category, title, alt, ticket pairs — wording describes only what the photo shows
PHOTOS = [
    ("wood-fence-corner", "Wood privacy", "Privacy fence with a framed drive gate", "Wood privacy fence wrapping a side yard with a wide steel-framed gate",
     [("Style", "Privacy, rail side shown"), ("Gate", "Wide steel-framed gate"), ("Setting", "Side yard, brick home")]),
    ("wood-privacy-fence", "Wood privacy", "Arched privacy along a garden path", "Wood privacy fence with arched sections and capped posts along a curved path",
     [("Style", "Arched sections, capped posts"), ("Material", "Pressure-treated pine"), ("Setting", "Curved line beside a path")]),
    ("wood-fence-backyard", "Wood privacy", "Backyard privacy with walk gate", "Wood privacy fence closing in a backyard with a walk gate in the center",
     [("Style", "Privacy with walk gate"), ("Material", "Pressure-treated pine"), ("Setting", "New-build backyard")]),
    ("black-pool-fence", "Metal & pool", "Black metal pool enclosure", "Black metal fence enclosing an in-ground pool",
     [("Style", "Flat-top picket"), ("Material", "Black metal"), ("Use", "Pool enclosure")]),
    ("black-fence-stone-columns", "Metal & pool", "Black metal between brick columns", "Black metal fence running between white brick columns",
     [("Style", "Flat-top picket"), ("Material", "Black metal"), ("Extras", "Brick columns")]),
    ("metal-fence-poolside", "Metal & pool", "White metal pool fence", "White metal fence around a pool deck",
     [("Style", "Flat-top picket"), ("Material", "White metal"), ("Use", "Pool deck")]),
    ("metal-fence-garden", "Metal & pool", "White metal on a brick wall", "White metal fence set on a brick wall above a planted bed",
     [("Style", "Flat-top picket"), ("Material", "White metal"), ("Set", "Brick wall, planted bed")]),
    ("white-vinyl-yard", "Vinyl", "White vinyl with lattice top", "White vinyl privacy fence with a lattice top along a yard",
     [("Style", "Privacy, lattice top"), ("Material", "White vinyl"), ("Setting", "Open side yard")]),
]
CATS = ["Wood privacy", "Metal & pool", "Vinyl"]
assert len(PHOTOS) == 8 and len({p[0] for p in PHOTOS}) == 8
assert all(os.path.exists(os.path.join(HERE, "..", "img", f"advanced-demo-{p[0]}.jpg")) for p in PHOTOS)

def hero():
    copy = FX("hr-copy", [
        P("hr-eb", "Fence contractor · Columbia, SC", EYEBROW + f" color: {COPPER};"),
        H("hr-h1", "Fences done right,", "h1", f"color: {ONDARK}; font-weight: 600; font-size: 5rem; @media(--tablet) {{ font-size: 4rem; }} @media(--mobile) {{ font-size: 2.7rem; }}"),
        P("hr-h1b", "gate to post.", f"font-family: {DISP}; font-weight: 600; line-height: 1.02; text-transform: uppercase; color: {COPPER}; font-size: 5rem; margin-block-start: -1.2rem; @media(--tablet) {{ font-size: 4rem; }} @media(--mobile) {{ font-size: 2.7rem; margin-block-start: -0.9rem; }}"),
        P("hr-ld", "Wood privacy, vinyl, metal and pool fencing, chain link and split rail, plus gates, for homes and businesses around Columbia.",
          f"font-family: {BODY}; font-size: 1.2rem; line-height: 1.6; color: {ONDARK_M}; max-width: 52ch; @media(--mobile) {{ font-size: 1.08rem; }}"),
        FX("hr-act", [BTN("hr-b1", "Get a free estimate", "#estimate"), BTN("hr-b2", "See recent projects", "#work", kind="ghost-dark")], "flex-wrap: wrap; gap: 0.75rem;"),
    ], "flex-direction: column; gap: 1.4rem; min-width: 0px;")
    emblem = IMG("hr-logo", "logo-facebook.jpg", "Advanced Fence Service emblem",
                 f"width: 320px; height: 320px; max-width: 100%; object-fit: cover; border-radius: 50%; display: block; border-width: 1px; border-style: solid; border-color: #3A342E; @media(--tablet) {{ width: 240px; height: 240px; }} @media(--mobile) {{ width: 160px; height: 160px; }}")
    g = GR("hr-g", [copy, FX("hr-em", [emblem], "justify-content: center; align-items: center; @media(--tablet) { justify-content: flex-start; }")],
           "grid-template-columns: minmax(0,7fr) minmax(0,4fr); grid-template-rows: auto; align-items: center; gap: 4rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 2.5rem; }")
    rule = DV("hr-rule", [], f"height: 4px; width: 100%; background-image: linear-gradient(90deg, {COPPER_D} 0%, {COPPER} 50%, {COPPER_D} 100%);")
    w = FX("hr-w", [g], WRAP + " flex-direction: column; padding-block-start: 6rem; padding-block-end: 6rem; @media(--mobile) { padding-block-start: 3.5rem; padding-block-end: 3.5rem; }")
    return FX("hr", [w, rule], f"width: 100%; background-color: {NIGHT}; flex-direction: column;", tag="section")

def card(i, p):
    n, cat, title, alt, pairs = p
    return FX(f"pc{i}", [PH(f"pc{i}-ph", f"{n}.jpg", alt, "aspect-ratio: 4 / 3; width: 100%;"),
                         FX(f"pc{i}-b", [P(f"pc{i}-c", cat.replace("&", "&amp;"), EYEBROW + " font-size: 0.68rem;"), H(f"pc{i}-h", title, "h3", "font-size: 1.35rem; line-height: 1.1;"), TICKET(f"pc{i}-t", pairs)],
                            "flex-direction: column; gap: 0.75rem; padding-block-start: 1.25rem; padding-block-end: 1.5rem; padding-inline-start: 1.25rem; padding-inline-end: 1.25rem;")],
              f"flex-direction: column; background-color: {CARD}; border-width: 1px; border-style: solid; border-color: {LINE}; border-radius: 3px; overflow: hidden; text-decoration: none; min-width: 0px; width: 100%; max-width: 400px; cursor: zoom-in; {FOCUS} &:hover {{ border-color: {COPPER_D}; }}",
              tag="a", link=L(gen.U + f"{n}.jpg", True))

TAB = gen.TAB
def work():
    groups = [(c, [(i, p) for i, p in enumerate(PHOTOS) if p[1] == c]) for c in CATS]
    menu, panels = [], []
    for gi, (name, ps) in enumerate(groups):
        nm = name.replace("&", "&amp;")
        menu.append(N("e-tab", f"wk-t{gi}", None, TAB, [P(f"wk-t{gi}-l", f"{nm} · {len(ps)}", "color: inherit;", tag="span")]))
        note = f"{nm} · {len(ps)} {'photo' if len(ps) == 1 else 'photos'}"
        panels.append(N("e-tab-content", f"wk-c{gi}", None, "padding: 0px; width: 100%;", [
            P(f"wk-c{gi}-n", note, EYEBROW + " margin-block-end: 1rem;"),
            GR(f"wk-c{gi}-g", [card(i, p) for i, p in ps],
               "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; gap: 1.5rem; justify-items: start; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); } @media(--mobile) { grid-template-columns: minmax(0,1fr); justify-items: center; }")]))
    tabs = N("e-tabs", "wk-tabs", {"default-active-tab": 0}, "gap: 1.5rem; padding: 0px;", [
        N("e-tabs-menu", "wk-menu", None, "justify-content: flex-start; flex-wrap: wrap; gap: 0.5rem; padding-block-end: 0.5rem;", menu),
        N("e-tabs-content-area", "wk-area", None, "padding: 0px;", panels)])
    note = P("wk-note", f"{len(PHOTOS)} finished jobs, sorted by fence type. Tap a photo to open it on its own.", f"font-family: {BODY}; font-size: 0.95rem; color: {MUTED}; margin-block-start: 1.5rem;")
    return SEC("wk", "work", [HEAD("wk-hd", "Recent projects", "Fences we've built", "Finished Advanced Fence Service jobs around Columbia and the Midlands."), tabs, note])

def types():
    items = [("Wood privacy", "Pressure-treated pine privacy fences with walk and drive gates, built straight across sloped and curved lines."),
             ("Metal &amp; pool", "Black and white metal fencing for pools, front yards and brick-column runs."),
             ("Vinyl", "Low-maintenance white vinyl privacy fencing, including lattice-top styles."),
             ("Chain link", "Galvanized and coated chain link for yards, businesses and commercial lots."),
             ("Split rail &amp; gates", "Split rail for open lots, plus walk gates and drive gates built to match the fence.")]
    k = [FX(f"ty{i}", [P(f"ty{i}-n", f"0{i+1}", f"font-family: {TAG}; font-size: 0.75rem; letter-spacing: 0.12em; color: {COPPER_D};"),
                       H(f"ty{i}-h", t, "h3", "font-size: 1.45rem; line-height: 1.1;"), P(f"ty{i}-p", d, f"font-family: {BODY}; font-size: 0.98rem; line-height: 1.6; color: {MUTED};")],
            f"flex-direction: column; gap: 0.6rem; padding: 1.5rem; background-color: {CARD}; border-style: solid; border-color: {COPPER_D}; border-width: 3px 0px 0px 0px; min-width: 0px;")
         for i, (t, d) in enumerate(items)]
    g = GR("ty-g", k, "grid-template-columns: repeat(5, minmax(0,1fr)); grid-template-rows: auto; gap: 1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(3, auto); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(5, auto); }")
    return SEC("ty", "types", [HEAD("ty-hd", "What we build", "Fence types"), g], f"background-color: {CARD}; border-style: solid; border-color: {LINE}; border-width: 1px 0px 1px 0px;")

def owner():
    g = GR("ow-g", [FX("ow-l", [P("ow-eb", "Talk to the owner", EYEBROW), H("ow-h", "Call Chris, not a call center.", "h2", H2)], "flex-direction: column; gap: 0.9rem; min-width: 0px;"),
                    FX("ow-c", [P("ow-ld", "Advanced Fence Service is Chris's fence company in Columbia. You talk to him about the job, the materials and the price, and he's who you call when it's done.", LEDE),
                                P("ow-p", "Wood, vinyl, metal or chain link, the work is the same: posts set solid, lines straight and gates that close the way they should.", f"font-family: {BODY}; font-size: 1.0625rem; line-height: 1.6; color: {INK}; max-width: 62ch;")],
                       "flex-direction: column; gap: 1.2rem; min-width: 0px;")],
           "grid-template-columns: minmax(0,5fr) minmax(0,7fr); grid-template-rows: auto; align-items: start; gap: 4rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 1.5rem; }")
    return SEC("ab", "about", [g])

def band():
    copy = FX("bd-c", [H("bd-h", "Need a fence up?", "h2", H2 + f" color: {ONDARK};"), P("bd-p", "Tell Chris what you're after and he'll get back to you with a price.", f"font-family: {BODY}; font-size: 1.0625rem; line-height: 1.6; color: {ONDARK_M};")],
              "flex-direction: column; gap: 1rem; min-width: 0px; flex: 1 1 auto;")
    w = FX("bd-w", [copy, BTN("bd-b", "Get a free estimate", "#estimate")], WRAP + " gap: 2.5rem; align-items: center; justify-content: space-between; @media(--tablet) { flex-direction: column; align-items: flex-start; }")
    return FX("bd", [w], f"width: 100%; background-color: {NIGHT}; border-style: solid; border-color: {COPPER_D}; border-width: 4px 0px 0px 0px; padding-block-start: 5rem; padding-block-end: 5rem; flex-direction: column; @media(--mobile) {{ padding-block-start: 3.5rem; padding-block-end: 3.5rem; }}", tag="section")

def root():
    return FX("afs", [gen.header(), hero(), gen.spec(), work(), types(), owner(), gen.estimate(), band(), gen.footer(), gen.mobilebar()],
              f"width: 100%; max-width: 100%; flex-direction: column; gap: 0px; background-color: {PAPER}; color: {INK};")

if __name__ == "__main__":
    r = root(); k = {n.cid: n for n in r.kids}
    shell = N("e-flexbox", "afs", None, r.css, [k["hd"], k["hr"], k["sp"]])
    batches = {"A": [shell], "B": [k["wk"]], "C": [k["ty"], k["ab"]], "D": [k["es"]], "E": [k["bd"], k["fo"], k["mb"]]}
    for name, nodes in batches.items():
        ps = [payload(n) for n in nodes]; out = {"xml_structure": "".join(p["xml_structure"] for p in ps), "element_config": {}, "style": {}}
        for p in ps: out["element_config"].update(p["element_config"]); out["style"].update(p["style"])
        json.dump(out, open(os.path.join(HERE, f"v2-{name}.json"), "w"), ensure_ascii=False); print(name, len(json.dumps(out, ensure_ascii=False)))
