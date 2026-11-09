"""Large-patch quilting of a top-down grass photo (all 8 rotations/flips) after inpainting fallen leaves.
usage: python3 -I quilt2.py <texture.jpg> <out.png> W H P O step"""
import cv2, numpy as np, sys
rng = np.random.default_rng(9)
T = cv2.imread(sys.argv[1]); W, H, P, O, ST = map(int, sys.argv[3:8])
hsv = cv2.cvtColor(T, cv2.COLOR_BGR2HSV)
leaf = ((hsv[..., 0] < 22) & (hsv[..., 1] > 60) & (hsv[..., 2] > 70)).astype(np.uint8)
leaf = cv2.morphologyEx(leaf, cv2.MORPH_OPEN, np.ones((4, 4), np.uint8))
leaf = cv2.dilate(leaf, np.ones((7, 7), np.uint8)) * 255
src = cv2.inpaint(T, leaf, 6, cv2.INPAINT_TELEA)
cv2.imwrite('src-clean.jpg', src)
f = src.astype(np.float32); low = cv2.GaussianBlur(f, (0, 0), 60); f = f / np.maximum(low, 1) * low.reshape(-1, 3).mean(0)
src = np.clip(f, 0, 255).astype(np.uint8)
views = []
for k in range(4):
    r = np.rot90(src, k); views += [r, r[:, ::-1]]
C = []
for v in views:
    for y in range(0, v.shape[0] - P + 1, ST):
        for x in range(0, v.shape[1] - P + 1, ST):
            C.append(v[y:y + P, x:x + P])
C = np.stack(C); G = C.mean(-1).astype(np.float32); print('candidates', len(C))
step = P - O; nx, ny = (W - O) // step + 1, (H - O) // step + 1
out = np.zeros((ny * step + O, nx * step + O, 3), np.float32)
def min_cut(err):
    r, c = err.shape; E = err.copy()
    for i in range(1, r):
        p = np.pad(E[i - 1], 1, constant_values=np.inf); E[i] += np.minimum(np.minimum(p[:-2], p[1:-1]), p[2:])
    path = np.zeros(r, int); path[-1] = int(np.argmin(E[-1]))
    for i in range(r - 2, -1, -1):
        j = path[i + 1]; lo, hi = max(0, j - 1), min(c, j + 2); path[i] = lo + int(np.argmin(E[i, lo:hi]))
    m = np.zeros((r, c), np.float32)
    for i in range(r): m[i, path[i]:] = 1
    return m
recent = []
for j in range(ny):
    for i in range(nx):
        X, Y = i * step, j * step; tgt = out[Y:Y + P, X:X + P]; tg = tgt.mean(-1)
        cost = np.zeros(len(C), np.float32)
        if i: cost += ((G[:, :, :O] - tg[None, :, :O]) ** 2).sum((1, 2))
        if j: cost += ((G[:, :O, :] - tg[None, :O, :]) ** 2).sum((1, 2))
        cost[recent] = np.inf                                       # never reuse a patch nearby
        k = rng.integers(len(C)) if not (i or j) else rng.choice(np.argsort(cost)[:max(5, len(C) // 60)])
        recent = (recent + [k])[-(nx + 2):]
        p = C[k].astype(np.float32); m = np.ones((P, P), np.float32)
        if i: m[:, :O] = np.minimum(m[:, :O], min_cut(((p[:, :O] - tgt[:, :O]) ** 2).sum(-1)))
        if j: m[:O, :] = np.minimum(m[:O, :], min_cut(((p[:O, :] - tgt[:O, :]) ** 2).sum(-1).T).T)
        if i or j: m = cv2.GaussianBlur(m, (0, 0), 1.5)
        out[Y:Y + P, X:X + P] = p * m[..., None] + tgt * (1 - m[..., None])
cv2.imwrite(sys.argv[2], np.clip(out[:H, :W], 0, 255).astype(np.uint8)); print('ok')
