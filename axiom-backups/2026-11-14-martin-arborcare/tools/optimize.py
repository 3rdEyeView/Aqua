"""shortlist.tsv -> site/img/martin-demo-<slug>.jpg  (hero 2000px q80, others 1200px q82, never upscaled)"""
import csv, json, os
from PIL import Image, ImageOps
h = {r['n']: r for r in json.load(open('harvest.json'))}; out = []
for r in csv.DictReader(open('shortlist.tsv'), delimiter='\t'):
    src = os.path.join('scrape', h[int(r['n'])]['file']); im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    if r['crop']:
        a, b, c, d = map(float, r['crop'].split(',')); W, H = im.size; im = im.crop((int(a * W), int(b * H), int(c * W), int(d * H)))
    lim = 2000 if r['role'] == 'hero' else 1200
    if max(im.size) > lim: im.thumbnail((lim, lim), Image.LANCZOS)
    f = f"site/img/martin-demo-{r['slug']}.jpg"; im.save(f, quality=80 if r['role'] == 'hero' else 82, optimize=True, progressive=True)
    out.append({**r, 'file': f, 'w': im.width, 'h': im.height, 'kb': os.path.getsize(f) // 1024})
json.dump(out, open('site/images.json', 'w'), indent=1)
print(sum(o['kb'] for o in out), 'KB total'); [print(o['slug'], o['w'], o['h'], o['kb']) for o in out]
