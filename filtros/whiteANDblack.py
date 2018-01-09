import numpy as np
import cv2
import os
import glob
import imutils
import math

num = '8'
numl = 'ocho'
letra = 'y'

# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\Dataset\\datasetNumero\\Numero\\'+num+'-'+numl+'\\'+num+'\\New folder'
train_path ='C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\Dataset\\datasetNumero\\Numero\\'+num+'-'+numl+'\\'+num+'\\finalTest'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\tools\\FotoseRacita'
train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\tools\\FOtose\\' + letra

def createFolder():
    if not os.path.exists(save_path +'\\'+ letra):
        os.makedirs(save_path +'\\'+ letra)
        print('Folder "', letra, '"created')

def saveImage(name, img):
    createFolder()

    name = name.split('.')
    print(save_path+ '\\'+letra+ '\\' + name[0] + '-Canny.png')
    cv2.imwrite(save_path + '\\'+letra+'\\'+ name[0] + '-Canny.png', img)

def drawCircle(contours, frame):
    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)

    # finding convex hull
    hull = cv2.convexHull(cnt)

    # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    # cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        # apply cosine rule here
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle <= 90:
            count_defects += 1
            cv2.circle(frame, far, 1, [0,0,255], -1)
        #dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.circle(frame,far,5,[0,0,255],-1)
        return frame

def fill(edge):
    im_floodfill = edge
    h, w = edge.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    cv2.floodFill(im_floodfill, mask, (0,0), 255)

    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    im_out = edge | im_floodfill_inv

    cv2.imshow("Filter Melma", im_floodfill)

    return im_floodfill


