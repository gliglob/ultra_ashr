"""
Data Cleaning & analysis (at the moment)
"""

from SetUp import *


def TickDataCleaning(df):
    
    """
    Drop NA values
    Fix the format of time
    Restricting to Trading Hours only
    """
    
    df = DropNaData(df, ['time', 'price', 'volume', 'side'])
    df['time'] = TimeWrapper4(df['time'])
    df = DropOutliers(df, 'price')
    return df

def SecondDataCleaning(df):
    
    """
    Drop NA values
    Drop Buy1-Sell5 prices
    Fix the format of time
    Note, Since we are doing As-Of join on Second Data, restricting to trading hour is not necessary
    """
    
    df = DropNaData(df)
    df = DropColumn(df, ['count', 'amount', 'volume', 'side', 'buy1', 'buy2', 'buy3', 'buy4', 'buy5', 'sell1', 'sell2', 'sell3', 'sell4', 'sell5'])
    df['time'] = TimeWrapper3(df['time'])

    # df = RestrictTradingHour(df, TradingHours, TimeFormat = False)
    
    return df

def IndexDataCleaning(df):
    """
    Drop NA values
    Drop Buy1-Sell5 prices, Volume
    Fix the format of time
    """
    df = DropColumn(df, ['count', 'amount', 'side', 'buy1', 'buy2', 'buy3', 'buy4', 'buy5', 'sell1', 'sell2', 'sell3', 'sell4', 'sell5', 'exchange', 'ticker', 'buy1Volume', 'buy2Volume', 'buy3Volume', 'buy4Volume', 'buy5Volume', 'sell1Volume', 'sell2Volume', 'sell3Volume', 'sell4Volume', 'sell5Volume'])    
    df = DropNaData(df)
    df['time'] = TimeWrapper3(df['time'])
    
    return df
