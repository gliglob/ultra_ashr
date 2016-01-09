#####################
####             ####
#### Pull Data   ####
####             ####
#####################

import tushare as ts
import pandas as pd
import numpy as np
from HelperFunctions import *
from Config import CONFIG

def CodeWrapper2(series):
    return series.map(lambda x: 'SH'+x if x[0] == '6' else 'SZ'+x)

# Restrict Stock Set to CSI All


############
# Industry #
############

StockList = pd.read_excel(CONFIG.STOCKLISTPATH, header = None, names = ['Ticker'])['Ticker']
StockList = CodeWrapper(StockList)
StockList = StockList.map(lambda x: 'SH' + x if x[0] == '6' else 'SZ' + x)

IndustryList = ['综合行业', '公路桥梁', '化纤行业', '机械行业', '生物制药', '石油行业', '玻璃行业', '仪器仪表', '交通运输', 
 '飞机制造', '农林牧渔', '建筑建材',  '塑料制品', '商业百货', '纺织行业',  '医疗器械', '有色金属', '供水供气', 
 '发电设备', '造纸行业', '船舶制造',  '煤炭行业', '食品行业', '陶瓷行业',  '纺织机械', '钢铁行业', '环保行业', 
 '酿酒行业', '电器行业',  '传媒娱乐', '化工行业', '房地产',  '金融行业', '开发区', 
 '电子信息', '服装鞋类', '电子器件',  '电力行业', '汽车制造', '家具行业', '农药化肥', '酒店旅游',  '水泥行业',
 '物资外贸', '摩托车', '印刷包装', '家电行业']
 
IndustryEnglishList = ['ConsumerDiscretionary', 'Industrials', 'Materials', 'Industrials', 'HealthCare', 'Energy', 'Materials', 
  'Industrials', 'Industrials', 'Industrials', 'ConsumerStaples', 'Materials', 'Materials', 'ConsumerDiscretionary',
  'ConsumerDiscretionary', 'HealthCare', 'Materials', 'Utilities', 'Industrials', 'Materials', 'Industrials',
  'Materials', 'ConsumerStaples', 'Materials', 'Industrials', 'Materials', 'Utilities', 'ConsumerStaples', 
  'ConsumerDiscretionary', 'ConsumerDiscretionary', 'Materials', 'Financials', 'Financials', 'Financials',
  'InformationTechnology', 'ConsumerDiscretionary', 'ConsumerDiscretionary', 'Utilities', 'ConsumerDiscretionary', 
  'ConsumerDiscretionary', 'Materials', 'ConsumerDiscretionary', 'Materials', 'Industrials', 'ConsumerDiscretionary',
  'Materials', 'ConsumerDiscretionary']



IndustryClassified = ts.get_industry_classified()
IndustryClassified = IndustryClassified.drop_duplicates('code')
IndustryClassified['code'] = IndustryClassified['code'].map(lambda x: 'SH'+x if x[0] == '6' else 'SZ'+x)
IndustryClassified = IndustryClassified.set_index('code')

#IndustryClassified[IndustryClassified.code.isin(StockList)]

for i,e in enumerate(IndustryList):
    IndustryClassified['c_name'] = IndustryClassified['c_name'].map(lambda x: IndustryEnglishList[i] if x == e else x)


RestofStock = pd.read_csv('./ASHR/DATA/Index/rest.csv', header = None, index_col = 0, names = ['stock', 'industry'])

# Restrict To Stock List Only
Industry = pd.DataFrame({'Stock': StockList})
Industry['Industry'] = Industry['Stock'].map(lambda x: RestofStock.industry.loc[x] if x in RestofStock.index else IndustryClassified.c_name.loc[x])


Industry.to_csv('./ASHR/DATA/INDEX/INDEX/Industry_csi_all.csv')



#########
# Index #
#########
IndexDict = {'CSI100': 'SH000903', 'CSI200': 'SH000904', 'CSI300': 'SH000300', 'CSI500': 'SH000905', 'CSI1000': 'SH000852', 'CSIALL': 'SH000985'}

#IndexDict = {'CSI100': 'SZ399903', 'CSI200': 'SZ399904', 'CSI500': 'SH000905'}


