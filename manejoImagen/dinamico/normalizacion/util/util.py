import cv2
import numpy as np 
import config

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
	newImage = np.zeros((int(config.cuadritoH), int(config.cuadritoW)))
	newImage.fill(config.Fill.WHITE.value)

	# print('tamanio new image')
	# print(newImage.shape)

	# Putting the image in the middle
	x_offset = (width - frame.shape[1])/2
	y_offset = (height - frame.shape[0])/2

	# print(x_offset)
	# print(y_offset)

	newImage[:,:][int(y_offset):int(y_offset+frame.shape[0]), int(x_offset):int(x_offset+frame.shape[1])] = frame

	return newImage

def findBiggestContour(contours):
    indexOfBiggestContour = 1
    sizeOfBiggestContour = 0
    for i in range(0,len(contours)):
        if len(contours[i]) > sizeOfBiggestContour and len(contours[i]) > 0:
            sizeOfBiggestContour = len(contours[i])
            indexOfBiggestContour = i

    return indexOfBiggestContour

def makeBackground(height, width, fillValue):
	background = np.zeros((height, width), dtype=np.uint8)
	background.fill(fillValue)
	return background

