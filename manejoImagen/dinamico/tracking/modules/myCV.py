import os
import math
import cv2
import numpy as np
import argparse
import random
import sys
sys.path.append("../..")
import setup
# import imutils


def distanceP2P(a,b):
    return math.sqrt(math.fabs(math.pow((a[0][0]-b[0][0]),2) + math.pow((a[0][1]-b[0][1]),2)))  

def getAngle(s, f, e):
    l1 = distanceP2P(f,s)
    l2 = distanceP2P(f,e)
    dot = (s[0][0]-f[0][0])*(e[0][0]-f[0][0]) + (s[0][1]-f[0][1])*(e[0][1]-f[0][1])
    angle = math.acos(dot/(l1*l2))
    angle = angle*180/math.pi
    return angle

def removeRedundantEndPoints(newDefects, median, bRect, contours):
    tolerance = bRect[2]/6
    startidx, endidx, faridx = (0, 0, 0)
    startidx2, endidx2 = (0, 0)
    thisContours = -1
    for i in range(0, len(newDefects)):
        for j in range(0, len(newDefects)):
            startidx = newDefects[i][0]
            ptStart = contours[startidx] 
            endidx = newDefects[i][1]
            ptEnd = contours[endidx]
            startidx2 = newDefects[j][0] 
            ptStart2 = contours[startidx2]
            endidx2 = newDefects[j][1]
            ptEnd2 = contours[endidx2]
            if(distanceP2P(ptStart,ptEnd2) < tolerance ):
                thisContours = ptEnd2
                break
            if(distanceP2P(ptEnd,ptStart2) < tolerance ):
                thisContours = ptEnd

    return thisContours, startidx2
   
def detectIfHand(bRect, fingerTips):
    h = bRect[3]
    w = bRect[2]
    isHand = True
    if len(fingerTips) > 5:
        isHand = False
    elif h == 0 or w == 0 :
        isHand = False
    elif h/w > 4 or w/h > 4:
        isHand = False   
    elif(bRect[0] < 20):
        isHand = False  
    
    return isHand

def eleminateDefects(median, bRect, defects, contours, cIdx):
    tolerance = bRect[3]/5
    angleTol = 95
    newDefects = []
    startidx, endidx, faridx = (0, 0, 0) # No se
  
    for d in defects[cIdx]: #Cambio
      v = d[0]
      startidx = v[0]
      ptStart = contours[startidx]
      endidx = v[1]
      ptEnd = contours[endidx]
      faridx = v[2] 
      ptFar = contours[faridx]

      if distanceP2P(ptStart, ptFar) > tolerance and distanceP2P(ptEnd, ptFar) > tolerance and getAngle(ptStart, ptFar, ptEnd) < tolerance:
        if ptEnd[0][1] > (bRect[1] + bRect[3] - bRect[3]/4):
          pass
        elif ptStart[0][1] > (bRect[1] + bRect[3] -bRect[3]/4 ):
          pass
        else:
            newDefects.append(v) 

    if len(newDefects)>0:
        # print(newDefects)
        # print(newDefects[0])
        nrOfDefects = len(newDefects[0])
        # print("nrOfDefects", nrOfDefects)
        # print("\n\n")
        temp = defects[cIdx]
        defects[cIdx] = newDefects[0]
        newDefects = temp
        cStart, start = removeRedundantEndPoints(defects, median, bRect, contours)
        if len(cStart) >= 0:
            contours[start] = cStart
    return contours, defects[cIdx]

def checkForOneFinger(median, bRect, defects, hullP, fingerTips, contours):
    yTol = bRect[3]/6
    highestP = median.shape

    for d in contours:
        v = d
        if v[0][0] < highestP[0]:
            highestP = v[0]
        d += 1 
    
    n = 0
    for d in hullP:
        v = d
        if v[0][1] < (highestP[0] + yTol) and v[0][1] is not highestP[0] and v[0][0] is not highestP[1]:
            n += 1
              
    if n == 0:
        fingerTips.append(highestP)

    return fingerTips

