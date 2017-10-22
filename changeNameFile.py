import os
import glob

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\20-10-2017\\Samuel\\canny_WB'
classesNum = ['0','1','2','3','4','5','6','7','8','9']
folders = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# folders= ['0','1','2','3','4','5','6','7','8','9']

for fld in folders:
    index = folders.index(fld)
    print('Loading {} files (Index: {})'.format(fld, index))
    path = os.path.join(train_path, fld,'*g')
    files = glob.glob(path)
    print('Reading image')
    counter = 0;
    for fl in files:
    	name = os.path.basename(fl)
    	name = name.split('.png', 1)
    	print(train_path + '\\' + fld + '\\'+ name[0] +'-s.png')
    	os.rename(fl, train_path + '\\' + fld + '\\'+ name[0] +'-s.png')
    	counter +=1
print('Done!')