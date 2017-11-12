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

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def readVideo(video, fld):
    global frame
    cap = cv2.VideoCapture(video) 
    i = 0
    newTemplate = False
    while( cap.isOpened() ) :
        ret,frame = cap.read()

        if ret is not True:
            break
        
        rotated = rotate_bound(frame, 90)
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

            # for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            #     # resize the image according to the scale, and keep track
            #     # of the ratio of the resizing
            #     widthImage = img_gray.shape[1] * scale
            #     wx = widthImage / img_gray.shape[1]
            #     heightImage = img_gray.shape[0] * wx
            #     resized = tools.resize(rotated, int(widthImage), int(heightImage))
            #     # resized = cv2.resize(img_gray.copy(), int(img_gray.shape[1] * scale), img_gray.shape[0])
            #     r = img_gray.shape[1] / float(resized.shape[1])
         
            #     # if the resized image is smaller than the template, then break
            #     # from the loop
            #     if resized.shape[0] < h or resized.shape[1] < w:
            #         break

            #     # detect edges in the resized, grayscale image and apply template
            #     # matching to find the template in the image
            #     edged = cv2.Canny(resized, 50, 200)
            #     result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
            #     (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
         
            #     # check to see if the iteration should be visualized
            #     # if args.get("visualize", False):
            #         # draw a bounding box around the detected region
            #     clone = np.dstack([edged, edged, edged])
            #     cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
            #         (maxLoc[0] + w, maxLoc[1] + h), (0, 0, 255), 2)
            #     cv2.imshow("Visualize", clone)
            #     # cv2.waitKey(0)
         
            #     # if we have found a new maximum correlation value, then ipdate
            #     # the bookkeeping variable
            #     if found is None or maxVal > found[0]:
            #         found = (maxVal, maxLoc, r)
         
            # # unpack the bookkeeping varaible and compute the (x, y) coordinates
            # # of the bounding box based on the resized ratio
            # (_, maxLoc, r) = found
            # (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
            # (endX, endY) = (int((maxLoc[0] + w) * r), int((maxLoc[1] + h) * r))
         
            # # draw a bounding box around the detected result and display the image
            # cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
            # cv2.imshow("Image", image)
            # # cv2.waitKey(0)



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
                # else:
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
