from __future__ import division
import pandas as pd
import numpy as np
import datetime

CURRENT = datetime.datetime.now()

# Indicator
class Indicator():
    
    # Assuming the data type of Data is in pd.DataFrame
    # Note, the index will be the time stamp
    def __init__(self, Data):
        self.DF = Data
        self.length = self.DF.shape[0]
        
    # Stochstic oscillator
    def StochasticOscillator(self, K_Scale, D_Scale, DSlow_Scale):
        '''
        Stochastic oscillator: comparing current price in relation to its price range over a period of time
        Input: 
            /K_Scale/     The time range that we look back to compute K
            /D_Scale/     The number of %K that we look at to compute %D
        NOTE: 
            length of self.K = self.length - K_Scale + 1
            length of self.D = len(self.K) - D_Scale + 1
        
        TODO: D is calculated using SMA of K right now
        '''
        Current = self.DF[K_Scale-1:]
        Low = pd.rolling_min(self.DF, K_Scale)[K_Scale-1:]
        High = pd.rolling_max(self.DF, K_Scale)[K_Scale-1:]
        self.K = 100 * ( Current - Low) / (High - Low)
        
        self.D = pd.rolling_mean(self.K, D_Scale)[D_Scale-1:]
        self.DSlow = pd.rolling_mean(self.D, DSlow_Scale)[DSlow_Scale-1:]
    
        return self.K, self.D, self.DSlow
    
    # Larry William %R
    def WilliamR(self, Scale):
        '''
        Larry William %R: on a negative scale from -100 to 0
        -100: today was lowest low of past N days (oversold)
        '''
        Current = self.DF[Scale-1:]
        Low = pd.rolling_min(self.DF, Scale)[Scale-1:]
        High = pd.rolling_max(self.DF, Scale)[Scale-1:]
        self.WilliamR = -100 * ( High - Current ) / (High - Low)
    
        return self.WilliamR
    
    # 
    

class TradeData():
    
    def __init__(self, Data):
        self.DF = Data
        

# Pull Data
import tushare as ts
import os 
os.chdir('C:/Users/zklnu66/Desktop')

# Industry
StockInfo = ts.get_industry_classified()
StockInfo = StockInfo.rename(columns = {'c_name': 'industry'})
StockInfo = StockInfo.set_index('code')
StockInfo = StockInfo.drop('name', 1)

# Concept
Concept = ts.get_concept_classified()
Concept = Concept.set_index('code')
Concept = Concept.rename(columns = {'c_name': 'concept'})
Concept = Concept.drop('name', 1)
# Load Concept Mapping from local drive
concept_translation = 

# Merge
StockInfo = pd.merge(StockInfo, Concept, how = 'outer', on = 'code')

# get all stocks
StockName = Industry['code']
StockName.to_csv('./ASHR/DATA/StockName.csv', index = False)

# Small & Medium Enterprise
# Note SME is a pd.series data type
SME = ts.get_sme_classified()['code']
SME.to_csv('./ASHR/DATA/SME.csv', index = False)

# Growth Enterprise Market
GEM = ts.get_gem_classified()['code']
GEM.to_csv('./ASHR/DATA/GEM.csv', index = False)

# ST Enterprise
ST = ts.get_st_classified()['code']
ST.to_csv('./ASHR/DATA/ST.csv', index = False)

# HS 300
HS300S = ts.get_hs300s()['code']
HS300S.to_csv('./ASHR/DATA/HS300S.csv', index = False)

# SZ 50
SZ50S = ts.get_sz50s()['code']
SZ50S.to_csv('./ASHR/DATA/SZ50S.csv', index = False)

# ZZ 500
ZZ500S = ts.get_zz500s()['code']
ZZ500S.to_csv('./ASHR/DATA/ZZ500S.csv', index = False)

# Fund Holdings
# TODO Data is available quarterly
FundHolding = ts.fund_holdings(CURRENT.year, np.floor((CURRENT.month+2)/3))


def main():
    # Example
    df = pd.DataFrame({'a':[1,2,4,5,9],'b':[2,3,1,6,15], 'c':[3,4,10,8,17]})
    df2 = pd.DataFrame({'a':[1,2,4,5,9],'bb':['a','b','c','d','e'], 'c':[3,4,10,8,18]})