def getFingerTips(fingerTips, contours, defects, median, bRect, hullP):
    fingerTips = []
    i = 0
    for d in defects:
        print("\n que tiene d", d)
        v = d[0]

        startidx = v[0]
        ptStart = contours[startidx]
        endidx = v[1]
        ptEnd = contours[endidx]
        faridx = v[2] 
        ptFar = contours[faridx] 
        if i == 0:
            fingerTips.append(ptStart)
            i += 1
        fingerTips.append(ptEnd);
        i += 1

    if len(fingerTips) == 0:
        print("fingerTips es igual a ccero", fingerTips)
        fingerTips = checkForOneFinger(median, bRect, defects, hullP, fingerTips, contours)

    return fingerTips

def myDrawContours(frame, defects, hullP, cIdx, bRect, output, contours):
    # cv2.drawContours(frame, hullP, cIdx, (0, 255, 0), 2)
    cv2.drawContours(frame, hullP, cIdx, (200,0,0), 2, 8)

    cv2.rectangle(frame,(bRect[0], bRect[1]),(bRect[2], bRect[3]), (0,0,200)) 
    d = 0
    
    fontFace = cv2.FONT_HERSHEY_PLAIN;
    channels = []
    result = np.array([])
    i = 0
    while i < 3:
        channels.append(output)
        i += 1         
    
    channels = np.array(channels)
    # print(channels)
    cv2.imshow("mostrar", output)
    cv2.waitKey(0)
    cv2.merge(channels, result)
    # drawContours(result,hg->contours,hg->cIdx,cv::Scalar(0,200,0),6, 8, vector<Vec4i>(), 0, Point());
    cv2.drawContours(result, hullP, cIdx, (0,0,250), 10, 8)

        
    while d < len(defects):
        v = defects[d]
        startidx = v[0] 
        ptStart = contours[startidx] 
        endidx = v[1] 
        ptEnd = contours[endidx] 
        faridx = v[2]
        ptFar = contours[faridx]
        depth = (v[3] / 256)
        """
        line( m->src, ptStart, ptFar, Scalar(0,255,0), 1 )
        line( m->src, ptEnd, ptFar, Scalar(0,255,0), 1 )
        circle( m->src, ptFar,   4, Scalar(0,255,0), 2 )
        circle( m->src, ptEnd,   4, Scalar(0,0,255), 2 )
        circle( m->src, ptStart,   4, Scalar(255,0,0), 2 )
        """
        cv2.circle(result, ptFar, 9, [0,205,0], 5 )

        d += 1

    cv2.imwrite("./contour_defects_before_eliminate.jpg",result)
    
    return result

def drawFingerTips(fingerTips, frame):
    for i in range(len(fingerTips)):
        p = fingerTips[i][0]

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(i),(p[1], p[0]), font, 1,(200,200,200),2)
        cv2.circle(frame, (p[1], p[0]), 5, (100,255,100), 4)

        return frame

# ===============================================================
def resize(img, w, h):
    return cv2.resize(img, (w, h), interpolation = cv2.INTER_CUBIC)

def createFolder(letra, save_path):
    if not os.path.exists(save_path + '\\' + letra):
        os.makedirs(save_path + '\\' + letra)
        print('Folder "', letra, '"created')

def saveImage(name, img, save_path, letra, alias = ''):
    createFolder(letra, save_path)

    name = name.split('.')
    if alias is not '':
        alias = '-' + alias
    print(save_path + '\\' + letra + '\\' + name[0] +alias+'.png')
    cv2.imwrite(save_path + '\\' + letra + '\\' + name[0] +alias+'.png', img)

def drawCircle(contours, frame):
    cnt = max(contours, key=lambda x: cv2.contourArea(x))
    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)

    # finding convex hull
    hull = cv2.convexHull(cnt)

    # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    # cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        # apply cosine rule here
        angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle <= 90:
            count_defects += 1
            cv2.circle(frame, far, 1, [0, 0, 255], 3)
        # dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.circle(frame, end, 5, [255, 0, 0], 3)
    return frame

def fill(edge):
    im_floodfill = edge
    h, w = edge.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    cv2.floodFill(im_floodfill, mask, (0, 0), 255)

    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    im_out = edge | im_floodfill_inv

    cv2.imshow("Filter Melma", im_floodfill)

    return im_floodfill

