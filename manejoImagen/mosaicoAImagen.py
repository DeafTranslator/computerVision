import cv2
import os
import glob
import numpy as np
import myCV
from enum import Enum

clase = 'bien'
saveMode = {'y':True, 'n':False, '':False}[input('save mode? (y, n): ')]
showMode = {'y':True, 'n':False, '':True}[input('show mode? (y, n): ')]
stepByStep = 0
cantHands = 1

print(saveMode)
print(showMode)

date = '28-1-2018'
cameraTypes = ["\\LG", "\\SAMSUNG"]
camera = cameraTypes[0]

sources = ["\\Juan", "\\Jesus"]
who = sources[1]

filterName = 'Laplacian\\'

defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

image_path = defURLTrain +'imagenes\\' + date + camera + who + filterName + clase + '\\'
save_path =  defURLSave + 'imagenes\\'+ date + camera + who + filterName + clase + '_450_450'

image_path = defURLTrain +'imagenes\\' + date + camera + who + filterName +'0\\'+ clase + '\\'
# save_path =  defURLSave + 'imagenes\\'+ date + who + filterName + '\\0\\'+ clase + '_450_450'

# image_path = defURLTrain +'imagenes\\' + date + "\\MosaicoJesusLaplacian\\jesus\\" +  clase + '\\'
# save_path =  defURLSave + 'imagenes\\'+ date + "\\MosaicoJesusLaplacian\\" + clase + '_450_450'


cantClasses = 34
auxPath = ['450_450', '_', ' ', '']
classes = []

print(image_path)

for i in range(0,cantClasses):
	classes.append(str(i))

class Fill(Enum):
	BLACK = 0
	WHITE = 255

cantCuadritoW = 3
cantCuadritoH = 3

cuadritoW = int(450/cantCuadritoW)
cuadritoH = int(450/cantCuadritoH)

llenar = 0

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

	if frame.shape[1] > width:
		hx = width/frame.shape[1]
		hy = frame.shape[0]*hx
		frame = cv2.resize(frame, (int(width), int(hy)), interpolation = cv2.INTER_CUBIC)
	if frame.shape[0] > height:
		hy = height/frame.shape[0]
		hx = frame.shape[1]*hy
		frame = cv2.resize(frame, (int(hx), int(height)), interpolation = cv2.INTER_CUBIC)

	# Mask
	newImage = np.zeros((int(cuadritoH), int(cuadritoW)))
	newImage.fill(Fill.WHITE.value)

	# print('tamanio new image')
	# print(newImage.shape)

	# Putting the image in the middle
	x_offset = (width - frame.shape[1])/2
	y_offset = (height - frame.shape[0])/2

	# print(x_offset)
	# print(y_offset)

	newImage[:,:][int(y_offset):int(y_offset+frame.shape[0]), int(x_offset):int(x_offset+frame.shape[1])] = frame

	return newImage

def adjustImage(img):
	frame = fillContour(img.copy())
	_, thresh1 = cv2.threshold(frame.copy(), 100, 255, cv2.THRESH_BINARY)
	_, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	# Encuentra el controno de la imagen completa
	biggestContour = myCV.findBiggestContour(contours)
	contours.pop(biggestContour)

	# Find biggest contour (face)
	biggestContour = myCV.findBiggestContour(contours)
	cnt = contours[biggestContour]

	# Bounding points
	(x,y,w,h) = cv2.boundingRect(cnt)
	maxBound = max(w, h)
	newImg = makeBackground(int((maxBound)*cantCuadritoH), int((maxBound)*cantCuadritoW), Fill.WHITE.value)

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

def makeBackground(height, width, fillValue):
	background = np.zeros((height, width), dtype=np.uint8)
	background.fill(fillValue)
	return background

def fillContour(img):
	frame = img.copy()
	_, contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	biggestContour = myCV.findBiggestContour(contours)
	contours.pop(biggestContour)

	i = 0
	while len(contours) > 0:
		i += 1
		# Find biggest contour
		biggestContour = myCV.findBiggestContour(contours)
		cnt = contours[biggestContour]
		cv2.drawContours(frame, cnt, -1, 0, llenar)
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

	biggestContour = myCV.findBiggestContour(contours)
	contours.pop(biggestContour)

	while i < 1 + cantHands and len(contours) is not 0:
		i += 1
		# Find biggest contour
		biggestContour = myCV.findBiggestContour(contours)
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
			if showMode:
				cv2.imshow("newImage", newImage)
				cv2.waitKey(stepByStep)
			cv2.destroyWindow("newImage")
				
			contours.pop(biggestContour)

	return shades, location

