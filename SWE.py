
import json
import re
from tokenize import Double
import requests
import time
import datetime
from Cache import Cache
from Frame import Frame
import pandas as pd



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
        self.command = ''
        self.TimeExec = time.time() 
        

        

       

        
        
        

        

                        ######PUBLIC CLASSES#########


    def Search(self,args):

        self._CheckArgs(args)
        check = self._CheckName(args[1])

       
            
            
        if not check:
            self._ForceNotWithYou()
            #raise Exception('Error: Invalid Name')
        else:

            self.SearchName = args[1]
            
            self.command = args # To store into DataFrame 

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
                
            data.append({'Name':info[i]['name'],'Height':info[i]['height'],'Mass':info[i]['mass'],'Birth_Year':info[i]['birth_year'],'homeworld':info[i]['homeworld']}) if not FromCache else data.append({'Name':info[i]['Name'],'Height':info[i]['Height'],'Mass':info[i]['Mass'],'Birth_Year':info[i]['Birth_Year'],'homeworld':info[i]['homeworld']})
            
            # InsertInCache
            
            self.CacheHandler.Store(data[i],'people',datetime.datetime.now()) if not FromCache else print("")
           

            
            SearchedNames.append(info[i]['name']) if not FromCache else SearchedNames.append(info[i]['Name'])

            #Get num of Planet 
            NumOfPlanet = self._GetPlanetNum(info[i]['homeworld']) 
            Planets.append(NumOfPlanet)
            
            
        

            
        
            # method to retrieve planetes info 
        
        SearchedPlanets,FromPlanetsCache,CachePlanetsTime=self._GetPlanetesInfo(Planets)#,SearchedNames)# searched planets is a dict of dict
        
            
            
           
        CharOnPlanet={SearchedNames[i]:Planets[i] for i in range(len(SearchedNames))}
                         

        self._Display(data,SearchedPlanets,CharOnPlanet,FromCache,FromPlanetsCache,CacheNameTime,CachePlanetsTime)

    def _Display(self,Nameresults,Planetresults,CharOnPlanet,FromPeopleCache,FromPlanetsCache,CacheNameTime,CachePlanetsTime):# charonplanet-> {names:numofplanet} , planetresults {numofplanet:info}
        name=''
        Firstframe = ''
        Iterframe=''
        count=True # initialize dataframe
        for result in Nameresults:

            keys = result.keys()
            vals = result.values()
            
            # names vis
           
            ######Name DataFrames##########
            if count:
                Firstframe = Frame(keys,vals)
                frame = Firstframe
            else:
                Iterframe = Frame(keys,vals)
                frame=Iterframe
                

            
            frame.Delete('homeworld')
            name = frame.GetVal('Name')



            if FromPeopleCache and self.TimestampOption == 0:
                frame.Insert('NCacheTime',CacheNameTime[name])
                
            else:
                frame.Insert('NCacheTime','None')
            ######Name DataFrames##########
            
            
            
            

            ######Name Display########## (Planet Display on line 214)
            
            for key,val in zip(keys,vals):
                if key=='Name':
                    name=val

                print(key+": "+val+"\n") if key!='homeworld'else print('')

                if FromPeopleCache and self.TimestampOption == 0 and key == 'Birth_Year' :# check key to print cache time on last iter
                    print('\n Cached :'+CacheNameTime[name]+'\n')
            
            ######Name Display##########
            print('---------------')
            
            Plnum = CharOnPlanet[name]
            Plinfo = Planetresults[Plnum] # find matched Planet of person
            ######Planet DataFrames##########
            Plkeys = Plinfo.keys()
            Plvals = Plinfo.values()

            Plframe = Frame(Plkeys,Plvals)

            if FromPlanetsCache:# None from API, else {num:True} or {}
                if FromPlanetsCache!= None and self.TimestampOption == 1:
                    if Plnum in FromPlanetsCache:
                        Plframe.Insert('PCacheTime',CachePlanetsTime[Plnum])
                        
                    else:
                        Plframe.Insert('PCacheTime','None')
                else:
                   Plframe.Insert('PCacheTime','None')

                   
            else:
                Plframe.Insert('PCacheTime','None')

            ######Planet DataFrames##########


            ###Merge Planet and Names Dataframes#######
            
            frame.Insert('PlanetName',Plframe.GetVal('Name')) # insert planetname nad merge planet info
            Plframe.Delete('Name')
            
            frame.Merge(Plframe,1) # Returns a me
            
            #frame.Insert('Search Args',self.command)
            
            del Plframe
            
            if count:
                count=False # use iterframe
            else:
                Firstframe.Merge(Iterframe,0)
            ###Merge Planet and Names Dataframes#######
                
                

            ####Planet Display#######
         
            
            

            print('Name: ' ,Plinfo['Name'])
            print('Population: ' ,Plinfo['Population'])
            print('\n')

            PlanetDays,IsDaysUknown = self._GetEarthTime(Plinfo['Rotation_Period'],24.0)
            PlanetYears,IsYearsUknown = self._GetEarthTime(Plinfo['Orbital_Period'],365.0)
            self._GetDispEarthTime(Plinfo['Name'],PlanetYears,PlanetDays,IsYearsUknown,IsDaysUknown)# must check case years and days are unknown on char's planet
            
            if FromPlanetsCache:# None from API, else {num:True} or {}
                if FromPlanetsCache!= None and self.TimestampOption == 1:
                    if Plnum in FromPlanetsCache:
                        print('\n Cached : '+CachePlanetsTime[Plnum])
            
            ####Planet Display#######
            print('\n\n')
        #Firstframe.Delete('Search Args')
        Time = time.time() -self.TimeExec
        GroupObj=Firstframe.df.groupby(['PlanetName','Name'])#.apply(print)

        print(GroupObj.first()) # ot of loop (Group according to planets) ###CHECKPOINT####
        # output.txt for results , Store... store time and num of searches
        with open('output.txt','a') as O,open('StoreSearchTimeBeforeCleanCache.txt','a') as SST:
            c =0
            for name,group in GroupObj:
                
                if c==0:
                    ds = str(group)
                    ds = ds.split('PCacheTime')
                    f=ds[0] + 'PCacheTime'
                    s=ds[1]
                    s=s.replace('0','')
                    ds = f+'\n'+s
                    
                    c=c+1
                else:
                    ds = str(group).split('PCacheTime')
                    
                    ds=ds[1]
                    ds = ds.replace('0','')
                    
                    c=c+1
                    
               


                    
               
                O.write(ds)
                O.write('\n')
                
                
           
            O.write('\n                   Search Arguments: '+str(self.command))
            O.write('\n\n')
            SST.write(str(Time)+','+str(c)+'\n')
            O.close()
            SST.close()

