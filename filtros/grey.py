import cv2
import os
import glob

train_path = 'C:\\Users\\Juan Graciano\\Desktop'
save_path = 'C:\\Users\\Juan Graciano\\Desktop'

def saveImage(name, img, folder = '', create = True):
    name = name.split('.')
    if create:
        createFolder(folder)
        print(save_path+ '\\'+folder+ '\\' + name[0] + '-grey.png')
        cv2.imwrite(save_path + '\\'+folder+'\\'+ name[0] + '-grey.png', img)
    else:
        print(save_path+ '\\' + name[0] + '-grey.png')
        cv2.imwrite(save_path + '\\' + name[0] + '-grey.png', img)

print('Reading image')
path = os.path.join(train_path, '*g')
files = glob.glob(path)
for fl in files:
    img = cv2.imread(fl) 
    name = os.path.basename(fl)
    # frame = cv2.resize(frame, (400, 600), interpolation = cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # cv2.imshow('otputedge',gray)
    saveImage(name, gray, create = False)
    # cv2.waitKey(0)

print('DONE!!!')	
