import os
import glob
import cv2

clase = 'tu'

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\13-1-2018\\JuanEtE\\0\\' + clase
save_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\13-1-2018\\MosaicoJuanLaplacian\\' + clase

text_path = 'C:\\Users\\jgraciano\\Desktop\\TeEnsenia\\computerVision\\manejoImagen\\textos\\juan\\' + clase

classesNum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
    '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39']

folders = classesNum

actualPath = '' 

def saveImage(name, img, save_path, alias = ''):
    name = name.split('.')
    if alias is not '':
        alias = '-' + alias
    print(save_path + '\\' + name[0] +alias+'.png')
    cv2.imwrite(save_path + '\\' + name[0] +alias+'.png', img)

def loadNames(file):
    names = []
    f = open(file, 'r+')
    for line in f:
        names.append(line)
    f.close()
    return names

def createFolder(fl):
    fl = fl.split('.txt')
    global actualPath
    actualPath = save_path + "\\" + fl[0]
    if not os.path.exists(actualPath):
        os.makedirs(actualPath)
        print('Folder "', fl[0], '"created')

def matchImage(imageName, mosaic):
    imageName = imageName.split('.')
    # for 'tuv2'
    # imageName[0] = str(imageName[0]) + '-merge'
    # for anything else
    imageName[0] = str(imageName[0])
    for name in mosaic:
        name = name.split('\n')
        if str(imageName[0]) == str(name[0]):
            print('image \'' + name[0] + '\' was found')
            return True

    return False


def readimage(mosaic):
    global actualPath
    print('Reading images')
    path = os.path.join(train_path, '*g')
    files = glob.glob(path)
    for fl in files:
        frame = cv2.imread(fl)
        name = os.path.basename(fl)

        if matchImage(name, mosaic) is True:
            saveImage(name, frame.copy(), actualPath)

    print('Done!')


def match():
    mosaic = [] 
    path = os.path.join(text_path, '*txt')
    files = glob.glob(path)
    print('Reading text')
    for fl in files:
        mosaic = loadNames(fl)
        print('Number of images in this mosaic: ' + str(len(mosaic)))
        createFolder(os.path.basename(fl))
        readimage(mosaic)
    print('Done!')

match()
print('2x Done!')
