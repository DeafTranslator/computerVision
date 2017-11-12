import cv2
import os
import glob
import tools
import numpy as np
import math

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\2-11-2017\\Jesus\\simpleCrop'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['nombre']
classes = classesDinamic

frame = None
roiPts = [(106, 288), (176, 278), (216, 232), (148, 253), (111, 227), (172, 188), (169, 134)]
inputMode = False

roiPts = []

cantPoint = 4

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

        xmax = x + frame.shape[1]*0.035
        ymax = y + frame.shape[0]*0.03
        
        print("xmax: ", xmax)
        print("ymax: ", ymax)

        cv2.rectangle(frame, (x,y), (int(xmax), int(ymax) ), (0,0,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str((len(roiPts))),(int(x), int(y)), font, 1,(255,255,255),2)

        i = 0
        if len(roiPts) >cantPoint-1:
          while(i < cantPoint):
            xmax = roiPts[i][0] + frame.shape[1]*0.035
            ymax = roiPts[i][1] + frame.shape[0]*0.03
            cv2.rectangle(frame, roiPts[i], (int(xmax), int(ymax) ), (0,255,0),2)
            cv2.putText(frame, 'Press any key',(int(frame.shape[1]*0.35), int(frame.shape[0]*0.2)), font, 1,(0,255,0),3)
            i += 1
        cv2.imshow("frame", frame)

k = 0

def readFolder():
    global frame, roiPts, inputMode
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)
    vainita = False
    time = 1
    begin = False
    k = ord("p")
    fingerTips = []
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(train_path, fld,'*g')
        files = glob.glob(path)

        lower = []
        upper = []

        for fl in files:
            frame = cv2.imread(fl)
            frame = tools.resize(frame, 450, 700)

            if k == ord("d"):
              inputMode = True
              while len(roiPts) < 4:
                  cv2.imshow("frame", frame)
                  cv2.waitKey(0)
              begin = True
            elif k == ord("s"):
                cv2.waitKey(0)

            gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            fdifetente = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
            # print(fdifetente)
            # cv2.imshow("ress",fdifetente[1])

            hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HLS)

            # if k == ord("d"):
            

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
              blurFrame = cv2.blur(frame.copy(),(25,25))
              hsvB = cv2.cvtColor(blurFrame, cv2.COLOR_BGR2HLS)

              print("lower", lower)
              print("upper", upper)

              # upper, 29, 124, 150
              # lower, 0, 65, 13
              output = tools.mergeColorsImage(hsvB, lower, upper)
              res = cv2.bitwise_and(frame, frame, mask= output)
              median = cv2.medianBlur(output,7)
              
              ###############################################################
              # makeContours
              image, contours, hierarchy = cv2.findContours(median, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
              cIdx = tools.findBiggestContour(contours)
              hullP = [(0, 0)] * len(contours)
              hullI = [0] * len(contours)
              defects = [(0, 0, 0, 0)] * len(contours)

              cv2.imshow("res",res)
              cv2.imshow("output ", median)
            cv2.imshow("frame", frame)
            k = cv2.waitKey(1)
       
            if k == ord("q"):
                break

        if k == ord("q"):
            break

readFolder()
