"""Builds the Comer's DRAFT page (default 1996, override with CMZ_PID) from A..F.json in one replace call (ALL.json).
appends B..F inside the shell. The page stays a draft: nothing here publishes it."""
import json, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import axmcp as mcp
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PID = int(os.environ.get("CMZ_PID", "1996"))  # current draft; see README for why the ID changes
mcp.init(); log = {}
def bc(name, **kw):
    r = mcp.call("elementor-build-composition", {"post_id": PID, **json.load(open(f"{name}.json")), **kw})
    if "error" in r or not r.get("success"): print(name, "FAILED", json.dumps(r)[:3000]); sys.exit(1)
    print(name, "ok; warnings:", json.dumps(r.get("warnings"))[:1500]); log[name] = r; return r
# One replace call with every batch nested in the shell: Elementor regenerates the page's V4 CSS file on a document
# replace but not on later appends, so a multi-call build leaves the CSS a build behind (seen 2026-11-14).
parts = [json.load(open(f"{n}.json")) for n in "ABCDEF"]
xml = parts[0]["xml_structure"]; assert xml.endswith("</e-flexbox>")
xml = xml[:-len("</e-flexbox>")] + "".join(p["xml_structure"] for p in parts[1:]) + "</e-flexbox>"
merged = {"xml_structure": xml, "element_config": {}, "style": {}}
for p in parts: merged["element_config"].update(p["element_config"]); merged["style"].update(p["style"])
json.dump(merged, open("ALL.json", "w"), ensure_ascii=False)
r = bc("ALL", parent_id="document", mode="replace_children")
shell = re.search(r'configuration-id="cmz" id="([^"]+)"', r["resolved_xml"]).group(1)
json.dump(log, open("build-log.json", "w"), indent=1)
print("shell", shell)
