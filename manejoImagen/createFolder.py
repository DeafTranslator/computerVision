import os

save_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\videos\\29-10-2017\\Mirta'

folders = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# folders = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

print('Reading image')
for fld in folders:   
    index = folders.index(fld)
    print('Loading {} files (Index: {})'.format(fld, index))
    if not os.path.exists(save_path + fld):
    	os.makedirs(save_path + "\\" + fld)
    	print('Folder "', fld, '"created')
    	