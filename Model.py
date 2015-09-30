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
        
#############
#############
# Pull Data #
#############
#############

import tushare as ts
import os 
os.chdir('C:/Users/zklnu66/Desktop')

#################
#  Fundamentals #
#################

# Industry, PE, Outstanding, PB, TimeToMarket, Concept

StockInfo = ts.get_stock_basics()
StockInfo = StockInfo.set_index('code')
StockInfo = StockInfo.drop(['name', 'area', 'totals', 'totalAssets', 'liquidAssets', \
    'fixedAssets', 'reserved', 'reservedPerShare', 'eps', 'bvps'], axis = 1)

# Concept
Concept = ts.get_concept_classified()
Concept = Concept.set_index('code')
Concept = Concept.rename(columns = {'c_name': 'concept'})
Concept = Concept.drop('name', axis = 1)
# TODO Load Concept Mapping from local drive
# concept_translation = 

# Merge
StockInfo = pd.merge(StockInfo, Concept, how = 'outer', on = 'code')

# get all stocks
StockName = StockInfo['code']
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

#################
# Fund Holdings #
#################

# TODO Data is available quarterly
FundHolding = ts.fund_holdings(CURRENT.year, np.floor((CURRENT.month+2)/3))


####################
# Financial Report #
####################

# FinancialReport: EPS, EPS_YOY, ROE, EPCF (cash flow per share),net_profits, profits_yoy
# ProfitData: ROE, net_profit_ratio, gross_profit_rate, EPS, bips (business income per share)
# GrowthData: mbrg (main business rate growth), nprg (net profit), 
#             nav, targ (total asset), epsg, seg (shareholder's eqty)
# DebtPayingData: currentratio, quickratio, cashratio, icratio (interest coverage)


# TODO Data is available quarterly
# TODO Compare data for FinancialReport and ProfitData

FinancialData = ts.get_report_data(CURRENT.year, np.floor((CURRENT.month+2)/3))
FinancialData = FinancialData.drop(['name', 'bvps', 'distrib', 'report_date'], axis = 1)

ProfitData = ts.get_profit_data(CURRENT.year, np.floor((CURRENT.month+2)/3))
ProfitData = ProfitData.drop(['name', 'bvps', 'distrib', 'report_date'], axis = 1)

GrowthData = ts.get_growth_data(CURRENT.year, np.floor((CURRENT.month+2)/3))
GrowthData = GrowthData.drop(['name'], axis = 1)

DebtPayingData = ts.get_debtpaying_data(CURRENT.year, np.floor((CURRENT.month+2)/3))
DebtPayingData = DebtPayingData.drop(['name', 'sheqratio', 'adratio'], axis = 1)

# Merging data
for subtab in [FinancialData, ProfitData, GrowthData, DebtPayingData]:
    StockInfo = pd.merge(StockInfo, subtab, how = 'outer', on = 'code')

# Saving data
StockInfo = StockInfo.to_csv('./ASHR/DATA/StockInfo.csv', index = False)

################
##   Trade    ##
################


def WriteExcel(writer, sheet, df, index = False, header = True):
    # Example: writer = pd.ExcelWriter('./ASHR/DATA/test.xlsx')
    df.to_excel(writer, sheet, index = index, header = header)
    writer.save()

def ReadExcel(file, sheetname):
    # Example: file = pd.ExcelFile('./ASHR/DATA/test.xlsx')
    # read the sheet from the excel file
    df = file.parse(sheetname)
    return df
    
def main():
    # Example
    df = pd.DataFrame({'a':[1,2,4,5,9],'b':[2,3,1,6,15], 'c':[3,4,10,8,17]})
    df2 = pd.DataFrame({'a':[1,2,4,5,9],'bb':['a','b','c','d','e'], 'c':[3,4,10,8,18]})
