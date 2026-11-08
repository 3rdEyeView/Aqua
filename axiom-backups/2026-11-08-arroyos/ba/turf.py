"""Grass-only visualization: before photo with its lawn replaced by mowed turf texture from the existing after photo.
Everything outside the lawn mask is the untouched before photo. Before's own shadows/sunlight are re-applied."""
import cv2, numpy as np, sys
rng = np.random.default_rng(7)
B = cv2.imread('src/assets/img/ba-before.webp'); A = cv2.imread('src/assets/img/ba-after.webp')
h, w = B.shape[:2]
# 1) lawn mask: region below the bed / hedge line, refined by grass colour near the boundary
top = np.array([(0,127),(240,124),(338,128),(332,150),(420,172),(540,203),(760,199),(1000,198),(1100,188),(1275,153),
                (1225,128),(1208,92),(1400,84),(1520,82),(1600,80),(1600,h),(0,h)], np.int32)
region = np.zeros((h,w), np.uint8); cv2.fillPoly(region, [top], 255)
hsv = cv2.cvtColor(B, cv2.COLOR_BGR2HSV)
grass = ((hsv[...,0] >= 28) & (hsv[...,0] <= 62) & (hsv[...,1] >= 70)).astype(np.uint8)*255
grass = cv2.morphologyEx(grass, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
core = cv2.erode(region, np.ones((25,25),np.uint8))          # deep inside the lawn: always grass (incl. shadows)
band = cv2.subtract(region, core)                              # near the edge: only grass-coloured pixels
mask = cv2.max(core, cv2.bitwise_and(band, grass))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
m = cv2.GaussianBlur(mask.astype(np.float32)/255, (0,0), 1.6)
# 2) warp the after's sunlit lawn onto the before's ground plane
src = np.float32([(0,92),(w,92),(w,h),(0,h)])
dst = np.float32([tuple(map(float, p)) for p in [(170,232),(1430,232),(1585,690),(25,690)]])
Hm = cv2.getPerspectiveTransform(src, dst)
T = cv2.warpPerspective(A, Hm, (w,h), flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
yy = np.linspace(1, 0, h, dtype=np.float32)[:,None,None]
Tf = T.astype(np.float32); Tb = cv2.GaussianBlur(Tf, (0,0), 1.2)
T = np.clip(Tf + (Tf - Tb) * (0.35 + 0.9 * yy), 0, 255).astype(np.uint8)
# 3) colour: match texture to the before's sunlit grass tone (same light), keep its own detail
Bl = cv2.cvtColor(B, cv2.COLOR_BGR2LAB).astype(np.float32); Tl = cv2.cvtColor(T, cv2.COLOR_BGR2LAB).astype(np.float32)
L = Bl[...,0]
# illumination from the bright blade-tip envelope: lit tips stay bright in sun, drop in shade
E = cv2.dilate(L, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)))
E = cv2.GaussianBlur(E, (0,0), 3.0)
inm = mask > 128
ref = np.zeros(h, np.float32)
for y in range(h):
    v = E[y][inm[y]]; ref[y] = np.percentile(v, 70) if v.size > 20 else np.nan
idx = np.arange(h); ok = ~np.isnan(ref); ref = np.interp(idx, idx[ok], ref[ok]); ref = cv2.GaussianBlur(ref.reshape(-1,1), (0,0), 25).ravel()
S = np.clip(E / ref[:,None], 0.2, 1.2)
S = np.where(S > 0.95, 1 + (S-1)*0.2, S)                      # flatten sunlit variation, keep real shadows
S = np.clip((S - 0.95) * 2.1 + 0.95, 0.3, 1.04)                 # deepen shade to match the original contrast
S = cv2.GaussianBlur(S, (0,0), 1.8)
sun = inm & (S > 0.97)
# tone + colour transfer per distance band: quantile-map L to the before's sunlit grass in that band,
# then give each brightness level the before's own a/b (warm yellow-green tips, deeper green gaps)
centers = [110, 220, 360, 520, 650]; q = np.linspace(0, 100, 101)
Lt, At, Bt = Tl[...,0], Tl[...,1], Tl[...,2]
outs = []
for cy in centers:
    y0, y1 = max(0, cy-90), min(h, cy+90)
    sb = sun[y0:y1]; tb = inm[y0:y1]
    Lsrc = Bl[y0:y1,:,0][sb]; Asrc = Bl[y0:y1,:,1][sb]; Bsrc = Bl[y0:y1,:,2][sb]
    qt = np.percentile(Lt[y0:y1][tb], q); qs = np.percentile(Lsrc, q)
    Lm = np.interp(Lt, qt, qs)
    bins = np.linspace(0, 255, 33); bi = np.clip(np.digitize(Lsrc, bins)-1, 0, 31)
    am = np.array([Asrc[bi==k].mean() if (bi==k).sum() > 30 else np.nan for k in range(32)])
    bm = np.array([Bsrc[bi==k].mean() if (bi==k).sum() > 30 else np.nan for k in range(32)])
    cx = (bins[:-1]+bins[1:])/2; ok = ~np.isnan(am)
    ti = np.clip(np.digitize(Lt[y0:y1][tb], bins)-1, 0, 31)
    tam = np.array([At[y0:y1][tb][ti==k].mean() if (ti==k).sum() > 30 else np.nan for k in range(32)])
    tbm = np.array([Bt[y0:y1][tb][ti==k].mean() if (ti==k).sum() > 30 else np.nan for k in range(32)])
    ok2 = ~np.isnan(tam)
    A2 = np.interp(Lm, cx[ok], am[ok]) + (At - np.interp(Lt, cx[ok2], tam[ok2])) * 0.7
    B2 = np.interp(Lm, cx[ok], bm[ok]) + (Bt - np.interp(Lt, cx[ok2], tbm[ok2])) * 0.7
    outs.append(np.dstack([Lm, A2, B2]))
out = np.zeros_like(Tl); ys = np.arange(h)
for i in range(len(centers)-1):
    c0, c1 = centers[i], centers[i+1]
    sel = (ys >= (0 if i == 0 else c0)) & (ys < (h if i == len(centers)-2 else c1))
    t = np.clip((ys[sel]-c0)/(c1-c0), 0, 1)[:,None,None]
    out[sel] = outs[i][sel]*(1-t) + outs[i+1][sel]*t
# natural variation: soft low-frequency patches in lightness and green-yellow balance
def blob(s, amp):
    n = cv2.GaussianBlur(rng.standard_normal((h,w)).astype(np.float32), (0,0), s); return n / n.std() * amp
out[...,0] += blob(45, 2.5); out[...,2] += blob(60, 2.2); out[...,1] += blob(70, 1.0)
# re-apply before's lighting: shadows darken and cool, like the original shade
out[...,0] = out[...,0] * S
shade = np.clip(1 - S, 0, 1)
out[...,2] -= shade * 10; out[...,1] += shade * 1.5
# slight distance haze: match before's far-row contrast
R = cv2.cvtColor(np.clip(out,0,255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
res = R * m[...,None] + B.astype(np.float32) * (1 - m[...,None])
res = np.clip(res, 0, 255).astype(np.uint8)
cv2.imwrite('ba/after-vis.png', res); cv2.imwrite('ba/mask.png', mask); cv2.imwrite('ba/warp.jpg', T)
print('lawn px', inm.sum(), 'of', h*w)
