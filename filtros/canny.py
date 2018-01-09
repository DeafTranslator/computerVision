import cv2
import os
import glob
import tools

# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Nati videos\\juan\\numero2\\cropV3'
train_path = 'C:\\Users\\Juan Graciano\\Desktop'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\Nati videos\\juan\\numero2\\canny'
classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# classesAlph = ['c','g','m','n','o','p','q','u','v','x','y']
# classesAlph = ['a','b','c','d','e','f','g','h','i','k','m','n','o','p','q','r','s','t','u','v','w','x','y']
classesNum = ['0','1','2','3','4','5','6','7','8','9']

classes = classesNum


k = 0
def readFolder():
    global frame, roiPts, inputMode
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
            # frame = tools.resize(frame, 711, 400)
            edge = cv2.Canny(frame.copy(), 100, 255)
        
            # cv2.imshow("gray frame", edge)
            tools.saveImage(name, edge, save_path, fld, 'canny')


    print('Terminamo')

def readimage():
    print('Reading images')
    path = os.path.join(train_path, '*g')
    files = glob.glob(path)
    for fl in files:
        frame = cv2.imread(fl)
        name = os.path.basename(fl)
        frame = tools.resize(frame, 400, 711)
        edge = cv2.Canny(frame.copy(), 100, 255)
        # frame = resize(frame, 400, 600)
        # gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        # img = frame.copy()
        # aux = frame.copy()

        # nueva = orb(gray, frame)
        # nueva, x, y, w, h = circlePoint(img)
        # nueva = circlePoint(img)

        # corte = cropImage2(nueva, x, y, w, h)
        cv2.imshow("canny", edge)

        # saveImage(name, corte)

        cv2.waitKey(0)
        # k += 1
        # if k > 100:
        #     break

    print('Terminamo')

# readFolder()
readimage()

print('DONE!!!')