CSI100 = CodeWrapper2(CodeWrapper(pd.read_excel('./ASHR/DATA/Index/Index/csi100.xls', header = None, names = ['Ticker'])['Ticker']))
CSI200 = CodeWrapper2(CodeWrapper(pd.read_excel('./ASHR/DATA/Index/Index/csi200.xls', header = None, names = ['Ticker'])['Ticker']))

CSI500 = CodeWrapper2(CodeWrapper(pd.read_excel('./ASHR/DATA/Index/Index/csi500.xls', header = None, names = ['Ticker'])['Ticker']))
CSI1000 = CodeWrapper2(CodeWrapper(pd.read_excel('./ASHR/DATA/Index/Index/csi1000.xls', header = None, names = ['Ticker'])['Ticker']))

CSI300 = CodeWrapper2(CodeWrapper(pd.read_excel('./ASHR/DATA/Index/Index/csi300.xls', header = None, names = ['Ticker'])['Ticker']))
CSIALL = CodeWrapper2(CodeWrapper(pd.read_excel('./ASHR/DATA/Index/Index/csi_all.xls', header = None, names = ['Ticker'])['Ticker']))


##########################
# Specify Industry Index #
##########################

# Priority: CSI100 > CSI200 > CSI500 > CSI1000 > CSIALL

Stock = pd.read_csv('./ASHR/DATA/StockList.csv', header = None, names = ['Ticker'])
Stock['Category'] = 'CSIALL'
Stock.ix[(Stock.Ticker.isin(CSI100.values)) & (Stock.Category == 'CSIALL'), 'Category'] = 'CSI100'
Stock.ix[(Stock.Ticker.isin(CSI200.values)) & (Stock.Category == 'CSIALL'), 'Category'] = 'CSI200'
Stock.ix[(Stock.Ticker.isin(CSI500.values)) & (Stock.Category == 'CSIALL'), 'Category'] = 'CSI500'
Stock.ix[(Stock.Ticker.isin(CSI1000.values)) & (Stock.Category == 'CSIALL'), 'Category'] = 'CSI1000'

Stock.to_csv('./ASHR/DATA/StockCategory.csv', index = False)

# CSI300 Industry + CSI800 Industry + CSIALL Industry
# NOTE, CSI300 = CSI100 + CSI200, CSI800 = CSI300 + CSI500
Industry = pd.read_csv('./ASHR/DATA/Index/Index/Industry_csi_all.csv')
Category = pd.read_csv('./ASHR/DATA/StockCategory.csv')
Industry = Industry.set_index('Ticker')
Category = Category.set_index('Ticker')
Category = pd.concat([Category, Industry], axis = 1)
Category['IndustryCategory'] = 'CSIALL'
Category.ix[(Category.Category == 'CSI100') | (Category.Category == 'CSI200'), 'IndustryCategory'] = 'CSI300'
Category.ix[(Category.Category == 'CSI500'), 'IndustryCategory'] = 'CSI800'

Category['IndustryCategory'] += '_' + Category['Industry']

# Industry Index Dict
Category.to_csv('./ASHR/DATA/Index/Index/Industry_Category.csv')



##############################
# Match with Index Component #
##############################
# Use component data pulled from CSI website
directory = './ashr/data/index/index/industryindexcons'
Stock = pd.read_csv('./ASHR/DATA/StockList.csv', header = None, names = ['Ticker'])
Stock['Industry'] = None

for filename in os.listdir(directory):
    Temp = CodeWrapper2(CodeWrapper(pd.read_excel('./ASHR/DATA/Index/Index/IndustryIndexCons/%s'%filename, header = None, names = ['Ticker'])['Ticker']))
    # Note, Confirmed that all industry index data pulled from csi website match with each other and no conflict exists
    Stock['Industry'] = Stock.apply(lambda x: filename[:-4] if x['Ticker'] in Temp.values and (not x['Industry']) else x['Industry'], axis = 1)

# 412 of 2526 CSI ALL stocks are not included
Stock.to_csv('./ASHR/DATA/Index/Index/Industry_Confirmed.csv', index = False)

# Combine with sina or hand coded data
Industry = pd.read_csv('./ASHR/DATA/Index/Index/Industry_Confirmed.csv')
Industry.ix[~pd.isnull(Industry.Industry) & (Industry.Industry.str.startswith('CSI500')), 'Industry'] = 'CSI800' + Industry.Industry.str[6:]
Industry.ix[~pd.isnull(Industry.Industry) & (Industry.Industry.str.startswith('CSI1000')), 'Industry'] = 'CSIALL' + Industry.Industry.str[7:]

