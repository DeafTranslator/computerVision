from enum import Enum

clase = 'tu'
saveMode = {'y':True, 'n':False, '':False}[input('save mode? (y, n): ')]
showMode = {'y':True, 'n':False, '':False}[input('show mode? (y, n): ')]
stepByStep = 0
cantHands = 1

date = '13-1-2018'
cameraTypes = ["\\LG", "\\SAMSUNG", ""]
camera = cameraTypes[2]

sources = ["\\Juan", "\\Jesus"]
who = sources[0]

filterName = 'Laplacian\\'

defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

image_path = defURLTrain +'imagenes\\' + date + camera + who + filterName + clase + '\\'
save_path =  defURLSave + 'imagenes\\'+ date + camera + who + filterName + clase + '_450_450'

image_path = defURLTrain +'imagenes\\' + date + camera + who + filterName +'0\\'+ clase + '\\'
# save_path =  defURLSave + 'imagenes\\'+ date + who + filterName + '\\0\\'+ clase + '_450_450'

# image_path = defURLTrain +'imagenes\\' + date + "\\MosaicoJesusLaplacian\\jesus\\" +  clase + '\\'
# save_path =  defURLSave + 'imagenes\\'+ date + "\\MosaicoJesusLaplacian\\" + clase + '_450_450'

print(image_path)
cantClasses = 34
auxPath = ['450_450', '_', ' ', '']
classes = []

print(image_path)

for i in range(0,cantClasses):
	classes.append(str(i))

class Fill(Enum):
	BLACK = 0
	WHITE = 255

cantCuadritoW = 3
cantCuadritoH = 3

cuadritoW = int(450/cantCuadritoW)
cuadritoH = int(450/cantCuadritoH)

llenar = 10