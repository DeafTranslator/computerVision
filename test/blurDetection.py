import cv2
import os
import glob
import myCV

train_path = 'C:\\Users\\jgraciano\\Desktop\\TeEnsenia\\computerVision\\test'
classes = ['image']

def variance_of_laplacian(image):
  return cv2.Laplacian(image, cv2.CV_64F).var()

k = 0
def readFolder():
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(train_path, fld,'*g')
        files = glob.glob(path)
        for fl in files:
            frame = cv2.imread(fl)
            name = os.path.basename(fl)
            frame = myCV.resize(frame, 1450, 800)
            gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            fm = variance_of_laplacian(gray)
            
            print("{}\t {}\t {}".format(name, fm, gray.shape))

            # cv2.imshow("gray frame", edge)

readFolder()

print('DONE!!!')