
import json
import re
import requests
import time
import datetime
from Cache import Cache

# Functions :
#   - 1 public Search Function
#   -Display Functions
#   -Validation Funtions
#   -Getters
#   -Other Functions

class StarWars_Search_Engine:
    def __init__(self):
        
        #self.cache={'CachePeople:{}','CachePlanets:{}'}
        self.SearchName = ''
        self.TimestampOption = -1 # 1 for --world else 0
        self.host = 'https://swapi.dev/'
        self.API = {'people':'/api/people/','planets':'/api/planets/'}
        self.CacheHandler = Cache() 
        

        

       

        
        
        

        

                        ######PUBLIC CLASSES#########


    def Search(self,args):

        self._CheckArgs(args)
        check = self._CheckName(args[1])

       
            
            
        if not check:
            self._ForceNotWithYou()
            #raise Exception('Error: Invalid Name')
        else:

            self.SearchName = args[1]

            #Cache checkpoint
            CacheEmpty=self.CacheHandler.IsEmpty('people')



            if CacheEmpty:

               self._GetNamesFromAPI()

            else:

                self._GetNamesFromCache()
                
        

    
                             ######PRIVATE CLASSES#########

    

########DISPLAY FUNCTIONS############
    def _InfoDisp(self,count,info,CacheNameTime = None,FromCache = False):
        
        data = [] # store people info to display (list of dicts)
        Planets = [] # store planets num (arr)
        SearchedNames = [] # store people names (arr)
        
        for i in range(count):
                
            data.append({'Name':info[i]['name'],'Height':info[i]['height'],'Mass':info[i]['mass'],'Birth Year':info[i]['birth_year'],'homeworld':info[i]['homeworld']}) if not FromCache else data.append({'Name':info[i]['Name'],'Height':info[i]['Height'],'Mass':info[i]['Mass'],'Birth Year':info[i]['Birth Year'],'homeworld':info[i]['homeworld']})
            
            # InsertInCache
            
            self.CacheHandler.Store(data[i],'people',datetime.datetime.now()) if not FromCache else print("")
           

            
            SearchedNames.append(info[i]['name']) if not FromCache else SearchedNames.append(info[i]['Name'])

            #Get num of Planet 
            NumOfPlanet = self._GetPlanetNum(info[i]['homeworld']) 
            Planets.append(NumOfPlanet)
        

            
        
            # method to retrieve planetes info 
        SearchedPlanets,FromPlanetsCache,CachePlanetsTime=self._GetPlanetesInfo(Planets,SearchedNames)# searched planets is a dict of dict
        #print("DictOfDicts ",SearchedPlanets)
            
            
           
        CharOnPlanet={SearchedNames[i]:Planets[i] for i in range(len(SearchedNames))}                  

        self._Display(data,SearchedPlanets,CharOnPlanet,FromCache,FromPlanetsCache,CacheNameTime,CachePlanetsTime)

    def _Display(self,Nameresults,Planetresults,CharOnPlanet,FromPeopleCache,FromPlanetsCache,CacheNameTime,CachePlanetsTime):# charonplanet-> {names:numofplanet} , planetresults {numofplanet:info}
        name=''
        for result in Nameresults:

            keys = result.keys()
            vals = result.values()

            for key,val in zip(keys,vals):
                if key=='Name':
                    name=val

                print(key+": "+val+"\n") if key!='homeworld'else print('')

                if FromPeopleCache and self.TimestampOption == 0 and key == 'Birth Year' :# check key to print cache time on last iter
                    print('\n Cached :'+CacheNameTime[name]+'\n')
            
            
            print('---------------')
            Plnum = CharOnPlanet[name]
            Plinfo = Planetresults[Plnum] 

            print('Name: ' ,Plinfo['Name'])
            print('Population: ' ,Plinfo['Population'])
            print('\n')

            PlanetDays,IsDaysUknown = self._GetEarthTime(Plinfo['Rotation Period'],24.0)
            PlanetYears,IsYearsUknown = self._GetEarthTime(Plinfo['Orbital Period'],365.0)
            self._GetDispEarthTime(Plinfo['Name'],PlanetYears,PlanetDays,IsYearsUknown,IsDaysUknown)# must check case years and days are unknown on char's planet
            
            if FromPlanetsCache:# None from API, else {num:True} or {}
                if FromPlanetsCache!= None and self.TimestampOption == 1:
                    if Plnum in FromPlanetsCache:
                        print('\n Cached : '+CachePlanetsTime[Plnum])
            print('\n\n')


########DISPLAY FUNCTIONS############
 


