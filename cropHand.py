import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\29-10-2017\\Mirta\\simpleCrop'
save_path =  'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\29-10-2017\\Mirta\\cropHand'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classRemaining = ['x']
classesAll = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['nombre']
classes = ['q']

frame = None
def drawContour(frame):

        grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        value = (25, 25)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred,70,255, cv2.THRESH_BINARY)
        # _, thresh1 = cv2.threshold(blurred,150,255, 12)
        image, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        height, width, _ = frame.shape
        min_x, min_y = width, height
        max_x = max_y = 0

        # computes the bounding box for the contour, and draws it on the frame,
        xs = 0
        ys = thresh1.shape[0]
        ws = 0
        hs = 0

        xs2 = 0
        ys2 = thresh1.shape[0]
        ws2 = 0
        hs2 = 0

        print("cantidad", len(contours))
        frame2 = blurred.copy()

        if len(contours) is not 0:
            a1Idx = tools.findBiggestContour(contours)

            cnt1 = contours[a1Idx]
            cv2.drawContours(frame2, [cnt1], 0, (0,255,0), 3)
            (xs,ys,ws,hs) = cv2.boundingRect(cnt1)

            contours.pop(a1Idx)

        if len(contours) is not 0: 
            a2Idx = tools.findBiggestContour(contours)
            cnt2 = contours[a2Idx]
            cv2.drawContours(frame2, [cnt2], 0, (0,255,255), 3)
            (xs2,ys2,ws2,hs2) = cv2.boundingRect(cnt2)

        cv2.imshow('frame2', frame2)
        cv2.imshow('thresh1', thresh1)

        masr = 20
        masb = 25
        menot = 10
        menol = 10
        if ys - menot <= 0 :
            menot = 0
        if xs - menol <= 0:
            menol = 0
        if ys+hs + masb >= frame.shape[0] :
            masb = frame.shape[0] - (ys+hs)
            # masb = 0
        if xs+ws + masr >= frame.shape[1]:
            masr = frame.shape[1] - (xs+ws)


        hand1 = frame[int(ys-menot):int(ys+hs+masb), int(xs-menol):int(xs+ws+masr)]
        # cv2.imshow("contorno1", hand1)

        masr2 = 10
        masb2 = 10
        menot2 = 10
        menol2 = 10
        if ys2 - menot2 <= 0 :
            menot2 = 0
        if xs2 - menol2 <= 0:
            menol2 = 0
        if ys2+hs2 + masb2 >= frame.shape[0] :
            masb2 = frame.shape[0] - (ys2+hs2)
            # masb2 = 0
        if xs2+ws2 + masr2 >= frame.shape[1]:
            masr2 = frame.shape[1] - (xs2+ws2)

        hand2 = frame[int(ys2-menot2):int(ys2+hs2+masb2), int(xs2-menol2):int(xs2+ws2+masr2)]

        # Merge image
        heightMerge = max(hand2.shape[0],hand1.shape[0])
        widthMerge = hand2.shape[1]+hand1.shape[1]+1
        merge = np.zeros((int(heightMerge), int(widthMerge), 3))

        # if xs < xs2:
        #     # for channel in range(1,3):
        #     merge[int(heightMerge-(hs+masb+menot)):int(heightMerge), 0:int(ws+menol+masr)] = hand1
        #     merge[int(heightMerge-(hs2+masb2+menot2)):int(heightMerge), int(ws+menol+masr)+1:int(widthMerge)]=hand2
        # else:
        #     # for channel in range(1,3):
        #     merge[int(heightMerge-(hs2+masb2+menot2)):int(heightMerge), 0:int(ws2+menol2+masr2)] = hand2
        #     merge[int(heightMerge-(hs+masb+menot)):int(heightMerge), int(ws2+menol2+masr2)+1:int(widthMerge)] = hand1

        # cv2.imshow("contorno2", hand2)
        # cv2.imshow("merge", merge)

        # cv2.waitKey(0)
        return merge, hand1, hand2

k = 0
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()
def readFolder():
    global frame
    cv2.namedWindow("frame")
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(train_path, fld,'*g')
        files = glob.glob(path)

        for fl in files:
            frame = cv2.imread(fl)
            name = os.path.basename(fl)

            # Crop Tape
            # cv2.imshow("frame", frame)
            frame, hand1, hand2 = drawContour(frame)
            
            if type(frame) is np.ndarray:
                cv2.imshow("frame", hand1)
                # tools.saveImage(name, frame.copy(), save_path, fld, 'ch')
                tools.saveImage(name, hand1.copy(), save_path, fld, 'ch')
                # tools.saveImage(name, hand2.copy(), save_path, fld, 'ch'+'_s2')
            k = cv2.waitKey(1)
                    
            if k == ord("q"):
                break

        if k == ord("q"):
            break

readFolder()
