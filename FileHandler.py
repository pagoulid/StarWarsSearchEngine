
import os

class FileHandler:
    def IsDir(self,path,mkdir=True): # if dir not exists , make it
           

        if os.path.isdir(path):

            return True
            #print("Dir already exists")
        else:
            if(mkdir == True):
                os.mkdir(path)
            return False

    
    def IsDirEmpty(self,path):

        dir = os.listdir(path)

    def GetSubDir(self,parent,child):
        path = parent+'/'+child
        return path
  
    # Checking if the list is empty or not
        if len(dir) == 0:
            
            return True
        else:
    
            return False
    def ListDir(self,parent):
        ParentPath = './'+parent+'/'
        FileList = os.listdir(ParentPath)

        return FileList # array with folder names or filename



    def CreateFile(self,path,filename,data):
        subfolder = path + filename
        os.mkdir(subfolder)
        file = '/'+filename +'.txt'
        with open(subfolder+file,'w') as f:

            f.write(data)

    
