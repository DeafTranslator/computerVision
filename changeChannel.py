import cv2
import os
import glob
import tools
import numpy as np


img = cv2.imread("C:\\Users\\Juan Graciano\\Desktop\\Nati videos\\juan\\numero2\\cropV3\\0\\0-25-Tapecrop-cropV2-cropV3.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img2 = np.zeros_like(img)
img2[:,:,0] = gray
img2[:,:,1] = gray
img2[:,:,2] = gray

cv2.circle(img2, (10,10), 5, (255,255,0))
cv2.imshow("original", img)

cv2.imshow("gray", gray)

cv2.imshow("colour again", img2)
print("original", img.shape)
print("gray", gray.shape)
print("colour again", img2.shape)
cv2.waitKey()