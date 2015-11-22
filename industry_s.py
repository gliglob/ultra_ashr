#####################
####             ####
#### Pull Data   ####
####             ####
#####################

import tushare as ts

# Restrict Stock Set to CSI All


StockList = pd.read_excel('./ASHR/DATA/Index/Index/csi_all.xls', header = None, names = ['Ticker'])['Ticker']
StockList = CodeWrapper(StockList)
StockList = StockList.map(lambda x: 'SH' + x if x[0] == '6' else 'SZ' + x)

IndustryList = ['综合行业', '公路桥梁', '化纤行业', '机械行业', '生物制药', '石油行业', '玻璃行业', '仪器仪表', '交通运输', 
 '飞机制造', '农林牧渔', '建筑建材',  '塑料制品', '商业百货', '纺织行业',  '医疗器械', '有色金属', '供水供气', 
 '发电设备', '造纸行业', '船舶制造',  '煤炭行业', '食品行业', '陶瓷行业',  '纺织机械', '钢铁行业', '环保行业', 
 '酿酒行业', '次新股', '电器行业',  '传媒娱乐', '化工行业', '房地产',  '金融行业', '其他行业', '开发区', 
 '电子信息', '服装鞋类', '电子器件',  '电力行业', '汽车制造', '家具行业', '农药化肥', '酒店旅游',  '水泥行业',
 '物资外贸', '摩托车', '印刷包装', '家电行业']
 
IndustryEnglishList = ['ConsumerDiscretionary', 'Industrials', 'Materials', 'Industrials', 'HealthCare', 'Energy', 'Materials', 
  'Industrials', 'Industrials', 'Industrials', 'ConsumerStaples', 'Materials', 'Materials', 'ConsumerDiscretionary',
  'ConsumerDiscretionary', 'HealthCare', 'Materials', 'Utilities', 'Industrials', 'Materials', 'Industrials',
  'Materials', 'ConsumerStaples', 'Materials', 'Industrials', 'Materials', 'Utilities', 'ConsumerStaples', 'Financials', 
  'ConsumerDiscretionary', 'ConsumerDiscretionary', 'Materials', 'Financials', 'Financials', 'Other', 'Other',
  'InformationTechnology', 'ConsumerDiscretionary', 'ConsumerDiscretionary', 'Utilities', 'ConsumerDiscretionary', 
  'ConsumerDiscretionary', 'Materials', 'ConsumerDiscretionary', 'Materials', 'Industrials', 'ConsumerDiscretionary',
  'Materials', 'ConsumerDiscretionary']

IndustryClassified = ts.get_industry_classified()
IndustryClassified['code'] = IndustryClassified['code'].map(lambda x: 'SH'+x if x[0] == '6' else 'SZ'+x)

IndustryClassified[IndustryClassified.code.isin(StockList)]

# Restrict To Stock List Only
Industry

CURRENT = datetime.datetime.now()
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
    
    
########################
##   Trade Hist Data  ##
########################




def main():
    # Example
    df = pd.DataFrame({'a':[1,2,4,5,9],'b':[2,3,1,6,15], 'c':[3,4,10,8,17]})
    df.reset_index()


pd.read_csv()
ts.get_tick_data()
