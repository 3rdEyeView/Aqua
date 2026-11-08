"""Builds page 1716 from A..E.json: replaces the document with A (shell, top bars, header, hero), then appends B..E inside the shell."""
import json, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import axmcp as mcp
PID = 1716
mcp.init(); log = {}
def bc(name, **kw):
    r = mcp.call("elementor-build-composition", {"post_id": PID, **json.load(open(f"{name}.json")), **kw})
    if "error" in r or not r.get("success"): print(name, "FAILED", json.dumps(r)[:3000]); sys.exit(1)
    print(name, "ok; warnings:", r.get("warnings")); log[name] = r; return r
r = bc("A", parent_id="document", mode="replace_children")
shell = re.search(r'configuration-id="arl" id="([^"]+)"', r["resolved_xml"]).group(1)
mb_before = None
for n in "BCDE": bc(n, parent_id=shell)
json.dump(log, open("build-log.json", "w"), indent=1)
print("shell", shell)
