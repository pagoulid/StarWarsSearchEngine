import sys
import json
import re
import requests
#CheckName , GetData if valid

class StarWars_Search_Engine:
    def __init__(self,args):
        
        
        self.host = 'https://swapi.dev/'
        self.API = {'people':'/api/people/','planets':'/api/planets/'}

        self._CheckArgs(args)
        check = self._CheckName(args[1])

        if(check):
            self.SearchName = args[1]
        else:
            self.SearchName = 'ErrorName'
            self._ForceNotWithYou()

       

        
        
        

        

    ######PUBLIC CLASSES#########
    def Search(self):
        if self.SearchName == 'ErrorName':
            pass
            #raise Exception('Error: Invalid Name')
        else:
            filter = self._SearchFilter()
            link =self.host+self.API['people']+filter
            req=requests.get(link)

            info = json.loads(req.content.decode())# decode gives data in string format -> convert to dict
            
            count = info['count'] # case search returned more than 1 charachter
            info = info['results']# array of dictionaries
            
            


            if count!=0:
                data = []
        
                for i in range(count):
                
                    data.append({'Name':info[i]['name'],'Height':info[i]['height'],'Mass':info[i]['mass'],'Birth Year':info[i]['birth_year']})

                    self._Display(data)

            else:# case not fount any relative match
                self._ForceNotWithYou()
        
             
    ######PRIVATE CLASSES#########
    def _Display(self,results):

        for result in results:

            keys = result.keys()
            vals = result.values()

            for key,val in zip(keys,vals):
                print(key+": "+val+"\n")
            print('\n\n')

    def _CheckArgs(self,args):# check length of args and if 1st arg is search , return name
    
        expr = 1 if (len(args)==2 and args[0]=='search') else 0

        if not expr:
            raise Exception("Given invalid arguments or wrong number of arguments")
        else:
            pass

    def _CheckName(self,SearchName):# not saved in searchName of THIS object yet
        # Restrictions: 
        # if num of spaces in string>2(at least 2 words for a full given name) 
        # If not at least length string -> len(str)>=2 invalid (avoid useless search)
        # if empty invalid


            # Returns true/false if name is valid/invalid due to restrictions

        
        namelength = len(SearchName)
        if   namelength>=2 and namelength<=15:

            words =re.split(' ',SearchName)
            
            spacelength = len(words)-1 # in case of 1 word we have 0 spaces


            if spacelength == 0 or spacelength >=2  :# If 2 or more spaces more , 3 or more words(need at least 2 or None) 

                if spacelength == 0: # we have 1 word
                    return True
                else:

                    return False

            else:
                return True
            
           
        else:
            return False
            
                


    def _SearchFilter(self):
        filter = '?search='+self.SearchName
        return filter

    def _ForceNotWithYou(self):
        print("The force is not with you")

            
    
    



if __name__=="__main__":

    SW = StarWars_Search_Engine(sys.argv[1:])
    SW.Search()
    
    

