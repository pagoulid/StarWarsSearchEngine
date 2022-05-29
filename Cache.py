from genericpath import isdir
from FileHandler import FileHandler
import os
import json 
class Cache:

    def __init__(self):
        self.fhandler = FileHandler()
        

    def StoreInPeople(self,data):
        self.path = './people/'
        self.fhandler.IsDir(self.path)


        self.fhandler.CreateFile(self.path,str(data['Name']),str(data))
       


        

    def StoreInPlanet(self,data):
        self.path='./planets/'
        self.fhandler.IsDir(self.path)
        self.fhandler.CreateFile(self.path,str(data['Name']),str(data))

        
        

        


        
        

