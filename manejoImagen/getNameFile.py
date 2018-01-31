import os
import glob

clase = 'nombre'

train_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\imagenes\\20-1-2018\\JesuMosaico\\jesus\\' + clase

classesAlph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
classesNum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
    '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39']
classesDinamic = ['como']

folders = classesNum

for fld in folders:
    index = folders.index(fld)
    print('Loading {} files (Index: {})'.format(fld, index))
    path = os.path.join(train_path, fld, '*g')
    files = glob.glob(path)
    print('Reading image')

    nameFile =  clase + "_" + str(fld) + ".txt"
    file = open(nameFile, 'w+')

    for fl in files:
        name = os.path.basename(fl)
        name = name.split('.png', 1)

        file.write("{}\n".format(name[0]))

        print(name[0])

    file.close()

print('Done!')
