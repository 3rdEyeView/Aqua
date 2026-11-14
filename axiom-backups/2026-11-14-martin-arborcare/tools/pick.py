"""Larger sheet of chosen harvest numbers: python3 -I tools/pick.py <out.jpg> <n> <n> ..."""
import json, sys, os
from PIL import Image, ImageDraw
rows = {r['n']: r for r in json.load(open('harvest.json'))}; ns = [int(x) for x in sys.argv[2:]]; T, C = 600, 4
R = (len(ns) + C - 1) // C; sheet = Image.new('RGB', (C * T, R * (T + 26)), 'white'); d = ImageDraw.Draw(sheet)
for k, n in enumerate(ns):
    im = Image.open(os.path.join('scrape', rows[n]['file'])).convert('RGB'); im.thumbnail((T, T)); x, y = (k % C) * T, (k // C) * (T + 26)
    sheet.paste(im, (x + (T - im.width) // 2, y)); d.text((x + 6, y + T + 6), f"#{n} {rows[n]['w']}x{rows[n]['h']} {rows[n]['date']}", fill='black')
sheet.save(sys.argv[1], quality=85)
