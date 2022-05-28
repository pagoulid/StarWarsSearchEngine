import sys
import requests
#CheckName , GetData if valid
class StarWars_Search_Engine:
    def __init__(self,args):
        self._CheckArgs(args)
        self.SearchName = args[1]


    def _CheckArgs(self,args):# check length of args and if 1st arg is search , return name
    
        expr = 1 if (len(args)==2 and args[0]=='search') else 0

        if not expr:
            raise Exception("Given invalid arguments or wrong number of arguments")
        else:
            pass
            
    
    #def CheckName():



if __name__=="__main__":

    SW = StarWars_Search_Engine(sys.argv[1:])
    print(SW.SearchName)

#s= requests.get("https://swapi.dev/api/people/?search=wa")
#print(s.content)