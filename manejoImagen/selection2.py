import cv2
import os
import glob
import myCV
import numpy as np

train_path ='C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\4-3-2018\\SAMSUNG\\JuanLaplacian\\0\\yo'
save_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\4-3-2018\\SAMSUNG\\JuanLaplacian\\M'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']

classes = classesNum

frame = None
k = 0

maxImg = 7

def readimage():
    global frame
    print('Reading images')
    path = os.path.join(train_path, '*g')
    files = glob.glob(path)

    Idxfolder = 0
    sumImg = 0
    for fl in files:
        frame = cv2.imread(fl)
        name = os.path.basename(fl)

        # src = train_path + '\\' + Idxfolder + '\\' + str(name)
        # myCV.createFolder(Idxfolder, save_path)
        myCV.saveImage(name, frame, save_path, str(Idxfolder))

        sumImg += 1
        if sumImg > maxImg:
            Idxfolder += 1
            sumImg = 0

        
    print('Terminamo')

readimage()