#########  VALIDATION FUNCTIONS ##########
    def _CheckArgs(self,args):# check length of args and if 1st arg is search , return name
    
            length = len(args)
            expr = 1 if ((length==2 or length==3) and args[0]=='search') else 0

            if not expr:
                raise Exception("Given invalid arguments or wrong number of arguments")
            else:

                self._SetCacheOptions(length,args)

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

######SETTERS#######
    def _SetCacheOptions(self,length,args):
        if length == 2:
            self.TimestampOption = 0
        else :# length is definetely 3
            if args[2] == '--world':
                self.TimestampOption = 1
            else:
                raise Exception('Invalid Arguments')
        
######SETTERS#######

######GETTERS#######



    def _GetNamesFromAPI(self):
        filter = self._SearchFilter()
        link =self.host+self.API['people']+filter


        # check if  searchname is substring to stored name if cache not empty
        count,info = self._GetInfo(link)# Should check and store in cache
           
            # count in case search returned more than 1 charachter
            # info array of dictionaries
         
        if count!=0:

            self._InfoDisp(count,info)
         
        else:# case not fount any relative match

            self._ForceNotWithYou()


    def _GetNamesFromCache(self):
        #count,info = Cache.retrieve(self.SearchName) returns counter and array of dicts if match else false false
        # if count,info ->  self._InfoDisp(count,info)  else self._GetNamesFromAPI
        count,info,CacheNameTime = self.CacheHandler.retrieve(self.SearchName,'people')# CacheTime [] othe ret var
        
        if count==0: # No match from cache
            self._GetNamesFromAPI()
        else:
            print(info)
            self._InfoDisp(count,info,CacheNameTime,True)

        # check if SearchName is part of Names in Cache and if yes return that names
    def _GetPlanetesInfoFromAPI(self,planets,FromCache=False):
        DictOfDicts={}
        for planet in planets:
            

            if planet in DictOfDicts:
                pass

            else:
                #ifemptycache true or not in cache 
                link = self.host+self.API['planets']+planet
                Planetinfo = self._GetInfo(link)
                
                
                DictOfDicts[planet]={"Name":Planetinfo['name']+"","Population":Planetinfo['population'] , "Orbital Period":Planetinfo['orbital_period'],"Rotation Period":Planetinfo['rotation_period']}
               
                # stored valid people data on search() , already got valid info for planets from people data
                self.CacheHandler.Store(DictOfDicts[planet],'planets',datetime.datetime.now(),planet) if not FromCache else print("")


        return DictOfDicts
    def _GetPlanetesInfoFromCache(self,planets,names):
        FromCache = {}
        DictOfDicts = {}
        CachePlanetsTime={}
        i = 0
        for planet in planets:
                count,info,CachePlanetTime = self.CacheHandler.retrieve(planet,'planets')# CacheTime []
                if count!=0:
                    if planet in DictOfDicts:
                        pass
                    else:
                        DictOfDicts[planet]=info[0]
                        FromCache[planet] = True
                        CachePlanetsTime[planet] = CachePlanetTime[0]
                else:
                     link = self.host+self.API['planets']+planet
                     Planetinfo = self._GetInfo(link)

                     
                
                
                     DictOfDicts[planet]={"Name":Planetinfo['name']+"","Population":Planetinfo['population'] , "Orbital Period":Planetinfo['orbital_period'],"Rotation Period":Planetinfo['rotation_period']}
                    # store to cache
                     self.CacheHandler.Store(DictOfDicts[planet],'planets',PlanetNum=planet)

        
        return DictOfDicts,FromCache,CachePlanetsTime


            
        

    def _GetPlanetesInfo(self,planets,names):
        DictOfDicts = {}
        FromCache = None # if API return none cache , else return True array or []
        CachePlanetsTime = None
        # ifemptycache
        IsEmptyCache = self.CacheHandler.IsEmpty('planets')
        if IsEmptyCache:
            DictOfDicts=self._GetPlanetesInfoFromAPI(planets)
        else:
            DictOfDicts,FromCache,CachePlanetsTime=self._GetPlanetesInfoFromCache(planets,names)

        return DictOfDicts,FromCache,CachePlanetsTime




       

   

    def _GetInfo(self,URL):
        req = requests.get(URL)
        info = json.loads(req.content.decode())

        if 'count' in info: # count,results only in people search , not in planet
            count = info['count']
            info = info['results']
            
            
            
            return count,info 
        else:
            
            
            return info

    def _GetPlanetNum(self,PlanetLink):

        num = PlanetLink.split('/',5)
        num =  num[len(num)-1] # because last element is x/ 
        num = num[:len(num)-1]
        

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
