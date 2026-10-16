#!/usr/bin/env python3
"""Restore one document's Elementor JSON, page settings and post content from a backup made by backup_site.py.
Usage: tools/restore_from_backup.py <backup_dir> <type: pages|posts|jet-theme-core> <id> [--dry-run]
After a restore: open the document via MCP publish-document (or Elementor Update) and clear caches.
Never touches other documents, orders, bookings or form entries."""
import json, os, sys, urllib.request
B, T, ID = sys.argv[1:4]; DRY = "--dry-run" in sys.argv
rec = json.load(open(os.path.join(B, T, f"{ID}.json")))
H = {"User-Agent": "XtremeAudit-Claude/1.0", "Content-Type": "application/json", "Authorization": "Basic " + os.environ["XTREME_WP_BASIC_AUTH"]}
u = f"https://xtremestpete.com/wp-json/wp/v2/{T}/{ID}"
body = {"content": rec["content"]["raw"], "meta": {"_elementor_data": rec["meta"]["_elementor_data"], "_elementor_page_settings": rec["meta"].get("_elementor_page_settings") or []}}
json.loads(body["meta"]["_elementor_data"])  # must be valid
if DRY: print("dry-run ok", T, ID, len(body["meta"]["_elementor_data"]), "bytes"); sys.exit()
r = urllib.request.Request(u + "?_fields=id", data=json.dumps(body).encode(), method="POST", headers=H)
urllib.request.urlopen(r, timeout=90).read()
r = urllib.request.Request(u + "?context=edit&_fields=content,meta", headers=H)
now = json.loads(urllib.request.urlopen(r, timeout=90).read())
ok = now["meta"]["_elementor_data"] == body["meta"]["_elementor_data"] and now["content"]["raw"] == body["content"]
print("restored" if ok else "MISMATCH", T, ID)
