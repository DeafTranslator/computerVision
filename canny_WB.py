import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\alpha_newSCrop\\selectwithFlip\\cropHand'
save_path =  'C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\alpha_newSCrop\\selectwithFlip\\cropHand\\canny_wb'


classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classes = ['e']

frame = None

k = 0

def readFolder():
    global frame, roiPts, inputMode
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

            # force
            frame = tools.forceSize(frame, 334)

            #######
            grayOrigi = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)
            
            # hsv[:,:,0] = 100
            hsv[:,:,2] = 200

            bgr = cv2.cvtColor(hsv.copy(), cv2.COLOR_HSV2BGR)

            gray = cv2.cvtColor(bgr.copy(), cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray.copy(), 3)
            # print(gray.shape)
            # _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
            _, thresh1 = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
            # print(thresh1.shape)
            yuv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2YUV)
            
            # _, thresh2 = cv2.threshold(grayYuv, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
            (b,g,r) = cv2.split(yuv.copy())
            # print(len(b))
            equ = cv2.equalizeHist(gray)
            img = cv2.merge((equ, g, r))
            grayYuv = cv2.cvtColor(img.copy(), cv2.COLOR_YUV2BGR)

            f11 = cv2.Canny(grayOrigi, 120, 190, L2gradient=True)
            out = thresh1 + f11
            cv2.imshow("origial", out)
            cv2.imshow("gray", equ)
            cv2.imshow("hsv", hsv)
            cv2.imshow("canny", f11)
            # print("antes", out.shape)
            # out[:,:,0] = fdifetente[1] + f11
            # out[:,:,1] = fdifetente[1] + f11
            # out[:,:,2] = fdifetente[1] + f11
            cv2.imshow("frames", out)
            cv2.waitKey(0)











            #################
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # value = (25, 25)
            # blurred = cv2.GaussianBlur(gray, value, 0)
            # # blurFrame = cv2.medianBlur(gray.copy(),7)
            # myThreshBinaryInv = cv2.threshold(blurred,70,255,cv2.THRESH_BINARY_INV)
            
            # # Canny
            # myCanny = cv2.Canny(frame, 58, 255)
            # # myCanny = cv2.cornerHarris(myCanny,2,3,0.04)
            # # myCanny = cv2.dilate(myCanny,None)
      
            # cv2.imshow("myCanny", myCanny)
            # cv2.imshow("myThreshBinaryInv", myThreshBinaryInv[1])
            # out = myThreshBinaryInv[1] + myCanny
            # cv2.imshow("out", out)

            # Merge
            # frame = tools.mergeImage(out, 334, 334)
            
            cv2.imshow("frame", frame)
            # tools.saveImage(name, grayOrigi.copy(), save_path, fld, 'jesu')
            k = cv2.waitKey(0)
                    
            if k == ord("q"):
                break

        if k == ord("q"):
            break

readFolder()
