"""
Feature Preparation -- Prepare Daily Feature for each session
                    -- Prepare Intraday Feature
"""

from HelperFunctions import *
from SlopeCurvatureConstruction import SlopeCurvatureConstruction
from IntegratedDifferencerConstruction import IntegratedDifferencerConstruction
from PolyEmaConstruction import PolyEmaConstruction

def FeaturePreparation(df, DailyData, HolidayList):
    """
    Prepare the following end of day or intraday features:
    Date, EndOfDayPendingBuyRatio, Open, Close, High, Low, BuyRatio, A_buyRatio, B_buyRatio
    
    Input:
        /df/:   df for a single stock on a specific day
    Output:
        /DailyData/: columns = EndOfDayPendingBuyRatio, TotalAmount, Open, Close, High, Low, BuyRatio, A_buyRatio, B_buyRatio,
                               PriceSlope, PriceCurvature, PendingBuyRatioSlope, PendingBuyRatioCurvature, AmountSlope, AmountCurvature
    """
    
    # End of session feature preparation
    Date = df.index[-1]
    EndOfDayPendingBuyRatio = df.pendingBuyRatio[-1]
    Open = df.price[0]
    Close = df.price[-1]
    High = max(df.price)
    Low = min(df.price)
    BuyRatio = df.buyRatio[-1]
    A_buyRatio = df.A_buyRatio[-1]
    B_buyRatio = df.B_buyRatio[-1]
    TotalAmount = df.amountRolling[-1]

    # resulting df has columns: pendingBuyRatio, price, amount
    df = DropColumn(df, ['amountRolling', 'buyRatio', 'A_buyRatio', 'B_buyRatio'])
    
    # Intraday filtering feature preparation
    # Choosing Three Different M1. 
    # 1 min contains 20 data points, 1 hour contains 1200 data points, 1 day contains 4800 data points
    
    # M1 = 30min
    M1_1 = 600
    # M1 = 2day    
    M1_2 = 9600
    # M1 = 10 day
    M1_3 = 48000

    # Check if there are significnat price changes that are more than 11%, if so, we will restart the filter
    LastRecord = AddBusinessDay(Date, -1)    
    RestartFilter = (Open - DailyData.loc[LastRecord]['Close'] >= np.log(1.11)) or (Open - DailyData.loc[LastRecord]['Close'] <= np.log(0.89))
    if RestartFilter:
        logging.warning('Stock % Price changes more than 11% on %s. Today Open %f, Last Day Close %f.'%() )
    
    if (not DailyData.empty) and (not RestartFilter):
        price1_stored = LoadObject('./ASHR/DATA/FilterInstances/price1.pkl')
        price2_stored = LoadObject('./ASHR/DATA/FilterInstances/price2.pkl')
        price3_stored = LoadObject('./ASHR/DATA/FilterInstances/price3.pkl')
        pendingbuy1_stored = LoadObject('./ASHR/DATA/FilterInstances/pendingbuy1.pkl')
        pendingbuy2_stored = LoadObject('./ASHR/DATA/FilterInstances/pendingbuy2.pkl')
        pendingbuy3_stored = LoadObject('./ASHR/DATA/FilterInstances/pendingbuy3.pkl')
        amount1_stored = LoadObject('./ASHR/DATA/FilterInstances/amount1.pkl')
        amount2_stored = LoadObject('./ASHR/DATA/FilterInstances/amount2.pkl')
        amount3_stored = LoadObject('./ASHR/DATA/FilterInstances/amount3.pkl')
        integrated1_stored = LoadObject('./ASHR/DATA/FilterInstances/integrated1.pkl')
#        integrated2_stored = LoadObject('./ASHR/DATA/FilterInstances/integrated2.pkl')
#        integrated3_stored = LoadObject('./ASHR/DATA/FilterInstances/integrated3.pkl')
        integrateddiff1_stored = LoadObject('./ASHR/DATA/FilterInstances/integrateddiff1.pkl')
#        integrateddiff2_stored = LoadObject('./ASHR/DATA/FilterInstances/integrateddiff2.pkl')
#        integrateddiff3_stored = LoadObject('./ASHR/DATA/FilterInstances/integrateddiff3.pkl')
    else:
        price1_stored = None
        price2_stored = None
        price3_stored = None
        pendingbuy1_stored = None
        pendingbuy2_stored = None
        pendingbuy3_stored = None
        amount1_stored = None
        amount2_stored = None
        amount3_stored = None
        integrated1_stored = None
#        integrated2_stored = None
#        integrated3_stored = None
        integrateddiff1_stored = None
