from Config import CONFIG
import pandas as pd

def DailyDataFeaturePrep(stock):
    """
    Daily Data Feature Preparation
    """
    
    df = pd.read_csv(CONFIG.DAILYDATAPATH%stock)
    Scale1 = 1
    Scale2 = CONFIG.M1_2 / 4800
    Scale3 = CONFIG.M1_3 / 4800
    High_Scale2 = pd.rolling_max(df.Close, Scale2)
    Close_Scale3 = pd.    
    
    # William %R
    # (High - Current) / (High - Low)

    df['WilliamR_1'] = (df.Close - df.Low) / (df.High - df.Low)
    
    pd.rolling_min(df, Scale2)[K_Scale-1:]
    df['WilliamR_2']
    
    # Inverse William %R
