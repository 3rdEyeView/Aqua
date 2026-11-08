#!/usr/bin/env python3
"""Cut the post photo out of each Instagram app screenshot in Jenny's ZIP and drop the IG overlays.

usage: python3 -I tools/crop_screens.py      (reads originals/Fence_It_Up_Demo_Media, writes crops/ + sources.tsv)

Each screenshot is 706x1536. The post photo is the full-width band starting at y=298, the first long run of rows
that aren't pure-white UI (found with the row-stat scan in this script). The box per file then trims the overlays
Instagram draws on top: the mute icon (video posts), the account's repost badge, and stickers or text.
Crops are saved as lossless PNG, so the only lossy steps are Instagram's own and the final web JPEG.
"""
import csv
from pathlib import Path
from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "originals" / "Fence_It_Up_Demo_Media"
OUT = ROOT / "crops"
TOP = 298

# file: slug, box within the band (x0, y0, x1, y1; None = band edge), date, location, video post?, caption (as shown), overlays removed
POSTS = {
 "IMG_0343": ("pool-backyard-vinyl", (0, 0, 706, 555), "2026-10-30", "Orlando, FL", True,
              "Privacy, Beauty & Peace of Mind! Another beautiful backyard transformed with a…", "mute icon"),
 "IMG_0344": ("work-in-progress", (0, 0, 706, 740), "2026-02-15", "Orlando, FL", True,
              "Fence It Up This Month! We're excited to offer a special promotion—when…", "'Work in progress' text, badge, mute icon"),
 "IMG_0345": ("side-yard-walkway", (0, 0, 706, 840), "2026-01-20", "Orlando, FL", True,
              "Not all fences are created equal. The right company means stronger installs, better materials, and peace of mind.", "badge, mute icon"),
 "IMG_0346": ("vinyl-privacy-corner", (0, 0, 706, 840), "2026-01-03", "Orlando, FL", True,
              "Why is permit crucial when planning a fence? Permits done right = no fines, no stress.", "badge, mute icon"),
 "IMG_0347": ("new-build-backyard", (145, 0, 706, 445), "2025-12-09", "Altamonte Springs, FL", True,
              "Why pick FENCE IT UP as your preferred Fence company…", "'Want a Fence?' sticker, badge, mute icon"),
 "IMG_0348": ("black-chain-link", (0, 0, 706, None), "2025-12-07", "Orlando, FL", False,
              "Quality materials. Clean installation. Trusted results. Chain-link fence by Fence It Up LLC.", "none"),
 "IMG_0349": ("vinyl-privacy-sunburst", (0, 0, 706, 840), "2025-11-08", "Orlando, FL", True,
              "Peace and privacy, Orlando style. Nothing like a clean PVC fence to give your backyard that private oasis vibe.", "badge, mute icon"),
 "IMG_0350": ("double-gate-sunset", (0, 0, 706, None), "2025-10-18", "Kissimmee / Orlando, FL", False,
              "Client realized she needed more space — so we added a double gate for easy access!", "none"),
 "IMG_0351": ("pvc-side-yard", (0, 0, 706, None), "2025-10-16", "Kissimmee / Orlando, FL", False,
              "Strong. Stylish. Secure. Transform your property with a premium PVC privacy fence built to last…", "none"),
 "IMG_0352": ("pvc-double-gate", (0, 0, 636, None), "2025-07-20", "Kissimmee / Orlando, FL", True,
              "Clean lines. Strong privacy. Zero maintenance. Another PVC fence installed and standing strong!", "mute icon"),
 "IMG_0353": ("wood-privacy-gate", (0, 0, 706, 490), "2025-05-28", "Orlando, FL", True,
              "New fence, who dis…", "Fence It Up watermark, mute icon"),
}


def band(im):
    g = im.convert("L")
    W, H = g.size
    y = TOP
    while y < H:
        s = ImageStat.Stat(g.crop((0, y, W, y + 1)))
        if s.mean[0] > 248 and s.stddev[0] < 6:
            break
        y += 1
    return y - TOP


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for name, (slug, (x0, y0, x1, y1), date, loc, video, cap, removed) in POSTS.items():
        im = Image.open(SRC / f"{name}.jpeg").convert("RGB")
        h = band(im)
        crop = im.crop((x0, TOP + y0, x1, TOP + (y1 if y1 is not None else h)))
        crop.save(OUT / f"fenceitup-{slug}.png")
        rows.append(dict(file=f"crops/fenceitup-{slug}.png", source=f"originals/Fence_It_Up_Demo_Media/{name}.jpeg",
                         w=crop.width, h=crop.height, post_band_h=h, ig_post_date=date, ig_location=loc,
                         ig_video_post="y" if video else "n", ig_caption=cap, overlays_removed=removed))
        print(f"{name} band {h:4d} -> {crop.width}x{crop.height}  fenceitup-{slug}.png")
    with open(ROOT / "sources.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, rows[0].keys(), delimiter="\t")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
