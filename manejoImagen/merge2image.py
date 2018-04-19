import cv2
import os
import glob
import numpy as np
import random

date = '4-3-2018'
cameraTypes = ["\\LG", "\\SAMSUNG"]
camera = cameraTypes[1]

sources = ["\\Juan", "\\Jesus"]
who = sources[1]
filterName = 'Laplacian'

defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

train_path = defURLTrain +'imagenes\\' + date + camera + who + filterName + "\\0\\"
save_path =  defURLSave + 'imagenes\\'+ date + camera + who + filterName + "\\0\\"

classesDinamic = ['z']
classes = classesDinamic

clase = "adios_"

cantClasses = 39
classesNum = []

for i in range(0, cantClasses):
    classesNum.append(str(i))

laverdadera = []

for i in range(0, len(classesNum) - 1):
    laverdadera.append(clase + classesNum[i])


frame = None

def createFolder(letra, save_path):
    if not os.path.exists(save_path + '\\' + letra):
        os.makedirs(save_path + '\\' + letra)
        print('Folder "', letra, '"created')

def saveImage(name, img, save_path, letra, alias = ''):
    createFolder(letra, save_path)

    name = name.split('.')
    if alias is not '':
        alias = '-' + alias
    print(save_path + '\\' + letra + '\\' + name[0] +alias+'.png')
    cv2.imwrite(save_path + '\\' + letra + '\\' + name[0] +alias+'.png', img)

k = 0
def readFolder():
    global frame
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        for num in classesNum:
            path = os.path.join(train_path, fld, num,'*g')
            files = glob.glob(path)
            for fl in files:
                frame = cv2.imread(fl)
                name = os.path.basename(fl)

                hdMerge = 100
                merge = np.zeros((int(hdMerge), int(450), 1))
                merge.fill(255)
                
                frame[:,:][int(700 - hdMerge):int(700), int(0):int(merge.shape[1])] = merge

                cv2.imshow("frame", frame)
                saveImage(name, frame.copy(), save_path, fld +'\\'+ num, '')
                k = cv2.waitKey(1)
                        
                if k == ord("q"):
                    break
            if k == ord("q"):
                break

    print('Terminamo')

readFolder()
