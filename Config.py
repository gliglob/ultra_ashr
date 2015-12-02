import pandas as pd
from HelperFunctions import *
from Static import STATIC

class CONFIG(object):
    
    
    # File path
    TICKDATAPATH = './ASHR/DATA/Test/Test_Tick/%s/%s/%s.csv'
    SECONDDATAPATH = './ASHR/DATA/Test/Test_Second/%s/%s/%s_%s.csv'
    PROCESSEDFOLDERPATH = './ASHR/DATA/Processed/%s/'
    PROCESSEDDATAPATH = './ASHR/DATA/Processed/%s/%s.csv'
    STOCKINDUSTRYMAPPATH = './ASHR/DATA/StockIndustryIndex.csv'
    STOCKLISTPATH = './ASHR/DATA/Index/Index/csi_all.xls'
    INDEXDATAPATH = './ASHR/DATA/%s/%s.csv'
    
    # Quantitative config
    TYPEA_CUTOFF = 500000
        
    TRADINGHORIZON_STRATEGY1 = 5
    TRADINGHORIZON_STRATEGY2 = 1
    STOPLOSSTHRESH = 0.1
    MAXPROFITTHRESH = 0.1    
    SELLTHRESH = 0.01

    # Choosing Three Different M1. 
    # 1 min contains 20 data points, 1 hour contains 1200 data points, 1 day contains 4800 data points
    # M1 = 30min
    M1_1 = 600
    # M1 = 2day    
    M1_2 = 9600
    # M1 = 10 day
    M1_3 = 48000    
    
    # Feature config
    TRADINGSTARTDATE = datetime.date(2015, 9, 1)
    TRADINGENDDATE = datetime.date(2015, 9, 7)
    MASTERCLOCKSCALE = '3s'
        
    # Daily Stock Data for a single Stock
    DAILYDATAFRAME = pd.DataFrame(columns = ['EndOfDayPendingBuyRatio', 'TotalAmount', 'Open', 'Close', 'High', 'Low', 
        'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2', 'PriceCurvature2', 
        'PriceSlope3', 'PriceCurvature3', 'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 
        'PendingBuySlope3', 'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2', 
        'AmountSlope3', 'AmountCurvature3', 'IntegratedDiff1', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2', 
        'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3', 'Return1', 'Return2'])



    ###############
    # Preparation #
    ###############
    
    TRADINGDAYS = GenerateMasterClock(TRADINGSTARTDATE, TRADINGENDDATE, '1d').MasterClock.map(lambda x: x.strftime('%Y%m%d')).tolist()
    
    # Intraday Master Clock
    StartDate = datetime.datetime.combine(datetime.date(2015, 10, 9), STATIC.TRADINGHOURS[0])
    EndDate = datetime.datetime.combine(datetime.date(2015, 10, 9), STATIC.TRADINGHOURS[-1])
    INTRADAYMASTERCLOCK = GenerateMasterClock(StartDate, EndDate, MASTERCLOCKSCALE)
    INTRADAYMASTERCLOCK['MasterClock'] = INTRADAYMASTERCLOCK['MasterClock'].apply(lambda x: x.time())
    


