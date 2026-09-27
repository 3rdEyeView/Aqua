#!/usr/bin/env python3
"""Copy the Elementor document of a rebuilt draft into an existing live page (keeps the
live page's ID, slug, Yoast meta, menu links and canonical). Back up first (docs/backup).

Usage: tools/swap_content.py <draft_id> <live_page_id>
       tools/swap_content.py --restore <live_page_id>   # restore from docs/backup/page-<id>.json

After copying, run an Elementor save on the live page (MCP manage-elements + publish-document)
so Elementor regenerates CSS and post content.
"""
import json, os, sys, urllib.request

BASE = "https://xtremestpete.com/wp-json/wp/v2/pages/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def req(url, data=None):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
                               method="POST" if data else "GET",
                               headers={"User-Agent": "XtremeAudit-Claude/1.0",
                                        "Content-Type": "application/json",
                                        "Authorization": "Basic " + os.environ["XTREME_WP_BASIC_AUTH"]})
    with urllib.request.urlopen(r, timeout=90) as resp:
        return json.loads(resp.read())


if sys.argv[1] == "--restore":
    live = sys.argv[2]
    bak = json.load(open(os.path.join(ROOT, "docs", "backup", f"page-{live}.json")))
    out = req(BASE + live, {"meta": {"_elementor_data": bak["meta"]["_elementor_data"]}})
    print("restored", live, len(out["meta"]["_elementor_data"]))
    sys.exit()

draft, live = sys.argv[1], sys.argv[2]
assert os.path.exists(os.path.join(ROOT, "docs", "backup", f"page-{live}.json")), "no backup for live page"
src = req(BASE + draft + "?context=edit&_fields=meta")["meta"]["_elementor_data"]
json.loads(src)  # must be valid JSON
out = req(BASE + live + "?_fields=id,link,meta", {"meta": {"_elementor_data": src}})
assert out["meta"]["_elementor_data"] == src, "write did not stick"
print("copied", draft, "->", live, out["link"], len(src), "bytes")
