import cv2
import os
import glob
import tools
import numpy as np

train_path ='C:\\Users\\Juan Graciano\\Desktop\\d'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\d\\saved'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']

classes = classesNum


frame = None
cantPoint = 7
roiPts = []
inputMode = False

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

        xmax = x + frame.shape[1]*0.035
        ymax = y + frame.shape[0]*0.045
        
        print("xmax: ", xmax)
        print("ymax: ", ymax)

        cv2.rectangle(frame, (x,y), (int(xmax), int(ymax) ), (0,0,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str((len(roiPts))),(int(x), int(y)), font, 1,(255,255,255),2)

        i = 0
        if len(roiPts) >cantPoint-1:
          while(i < cantPoint):
            xmax = roiPts[i][0] + frame.shape[1]*0.035
            ymax = roiPts[i][1] + frame.shape[0]*0.045
            cv2.rectangle(frame, roiPts[i], (int(xmax), int(ymax) ), (0,255,0),2)
            cv2.putText(frame, 'Press any key',(int(frame.shape[1]*0.35), int(frame.shape[0]*0.2)), font, 1,(0,255,0),3)
            i += 1
        cv2.imshow("frame", frame)

k = 0
def readFolder():
    global frame, roiPts, inputMode
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)
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
        
            
            # if inputMode is not False:
            #     y0 = roiPts[3][1]
            #     y1 = roiPts[0][1]
            #     x0 = roiPts[0][0]
            #     x1 = roiPts[3][0]
                
            frame = tools.CropHand(frame)
            # cv2.imshow("frame", frame)

            if inputMode is False:
                k = ord("i")
            else:
                # tools.saveImage(name, frame.copy(), save_path, fld, 'tape')
                k = cv2.waitKey(1)

            if k == ord("i"):
                inputMode = True
                orig = frame.copy()

                while len(roiPts) < 4:
                    cv2.imshow("frame", frame)
                    cv2.waitKey(0)
                    
            elif k == ord("q"):
                break
            else :
                pass
        if k == ord("q"):
            break

    print('Terminamo')

def readimage():
    global frame, roiPts, inputMode
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)
    roiBox =  None
    print('Reading images')
    path = os.path.join(train_path, '*g')
    files = glob.glob(path)
    for fl in files:
        frame = cv2.imread(fl)
        name = os.path.basename(fl)
        frame = tools.resize(frame, 400, 711)
        
        # if inputMode is not False:
        #     y0 = roiPts[3][1]
        #     y1 = roiPts[0][1]
        #     x0 = roiPts[0][0]
        #     x1 = roiPts[3][0]
        #     # frame = tools.detectTape(frame[y0:y1, x0:x1])
        # frame = cv2.Canny(frame, 100, 255)
        hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
        value = (5, 5)
        blurred = cv2.GaussianBlur(gray.copy(), value, 0)
        # thresh1 = cv2.adaptiveThreshold(gray, 100, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
        _, thresh2 = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        cv2.imshow("frame", hsv)
        cv2.imshow("gray", gray)
        cv2.imshow("thresh2", thresh2)


        if inputMode is False:
            k = ord("i")
        else:
            # tools.saveImage(name, frame.copy(), save_path, fld, 'tape')
            k = cv2.waitKey(0)

        if k == ord("i"):
            inputMode = True
            orig = frame.copy()

            while len(roiPts) < 4:
                cv2.imshow("frames", frame)
                cv2.waitKey(0)
                
        elif k == ord("q"):
            break
        else :
            pass
        if k == ord("q"):
            break

    print('Terminamo')

def readVideo():
  global frame, roiPts, inputMode
  cv2.namedWindow("frame")
  cv2.setMouseCallback("frame", selectROI)
  roiBox =  None
  cap = cv2.VideoCapture(0)
  k = ord("s")
  vainita = False
  lower = [0, 0, 0]
  upper = [0, 0, 0]
  while( cap.isOpened() ) :
      ret,frame = cap.read()
      # frame = tools.resize(frame, 400, 711)
        
      hsv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)

      if inputMode is not False and vainita == False:
          y0 = roiPts[3][1]
          y1 = roiPts[0][1]
          x0 = roiPts[0][0]
          x1 = roiPts[3][0]
          lower, upper =  tools.boundsColor(hsv, roiPts)
          # lower = np.array([85,36,141])
          # upper = np.array([219,172, 255])
          # lower = np.array([0, 10, 60])
          # upper = np.array([20, 150, 255])
          print("entro")
          vainita = True
          # frame = tools.detectTape(frame[y0:y1, x0:x1])

      # res = cv2.bitwise_and(frame,frame, mask= mask)

      if vainita:
        output = tools.mergeColorsImage(hsv, lower, upper, len(roiPts))
        res = cv2.bitwise_and(frame, frame, mask= output)

        kernel = np.ones((5,5),np.uint8)
        # erosion = cv2.erode(output,kernel,iterations = 1)
        erosion = cv2.morphologyEx(output, cv2.MORPH_OPEN, kernel)

        median = cv2.medianBlur(output,7)
        cv2.imshow("output ", median)

        # print("bajo afuera ", lower)
        # print("alto afuera ", upper)
        # mask = cv2.inRange(frame, lower, upper)
        # cv2.imshow("thresh2", mask)


      gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
      value = (5, 5)
      blurred = cv2.GaussianBlur(gray.copy(), value, 0)
      # thresh1 = cv2.adaptiveThreshold(gray, 100, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
      _, thresh2 = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


      cv2.imshow("frame", frame)
      cv2.imshow("hsv", hsv)
      cv2.imshow("gray", thresh2)
      

      if k == ord("i") and inputMode is False:
            k = ord("i")
      else:
          # tools.saveImage(name, frame.copy(), save_path, fld, 'tape')
          k = cv2.waitKey(1)

      if k == ord("i"):
          inputMode = True

          while len(roiPts) < cantPoint:
              cv2.imshow("frame", frame)
              cv2.waitKey(0)
              
      elif k == ord("q"):
          break

      if k == ord("q"):
          break

      # k = cv2.waitKey(10)
      # if k == 27:
      #     break

readVideo()
