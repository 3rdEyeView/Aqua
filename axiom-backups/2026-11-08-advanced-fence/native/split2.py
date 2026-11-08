import json, gen2
from gen2 import payload
r = gen2.root(); k = {n.cid: n for n in r.kids}
wk = k["wk"]; cards = {}
def strip(n):
    for c in n.kids:
        if c.cid.startswith("wk-c") and c.cid.endswith("-g"): cards[c.cid] = c.kids; c.kids = []
        else: strip(c)
strip(wk)
def dump(name, nodes):
    ps = [payload(n) for n in nodes]; out = {"xml_structure": "".join(p["xml_structure"] for p in ps), "element_config": {}, "style": {}}
    for p in ps: out["element_config"].update(p["element_config"]); out["style"].update(p["style"])
    json.dump(out, open(f"v2-{name}.json", "w"), ensure_ascii=False); print(name, len(json.dumps(out, ensure_ascii=False)))
dump("B", [wk])
for cid, kids in cards.items(): dump(cid, kids)
