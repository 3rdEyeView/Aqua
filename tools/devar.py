#!/usr/bin/env python3
"""Replace V4 global-variable references in a page's stored Elementor styles with literal values.
Needed because this site's Elementor does not print V4 variables on the front end.
Usage: tools/devar.py <page_id> [<page_id> ...]
"""
import json, os, sys, urllib.request

LIT = {  # variable id -> (prop type, literal value)
    "e-gv-46c4d4e": ("color", "#FF6123"), "e-gv-3a7d295": ("color", "#E2470C"),
    "e-gv-7d36bc2": ("color", "#04293A"), "e-gv-f4fc840": ("color", "#0A3D62"),
    "e-gv-e1a6203": ("color", "#0B1F29"), "e-gv-d429799": ("color", "#F7F2EA"),
    "e-gv-4dadace": ("color", "#FFFFFF"), "e-gv-9456264": ("color", "#13B5BF"),
    "e-gv-e304616": ("color", "#51646D"),
    "e-gv-0b9d441": ("string", "Barlow Condensed"), "e-gv-b4900d4": ("string", "Manrope"),
}


def req(url, data=None):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, method="POST" if data else "GET",
                               headers={"User-Agent": "XtremeAudit-Claude/1.0", "Content-Type": "application/json",
                                        "Authorization": "Basic " + os.environ["XTREME_WP_BASIC_AUTH"]})
    with urllib.request.urlopen(r, timeout=90) as resp:
        return json.loads(resp.read())


def fix(o, n):
    if isinstance(o, dict):
        if o.get("$$type") in ("global-font-variable", "global-color-variable") and o.get("value") in LIT:
            t, v = LIT[o["value"]]
            n[0] += 1
            return {"$$type": t, "value": v}
        return {k: fix(v, n) for k, v in o.items()}
    if isinstance(o, list):
        return [fix(v, n) for v in o]
    return o


for pid in sys.argv[1:]:
    url = f"https://xtremestpete.com/wp-json/wp/v2/pages/{pid}"
    raw = req(url + "?context=edit&_fields=meta")["meta"]["_elementor_data"]
    n = [0]
    new = json.dumps(fix(json.loads(raw), n), ensure_ascii=False, separators=(",", ":"))
    if n[0]:
        req(url + "?_fields=id", {"meta": {"_elementor_data": new}})
    left = new.count("global-font-variable") + new.count("global-color-variable")
    print(pid, "replaced", n[0], "remaining var refs", left)
