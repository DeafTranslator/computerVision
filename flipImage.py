import cv2
import os
import glob

num = '9'
numl = 'nueve'

train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\tools\\FotoseRacista\\'
save_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\tools\\FotoseRacista\\'
# train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Proyecto\\Dataset\\datasetTODO\\nuevasTrain'
classes = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

print('Reading image')
for fld in classes:   # assuming data directory has a separate folder for each class, and that each folder is named after the class
    index = classes.index(fld)
    print('Loading {} files (Index: {})'.format(fld, index))
    path = os.path.join(train_path, fld,'*g')
    files = glob.glob(path)
    if not os.path.exists(save_path + fld):
    	os.makedirs(save_path + fld)
    	print('Folder', fld, 'not found')
    i = 0
    for fl in files:
    	img=cv2.imread(fl)
    	rimg=cv2.flip(img.copy(),1)
    	name = os.path.basename(fl)
    	name = name.split('.')
    	print(save_path +fld + '\\' + name[0] + '-flip.jpeg')
    	cv2.imwrite(save_path +fld + '\\' + name[0] + '-flip.jpeg', rimg)
    	i += 1

print('Done!')
