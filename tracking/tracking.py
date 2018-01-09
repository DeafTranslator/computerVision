import numpy as np
import cv2
import os
import glob
# import imutils
import tools

num = '8'
numl = 'ocho'
# letra = 'y'

# train_path = 'C:\\Users\\Juan
# Graciano\\Desktop\\Proyecto\\Dataset\\datasetNumero\\Numero\\'+num+'-'+numl+'\\'+num+'\\New
# folder'
train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\Dataset\\datasetNumero\\Numero\\' + \
    num + '-' + numl + '\\' + num + '\\finalTest'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\tools\\FotoseRacista'
train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\tools\\nuewas'
classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def readPhothoClasse():
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(train_path, fld, '*g')
        files = glob.glob(path)
        for fl in files:
            frame = cv2.imread(fl)
            name = os.path.basename(fl)
            img = tools.changeSize(frame.copy(), 400, 600)
            edge = cv2.Canny(img, 100, 255)

            cv2.imshow('out',edge)
            cv2.waitKey(0)
    # tools.saveImage(name, edge, fld, save_path)

    print('Eta vaina termino')

def readPhotho():
    print('Reading image')
    path = os.path.join(train_path, '*g')
    files = glob.glob(path)
    for fl in files:
        frame = cv2.imread(fl)
        name = os.path.basename(fl)
        img = tools.changeSize(frame.copy(), 400, 600)
        edge = cv2.Canny(img, 100, 255)

        cv2.imshow('out',edge)
        cv2.waitKey(0)
    # tools.saveImage(name, edge, fld, save_path)

    print('Eta vaina termino')


frame = None
# roiPts = [(205, 159),(346, 162),(347, 254),(230, 270)]
roiPts = []
inputMode = False

cantPts = 0

def selectROI(event, x, y, flags, param):
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode
    print("holaa")
    # if we are in ROI selection mode, the mouse was clicked,
    # and we do not already have four points, then update the
    # list of ROI points with the (x, y) location of the click
    # and draw the circle
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
        roiPts.append((x, y))
        print("x: ", x)
        print("y: ", y)
        cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
        cv2.imshow("frame", frame)


def readVideo():
    cap = cv2.VideoCapture(0)
    entra = False
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)
    global frame, roiPts, inputMode
    roiBox =  None
    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    while(cap.isOpened()):
        ret, frame = cap.read()

        # track_window, term_crit, roi_hist = tools.dimensions(frame.copy())
        # if len(roiPts) >= 4:

        if roiBox is not None:
            frame = tools.trackHand(ret, frame, roiBox, roiHist, termination)

        # edge = cv2.Canny(frame.copy(), 100, 255)
        
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xFF
        # if k == ord("i") and len(roiPts) < 4:
        if k == ord("i"):
            inputMode = True
            orig = frame.copy()

            while len(roiPts) < 4:
                cv2.imshow("frame", frame)
                cv2.waitKey(0)

            # determine the top-left and bottom-right points
            print(roiPts)
            roiPts = np.array(roiPts)
            s = roiPts.sum(axis = 1)
            print(s)
            tl = roiPts[np.argmin(s)]
            br = roiPts[np.argmax(s)]
            print(tl)
            print(br)
            print(roiPts)

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
            

        elif k == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()







readVideo()

