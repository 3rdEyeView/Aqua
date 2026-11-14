"""Contact sheets of the harvested photos: python3 -I tools/sheet.py <harvest.json> <outdir>"""
import json, sys, os
from PIL import Image, ImageDraw, ImageOps
rows = [r for r in json.load(open(sys.argv[1])) if r['file']]
base = os.path.dirname(os.path.abspath(sys.argv[1])); out = sys.argv[2]; T, C, PER = 300, 6, 30
for s in range(0, len(rows), PER):
    chunk = rows[s:s + PER]; R = (len(chunk) + C - 1) // C
    sheet = Image.new('RGB', (C * T, R * (T + 22)), 'white'); d = ImageDraw.Draw(sheet)
    for k, r in enumerate(chunk):
        im = ImageOps.exif_transpose(Image.open(os.path.join(base, 'scrape', r['file'])).convert('RGB')); im.thumbnail((T, T))
        x, y = (k % C) * T, (k // C) * (T + 22); sheet.paste(im, (x + (T - im.width) // 2, y + (T - im.height) // 2))
        d.text((x + 4, y + T + 4), f"#{r['n']} {r['w']}x{r['h']} {'AI ' if r['ai'] else ''}{r['date'][-12:]}", fill='red' if r['ai'] else 'black')
    sheet.save(f"{out}/sheet-{s // PER + 1:02d}.jpg", quality=80)
print(len(rows))
