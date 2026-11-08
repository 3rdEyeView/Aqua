#!/usr/bin/env python3
"""Bulk intake for Jenny's media drop (Fence It Up demo).

usage: python3 -I tools/intake.py <zip-or-folder> [<zip-or-folder> ...]

  - Unzips each input into originals/<input-name>/ (never modified afterwards).
  - Walks every photo (jpg/jpeg/png/webp/heic/heif) and video (mp4/mov/m4v/webm).
  - Maps files to their source post when an Instagram data export is present
    (any posts_*.json / reels.json / stories.json under the export):
    post date, caption and carousel position. Camera-roll files fall back to EXIF / file date.
  - Scores photos: resolution plus sharpness (Laplacian variance on a 1024px copy).
  - Removes duplicates: perceptual hash (photos) and duration + middle-frame hash (videos);
    the highest-resolution / highest-bitrate copy wins, the others are marked dup_of.
  - Writes inventory.tsv and contact sheets in review/ (numbered tiles, so a shortlist can name them).
"""
import csv, hashlib, json, os, subprocess, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageStat
import imagehash
import pillow_heif

pillow_heif.register_heif_opener()
ROOT = Path(__file__).resolve().parent.parent
ORIG, REVIEW = ROOT / "originals", ROOT / "review"
PHOTO = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}
VIDEO = {".mp4", ".mov", ".m4v", ".webm"}


def fix_text(s):
    """Instagram exports store UTF-8 bytes as latin-1 escapes."""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def unpack(src: Path) -> Path:
    dest = ORIG / src.stem
    if src.is_dir():
        return src
    if not dest.exists():
        dest.mkdir(parents=True)
        with zipfile.ZipFile(src) as z:
            for m in z.infolist():
                p = (dest / m.filename).resolve()
                if not str(p).startswith(str(dest.resolve())):  # zip-slip guard
                    continue
                if m.filename.split("/")[-1].startswith("._") or "__MACOSX" in m.filename:
                    continue
                z.extract(m, dest)
        for inner in list(dest.rglob("*.zip")):  # IG exports sometimes arrive as zip-in-zip
            unpack(inner)
    return dest


def post_index(base: Path):
    """uri suffix -> {post, date, caption, pos, count} from an Instagram export, if any."""
    idx = {}
    for j in base.rglob("*.json"):
        if not any(k in j.name for k in ("posts_", "reels", "stories", "igtv")):
            continue
        try:
            data = json.loads(j.read_text(encoding="utf-8"))
        except Exception:
            continue
        posts = data if isinstance(data, list) else next((v for v in data.values() if isinstance(v, list)), [])
        for n, post in enumerate(posts, 1):
            media = post.get("media", [post]) if isinstance(post, dict) else []
            ts = post.get("creation_timestamp") or (media[0].get("creation_timestamp") if media else None)
            cap = fix_text(post.get("title") or (media[0].get("title", "") if media else ""))
            pid = f"{j.stem}#{n}"
            for i, m in enumerate(media, 1):
                uri = m.get("uri")
                if not uri:
                    continue
                t = m.get("creation_timestamp") or ts
                idx[Path(uri).name] = {
                    "post": pid,
                    "date": datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d") if t else "",
                    "caption": " ".join(cap.split())[:200],
                    "pos": f"{i}/{len(media)}",
                }
    return idx


def photo_info(p: Path):
    im = Image.open(p)
    exif_date = ""
    try:
        exif_date = (im.getexif().get(306) or "")[:10].replace(":", "-")
    except Exception:
        pass
    im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size
    small = im.copy()
    small.thumbnail((1024, 1024))
    lap = small.convert("L").filter(ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], 1, 128))
    sharp = ImageStat.Stat(lap).var[0]
    bright = ImageStat.Stat(small.convert("L")).mean[0]
    return im, dict(w=w, h=h, sharp=round(sharp, 1), bright=round(bright), hash=str(imagehash.phash(im)), exif_date=exif_date)