# frame = resize(frame, 400, 600)
# cv2.resize(frame, (400, 600), interpolation = cv2.INTER_CUBIC)
def changeSize(img, w, h):
    return cv2.resize(img, (w, h), interpolation = cv2.INTER_CUBIC)

def rotateImage(frame, grade):
    # print(frame.shape)
    rows,cols = frame.shape[:2]

    M = cv2.getRotationMatrix2D((cols/2,rows/2), grade, 1)

    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((rows * sin) + (cols * cos))
    nH = int((rows * cos) + (cols * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - (cols/2)
    M[1, 2] += (nH / 2) - (rows/2)

    dst = cv2.warpAffine(frame, M, (nW,nH), flags=cv2.INTER_LINEAR)
    return dst

def rotate(image, angle):
    rotated = imutils.rotate_bound(image, angle)
    # cv2.imshow("Rotated (Correct)", rotated)
    return rotated

def selectROI(event, x, y, flags, param):
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode
 
    # if we are in ROI selection mode, the mouse was clicked,
    # and we do not already have four points, then update the
    # list of ROI points with the (x, y) location of the click
    # and draw the circle
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
        roiPts.append((x, y))
        cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
        cv2.imshow("frame", frame)

def dimensions(frame):
    # # setup initial location of window
    # r,h,c,w = 250,90,400,125  # simply hardcoded the values
    # track_window = (c,r,w,h)
    # # set up the ROI for tracking
    # roi = frame[r:r+h, c:c+w]
    # hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
    # roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
    # cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
    # # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    # term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
    # return track_window, term_crit, roi_hist
    inputMode = True
    orig = frame.copy()

    while len(roiPts) < 4:
        cv2.imshow("frame", frame)
        cv2.waitKey(0)

    # determine the top-left and bottom-right points
    roiPts = np.array(roiPts)
    s = roiPts.sum(axis = 1)
    # print(s)
    tl = roiPts[np.argmin(s)]
    br = roiPts[np.argmax(s)]

    # grab the ROI for the bounding box and convert it
    # to the HSV color space
    roi = orig[tl[1]:br[1], tl[0]:br[0]]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    #roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)

    # compute a HSV histogram for the ROI and store the
    # bounding box
    roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
    roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
    roiBox = (tl[0], tl[1], br[0], br[1])

def trackHand(ret, frame, roiBox, roiHist, termination):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roiHist,[0,180],1)
    # apply meanshift to get the new location
    (ret, roiBox) = cv2.CamShift(dst, roiBox, termination)
    # Draw it on image
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)

    # pts[0][0] += int((2*pts[0][0])/4) 
    # pts[3][0] += int((2*pts[3][0])/4)

    # pts[1][0] -= int((pts[1][0])/8) 
    # pts[2][0] -= int((pts[2][0])/8)

    # roiPts = np.array(pts)
    # s = roiPts.sum(axis = 1)
    # tl = roiPts[np.argmin(s)]
    # br = roiPts[np.argmax(s)]

    # img2 = cv2.rectangle(frame, (br[0],tl[0]), (br[1],tl[1]), (0,255,0),2)
    img2 = cv2.polylines(frame,[pts],True, (0,255,0),2)
    

    cx = int((pts[0][0]+pts[1][0])/2)
    cy = int((pts[0][1]+pts[2][1])/2)
    cv2.circle(frame, (cx, cy), 4, (0, 255, 0), 2)

    return img2

