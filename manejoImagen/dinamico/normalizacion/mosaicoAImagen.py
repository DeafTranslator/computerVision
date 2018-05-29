import cv2
import os
import glob
import numpy as np
import util.util as util
import config

k = 0

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

def adjustImage(img):
	frame = fillContour(img.copy())
	_, thresh1 = cv2.threshold(frame.copy(), 100, 255, cv2.THRESH_BINARY)
	_, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	# Encuentra el controno de la imagen completa
	biggestContour = util.findBiggestContour(contours)
	contours.pop(biggestContour)

	# Find biggest contour (face)
	biggestContour = util.findBiggestContour(contours)
	cnt = contours[biggestContour]

	# Bounding points
	(x,y,w,h) = cv2.boundingRect(cnt)
	maxBound = max(w, h)
	newImg = util.makeBackground(int((maxBound)*config.cantCuadritoH), int((maxBound)*config.cantCuadritoW), config.Fill.WHITE.value)

	height = newImg.shape[0]
	if img.shape[0]-y < height:
		height = img.shape[0]-y

	width = newImg.shape[1]
	if img.shape[1] < width:
		width = img.shape[1]

	x -= maxBound 
	if x-maxBound < 0:
		x = 0

	deff = (newImg.shape[1] - width)/2
	newImg[int(0):int(height), int(deff):int(deff + width)] = img[int(y):int(height+y), int(0):int(width)]

	return newImg

def getHead(shapes, location):
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

def fillContour(img):
	frame = img.copy()
	_, contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	biggestContour = util.findBiggestContour(contours)
	contours.pop(biggestContour)

	i = 0
	while len(contours) > 0:
		i += 1
		# Find biggest contour
		biggestContour = util.findBiggestContour(contours)
		cnt = contours[biggestContour]
		cv2.drawContours(frame, cnt, -1, 0, config.llenar)
		contours.pop(biggestContour)
	return frame

def getShapes(img):
	frame = fillContour(img.copy())
	_, thresh1 = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)
	_, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	shades = []
	location = []
	frame2 = img.copy()

	(restX, restY, sumX, sumY) = (0, 0, 0, 0)
	i = 0

	biggestContour = util.findBiggestContour(contours)
	contours.pop(biggestContour)

	while i < 1 + config.cantHands and len(contours) is not 0:
		i += 1
		# Find biggest contour
		biggestContour = util.findBiggestContour(contours)
		cnt = contours[biggestContour]
		# Bounding points
		(x,y,w,h) = cv2.boundingRect(cnt)

		if y - restY >= 0:
			y -= restY
		if y + h + sumY < img.shape[0]:
			h += sumY
		if x - restX >= 0:
			x -= restX
		if x + w + sumX < img.shape[1]:
			w += sumX

		# Get new image. Crop original image
		newImage = img[int(y):int(y+h), int(x):int(x+w)]

		# Validation
		if type(newImage) is np.ndarray and newImage.shape[0] > 0 and newImage.shape[1] > 0:
			shades.append(newImage)
			# Get porcentage location
			location.append(( ((x+w+x)/2)/img.shape[1], ((y+h+y)/2)/img.shape[0] ))
			# print(newImage.shape)
			if config.showMode:
				cv2.imshow("newImage", newImage)
				cv2.waitKey(config.stepByStep)
			cv2.destroyWindow("newImage")
				
			contours.pop(biggestContour)

	return shades, location

def setLocationX(x):
	x = int(x * config.cuadritoW * config.cantCuadritoW)
	lastPos = 0 
	porcentage = 0.6
	for i in range(0,config.cantCuadritoW - 1):
		height = config.cuadritoW * porcentage
		if (x >= lastPos)  and x < lastPos + height:
			return i
		lastPos += height
		porcentage = (2 * (1 - porcentage)) + 1
	return config.cantCuadritoW - 1

def setLocationY(y):
	y = int(y * config.cuadritoH * config.cantCuadritoH)
	lastPos = 0 
	height = config.cuadritoH
	for i in range(0,config.cantCuadritoH - 1): 
		# height = max(cuadritoH, (min(1, i) * 1.895 * cuadritoH))
		if (y >= lastPos)  and y < lastPos + height:
			return i
		lastPos += height
		height = 1.895 * config.cuadritoH
	return config.cantCuadritoH - 1

