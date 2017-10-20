import cv2
import numpy as np

k = 0

def readVideo():
  cap = cv2.VideoCapture(0)

  while( cap.isOpened() ) :
      ret,img = cap.read()

      img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

      # lower mask (0-10)
      lower_red = np.array([0,50,50])
      upper_red = np.array([10,255,255])
      mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

      # upper mask (170-180)
      lower_red = np.array([170,50,50])
      upper_red = np.array([180,255,255])
      mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

      # join my masks
      mask = mask0+mask1

      # set my output img to zero everywhere except my mask
      output_img = img.copy()
      output_img[np.where(mask==0)] = 0

      # or your HSV image, which I *believe* is what you want
      output_hsv = img_hsv.copy()
      output_hsv[np.where(mask==0)] = 0

      cv2.imshow("output_img", output_img)
      cv2.imshow("output_hsv", output_hsv)

      k = cv2.waitKey(1)

      if k == ord("q"):
          break

readVideo()
