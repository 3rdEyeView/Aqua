import json, gen
from gen import *
r = root()
k = {n.cid: n for n in r.kids}
def dump(name, obj): json.dump(obj, open(f"call-{name}.json", "w"), ensure_ascii=False); print(name, len(json.dumps(obj, ensure_ascii=False)))
shell = FX("bfc", [k["hd"], k["hr"], k["sp"]], r.css.replace("padding: 0px; ", "", 0)); shell.css = r.css
dump("A", payload(shell))
dump("B", payload(k["ft"])); dump("C", payload(k["pk"])); dump("D", payload(k["ty"]))
# gallery skeleton: strip tiles
g = k["gl"]
tiles = {}
def strip(n):
    for c in n.kids:
        if c.cls == ["bfc-gallery"]:
            tiles[c.cid] = c.kids; c.kids = []
        else: strip(c)
strip(g)
dump("E", payload(g))
for cid, ts in tiles.items():
    wrapper = [payload(t) for t in ts]
    # merge tiles into a single payload (multiple roots allowed? use one call per tile list via fake container check)
    xml = "".join(w["xml_structure"] for w in wrapper)
    cfg = {}; cl = {}
    for w in wrapper: cfg.update(w["element_config"]); cl.update(w.get("classes", {}))
    dump("T-" + cid, {"xml_structure": xml, "element_config": cfg, "classes": cl})
dump("F", payload(k["ab"])); dump("G", payload(k["es"])); dump("H", payload(k["bd"])); dump("I", payload(k["fo"])); dump("J", payload(k["mb"]))