def circlePoint(frame):

    # frame = rotateImage(frame)
    grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    _, thresh1 = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    thresh1 = cv2.erode(thresh1, None, iterations=2)
    thresh1 = cv2.dilate(thresh1, None, iterations=2)

    image, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)

    # finding convex hull
    hull = cv2.convexHull(cnt)

    # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0

    # cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    # ----------------------------------------v------------------------------------------------
    suma = 0
    cantElem = 0    
    c = 0
    vmin = thresh1.shape[0]
    vmax = 0
    endHand = thresh1.shape[1]
    into = False
    while(c < thresh1.shape[0]):
        r = 0
        tape = True
        while(r < thresh1.shape[1]):     
            if thresh1[c][r] != 255:
                if r < vmin:
                    vmin = r
                if r > vmax:
                    vmax = r
                    
                into = True
                tape = False
                # suma += r
                # cantElem += 1
                # cv2.circle(frame, (int(r), int(c)), 5, [0, 255, 255], 10) #amarillo
            r += 1
        if tape == True and into == True:
            endHand = c
            
            break
        c += 1

    optimalAvg = (vmin+vmax)/2

    # ----------------------------------------^------------------------------------------------

    # ----------------------------------------v------------------------------------------------
    
    xmin = 0
    xmax = frame.shape[0]
    xminMid = 0
    xmaxMid = frame.shape[0]
    # i = 0


    avgCenterPoint = (xmax+xmin)/2
    avgCenterPointMid = (xmaxMid+xminMid)/2
    # print("xmax", xmax)
    # print("xmin", xmin)
    # print("avg", avgCenterPoint)
    # print("avgMid", avgCenterPointMid)

    realAvg = (avgCenterPoint+avgCenterPointMid)/2

    # print("realAvg", realAvg)
    font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.circle(frame, (int(avgCenterPointMid), int(frame.shape[1]/2)), 5, [0, 255, 255], 10) #amarillo
    # cv2.putText(frame,'l',(int(avgCenterPointMid), int(frame.shape[1]/2)), font, 1,(255,255,255),1)

    # cv2.circle(frame, (int(avgCenterPoint), int(frame.shape[1]/2)), 5, [0, 128, 255], 10) #naranja
    # cv2.putText(frame,'c',(int(avgCenterPointMid), int(frame.shape[1]/2)), font, 1,(255,255,255),1)

    # cv2.circle(frame, (int(optimalAvg), int(frame.shape[0]/2)), 5, [200, 100, 150], 10)
    # cv2.putText(frame,'r',(int(avgCenterPointMid), int(frame.shape[1]/2)), font, 1,(255,255,255),1)

    # x0Real = realAvg-int(frame.shape[0]/2)+1
    # x1Real = realAvg+int(frame.shape[0]/2)+1

    x0Real = optimalAvg-int((endHand)/2)+1
    x1Real = optimalAvg+int((endHand)/2)-1
    # print("average ", optimalAvg)
    # print("min ", x0Real)
    # print("max ", x1Real)
    # cv2.circle(frame, (int(optimalAvg), int(endHand/2)), 5, [0, 255, 255], 10) #amarillo
    if x0Real >= 0 and x1Real <= frame.shape[1]:
        # cv2.rectangle(frame, (int(x0Real), 0), (int(x1Real), frame.shape[0]-1), (255, 0, 0), 3)
        # cv2.imshow("Real", frame[0:endHand-10, int(x0Real):int(x1Real)])
        # cv2.imshow("Real", frame)
        pass
    else:
        if x0Real < 0:
            x0Real = 0
            x1Real = endHand
            print("la mano termina en " ,endHand)
            print("x es menor que cero", x1Real)
        if x1Real > frame.shape[1]-1:
            x1Real = frame.shape[1]-1
            x0Real = frame.shape[1] - endHand
            if x0Real < 0:
                x0Real = 0
                x1Real = endHand
                print("la mano termina en ", endHand)
                print("x es menor que cero", x1Real)
            print("la mano termina en ", endHand)
            print("x es mayor que la imagen", x0Real)
    print("max ancho ", frame.shape[1])

    # ----------------------------------------^------------------------------------------------

    cv2.imshow("thresh1", thresh1)

    # x-int(h/5.5), y-int(y/20), x+h-int(h/3.5), y+h
    return frame[0:endHand-10, int(x0Real):int(x1Real)]

def drawCircle(contours, frame):
    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)

    # finding convex hull
    hull = cv2.convexHull(cnt)

    # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    # cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        # apply cosine rule here
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle <= 90:
            count_defects += 1
            cv2.circle(frame, far, 1, [0,0,255], -1)
        #dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.circle(frame,far,5,[0,0,255],-1)
        return frame


