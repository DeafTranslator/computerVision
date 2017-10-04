import cv2
import os
import glob
import tools
import numpy as np
import math

train_path ='C:\\Users\\Juan Graciano\\Desktop\\d'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\d\\saved'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']

classes = classesNum


frame = None
cantPoint = 7
roiPts = [(172, 315), (203, 314), (177, 285), (210, 287), (183, 256), (218, 254), (205, 228)]
roiPts = [(106, 288), (176, 278), (216, 232), (148, 253), (111, 227), (172, 188), (169, 134)]
inputMode = False

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()

def selectROI(event, x, y, flags, param):
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode

    # if we are in ROI selection mode, the mouse was clicked,
    # and we do not already have four points, then update the
    # list of ROI points with the (x, y) location of the click
    # and draw the circle
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < cantPoint:
        roiPts.append((x, y))
        print("x: ", x)
        print("y: ", y)

        xmax = x + frame.shape[1]*0.045
        ymax = y + frame.shape[0]*0.045
        
        print("xmax: ", xmax)
        print("ymax: ", ymax)

        cv2.rectangle(frame, (x,y), (int(xmax), int(ymax) ), (0,0,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str((len(roiPts))),(int(x), int(y)), font, 1,(255,255,255),2)

        i = 0
        if len(roiPts) >cantPoint-1:
          while(i < cantPoint):
            xmax = roiPts[i][0] + frame.shape[1]*0.045
            ymax = roiPts[i][1] + frame.shape[0]*0.045
            cv2.rectangle(frame, roiPts[i], (int(xmax), int(ymax) ), (0,255,0),2)
            cv2.putText(frame, 'Press any key',(int(frame.shape[1]*0.35), int(frame.shape[0]*0.2)), font, 1,(0,255,0),3)
            i += 1
        cv2.imshow("frame", frame)

k = 0
def readFolder():
    global frame, roiPts, inputMode
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)
    roiBox =  None
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(train_path, fld,'*g')
        files = glob.glob(path)
        for fl in files:
            frame = cv2.imread(fl)
            name = os.path.basename(fl)
            # frame = tools.resize(frame, 711, 400)
        
            
            # if inputMode is not False:
            #     y0 = roiPts[3][1]
            #     y1 = roiPts[0][1]
            #     x0 = roiPts[0][0]
            #     x1 = roiPts[3][0]
                
            frame = tools.CropHand(frame)
            # cv2.imshow("frame", frame)

            if inputMode is False:
                k = ord("i")
            else:
                # tools.saveImage(name, frame.copy(), save_path, fld, 'tape')
                k = cv2.waitKey(1)

            if k == ord("i"):
                inputMode = True
                orig = frame.copy()

                while len(roiPts) < 4:
                    cv2.imshow("frame", frame)
                    cv2.waitKey(0)
                    
            elif k == ord("q"):
                break
            else :
                pass
        if k == ord("q"):
            break

    print('Terminamo')

def readimage():
    global frame, roiPts, inputMode
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)
    roiBox =  None
    print('Reading images')
    path = os.path.join(train_path, '*g')
    files = glob.glob(path)
    for fl in files:
        frame = cv2.imread(fl)
        name = os.path.basename(fl)
        frame = tools.resize(frame, 400, 711)
        
        # if inputMode is not False:
        #     y0 = roiPts[3][1]
        #     y1 = roiPts[0][1]
        #     x0 = roiPts[0][0]
        #     x1 = roiPts[3][0]
        #     # frame = tools.detectTape(frame[y0:y1, x0:x1])
        # frame = cv2.Canny(frame, 100, 255)
        hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
        value = (5, 5)
        blurred = cv2.GaussianBlur(gray.copy(), value, 0)
        # thresh1 = cv2.adaptiveThreshold(gray, 100, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
        _, thresh2 = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        cv2.imshow("frame", hsv)
        cv2.imshow("gray", gray)
        cv2.imshow("thresh2", thresh2)


        if inputMode is False:
            k = ord("i")
        else:
            # tools.saveImage(name, frame.copy(), save_path, fld, 'tape')
            k = cv2.waitKey(0)

        if k == ord("i"):
            inputMode = True
            orig = frame.copy()

            while len(roiPts) < 4:
                cv2.imshow("frames", frame)
                cv2.waitKey(0)
                
        elif k == ord("q"):
            break
        else :
            pass
        if k == ord("q"):
            break

    print('Terminamo')

def readVideo():
  global frame, roiPts, inputMode
  cv2.namedWindow("frame")
  cv2.setMouseCallback("frame", selectROI)
  roiBox =  None
  cap = cv2.VideoCapture(0)
  k = ord("n")
  vainita = False
  time = 20
  begin = False

  lower = []
  upper = []
  fingerTips = []
  while( cap.isOpened() ) :
      ret,frame = cap.read()
      # frame = tools.resize(frame, 400, 711)

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
        
        ####
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
