"""(About-photo variant of ba2/compose.py: manicured St. Augustine texture on project-2001's lawn.)
Demo visualization for the Arroyo's slider.
AFTER  = Arroyo's own photo clean-1008, untouched.
BEFORE = the same photo; only the lawn (mask1008.png) is replaced by real, openly licensed overgrown-grass texture,
         mapped onto this yard's ground plane with a homography (exact for two views of a plane), then given this photo's
         own light: per-distance tone/colour match to its sunlit lawn, its shadows re-applied, natural colour variation.
         House, beds, shrubs, pavers, sky and camera angle are the original pixels.
usage: python3 -I compose.py <texture.jpg> "x0,y0 x1,y1 x2,y2 x3,y3" [out.png]
       the four points are a quad on the texture's lawn (far-left, far-right, near-right, near-left) that maps onto this
       photo's lawn quad DST below."""
import cv2, numpy as np, sys
rng = np.random.default_rng(11)
I = cv2.imread('../src/assets/img/project-2001.webp'); h, w = I.shape[:2]
M = (cv2.imread('mask.png', 0) > 128).astype(np.uint8) * 255
# Real-texture sheet (quilt.py output from the licensed photo) laid flat on this photo's ground plane.
# args: <sheet.png> <M0> <out> "HI,CX"   M0 = image px per sheet px at the bottom edge (isotropic there)
SHEET = cv2.imread(sys.argv[1]).astype(np.float32)
M0 = float(sys.argv[2]); out_path = sys.argv[3]
HI, CXI = [float(v) for v in (sys.argv[4] if len(sys.argv) > 4 else '536,800').split(',')]
SH, SW = SHEET.shape[:2]
SHEET = np.concatenate([SHEET, SHEET[::-1], SHEET], 0)          # room for the far distance (minified, flip invisible there)
dn = (h - 1) - HI; K = dn / M0
VN = SHEET.shape[0] - 40; U0 = SW / 2
# Upright blades: render in overlapping horizontal bands. Inside a band the horizontal scale is constant (no convergence
# shear, blades stay vertical); vertical mapping follows the ground plane per row (foreshortening). Each band gets a random
# sideways offset; neighbours cross-fade with triangular weights, so no band edge is visible.
W = np.zeros((h, w, 3), np.float32); WT = np.zeros((h, 1, 1), np.float32)
xs = np.arange(w, dtype=np.float32)
centers = []; y = float(h - 1 + 30)
while y > 1215:
    centers.append(y); y -= max(10.0, 0.14 * (y - HI))
brng = np.random.default_rng(3)
cache = {}
def level(fx, fy):
    key = (round(fx, 2), round(fy, 2))
    if key not in cache:
        cache.clear()
        cache[key] = SHEET if (fx <= 1 and fy <= 1) else cv2.resize(SHEET, (max(8, int(SHEET.shape[1] / max(1, fx))), max(8, int(SHEET.shape[0] / max(1, fy)))), interpolation=cv2.INTER_AREA)
    return cache[key]
for i, yc in enumerate(centers):
    up = centers[i + 1] if i + 1 < len(centers) else yc - (centers[i - 1] - yc)
    dn_ = centers[i - 1] if i > 0 else yc + (yc - up)
    y0b, y1b = int(max(1215, np.floor(up))), int(min(h - 1, np.ceil(dn_)))
    if y1b < y0b: continue
    db = max(8.0, yc - HI); kx = K / db
    off = brng.uniform(0, SW)
    fx, fy = max(1.0, kx), max(1.0, K * dn / db ** 2)            # one prefilter level per band (consistent rows)
    lvl = level(fx, fy)
    for yy in range(y0b, y1b + 1):
        wgt = (yy - up) / (yc - up) if yy <= yc else (dn_ - yy) / (dn_ - yc)
        if wgt <= 0: continue
        dd = max(8.0, yy - HI)
        small = lvl
        u = off + (xs - CXI) * kx
        v = VN - K * dn * (1.0 / dd - 1.0 / dn)
        Wl = small.shape[1] - 1; per = 2 * Wl; t = np.mod(u / fx, per); mxr = np.where(t > Wl, per - t, t)
        mx = mxr.astype(np.float32).reshape(1, -1); my = np.full_like(mx, min(v / fy, small.shape[0] - 2))
        W[yy] += wgt * cv2.remap(small, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT_101)[0]
        WT[yy] += wgt
W = W / np.maximum(WT, 1e-6)
_wb = cv2.GaussianBlur(W, (0, 0), 1.0); W = W + (W - _wb) * 0.6          # crisp blade edges (source is a 1024px JPEG)
W = np.clip(W, 0, 255).astype(np.uint8)
print('sheet rows used: bottom', VN, 'far', round(VN - K * dn * (1 / (1230 - HI) - 1 / dn)), 'of', SHEET.shape[0])

Il = cv2.cvtColor(I, cv2.COLOR_BGR2LAB).astype(np.float32); Wl = cv2.cvtColor(W, cv2.COLOR_BGR2LAB).astype(np.float32)
inm = M > 0
# light of this photo: bright blade-tip envelope (lit tips stay bright in sun, drop in shade), relative to each row's sunlit level
L = Il[..., 0]
E = cv2.GaussianBlur(cv2.dilate(L, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))), (0, 0), 5)
ref = np.full(h, np.nan, np.float32)
for y in range(h):
    v = E[y][inm[y]]
    if v.size > 40: ref[y] = np.percentile(v, 75)
