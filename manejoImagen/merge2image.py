import cv2
import os
import glob
import numpy as np
import random

train_path ='C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\20-1-2018\\JesusPrewitt\\0\\'
save_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\20-1-2018\\JesusPrewitt\\0\\tuv2'

classTu = ['tu']
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

            merge = np.zeros((int(175), int(450), 1))
            merge.fill(255)
            
            frame[:,:][int(525):int(700), int(0):int(merge.shape[1])] = merge

            cv2.imshow("frame", frame)

            saveImage(name, frame.copy(), save_path, fld, '')
            k = cv2.waitKey(1)
                    
            if k == ord("q"):
                break
        if k == ord("q"):
            break

    print('Terminamo')

readFolder()
