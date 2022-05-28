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
            info = self._GetInfo(link)
            #req=requests.get(link)

            #info = json.loads(req.content.decode())# decode gives data in string format -> convert to dict
            
            count = info['count'] # case search returned more than 1 charachter
            info = info['results']# array of dictionaries
            
            

            
            if count!=0:

                self._InfoDisp(info,count)
                
                

            else:# case not fount any relative match
                self._ForceNotWithYou()
        
             
                             ######PRIVATE CLASSES#########

    

########DISPLAY FUNCTIONS############
    def _InfoDisp(self,info,count):
        
        data = []
        Planets = []
        SearchedNames = [] 
        
        for i in range(count):
                
            data.append({'Name':info[i]['name'],'Height':info[i]['height'],'Mass':info[i]['mass'],'Birth Year':info[i]['birth_year']})

            # method to retrieve planetes info 
              #self._Planetes(info[i]['name'],info[i]['homeworld']) # line 146
            NumOfPlanet = self._GetPlanetNum(info[i]['homeworld']) 

           
            Planets.append(NumOfPlanet)
            SearchedNames.append(info[i]['name'])
        

        SearchedPlanets=self._GetPlanetesInfo(Planets,SearchedNames)# searched planets is a dict of dict
            
            
           
        CharOnPlanet={SearchedNames[i]:Planets[i] for i in range(len(SearchedNames))}                  

        self._Display(data,SearchedPlanets,CharOnPlanet)

    def _Display(self,Nameresults,Planetresults,CharOnPlanet):# charonplanet-> {names:numofplanet} , planetresults {numofplanet:info}
        name=''
        for result in Nameresults:

            keys = result.keys()
            vals = result.values()

            for key,val in zip(keys,vals):
                if key=='Name':
                    name=val

                print(key+": "+val+"\n")
            
            
            print('---------------')
            Plnum = CharOnPlanet[name]
            Plinfo = Planetresults[Plnum] 

            print('Name: ' +Plinfo['Name'])
            print('Population: ' +Plinfo['Population'])
            print('\n')

            PlanetDays,IsDaysUknown = self._GetEarthTime(Plinfo['Rotation Period'],24.0)
            PlanetYears,IsYearsUknown = self._GetEarthTime(Plinfo['Orbital Period'],365.0)
            self._GetDispEarthTime(Plinfo['Name'],PlanetYears,PlanetDays,IsYearsUknown,IsDaysUknown)# must check case years and days are unknown on char's planet
            
            print('\n\n')


########DISPLAY FUNCTIONS############
 


#########  VALIDATION FUNCTIONS ##########
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
            
#########  VALIDATION FUNCTIONS ##########  

######GETTERS#######



    def _GetPlanetesInfo(self,planets,names):
        DictOfDicts = {}
        for planet,name in zip(planets,names):
            

            if planet in DictOfDicts:
                pass

            else:
                link = self.host+self.API['planets']+planet
                Planetinfo = self._GetInfo(link)
                
                DictOfDicts[planet]={'Name':Planetinfo['name'],'Population':Planetinfo['population'] , 'Orbital Period':Planetinfo['orbital_period'],'Rotation Period':Planetinfo['rotation_period']}

        return DictOfDicts

    def _GetInfo(self,URL):
        req = requests.get(URL)
        info = json.loads(req.content.decode())
        return info
    def _GetPlanetNum(self,PlanetLink):

        num = PlanetLink.split('/',5)
        num =  num[len(num)-1] # because last element is x/ 
        num = num[:len(num)-1]
        print(num)

        return num

    def _GetEarthTime(self,PlanetTime,EarthTime):# returns planet time analogous to earth time and , if planet time is known
        IsUknown = False
        if PlanetTime != 'unknown':
            PlanetTime = float(PlanetTime) # earth time is already float
            res = PlanetTime/EarthTime
        else:
            res = 'unknown'
            IsUknown=True
        
        
        return res,IsUknown

    def _GetDispEarthTime(self,planet,years,days,years_unknown,days_unknown):

        

        if years_unknown and days_unknown:
            print('On {} 1 year on Earth  is uknown years and 1 day unknown days'.format(planet))
        else:

            if years_unknown :
                print('On {} 1 year on Earth  is uknown years and 1 day {:.2f} days'.format(planet,days))
            elif days_unknown:

                print('On {} 1 year on Earth  is {:.2f} years and 1 day unknown days'.format(planet,years))
            else:
                print('On {} 1 year on Earth  is {:.2f} years and 1 day {:.2f} days'.format(planet,years, days))








######GETTERS####### 


    def _SearchFilter(self):
        filter = '?search='+self.SearchName
        return filter

    def _ForceNotWithYou(self):
        print("The force is not with you")

    


            
    
    



if __name__=="__main__":

    SW = StarWars_Search_Engine(sys.argv[1:])
    SW.Search()
    
    

