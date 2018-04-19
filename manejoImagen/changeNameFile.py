import os
import glob
import numpy

clase = 'bien'
train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\mosaico\\test\\' + clase + '\\'


path = os.path.join(train_path,'*g')
files = glob.glob(path)
print('Reading image')
counter = 0
print(len(files))
for fl in files:
    print(train_path + clase +'_'+ str(counter)+ '.png')
    os.rename(fl, train_path + clase +'_'+ str(counter)+ '.png')
    counter +=1

print('Done!')