import cv2
import os
import glob
import numpy as np
import math
import modules.myCV as myCV

date = '28-1-2018'
cameraTypes = ["\\LG", "\\SAMSUNG"]
camera = cameraTypes[1]
defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

train_path = defURLTrain +'imagenes\\' + date
video_path = defURLTrain+ 'videos\\2018\\'+ date + camera
save_path =  defURLSave + 'imagenes\\'+ date + camera +'\\JuanLaplacian_prewitt'

classesDinamic = ['bien']
classes = classesDinamic

# SAVE MODE
saveMode = False

# cant ROI
cantPoint = 8

# Bien
roiPts = []

# 8 para "nombre"
# roiPts = [(233, 144), (259, 137), (284, 196), (220, 193), (127, 418), (354, 436), (360,460), (123,441) ]

# ROI measure (LO CUADRITO PA COGER LO COLORE)
diamRoi = 0.02

# Text measure
wdTxt = 0.35
hiTxt = 0.2
sizThk = 1
font = cv2.FONT_HERSHEY_SIMPLEX

# frame collected to get colors
frameCollected = 12

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
degree = 90