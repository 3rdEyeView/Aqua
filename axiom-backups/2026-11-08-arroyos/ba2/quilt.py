"""Image quilting (Efros & Freeman 2001, overlap-SSD patch choice + minimum-error boundary cut) of the licensed
overgrown-lawn photo into a large seamless sheet of real grass texture.
usage: python3 -I quilt.py <texture.jpg> x0,y0,x1,y1 <out.png> [W H patch overlap]"""
import cv2, numpy as np, sys
rng = np.random.default_rng(5)
T = cv2.imread(sys.argv[1]); x0, y0, x1, y1 = map(int, sys.argv[2].split(','))
src = T[y0:y1, x0:x1].astype(np.float32)
# flatten the photo's own light (shade gradient) so patches have even brightness; this yard's light is applied later
low = cv2.GaussianBlur(src, (0, 0), 35); src = src / np.maximum(low, 1) * low.reshape(-1, 3).mean(0)
# debris in the source (dead leaves) must not be repeated: skip any patch that touches these points (texture coords)
AVOID = [(720, 540), (920, 380), (905, 400), (790, 240)]
W, H, P, O = (int(v) for v in (sys.argv[4:8] if len(sys.argv) > 7 else (2600, 1900, 150, 46)))
# candidate patches: every 6 px, plus horizontally flipped copies (grass has no handedness; light is flattened later)
cands = []
for s in (src, src[:, ::-1]):
    flip = s is not src
    for yy in range(0, s.shape[0] - P, 4):
        for xx in range(0, s.shape[1] - P, 5):
            bad = False
            for ax, ay in AVOID:
                px = (x1 - 1 - ax) if flip else (ax - x0); py = ay - y0
                if xx - 30 <= px <= xx + P + 30 and yy - 30 <= py <= yy + P + 30: bad = True; break
            if not bad: cands.append(s[yy:yy + P, xx:xx + P])
C = np.stack(cands); print('candidates', len(C))
Cg = C.mean(-1)
step = P - O
nx, ny = (W - O) // step + 1, (H - O) // step + 1
out = np.zeros((ny * step + O, nx * step + O, 3), np.float32)
def min_cut(err):        # err: (rows, overlap) → mask (1 = take new patch) via dynamic programming along rows
    r, c = err.shape; E = err.copy()
    for i in range(1, r):
        prev = np.pad(E[i - 1], 1, constant_values=np.inf)
        E[i] += np.minimum(np.minimum(prev[:-2], prev[1:-1]), prev[2:])
    path = np.zeros(r, int); path[-1] = int(np.argmin(E[-1]))
    for i in range(r - 2, -1, -1):
        j = path[i + 1]; lo, hi = max(0, j - 1), min(c, j + 2); path[i] = lo + int(np.argmin(E[i, lo:hi]))
    m = np.zeros((r, c), np.float32)
    for i in range(r): m[i, path[i]:] = 1
    return m
for j in range(ny):
    for i in range(nx):
        X, Y = i * step, j * step
        tgt = out[Y:Y + P, X:X + P]
        cost = np.zeros(len(C), np.float32)
        tg = tgt.mean(-1)
        if i > 0: cost += ((Cg[:, :, :O] - tg[None, :, :O]) ** 2).sum((1, 2))
        if j > 0: cost += ((Cg[:, :O, :] - tg[None, :O, :]) ** 2).sum((1, 2))
        if i == 0 and j == 0: k = rng.integers(len(C))
        else:
            best = np.argsort(cost)[:max(6, len(C) // 150)]; k = rng.choice(best)
        p = C[k]
        mask = np.ones((P, P), np.float32)
        if i > 0: mask[:, :O] = np.minimum(mask[:, :O], min_cut(((p[:, :O] - tgt[:, :O]) ** 2).sum(-1)))
        if j > 0: mask[:O, :] = np.minimum(mask[:O, :], min_cut(((p[:O, :] - tgt[:O, :]) ** 2).sum(-1).T).T)
        mask = cv2.GaussianBlur(mask, (0, 0), 1.2) if (i or j) else mask
        out[Y:Y + P, X:X + P] = p * mask[..., None] + tgt * (1 - mask[..., None])
out = out[:H, :W]
cv2.imwrite(sys.argv[3], np.clip(out, 0, 255).astype(np.uint8)); print('sheet', out.shape)
