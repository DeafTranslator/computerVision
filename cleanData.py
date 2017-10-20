import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:\\Users\\Juan Graciano\\Desktop\\HandComp\\dataset\\veremoJJ'
save_path =  'C:\\Users\\Juan Graciano\\Desktop\\HandComp\\dataset\\veremoJJ\\train\\CANNY+THRESH_BINARY\\334x334\\train\\train2\\selected'
train_path = 'C:\\Users\\Juan Graciano\\Desktop\\HandComp\\dataset\\veremoJJ\\train\\CANNY+THRESH_BINARY\\334x334\\train\\train2'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
# test = ['testFixed2']
classes = classesNum


frame = None
# roiPts = [(205, 159),(346, 162),(347, 254),(230, 270)]
roiPts = []
inputMode = True

k = 0
def readFolder():
    global frame, roiPts, inputMode
    cv2.namedWindow("frame")
    roiBox =  None
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(train_path, fld,'*g')
        files = glob.glob(path)
        idx = 0
        image = []
        for fl in files:
            frame = cv2.imread(fl)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            name = os.path.basename(fl)
            # fdifetente = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
            # cv2.imshow("frame1", f[1])
            # f11 = cv2.Canny(frame, 100, 250)
            # cv2.imshow("frame1", f[1])
            # out = fdifetente[1] + f11
            # cv2.imshow("frame", out)
            # frame = np.dtype(float)
            # frame = tools.resize(frame, 400, 400)
            
            # if inputMode is not False:
            #     y0 = roiPts[3][1]
            #     y1 = roiPts[0][1]
            #     x0 = roiPts[0][0]
            #     x1 = roiPts[3][0]
            #     # frame = tools.CropHand(frame)
            #     frame = frame[int(y0):int(y1), int(x0):int(x1)]

            # Crop Tape
            # frame = tools.detectTape(frame)

            # Crop Hand
            # frame = tools.cropHand(frame)

            # Canny
            # frame = cv2.Canny(frame, 100, 255)

            # force
            # frame = tools.forceResize(frame, 334, 334)
            
            # Merge
            # frame = tools.mergeImage(frame, 334, 334)
            # frame = tools.resize(frame, 224, 224)
            # f = np.array(frame)
            # f = f.astype('float32')

            # f = f / 255
            # image.append(f)
            # cv2.imshow("frame", f[1])
            # print("frame shape", f[1].shape)
            # print("\n\n\nframe shape", frame.shape)
            # print("frame 0")
            # for h in f[1][150]:
            #     print(h)
            
            # # print("%.5f" % f[:, :][0])
            # print("\n\n")
            # print("frame 1")
            # for h in f[:, :, 1][150]:
            #     print("%.5f" % h)
            # print(f[:, :, 1][0])
            # print("\n\n")
            # print("frame 2")
            # for h in f[:, :, 2][150]:
            #     print("%.5f" % h)

            # print((f[:, :, 2]==f[:, :, 2]).all())
            
            
            # break
            # print(f[:, :, 2][0])
            if idx % 2 == 0:
                one = frame.copy()
                tools.saveImage(name, one, save_path, fld, 's')
                k = cv2.waitKey(1)
            idx += 1  

            if k == ord("q"):
                break

        # print(image[0].shape)
        # print(image)
        if k == ord("q"):
            break

readFolder()
