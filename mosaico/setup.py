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

classesDinamic = ['adios']
classes = classesDinamic
	
# SAVE MODE
saveMode = False

# cant ROI
cantPoint = 5

# Bien
roiPts = []

# 12 para "adios" SAMSUNG JESUS 0.015
# roiPts = [(53, 386), (55, 399), (63, 411), (75, 411), (100, 411), (93, 399), (86, 383), (74, 382), (61, 355), (116, 405), (93, 355), (263, 260)]

# ROI measure (LO CUADRITO PA COGER LO COLORE)
diamRoi = 0.023

# Text measure
wdTxt = 1
hiTxt = 1
sizThk = 0.8
font = cv2.FONT_HERSHEY_SIMPLEX

# frame collected to get colors
frameCollected = 20

# 
wdImage = 450
hiImage = 700

# modulus
modulu = 2

#
valueBlur = (25, 25)

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