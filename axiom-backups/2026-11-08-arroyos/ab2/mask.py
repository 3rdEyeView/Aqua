import cv2, numpy as np
I = cv2.imread('../src/assets/img/project-2001.webp'); h, w = I.shape[:2]
hsv = cv2.cvtColor(I, cv2.COLOR_BGR2HSV); H, S, V = [hsv[..., k].astype(int) for k in range(3)]
g = ((H >= 28) & (H <= 55) & (S >= 90) & (V >= 80)).astype(np.uint8) * 255
g[:int(1225)] = 0                       # above the lake bank: no lawn
# planting bed region (plants are green too): exclude a polygon around the bed, keep the lawn below its mulch edge
bed = np.array([(0, 1250), (420, 1250), (900, 1230), (1080, 1310), (1300, 1380), (1310, 1440), (1140, 1500),
                (800, 1530), (500, 1520), (200, 1500), (0, 1470)], np.int32)
B = np.zeros_like(g); cv2.fillPoly(B, [bed], 255)
mulch = ((V < 110) | (S < 60)).astype(np.uint8) * 255   # dark mulch / rocks / shadows inside the bed area
inside = cv2.bitwise_and(B, cv2.bitwise_not(cv2.dilate(mulch, np.ones((3, 3), np.uint8))))
g[B > 0] = 0
# the bed's lawn side: grass below the mulch edge is handled by the colour test once the polygon is dilated a bit less
g = cv2.morphologyEx(g, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
g = cv2.morphologyEx(g, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(g); keep = np.zeros_like(g)
for k in range(1, n):
    if st[k, cv2.CC_STAT_AREA] > 4000: keep[lab == k] = 255
# fill interior holes (dark blade gaps / shadows) without filling the bed: flood the non-lawn from the top edge
inv = cv2.bitwise_not(keep); ff = inv.copy(); fm = np.zeros((h + 2, w + 2), np.uint8)
for x in range(0, w, 20):
    if ff[1300, x] == 255: cv2.floodFill(ff, fm, (x, 1300), 128)
for x in range(0, w, 20):
    if ff[0, x] == 255: cv2.floodFill(ff, fm, (x, 0), 128)
keep[ff == 255] = 255            # enclosed holes
cv2.imwrite('mask.png', keep)
vis = I.copy(); vis[keep > 0] = (vis[keep > 0] * 0.4 + np.array([255, 0, 255]) * 0.6).astype(np.uint8)
cv2.imwrite('maskvis.jpg', cv2.resize(vis[1100:], (800, int((h - 1100) * 0.5))))
print((keep > 0).mean())