#        integrateddiff2_stored = None
#        integrateddiff3_stored = None
        
    # Apply Slope Curvature Filter to Price, PendingBuyRatio, Amount
    # TODO VWAP on overnights    
    df['PriceSlope1'], df['PriceCurvature1'], price1 = SlopeCurvatureConstruction('Price1', df['price'], M1_1, price1_stored)
    df['PriceSlope2'], df['PriceCurvature2'], price2 = SlopeCurvatureConstruction('Price2', df['price'], M1_2, price2_stored)
    df['PriceSlope3'], df['PriceCurvature3'], price3 = SlopeCurvatureConstruction('Price3', df['price'], M1_3, price3_stored)
    
    df['PendingBuySlope1'], df['PendingBuyCurvature1'], pendingbuy1 = SlopeCurvatureConstruction('PendingBuy1', df['pendingBuyRatio'], M1_1, pendingbuy1_stored)
    df['PendingBuySlope2'], df['PendingBuyCurvature2'], pendingbuy2 = SlopeCurvatureConstruction('PendingBuy2', df['pendingBuyRatio'], M1_2, pendingbuy2_stored)
    df['PendingBuySlope3'], df['PendingBuyCurvature3'], pendingbuy3 = SlopeCurvatureConstruction('PendingBuy3', df['pendingBuyRatio'], M1_3, pendingbuy3_stored)
    
    df['AmountSlope1'], df['AmountCurvature1'], amount1 = SlopeCurvatureConstruction('Amount1', df['amount'], M1_1, amount1_stored)
    df['AmountSlope2'], df['AmountCurvature2'], amount2 = SlopeCurvatureConstruction('Amount2', df['amount'], M1_2, amount2_stored)
    df['AmountSlope3'], df['AmountCurvature3'], amount3 = SlopeCurvatureConstruction('Amount3', df['amount'], M1_3, amount3_stored)

    # Apply Integrated Differencer Filter to Price, then take difference Integrated Price - Price and run Polyema filter
    # Note, we need to advance the difference series and add the delays back
    df['Integrated1'], integrated1 = IntegratedDifferencerConstruction('Integrated1', df['price'], M1_1, integrated1_stored)
    # TODO check level of integrated diff using larger M1
#    df['Integrated2'], integrated2 = IntegratedDifferencerConstruction('Integrated2', df['price'], M1_2, integrated2_stored)
#    df['Integrated3'], integrated3 = IntegratedDifferencerConstruction('Integrated3', df['price'], M1_3, integrated3_stored)
    DifferenceSeries1 = [x-y for x,y in zip(df['price'][:len(df)-M1_1].tolist(), df['Integrated1'][M1_1:].tolist())] + [0] * M1_1
#    DifferenceSeries2 = [x-y for x,y in zip(df['price'][:len(df)-M1_2].tolist(), df['Integrated1'][M1_2:].tolist())] + [0] * M1_2
#    DifferenceSeries3 = [x-y for x,y in zip(df['price'][:len(df)-M1_3].tolist(), df['Integrated1'][M1_3:].tolist())] + [0] * M1_3
    
    df['IntegratedDiff1'], integrateddiff1 = PolyEmaConstruction('IntegratedDiff1', DifferenceSeries1, M1_1,  integrateddiff1_stored)
#    df['IntegratedDiff2'], integrateddiff2 = PolyEmaConstruction('IntegratedDiff2', DifferenceSeries2, M1_2,  integrateddiff2_stored)
#    df['IntegratedDiff3'], integrateddiff3 = PolyEmaConstruction('IntegratedDiff3', DifferenceSeries3, M1_3,  integrateddiff3_stored)

    for item in [('price1', price1), ('price2', price2), ('price3', price3), ('pendingbuy1', pendingbuy1), \
        ('pendingbuy2', pendingbuy2), ('pendingbuy3', pendingbuy3), ('amount1', amount1), ('amount2', amount2), ('amount3', amount3), \
        ('integrated1', integrated1), ('integrateddiff1', integrateddiff1)]:
        SaveObject(item[1], './ASHR/DATA/FilterInstances/%s.pkl'%item[0])
    
    
    # Select Last Data Point
    # TODO different starting point for downsampling
    DailyData.loc[Date] = [EndOfDayPendingBuyRatio, TotalAmount, Open, Close, High, Low, BuyRatio, A_buyRatio, B_buyRatio] + \
        df.iloc[-1][['PriceSlope1', 'PriceCurvature1', 'PriceSlope2', 'PriceCurvature2', 
        'PriceSlope3', 'PriceCurvature3', 'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 
        'PendingBuySlope3', 'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2', 
        'AmountSlope3', 'AmountCurvature3', 'IntegratedDiff1']].tolist()
        

    return DailyData

# Exapmle of Feature Addition, Adding Spread
def AddSpreadFeature(df, FeatureToAdd):
    Index = 
    return

