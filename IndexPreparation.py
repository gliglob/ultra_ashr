"""
Index Preparation - Prepares the Following Index
SH Composite Index SH 000001
CSI 300/800/1000
Industry Index
"""

    
IndexList = pd.read_csv('./ASHR/DATA/Index/Index/IndustryIndexPrep/Industry_Category_to_Code.csv')['Code']


for index in IndexList:
    for date in TradingDays:
        if not os.path.exists('./ASHR/DATA/Index/Processed/%s/'%index):
            os.makedirs('./ASHR/DATA/Index/Processed/%s/'%index)
        IndexPath = '/Volumes/Hui/Stk_Tick/Stk_Tick_%s/Stk_Tick_%s/%s/%s_%s.csv'%(date[:4], date[:-2], date, index, date)
        df_index = pd.read_csv(IndexPath, header = 0, 
            names = ['exchange', 'ticker', 'time', 'price', 'count', 'amount', 'volume', 'side',
            'buy1', 'buy2', 'buy3', 'buy4', 'buy5',
            'sell1', 'sell2', 'sell3', 'sell4', 'sell5',
            'buy1Volume', 'buy2Volume', 'buy3Volume', 'buy4Volume', 'buy5Volume',
            'sell1Volume', 'sell2Volume', 'sell3Volume', 'sell4Volume', 'sell5Volume'])
        
        df_index = IndexDataCleaning(df_index)
        df_index = IndexDataProcessing(df_index)
        df_index.to_csv('./ASHR/DATA/Index/Processed/%s/%s.csv'%(index, date))