def probe(p: Path):
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(p)],
                         capture_output=True, text=True).stdout
    d = json.loads(out or "{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    a = any(s.get("codec_type") == "audio" for s in d.get("streams", []))
    w, h = v.get("width", 0), v.get("height", 0)
    rot = str(v.get("tags", {}).get("rotate", "")) or next((str(int(x.get("rotation", 0))) for x in v.get("side_data_list", []) if "rotation" in x), "")
    if rot.lstrip("-") in ("90", "270"):
        w, h = h, w
    num, den = (v.get("avg_frame_rate", "0/1").split("/") + ["1"])[:2]
    fps = round(float(num) / float(den or 1), 1) if float(den or 1) else 0
    return dict(w=w, h=h, dur=round(float(d.get("format", {}).get("duration", 0)), 1),
                kbps=int(int(d.get("format", {}).get("bit_rate", 0) or 0) / 1000), fps=fps, audio="y" if a else "n")


def frame(p: Path, t: float) -> Image.Image | None:
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(p), "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True)
    if not r.stdout:
        return None
    from io import BytesIO
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def sheet(items, name, cols=6, tile=300):
    rows = (len(items) + cols - 1) // cols
    S = Image.new("RGB", (cols * tile, rows * (tile + 22)), "white")
    d = ImageDraw.Draw(S)
    for k, (label, im) in enumerate(items):
        t = im.copy()
        t.thumbnail((tile - 6, tile - 6))
        x, y = (k % cols) * tile, (k // cols) * (tile + 22)
        S.paste(t, (x + (tile - t.width) // 2, y + 3 + (tile - 6 - t.height) // 2))
        d.text((x + 4, y + tile + 4), label, fill="black")
    S.save(REVIEW / name, quality=85)


def main(srcs):
    ORIG.mkdir(exist_ok=True)
    REVIEW.mkdir(exist_ok=True)
    bases = [unpack(Path(s)) for s in srcs]
    idx = {}
    for b in bases:
        idx.update(post_index(b))
    files = sorted(p for b in bases for p in b.rglob("*") if p.is_file() and p.suffix.lower() in PHOTO | VIDEO)
    rows, thumbs = [], {}
    for p in files:
        rel = p.relative_to(ROOT) if ROOT in p.parents else p
        src = idx.get(p.name, {})
        r = dict(id="", file=str(rel), kind="photo" if p.suffix.lower() in PHOTO else "video", w=0, h=0, dur="", kbps="",
                 fps="", audio="", sharp="", bright="", hash="", bytes=p.stat().st_size,
                 sha1=hashlib.sha1(p.read_bytes()).hexdigest()[:12], dup_of="", also_in="", post=src.get("post", ""),
                 pos=src.get("pos", ""), date=src.get("date", ""), caption=src.get("caption", ""), error="")
        try:
            if r["kind"] == "photo":
                im, info = photo_info(p)
                r.update({k: v for k, v in info.items() if k != "exif_date"})
                r["date"] = r["date"] or info["exif_date"]
            else:
                r.update(probe(p))
                im = frame(p, max(0.0, r["dur"] / 2)) if r["dur"] else None
                r["hash"] = f"{r['dur']:.0f}s:" + (str(imagehash.phash(im)) if im else "")
            if im:
                thumbs[r["file"]] = im
        except Exception as e:
            r["error"] = f"{type(e).__name__}: {e}"[:120]
        rows.append(r)

    # exact duplicates, then near duplicates; best copy = most pixels, then bitrate, then bytes
    rank = lambda r: (r["w"] * r["h"], r["kbps"] or 0, r["bytes"])
    rows.sort(key=rank, reverse=True)
    keep = []
    for r in rows:
        if r["error"]:
            continue
        for k in keep:
            if k["kind"] != r["kind"]:
                continue
            if k["sha1"] == r["sha1"]:
                r["dup_of"] = k["file"]
                break
            if r["kind"] == "photo" and imagehash.hex_to_hash(k["hash"]) - imagehash.hex_to_hash(r["hash"]) <= 6:
                r["dup_of"] = k["file"]
                break
            if r["kind"] == "video" and r["hash"].endswith(":") is False and k["hash"].split(":")[0] == r["hash"].split(":")[0] \
                    and imagehash.hex_to_hash(k["hash"].split(":")[1]) - imagehash.hex_to_hash(r["hash"].split(":")[1]) <= 8:
                r["dup_of"] = k["file"]
                break
        else:
            keep.append(r)
            continue
        k = next(k for k in keep if k["file"] == r["dup_of"])  # keeper also records where the copy was posted
        if r["post"] and r["post"] != k["post"] and r["post"] not in k["also_in"].split(" "):
            k["also_in"] = (k["also_in"] + " " + r["post"]).strip()

    photos = sorted([r for r in keep if r["kind"] == "photo"], key=lambda r: r["sharp"], reverse=True)
    videos = sorted([r for r in keep if r["kind"] == "video"], key=lambda r: (r["w"] * r["h"], r["kbps"]), reverse=True)
    for n, r in enumerate(photos, 1):
        r["id"] = f"P{n:03d}"
    for n, r in enumerate(videos, 1):
        r["id"] = f"V{n:02d}"

    cols = list(rows[0].keys()) if rows else []
    with open(ROOT / "inventory.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, cols, delimiter="\t")
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["id"] == "", r["id"], r["file"])):
            w.writerow(r)

    for i in range(0, len(photos), 48):
        sheet([(f"{r['id']} {r['w']}x{r['h']} s{r['sharp']:.0f}", thumbs[r["file"]]) for r in photos[i:i + 48]],
              f"photos-{i // 48 + 1:02d}.jpg")
    for r in videos:  # 6 frames per clip across its length
        fr = [(f"{r['id']} @{t:.1f}s", im) for t in [r["dur"] * k / 7 for k in range(1, 7)]
              if (im := frame(ROOT / r["file"] if not Path(r["file"]).is_absolute() else Path(r["file"]), t))]
        if fr:
            sheet(fr, f"video-{r['id']}.jpg", cols=6, tile=260)

    dups = sum(1 for r in rows if r["dup_of"])
    errs = [r for r in rows if r["error"]]
    print(f"files {len(rows)} · photos kept {len(photos)} · videos kept {len(videos)} · duplicates {dups} · "
          f"errors {len(errs)} · mapped to posts {sum(1 for r in rows if r['post'])}")
    for r in errs:
        print("  error:", r["file"], r["error"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
