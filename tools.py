import os
import math
import cv2
import numpy as np
import argparse


def resize(img, w, h):
    return cv2.resize(img, (w, h), interpolation = cv2.INTER_CUBIC)

def createFolder(letra, save_path):
    if not os.path.exists(save_path + '\\' + letra):
        os.makedirs(save_path + '\\' + letra)
        print('Folder "', letra, '"created')

def saveImage(name, img, save_path, letra, alias):
    createFolder(letra, save_path)

    name = name.split('.')
    print(save_path + '\\' + letra + '\\' + name[0] + '-'+alias+'.png')
    cv2.imwrite(save_path + '\\' + letra + '\\' + name[0] + '-'+alias+'.png', img)

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
    rows,cols = frame.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),grade,1)
    dst = cv2.warpAffine(frame,M,(cols,rows))
    return dst

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
    print(s)
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
    while(c < thresh1.shape[0]):
        r = 0
        while(r < thresh1.shape[1]):
            if thresh1[c][r] != 255:
                if r < vmin:
                    vmin = r
                if r > vmax:
                    vmax = r
                suma += r
                cantElem += 1
            r += 1
        c += 1

    optimalAvg = (vmin+vmax)/2

    # ----------------------------------------^------------------------------------------------

    # ----------------------------------------v------------------------------------------------
    
    xmin = 0
    xmax = frame.shape[0]
    xminMid = 0
    xmaxMid = frame.shape[0]
    i = 0
    # Look for the center of the wrist
    # while(i < thresh1.shape[0]):
    #     if xmin == 0:
    #         if thresh1[thresh1.shape[0]-1][i] != 255:
    #             xmin = i
    #     elif xmax == frame.shape[0]:
    #         if thresh1[thresh1.shape[0]-1][i] == 255:
    #             xmax = i
    #     if xminMid == 0:
    #         if thresh1[int(thresh1.shape[0]/1.5)][i] != 255:
    #             xminMid = i
    #     elif xmaxMid == frame.shape[0]:
    #         if thresh1[int(thresh1.shape[0]/1.5)][i] == 255:
    #             xmaxMid = i
    #     i += 1

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

    x0Real = optimalAvg-int(frame.shape[0]/2)+1
    x1Real = optimalAvg+int(frame.shape[0]/2)-1

    if x0Real >= 0 and x1Real <= frame.shape[1]:
        # cv2.rectangle(frame, (int(x0Real), 0), (int(x1Real), frame.shape[0]-1), (255, 0, 0), 3)
        cv2.imshow("Real", frame[0:frame.shape[1]-1, int(x0Real):int(x1Real)])
    else:
        if x0Real < 0:
            x0Real = 0
            x1Real = frame.shape[0]
        if x1Real > frame.shape[1]-1:
            x1Real = frame.shape[1]-1
            x0Real = frame.shape[1] - frame.shape[0]
    
    # ----------------------------------------^------------------------------------------------

    cv2.imshow("thresh1", thresh1)

    # x-int(h/5.5), y-int(y/20), x+h-int(h/3.5), y+h
    return frame[0:frame.shape[0]-1, int(x0Real):int(x1Real)]

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
