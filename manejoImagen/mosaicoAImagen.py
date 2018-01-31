

cuadritoW = 200
cuadritoH = 200

cantCuadritoW = 3
cantCuadritoH = 3

fill = [0, 255]

# fill (0 0r 255)
def makeBackground(fill):
	background = np.zeros((int(cuadritoH*cantCuadritoH), int(cuadritoW*cantCuadritoW), 1))
    background.fill(fill)
	return background

def cropImage(img):
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
	      name = name + '_' + str(idx)
	      idx += 1
	      cant += 1

	      # # center 
	      # (xB, yB, wB, hB) = newImage.shape[0]*0.3, newImage.shape[1]*0.3, newImage.shape[0]*0.7, newImage.shape[1]*0.7
	      contours.pop(biggestContour)

	  return shades

def makeMosaic(img):

	shapes = cropImage(img)
	background = makeBackground(fill[1])

	# change shape's size for (cuadritoW * cuadritoH)
	for i in shapes:
		i = myCV.resize(i, cuadritoW, cuadritoH)

	# head location
	background[0:int(cuadritoH), int(cuadritoW):int(cuadritW*2)] = shapes[0]

	# left location
	background[int(cuadritoH):int(cuadritoH*2), 0:int(cuadritW)] = shapes[1]

	# right location
	background[int(cuadritoH):int(cuadritoH*2), int(cuadritoW*2):int(cuadritW*3)] = shapes[2]