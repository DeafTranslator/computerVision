import cv2
import os
import glob
import numpy as np
import math
import modules.myCV as myCV

date = '4-3-2018'
cameraTypes = ["\\LG", "\\SAMSUNG"]
camera = cameraTypes[1]

sources = ["\\Juan", "\\Jesus"]
who = sources[1]
filterName = 'Laplacian'

defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

train_path = defURLTrain +'imagenes\\' + date
video_path = defURLTrain+ 'videos\\2018\\'+ date + camera + who
save_path =  defURLSave + 'imagenes\\'+ date + camera + who + filterName

classesDinamic = ['j']
classes = classesDinamic
	
# SAVE MODE
saveMode = True

# cant ROI
cantPoint = 10

# Bien
roiPts = []

# 10 para "adios" SAMSUNG JESUS 0.014
roiPts = [(55, 383), (71, 378), (85, 375), (96, 375), (61, 402), (81, 398), (100, 398), (67, 418), (89, 416), (107, 411)]

# ROI measure (LO CUADRITO PA COGER LO COLORE)
diamRoi = 0.014 

# Text measure
wdTxt = 1
hiTxt = 1
sizThk = 0.8
font = cv2.FONT_HERSHEY_SIMPLEX

# frame collected to get colors
frameCollected = 30

# 
wdImage = 450
hiImage = 700

# modulus
modulu = 2

#
valueBlur = (5, 5)

# Blurry 
blurryLim = 10

# degree of rotation
degree = 0

hands = 2

# depreciacion = costo - valor residual / la vida util

# caja y banco
# inventario
# documento y cuentas por cobrar

# ejercicio 4.7 de flujo de efectivo hay que estudiarlo para el examen