import cv2
import os
import glob
import tools
import numpy as np

# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\tools\\FOtose'
# save_path =  'C:\\Users\\Juan Graciano\\Desktop\\prueva'

train_path = 'C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\alpha'
save_path =  'C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\nuevaPrueba'


classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
# test = ['testCanny']
# classesAlph = ['r','s','t','u','v','w','x','y','z']
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

        xmax = x + frame.shape[1]*0.3
        ymin = y + frame.shape[0]*0.4

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


def drawContour(frame):
        grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        value = (15, 15)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(grey,5,255, 8)
        image, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        height, width, _ = frame.shape
        min_x, min_y = width, height
        max_x = max_y = 0

        # computes the bounding box for the contour, and draws it on the frame,
        contando = 0 
        saved = []
        for contour in contours:
            (x,y,w,h) = cv2.boundingRect(contour)
            min_x, max_x = min(x, min_x), max(x+w, max_x)
            min_y, max_y = min(y, min_y), max(y+h, max_y)
            # print((x,y,w,h))
            if w > 70 and h > 70:
                # cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)
                masr = 40
                masb = 30
                menot = 30
                menol = 10
                if y - menot <= 0 :
                    menot = -1
                if x - menol <= 0:
                    menol = -1
                if y+h + masb >= frame.shape[0] :
                    masb = 0
                if x+w + masr >= frame.shape[1]:
                    masr = 0

                saved = frame[int(y-menot):int(y+h+masb), int(x-menol):int(x+w+masr)]
                # tools.saveImage(name +'-'+str(contando), saved.copy(), save_path, fld, 'ct')
                contando += 1
                # cv2.imshow("contorno", frame[int(y-menot):int(y+h+masb), int(x-menol):int(x+w+masr)])
                # cv2.waitKey(0)
                # break

        # if max_x - min_x > 0 and max_y - min_y > 0:
        #     # cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
        #     saved = frame[int(min_y):int(max_y), int(min_x):int(max_x)]
        #     cv2.imshow("especial", saved)
        #     # tools.saveImage(name + "es", saved.copy(), save_path, fld, 'ct')
        
        # cv2.imshow("cnt", frame)
        return saved

k = 0
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()
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
            # grayOrigi = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            # # fgmask = fgbg.apply(frame)
            # # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            # hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)
            
            # # maskara = cv2.zeros()
            # # clon = hsv.copy()
            # hsv[:,:,0] = 100
            # hsv[:,:,1] = 100
            # # img = cv2.merge((clon, 3, hsv))
            # # print(img[0])

            # bgr = cv2.cvtColor(hsv.copy(), cv2.COLOR_HSV2BGR)

            # gray = cv2.cvtColor(bgr.copy(), cv2.COLOR_BGR2GRAY)
            # gray = cv2.medianBlur(gray.copy(),3)
            # print(gray.shape)
            # linea150 = gray[:,75]
            # print(linea150)
            # _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
            # # _, thresh1 = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
            # print(thresh1.shape)
            # yuv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2YUV)
            
            # # _, thresh2 = cv2.threshold(grayYuv, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
            # (b,g,r) = cv2.split(yuv.copy())
            # # print(len(b))
            # equ = cv2.equalizeHist(gray)
            # img = cv2.merge((equ, g, r))
            # grayYuv = cv2.cvtColor(img.copy(), cv2.COLOR_YUV2BGR)
            # # img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
            # # # force
            # # frame = tools.forceSize(frame, 334)
            # # out = frame
            # # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # # blurFrame = cv2.medianBlur(frame.copy(),7)
            # # fdifetente = cv2.threshold(frame,10,255,cv2.THRESH_BINARY_INV)
            # # print(fdifetente[1].shape)
            # # # cv2.imshow("fdifetente", fdifetente[1])
            # f11 = cv2.Canny(grayOrigi, 170, 190, L2gradient=True)
            # # f11 = cv2.cornerHarris(grayOrigi,2,3,0.04)
            # # f11 = cv2.dilate(f11,None)
            # # print(f11.shape)
            # # cv2.imshow("f11", f11)
            # # out = fdifetente[1] + f11
            # out = thresh1 + f11
            # cv2.imshow("origial", out)
            # cv2.imshow("gray", equ)
            # cv2.imshow("hsv", hsv)
            # cv2.imshow("canny", f11)
            # print("antes", out.shape)
            # out[:,:,0] = fdifetente[1] + f11
            # out[:,:,1] = fdifetente[1] + f11
            # out[:,:,2] = fdifetente[1] + f11
            # cv2.imshow("frames", out)
            # cv2.waitKey(0)

            # frame = tools.resize(frame,393, 700)
            
            if inputMode is not False:
                y0 = roiPts[3][1]
                y1 = roiPts[0][1]
                x0 = roiPts[0][0]
                x1 = roiPts[3][0]
                # frame = tools.CropHand(frame)
                # frame = frame[int(y1):int(y0), int(x0):int(x1)]

            # Crop Tape
            # print(len(frame))
            # frame = drawContour(frame)
            # Crop Hand
            # frame = tools.cropHand(frame)

            # Canny
            # frame = cv2.Canny(frame, 127, 255)

            # Merge
            # frame = tools.mergeImage(out, 334, 334)
            # lista = [1]
            # v = 0
            # print(type(frame))
            # h = type(lista)
            # print(h)
            # if type(frame) is np.ndarray:
            #     v = 1
            # print(v)
            if len(frame) is not 0:
                cv2.imshow("frame", frame)
            if inputMode is False:
                k = ord("i")
            else:
                if len(frame) is not 0:
                    # tools.saveImage(name, grayOrigi.copy(), save_path, fld, 'jesu')
                    k = cv2.waitKey(0)

            if len(frame) is not 0 and k == ord("i"):
                inputMode = True
                orig = frame.copy()

                while len(roiPts) < 4:
                    cv2.imshow("frame", frame)
                    cv2.waitKey(0)
                    
            elif len(frame) is not 0 and k == ord("q"):
                break

        if len(frame) is not 0 and k == ord("q"):
            break

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
            # frame = cv2.Canny(frame[y0:y1, x0:x1], 100, 255)

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
