from __future__ import division
from Config import CONFIG
import pandas as pd

def DailyDataFeaturePrep(stock):
    """
    Daily Data Feature Preparation
    """
    
    df = pd.read_csv(CONFIG.DAILYDATAPATH%stock)
    Scale1 = int(np.ceil(CONFIG.M1_1 / 4800))
    Scale2 = CONFIG.M1_2 / 4800
    Scale3 = CONFIG.M1_3 / 4800
    High_Scale1 = pd.rolling_max(df.High, Scale1, 0)
    High_Scale2 = pd.rolling_max(df.High, Scale2, 0)
    High_Scale3 = pd.rolling_max(df.High, Scale3, 0)
    Low_Scale1 = pd.rolling_min(df.Low, Scale1, 0)
    Low_Scale2 = pd.rolling_min(df.Low, Scale2, 0)
    Low_Scale3 = pd.rolling_min(df.Low, Scale3, 0)
    MA_Scale1 = df.PricePema1
    MA_Scale2 = df.PricePema2
    MA_Scale3 = df.PricePema3
    Current = df.Close
    
    
    # William %R
    # (High - Current) / (High - Low)
    
    df['WilliamR_1'] = (High_Scale1 - Current) / (High_Scale1 - Low_Scale1)
    df['WilliamR_2'] = (High_Scale2 - Current) / (High_Scale2 - Low_Scale2)
    df['WilliamR_3'] = (High_Scale3 - Current) / (High_Scale3 - Low_Scale3)
    
    # Inverse William %R
    # (Low - Current) / (High - Low)
    
    df['InverseWilliamR_1'] = (Low_Scale1 - Current) / (High_Scale1 - Low_Scale1)
    df['InverseWilliamR_2'] = (Low_Scale2 - Current) / (High_Scale2 - Low_Scale2)
    df['InverseWilliamR_3'] = (Low_Scale3 - Current) / (High_Scale3 - Low_Scale3)
    
    # Disparity
    # Current - MA_M1
    df['Disparity1'] = Current - MA_Scale1
    df['Disparity2'] = Current - MA_Scale2
    df['Disparity3'] = Current - MA_Scale3
    
    df['Disparity12'] = MA_Scale1 - MA_Scale2
    df['Disparity13'] = MA_Scale1 - MA_Scale3
    df['Disparity23'] = MA_Scale2 - MA_Scale3
    
    # Buy Ratio
    df['BuyRatio2'] = pd.rolling_mean(df.BuyRatio, Scale2, 0)
    df['BuyRatio3'] = pd.rolling_mean(df.BuyRatio, Scale3, 0)
    
    # A_buyRatio
    df['A_buyRatio2'] = pd.rolling_mean(df.A_buyRatio, Scale2, 0)
    df['A_buyRatio3'] = pd.rolling_mean(df.A_buyRatio, Scale3, 0)
    
    # B_buyRatio
    df['B_buyRatio2'] = pd.rolling_mean(df.B_buyRatio, Scale2, 0)
    df['B_buyRatio3'] = pd.rolling_mean(df.B_buyRatio, Scale3, 0)
    
    # PendingBuyRatio
    df['EndOfDayPendingBuyRatio2'] = pd.rolling_mean(df.EndOfDayPendingBuyRatio, Scale2, 0)
    df['EndOfDayPendingBuyRatio3'] = pd.rolling_mean(df.EndOfDayPendingBuyRatio, Scale3, 0)
    

df = pd.read_csv('/Users/zklnu66/Desktop/DailyDataSZ000001.csv', index_col = 'Time')
