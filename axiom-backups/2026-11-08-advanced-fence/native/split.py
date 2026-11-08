import json, gen
r = gen.root()
def strip(n):
    for c in n.kids:
        if c.cls == ["afs-gallery"]: c.kids = []
        else: strip(c)
strip(r)
k = {n.cid: n for n in r.kids}
shell = gen.N("e-flexbox", "afs", None, r.css, [k["hd"], k["hr"], k["sp"]])
batches = {"A": [shell], "B": [k["ft"], k["ty"]], "C": [k["gl"]], "D": [k["ab"], k["es"]], "E": [k["bd"], k["fo"], k["mb"]]}
for name, nodes in batches.items():
    ps = [gen.payload(n) for n in nodes]; out = {"xml_structure": "".join(p["xml_structure"] for p in ps), "element_config": {}, "style": {}, "classes": {}}
    for p in ps: out["element_config"].update(p["element_config"]); out["style"].update(p["style"]); out["classes"].update(p.get("classes", {}))
    json.dump(out, open(f"batch-{name}.json", "w"), ensure_ascii=False); print(name, len(json.dumps(out, ensure_ascii=False)))