def orb(gray, frame):
    orb = cv2.ORB_create()
    keypoints = orb.detect(gray, None)
    keypoints, descriptors = orb.compute(gray, keypoints)
    _ = gray
    final_keypoints = cv2.drawKeypoints(frame, keypoints, _, color=(0,255,0), flags=0)
    return final_keypoints

def cropImage1(img):
    print(img.shape)
    aux = img.copy()
    shio = 0
    top = 0
    left = 0
    for kaka in range(img.shape[0]):
        if top == 0 or top == 2:
            aux = np.delete(aux, shio, 0)
        else:
            shio += 1
        if (img[kaka] == [0,0,0]).any():
            top += 1

    shio = 0
    for colum in range(img.shape[1]):
        if left == 0 or left == 2:
            aux = np.delete(aux, shio, 1)
        else:
            shio += 1
        if (img[:, colum] == [0,0,0]).any():
            left += 1
    return aux

def cropImage2(img, x, y, w, h):
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if w > img.shape[1]:
        w = img.shape[1]
    if h > img.shape[0]:
        h = img.shape[0]
    aux = img[y:h, x:w]
    return aux

def detectTape(frame): 

    # Converting image to black and white
    grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    _, thresh1 = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    thresh1 = cv2.erode(thresh1, None, iterations=2)
    thresh1 = cv2.dilate(thresh1, None, iterations=2)

    cv2.imshow("thresh1", thresh1)

    # shape [0] means the y-axis
    # shape [1] means the x-axis
    c = 0
    bottomHand = thresh1.shape[1]
    findHand = False

    while(c < thresh1.shape[0]):
        r = 0
        tape = True
        while(r < thresh1.shape[1]):     
            if thresh1[c][r] != 255:
                findHand = True
                tape = False
                # cv2.circle(frame, (int(r), int(c)), 5, [0, 255, 255], 10) #amarillo
            r += 1
        if tape == True and findHand == True:
            bottomHand = c
            break
        c += 1
        
    if (bottomHand + 2) <= frame.shape[0]:
        bottomHand = bottomHand + 2
    # return frame
    return frame[0:bottomHand, 0:frame.shape[1]-1]

def semiCropImage(frame): 

    # Converting image to black and white
    grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    _, thresh1 = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    thresh1 = cv2.erode(thresh1, None, iterations=2)
    thresh1 = cv2.dilate(thresh1, None, iterations=2)

    # cv2.imshow("thresh1", thresh1)

    # shape [0] means the y-axis
    # shape [1] means the x-axis
    c = 0
    leftHand = thresh1.shape[0]
    rightHand = 0
    bottomHand = thresh1.shape[1]
    while(c < thresh1.shape[0]):
        r = 0
        while(r < thresh1.shape[1]):     
            if thresh1[c][r] != 255:
                if r < leftHand:
                    leftHand = r
                if r > rightHand:
                    rightHand = r
                # cv2.circle(frame, (int(r), int(c)), 5, [0, 255, 255], 10) #amarillo
            r += 1
        c += 1

    # center of the hand
    optimalAvg = (leftHand+rightHand)/2

    # Width of the image
    x0Real = optimalAvg-int((thresh1.shape[0])/2)+1 # Left
    x1Real = optimalAvg+int((thresh1.shape[0])/2)-1 # Right

    # print("average ", optimalAvg)
    # print("min ", x0Real)
    # print("max ", x1Real)

    # cv2.circle(frame, (int(optimalAvg), int(endHand/2)), 5, [0, 255, 255], 10) #amarillo

    if x0Real < 0:
        x0Real = 0
        x1Real = frame.shape[0] -1 
        print("la mano termina en ", x1Real)
    if x1Real > frame.shape[1]-1:
        x1Real = frame.shape[1]-1
        x0Real = frame.shape[1] - frame.shape[0]
        if x0Real < 0:
            x0Real = 0
            x1Real = frame.shape[0]-1
            print("x es menor que cero", x1Real)
        print("la mano comienza en ", x0Real)

    return frame[0:frame.shape[0]-1, int(x0Real):int(x1Real)]

