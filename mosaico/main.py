import setup
import scripts.rotate_bound as rot
import scripts.cropContour as crp
import scripts.coverFace as cfa
import scripts.edgeDetection as edd
import scripts.blurDetection as bld

frame = None
inputMode = False
idxVideo = 1
k = 0

# Clean .txt file
file = open("coordenadas.txt", "w").close()

# Write file
def writeTXT(posX, posY):
  file = open("coordenadas.txt", "r+")
  old = file.read()
  file.seek(0)
  file.write("{} ({}, {}),".format(old, posX, posY))
  file.close()

def selectROI(event, x, y, flags, param):
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, inputMode

    # if we are in ROI selection mode, the mouse was clicked,
    # and we do not already have four points, then update the
    # list of ROI points with the (x, y) location of the click
    # and draw the circle
    if inputMode and event == setup.cv2.EVENT_LBUTTONDOWN and len(setup.roiPts) < setup.cantPoint:
        setup.roiPts.append((x, y))

        xmax = x + frame.shape[1]*setup.diamRoi
        ymax = y + frame.shape[0]*setup.diamRoi
        
        print("({0}, {1})\n xmax: {2}\n ymax: {3}\n".format(x, y, xmax, ymax))

        # Take ROI positions
        writeTXT(x, y)

        # Make rectangle
        setup.cv2.rectangle(frame, (x,y), (int(xmax), int(ymax) ), (0,0,255),2)

        # Draw cant of rectangles
        setup.cv2.putText(frame, str((len(setup.roiPts))),(int(x), int(y)), setup.font, setup.sizThk,(255,255,255),2)

        # Green go
        i = 0
        if len(setup.roiPts) > setup.cantPoint-1:
          while(i < setup.cantPoint):
            xmax = setup.roiPts[i][0] + frame.shape[1]*setup.diamRoi
            ymax = setup.roiPts[i][1] + frame.shape[0]*setup.diamRoi
            setup.cv2.rectangle(frame, setup.roiPts[i], (int(xmax), int(ymax) ), (0,255,0),2)
            setup.cv2.putText(frame, 'Press any key',(int(frame.shape[1]*setup.wdTxt), int(frame.shape[0]*setup.hiTxt)), setup.font, setup.sizThk,(0,255,0),3)
            i += 1
        setup.cv2.imshow("frame", frame)

def fillContour(img):
  frame = img.copy()
  _, thresh1 = setup.cv2.threshold(frame.copy(), 75, 255, setup.cv2.THRESH_BINARY)
  __, contours, hierarchy = setup.cv2.findContours(thresh1, setup.cv2.RETR_LIST, setup.cv2.CHAIN_APPROX_NONE)

  i = 0
  while len(contours) is not 0:
    i += 1
    # Find biggest contour
    biggestContour = setup.myCV.findBiggestContour(contours)
    cnt = contours[biggestContour]
    setup.cv2.drawContours(frame, [cnt], -1, 255, 2)
    contours.pop(biggestContour)

  # setup.cv2.imshow("thresh1",thresh1)
  # setup.cv2.imshow("cambio",frame)
  # setup.cv2.waitKey(0)

  # _, thresh1 = setup.cv2.threshold(frame.copy(), 100, 255, setup.cv2.THRESH_BINARY_INV)
  return frame

def loadVideo(video, fld, namePath):

    global frame, roiPts, inputMode, idxVideo
    inputMode = True
    setup.cv2.namedWindow("frame")
    setup.cv2.setMouseCallback("frame", selectROI)
    
    ###
    collect = True
    lower, upper = [], []
    idxFrame, idxVideo = 0, 1
    ###

    cap = setup.cv2.VideoCapture(video) 
    
    while( cap.isOpened() ):
        ret, frame = cap.read()
        name = fld + '_' + str(idxFrame)

        if ret is not True:
            break

        rotated = rot.rotate_bound(frame, setup.degree)
        # frame = rotated
        frame = setup.myCV.resize(rotated, setup.wdImage, setup.hiImage)
 
        if idxFrame % setup.modulu:
            while len(setup.roiPts) < setup.cantPoint:
                setup.cv2.imshow("frame", frame)
                setup.cv2.waitKey(0)

            # Vamo a coge lo colore
            hsv = setup.cv2.cvtColor(frame.copy(), setup.cv2.COLOR_BGR2HLS)

            if setup.frameCollected > 0:
              frame = setup.myCV.drawRectangle(frame, setup.roiPts)
            # *
            if setup.frameCollected > 0 and collect:
              l, u =  setup.myCV.boundsColor(hsv.copy(), setup.roiPts)
              lower.append(l)
              upper.append(u)
              setup.frameCollected -= 1
            else:
              lower = setup.np.array(lower)
              upper = setup.np.array(upper)
              collect = False
            
            # Vamo a filtra lo colore
            if not collect:
              blurFrame = setup.cv2.blur(frame.copy(),setup.valueBlur)
              hsvB = setup.cv2.cvtColor(blurFrame, setup.cv2.COLOR_BGR2HLS)

              output, promLower, promUpper = setup.myCV.mergeColorsImage(hsvB, lower, upper)
              median = setup.cv2.medianBlur(output,7)
              median = fillContour(median.copy())
              res = setup.cv2.bitwise_and(frame, frame, mask = median)
              
              ####
              gray = setup.cv2.cvtColor(res.copy(), setup.cv2.COLOR_BGR2GRAY)
              # blurred = setup.cv2.GaussianBlur(gray, setup.valueBlur, 0)
              myThreshBinaryInv = setup.cv2.threshold(gray, 20,255, setup.cv2.THRESH_BINARY)
              
              # Vamo a recortar los contornos
              shades = crp.cropContour(frame, median.copy(), name , cant = setup.hands)
              gray, nurvo = cfa.coverFace(gray, median)
              inv = setup.cv2.threshold(nurvo.copy(), 90,255, setup.cv2.THRESH_BINARY_INV)

              # Merge canny and threshold
              aha = edd.edgeDetection(gray.copy())
              out = inv[1] + aha

              bld.blurDetection(shades, frame, name, out, fld, namePath)

              if setup.saveMode is False:
                setup.cv2.imshow("out",out)
                setup.cv2.imshow("res",res)
            if setup.saveMode is False:
              setup.cv2.imshow("frame", frame)
            k = setup.cv2.waitKey(1)
        idxFrame += 1

        if setup.cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    setup.cv2.destroyAllWindows()

def loadFolder():
    global frame
    print('Reading image')
    for fld in setup.classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = setup.classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = setup.os.path.join(setup.video_path, fld,'*mp4')
        files = setup.glob.glob(path)
        idxVideo = 0
        for fl in files:
            loadVideo(fl, fld, str(idxVideo))
            idxVideo += 1
            setup.roiPts = []
            setup.cv2.waitKey(0)

            if k == ord("e"):
                break

        if k == ord("e"):
            break

loadFolder()
