"""Builds the Martin Arborcare page (default 2057, override with MA_PID) from ALL.json in one replace call.
One replace (not replace + appends) so Elementor regenerates the page's V4 CSS file (see the Comer's README)."""
import json, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import axmcp as mcp
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PID = int(os.environ.get("MA_PID", "2057"))
mcp.init()
r = mcp.call("elementor-build-composition", {"post_id": PID, **json.load(open("ALL.json")), "parent_id": "document", "mode": "replace_children"})
if "error" in r or not r.get("success"): print("FAILED", json.dumps(r)[:4000]); sys.exit(1)
print("ok; warnings:", json.dumps(r.get("warnings"))[:3000])
json.dump(r, open("build-log.json", "w"), indent=1)