def cropHand(frame): 

    # Converting image to black and white
    grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    _, thresh1 = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    thresh1 = cv2.erode(thresh1, None, iterations=2)
    thresh1 = cv2.dilate(thresh1, None, iterations=2)

    cv2.imshow("thresh1", thresh1)

    c = 0
    leftHand = thresh1.shape[1]
    rightHand = 0
    bottomHand = thresh1.shape[1]
    topHand = thresh1.shape[0]
    while(c < thresh1.shape[0]):
        r = 0
        while(r < thresh1.shape[1]):     
            if thresh1[c][r] != 255:
                if c < topHand:
                    topHand = c
                if r < leftHand:
                    leftHand = r
                if r > rightHand:
                    rightHand = r
            r += 1
        c += 1

    topHand -= 7
    if topHand < 0:
        topHand = 0

    leftHand -= 7
    if leftHand < 0:
        leftHand = 0

    rightHand += 7
    if leftHand > thresh1.shape[1]:
        leftHand = thresh1.shape[1]

    # Width of the image
    return frame[topHand:frame.shape[0], int(leftHand):int(rightHand)]
    # return frame

def mergeImage(frame, width, height):
 
    print("Original", frame.shape)

    # Adjusting size
    if frame.shape[0] > height:
        hy = height/frame.shape[0]
        hx = frame.shape[1]*hy
        frame = cv2.resize(frame, (int(hx), int(height)), interpolation = cv2.INTER_CUBIC)
        print("Change y", frame.shape)
    if frame.shape[1] > width:
        hx = width/frame.shape[1]
        hy = frame.shape[0]*hx
        frame = cv2.resize(frame, (int(width), int(hy)), interpolation = cv2.INTER_CUBIC)
        print("Change x", frame.shape)
    
    # Mask
    merge = np.zeros((int(width), int(height), 3))
    # Make white mask
    # merge.fill(255)
    # cv2.imshow("merge", merge)
    
    # Putting the image in the middle
    x_offset = (width - frame.shape[1])/2
    y_offset = (height - frame.shape[0])/2


    # Random positions
    # x_offset = width - frame.shape[1]
    # y0 = random.randint(0, int(y_offset))
    # x0 = random.randint(0, int(x_offset))
    
    # merge[int(y_offset):int(y_offset+frame.shape[0]), int(x_offset):int(x_offset+frame.shape[1])] = frame
    # Merge
    merge[:,:, 0][int(y_offset):int(y_offset+frame.shape[0]), int(x_offset):int(x_offset+frame.shape[1])] = frame
    merge[:,:, 1][int(y_offset):int(y_offset+frame.shape[0]), int(x_offset):int(x_offset+frame.shape[1])] = frame
    merge[:,:, 2][int(y_offset):int(y_offset+frame.shape[0]), int(x_offset):int(x_offset+frame.shape[1])] = frame
    # Random merge
    # merge[int(y0):int(y0+frame.shape[0]), int(x0):int(x0+frame.shape[1])] = frame

    return merge

def forceSize(frame, height):
    # Adjusting size
    if frame.shape[0] > frame.shape[1]:
        if frame.shape[0] is not height:
            hy = height / frame.shape[0]
            hx = frame.shape[1] * (hy)
            frame = cv2.resize(frame, (int(hx), int(height)), interpolation = cv2.INTER_CUBIC)
            print("Change y", frame.shape)
    else:
        if frame.shape[1] is not height:
            hy = height / frame.shape[1]
            hx = frame.shape[0] * (hy)
            frame = cv2.resize(frame, (int(height), int(hx)), interpolation = cv2.INTER_CUBIC)
            print("Change y", frame.shape)
        
    return frame

def normalize(mean, std, isLower):
    if isLower:
         if mean-std < 0:
            return 0

    if mean+std > 255:
        return 255 

