import os
import glob
import shutil

train_path = 'C:\\Users\\Juan Graciano\\Desktop\\Nati videos\\juan\\numero2\\cropV1'
classesNum = ['0','1','2','3','4','5','6','7','8','9']
folders = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
folders= ['0','1','2','3','4','5','6','7','8','9']

# for fld in folders:
#     index = folders.index(fld)
#     print('Loading {} files (Index: {})'.format(fld, index))
#     path = os.path.join(train_path, fld,'*g')
#     files = glob.glob(path)
#     print('Reading image')
#     counter = 0;
#     for fl in files:
#     	name = os.path.basename(fl)
#     	# name = name.split('Tapecrop', 1)
#     	print(train_path + '\\' + fld + '\\'+ fld +'-'+ str(counter) +'-Tapecrop'+'.png')
#     	# os.rename(fl, train_path + '\\' + fld + '\\'+ fld +'-'+ str(counter) +'-Tapecrop'+'.png')
#     	shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
#     	# counter +=1
# print('Done!')

# src = train_path +'\\'+ str(ids[i])
src = "C:\\Users\\Juan Graciano\\Desktop\\Nati videos\\cannyRandom\\train\\9 001-sC-CT-CH-CNY-rc-.png"
dst = "C:\\Users\\Juan Graciano\\Desktop\\Nati videos\\cannyRandom\\train\\vaina\\9 001-sC-CT-CH-CNY-rc-.png"
print(src)
print(dst)  
shutil.move(src, dst)
