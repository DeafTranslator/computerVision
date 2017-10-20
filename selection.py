import cv2
import os
import glob
import tools
import numpy as np
import random
import shutil

train_path ='C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\alpha_newSCrop'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\alpha_newSCrop\\selectwithFlip'

classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']

classes = classesAlph

frame = None
k = 0

def readFolder():
    global frame

    print('Reading image')
    for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
        index = classes.index(fld)
        print('Loading {} files (Index: {})'.format(fld, index))
        path = os.path.join(train_path, fld,'*g')
        files = glob.glob(path)

        images = []
        ids = []

        # Read images
        for fl in files:
            frame = cv2.imread(fl)
            name = os.path.basename(fl)

            # images.append(frame)
            ids.append(name)

            if k == ord("q"):
                break
        
        # images = np.array(images)
        ids = np.array(ids)

        # Population samples
        population = 109
        if len(ids) < population:
            population = len(ids)

        # Take random samples
        r = random.sample(range(len(ids)), population)

        # Move samples
        for i in r:
            print(i)
            src = train_path + '\\' + fld + '\\' + str(ids[i])
            # Train
            tools.createFolder(fld, save_path)
            dst = save_path + '\\' + fld + '\\' + str(ids[i])
            # Test
            # dst = save_path + '\\' + str(ids[i])
            print(src)
            print(dst)  
            shutil.move(src, dst)
            
        # if k == ord("q"):
        #     break

    print('Terminamo')

def readimage():
    global frame
    print('Reading images')
    path = os.path.join(train_path, '*g')
    files = glob.glob(path)
    for fl in files:
        frame = cv2.imread(fl)
        name = os.path.basename(fl)
        frame = tools.resize(frame, 400, 711)
        
        cv2.imshow("frame", frame)

        if k == ord("q"):
            break
        
    print('Terminamo')

readFolder()
