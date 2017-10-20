import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\alpha_newSCrop\\selectwithFlip'
save_path =  'C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\alpha_newSCrop\\selectwithFlip\\cropHand'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classes = classesAlph

frame = None
def drawContour(frame):
        grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        value = (55, 55)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred,5,255, 8)
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

            frame2 = frame.copy()
            if w > 80 and h > 80:
                # cv2.rectangle(frame2, (x,y), (x+w,y+h), (255, 0, 0), 2)
                masr = 40
                masb = 25
                menot = 30
                menol = 10
                if y - menot <= 0 :
                    menot = -1
                if x - menol <= 0:
                    menol = -1
                if y+h + masb >= frame.shape[0] :
                    masb = frame.shape[0] - (y+h)
                    # masb = 0
                if x+w + masr >= frame.shape[1]:
                    masr = frame.shape[1] - (x+w)

                saved = frame[int(y-menot):int(y+h+masb), int(x-menol):int(x+w+masr)]
                # tools.saveImage(name +'-'+str(contando), saved.copy(), save_path, fld, 'ct')
                contando += 1
                cv2.imshow("contorno", frame2)
                # cv2.waitKey(0)
                break

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

            # frame = tools.resize(frame,393, 700)
            
            # Crop Tape
            # print(len(frame))
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