def setLocationX(x):
	x = int(x * cuadritoW * cantCuadritoW)

	i = 0
	while i < cantCuadritoW - 1:
		if y >= cuadritoW * i and y < cuadritoW * (i+1):
			return i
	return cuadritoW - 1

	# if x >= 0 and x < cuadritoW:
	# 	return 0
	# if x >= cuadritoW and x < cuadritoW*2: 
	# 	return 1
	# return 2 

def setLocationY(y):
	y = int(y * cuadritoH * cantCuadritoH)

	i = 0
	while i < cantCuadritoH - 1:
		if y >= cuadritoH * i and y < cuadritoH * (i+1):
			return i
	return cuadritoH - 1

	# if y >= 0 and y < cuadritoH: 
	# 	return 0
	# if y >= cuadritoH and y < cuadritoH*2: 
	# 	return 1
	# return 2

def setLocationXY(location, matrix, shapes):

	# toma primera posicion de la imagen original
	r[0], c[0] = setLocationY(location[0][1]), setLocationX(location[0][0])
	matrix[r[0]*cantCuadritoW + c[0]] = (1, (location[0][0], location[0][1]))
	diffInX = 0
	# Guarda posicion en la imagen normalizada 
	x[0] = (cuadritoW*c, diffInX)
	y[0] = (cuadritoH*r, 0)
	# Busqueda de las demas imagenes
	for i in range(1,len(shapes)):
		# toma primera posicion de la imagen original
		r[i], c[i] = setLocationY(location[0][1]), setLocationX(location[0][0])
		diffInX = 0
		# Si exite otra imagen en la misma posicion de la imagen actual se ajusta las posiciones de la imagenes
		if matrix[r[i-1]*cantCuadritoW + c[i-1]][0] is 1:
			# Busca la relacion de posicion de ambas imagenes (derecha o izquierda)
			diffInX = int((location[i][0] - matrix[r[i-1]*cantCuadritoW + c[i-1]][1][0])*1000)
			diffInX /= (abs(diffInX))
			diffInX = int(diffInX)
			# Cambia la orientacion de la imagen anterior 
			x[i-1] = (cuadritoW*c[i-1], diffInX*-1)
		# Guarda posicion en la nueva imagen normalizada 
		matrix[r[i]*cantCuadritoW + c[i] + diffInX] = (1, (location[0][0], location[0][1]))
		x[i] = (cuadritoW*c[i], diffInX)
		y[i] = (cuadritoH*r[i], 0)

	return x, y

def makeMosaic(img):

	sheri = adjustImage(img.copy())
	shapes, location = getShapes(sheri)
	head, shapes, location = getHead(shapes, location)
	# location, shapes = sortHands(location, shapes)
	background = makeBackground(int(cuadritoH*cantCuadritoH), int(cuadritoW*cantCuadritoW), Fill.WHITE.value)

	# change shape's size for (cuadritoW * cuadritoH)
	matrix = [(0, (-1,-1))] * (int(cuadritoW) * int(cuadritoH))
	matrix[1] = (1, (int(cuadritoW + (cuadritoW/2)), int(cuadritoH/2)))

	x, y = setLocationXY(location, matrix, shapes)
	for i in range(0,len(x0)):
		x0 = x[i][0]
		if x[i][1] is not 0:
			x0 = x[i][0] + cuadritoW * x[i][1]
		y0 = y[i][0]
		y1 = y0 + cuadritoH
		x1 = x0 + cuadritoW
		shapes[i] = resizeImage(shapes[i], int(cuadritoW), int(cuadritoH))
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
        	name = os.path.basename(fl)

        	frame = makeMosaic(cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY))

        	if saveMode is True:
	        	path2Save = save_path + '\\' + fld
	        	createFolder(path2Save)
	        	saveImage(name, frame.copy(), path2Save)
	        if showMode is True:
	        	cv2.imshow("resultado", frame)
	        	cv2.waitKey(stepByStep)

        	if k == ord("e"):
        		break

        if k == ord("e"):
        	break

loadFolder()