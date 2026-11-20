"""originals/NN.webp -> site/img/miracle-demo-<slug>.jpg (hero 2000px q80, others <=1400px q82, never upscaled).
Before/after composites (16, 27, 29) are split into two frames; #19 is cropped to drop another company's sign."""
import json, os
from PIL import Image
O = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(O)
# slug: (source, crop box in px (l,t,r,b) or None)
J = {
 'hero-tan-stucco-home': (17, None), 'exterior-bungalow': (23, None), 'interior-navy-room': (28, None),
 'commercial-building': (18, None), 'commercial-stucco-frontage': (19, (0, 0, 860, 1020)),
 'deck-pavilion': (24, None), 'deck-stained': (25, None), 'arched-iron-door': (20, None),
 'teal-coastal-home': (22, None), 'sage-ranch-metal-roof': (26, None), 'white-ranch-clouds': (30, None),
 'ba1-before': (16, (0, 0, 574, 456)), 'ba1-after': (16, (0, 568, 574, 1020)),
 'ba2-before': (27, (0, 0, 574, 524)), 'ba2-after': (27, (0, 636, 574, 1020)),
 'ba3-before': (29, (0, 0, 481, 462)), 'ba3-after': (29, (0, 498, 481, 1020)),
}
out = {}
for slug, (n, box) in J.items():
    im = Image.open(f'originals/{n}.webp').convert('RGB')
    if box: im = im.crop(box)
    lim = 2000 if slug.startswith('hero') else 1400
    if max(im.size) > lim: im.thumbnail((lim, lim), Image.LANCZOS)
    f = f'site/img/miracle-demo-{slug}.jpg'; im.save(f, quality=80 if slug.startswith('hero') else 84, optimize=True, progressive=True)
    out[slug] = [im.width, im.height, os.path.getsize(f) // 1024]; print(slug, out[slug])
json.dump(out, open('site/images.json', 'w'), indent=1)
