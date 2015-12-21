"""
Data Processing
"""

from SetUp import *
from Config import CONFIG

def TickDataProcessing(df):
    """
    Add the following features/columns:
        /amount/:     price * volume
        /orderType/:  'A' if amount >= 500000
                      'B' if amount < 500000
        /buyRatio/:   (Buy amount - Sell amount) / (Buy amount + Sell amount)
        /A_buyRatio/: (A type Buy - A type Sell) / (A type Buy + A type Sell)
                      NOTE: Inf values are changed to np.nan
        /B_buyRatio/: (B type Buy - B type Sell) / (B type Buy + B type Sell)
    """
    
    def OrderTypeMap(e):
        return "A" if e >= CONFIG.TYPEA_CUTOFF else "B"
        
    df['amount'] = df['price'] * df['volume']
    df['amountRolling'] = df['amount'].cumsum()
    df['orderType'] = df['amount'].map(lambda x: OrderTypeMap(x))
    #df['sidedAmount'] = df.apply(lambda x: x['amount'] if x['side'] == 'B' else -x['amount'], axis = 1)
    df['volumeRolling'] = df['volume'].cumsum()
    df['buyRollingSum'] = df['volume'][df['side'] == 'B'].cumsum()
    df['sellRollingSum'] = df['volume'][df['side'] == 'S'].cumsum()
    df = df.fillna(method = 'ffill').fillna(value = 0)
    df['buyRatio'] = (df['buyRollingSum'] - df['sellRollingSum']) / (df['buyRollingSum'] + df['sellRollingSum'])
    df = df.replace([-np.inf, np.inf], 0)
    df['A_buyRollingSum'] = df['volume'][(df['side'] == 'B') & (df['orderType'] == 'A')].cumsum()
    df['A_sellRollingSum'] = df['volume'][(df['side'] == 'S') & (df['orderType'] == 'A')].cumsum()
    df['B_buyRollingSum'] = df['volume'][(df['side'] == 'B') & (df['orderType'] == 'B')].cumsum()
    df['B_sellRollingSum'] = df['volume'][(df['side'] == 'S') & (df['orderType'] == 'B')].cumsum()
    df = df.fillna(method = 'ffill').fillna(value = 0)
    df['A_buyRatio'] = (df['A_buyRollingSum'] - df['A_sellRollingSum']) / (df['A_buyRollingSum'] + df['A_sellRollingSum'])
    df['B_buyRatio'] = (df['B_buyRollingSum'] - df['B_sellRollingSum']) / (df['B_buyRollingSum'] + df['B_sellRollingSum'])
    df = df.replace([-np.inf, np.inf], np.nan)
        
    df['sidedAmount'] = df['amount']
    df['sidedAmount'][df['side'] == 'S'] = -df['amount']
    df['sidedAmountRolling'] = df['sidedAmount'].cumsum()
    
    
    df = DropColumn(df, ['A_buyRollingSum', 'A_sellRollingSum', 'B_buyRollingSum', 'B_sellRollingSum', 'buyRollingSum', 'sellRollingSum', 'volumeRolling', 'side', 'volume', 'orderType'])
    
    # Asof join by MasterClock
    df = df.set_index('time')
    df = df.apply(lambda x: x.asof(CONFIG.INTRADAYMASTERCLOCK.MasterClock))    
    
    df['sidedAmount'].iloc[1:] = df['sidedAmountRolling'].diff()
    df['amount'].iloc[1:] = df['amountRolling'].diff()    
    
    ################################################################
    # Note, Price, Amount, Volume Columns Are All On the Log Scale #
    ################################################################
    #    df = df.rename(columns = {'price': 'logPrice', 'amount' : 'logAmount', 'amountRolling': 'LogAmountRolling', 'volumeRolling' : 'LogVolumeRolling'})
    
    # Take log of price, amount
    for col in ['price', 'amount', 'amountRolling', 'sidedAmount', 'sidedAmountRolling']:
        df[col] = np.log(abs(df[col])) * (df[col] / abs(df[col]))
   
    return df
    
def SecondDataProcessing(df):
    """
    Generate 3 second master clock, as of join.
    Add the following features:
        /pendBuyRatio/:  Wei Bi (sum top five buy limit order volume - sum top five sell limit order volume) / (buy + sell)
    """
    df['pendingBuyVolume'] = df['buy1Volume'] + df['buy2Volume'] + df['buy3Volume'] + df['buy4Volume'] + df['buy5Volume']
    df['pendingSellVolume'] = df['sell1Volume'] + df['sell2Volume'] + df['sell3Volume'] + df['sell4Volume'] + df['sell5Volume']
    df['pendingBuyRatio'] = (df['pendingBuyVolume'] - df['pendingSellVolume']) / (df['pendingBuyVolume'] + df['pendingSellVolume']) 
    df = DropColumn(df, ['exchange', 'ticker', 'pendingBuyVolume', 'pendingSellVolume', 'buy1Volume', 'buy2Volume', 'buy3Volume', 'buy4Volume', 'buy5Volume', 'sell1Volume', 'sell2Volume', 'sell3Volume', 'sell4Volume', 'sell5Volume', 'price'])    
    ### TODO: Note, at the moment is pulling the date info from the dataframe
    Date = df['time'].iloc[0].date()
    MasterClock = AddDateToIntradayMasterClock(Date, CONFIG.INTRADAYMASTERCLOCK)
    # Asof join by MasterClock
    df = df.set_index('time')
    df = df.apply(lambda x: x.asof(MasterClock.MasterClock))
    return df

def IndexDataProcessing(df):
    """
    Process the index data, generate 3 second master clock, as of join.
    Output:
        /df/: datetime index, price column
    """
    df = DropColumn(df, ['volume'])    
    Date = df['time'].iloc[0].date()
    MasterClock = AddDateToIntradayMasterClock(Date, CONFIG.INTRADAYMASTERCLOCK)
    # Asof join by MasterClock
    df = df.set_index('time')
    df = df.apply(lambda x: x.asof(MasterClock.MasterClock))
    df['price'] = np.log(df['price'])
    return df
