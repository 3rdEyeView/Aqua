"""v3 of the Advanced Fence demo: 26 job photos from the owner's own uploads (one strong shot per job plus workmanship
details), a full-bleed photo hero, and an owner photo in About. Only the hero, gallery, fence types and About change
from v2; header, spec strip, estimate, band, footer and mobile bar are kept as published.
Writes v3-*.json payloads for build-composition; cards use the afs-card* kit classes to keep payloads small."""
import json, os
import gen, gen2
from gen import N, payload, L, P, H, FX, DV, GR, IMG, PH, SEC, HEAD, EYEBROW, LEDE, H2, INK, MUTED, CARD, LINE, COPPER_D, BODY, TAG, U
from photos_v3 import SEL, CATS, HERO, OWNER
HERE = os.path.dirname(os.path.abspath(__file__))
assert len(SEL) == 26 and len({s[1] for s in SEL}) == 26 and {s[2] for s in SEL} == set(CATS)
for s in SEL + [HERO, OWNER]: assert os.path.exists(os.path.join(HERE, "..", "img", f"advanced-demo-{s[1]}.jpg")), s

def hero():
    h = gen.hero()  # v1 photo hero layout; swap in the new wide shot
    bg = h.kids[0]; assert bg.cid == "hr-bg"
    bg.cfg = {"image": {"src": {"url": U + f"{HERO[1]}.jpg", "alt": "Scalloped-top wood privacy fence with post caps running along a new backyard"}, "size": "full"}}
    bg.css = gen.FILL + " object-position: 55% 62%; @media(--mobile) { object-position: 72% 60%; }"
    return h

def card(i, s):
    n, slug, cat, y, title, alt, pairs = s
    url = U + f"{slug}.jpg"
    t = []
    for k, (a, b) in enumerate(pairs):
        t += [N("e-paragraph", f"q{i}-k{k}", {"paragraph": a, "tag": "p"}, "", cls=["afs-card-k"]),
              N("e-paragraph", f"q{i}-v{k}", {"paragraph": b.replace("&", "&amp;"), "tag": "p"}, "", cls=["afs-card-v"])]
    img = N("e-image", f"q{i}-i", {"image": {"src": {"url": url, "alt": alt}, "size": "full"}}, f"object-position: 50% {y}%;", cls=["afs-card-img"])
    body = N("e-flexbox", f"q{i}-b", None, "", [
        N("e-paragraph", f"q{i}-c", {"paragraph": cat.replace("&", "&amp;"), "tag": "p"}, "", cls=["afs-card-c"]),
        N("e-heading", f"q{i}-h", {"title": title, "tag": "h3"}, "", cls=["afs-card-h"]),
        N("e-grid", f"q{i}-t", None, "", t, cls=["afs-card-t"])], cls=["afs-card-b"])
    return N("e-flexbox", f"q{i}", {"tag": "a", "link": L(url, True)}, "", [N("e-div-block", f"q{i}-ph", None, "", [img], cls=["afs-card-ph"]), body], cls=["afs-card"])

GRID = "grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: auto; gap: 1.5rem; justify-items: start; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); } @media(--mobile) { grid-template-columns: minmax(0,1fr); justify-items: center; }"
def groups(): return [(c, [(i, s) for i, s in enumerate(SEL) if s[2] == c]) for c in CATS]
def work(with_cards=True):
    menu, panels = [], []
    for gi, (name, ps) in enumerate(groups()):
        nm = name.replace("&", "&amp;")
        menu.append(N("e-tab", f"xk-t{gi}", None, gen.TAB, [P(f"xk-t{gi}-l", f"{nm} · {len(ps)}", "color: inherit;", tag="span")]))
        panels.append(N("e-tab-content", f"xk-c{gi}", None, "padding: 0px; width: 100%;", [
            P(f"xk-c{gi}-n", f"{nm} · {len(ps)} {'photo' if len(ps) == 1 else 'photos'}", EYEBROW + " margin-block-end: 1rem;"),
            GR(f"xk-c{gi}-g", [card(i, s) for i, s in ps] if with_cards else [], GRID)]))
    tabs = N("e-tabs", "xk-tabs", {"default-active-tab": 0}, "gap: 1.5rem; padding: 0px;", [
        N("e-tabs-menu", "xk-menu", None, "justify-content: flex-start; flex-wrap: wrap; gap: 0.5rem; padding-block-end: 0.5rem;", menu),
        N("e-tabs-content-area", "xk-area", None, "padding: 0px;", panels)])
    note = P("xk-note", f"{len(SEL)} photos from finished Advanced Fence Service jobs, sorted by type. Tap a photo to open it full size.",
             f"font-family: {BODY}; font-size: 0.95rem; color: {MUTED}; margin-block-start: 1.5rem;")
    return SEC("xk", "work", [HEAD("xk-hd", "Recent projects", "Fences we've built", "Real jobs from around Columbia and the Midlands: privacy runs, gates, vinyl, aluminum, rail and commercial work."), tabs, note])

