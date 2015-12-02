from SetUp import *

# Indicator
class Indicator():
    
    # Assuming the data type of Data is in pd.DataFrame
    # Note, the index will be the time stamp
    def __init__(self, Data):
        self.DF = Data
        self.length = self.DF.shape[0]
        
    # Stochstic oscillator
    def StochasticOscillator(self, K_Scale, D_Scale, DSlow_Scale):
        '''
        Stochastic oscillator: comparing current price in relation to its price range over a period of time
        Input: 
            /K_Scale/     The time range that we look back to compute K
            /D_Scale/     The number of %K that we look at to compute %D
        NOTE: 
            length of self.K = self.length - K_Scale + 1
            length of self.D = len(self.K) - D_Scale + 1
        
        TODO: D is calculated using SMA of K right now
        '''
        Current = self.DF[K_Scale-1:]
        Low = pd.rolling_min(self.DF, K_Scale)[K_Scale-1:]
        High = pd.rolling_max(self.DF, K_Scale)[K_Scale-1:]
        self.K = 100 * ( Current - Low) / (High - Low)
        
        self.D = pd.rolling_mean(self.K, D_Scale)[D_Scale-1:]
        self.DSlow = pd.rolling_mean(self.D, DSlow_Scale)[DSlow_Scale-1:]
    
        return self.K, self.D, self.DSlow
    
    # Larry William %R
    def WilliamR(self, Scale):
        '''
        Larry William %R: on a negative scale from -100 to 0
        -100: today was lowest low of past N days (oversold)
        '''
        Current = self.DF[Scale-1:]
        Low = pd.rolling_min(self.DF, Scale)[Scale-1:]
        High = pd.rolling_max(self.DF, Scale)[Scale-1:]
        self.WilliamR = -100 * ( High - Current ) / (High - Low)
    
        return self.WilliamR
    

# RSI index

def RSI(df, Scale):
    from tools.filter_construction import Filter
    df['U'] = (df['Close'] - df['Close'].shift(1)).map(lambda x: x if x > 0 else 0)
    df['D'] = (df['Close'] - df['Close'].shift(1).map(lambda x: -x if x < 0 else 0)
    M1 = Scale
    RS = Filter('U', df['U'], M1, 'pmea') / Filter('D', df['D'], M1, 'pmea')
    RSI = 100 - 100 / (1 + RS)
    return RSI

# CCI index

def CCI(df, Scale):
    
    

class TradeData():
    
    def __init__(self, Data):
        self.DF = Data
        

def main():
    # Example
    df = pd.DataFrame({'a':[1,2,4,5,9],'b':[2,3,1,6,15], 'c':[3,4,10,8,17]})
    df2 = pd.DataFrame({'a':[1,2,4,5,9],'bb':['a','b','c','d','e'], 'c':[3,4,10,8,18]})
    df.reset_index()
