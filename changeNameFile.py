import os
import glob

train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Photos8-7-2017'
folders = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

for fld in folders:
    index = folders.index(fld)
    print('Loading {} files (Index: {})'.format(fld, index))
    path = os.path.join(train_path, fld,'*g')
    files = glob.glob(path)
    idImage = 0
    print('Reading image')
    for fl in files:
    	os.rename(fl, train_path + '\\' + fld + '\\'+ fld+'-'+str(idImage)+'.png')
    	idImage += 1

print('Done!')