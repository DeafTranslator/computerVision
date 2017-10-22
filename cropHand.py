import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\20-10-2017\\Samuel\\simpleCrop'
save_path =  'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\20-10-2017\\Samuel\\cropHand'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classRemaining = ['g', 'h', 'p', 'q']
classes = classRemaining

frame = None
def drawContour(frame):
    
        # HSV = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)
        # HSV[-75,:,:]



        grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        value = (15, 15)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(grey,50,255, 8)
        # _, thresh1 = cv2.threshold(blurred,150,255, 12)
        image, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        height, width, _ = frame.shape
        min_x, min_y = width, height
        max_x = max_y = 0

        # print("cantidad", len(contours))
        cIdx = tools.findBiggestContour(contours)
        # print("el mas grande",cIdx)

        frame2 = blurred.copy()
        cnt = contours[cIdx]
        cv2.drawContours(frame2, [cnt], 0, (0,255,0), 3)
        # thresh1 = cv2.GaussianBlur(thresh1, value, 0)
        cv2.imshow('frame2', frame2)
        cv2.imshow('thresh1', thresh1)

        # computes the bounding box for the contour, and draws it on the frame,
        contando = 0 
        saved = []
        xs = 0
        ys = thresh1.shape[0]
        ws = 0
        hs = 0
        for contour in contours:
            (x,y,w,h) = cv2.boundingRect(contour)
            min_x, max_x = min(x, min_x), max(x+w, max_x)
            min_y, max_y = min(y, min_y), max(y+h, max_y)

            # print("x", x)
            # print("y", y)
            # print("w", w)
            # print("h", h)
            # print('------------------')

            if y < ys:
                xs = x
                ys = y
                ws = w
                hs = h

            
            # if w > 40 and h > 40:
            #     # cv2.rectangle(frame2, (x,y), (x+w,y+h), (255, 0, 0), 2)
            #     masr = 15
            #     masb = 15
            #     menot = 15
            #     menol = 15
            #     if y - menot <= 0 :
            #         menot = -1
            #     if x - menol <= 0:
            #         menol = -1
            #     if y+h + masb >= frame.shape[0] :
            #         masb = frame.shape[0] - (y+h)
            #         # masb = 0
            #     if x+w + masr >= frame.shape[1]:
            #         masr = frame.shape[1] - (x+w)

            #     saved = frame[int(y-menot):int(y+h+masb), int(x-menol):int(x+w+masr)]
            #     # tools.saveImage(name +'-'+str(contando), saved.copy(), save_path, fld, 'ct')
            #     contando += 1
            #     cv2.imshow("contorno", saved)
            #     cv2.waitKey(0)
                # break


        masr = 15
        masb = 30
        menot = 15
        menol = 15
        if ys - menot <= 0 :
            menot = -1
        if xs - menol <= 0:
            menol = -1
        if ys+hs + masb >= frame.shape[0] :
            masb = frame.shape[0] - (ys+hs)
            # masb = 0
        if xs+ws + masr >= frame.shape[1]:
            masr = frame.shape[1] - (xs+ws)

        saved = frame[int(ys-menot):int(ys+hs+masb), int(xs-menol):int(xs+ws+masr)]
        # tools.saveImage(name +'-'+str(contando), saved.copy(), save_path, fld, 'ct')
        contando += 1
        cv2.imshow("contorno", saved)
        # cv2.waitKey(0)

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
            cv2.imshow("frame", frame)
            frame = drawContour(frame)
            
            if type(frame) is np.ndarray:
                cv2.imshow("frame", frame)
                tools.saveImage(name, frame.copy(), save_path, fld, 'ch')
            k = cv2.waitKey(1)
                    
            if k == ord("q"):
                break

        if k == ord("q"):
            break

readFolder()
