import numpy as np
import cv2
import os
import glob

num = '9'
numl = 'nueve'

# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\Dataset\\datasetNumero\\Numero\\'+num+'-'+numl+'\\'+num+'\\New folder'
train_path ='C:\\Users\\Juan Graciano\\Desktop\\d'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\d'
# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\New folder'

print('Reading image')
path = os.path.join(train_path, '*g')
files = glob.glob(path)
for fl in files:
    img = cv2.imread(fl) 
    name = os.path.basename(fl)
    # img = cv2.resize(img, (400, 711), interpolation = cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(hsv.copy(), cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    value = (5, 5)
    blurred = cv2.GaussianBlur(gray.copy(), value, 0)
    thresh1 = cv2.adaptiveThreshold(gray, 100, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    _, thresh2 = cv2.threshold(thresh1, 5, 100, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # _, thresh1 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    # kernel = np.ones((5,5), np.uint8)
    # opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
    # closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    # thresh1 = cv2.erode(thresh1, None, iterations=2)
    # thresh1 = cv2.dilate(thresh1, None, iterations=2)

    im2, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    hull = cv2.convexHull(cnt)

    # epsilon = 0.1*cv2.arcLength(cnt,True)
    # approx = cv2.approxPolyDP(cnt,epsilon,True)
    # area = cv2.contourArea(cnt)
    cv2.drawContours(img, [cnt], -1, (0,255,0), 3)
    cv2.drawContours(img, [hull], -1, (0,255,0), 3)
    cv2.imshow('original', img)

    cv2.imshow('gray',gray)
    # cv2.imshow('res', res)
    cv2.imshow('thresh1', thresh1)
    cv2.imshow('thresh2', thresh2)
    # saveImage(name, thresh1, create = False)
    cv2.waitKey(0)

print('DONE!!!')	

