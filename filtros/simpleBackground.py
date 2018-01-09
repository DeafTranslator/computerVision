import numpy as np
import cv2
cap = cv2.VideoCapture('C:\\Users\\Juan Graciano\\Desktop\\Nati videos\\juan\\videos\\nati\\a.mp4')

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=0)

# while(1):
#     ret, frame = cap.read()
#     fgmask = fgbg.apply(frame)
#     # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    
#     res = cv2.bitwise_and(frame, frame, mask = fgmask)

#     cv2.imshow('frame',res)
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()

def readVideo():
  global frame, roiPts, inputMode
  cap = cv2.VideoCapture(0)
 
  while( cap.isOpened() ) :
      ret,frame = cap.read()

      fgmask = fgbg.apply(frame)
      fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

      res = cv2.bitwise_and(frame, frame, mask = fgmask)

      cv2.imshow("frame", frame)
      cv2.imshow("res", res)
      k = cv2.waitKey(1)

      if k == ord("q"):
          break

readVideo()