def setLocationXY(location, matrix):

	# # toma primera posicion de la imagen original
	r, c, x, y = [],[],[],[]
	# r.append(setLocationY(location[0][1])) 
	# c.append(setLocationX(location[0][0]))
	# matrix[r[0]*config.cantCuadritoW + c[0]] = (1, (location[0][0], location[0][1]))
	# diffInX = 0
	# # Guarda posicion en la imagen normalizada 
	# x.append((config.cuadritoW*c[0]))
	# y.append((config.cuadritoH*r[0]))
	
	# Busqueda de las demas imagenes
	for i in range(0,len(location)):
		# toma primera posicion de la imagen original
		r.append(setLocationY(location[i][1])) 
		c.append(setLocationX(location[i][0]))
		diffInX = 0
		# Si exite otra imagen en la misma posicion de la imagen actual se ajusta las posiciones de la imagenes
		x.append((config.cuadritoW*c[i]))
		y.append((config.cuadritoH*r[i]))

		if matrix[r[i]*config.cantCuadritoW + c[i]][0] is 1:
			# Busca la relacion de posicion de ambas imagenes (derecha o izquierda)
			diffInX = int((location[i][0] - matrix[r[i-1]*config.cantCuadritoW + c[i-1]][1][0])*1000)
			diffInX /= (abs(diffInX))
			diffInX = int(diffInX)
			# Cambia la orientacion de la imag
			# en anterior 
			x[i-1] = (config.cuadritoW*c[i-1] + ((diffInX*-1) * (config.cuadritoW/2)) )
			x[i] = (config.cuadritoW*c[i] + ((diffInX) * (config.cuadritoW/2)) )
		# Guarda posicion en la nueva imagen normalizada 
		matrix[r[i]*config.cantCuadritoW + c[i]] = (1, (location[i][0], location[i][1]))	

	return x, y

def makeMosaic(img):
	background = util.makeBackground(int(config.cuadritoH*config.cantCuadritoH), int(config.cuadritoW*config.cantCuadritoW), config.Fill.WHITE.value)
	sheri = adjustImage(img.copy())
	shapes, location = getShapes(sheri)
	head, shapes, location = getHead(shapes, location)
	
	if len(location) is 0:
		return background
	
	location, shapes = sortHands(location, shapes)
	
	# change shape's size for (cuadritoW * cuadritoH)
	matrix = [(0, (-1,-1))] * (int(config.cantCuadritoW) * int(config.cantCuadritoH))
	matrix[1] = (1, (0, 0))
	
	x, y = setLocationXY(location, matrix)
	for i in range(0,len(x)):
		x0 = x[i]
		y0 = y[i]
		y1 = y0 + config.cuadritoH
		x1 = x0 + config.cuadritoW
		shapes[i] = util.resizeImage(shapes[i], int(config.cuadritoW), int(config.cuadritoH))
		background[int(y0):int(y1), int(x0):int(x1)] = shapes[i]

	# el caco.resize(head, cuadritoW, cuadritoH)
	head = np.zeros((int(config.cuadritoH), int(config.cuadritoW)))
	background[int(0):int(config.cuadritoH), int(config.cuadritoW):int(config.cuadritoW*2)] = head

	return background

def loadFolder():
    print('Reading image')
    for fld in config.classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = config.classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(config.image_path, fld,'*g')
        files = glob.glob(path)
        for fl in files:
        	frame = cv2.imread(fl)
        	name = os.path.basename(fl)

        	frame = makeMosaic(cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY))

        	if config.saveMode is True:
	        	path2Save = config.save_path + '\\' + fld
	        	util.createFolder(path2Save)
	        	util.saveImage(name, frame.copy(), path2Save)
	        if config.showMode is True:
	        	cv2.imshow("resultado", frame)
	        	cv2.waitKey(config.stepByStep)

        	if k == ord("e"):
        		break

        if k == ord("e"):
        	break

loadFolder()