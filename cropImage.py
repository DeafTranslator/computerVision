import cv2
import os
import glob
import tools
import numpy as np

num = '0'
numl = 'nueve'

letra = 'y'

# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\Dataset\\datasetNumero\\Numero\\'+num+'-'+numl+'\\'+num+'\\New folder'
train_path ='C:\\Users\\Juan Graciano\\Desktop\\Nati videos\\jesu\\letra'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\Nati videos\\jesu\\letra\\letraJesus'
# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Photos8-7-2017\\' + letra
classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# classesAlph = ['c','g','m','n','o','p','q','u','v','x','y']
# classesAlph = ['a','b','c','d','e','f','g','h','i','k','m','n','o','p','q','r','s','t','u','v','w','x','y']
classesNum = ['0','1','2','3','4','5','6','7','8','9']

classes = classesAlph


frame = None
# roiPts = [(205, 159),(346, 162),(347, 254),(230, 270)]
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
        xmax = x*1.82
        ymin = y-(y*0.62)
        print("x+400: ", xmax)
        print("y-400: ", ymin)
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
            frame = tools.resize(frame, 711, 400)
            # gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            # img = frame.copy()
            # aux = frame.copy()

            # nueva = orb(gray, frame)
            # nueva, x, y, w, h = circlePoint(img)
            # nueva = circlePoint(img)
            
            if inputMode is not False:
                y0 = roiPts[3][1]
                y1 = roiPts[0][1]
                x0 = roiPts[0][0]
                x1 = roiPts[3][0]
                # cv2.rectangle(frame, (roiPts[0][0], roiPts[3][1]), (roiPts[3][0], roiPts[0][1]), (0, 0, 255), 2)
                # cv2.rectangle(frame, (int(x0), int(y0)), (int(x1), int(y1)), (0, 0, 255), 2)
                frame = tools.circlePoint(frame[int(y0):int(y1), int(x0):int(x1)])
            

            cv2.imshow("frame", frame)

            if inputMode is False:
                k = ord("i")
            else:
                tools.saveImage(name, frame.copy(), save_path, fld, 'crop')
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
    print('Reading images')
    path = os.path.join(train_path, '*g')
    files = glob.glob(path)
    for fl in files:
        frame = cv2.imread(fl)
        name = os.path.basename(fl)
        # frame = resize(frame, 400, 600)
        gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        img = frame.copy()
        aux = frame.copy()

        # nueva = orb(gray, frame)
        nueva, x, y, w, h = circlePoint(img)
        # nueva = circlePoint(img)

        corte = cropImage2(nueva, x, y, w, h)
        # cv2.imshow("nuevas", corte)

        saveImage(name, corte)

        # cv2.waitKey(0)
        # k += 1
        # if k > 100:
        #     break

    print('Terminamo')

readFolder()
