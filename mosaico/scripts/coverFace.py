import sys
sys.path.append("../..")
from setup import cv2, np

def coverFace(frame, frameWB):
  frameWB, contours, hierarchy = cv2.findContours(frameWB, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  restX = 10
  restY = 10
  sumX = 10
  sumY = 10

  indexOfHighContour = 1
  i = 0
  yMax = frameWB.shape[0]
  while i < len(contours):
    (x,y,w,h) = cv2.boundingRect(contours[i])
    if yMax > y:
      yMax = y
      indexOfHighContour = i
    i += 1

  (x,y,w,h) = cv2.boundingRect(contours[indexOfHighContour])
  
  face = frame[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)]
  merge = np.zeros((int(face.shape[0]), int(face.shape[1])))
  # Make white mask
  merge.fill(255)

  result = frameWB.copy()
  result[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)] = merge
  frame[int(y-restY):int(y+h+sumY), int(x-restX):int(x+w+sumX)] = merge

  return frame, result

  # return indexOfBiggestContour