print('Reading image')
path = os.path.join(train_path, '*g')
files = glob.glob(path)
for fl in files:
    frame = cv2.imread(fl) 
    name = os.path.basename(fl)

    edge = cv2.Canny(frame.copy(), 100, 255)
    image, contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    _, thresh1 = cv2.threshold(edge, 0,255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    x, y, w, h = cv2.boundingRect(cnt)
    hull = cv2.convexHull(cnt)

    # # drawing contours
    drawing = np.zeros(frame.shape,np.uint8)
    cv2.drawContours(drawing, contours, -1, (255, 255, 255), 3)

    saveImage(name, drawing)

print('Eta vaina termino')


    # cv2.imshow("Probando eta vaina", drawing)

    # fill(drawing)

    # cv2.waitKey(0)



   # grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    # value = (15, 15)
    # blurred = cv2.GaussianBlur(grey, value, 0)

    # _, thresh1 = cv2.threshold(blurred, 0,255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # # thresh1 = cv2.erode(thresh1, None, iterations=2)
    # # thresh1 = cv2.dilate(thresh1, None, iterations=2)

    # cv2.imshow("Probando eta vaina", thresh1)

# cap = cv2.VideoCapture(0)
# while(cap.isOpened()):
#     # read image
#     ret, frame = cap.read()

    # grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    # value = (15, 15)
    # blurred = cv2.GaussianBlur(grey, value, 0)

    # _, thresh1 = cv2.threshold(grey, 5,255, 8)

    # thresh1 = cv2.erode(thresh1, None, iterations=2)
    # thresh1 = cv2.dilate(thresh1, None, iterations=2)

    # # cv2.imshow("Filter Melmad", thresh1)
    # # cv2.imshow("Filter MelmadD", thresh12)
    # # k = cv2.waitKey(10)
    # # if k == 27:
    # #     break

    # image, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # cnt = max(contours, key = lambda x: cv2.contourArea(x))

    # # create bounding rectangle around the contour (can skip below two lines)
    # x, y, w, h = cv2.boundingRect(cnt)
    # # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 0)

    # # finding convex hull
    # hull = cv2.convexHull(cnt)

    # # # drawing contours
    # # drawing = np.zeros(frame.shape,np.uint8)
    # # cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    # # cv2.drawContours(drawing, [hull], 0,(0, 0, 255), 0)

    # # finding convex hull
    # hull = cv2.convexHull(cnt, returnPoints=False)

    # # finding convexity defects
    # defects = cv2.convexityDefects(cnt, hull)
    # count_defects = 0
    # # cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    # # applying Cosine Rule to find angle for all defects (between fingers)
    # # with angle > 90 degrees and ignore defects
    # for i in range(defects.shape[0]):
    #     s,e,f,d = defects[i,0]

    #     start = tuple(cnt[s][0])
    #     end = tuple(cnt[e][0])
    #     far = tuple(cnt[f][0])

    #     # find length of all sides of triangle
    #     a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    #     b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
    #     c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

    #     # apply cosine rule here
    #     angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

    #     # ignore angles > 90 and highlight rest with red dots
    #     if angle <= 90:
    #         count_defects += 1
    #         cv2.circle(frame, far, 1, [0,0,255], -1)
    #     #dist = cv2.pointPolygonTest(cnt,far,True)

    #     # draw a line from start to end i.e. the convex points (finger tips)
    #     # (can skip this part)
    #     # cv2.line(frame,start, end, [0,255,0], 2)
    #     cv2.circle(frame,far,5,[0,0,255],-1)



    # # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # # c = max(cnts, key=cv2.contourArea)
    # # print(c)
    # # # determine the most extreme points along the contour
    # # extLeft = tuple(c[c[:,0].argmin()])
    # # print(extLeft)
    # # extRight = tuple(c[c[:, 0].argmax()])
    # # extTop = tuple(c[c[:, 1].argmin()])
    # # extBot = tuple(c[c[:, 1].argmax()])

    # # cv2.drawContours(frame, [c], -1, (0, 255, 255), 2)
    # # cv2.circle(frame, extLeft, 8, (0, 0, 255), -1)
    # # cv2.circle(frame, extRight, 8, (0, 255, 0), -1)
    # # cv2.circle(frame, extTop, 8, (255, 0, 0), -1)
    # # cv2.circle(frame, extBot, 8, (255, 255, 0), -1)

    # # # cnt = max(contours, key = lambda x: cv2.contourArea(x))
    # # # x, y, w, h = cv2.boundingRect(cnt)
    # # # hull = cv2.convexHull(cnt)

    # # # # drawing contours
    # # # drawing = np.zeros(frame.shape,np.uint8)
    # # # cv2.drawContours(drawing, [cnt], 0, (255, 255, 255), -1)
    # # # # cv2.drawContours(drawing, [hull], 0,(0, 0, 255), -1)

    # cv2.imshow("Filter Melma", frame)

    # k = cv2.waitKey(10)
    # if k == 27:
    #     break



# print('Reading image')
# path = os.path.join(train_path, '*g')
# files = glob.glob(path)
# i = -1
# for fl in files:
#     i += 1
#     frame = cv2.imread(fl) 
#     edges = cv2.Canny(frame, 100, 200)
    
#     grey = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
#     grey2 = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
#     value = (15, 15)
#     blurred = cv2.GaussianBlur(grey, value, 0)
#     _, thresh1 = cv2.threshold(grey, 5,255, 12)

#     image, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cnt = max(contours, key = lambda x: cv2.contourArea(x))
#     x, y, w, h = cv2.boundingRect(cnt)
#     hull = cv2.convexHull(cnt)

#     # drawing contours
#     drawing = np.zeros(frame.shape,np.uint8)
#     cv2.drawContours(drawing, [cnt], 0, (255, 255, 255), -1)
#     # cv2.drawContours(drawing, [hull], 0,(0, 0, 255), -1)

#     # cv2.imshow('input1',img)

#     name = os.path.basename(fl)
#     name = name.split('.')

#     print(save_path+ '\\' + name[0] + '-thresh.jpeg')

#     cv2.imwrite(save_path + '\\' + name[0] + '-thresh.jpeg', drawing)

#     # cv2.imshow("image1", frame)
#     # cv2.imshow("image2", drawing)
#     # cv2.waitKey(0)
#     # if i > 6:
#     #     print('DONE!!!')
#     #     break
#     #break