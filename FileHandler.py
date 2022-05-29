
import os
class FileHandler:
    def IsDir(self,path):
           

        if os.path.isdir(path):
            pass
            #print("Dir already exists")
        else:
            os.mkdir(path)

    def CreateFile(self,path,filename,data):
        subfolder = path + filename
        os.mkdir(subfolder)
        file = '/'+filename +'.txt'
        with open(subfolder+file,'w') as f:

            f.write(data)