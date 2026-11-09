import cv2, numpy as np
I = cv2.imread('../src/assets/img/clean-1008.webp'); h, w = I.shape[:2]
hsv = cv2.cvtColor(I, cv2.COLOR_BGR2HSV); H, S, V = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
g = ((H >= 28) & (H <= 58) & (S >= 70) & (V >= 70)).astype(np.uint8) * 255
g[:598] = 0
# island planting bed and house-front shrub line are not lawn
bed = np.zeros_like(g)
cv2.ellipse(bed, (1160, 685), (255, 38), 0, 0, 360, 255, -1)   # planting inside the island ring
cv2.rectangle(bed, (0, 598), (w, 628), 255, -1)                 # shrub line along the house (keeps lawn below)
g[bed > 0] = 0
# restore thin lawn strips between y 598-628 that are actual turf (left lawn edge, right strip)
strip = ((H >= 30) & (H <= 52) & (S >= 110) & (V >= 120)).astype(np.uint8) * 255
strip[:598] = 0; strip[630:] = 0
dark_shrub = cv2.GaussianBlur((V < 120).astype(np.float32), (0, 0), 3) > 0.15
strip[dark_shrub] = 0
g = cv2.max(g, strip)
g = cv2.morphologyEx(g, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
g = cv2.morphologyEx(g, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(g)
keep = np.zeros_like(g)
for k in range(1, n):
    if st[k, cv2.CC_STAT_AREA] > 3000: keep[lab == k] = 255
cv2.imwrite('mask1008.png', keep)
vis = I.copy(); vis[keep > 0] = (vis[keep > 0] * 0.4 + np.array([255, 0, 255]) * 0.6).astype(np.uint8)
cv2.imwrite('maskvis.jpg', cv2.resize(vis[480:], (1200, int((h - 480) * 1200 / w))))
print((keep > 0).mean())
