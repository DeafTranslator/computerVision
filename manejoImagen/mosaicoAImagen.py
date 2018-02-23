import cv2
import os
import glob
import numpy as np
import myCV
from enum import Enum

clase = 'nombre'
saveMode = True
showMode = False

image_path ='C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\20-1-2018\\MosaicoJesusLaplacian\\jesus\\' + clase + '\\'
save_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\20-1-2018\\MosaicoJesusLaplacian\\' + clase + '480_720' + '\\ajuste480_720'

classnombre = [clase + '_1', clase + '_2', clase +'_3', clase +'_4', clase +'_5', clase +'_6', clase +'_7', clase +'_8',
clase +'_9', clase +'_10', clase +'_11', clase +'_12', clase +'_13', clase +'_14', clase +'_15', clase +'_16',
clase +'_17', clase +'_18', clase +'_19', clase +'_20', clase +'_21', clase +'_22', clase +'_23', clase +'_24',
clase +'_25', clase +'_26', clase +'_27', clase +'_28', clase +'_29', clase +'_30', clase +'_31', clase +'_32',
clase +'_33', clase +'_34', clase +'_0']

classPrimera = [ '1',  '2', '3', '4', '5', '6', '7', '8',
'9', '10', '11', '12', '13', '14', '15', '16',
'17', '18', '19', '20', '21', '22', '23', '24',
'25', '26', '27', '28', '29', '30', '31', '32',
'33', '34', '0']

classes = classPrimera


class Fill(Enum):
	BLACK = 0
	WHITE = 255

cantCuadritoW = 3
cantCuadritoH = 3

cuadritoW = int(480/cantCuadritoW)
cuadritoH = int(720/cantCuadritoH)

# 334, 334

k = 0

def createFolder(fl):
    if not os.path.exists(fl):
        os.makedirs(fl)
        print('Folder "', fl, '"created')

def saveImage(name, img, save_path, alias = ''):
    name = name.split('.')
    if alias is not '':
        alias = '-' + alias
    print(save_path + '\\' + name[0] +alias+'.png')
    cv2.imwrite(save_path + '\\' + name[0] +alias+'.png', img)

def sortHands(locations, shades):

	if len(locations) > 0 and locations[0][0] > locations[len(locations)-1][0]:
		auxL = locations[len(locations)-1]
		auxS = shades[len(shades)-1]
		# Locaitons
		locations[len(locations)-1] = locations[0]
		locations[0] = auxL
		# Shades
		shades[len(locations)-1] = shades[0]
		shades[0] = auxS

	return locations, shades

def resizeImage(frame, width, height):

    # Adjusting size
    if frame.shape[0] > height:
        hy = height/frame.shape[0]
        hx = frame.shape[1]*hy
        frame = cv2.resize(frame, (int(hx), int(height)), interpolation = cv2.INTER_CUBIC)
    if frame.shape[1] > width:
        hx = width/frame.shape[1]
        hy = frame.shape[0]*hx
        frame = cv2.resize(frame, (int(width), int(hy)), interpolation = cv2.INTER_CUBIC)
    
    # Mask
    newImage = np.zeros((int(cuadritoH), int(cuadritoW)))
    newImage.fill(Fill.WHITE.value)
    
    # Putting the image in the middle
    x_offset = (width - frame.shape[1])/2
    y_offset = (height - frame.shape[0])/2

    newImage[:,:][int(y_offset):int(y_offset+frame.shape[0]), int(x_offset):int(x_offset+frame.shape[1])] = frame

    return newImage

