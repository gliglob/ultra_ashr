"""
For Volume weighted price specifically
"""

"""
Feature Preparation -- Prepare Daily Feature for each session
                    -- Prepare Intraday Feature
"""

from HelperFunctions import *
from SlopeCurvatureConstruction import SlopeCurvatureConstruction
#from IntegratedDifferencerConstruction import IntegratedDifferencerConstruction
from PolyEmaConstruction import PolyEmaConstruction
from Strategy import *
from Config import CONFIG



def VwapFeaturePreparation(df, Stock, IndustryIndex, Index, DailyData):
    """
    Prepare the following end of day or intraday features:
    Date, EndOfDayPendingBuyRatio, Open, Close, High, Low, BuyRatio, A_buyRatio, B_buyRatio
    
    Input:
        /df/:   df for a single stock on a specific day
    Output:
        /DailyData/: columns = EndOfDayPendingBuyRatio, TotalAmount, Open, Close, High, Low, BuyRatio, A_buyRatio, B_buyRatio,
                               PriceSlope, PriceCurvature, PendingBuyRatioSlope, PendingBuyRatioCurvature, AmountSlope, AmountCurvature
    """
    ########################## 
    # End of session feature #
    ##########################
    df['price'] = df['vw_price']
    Date = df.index[-1]
    Open = df.price[0]
    Close = df.price[-1]
    High = max(df.price)
    Low = min(df.price)
    
    ##############
    # Volatility #
    ##############
    Volatility = np.std(df['price'])
    
    # resulting df has columns: pendingBuyRatio, price, amount
    df = DropColumn(df, ['amountRolling', 'buyRatio', 'A_buyRatio', 'B_buyRatio'])
    
    ##############################
    # Intraday filtering feature #
    ##############################
    
    # Check if there are significnat price changes that are more than 11%, if so, we will restart the filter
    d = 0
    while True:
        d -= 1
        LastRecord = AddBusinessDay(Date, d)
        
        if LastRecord in DailyData.index:
            RestartFilter = (Open - DailyData.loc[LastRecord]['Close'] >= np.log(1.11)) or (Open - DailyData.loc[LastRecord]['Close'] <= np.log(0.89))
            if RestartFilter:
                logging.warning('Stock price changes more than 11 pct on %s. Today Open %f, Last Trading Day Close %f. Restarting filter for %s...'%(LastRecord.date().strftime('%Y%m%d'), Open, DailyData.loc[LastRecord]['Close'], Date.date().strftime('%Y%m%d')))
            break
        elif d <= -5:
            logging.warning('Stock was closed or data was missing for past 5 business days on %s. Restarting filter for %s...'%(LastRecord.date().strftime('%Y%m%d'), Date.date().strftime('%Y%m%d')))
            RestartFilter = True
            break
        
    # Add industry spread column, spread = log(exp(Index.price) - exp(df.price))
    IndexDate = Date.date().strftime('%Y%m%d')
    try:     
        IndexData = pd.read_csv(CONFIG.INDEXDATAPATH%(Index, IndexDate), header = 0, names = ['time', 'price'], index_col = 0)
        IndexSpread = np.log(np.exp(IndexData.price) - np.exp(df.price))
        BetaIndex = np.corrcoef(IndexData.price.diff(periods = 1).fillna(0), df.price.diff().fillna(0))[0][1] * (np.std(df.price.diff().fillna(0)) / np.std(IndexData.price.diff().fillna(0)))
        df['indexspread'] = IndexSpread.tolist()
        if np.isnan(df['indexspread']).sum() > 0:
            logging.warning('Not able to take the log of %d spreads between stock %s and index %s for date %s. Taking the abs value instead.'%(np.isnan(df['indexspread']).sum(), Stock, Index, IndexDate))
            df['indexspread'][np.isnan(df['indexspread'])] = np.log(abs(np.exp(IndexData.price) - np.exp(df.price)))
        VolatilityIndexSpread = np.std(IndexSpread)
        
    except Exception, e:
        df['indexspread'] = 0
        VolatilityIndexSpread = 0
        BetaIndex = 0
        logging.warning(str(e))
        if not os.path.isfile(CONFIG.INDEXDATAPATH%(Index, IndexDate)):
            logging.warning('Index Data is missing for stock %s on %s. Setting index spread slope and curvature to 0.'%(Stock, IndexDate))
        else:
            logging.warning('Other critical errors occurred when computing the index spread for stock %s on %s. Setting index spread slope and curvature to 0.'%(Stock, IndexDate))
    
            
    try:   
        IndustryIndexData = pd.read_csv(CONFIG.INDEXDATAPATH%(IndustryIndex, IndexDate), header = 0, names = ['time', 'price'], index_col = 0)
        IndustryIndexSpread = np.log(np.exp(IndustryIndexData.price) - np.exp(df.price))
        BetaIndustryIndex = np.corrcoef(IndustryIndexData.price.diff(periods = 1).fillna(0), df.price.diff().fillna(0))[0][1] * (np.std(df.price.diff().fillna(0)) / np.std(IndustryIndexData.price.diff().fillna(0)))
        df['industryspread'] = IndustryIndexSpread.tolist()
        if np.isnan(df['industryspread']).sum() > 0:
            logging.warning('Not able to take the log of %d spreads between stock %s and index %s for date %s. Taking the abs value instead.'%(np.isnan(df['industryspread']).sum(), Stock, Index, IndexDate))
            df['industryspread'][np.isnan(df['industryspread'])] = np.log(abs(np.exp(IndustryIndexData.price) - np.exp(df.price)))
        VolatilityIndustryIndexSpread = np.std(IndustryIndexSpread)
        
    except Exception, e:
        df['industryspread'] = 0
        VolatilityIndustryIndexSpread = 0
        BetaIndustryIndex = 0
        logging.warning(str(e))
        if not os.path.isfile(CONFIG.INDEXDATAPATH%(IndustryIndex, IndexDate)):
            logging.warning('Industry index Data is missing for stock %s on %s. Setting industry index spread slope and curvature to 0.'%(Stock, IndexDate))
        else:
            logging.warning('Other critical errors occurred when computing the industry spread for stock %s on %s. Setting industry index spread slope and curvature to 0.'%(Stock, IndexDate))
            
    
    if (not DailyData.empty) and (not RestartFilter):
        price1_stored = LoadObject('./ASHR/DATA/FilterInstances/price1.pkl')
        price2_stored = LoadObject('./ASHR/DATA/FilterInstances/price2.pkl')
        price3_stored = LoadObject('./ASHR/DATA/FilterInstances/price3.pkl')
        pricepema1_stored = LoadObject('./ASHR/DATA/FilterInstances/pricepema1.pkl')
        pricepema2_stored = LoadObject('./ASHR/DATA/FilterInstances/pricepema2.pkl')
        pricepema3_stored = LoadObject('./ASHR/DATA/FilterInstances/pricepema3.pkl')
        industryspread1_stored = LoadObject('./ASHR/DATA/FilterInstances/industryspread1.pkl')
        industryspread2_stored = LoadObject('./ASHR/DATA/FilterInstances/industryspread2.pkl')
        industryspread3_stored = LoadObject('./ASHR/DATA/FilterInstances/industryspread3.pkl')
        indexspread1_stored = LoadObject('./ASHR/DATA/FilterInstances/indexspread1.pkl')
        indexspread2_stored = LoadObject('./ASHR/DATA/FilterInstances/indexspread2.pkl')
        indexspread3_stored = LoadObject('./ASHR/DATA/FilterInstances/indexspread3.pkl')
        uptick1_stored = LoadObject('./ASHR/DATA/FilterInstances/uptick1.pkl')
        uptick2_stored = LoadObject('./ASHR/DATA/FilterInstances/uptick2.pkl')
        uptick3_stored = LoadObject('./ASHR/DATA/FilterInstances/uptick3.pkl')
        downtick1_stored = LoadObject('./ASHR/DATA/FilterInstances/downtick1.pkl')
        downtick2_stored = LoadObject('./ASHR/DATA/FilterInstances/downtick2.pkl')
        downtick3_stored = LoadObject('./ASHR/DATA/FilterInstances/downtick3.pkl')

    else:
        price1_stored = None
        price2_stored = None
        price3_stored = None
        pricepema1_stored = None
        pricepema2_stored = None
        pricepema3_stored = None
        industryspread1_stored = None
        industryspread2_stored = None
        industryspread3_stored = None
        indexspread1_stored = None
        indexspread2_stored = None
        indexspread3_stored = None
        uptick1_stored = None
        uptick2_stored = None
        uptick3_stored = None
        downtick1_stored = None
        downtick2_stored = None
        downtick3_stored = None
    #        integrated1_stored = None
    #        integrated2_stored = None
    #        integrated3_stored = None
    #        integrateddiff1_stored = None
    #    integrateddiff2_stored = None
    #    integrateddiff3_stored = None
        
    # Apply Slope Curvature Filter to Price, PendingBuyRatio, Amount
    # TODO VWAP on overnights    
    df['PriceSlope1'], df['PriceCurvature1'], price1 = SlopeCurvatureConstruction('Price1', df['price'], CONFIG.M1_1, price1_stored)
    df['PriceSlope2'], df['PriceCurvature2'], price2 = SlopeCurvatureConstruction('Price2', df['price'], CONFIG.M1_2, price2_stored)
    df['PriceSlope3'], df['PriceCurvature3'], price3 = SlopeCurvatureConstruction('Price3', df['price'], CONFIG.M1_3, price3_stored)
    
    df['PricePema1'], pricepema1 = PolyEmaConstruction('PricePema1', df['price'], CONFIG.M1_1, pricepema1_stored) 
    df['PricePema2'], pricepema2 = PolyEmaConstruction('PricePema2', df['price'], CONFIG.M1_2, pricepema2_stored) 
    df['PricePema3'], pricepema3 = PolyEmaConstruction('PricePema3', df['price'], CONFIG.M1_3, pricepema3_stored) 

    if np.all(df['industryspread'] == 0):
        df['IndustrySpreadSlope1'], df['IndustrySpreadCurvature1'], df['IndustrySpreadSlope2'], df['IndustrySpreadCurvature2'], df['IndustrySpreadSlope3'], df['IndustrySpreadCurvature3'] = [0] * 6
    else:
        df['IndustrySpreadSlope1'], df['IndustrySpreadCurvature1'], industryspread1 = SlopeCurvatureConstruction('IndustrySpread1', df['industryspread'], CONFIG.M1_1, industryspread1_stored)
        df['IndustrySpreadSlope2'], df['IndustrySpreadCurvature2'], industryspread2 = SlopeCurvatureConstruction('IndustrySpread2', df['industryspread'], CONFIG.M1_2, industryspread2_stored)
        df['IndustrySpreadSlope3'], df['IndustrySpreadCurvature3'], industryspread3 = SlopeCurvatureConstruction('IndustrySpread3', df['industryspread'], CONFIG.M1_3, industryspread3_stored)
    
    if np.all(df['indexspread'] == 0):   
        df['IndexSpreadSlope1'], df['IndexSpreadCurvature1'], df['IndexSpreadSlope2'], df['IndexSpreadCurvature2'], df['IndexSpreadSlope3'], df['IndexSpreadCurvature3'] = [0] * 6
    else:
        df['IndexSpreadSlope1'], df['IndexSpreadCurvature1'], indexspread1 = SlopeCurvatureConstruction('IndexSpread1', df['indexspread'], CONFIG.M1_1, indexspread1_stored)
        df['IndexSpreadSlope2'], df['IndexSpreadCurvature2'], indexspread2 = SlopeCurvatureConstruction('IndexSpread2', df['indexspread'], CONFIG.M1_2, indexspread2_stored)
        df['IndexSpreadSlope3'], df['IndexSpreadCurvature3'], indexspread3 = SlopeCurvatureConstruction('IndexSpread3', df['indexspread'], CONFIG.M1_3, indexspread3_stored)


    #######
    # RSI #
    #######
    df['UpTick'] = 0
    df['DownTick'] = 0
    PriceDiff = df['price'].diff(periods = 1)
    df['UpTick'][PriceDiff > 0] = PriceDiff
    df['DownTick'][PriceDiff < 0] = -PriceDiff
    df['UpTick1'], uptick1 = PolyEmaConstruction('UpTick1', df['UpTick'], CONFIG.M1_1, uptick1_stored)
    df['UpTick2'], uptick2 = PolyEmaConstruction('UpTick2', df['UpTick'], CONFIG.M1_2, uptick2_stored)
    df['UpTick3'], uptick3 = PolyEmaConstruction('UpTick3', df['UpTick'], CONFIG.M1_3, uptick3_stored)
    df['DownTick1'], downtick1 = PolyEmaConstruction('DownTick1', df['DownTick'], CONFIG.M1_1, downtick1_stored)
    df['DownTick2'], downtick2 = PolyEmaConstruction('DownTick2', df['DownTick'], CONFIG.M1_2, downtick2_stored)
    df['DownTick3'], downtick3 = PolyEmaConstruction('DownTick3', df['DownTick'], CONFIG.M1_3, downtick3_stored)
    
    for item in [('PriceSlope1', 'price1', price1), ('PriceSlope2', 'price2', price2), ('PriceSlope3', 'price3', price3),\
        ('IndustrySpreadSlope1', 'industryspread1', industryspread1), ('IndustrySpreadSlope2', 'industryspread2', industryspread2), ('IndustrySpreadSlope3', 'industryspread3', industryspread3), \
        ('IndexSpreadSlope1', 'indexspread1', indexspread1), ('IndexSpreadSlope2', 'indexspread2', indexspread2), ('IndexSpreadSlope3', 'indexspread3', indexspread3), \
        ('PricePema1', 'pricepema1', pricepema1), \
        ('PricePema2', 'pricepema2', pricepema2), ('PricePema3', 'pricepema3', pricepema3), ('UpTick1', 'uptick1', uptick1), ('UpTick2', 'uptick2', uptick2), ('UpTick3', 'uptick3', uptick3), \
        ('DownTick1', 'downtick1', downtick1), ('DownTick2', 'downtick2', downtick2), ('DownTick3', 'downtick3', downtick3)]:
        if np.all(df[item[0]] == 0) or df[item[0]].isnull().any():
            logging.warning('Not saving the filter object for %s for stock %s on %s because data is missing or nan exists'%(item[1], Stock, Date.date().strftime('%Y%m%d')))
        else:            
            SaveObject(item[2], './ASHR/DATA/FilterInstances/%s.pkl'%item[1])
    
    RSI1 = 1 - 1 / (1 + (df['UpTick1'].iloc[-1] / df['DownTick1'].iloc[-1])) if df['DownTick1'].iloc[-1] != 0 else 1
    RSI2 = 1 - 1 / (1 + (df['UpTick2'].iloc[-1] / df['DownTick2'].iloc[-1])) if df['DownTick2'].iloc[-1] != 0 else 1
    RSI3 = 1 - 1 / (1 + (df['UpTick3'].iloc[-1] / df['DownTick3'].iloc[-1])) if df['DownTick3'].iloc[-1] != 0 else 1    
    
    ###############################
    # Vol weighted price analysis #
    ###############################
    
    
    # Select Last Data Point
    # TODO different starting point for downsampling
    DATA = [Open, Close, High, Low] + \
        df.iloc[-1][['PriceSlope1', 'PriceCurvature1', 'PriceSlope2', 'PriceCurvature2', 
        'PriceSlope3', 'PriceCurvature3', 'PricePema1', 'PricePema2', 'PricePema3', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustrySpreadSlope2', 
        'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3', 'IndexSpreadSlope1', 'IndexSpreadCurvature1', 
        'IndexSpreadSlope2', 'IndexSpreadCurvature2', 'IndexSpreadSlope3', 'IndexSpreadCurvature3']].tolist() + [RSI1, RSI2, RSI3, Volatility, VolatilityIndexSpread, VolatilityIndustryIndexSpread, BetaIndex, BetaIndustryIndex]


    DailyData.loc[Date] = DATA
    
    
    return DailyData
