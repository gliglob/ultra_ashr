"""
Implement the strategy, return the exit postion and return for a given stock
"""

from SetUp import *
from HelperFunctions import *
from Config import CONFIG

def Strategy1(Stock, EnterDate, EnterPrice, TradingHorizon, StopLossThresh, MaxProfitThresh, SellThresh):
    """
    Strategy1:
        Enter position: Open price on enter_date
        Close position: 
            Case 1: Stop loss: Current Price - Enter Price >= %StopLossThresh (Default = 0.1)
            Case 2: Max Profit: Current Profit - Max Profit <= %MaxProfitThresh (Default = 0.1)
            Case 3: Sell at Close at the end of Trading Horizon
    Input:
        /Stock/  stock ticker
        /EnterDate/ datetime.date date of entering the long 1 position
        /EnterPrice/ enter price
        /TradingHorizon/ trading horizon, default = 5
        /StopLossThresh/ stop loss cutoff in percentage, default = 0.1
        /MaxProfitThreush/ max profit cutoff in percentage, default = 0.1
        /SellThresh/ min abs return to achieve before selling
    Output:
        /ExitPosition/ datetime.datetime date time of closing the long 1 position
        /Return/ %Return (Price at Exit Position - Enter Price)
    """

    # NOTE, to avoid the situations of not able to sell, return is set to 0 and position = False automatically after max holding period expires
    MaxHoldingDay = max(10, 2 * TradingHorizon)
    # Trading Day represents the nth trading day. Note TradingDay starts at 1 since ASHR is T+1
    HoldingDay = 0
    MaxReturn = -StopLossThresh   
    
    while True:
        
        if HoldingDay == MaxHoldingDay:
                logging.warning('Strategy1 testing for %s... max holding days %d expires for stock %s on %s, manually setting return to 0 '%(EnterDate, MaxHoldingDay, Stock, CurrentDay))
                ExitPosition = None
                Return = 0
                break
        
        CurrentDay = AddBusinessDay(EnterDate, HoldingDay).strftime('%Y%m%d')
        DataPath = CONFIG.PROCESSEDDATAPATH%(Stock, CurrentDay)
        
        if os.path.isfile(DataPath):
            CurrentData = pd.read_csv(DataPath, index_col = 'time')
            CurrentData['return'] = np.exp(CurrentData['price'] - EnterPrice) - 1
            CurrentData['maxreturn'] = pd.rolling_max(CurrentData['return'], len(CurrentData), min_periods = 1)
            CurrentData.maxreturn[CurrentData.maxreturn < MaxReturn] = MaxReturn
            if HoldingDay > 0:
                CurrentData['drawdown'] = (CurrentData['return'] - CurrentData['maxreturn']) / CurrentData['maxreturn']
                CurrentData['drawdown'][CurrentData['maxreturn'] == 0] = CurrentData['return'] - CurrentData['maxreturn']
                Resulting = CurrentData.loc[((CurrentData['drawdown'] < -MaxProfitThresh) | (CurrentData['return'] < -StopLossThresh)) & (abs(CurrentData['return']) >= SellThresh)]           
                if not Resulting.empty:
                    ExitPosition = Resulting.index[0]
                    Return = Resulting['return'].loc[ExitPosition]
                    break
                
            MaxReturn = CurrentData['maxreturn'].max() 
            HoldingDay += 1
            if HoldingDay == TradingHorizon:
                ExitPosition = CurrentData.index[-1]
                Return = CurrentData['return'].loc[ExitPosition]
                break

            elif HoldingDay > TradingHorizon:
                logging.warning('Strategy1 testing for %s... Holding Days Exceed Trading Horizon for stock %s, selling at open on %s, holding days = %d'%(EnterDate, Stock, CurrentDay, HoldingDay))
                ExitPosition = CurrentData.index[0]
                Return = CurrentData['return'].loc[ExitPosition]
                break
            
        else:
            logging.warning('Strategy1 testing for %s... Stock %s is closed on %s'%(EnterDate, Stock, CurrentDay))
            HoldingDay += 1

    return Return, ExitPosition


def Strategy2(Stock, EnterDate, EnterPrice, TradingHorizon):
    """
    Strategy2:
        Enter position: Open price on enter_date
        Close position: Open price on the next trading day
    Input:
        /Stock/  stock ticker
        /EnterDate/ datetime.date date of entering the long 1 position
        /EnterPrice/ enter price
        /TradingHorizon/ trading horizon, default = 1
    Output:
        /Return/ %Return (Price at Exit Position - Enter Price)
        /ExitPosition/ datetime.datetime date time of closing the long 1 position
    """
    
    MaxHoldingDay = max(10, 2 * TradingHorizon)
    HoldingDay = TradingHorizon
    CurrentDay = AddBusinessDay(EnterDate, TradingHorizon)
    DataPath = CONFIG.PROCESSEDDATAPATH%(Stock, CurrentDay.strftime('%Y%m%d'))
    Return = 0
    ExitPosition = None
    while True:
        
        if HoldingDay == MaxHoldingDay:
            logging.warning('Strategy2 testing for %s... max holding days %d expires for stock %s on %s, manually setting return to 0 '%(EnterDate, MaxHoldingDay, Stock, CurrentDay))
            ExitPosition = None
            Return = 0
            break
        if os.path.isfile(DataPath):
            if HoldingDay > TradingHorizon:
                logging.warning('Strategy2 testing for %s... Holding Days Exceed Trading Horizon for stock %s, selling at open on %s, holding days = %d'%(EnterDate, Stock, CurrentDay, HoldingDay))
            CurrentData = pd.read_csv(DataPath, index_col = 'time')
            ExitPosition = CurrentData.index[0]
            Return = np.exp(CurrentData['price'].iloc[0] - EnterPrice) - 1
            break
        else:
            logging.warning('Strategy2 testing for %s... Stock %s is closed on %s'%(EnterDate, Stock, CurrentDay))
            CurrentDay = AddBusinessDay(CurrentDay, 1)
            DataPath = CONFIG.PROCESSEDDATAPATH%(Stock, CurrentDay.strftime('%Y%m%d'))
            HoldingDay += 1

    return Return, ExitPosition
