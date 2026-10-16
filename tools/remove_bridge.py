#!/usr/bin/env python3
"""Remove the temporary CDN bridge (HTML widget 7e5a1cb, <style id="xj-cdn-bridge">) from header template 27.
Run ONLY after a Kinsta CDN purge, once `NOBRIDGE=1` runs of tools/home_3hr_qa.cjs and tools/panel_qa.cjs pass
on the plain public URLs. Saves the current header first. Usage: tools/remove_bridge.py [--dry-run]
Afterwards: clear the Elementor + Hummingbird page caches and re-run the QA without NOBRIDGE."""
import json, os, sys, time, urllib.request
U = "https://xtremestpete.com/wp-json/wp/v2/jet-theme-core/27"
H = {"User-Agent": "XtremeAudit-Claude/1.0", "Content-Type": "application/json", "Authorization": "Basic " + os.environ["XTREME_WP_BASIC_AUTH"]}
def req(u, d=None):
    r = urllib.request.Request(u, data=json.dumps(d).encode() if d else None, method="POST" if d else "GET", headers=H)
    return json.loads(urllib.request.urlopen(r, timeout=90).read())
cur = req(U + "?context=edit&_fields=meta")["meta"]["_elementor_data"]
ed = json.loads(cur)
box = [e for e in ed if e["id"] == "ca4414b"][0]
before = len(box["elements"]); box["elements"] = [w for w in box["elements"] if w["id"] != "7e5a1cb"]
if len(box["elements"]) == before: sys.exit("bridge widget 7e5a1cb not found; nothing to do")
assert any(w["id"] == "8883d2f" for w in box["elements"]), "Turnstile widget must stay"
if "--dry-run" in sys.argv: print("dry-run: would remove widget 7e5a1cb"); sys.exit()
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bak = os.path.join(root, "docs", "backup", f"jtc-27-before-bridge-removal-{time.strftime('%Y%m%dT%H%M%S')}.json")
json.dump({"_elementor_data": cur}, open(bak, "w"))
new = json.dumps(ed, ensure_ascii=False, separators=(",", ":"))
out = req(U + "?_fields=id,meta", {"meta": {"_elementor_data": new}})
print("removed bridge widget 7e5a1cb" if out["meta"]["_elementor_data"] == new else "MISMATCH", "| previous header saved to", bak)
