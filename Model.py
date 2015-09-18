import pandas as pd

# Indicator
class Indicator():
    
    # Assuming the data type of Data is in pd.DataFrame
    # Note, the index will be the time stamp
    def __init__(self, Data):
        self.DF = Data
        self.length = self.DF.shape[0]
    # Stochstic oscillator
    def StochasticOscillator(self, K_Scale, D_Scale):
        '''
        Stochastic oscillator: comparing current price in relation to its price range over a period of time
        Input: 
            /K_Scale/     The time range that we look back to compute K
            /D_Scale/     The number of %K that we look at to compute %D
        '''
        Current = self.DF.iloc[0:(len(self.DF)-K_Scale)]
        Low = [self.DF.iloc[x: (x+K_Scale)] for x in range(K_Scale, len(self.DF))]
        
        self.K = 100 * ( Current -
