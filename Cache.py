
from FileHandler import FileHandler
import json

 
class Cache:

    def __init__(self):
        self.fhandler = FileHandler()
        
    def Store(self,data,spiece,PlanetNum=None):
        path = './'+spiece+'/'
        self.fhandler.IsDir(path)


        
        if PlanetNum==None:
            self.fhandler.CreateFile(path,str(data['Name']),str(data)) 
        else:
            self.fhandler.CreateFile(path,str(PlanetNum),str(data))

       

    def IsEmpty(self,subcache):# subcache is name of cache(e,g, people or planets)
        path = './'+subcache+'/'

        Existcheck = self.fhandler.IsDir(path,False) # cause (path,mkdir) , do not make dir if not exists

        if(Existcheck):# check first if exists dir to check if empty
            Emptycheck = self.fhandler.IsDirEmpty(path)
        else:
            return True

        if(Emptycheck):
            return True
        else:
            return False

    


    def retrieve(self,GivenName,spiece):
        count = 0
        info = []
        FolderList = self.fhandler.ListDir(spiece)
        
        for f in FolderList:

            if GivenName.lower() in f.lower():
                path = self.fhandler.GetSubDir(spiece,f)
                File = self.fhandler.ListDir(path)
                
                #print('./'+path+'/'+File[0])
                with open('./'+path+'/'+File[0],'r') as txt:
                    
                    data =txt.readline()
                    print(data)
                    data=json.loads(data.replace("'",'"'))
                    print("Data: ",data)

                    info.append(data)

                count=count+1



                
            else:

                continue

        return count,info





   

        
        

        


        
        

