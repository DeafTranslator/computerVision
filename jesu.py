import cv2
import os
import glob
import tools
import numpy as np

train_path = 'C:/Users/jgraciano/Desktop/TeEnsenia/computerVision'

classesDinamic = ['nombre']
classes = classesDinamic

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
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
            image = cv2.imread(fl)
            cv2.imshow("image", image)
            
            image = cv2.resize(image, (100, 200), interpolation=cv2.INTER_CUBIC)
			
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			
            fm = variance_of_laplacian(gray)
            text = "Not Blurry"
		 
			# if the focus measure is less than the supplied threshold,
			# then the image should be considered "blurry"
            if fm < 190:
               text = "Blurry"
		 
			# show the image
            cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
            cv2.imshow("Image", image)
            key = cv2.waitKey(0)
            
            
        if k == ord("q"):
            break

readFolder()
