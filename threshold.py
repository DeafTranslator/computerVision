import numpy as np
import cv2
import os
import glob
import imutils
import argparse
import math

num = '9'
numl = 'nueve'

# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\Dataset\\datasetNumero\\Numero\\'+num+'-'+numl+'\\'+num+'\\New folder'
train_path ='C:\\Users\\Juan Graciano\\Desktop'
save_path = 'C:\\Users\\Juan Graciano\\Desktop'
# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\New folder'

def rotateImage(grey, frame):
    rows,cols = grey.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
    dst = cv2.warpAffine(frame,M,(cols,rows))
    return dst

def saveImage(name, img, folder = '', create = True):
    name = name.split('.')
    if create:
        createFolder(folder)
        print(save_path+ '\\'+folder+ '\\' + name[0] + '-threshold.png')
        cv2.imwrite(save_path + '\\'+folder+'\\'+ name[0] + '-threshold.png', img)
    else:
        print(save_path+ '\\' + name[0] + '-threshold.png')
        cv2.imwrite(save_path + '\\' + name[0] + '-threshold.png', img)

print('Reading image')
path = os.path.join(train_path, '*g')
files = glob.glob(path)
for fl in files:
    img = cv2.imread(fl) 
    name = os.path.basename(fl)
    # frame = cv2.resize(frame, (400, 600), interpolation = cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    value = (5, 5)
    blurred = cv2.GaussianBlur(gray, value, 0)
    _, thresh1 = cv2.threshold(blurred, 5, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # _, thresh1 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    # kernel = np.ones((5,5), np.uint8)
    # opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
    # closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    # thresh1 = cv2.erode(thresh1, None, iterations=2)
    # thresh1 = cv2.dilate(thresh1, None, iterations=2)

    cv2.imshow('otputedge',thresh1)
    cv2.imshow('outLimpio',img)
    saveImage(name, thresh1, create = False)
    cv2.waitKey(0)

print('DONE!!!')	

########################IMPORTANTE#########################################
# Video
# # cascPath = "C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\dasar_haartrain\\myhaar2.xml"
# cascPath = "C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\handDetection\\hand.xml"
# cap = cv2.VideoCapture(0)
# while(cap.isOpened()):
#     # read image
#     ret, img = cap.read()
#     faceCascade = cv2.CascadeClassifier(cascPath)
#     edges = cv2.Canny(img, 100, 255)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.equalizeHist(gray)
#     # Detect faces in the image
#     faces = faceCascade.detectMultiScale(
# 	    gray,
# 	    scaleFactor=1.1,
# 	    minNeighbors=3,
# 	    minSize=(5, 5),
# 	    flags = 0
# 	)
    
#     extXY = 30
#     extWH = 30
# 	# Draw a rectangle around the faces
#     for (x, y, w, h) in faces:
#         if y-extXY < 0 or x-extXY < 0:
#             extXY = 0

#         crop = img[y-extXY:y+h+extWH, x-extXY:x+w+extWH]
#         #cv2.imwrite(str(i)+'.png', crop)
#         #cv2.imshow("Crop found", crop)
#         #cv2.waitKey(0)
#         cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         break

#     cv2.imshow("images", img)
#     k = cv2.waitKey(10)
#     if k == 27:
#     	break
