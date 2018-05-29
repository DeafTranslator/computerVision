import cv2
import os
import glob
import numpy as np
import math
from myCV import resize

date = '13-1-2018'
cameraTypes = ["\\LG", "\\SAMSUNG", ""]
camera = cameraTypes[2]

classesDinamic = ['nombre_450_450']

sources = ["\\Juan", "\\Jesus"]
who = sources[0]
filterName = 'Laplacian\\'

defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

train_path = defURLTrain +'imagenes\\' + date + camera + who + filterName +"\\"
# save_path =  defURLSave + 'imagenes\\'+ date + camera + who + filterName + "\\mosaico\\"

# train_path = defURLTrain +'imagenes\\' + date + "\\JuanLaplacian\\0\\"
save_path =  defURLSave + 'imagenes\\'+"mosaico\\train\\"

print(train_path)
classes = classesDinamic

cantClasses = 34
classesNum = []

for i in range(0, cantClasses):
    classesNum.append(str(i))

frame = None

def createFolder(save_path, folder):
    if not os.path.exists(save_path + '\\' + folder):
        os.makedirs(save_path + '\\' + folder)
        print('Folder "', folder,'"created')

def saveImage(name, img, save_path):
    clase = classesDinamic[0]
    clase = clase.split('_')
    clase[0] = clase[0]+"2"
    createFolder(save_path, clase[0])
    print(save_path + clase[0] + '\\' + name +'.png')
    cv2.imwrite(save_path + clase[0] + '\\' +name +'.png', img)

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

            if (len(files) > 0):
                cantFiles = len(files)
                imagesInMosaic = 7.0
                module = int(round((cantFiles / imagesInMosaic), 0))
                
                if  int(round((cantFiles / module), 0)) < imagesInMosaic:
                    module -= 1

                mosaic = []
                row = 0
                for i in range(0, len(files)):
                    if int((i - row) % module) == 0:
                        frame = cv2.imread(files[i])
                        frame = resize(frame, 480, 720)
                        mosaic.append(frame)

                    if math.ceil(cantFiles*1.0 / module) == len(mosaic):
                        row = i+1
                    
                    if len(mosaic) >= imagesInMosaic:
                        break

                mosaic = np.array(mosaic)
                numpy_horizontal_concat = np.concatenate(mosaic, axis=1)
                saveImage(num, numpy_horizontal_concat, save_path)


readFolder()
