import cv2
import os
import glob
import numpy as np
import math
import modules.myCV as myCV

date = '13-1-2018'
defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

train_path = defURLTrain +'imagenes\\' + date
video_path = defURLTrain+ 'videos\\'+ date
save_path =  defURLSave + 'imagenes\\'+ date +'\\JuanPrueba2'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['nombre']
classes = classesDinamic

# prueba2
# roiPts = [(310, 228), (322, 148), (303, 195), (331, 189), (380, 229), (393, 173), (365,204), (369,146)]
# prueba
# roiPts = [(312, 283), (374, 278), (377, 197), (322, 202), (307, 250), (374, 242), (354,242)]
# Bien
# roiPts = [(306, 298), (380, 288), (379, 190), (319, 194), (305, 262), (387, 250), (337,247)]
# Bien
roiPts = []
# roiPts = [(142, 428), (156, 459), (171, 425), (217, 438), (181, 448), (215, 460), (296,455), (273,488), (265,455), (250,476) ]

cantPoint = 10


# ROI measure (LO CUADRITO PA COGER LO COLORE)
diamRoi = 0.02

# Text measure
wdTxt = 0.35
hiTxt = 0.2
sizThk = 1
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