########DISPLAY FUNCTIONS############
 


#########  VALIDATION FUNCTIONS ##########
    def _CheckArgs(self,args):# check length of args and if 1st arg is search , return name
    
            length = len(args)
            expr = 1 if ((length==2 or length==3) and args[0]=='search') else 0

            if not expr:
                
                if(length==2 and args[0]=='cache'and args[1]=='--clean'):
                    #todo
                    self.CacheHandler.Clear(['people','planets'])


                    ###SST File To Retrieve Info###
                    with open('output.txt','a') as O ,  open('StoreSearchTimeBeforeCleanCache.txt','r') as SST:
                        tsum=0
                        ssum=0
                        lines = SST.readlines()
                        for line in lines:
                            
                            time,search=line.split(',')
                            
                            
                            tsum=tsum+float(time)
                            ssum=ssum+int(search)
                        O.write('\n \t\t Total Number Of Searches :'+str(ssum))
                        O.write('\n \t\t Total Time :'+str(tsum)+' sec\n\n')
                        
                        O.close()
                        SST.close()
                    with open('StoreSearchTimeBeforeCleanCache.txt','w') as WSST:
                        WSST.write('')
                        WSST.close()
                    print('Removed cache')
                    print('\n \t\t Total Number Of Searches :'+str(ssum))
                    print('\n \t\t Total Time :'+str(tsum)+' sec\n\n')

                    exit()
                else:
                    
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
        count,info,CacheNameTime = self.CacheHandler.retrieve(self.SearchName,'people')# CacheTime [] 
        
        if count!=0: # No match from cache
            
            self._InfoDisp(count,info,CacheNameTime,True)
        else:
            print(info)
            self._GetNamesFromAPI()
           

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
                
                
                DictOfDicts[planet]={"Name":Planetinfo['name']+"","Population":Planetinfo['population'] , "Orbital_Period":Planetinfo['orbital_period'],"Rotation_Period":Planetinfo['rotation_period']}
               
                # stored valid people data on search() , already got valid info for planets from people data
                self.CacheHandler.Store(DictOfDicts[planet],'planets',datetime.datetime.now(),planet) if not FromCache else print("")


        return DictOfDicts
    def _GetPlanetesInfoFromCache(self,planets):
        FromCache = {}
        DictOfDicts = {}
        CachePlanetsTime={}
        
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
                     
                        

                     
                
                
                     DictOfDicts[planet]={"Name":Planetinfo['name']+"","Population":Planetinfo['population'] , "Orbital_Period":Planetinfo['orbital_period'],"Rotation_Period":Planetinfo['rotation_period']}
                    # store to cache
                     self.CacheHandler.Store(DictOfDicts[planet],'planets',timestamp=datetime.datetime.now(),PlanetNum=planet)

        
        return DictOfDicts,FromCache,CachePlanetsTime


            
        

    def _GetPlanetesInfo(self,planets):
        DictOfDicts = {}
        FromCache = None # if API return none cache , else return True array or []
        CachePlanetsTime = None
        # ifemptycache
        IsEmptyCache = self.CacheHandler.IsEmpty('planets')
        if IsEmptyCache:
            DictOfDicts=self._GetPlanetesInfoFromAPI(planets)
        else:
            
            DictOfDicts,FromCache,CachePlanetsTime=self._GetPlanetesInfoFromCache(planets)

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
