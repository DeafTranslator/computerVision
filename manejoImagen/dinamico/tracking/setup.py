import cv2
import os
import glob
import numpy as np
import math
import modules.myCV as myCV

date = '26-5-2018'
cameraTypes = ["\\LG", "\\SAMSUNG"]
camera = cameraTypes[1]

sources = ["\\Juan", "\\Jesus"]
who = sources[0]
filterName = 'Laplacian'

defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

train_path = defURLTrain +'imagenes\\' + date
video_path = defURLTrain+ 'videos\\2018\\'+ date + camera + who
save_path =  defURLSave + 'imagenes\\'+ date + camera + who + filterName

classesDinamic = ['adios']
classes = classesDinamic
	
# SAVE MODE
saveMode = True

# cant ROI
cantPoint = 10

# Bien
roiPts = []

# 10 para "adios" SAMSUNG JUAN 0.024
roiPts = [(113, 98), (97, 126), (122, 129), (90, 159), (118, 164), (90, 187), (102, 206), (235, 36), (260, 32), (283, 99)]

# ROI measure (LO CUADRITO PA COGER LO COLORE)
diamRoi = 0.024 

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

# degree of rotation (0,90)
degree = 0

hands = 2

def enum(**enums):
    return type('Enum', (), enums)

smoothingFilters = enum(AVERAGING = 0,
    GAUSSIAN = 1,
    MEDIAN = 2,
    BILATERAL = 3)


