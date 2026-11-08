import cv2, numpy as np, sys
a=cv2.imread('src/assets/img/ba-before.webp'); b=cv2.imread('src/assets/img/ba-after.webp')
sift=cv2.SIFT_create(8000)
ka,da=sift.detectAndCompute(cv2.cvtColor(a,cv2.COLOR_BGR2GRAY),None)
kb,db=sift.detectAndCompute(cv2.cvtColor(b,cv2.COLOR_BGR2GRAY),None)
m=cv2.BFMatcher().knnMatch(da,db,k=2)
good=[x for x,y in m if x.distance<0.72*y.distance]
print('kp',len(ka),len(kb),'good',len(good))
pa=np.float32([ka[g.queryIdx].pt for g in good]); pb=np.float32([kb[g.trainIdx].pt for g in good])
H,mask=cv2.findHomography(pa,pb,cv2.RANSAC,4.0)
print('inliers',int(mask.sum())); print(H)
# where does the before frame land in the after image
h,w=a.shape[:2]
c=cv2.perspectiveTransform(np.float32([[0,0],[w,0],[w,h],[0,h]]).reshape(-1,1,2),H); print(c.reshape(-1,2))
inl=pa[mask.ravel()==1]; print('before inlier y range',inl[:,1].min(),inl[:,1].max(),'x',inl[:,0].min(),inl[:,0].max())
