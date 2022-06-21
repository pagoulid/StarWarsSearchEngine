# StarWarsSearchEngine
A Star Wars search engine consuming  the Star Wars API

# Info
After succesfull response , all entries are stored respectively in  local caches : people cache  for charachters , planet cache for planets
For a given request if a person/planet already exists program loads information from Cache
In file StoreSearchTimeBeforeCleanCache are stored information about the history of the searches

# Exec Commands
Search for character(s) along with respective planet(s) , he/she/they live on : python search '<name>'
  
If planet loaded from cache show additional store time information :  python search '<name>' --world
  
Clean Cache :   python cache --clean           


  
 
 
 