def adjustImage(img):
	frame = fillContour(img.copy())
	_, contours, hierarchy = cv2.findContours(frame.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	# tamanio ajustado
	cX, cY, cW, cH = img.shape[1], img.shape[0], 0, 0

	i = 0
	while i < 3 and len(contours) is not 1:
		# Find biggest contour
		biggestContour = myCV.findBiggestContour(contours)
		cnt = contours[biggestContour]

		# Bounding points
		(x,y,w,h) = cv2.boundingRect(cnt)

		constD = 0
		constDi = 0
		if x - constDi < cX - constDi:
			cX = x + constDi

		if y - constDi < cY - constDi:
			cY = y + constDi

		if w + x + constD > cW + constD:
			cW = w + x + constD

		if h + y + constD > cH + constD:
			cH = h + y + constD

		# Get new image. Crop original image
		newImage = img[int(y):int(y+h), int(x):int(x+w)]

	    # Validation
		if type(newImage) is np.ndarray:
			contours.pop(biggestContour)
			i += 1

	if cY - 10 >= 0:
		cY -= 10
	if cH + 10 < img.shape[0]:
		cH += 10
	if cX - 10 >= 0:
		cX -= 10
	if cW + 10 < img.shape[1]:
		cW += 10

	return img[int(cY):int(cH), int(cX):int(cW)]

def headShot(shapes, location):
	i = 1
	index = 0 
	head = []
	if len(location) > 0:
		avg = np.average(shapes[index])
		head = shapes[0]
		while i < len(shapes):
			if np.average(shapes[i]) < avg:
				avg = np.average(shapes[i])
				index = i
				head = shapes[i]
			i += 1

		shapes.pop(index)
		location.pop(index)

	return head, shapes, location

def makeBackground(fillValue):
	background = np.zeros((int(cuadritoH*cantCuadritoH), int(cuadritoW*cantCuadritoW)))
	background.fill(fillValue)
	return background

def fillContour(img):
	frame = img.copy()
	# thresh1 = cv2.adaptiveThreshold(frame, 100, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
	_, contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	i = 0
	while len(contours) is not 1:
		i += 1
		# Find biggest contour
		biggestContour = myCV.findBiggestContour(contours)
		cnt = contours[biggestContour]
		cv2.drawContours(frame, cnt, -1, 0, 15)
		contours.pop(biggestContour)
	return frame

def getHandsAndHead(img):
	frame = fillContour(img.copy())
	_, thresh1 = cv2.threshold(frame.copy(), 100, 255, cv2.THRESH_BINARY_INV)
	if showMode:
		cv2.imshow("thresh1", thresh1)
		cv2.waitKey(0)
	_, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	shades = []
	location = []
	frame2 = img.copy()

	(restX, restY, sumX, sumY) = (4, 6, 6, 4)
	i = 0
	while i < 3 and len(contours) is not 1:
		i += 1
		# Find biggest contour
		biggestContour = myCV.findBiggestContour(contours)
		cnt = contours[biggestContour]
		# Bounding points
		(x,y,w,h) = cv2.boundingRect(cnt)

		if y - restY >= 0:
			y -= 10
		if y + h + sumY < img.shape[0]:
			h += 10
		if x - restX >= 0:
			x -= 10
		if x + w + sumX < img.shape[1]:
			w += 10

		# Get new image. Crop original image
		newImage = img[int(y):int(y+h), int(x):int(x+w)]

		# Validation
		if type(newImage) is np.ndarray and newImage.shape[0] > 0 and newImage.shape[1] > 0:
			shades.append(newImage)
			# Get porcentage location
			location.append(( ((x+w+x)/2)/img.shape[1], ((y+h+y)/2)/img.shape[0] ))
			print(newImage.shape)
			if showMode:
				cv2.imshow("newImage", newImage)
				cv2.waitKey(0)
			cv2.destroyWindow("newImage")
				
			contours.pop(biggestContour)

	return shades, location

def setLocationX(x):
	x = int(x * cuadritoW * cantCuadritoW)

	if x >= 0 and x < cuadritoW:
		return 0
	elif x >= cuadritoW and x < cuadritoW*2: 
		return 1
	return 2

def setLocationY(y):
	y = int(y * cuadritoH * cantCuadritoH)

	if y >= 0 and y < cuadritoH: 
		return 0
	elif y >= cuadritoH and y < cuadritoH*2: 
		return 1
	return 2

def setLocationXY(x, y, matrix, locations):
	r, c = setLocationY(y), setLocationX(x)

	if matrix[r*cantCuadritoW + c] is 1:
		xSubtraction = locations[len(locations)-1][0] - locations[0][0]
		ySubtraction = locations[len(locations)-1][1] - locations[0][1]

		if int(xSubtraction) is not int(ySubtraction) :
			if ySubtraction > xSubtraction:
				if r is not cantCuadritoH - 1:
					r += 1
				elif c is not 0: 
					c -= 1
				else:
					c += 1
			else:
				if c is not cantCuadritoW - 1:
					c += 1
				elif r is not 0: 
					r -= 1
				else:
					r += 1
		else:
			r = -1
			c = -1

	matrix[r*cantCuadritoW + c] = 1
	x = cuadritoW*c
	y = cuadritoH*r

	return x, y, matrix

def makeMosaic(img):

	sheri = adjustImage(img.copy())
	
	shapes, location = getHandsAndHead(sheri)
	# head, shapes, location = headShot(shapes, location)
	# location, shapes = sortHands(location, shapes)
	background = makeBackground(Fill.WHITE.value)

	# change shape's size for (cuadritoW * cuadritoH)
	matrix = [0] * 9
	for i in range(0,len(shapes)):
		shapes[i] = resizeImage(shapes[i], cuadritoW, cuadritoH)

		x0, y0 , matrix = setLocationXY(location[i][0], location[i][1], matrix, location)
		if x0 >= 0 and y0 >= 0:
			y1 = y0 + cuadritoH
			x1 = x0 + cuadritoW

			background[int(y0):int(y1), int(x0):int(x1)] = shapes[i]

	# el caco
	# head = myCV.resize(head, cuadritoW, cuadritoH)
	head = np.zeros((int(cuadritoH), int(cuadritoW)))
	background[int(0):int(cuadritoH), int(cuadritoW):int(cuadritoW*2)] = head

	return background

def loadFolder():
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(image_path, fld,'*g')
        files = glob.glob(path)
        for fl in files:
        	frame = cv2.imread(fl)
        	# cv2.imshow("frame", frame)
        	name = os.path.basename(fl)
        	# cv2.waitKey(0)

        	frame = makeMosaic(cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY))

        	if saveMode is True:
	        	path2Save = save_path + '\\' + fld
	        	createFolder(path2Save)
	        	saveImage(name, frame.copy(), path2Save)
	        if showMode is True:
	        	cv2.imshow("resultado", frame)
	        	cv2.waitKey(0)

        	if k == ord("e"):
        		break

        if k == ord("e"):
        	break

loadFolder()