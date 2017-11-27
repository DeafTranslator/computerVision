import cv2
import os
import glob
import tools
import numpy as np
import math

senia = 'como'

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\12-11-2017\\Juan\\' + senia
video_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\videos\\12-11-2017\\Juan\\' + senia
save_path =  'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\12-11-2017\\Juan\\'+senia+'\\WB'


classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['CJESUS']
classes = classesDinamic

frame = None
# juan-como-CJESUS
roiPts = [(177, 341), (299, 352), (193, 273), (302, 265), (267, 338), (206, 315), (170, 310)]
# tools.resize(frame, 450, 700)
inputMode = False
# roiPts = []
cantPoint = 7

rWidth = 450
rHeight = 700

def adaptPoints(frame):
  global roiPts
  nuevoR = []
  for xy in roiPts:
    xy = (int(frame.shape[1] * (xy[0]/rWidth) ) , int(frame.shape[0] * (xy[1]/rHeight) ))
    nuevoR.append(xy) 
  roiPts = nuevoR

def variance_of_laplacian(image):
  return cv2.Laplacian(image, cv2.CV_64F).var()

def coverFace(frame, frameWB):
  frameWB, contours, hierarchy = cv2.findContours(frameWB, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  restX = 10
  restY = 10
  sumX = 10
  sumY = 10

  indexOfBiggestContour = 1
  i = 0
  yMax = frameWB.shape[0]
  while i < len(contours):
    (x,y,w,h) = cv2.boundingRect(contours[i])
    if yMax > y:
      yMax = y
      indexOfBiggestContour = i
    i += 1

  (x,y,w,h) = cv2.boundingRect(contours[indexOfBiggestContour])
  
  face = frame[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)]
  merge = np.zeros((int(face.shape[0]), int(face.shape[1])))
  # Make white mask
  merge.fill(255)

  result = frameWB.copy()
  result[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)] = merge
  frame[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)] = merge

  return frame, result