ys = np.arange(h); ok = ~np.isnan(ref); ref = np.interp(ys, ys[ok], ref[ok]); ref = cv2.GaussianBlur(ref.reshape(-1, 1), (0, 0), 30).ravel()
Sh = np.clip(E / ref[:, None], 0.25, 1.15)
Sh = np.where(Sh > 0.94, 1 + (Sh - 1) * 0.15, Sh)
Sh = np.clip((Sh - 0.94) * 1.8 + 0.94, 0.3, 1.04)
Sh = cv2.GaussianBlur(Sh, (0, 0), 3)
sun = inm & (Sh > 0.97)
# texture's own light, flattened (its shadows are not this yard's shadows)
Lt = Wl[..., 0]; Lt_low = cv2.GaussianBlur(Lt, (0, 0), 40)
Lt_flat = Lt - Lt_low + np.median(Lt[inm])
# tone/colour per distance band: map the texture's brightness distribution onto this photo's sunlit lawn in that band, but
# keep the texture's own detail contrast (overgrown turf is rougher than a cut lawn) and its own hue variation, pulled
# toward this photo's white balance
centers = [1240, 1380, 1560, 1760, 1960]
q = np.linspace(0, 100, 101); outs = []
for cy in centers:
    y0, y1 = max(0, cy - 70), min(h, cy + 70)
    tb = inm[y0:y1]; sb = sun[y0:y1]
    if sb.sum() < 500: sb = tb
    y0, y1 = max(0, cy - 110), min(h, cy + 110); tb = inm[y0:y1]; sb = sun[y0:y1]
    if sb.sum() < 500: sb = tb
    qs = np.percentile(Il[y0:y1, :, 0][sb], q); qt = np.percentile(Lt_flat[y0:y1][tb], q)
    Lm = np.interp(Lt_flat, qt, qs)
    Lm = Lm + (Lt_flat - np.interp(Lt_flat, qt, qt)) * 0  # (identity; keeps the mapping monotone)
    a_t, b_t = Wl[..., 1], Wl[..., 2]
    a_mu_t, b_mu_t = a_t[y0:y1][tb].mean(), b_t[y0:y1][tb].mean()
    a_mu_s, b_mu_s = Il[y0:y1, :, 1][sb].mean(), Il[y0:y1, :, 2][sb].mean()
    # neglected grass: a little less green (a toward neutral) and warmer/yellower than the cared-for lawn
    A2 = (a_t - a_mu_t) * 0.85 + a_mu_s
    B2 = (b_t - b_mu_t) * 0.85 + b_mu_s
    outs.append(np.dstack([Lm, A2, B2]))
O = np.zeros_like(Il)
for i in range(len(centers) - 1):
    c0, c1 = centers[i], centers[i + 1]
    sel = (ys >= (0 if i == 0 else c0)) & (ys < (h if i == len(centers) - 2 else c1))
    t = np.clip((ys[sel] - c0) / (c1 - c0), 0, 1)[:, None, None]
    O[sel] = outs[i][sel] * (1 - t) + outs[i + 1][sel] * t
# natural, patchy variation: thinner/drier and lusher areas at lawn scale
def blob(s, amp):
    n = cv2.GaussianBlur(rng.standard_normal((h, w)).astype(np.float32), (0, 0), s); return n / n.std() * amp
dry = np.clip(blob(70, 1.0), 0, None) ** 1.5 * 0.12
O[..., 0] += blob(40, 3.0) + dry * 4
O[..., 1] += dry * 5.0          # toward straw
O[..., 2] += dry * 6.0
# this yard's light: broad light/shadow of the original lawn (large scale, relative to each row's sunlit level) plus the
# crisp shadows from the envelope; taller grass also self-shades a little more than a cut lawn
Lbroad = cv2.GaussianBlur(np.where(inm, L, 0), (0, 0), 7) / np.maximum(cv2.GaussianBlur(inm.astype(np.float32), (0, 0), 7), 1e-3)
refb = np.full(h, np.nan, np.float32)
for y in range(h):
    v = Lbroad[y][inm[y]]
    if v.size > 40: refb[y] = np.percentile(v, 80)
okb = ~np.isnan(refb); refb = np.interp(ys, ys[okb], refb[okb]); refb = cv2.GaussianBlur(refb.reshape(-1, 1), (0, 0), 30).ravel()
Sb = np.clip(Lbroad / refb[:, None], 0.55, 1.05)
_lm = cv2.GaussianBlur(O[..., 0], (0, 0), 6); O[..., 0] = (O[..., 0] - _lm) * 1.15 + _lm + 9          # rougher turf: a touch more local contrast
O[..., 0] *= np.minimum(Sh, Sb)
Sh = np.minimum(Sh, Sb)
shade = np.clip(1 - Sh, 0, 1); O[..., 2] -= shade * 8; O[..., 1] += shade * 1.5
R = cv2.cvtColor(np.clip(O, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
# edges: overgrown blades spill a few px over the paver/bed edges (irregular), instead of a crisp cut line
grow = cv2.dilate(M, np.ones((7, 7), np.uint8))
edge_noise = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), 1.2)
spill = np.zeros((h, w), np.float32)
# blade-like spill: only where the texture is bright (lit blades), so it reads as grass tips, not a halo
tip = np.clip((cv2.cvtColor(R.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32) - 90) / 60, 0, 1)
alpha = np.maximum(cv2.GaussianBlur(M.astype(np.float32) / 255, (0, 0), 1.0), spill * tip * 0.85)
alpha[:1215] = 0
res = R * alpha[..., None] + I.astype(np.float32) * (1 - alpha[..., None])
cv2.imwrite(out_path, np.clip(res, 0, 255).astype(np.uint8))
cv2.imwrite('warp-preview.jpg', W)
print('ok', out_path)
