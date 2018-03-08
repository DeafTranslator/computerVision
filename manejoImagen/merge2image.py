import cv2
import os
import glob
import numpy as np
import random


train_path ='C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\28-1-2018\\LG\\JesusLaplacian\\0\\'
save_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\28-1-2018\\LG\\JesusLaplacian\\0\\'

clase = "adios_"
classesNum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
    '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39']

laverdadera = []

for i in range(0, len(classesNum) - 1):
    laverdadera.append(clase + classesNum[i])

classTu = ['bien']
classes = classTu

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
        path = os.path.join(train_path, fld,'*g')
        files = glob.glob(path)
        for fl in files:
            frame = cv2.imread(fl)
            name = os.path.basename(fl)

            merge = np.zeros((int(200), int(450), 1))
            merge.fill(255)
            
            frame[:,:][int(500):int(700), int(0):int(merge.shape[1])] = merge

            cv2.imshow("frame", frame)

            saveImage(name, frame.copy(), save_path, fld, '')
            k = cv2.waitKey(1)
                    
            if k == ord("q"):
                break
        if k == ord("q"):
            break

    print('Terminamo')

readFolder()