def cropContour(frame, frameWB,cant = 1):
  _, contours, hierarchy = cv2.findContours(frameWB.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  shades = []
  frame2 = frame.copy()

  restX = 10
  restY = 10
  sumX = 10
  sumY = 10

  # vaina = 1
  while len(shades) < cant and len(contours) is not 0:
    # Find biggest contour
    biggestContour = tools.findBiggestContour(contours)
    cnt = contours[biggestContour]
    # Draw rectangl
    cv2.drawContours(frame2, [cnt], 0, (0,255,255), 3)
    # Bounding points
    (x,y,w,h) = cv2.boundingRect(cnt)
    # Append image
    shades.append(frame[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)])

    # image =  frame[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)]

    # image = tools.forceSize(image, 334)

    # merge = tools.mergeImage(image, 334, 334)
  
    # tools.saveImage(str(name)+'_'+str(vaina), merge.copy(), save_path, 'CJESUS', 'CWB')
    # vaina += 1
    cant += 1

    contours.pop(biggestContour)

  return shades

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def selectROI(event, x, y, flags, param):
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode

    # if we are in ROI selection mode, the mouse was clicked,
    # and we do not already have four points, then update the
    # list of ROI points with the (x, y) location of the click
    # and draw the circle
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < cantPoint:
        roiPts.append((x, y))
        print("x: ", x)
        print("y: ", y)

        xmax = x + frame.shape[1]*0.02
        ymax = y + frame.shape[0]*0.02
        
        print("xmax: ", xmax)
        print("ymax: ", ymax)

        cv2.rectangle(frame, (x,y), (int(xmax), int(ymax) ), (0,0,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str((len(roiPts))),(int(x), int(y)), font, 1,(255,255,255),2)

        i = 0
        if len(roiPts) > cantPoint-1:
          while(i < cantPoint):
            xmax = roiPts[i][0] + frame.shape[1]*0.02
            ymax = roiPts[i][1] + frame.shape[0]*0.02
            cv2.rectangle(frame, roiPts[i], (int(xmax), int(ymax) ), (0,255,0),2)
            cv2.putText(frame, 'Press any key',(int(frame.shape[1]*0.35), int(frame.shape[0]*0.2)), font, 1,(0,255,0),3)
            i += 1
        cv2.imshow("frame", frame)

k = 0
def readVideo(video, fld):
    global frame, roiPts, inputMode
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)
    vainita = False
    time = 20
    begin = False
    k = ord("p")
    fingerTips = []

    lower = []
    upper = []
    k = ord("d")

    cap = cv2.VideoCapture(video) 
    selectionJump = 0
    idxName = 1
    adapt = True
    while( cap.isOpened() ) :
        ret,frame = cap.read()
        name = senia + '_' + fld + '_' + str(idxName)

        if ret is not True:
            break

        # rotated = rotate_bound(frame, 90)
        originalW = frame.shape[1]
        originalH = frame.shape[0]
        frame = tools.resize(frame, 450, 700)
        # if adapt is True:
        #   # adaptPoints(frame)
        #   adapt = False

        if selectionJump % 2:
            inputMode = True
            while len(roiPts) < cantPoint:
                cv2.imshow("frame", frame)
                cv2.waitKey(0)
            begin = True

            # Vamo a coge lo colore
            hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HLS)

            if time > 0:
              frame = tools.drawRectangle(frame, roiPts)

            if time > 0 and begin:
              l, u =  tools.boundsColor(hsv.copy(), roiPts)
              lower.append(l)
              upper.append(u)
              time -= 1
            elif time <= 0:
              vainita = True
              lower = np.array(lower)
              upper = np.array(upper)
              begin = False
            
            # Vamo a filtra lo colore
            if vainita:
              # frame = tools.resize(frame, originalW, originalH)
              blurFrame = cv2.blur(frame.copy(),(25,25))
              hsvB = cv2.cvtColor(blurFrame, cv2.COLOR_BGR2HLS)

              output = tools.mergeColorsImage(hsvB, lower, upper)
              median = cv2.medianBlur(output,7)
              res = cv2.bitwise_and(frame, frame, mask = median)

              # Vamo a recortar los contornos
              shades = cropContour(frame, median, cant = 3)
              
              ####
              gray = cv2.cvtColor(res.copy(), cv2.COLOR_BGR2GRAY)
              value = (15, 15)
              blurred = cv2.GaussianBlur(gray, value, 0)
              myThreshBinaryInv = cv2.threshold(blurred, 82,255,cv2.THRESH_BINARY)
              
              gray, nurvo = coverFace(gray, myThreshBinaryInv[1])
              inv = cv2.threshold(nurvo, nurvo.mean(),255,cv2.THRESH_BINARY_INV)
              
              # Canny
              myCanny = cv2.Canny(gray.copy(), gray.mean(), 255)

              # Merge canny and threshold
              out = inv[1] + myCanny

              blurryFlag = False
              for image in shades:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                if type(gray) is np.ndarray:
                  fm = variance_of_laplacian(gray)

                if fm < 850:
                  blurryFlag = True
                  # k = cv2.waitKey(0)
                  break

              text = "Not blurry"
              if blurryFlag is True:
                text = "Blurry"
              else:
                # tools.saveImage(name, out.copy(), save_path, fld, 'CWB')
                idxName +=1

              cv2.putText(frame, "{}: {:.2f}".format(text,fm), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)


              cv2.imshow("out",out)
              cv2.imshow("res",res)
            cv2.imshow("frame", hsv)
            k = cv2.waitKey(0)
        selectionJump += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def readFolder2():
    global frame
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(video_path, fld,'*mp4')
        files = glob.glob(path)
        for fl in files:
            readVideo(fl, fld)

            if k == ord("e"):
                break

        if k == ord("e"):
            break

readFolder2()
