import cv2
import os
import glob

train_path = 'C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\alpha_newSCrop\\selectwithFlip'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\pepegrillo\\alpha_canny_WB_M\\flip'
save_path = train_path

classesAll = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesAlph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
classesNum = ['0','1','2','3','4','5','6','7','8','9']
especial = ['test']
classes = classesAlph

print('Reading image')
for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
    index = classes.index(fld)
    print('Loading {} files (Index: {})'.format(fld, index))
    path = os.path.join(train_path, fld,'*g')
    files = glob.glob(path)
    if not os.path.exists(save_path +'\\'+ fld):
    	os.makedirs(save_path + "\\" + fld)
    	print('Folder', fld, 'not found')
    i = 0
    for fl in files:
    	img=cv2.imread(fl)
    	rimg=cv2.flip(img.copy(),1)
    	name = os.path.basename(fl)
    	name = name.split('.')
    	print(save_path + '\\' +fld + '\\' + name[0] + '-f.png')
    	cv2.imwrite(save_path + '\\' +fld + '\\' + name[0] + '-f.png', rimg)
    	i += 1

print('Done!')
