import sys
sys.path.append("../..")
from setup import cv2, np, myCV

def cropContour(frame, frameWB,name, cant = 1):
  _, contours, hierarchy = cv2.findContours(frameWB.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  shades = []
  frame2 = frame.copy()

  (restX, restY, sumX, sumY) = (2, 4, 4, 2)

  idxH = myCV.findHighContour(contours, frameWB)
  contours.pop(idxH)

  idx = 1
  while len(shades) < cant and len(contours) is not 0:
    # Find biggest contour
    biggestContour = myCV.findBiggestContour(contours)
    cnt = contours[biggestContour]
    # Draw rectangl
    cv2.drawContours(frame2, [cnt], 0, (0,255,255), 3)
    # Bounding points
    (x,y,w,h) = cv2.boundingRect(cnt)
    # Append image
    newImage = frame[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)]

    if type(newImage) is np.ndarray:
      shades.append(newImage)
      # cv2.imshow("nueva", newImage)
      name = name + '_' + str(idx)
      idx += 1
      # tools.saveImage(name, frame[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)].copy(), save_path, 'prueba', 'rgb')
      cant += 1

      # # center 
      # (xB, yB, wB, hB) = newImage.shape[0]*0.3, newImage.shape[1]*0.3, newImage.shape[0]*0.7, newImage.shape[1]*0.7
      contours.pop(biggestContour)

  return shades