def getAverageColors(frame, roiPts):  
    lower_bounds = []
    upper_bounds = []

    for roi in roiPts:
        # Dimensiones de cuadro en la pantalla
        xmin = int((roi[0]))
        ymin = int((roi[1]))
        xmax = int((xmin + frame.shape[1]*setup.diamRoi))
        ymax = int((ymin + frame.shape[0]*setup.diamRoi))

        # Image del cuadro en la pantalla
        # No es necesario ordenarlo
        color1 = np.sort(frame[ymin:ymax, xmin:xmax, 0].reshape(-1), kind = "mergesort")
        color2 = np.sort(frame[ymin:ymax, xmin:xmax, 1].reshape(-1), kind = "mergesort")
        color3 = np.sort(frame[ymin:ymax, xmin:xmax, 2].reshape(-1), kind = "mergesort")

        meanColor1 = np.mean(color1)
        meanColor2 = np.mean(color2)
        meanColor3 = np.mean(color3)

        stdcolor1 = np.std(color1)
        stdcolor2 = np.std(color2)
        stdcolor3 = np.std(color3)

        lower_bounds.append([int(meanColor1-(stdcolor1)), int(meanColor2-(stdcolor2)), int(meanColor3-(stdcolor3))])
        upper_bounds.append([int(meanColor1+(stdcolor1)), int(meanColor2+(stdcolor2)), int(meanColor3+(stdcolor3))])

    return (lower_bounds, upper_bounds)

def mergeColorsImage(frame, lowerBound, upperBound):
    output = cv2.inRange(frame, lowerBound[0][0], upperBound[0][0])
    for i in range(1, len(lowerBound)):
        for j in range(1, len(lowerBound[0])):
            output += cv2.inRange(frame, lowerBound[i][j], upperBound[i][j])
    return output

def drawRectangle(frame, roiPts):
    i = 0
    cantPoint = setup.cantPoint
    yRoi = int(frame.shape[0]*setup.diamRoi)
    xRoi = int(frame.shape[1]*setup.diamRoi)

    font = cv2.FONT_HERSHEY_SIMPLEX
    if len(roiPts) > len(roiPts)-1:
        # Poner texto en la pantalla
        cv2.putText(frame, 'Press D',(int(frame.shape[1]*setup.wdTxt), int(frame.shape[0]*setup.hiTxt)), setup.font, setup.sizThk,(0,255,0),3)
        # Colocar los cuadros en la pantalla para captua de colores
        while(i < len(roiPts)):
            xmax = roiPts[i][0] + xRoi
            ymax = roiPts[i][1] + yRoi
            cv2.rectangle(frame, roiPts[i], (int(xmax), int(ymax)), (0,255,0),2)
            i += 1

    return frame

def findBiggestContour(contours):
    indexOfBiggestContour = 1
    sizeOfBiggestContour = 0
    i = 0
    while i < len(contours):
        if len(contours[i]) > sizeOfBiggestContour:
            sizeOfBiggestContour = len(contours[i])
            indexOfBiggestContour = i
        i += 1

    return indexOfBiggestContour

def findHighContour(contours, frameWB):
    indexOfHighContour = 1
    i = 0
    yMax = frameWB.shape[0]
    while i < len(contours):
        (x,y,w,h) = cv2.boundingRect(contours[i])
        if yMax > y:
          yMax = y
          indexOfHighContour = i
        i += 1

    return indexOfHighContour



########################IMPORTANTE#########################################
# Video
# # cascPath = "C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\dasar_haartrain\\myhaar2.xml"
# cascPath = "C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\handDetection\\hand.xml"
# cap = cv2.VideoCapture(0)
# while(cap.isOpened()):
#     # read image
#     ret, img = cap.read()
#     faceCascade = cv2.CascadeClassifier(cascPath)
#     edges = cv2.Canny(img, 100, 255)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.equalizeHist(gray)
#     # Detect faces in the image
#     faces = faceCascade.detectMultiScale(
#       gray,
#       scaleFactor=1.1,
#       minNeighbors=3,
#       minSize=(5, 5),
#       flags = 0
#   )
    
#     extXY = 30
#     extWH = 30
#   # Draw a rectangle around the faces
#     for (x, y, w, h) in faces:
#         if y-extXY < 0 or x-extXY < 0:
#             extXY = 0

#         crop = img[y-extXY:y+h+extWH, x-extXY:x+w+extWH]
#         #cv2.imwrite(str(i)+'.png', crop)
#         #cv2.imshow("Crop found", crop)
#         #cv2.waitKey(0)
#         cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         break

#     cv2.imshow("images", img)
#     k = cv2.waitKey(10)
#     if k == 27:
#       break

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
