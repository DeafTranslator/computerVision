import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\2-11-2017\\Jesus\\simpleCrop'
save_path =  'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\2-11-2017\\Jesus\\canny_WB'


classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# classes = ['d','e','f','k','n','o','r','t','u','v','w','x','y']
classesDinamic = ['nombre']
classes = classesDinamic

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
            # grayOrigi = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            # hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)
            
            # # hsv[:,:,0] = 100
            # hsv[:,:,2] = 200

            # bgr = cv2.cvtColor(hsv.copy(), cv2.COLOR_HSV2BGR)

            # gray = cv2.cvtColor(bgr.copy(), cv2.COLOR_BGR2GRAY)
            # gray = cv2.medianBlur(gray.copy(), 3)
            # # print(gray.shape)
            # # _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

            # # Average gray color
            # # median = grayOrigi.copy()
            # # median = median.reshape(-1)
            # # mean = np.average(median)
            # # mean *= 0.70

            # # print('La media es\t', mean)
            
            # value = (35, 35)
            # blurred = cv2.GaussianBlur(grayOrigi.copy(), value, 0)
            # _, thresh1 = cv2.threshold(blurred,60,255, cv2.THRESH_BINARY_INV)
            # # print(thresh1.shape)
            # yuv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2YUV)
            
            # # _, thresh2 = cv2.threshold(grayYuv, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
            # (b,g,r) = cv2.split(yuv.copy())
            # # print(len(b))
            # equ = cv2.equalizeHist(gray)
            # img = cv2.merge((equ, g, r))
            # grayYuv = cv2.cvtColor(img.copy(), cv2.COLOR_YUV2BGR)

            # f11 = cv2.Canny(grayOrigi, 70, 150, L2gradient=True)
            # out = thresh1 + f11
            # cv2.imshow("origial", out)
            # cv2.imshow("gray", grayOrigi)
            # cv2.imshow("thresh1", thresh1)
            # cv2.imshow("canny", f11)
            # # print("antes", out.shape)
            # # out[:,:,0] = fdifetente[1] + f11
            # # out[:,:,1] = fdifetente[1] + f11
            # # out[:,:,2] = fdifetente[1] + f11
            # cv2.imshow("frames", out)
            # cv2.waitKey(0)



            #################
            gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            value = (33, 33)
            blurred = cv2.GaussianBlur(gray, value, 0)
            myThreshBinaryInv = cv2.threshold(blurred, 80,255,cv2.THRESH_BINARY)
            
            # Canny
            myCanny = cv2.Canny(gray.copy(), 90, 240)

            # cv2.imshow("myCanny", myCanny)
            cv2.imshow("myThreshBinaryInv", myThreshBinaryInv[1])
            # Merge canny and threshold
            out = myThreshBinaryInv[1] + myCanny
            # cv2.imshow("out", out)

            # Merge
            frame = tools.mergeImage(out, 334, 334)
            
            cv2.imshow("frame", frame)
            # tools.saveImage(name, frame.copy(), save_path, fld, 'CWB')
            k = cv2.waitKey(0)
                    
            if k == ord("q"):
                break

        if k == ord("q"):
            break

readFolder()
