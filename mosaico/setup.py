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
save_path =  defURLSave + 'imagenes\\'+ date +'\\Jesus2'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['tu']
classes = classesDinamic

# SAVE MODE
saveMode = True

# Fecha 13-1-2018
# 8 para "nombre"
# roiPts = [(233, 144), (259, 137), (284, 196), (220, 193), (127, 418), (354, 436), (360,460), (123,441) ]
# 6 para "tu"
# roiPts = [(209, 420), (226, 439), (237, 404), (252, 429), (272, 194), (206, 197) ]
# 8 para "como"
# roiPts = [(58, 438), (82, 450), (62, 462), (345, 470), (374, 451), (392, 457), (207, 162), (372, 472)]
# 8 para "nombre" Samsung
# roiPts = [(114, 465), (120, 448), (118, 437), (378, 493), (387, 464), (372, 463), (232,187), (275,110) ]

# Fecha 13-1-2018
# roiPts = [(233, 144), (259, 137), (284, 196), (220, 193), (127, 418), (354, 436), (360,460), (123,441) ]

# Fecha 20-1-2018
# 10 para "nombre" LG
# roiPts = [(72, 450), (85, 461), (87, 483), (70, 470), (52, 467), (339, 448), (359, 448), (369, 469),  (354, 480), (339, 474)]

# 10 para "tu" LG
# roiPts = [(157, 446), (156, 406), (169, 399), (188, 400), (205, 399), (169, 417), (149, 427), (157, 443), (186, 419), (172, 438), (190, 445), (391, 606), (394, 630), (198, 190), (188, 236), (251, 233)]

# 15 para "como" LG
# roiPts = [(42, 433), (55, 432), (67, 434), (80, 441), (48, 448), (66, 451), (289, 431), (303, 423), (314, 420), (328, 417), (316, 437), (158, 193), (192, 237), (209, 237), (180, 192)]


# cant ROI
cantPoint = 10

# Bien
roiPts = []

# 10 para "tu" LG
roiPts = [(157, 446), (156, 406), (169, 399), (188, 400), (205, 399), (169, 417), (149, 427), (157, 443), (186, 419), (172, 438), (190, 445), (391, 606), (394, 630), (198, 190), (188, 236), (251, 233)]


# ROI measure (LO CUADRITO PA COGER LO COLORE)
diamRoi = 0.02

# Text measure
wdTxt = 0.35
hiTxt = 0.2
sizThk = 1
font = cv2.FONT_HERSHEY_SIMPLEX

# frame collected to get colors
frameCollected = 5

# 
wdImage = 450
hiImage = 700

# modulus
modulu = 2

#
valueBlur = (25, 25)

# Blurry 
blurryLim = 15