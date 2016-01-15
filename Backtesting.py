"""
Backtesting -
Strategy:
Entering Position: Opening of Trading Day
Exit Position: Opening of Next Trading Day
"""

import pandas as pd
from HelperFunctions import *
from Config import CONFIG

BACKTESTSTARTDATE = datetime.date(2015, 10, 1)
BACKTESTENDDATE = datetime.date(2015, 10, 31)
BACKTESTDAYS = GenerateMasterClock(BACKTESTSTARTDATE, BACKTESTENDDATE, '1d').MasterClock.tolist()

BacktestFeatures = ['EndOfDayPendingBuyRatio', 'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2',
    'PriceCurvature2', 'PriceSlope3', 'PriceCurvature3', 
    'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 'PendingBuySlope3',
    'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2',
    'AmountSlope3', 'AmountCurvature3', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2',
    'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3',  'IndexSpreadSlope1', 'IndexSpreadCurvature1', 
    'IndexSpreadSlope2', 'IndexSpreadCurvature2', 'IndexSpreadSlope3', 'IndexSpreadCurvature3', 'SidedAmount1', 'SidedAmount2',
    'SidedAmount3', 'RSI1', 'RSI2', 'RSI3', 'Volatility', 'VolatilityIndexSpread', 'VolatilityIndustryIndexSpread', 'BetaIndex', 'BetaIndustryIndex',
    'WilliamR_1', 'WilliamR_2', 'WilliamR_3','InverseWilliamR_1', 'InverseWilliamR_2', 'InverseWilliamR_3', 'Disparity1', 'Disparity2', 'Disparity3',
    'Disparity12', 'Disparity13', 'Disparity23', 'BuyRatio2', 'BuyRatio3', 'A_buyRatio2', 'A_buyRatio3',
    'B_buyRatio2', 'B_buyRatio3', 'EndOfDayPendingBuyRatio2', 'EndOfDayPendingBuyRatio3', 'Volatility2', 'Volatility3', 
    'VolatilityIndexSpread2', 'VolatilityIndexSpread3', 'VolatilityIndustryIndexSpread2', 'VolatilityIndustryIndexSpread3',
    'BetaIndex2', 'BetaIndex3', 'BetaIndustryIndex2', 'BetaIndustryIndex3']

TargetFeature = 'Return2'

STRATEGYRETURNCUTOFF = 0.07


# Regression OR classification

model_name = 'Regr_'
# model_name = 'Class_'
total_return = 0
for date in BACKTESTDAYS:
    logging.info('Backtest start for %s'%date.strftime('%Y%m%d'))
    long_position = []
    accumulated_actual_return = 0
    for stock in CONFIG.STOCK:
        try:
            data = pd.read_csv(CONFIG.DAILYDATAPATH%stock, index_col = 'Time')
            data.index = TimeWrapper3(data.index)
            backtestdate = datetime.datetime.combine(date, datetime.time(15))
            
            model = LoadObject(CONFIG.MODELDATAPATH%(stock, model_name + CONFIG.LASTMODELUPDATE))
            X_test = data[BacktestFeatures].loc[backtestdate].as_matrix()
            # Note Y_test is always the actual return regardless of the model
            Y_test = data[TargetFeature].loc[backtestdate]
            predicted_return = model.predict(X_test)
            # Enter long position if predicted_return >= STRATEGYRETURNCUTOFF
            if (model_name == 'Regr_' and predicted_return >= STRATEGYRETURNCUTOFF) or (model_name  == 'Class_' and predicted_return == 1):
                    long_position.append(stock)
                    accumulated_actual_return += Y_test
                    logging.info('Enter long position for %s. Predicted Return %f. Actual Return %f.'%(stock, predicted_return, Y_test))

        except Exception:
            if backtestdate not in data.index:
                logging.warning('Data for %s is missing on %s when backtesting'%(stock, date.strftime('%Y%m%d')))
    
    count = len(long_position)
    actual_return = accumulated_actual_return / count if count > 0 else 0
    logging.info('Actual return for %s is %f. Number of long positions is %d'%(date.strftime('%Y%m%d'), actual_return, count))
    total_return += actual_return
logging.info('Compound return from %s to %s is %f'%(BACKTESTSTARTDATE.strftime('%Y%m%d'), BACKTESTENDDATE.strftime('%Y%m%d'), total_return))
