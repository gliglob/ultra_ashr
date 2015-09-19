from __future__ import division
import pandas as pd

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
    def WilliamR(self, 
    

def main():
    # Example
    df = pd.DataFrame({'a':[1,2,4,5,9],'b':[2,3,1,6,15], 'c':[3,4,10,8,17]})
