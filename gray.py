import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\internetNum\\flip'
save_path =  'C:\\Users\\jgraciano\\Desktop\\Dataset\\internetNum\\flip\\gray'


classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# classes = ['d','e','f','k','n','o','r','t','u','v','w','x','y']
classesDinamic = ['nombre']
classes = classesNum

frame = None

k = 0

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

            # force
            frame = tools.forceSize(frame, 334)


            #################
            gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            value = (25, 25)

            median = gray.copy()
            median = median.reshape(-1)
            mean = np.mean(median)
            mean *= 0.20

            blurred = cv2.GaussianBlur(gray, value, 0)
            myThreshBinaryInv = cv2.threshold(blurred, mean,255,cv2.THRESH_BINARY)
            
            cv2.imshow("myThreshBinaryInv", myThreshBinaryInv[1])

            res = cv2.bitwise_and(gray, gray, mask = myThreshBinaryInv[1])

            result = tools.mergeImage(res, 334, 334)
            
            cv2.imshow("frame", result)
            tools.saveImage(name, result.copy(), save_path, fld, 'G')
            k = cv2.waitKey(1)
                    
            if k == ord("q"):
                break

        if k == ord("q"):
            break

readFolder()
