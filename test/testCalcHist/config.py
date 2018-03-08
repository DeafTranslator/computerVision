import cv2
import os
import glob
import numpy as np
import math
import modules.myCV as myCV

date = '28-1-2018'
cameraTypes = ["\\LG", "\\SAMSUNG"]
camera = cameraTypes[0]
defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

train_path = defURLTrain +'imagenes\\' + date
video_path = defURLTrain+ 'videos\\2018\\'+ date + camera
save_path =  defURLSave + 'imagenes\\'+ date + camera +'\\JesusLaplacian'

classesDinamic = ['bien']
classes = classesDinamic
	
# SAVE MODE
saveMode = False

# cant ROI
cantPoint = 7

# Bien
roiPts = []

# 12 para "bien" LG JESUS
roiPts = [(218, 384), (210, 394), (202, 402), (194, 411), (190, 423), (210, 236), (242, 271)]

# ROI measure (LO CUADRITO PA COGER LO COLORE)
diamRoi = 0.016

# Text measure
wdTxt = 1
hiTxt = 1
sizThk = 0.8
font = cv2.FONT_HERSHEY_SIMPLEX

# frame collected to get colors
frameCollected = 15

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

hands = 2