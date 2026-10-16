#!/usr/bin/env python3
"""Timestamped backup of WordPress/Elementor content that edits could touch, plus a manifest.
Usage: tools/backup_site.py <backup_dir>
Saves: every page/post/jet-theme-core template (raw content, Elementor JSON, page settings, latest revision IDs),
all V4 global class styles, the Elementor kit, Customizer additional CSS (as rendered), Yoast head meta,
reading settings. Writes manifest.json with sha256 per file. Read-only against the site."""
import hashlib, json, os, re, sys, urllib.request
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SITE = "https://xtremestpete.com/wp-json"
H = {"User-Agent": "XtremeAudit-Claude/1.0", "Authorization": "Basic " + os.environ["XTREME_WP_BASIC_AUTH"]}
def get(path, raw=False):
    r = urllib.request.Request(path if path.startswith("http") else SITE + path, headers=H)
    with urllib.request.urlopen(r, timeout=90) as resp:
        b = resp.read(); return b if raw else json.loads(b)
def save(name, obj):
    p = os.path.join(OUT, name); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f: json.dump(obj, f, ensure_ascii=False, indent=1)
index = []
for t in ("pages", "posts", "jet-theme-core"):
    items = get(f"/wp/v2/{t}?context=edit&per_page=100&status=publish,draft,private")
    for it in items:
        try: revs = get(f"/wp/v2/{t}/{it['id']}/revisions?per_page=5&_fields=id,date")
        except Exception as e: revs = {"error": str(e)}
        rec = {k: it.get(k) for k in ("id", "slug", "status", "link", "modified_gmt", "template", "title", "content", "excerpt", "meta", "parent", "menu_order")}
        rec["latest_revisions"] = revs
        rec["yoast_head_json"] = it.get("yoast_head_json")
        save(f"{t}/{it['id']}.json", rec)
        index.append({"type": t, "id": it["id"], "slug": it["slug"], "status": it["status"], "modified_gmt": it["modified_gmt"],
                      "latest_revision": revs[0]["id"] if isinstance(revs, list) and revs else None,
                      "elementor_bytes": len((it.get("meta") or {}).get("_elementor_data") or "")})
classes = get("/elementor/v1/global-classes")["data"]
ids = ",".join(c["id"] for c in classes)
save("elementor/global-classes-list.json", classes)
save("elementor/global-classes-styles.json", get(f"/elementor/v1/global-classes/styles?ids={ids}"))
save("elementor/kit-7.json", get("/wp/v2/elementor_library/7?context=edit"))
save("wordpress/settings.json", get("/wp/v2/settings"))
html = get("https://xtremestpete.com/?bk=1", raw=True).decode("utf-8", "replace")
m = re.search(r'<style id="wp-custom-css">(.*?)</style>', html, re.S)
with open(os.path.join(OUT, "wordpress/customizer-additional-css.css"), "w") as f: f.write(m.group(1) if m else "")
save("index.json", index)
man = {}
for root, _, files in os.walk(OUT):
    for fn in files:
        if fn == "manifest.json": continue
        p = os.path.join(root, fn); man[os.path.relpath(p, OUT)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
save("manifest.json", man)
print(OUT, len(index), "documents,", len(classes), "global classes,", len(man), "files")
