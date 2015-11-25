"""
Index Preparation - Prepares the Following Index
SH Composite Index SH 000001
CSI 300/800/1000
Industry Index
"""

def IndexPreparation(TradingDays):
    
IndexList = ['SH000908']

for index in IndexList:
    for day in TradingDays:
        IndexPath = './ASHR/DATA/Test/%s_%s.csv'%(index, day)
        df_index = pd.read_csv(IndexPath, header = 0, 
            names = ['exchange', 'ticker', 'time', 'price', 'count', 'amount', 'volume', 'side',
            'buy1', 'buy2', 'buy3', 'buy4', 'buy5',
            'sell1', 'sell2', 'sell3', 'sell4', 'sell5',
            'buy1Volume', 'buy2Volume', 'buy3Volume', 'buy4Volume', 'buy5Volume',
            'sell1Volume', 'sell2Volume', 'sell3Volume', 'sell4Volume', 'sell5Volume'])
        
        df_index = IndexDataCleaning(df_index)
        df_index = IndexDataProcessing(df_index, IntradayMasterClock)
        return df_index
