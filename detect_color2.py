import cv2
import os
import glob
import tools
import numpy as np
import math


frame = None
# roiPts = [(172, 315), (203, 314), (177, 285), (210, 287), (183, 256), (218, 254), (205, 228)]
roiPts = [(106, 288), (176, 278), (216, 232), (148, 253), (111, 227), (172, 188), (169, 134)]
inputMode = False

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()

k = 0
def readVideo():
  global frame, roiPts
  cap = cv2.VideoCapture(0)
  vainita = False
  time = 20
  begin = False

  lower = []
  upper = []
  fingerTips = []
  while( cap.isOpened() ) :
      ret,frame = cap.read()

      hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HLS)

      if k == ord("d"):
        begin = True

      if time > 0:
        frame = tools.drawRectangle(frame, roiPts)

      if time > 0 and begin:
        l, u =  tools.boundsColor(hsv, roiPts)
        lower.append(l)
        upper.append(u)
        time -= 1
      elif time <= 0:
        vainita = True
        lower = np.array(lower)
        upper = np.array(upper)
        begin = False
        
      if vainita:
        blurFrame = cv2.blur(frame.copy(),(5,5))
        hsvB = cv2.cvtColor(blurFrame, cv2.COLOR_BGR2HLS)
        output, bw = tools.mergeColorsImage(hsvB, lower, upper)
        res = cv2.bitwise_and(frame, frame, mask= output)
        median = cv2.medianBlur(output,7)
        
        ###############################################################
        # makeContours
        image, contours, hierarchy = cv2.findContours(median, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cIdx = tools.findBiggestContour(contours)
        hullP = [(0, 0)] * len(contours)
        hullI = [0] * len(contours)
        defects = [(0, 0, 0, 0)] * len(contours)

        if cIdx is not -1:
          bRect = cv2.boundingRect(contours[cIdx])

          hullP[cIdx] = cv2.convexHull(contours[cIdx],returnPoints=True)
          hullI[cIdx] = cv2.convexHull(contours[cIdx],returnPoints=False)
          hullP[cIdx] = cv2.approxPolyDP(contours[cIdx],18,True)
         
          if len(contours[cIdx]) > 3:
            # hull = cv2.convexHull(contours[cIdx], returnPoints=False)
            defects[cIdx] = cv2.convexityDefects(contours[cIdx], hullI[cIdx])
            contours[cIdx], defects[cIdx] = tools.eleminateDefects(median, bRect, defects, contours[cIdx], cIdx)
            # print(defects)
            # count_defects = 0
            # for i in range(defects.shape[0]):
            #   print("ggggggggg", defects[i])
            #   s = defects[i, 0][0]
            #   e = defects[i, 0][1]
            #   f = defects[i, 0][2]
            #   d = defects[i, 0][3]
            #   print(contours[cIdx].shape)
            #   start = tuple(contours[cIdx][s][0])
            #   end = tuple(contours[cIdx][e][0])
            #   far = tuple(contours[cIdx][f][0])

            #   # find length of all sides of triangle
            #   a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            #   b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            #   c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

            #   # apply cosine rule here
            #   angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c)) * 57

            #   # ignore angles > 90 and highlight rest with red dots
            #   if angle <= 90:
            #       count_defects += 1
            #       cv2.circle(frame, far, 1, [0, 0, 255], 3)
            #   # dist = cv2.pointPolygonTest(cnt,far,True)

            #   # draw a line from start to end i.e. the convex points (finger tips)
            #   # (can skip this part)
            #   cv2.circle(frame, end, 5, [255, 255, 0], 3)

          isHand = tools.detectIfHand(bRect, fingerTips)

          print("isHand", isHand)

          if isHand: 
            fingerTips = tools.getFingerTips(fingerTips, contours[cIdx], defects[cIdx], median, bRect, hullP[cIdx])
          #   frame = tools.drawFingerTips(fingerTips, frame)
          #   frame = tools.myDrawContours(frame, defects, hullP, cIdx, bRect, output, contours[cIdx])

        cv2.imshow("res",res)
        cv2.imshow("output ", median)
      cv2.imshow("frame", frame)
      k = cv2.waitKey(1)

      if k == ord("q"):
          break

readVideo()
