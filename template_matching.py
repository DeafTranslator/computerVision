import cv2
import os
import glob
import tools
import numpy as np


video_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\videos\\29-10-2017\\Andreina'
save_path =  'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\2-11-2017\\Jesus'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['0']
classes = classesDinamic

frame = None

k = 0

def drawContour(frame):

        grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        value = (25, 25)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred,99,255, cv2.THRESH_BINARY)
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

        # print("cantidad", len(contours))
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

        # cv2.imshow('frame2', frame2)
        # cv2.imshow('thresh1', thresh1)

        masr = 20
        masb = 20
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

        return merge, hand1, hand2


def readVideo(video, fld):
    global frame
    cap = cv2.VideoCapture(video) 
    i = 0
    newTemplate = False
    while( cap.isOpened() ) :
        ret,frame = cap.read()

        if ret is not True:
            break
        
        rotated = tools.rotate_bound(frame, 90)
        image = rotated.copy()
        # rotated = tools.resize(rotated, 450, 700)
        if i % 2:
            # cv2.imshow("frame", rotated)
            img_gray = cv2.cvtColor(rotated.copy(), cv2.COLOR_BGR2GRAY)
            if newTemplate is False:
                template = cv2.imread('C:/Users/jgraciano/Desktop/TeEnsenia/computerVision/nombre/initHands.png')
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('template',template) cv2.waitKey(0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            threshold = 0.70
            loc = np.where( res >= threshold)

            found = None

            for pt in zip(*loc[::-1]):

                template2 = rotated.copy()[pt[1]:(pt[1] + h+30), pt[0]:(pt[0] + w+30)]

                cv2.rectangle(rotated, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)                

                # Clean image
                frames, template2, hand2 = drawContour(template2)
                
                # Update template
                if type(template) is np.ndarray:
                    newTemplate = True
                    template = cv2.cvtColor(template2, cv2.COLOR_BGR2GRAY)
                    print("despues", template.shape)
                break

            cv2.imshow('Detected',rotated)
            cv2.imshow('template',template)
            cv2.waitKey(1)
            name = fld + '_' + str(i)
            # tools.saveImage(name, rotated.copy(), save_path, fld, '')
        
        i += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def readFolder():
    global frame
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(video_path, fld,'*mp4')
        files = glob.glob(path)
        for fl in files:
            readVideo(fl, fld)

            if k == ord("e"):
                break

        if k == ord("e"):
            break

readFolder()
