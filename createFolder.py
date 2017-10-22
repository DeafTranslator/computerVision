import os

save_path = 'C:\\Users\\jgraciano\\Desktop\\Dataset\\videos\\20-10-2017\\Jorge'

folders = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
folders = ['testNohup']

print('Reading image')
for fld in folders:   
    index = folders.index(fld)
    print('Loading {} files (Index: {})'.format(fld, index))
    if not os.path.exists(save_path + fld):
    	os.makedirs(save_path + "\\" + fld)
    	print('Folder "', fld, '"created')
    	