Industry.to_csv('./ASHR/DATA/Index/Index/Industry_Confirmed.csv', index = False)

Industry_sina = pd.read_csv('./ASHR/DATA/Index/Index/Industry_Category_csi_all.csv')
Industry['Industry'] = Industry.apply(lambda x: Industry_sina.Industry.loc[x['Ticker']] if not x['Industry'] else x['Industry'])
Industry.ix[pd.isnull(Industry.Industry), 'Industry'] = Industry_sina.ix[pd.isnull(Industry.Industry), 'IndustryCategory']

Industry.to_csv('./ASHR/DATA/Index/Index/Industry_Confirmed_csi_all.csv', index = False)

###############
# Map to Code #
###############
IndustryIndex = pd.read_csv('./ASHR/DATA/Index/Index/Industry_Confirmed_csi_all.csv')
CodeMapping = pd.read_csv('./ASHR/DATA/Index/Index/Industry_Category_to_Code.csv')
IndustryIndex = pd.merge(IndustryIndex, CodeMapping, on = 'Industry')
IndustryIndex.to_csv('./ASHR/DATA/Index/Index/IndustryIndex.csv', index = False)

#############
# Map Index #
#############
Index = pd.read_csv('C:/Users/zklnu66/Desktop/ASHR/DATA/Index/IndustryIndex.csv')
def CodeMap(code):
    if code == 'CSI300':
        return 'SH000300'
    elif code == 'CSI800':
        return 'SH000906'
    elif code == 'CSIALL':
        return 'SH000985'

Index['Code'] = Index['Industry'].map(lambda x: CodeMap(x[:6]))
Index.to_csv('C:/Users/zklnu66/Desktop/ASHR/DATA/Index/IndexMap.csv', index = False)

#################
#  Fundamentals #
#################

# Industry, PE, Outstanding, PB, TimeToMarket, Concept

StockInfo = ts.get_stock_basics()
StockInfo = StockInfo.drop(['name', 'area', 'totals', 'totalAssets', 'liquidAssets', \
    'fixedAssets', 'reserved', 'reservedPerShare', 'esp', 'bvps'], axis = 1)

# Concept
#Concept = ts.get_concept_classified()
#Concept = Concept.set_index('code')
#Concept = Concept.rename(columns = {'c_name': 'concept'})
#Concept = Concept.drop('name', axis = 1)


# Merge
#StockInfo1 = StockInfo.join(Concept, how = 'outer')

# get all stocks
StockName = StockInfo['name']
StockName.to_csv('./ASHR/DATA/StockName.csv', index = True, header = True)

# Small & Medium Enterprise
# Note SME is a pd.series data type
SME = ts.get_sme_classified()
SME.to_csv('./ASHR/DATA/SME.csv', index = False)

# Growth Enterprise Market
GEM = ts.get_gem_classified()
GEM.to_csv('./ASHR/DATA/GEM.csv', index = False)

# ST Enterprise
ST = ts.get_st_classified()
ST.to_csv('./ASHR/DATA/ST.csv', index = False)

ts.get_h_data()

# HS 300
HS300S = ts.get_hs300s()
HS300S.to_csv('./ASHR/DATA/HS300S.csv', index = False)

# SZ 50
SZ50S = ts.get_sz50s()
SZ50S.to_csv('./ASHR/DATA/SZ50S.csv', index = False)

# ZZ 500
ZZ500S = ts.get_zz500s()
ZZ500S.to_csv('./ASHR/DATA/ZZ500S.csv', index = False)

#################
# Fund Holdings #
#################

# TODO Data is available quarterly
FundHolding = ts.fund_holdings(CURRENT.year, np.floor((CURRENT.month+2)/3))


####################
# Financial Report #
####################

# FinancialReport: EPS, EPS_YOY, ROE, net_profits, profits_yoy
# ProfitData: ROE, net_profit_ratio, gross_profit_rate, EPS, bips (business income per share)
# GrowthData: mbrg (main business rate growth), nprg (net profit), 
#             nav, targ (total asset), epsg, seg (shareholder's eqty)
# DebtPayingData: currentratio, quickratio, cashratio, icratio (interest coverage)


