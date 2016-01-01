from Config import CONFIG
import pandas as pd

def DailyDataFeaturePrep(stock):
    """
    Daily Data Feature Preparation
    """
    
    df = pd.read_csv(CONFIG.DAILYDATAPATH%stock)
    Scale1 = CONFIG.M1_1 / 4800
    Scale2 = CONFIG.M1_2 / 4800
    Scale3 = CONFIG.M1_3 / 4800
    High_Scale2 = pd.rolling_max(df.High, Scale2, 0)
    High_Scale2 = pd.rolling_max(df.High, Scale2, 0)
    High_Scale3 = pd.rolling_max(df.High, Scale3, 0)
    Low_Scale2 = pd.rolling_min(df.Low, Scale2, 0)
    Low_Scale3 = pd.rolling_min(df.Low, Scale3, 0)
    MA_Scale1 = df.PricePema1
    MA_Scale2 = df.PricePema2
    MA_Scale3 = df.PricePema3
    Current = df.Close
    
    
    # William %R
    # (High - Current) / (High - Low)

    df['WilliamR_1'] = (df.Close - df.Low) / (df.High - df.Low)
    
    pd.rolling_min(df, Scale2)[K_Scale-1:]
    df['WilliamR_2']
    
    # Inverse William %R

df = pd.read_csv('/Users/Hui/Desktop/DailyData_SZ000001.csv', index_col = 'Time')
