import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:\\Users\\Juan Graciano\\Desktop\\HandComp\\dataset\\veremoNati'
save_path =  'C:\\Users\\Juan Graciano\\Desktop\\HandComp\\dataset\\veremoNati\\mergeTest'


classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
test = ['testCanny']
classes = classesNum


frame = None
# roiPts = [(205, 159),(346, 162),(347, 254),(230, 270)]
roiPts = []
inputMode = True

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

        xmax = x + frame.shape[1]*0.5
        ymin = y - frame.shape[0]*0.55

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
            # frame = tools.resize(frame, 400, 400)
            
            # if inputMode is not False:
            #     y0 = roiPts[3][1]
            #     y1 = roiPts[0][1]
            #     x0 = roiPts[0][0]
            #     x1 = roiPts[3][0]
            #     # frame = tools.CropHand(frame)
            #     frame = frame[int(y0):int(y1), int(x0):int(x1)]

            # Crop Tape
            # frame = tools.detectTape(frame)

            # Crop Hand
            # frame = tools.cropHand(frame)

            # Canny
            # frame = cv2.Canny(frame, 127, 255)

            # force
            # frame = tools.forceSize(frame, 334)
            
            # Merge
            # frame = tools.mergeImage(frame, 334, 334)

           

            cv2.imshow("frame", frame)

            if inputMode is False:
                k = ord("i")
            else:
                tools.saveImage(name, frame.copy(), save_path, fld, 'm')
                k = cv2.waitKey(1)

            if k == ord("i"):
                inputMode = True
                orig = frame.copy()

                while len(roiPts) < 4:
                    cv2.imshow("frame", frame)
                    cv2.waitKey(0)
                    
            elif k == ord("q"):
                break

        # if k == ord("q"):
        #     break

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
        
        if inputMode is not False:
            y0 = roiPts[3][1]
            y1 = roiPts[0][1]
            x0 = roiPts[0][0]
            x1 = roiPts[3][0]
            # frame = tools.detectTape(frame[y0:y1, x0:x1])
            frame = cv2.Canny(frame[y0:y1, x0:x1], 100, 255)

        cv2.imshow("frame", frame)

        if inputMode is False:
            k = ord("i")
        else:
            # tools.saveImage(name, frame.copy(), save_path, fld, 'tape')
            k = cv2.waitKey(0)

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

readFolder()
