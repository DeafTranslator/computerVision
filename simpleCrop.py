import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\2-11-2017\\Jesus'
save_path =  'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\2-11-2017\\Jesus\\simpleCrop'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['nombre']
classes = classesDinamic

frame = None
roiPts = []
inputMode = False

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
        print("x: ", x)
        print("y: ", y)

        xmax = x + min(frame.shape[1], frame.shape[1]*1)
        ymin = y + min(frame.shape[0], frame.shape[0]*0.75)

        print("xmax: ", xmax)
        print("ymin: ", ymin)
        cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
        cv2.circle(frame, (int(xmax), y), 4, (0, 255, 0), 2)
        cv2.circle(frame, (x, int(ymin)), 4, (0, 255, 0), 2)
        cv2.circle(frame, (int(xmax), int(ymin)), 4, (0, 255, 0), 2)
        roiPts.append((int(xmax), y))
        roiPts.append((x, int(ymin)))
        roiPts.append((int(xmax), int(ymin)))
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
            # frame = tools.resize(frame, 393, 700)
            if inputMode is not False:
                y0 = roiPts[3][1]
                y1 = roiPts[0][1]
                x0 = roiPts[0][0]
                x1 = roiPts[3][0]
                frame = frame[int(y1):int(y0), int(x0):int(x1)]

            cv2.imshow("frame", frame)
            if inputMode is False:
                k = ord("i")
            else:
                tools.saveImage(name, frame.copy(), save_path, fld, '')
                k = cv2.waitKey(1)

            if k == ord("i"):
                inputMode = True
                orig = frame.copy()

                while len(roiPts) < 4:
                    cv2.imshow("frame", frame)
                    cv2.waitKey(0)
                    
            elif k == ord("q"):
                break

        if k == ord("q"):
            break

readFolder()
