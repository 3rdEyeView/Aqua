#!/usr/bin/env python3
"""Make web copies of the shortlist. Originals are never touched.

usage: python3 -I tools/optimize.py shortlist.tsv

shortlist.tsv columns (tab-separated, header row):
  id (inventory id or a path such as crops/x.png)
  id      role    slug                    start   len
  P004    hero    white-vinyl-privacy
  P001    photo   black-aluminum-pool
  V02     clip    vinyl-install           3.5     8      <- the muted page clip
  V01     video   gate-swing              0       12     <- shortlisted, also encoded

Outputs to site/ as fenceitup-demo-<slug>.*:
  hero  -> 2000px long side, JPEG q80 (progressive)
  photo -> 1200px long side, JPEG q82 (progressive), the same as Branham
  clip / video -> H.264 MP4, no audio, long side ≤1280px, CRF 26 capped at 2.5 Mbps, +faststart, plus a poster JPEG at the first frame
"""
import csv, subprocess, sys
from pathlib import Path

from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


def main(sl):
    SITE.mkdir(exist_ok=True)
    inv = {r["id"]: r for r in csv.DictReader(open(ROOT / "inventory.tsv"), delimiter="\t") if r["id"]}
    for r in csv.DictReader(open(sl), delimiter="\t"):
        src = ROOT / (inv[r["id"]]["file"] if r["id"] in inv else r["id"])  # an inventory id or a path (e.g. crops/*.png)
        name = f"fenceitup-demo-{r['slug']}"
        if r["role"] in ("hero", "photo"):
            im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
            im.thumbnail((2000, 2000) if r["role"] == "hero" else (1200, 1200), Image.LANCZOS)
            out = SITE / f"{name}.jpg"
            # sources already recompressed by Instagram (screenshot crops) get q86 so artifacts don't stack
            q = 86 if max(im.size) <= 1000 else (80 if r["role"] == "hero" else 82)
            im.save(out, quality=q, optimize=True, progressive=True)
        else:
            out = SITE / f"{name}.mp4"
            cut = (["-ss", r["start"]] if r.get("start") else []) + (["-t", r["len"]] if r.get("len") else [])
            subprocess.run(["ffmpeg", "-y", "-v", "error", *cut, "-i", str(src), "-an",
                            "-vf", "scale='if(gte(iw,ih),min(1280,iw),-2)':'if(gte(iw,ih),-2,min(1280,ih))':flags=lanczos,format=yuv420p",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "26", "-maxrate", "2500k", "-bufsize", "5000k",
                            "-profile:v", "high",
                            "-movflags", "+faststart", str(out)], check=True)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-frames:v", "1", "-q:v", "3",
                            str(SITE / f"{name}-poster.jpg")], check=True)
        print(f"{r['id']:5} {r['role']:6} -> {out.name}  {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
