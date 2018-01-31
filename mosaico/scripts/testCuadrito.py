import sys
sys.path.append("../..")
from setup import cv2, np

cantCuadritoH = 10
cantCuadritoW = 10

def cuadrito(img, avgOrigImg, sdvOrigImg):

	# Tamanio de los cuadritos
	cuadritoW = img.shape[1]/cantCuadritoW
	cuadritoH = img.shape[0]/cantCuadritoH

	# Llenando roi
	roiPts = []
	x, y, i, j = 0, 0, 0, 0
	while i < 10:
		while j < 10:
			roiPts.append((i*cuadritoW,j*cuadritoH))
			j += 1
		i += 1

	# cuadritos buenos
	desviacionBaja = [[]]
	desviacionAlta = [[]]

	# analizar cuadrito
	for pts in roiPts:
		roiImg1 = img[pts[1]:pts[1]+cuadritoH, pts[0]:pts[0]+cuadritoW, 0]
		roiImg2 = img[pts[1]:pts[1]+cuadritoH, pts[0]:pts[0]+cuadritoW, 1]
		roiImg3 = img[pts[1]:pts[1]+cuadritoH, pts[0]:pts[0]+cuadritoW, 2]

		roiImg1 = roiImg1.reshape(-1)
    	roiImg2 = roiImg2.reshape(-1)
    	roiImg3 = roiImg3.reshape(-1)

    	if np.average(roiImg1) >= (avgOrigImg[0]-sdvOrigImg[0]) and np.average(roiImg1) <= (avgOrigImg[0]+sdvOrigImg[0]):
    		desviacionBaja[0].append(np.average(roiImg1) - np.std(roiImg1))
    		desviacionAlta[0].append(np.average(roiImg1) + np.std(roiImg1))

    	if np.average(roiImg2) >= (avgOrigImg[1]-sdvOrigImg[1]) and np.average(roiImg2) <= (avgOrigImg[1]+sdvOrigImg[1]):
    		desviacionBaja[1].append(np.average(roiImg2) - np.std(roiImg2))
    		desviacionAlta[1].append(np.average(roiImg2) + np.std(roiImg2))

    	if np.average(roiImg3) >= (avgOrigImg[2]-sdvOrigImg[2]) and np.average(roiImg3) <= (avgOrigImg[2]+sdvOrigImg[2]):
    		desviacionBaja[2].append(np.average(roiImg3) - np.std(roiImg3))
    		desviacionAlta[2].append(np.average(roiImg3) + np.std(roiImg3))

	# promedio alto y bajos de los colores (azul, verde y rojo)

	colorBajo, colorAlto = [], []
	for i in range(0,2):
		sumaBaja, sumaAlta = 0, 0

		for num in desviacionBaja[i]:
			sumaBaja += num
		colorBajo[i] = sumaBaja / len(desviacionBaja[i])

		for num in desviacionAlta[i]:
			sumaAlta += num
		colorAlto[i] = sumaAlta / len(desviacionAlta[i])

	return np.array(colorAlto[0], colorAlto[1], colorAlto[2]), np.array(colorBajo[0], colorBajo[1], colorBajo[2])

def inColor(img, avgOrigImg, sdvOrigImg):

	upper, lower = cuadrito(img, avgOrigImg, sdvOrigImg)
	mask = cv2.inRange(img, lower, upper)

	

	res = cv2.bitwise_and(frame,frame, mask= mask)

