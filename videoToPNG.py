# Convierte videos mp4 a imagenes png.
# Pasos para usar el programa:
# 1. Insertar el path de la carpeta donde esta el video en 'video_path'. 
#    Ej: carpeta "letras" tiene las carpetas "a" y "b" y dentro de esta carpeta estan los videos
# 2. Insertar el path de la carpeta donde se guardaran las imagenes del video en 'save_path'.
# 3. Poner dentro de un arreglo el nombre de la carpeta donde esta el video y asignarlo a 'classes'.
#    Siguiendo el ejemplo serian las carpetas "a" y "b"
# 4. Escriba en la consola python videoToPNG o python3 videoToPNG para ejecutar el codigo. 

import cv2
import os
import glob
import tools
import numpy as np


video_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\videos\\2-11-2017\\Jesus'
save_path =  'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\2-11-2017\\Jesus'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
classesAll = ['2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesDinamic = ['nombre']
classes = classesDinamic

frame = None

k = 0

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def readVideo(video, fld):
    global frame
    cap = cv2.VideoCapture(video) 
    i = 0
    while( cap.isOpened() ) :
        ret,frame = cap.read()

        if ret is not True:
            break
        
        rotated = rotate_bound(frame, 90)
        if i % 60:
            cv2.imshow("frame", rotated)
            name = fld + '_' + str(i)
            tools.saveImage(name, rotated.copy(), save_path, fld, '')
        
        i += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def readFolder():
    global frame
    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(video_path, fld,'*mp4')
        files = glob.glob(path)
        for fl in files:
            readVideo(fl, fld)

            if k == ord("e"):
                break

        if k == ord("e"):
            break

readFolder()
