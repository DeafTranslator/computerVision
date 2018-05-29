import sys
sys.path.append("../..")
from setup import cv2, np, myCV

def cropContour(frame, frameWB,name, cant = 1):
  _, contours, hierarchy = cv2.findContours(frameWB.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  shades = []
  frame2 = frame.copy()

  (restX, restY, sumX, sumY) = (2, 4, 4, 2)

  # Elimina el cuadro superior
  idxH = myCV.findHighContour(contours, frameWB)
  contours.pop(idxH)

  idx = 1
  while len(shades) < cant and len(contours) is not 0:
    # Find biggest contour
    biggestContour = myCV.findBiggestContour(contours)
    cnt = contours[biggestContour]
    # Draw rectangl
    # cv2.drawContours(frame2, [cnt], 0, (0,255,255), 3)
    # Bounding points
    (x,y,w,h) = cv2.boundingRect(cnt)
    # Append image
    newImage = frame[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)]

    if type(newImage) is np.ndarray:
      shades.append(newImage)
      name = name + '_' + str(idx)
      idx += 1
      cant += 1
      contours.pop(biggestContour)

  return shades
