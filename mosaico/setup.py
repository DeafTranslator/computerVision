import cv2
import os
import glob
import numpy as np
import math
import modules.myCV as myCV

date = '20-1-2018'
defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

train_path = defURLTrain +'imagenes\\' + date
video_path = defURLTrain+ 'videos\\2018\\'+ date
save_path =  defURLSave + 'imagenes\\'+ date +'\\JesusCanny'

# classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# classesNum = ['0','1','2','3','4','5','6','7','8','9']
# classesAll = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['nombre']
classes = classesDinamic

# SAVE MODE
saveMode = True

# cant ROI
cantPoint = 10

# Bien
roiPts = []

# 10 para "nombre" LG
roiPts = [(72, 450), (85, 461), (87, 483), (70, 470), (52, 467), (339, 448), (359, 448), (369, 469),  (354, 480), (339, 474)]

# ROI measure (LO CUADRITO PA COGER LO COLORE)
diamRoi = 0.02

# Text measure
wdTxt = 0.35
hiTxt = 0.2
sizThk = 1
font = cv2.FONT_HERSHEY_SIMPLEX

# frame collected to get colors
frameCollected = 7

# 
wdImage = 450
hiImage = 700

# modulus
modulu = 2

#
valueBlur = (25, 25)

# Blurry 
blurryLim = 10