# TODO Data is available quarterly
# TODO Compare data for FinancialReport and ProfitData

FinancialData = ts.get_report_data(CURRENT.year, np.floor((CURRENT.month+2)/3)-1)
FinancialData = FinancialData.set_index('code')
FinancialData = FinancialData.drop(['name', 'bvps', 'distrib', 'epcf', 'report_date'], axis = 1)
FinancialData.to_csv('./ASHR/DATA/FinancialData_2015_1.csv', index = True)

ProfitData = ts.get_profit_data(CURRENT.year, np.floor((CURRENT.month+2)/3)-1)
ProfitData = ProfitData.set_index('code')
ProfitData = ProfitData.drop(['name', 'business_income', 'net_profits'], axis = 1)
ProfitData.to_csv('./ASHR/DATA/ProfitData_2015_1.csv', index = True)

GrowthData = ts.get_growth_data(CURRENT.year, np.floor((CURRENT.month+2)/3)-1)
GrowthData = GrowthData.set_index('code')
GrowthData = GrowthData.drop(['name'], axis = 1)
GrowthData.to_csv('./ASHR/DATA/GrowthData_2015_1.csv', index = True)

DebtPayingData = ts.get_debtpaying_data(CURRENT.year, np.floor((CURRENT.month+2)/3)-1)
DebtPayingData = DebtPayingData.set_index('code')
DebtPayingData = DebtPayingData.drop(['name', 'sheqratio', 'adratio'], axis = 1)
DebtPayingData.to_csv('./ASHR/DATA/DebtPayingData_2014_12.csv', index = True)

# Merging data
for subtab in [FinancialData, ProfitData, GrowthData, DebtPayingData]:
    StockInfo = pd.merge(StockInfo, subtab, how = 'outer', on = 'code')

# Saving data
StockInfo = StockInfo.to_csv('./ASHR/DATA/StockInfo.csv', index = True)



########################
##   Trade Tick Data  ##
##    NOT LEVEL 2     ##
########################

def DirectionMap(x):
    if x == '买盘':
        return 'Buy'
    elif x == '卖盘':
        return 'Sell'
    elif x == '中性盘':
        return 'Neutral'

#StockName = pd.read_csv('./ASHR/DATA/StockName.csv', header = None)
#StockName.columns = ['code', 'name']
StockName = pd.read_csv('./ASHR/DATA/Index/csi500.csv')
StockName = CodeWrapper(StockName['code'])
#StockName = StockName[StockName >= '000090']

StartDay = datetime.date(2015, 1, 1)
EndDay = datetime.date(2015, 10, 1)

for stock in StockName:
    day = StartDay
    TickData = ts.get_tick_data(code = stock, date = day.strftime('%Y-%m-%d'))
    try:
        TickData['time'] = TimeWrapper(TickData['time'])
        TickData['time'] = TickData['time'].map(lambda x: TimeMapToDatetime(x, day))
        TickData = TickData.sort('time')
    except Exception:
        print "%s on %s is not available"%(stock, day.strftime('%Y-%m-%d'))
        TickData = pd.DataFrame(columns = [u'time', u'price', u'change', u'volume', u'amount', u'type'])
    while day <= EndDay:
        day = pd.tseries.offsets.BDay(1) + day
        day = datetime.date(day.year, day.month, day.day)
        _tempdata = ts.get_tick_data(code = stock, date = day.strftime('%Y-%m-%d'))
        try:
            _tempdata['time'] = TimeWrapper(_tempdata['time'])
            _tempdata['time'] = _tempdata['time'].map(lambda x: TimeMapToDatetime(x, day))
            _tempdata = _tempdata.sort('time')
        except Exception:
            print "%s on %s is not available"%(stock, day.strftime('%Y-%m-%d'))
            _tempdata = pd.DataFrame(columns = [u'time', u'price', u'change', u'volume', u'amount', u'type'])
        TickData = pd.concat([TickData, _tempdata])
    TickData['type'] = TickData['type'].map(lambda x: DirectionMap(x))
    TickData.to_csv('./ASHR/DATA/TickData/%s_%s_to_%s.csv'%(stock, StartDay.strftime('%y-%m'), EndDay.strftime('%y-%m')), index = False, header = True)
    
