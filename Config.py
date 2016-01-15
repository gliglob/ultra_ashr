import pandas as pd
from HelperFunctions import *
from Static import STATIC

class CONFIG(object):
    
    # STOCK
    STOCK = ['SZ000001']
    
    
    # File path
    TICKDATAPATH = './ASHR/DATA/Test/Test_Tick/%s/%s/%s.csv'
    SECONDDATAPATH = './ASHR/DATA/Test/Test_Second/%s/%s/%s_%s.csv'
    PROCESSEDFOLDERPATH = './ASHR/DATA/Processed/%s/'
    PROCESSEDDATAPATH = './ASHR/DATA/Processed/%s/%s.csv'
    STOCKINDUSTRYMAPPATH = './ASHR/DATA/Index/IndustryIndex.csv'
    STOCKLISTPATH = './ASHR/DATA/Index/Index/csi_all.xls'
    INDEXDATAPATH = './ASHR/DATA/%s/%s.csv'
    MODELPATH = './ASHR/DATA/Model/%s'
    MODELDATAPATH = './ASHR/DATA/Model/%s/%s.pkl'
    DAILYDATAPATH = './Dailydata_%s.csv'
    DAILYVWAPDATAPATH = './Dailyvwapdata_%s.csv'
    
    # last model training update
    LASTMODELUPDATE = '20160106'
    
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
    TRADINGSTARTDATE = datetime.date(2014, 12, 1)
    TRADINGENDDATE = datetime.date(2015, 10, 31)
    MASTERCLOCKSCALE = '3s'
        
    # Daily Stock Data for a single Stock
    FEATURES = ['EndOfDayPendingBuyRatio', 'TotalAmount', 'Open', 'Close', 'High', 'Low', 
        'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2', 'PriceCurvature2', 
        'PriceSlope3', 'PriceCurvature3', 'PricePema1', 'PricePema2','PricePema3', 'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 
        'PendingBuySlope3', 'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2', 
        'AmountSlope3', 'AmountCurvature3', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2', 
        'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3', 'IndexSpreadSlope1', 'IndexSpreadCurvature1', 
        'IndexSpreadSlope2', 'IndexSpreadCurvature2', 'IndexSpreadSlope3', 'IndexSpreadCurvature3', 'SidedAmount1', 'SidedAmount2',
        'SidedAmount3', 'RSI1', 'RSI2', 'RSI3', 'Volatility', 'VolatilityIndexSpread', 'VolatilityIndustryIndexSpread', 'BetaIndex', 'BetaIndustryIndex', 'Return1', 'Return2', 'IncludedInTraining']
    DAILYDATAFRAME = pd.DataFrame(columns = FEATURES)
    
    VWAPFEATURES = ['Open', 'Close', 'High', 'Low', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2', 'PriceCurvature2', 
    'PriceSlope3', 'PriceCurvature3', 'PricePema1', 'PricePema2','PricePema3','IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2', 
    'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3', 'IndexSpreadSlope1', 'IndexSpreadCurvature1', 
    'IndexSpreadSlope2', 'IndexSpreadCurvature2', 'IndexSpreadSlope3', 'IndexSpreadCurvature3', 
    'RSI1', 'RSI2', 'RSI3', 'Volatility', 'VolatilityIndexSpread', 'VolatilityIndustryIndexSpread', 'BetaIndex', 'BetaIndustryIndex']



    DAILYVWAPDATAFRAME = pd.DataFrame(columns = VWAPFEATURES)



    ###############
    # Preparation #
    ###############
    
    TRADINGDAYS = GenerateMasterClock(TRADINGSTARTDATE, TRADINGENDDATE, '1d').MasterClock.map(lambda x: x.strftime('%Y%m%d')).tolist()
    
    # Intraday Master Clock
    StartDate = datetime.datetime.combine(datetime.date(2015, 10, 9), STATIC.TRADINGHOURS[0])
    EndDate = datetime.datetime.combine(datetime.date(2015, 10, 9), STATIC.TRADINGHOURS[-1])
    INTRADAYMASTERCLOCK = GenerateMasterClock(StartDate, EndDate, MASTERCLOCKSCALE)
    INTRADAYMASTERCLOCK['MasterClock'] = INTRADAYMASTERCLOCK['MasterClock'].apply(lambda x: x.time())
    

    # Stock Industry Index Map
    STOCKINDUSTRYINDEXMAP = pd.read_csv(STOCKINDUSTRYMAPPATH, index_col = 'Ticker')
    
    ###################
    # Strategy Config #
    ###################
    
    STRATEGY1_TRADINGHORIZON = 5
    STRATEGY1_STOPLOSSTHRESH = 0.1
    STRATEGY1_MAXPROFITTHRESH = 0.1
    STRATEGY1_SELLTHRESH = 0.01
    
    STRATEGY2_TRADINGHORIZON = 1
    
    
    """
    COMPLETE_FEATURES = ['EndOfDayPendingBuyRatio', 'TotalAmount', 'Open', 'Close', 'High',
    'Low', 'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2',
    'PriceCurvature2', 'PriceSlope3', 'PriceCurvature3', 'PricePema1', 'PricePema2', 'PricePema3',
    'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 'PendingBuySlope3',
    'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2',
    'AmountSlope3', 'AmountCurvature3', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2',
    'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3', 'SidedAmount1', 'SidedAmount2',
    'SidedAmount3', 'RSI1', 'RSI2', 'RSI3', 'Return1', 'Return2', 'WilliamR_1', 'WilliamR_2', 'WilliamR_3',
    'InverseWilliamR_1', 'InverseWilliamR_2', 'InverseWilliamR_3', 'Disparity1', 'Disparity2', 'Disparity3',
    'Disparity12', 'Disparity13', 'Disparity23', 'BuyRatio2', 'BuyRatio3', 'A_buyRatio2', 'A_buyRatio3',
    'B_buyRatio2', 'B_buyRatio3', 'EndOfDayPendingBuyRatio2', 'EndOfDayPendingBuyRatio3']
    """
