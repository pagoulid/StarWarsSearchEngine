import pandas as pd


class Frame:
    def __init__(self,keys,vals):
        self.keys=keys
        self.vals = vals
        self.df = self._CreateFrame()

    def GetVal(self,key):
        return self.df[key][0]
    def Insert(self,newkey,newval):
        self.df[newkey] = [newval]
    def Merge(self,OtherFrame,frameaxis):
        self.df =pd.concat([self.df,OtherFrame.df],axis=frameaxis)
       
    def Delete(self,key):
        del self.df[key]
    def _CreateFrame(self):
        return pd.DataFrame([self.vals],columns=self.keys)

    