def types():
    items = [("Wood privacy", "Board-on-rail, dog-ear, shadowbox and capped privacy fences in pressure-treated pine, stepped to follow the grade."),
             ("Gates &amp; arbors", "Walk gates, double drive gates, arched metal driveway gates and pergola arbors with lattice sides."),
             ("Vinyl", "White vinyl privacy fencing with matching X-brace gates and black hinges and latches."),
             ("Aluminum &amp; pool", "Black aluminum picket fencing with self-latching gates, and privacy fencing around pools."),
             ("Rail, chain link &amp; commercial", "Rail fencing for wooded lots and farm lanes, chain link yards, and commercial gates and enclosures.")]
    k = [FX(f"tz{i}", [P(f"tz{i}-n", f"0{i+1}", f"font-family: {TAG}; font-size: 0.75rem; letter-spacing: 0.12em; color: {COPPER_D};"),
                       H(f"tz{i}-h", t, "h3", "font-size: 1.45rem; line-height: 1.1;"), P(f"tz{i}-p", d, f"font-family: {BODY}; font-size: 0.98rem; line-height: 1.6; color: {MUTED};")],
            f"flex-direction: column; gap: 0.6rem; padding: 1.5rem; background-color: {CARD}; border-style: solid; border-color: {COPPER_D}; border-width: 3px 0px 0px 0px; min-width: 0px;")
         for i, (t, d) in enumerate(items)]
    g = GR("tz-g", k, "grid-template-columns: repeat(5, minmax(0,1fr)); grid-template-rows: auto; gap: 1rem; @media(--tablet) { grid-template-columns: repeat(2, minmax(0,1fr)); grid-template-rows: repeat(3, auto); } @media(--mobile) { grid-template-columns: minmax(0,1fr); grid-template-rows: repeat(5, auto); }")
    return SEC("tz", "types", [HEAD("tz-hd", "What we build", "Fence types"), g], f"background-color: {CARD}; border-style: solid; border-color: {LINE}; border-width: 1px 0px 1px 0px;")

def owner():
    photo = PH("oz-ph", f"{OWNER[1]}.jpg", "Chris, owner of Advanced Fence Service, on a job with a core drill",
               "aspect-ratio: 4 / 5; width: 100%; max-width: 340px; border-radius: 3px; @media(--tablet) { max-width: 260px; }")
    photo.kids[0].css = gen.FILL + " object-position: 50% 35%;"
    left = FX("oz-l", [P("oz-eb", "Talk to the owner", EYEBROW), H("oz-h", "Call Chris, not a call center.", "h2", H2), photo],
              "flex-direction: column; gap: 1.2rem; min-width: 0px;")
    right = FX("oz-c", [P("oz-ld", "Advanced Fence Service is Chris's fence company in Columbia. You talk to him about the job, the materials and the price, and he's on site for the work.", LEDE),
                        P("oz-p", "Wood, vinyl, aluminum or chain link, the work is the same: posts set solid, lines straight and gates that close the way they should.", f"font-family: {BODY}; font-size: 1.0625rem; line-height: 1.6; color: {INK}; max-width: 62ch;")],
               "flex-direction: column; gap: 1.2rem; min-width: 0px; padding-block-start: 0.5rem;")
    g = GR("oz-g", [left, right], "grid-template-columns: minmax(0,5fr) minmax(0,7fr); grid-template-rows: auto; align-items: start; gap: 4rem; @media(--tablet) { grid-template-columns: minmax(0,1fr); grid-template-rows: auto auto; gap: 1.5rem; }")
    return SEC("oz", "about", [g])

def dump(name, nodes):
    ps = [payload(n) for n in nodes]; out = {"xml_structure": "".join(p["xml_structure"] for p in ps), "element_config": {}, "style": {}, "classes": {}}
    for p in ps: out["element_config"].update(p["element_config"]); out["style"].update(p["style"]); out["classes"].update(p.get("classes", {}))
    json.dump(out, open(os.path.join(HERE, f"v3-{name}.json"), "w"), ensure_ascii=False); print(name, len(json.dumps(out, ensure_ascii=False)))

if __name__ == "__main__":
    dump("hero-types-about", [hero(), types(), owner()])
    dump("work-shell", [work(with_cards=False)])
    for gi, (name, ps) in enumerate(groups()):
        dump(f"cards-{gi}", [card(i, s) for i, s in ps]); print("  ", name, len(ps))
