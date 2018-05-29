

date = '13-1-2018'
cameraTypes = ["\\LG", "\\SAMSUNG", ""]
camera = cameraTypes[2]

classesDinamic = ['nombre_450_450']

sources = ["\\Juan", "\\Jesus"]
who = sources[0]
filterName = 'Laplacian\\'

defURLTrain = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'
defURLSave = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\'

train_path = defURLTrain +'imagenes\\' + date + camera + who + filterName +"\\"
# save_path =  defURLSave + 'imagenes\\'+ date + camera + who + filterName + "\\mosaico\\"

# train_path = defURLTrain +'imagenes\\' + date + "\\JuanLaplacian\\0\\"
save_path =  defURLSave + 'imagenes\\'+"mosaico\\train\\"