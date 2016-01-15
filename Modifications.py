"""
Modification 1:
    Change the first row of the processed data, column sidedAmount and amount to match sidedAmountRolling and amountRolling
"""

from Config import CONFIG
from SetUp import *

for stock in STOCK:
    
    
    #########################
    # Read and Process Data #
    #########################
    
    logging.warning('Reading Data Start... For Stock %s From %s To %s...'%(stock, CONFIG.TRADINGDAYS[0], CONFIG.TRADINGDAYS[-1]))
    
    for date in CONFIG.TRADINGDAYS:
        ProcessedDataPath = CONFIG.PROCESSEDDATAPATH%(stock, date)
        
        _checker = 0
        while _checker <= 2:
            _checker += 1
            try: 
                # Save Processed Daily Intraday 3sec Data
                df = pd.read_csv(ProcessedDataPath, index_col = 'time')
                df['sidedAmount'].iloc[0] = df['sidedAmountRolling'].iloc[0]
                df['amount'].iloc[0] = df['amountRolling'].iloc[0]
                df.to_csv(CONFIG.PROCESSEDDATAPATH%(stock, date))
                break
            except Exception, e:
                if _checker == 1:
                    logging.warning(str(e))
                if _checker >= 3:
                    if (not os.path.isfile(ProcessedDataPath)):
                        logging.warning('Data for %s is missing on %s when reading data'%(stock, date))
                    else:
                        logging.warning('Other Critical Error When Reading Data of %s on %s'%(stock, date))

"""
Modification 2:
    Add the volume column from raw tick data to processed data to prepare the VWAP
"""

for stock in CONFIG.STOCK:
    #########################
    # Read and Process Data #
    #########################
    logging.warning('Reading Data Start... For Stock %s From %s To %s...'%(stock, CONFIG.TRADINGDAYS[0], CONFIG.TRADINGDAYS[-1]))

    for date in CONFIG.TRADINGDAYS:
        TickDataPath = CONFIG.TICKDATAPATH%(date[:4], date[:-2], date, stock)
        ProcessedDataPath = CONFIG.PROCESSEDDATAPATH%(stock, date)
        _checker = 0
        while _checker <= 2:
            _checker += 1
            try: 
                STARTTIME = time.time()  
                df_tick = pd.read_csv(TickDataPath, header = None, names = ['time', 'price', 'side', 'volume'])
                df_tick = TickDataCleaning(df_tick)
                
                df_tick['volumeRolling'] = df_tick['volume'].cumsum()
                 
                df_tick = df_tick.set_index('time')
                df_tick = df_tick.apply(lambda x: x.asof(CONFIG.INTRADAYMASTERCLOCK.MasterClock)) 
                
                ### Note, volume and volumeRolling are not in log form
                df_tick['volume'].iloc[1:] = df_tick['volumeRolling'].diff()
                df_tick['volume'].iloc[0] = df_tick['volumeRolling'].iloc[0]                
                
                # Read Processed data
                df = pd.read_csv(ProcessedDataPath, index_col = 0)
                df.index.Name = 'time'
                df.index = TimeWrapper3(df.index)                
                
                Date = df.index[0].date()                
                df_tick.index = df_tick.index.map(lambda x: datetime.datetime.combine(Date, x))
                df = pd.concat([df, df_tick[['volume', 'volumeRolling']]], axis = 1)
                
                # Save Processed Daily Intraday 3sec Data
                df.to_csv(CONFIG.PROCESSEDDATAPATH%(stock, date), index_label = 'time')
                ENDTIME = time.time()
                logger.info('Stock: %s, Date: %s, Time to Process: %f sec'%(stock, date, ENDTIME-STARTTIME))
                break
            except Exception, e:
                if _checker == 1:
                    logging.warning(str(e))
                if _checker >= 3:
                    if (not os.path.isfile(TickDataPath)) or (not os.path.isfile(ProcessedDataPath)):
                        logging.warning('Data for %s is missing on %s when reading data'%(stock, date))
                    else:
                        logging.warning('Other Critical Error When Processing Data of %s on %s'%(stock, date))


"""
Modification 3:
# Add index CSI 300 CSI 800 CSI ALL
# CSI300: SH000300
# CSI800: SH000906
# CSIALL: SH000985
"""

IndexList = ['SH000300', 'SH000906', 'SH000985']
for index in IndexList:
    if not os.path.exists('./DATA/Index/Processed/%s/'%index):
        os.makedirs('./DATA/Index/Processed/%s/'%index)
    for date in CONFIG.TRADINGDAYS:
        IndexPath = './DATA/Stk_Tick/Stk_Tick_%s/Stk_Tick_%s/%s/%s_%s.csv'%(date[:4], date[:-2], date, index, date)
        _checker = 0
        while _checker <= 2:
            _checker += 1
            try:
                df_index = pd.read_csv(IndexPath, header = 0, 
                    names = ['exchange', 'ticker', 'time', 'price', 'count', 'amount', 'volume', 'side',
                    'buy1', 'buy2', 'buy3', 'buy4', 'buy5',
                    'sell1', 'sell2', 'sell3', 'sell4', 'sell5',
                    'buy1Volume', 'buy2Volume', 'buy3Volume', 'buy4Volume', 'buy5Volume',
                    'sell1Volume', 'sell2Volume', 'sell3Volume', 'sell4Volume', 'sell5Volume'])
                df_index = IndexDataCleaning(df_index)
                df_index = IndexDataProcessing(df_index)
                df_index.to_csv(CONFIG.INDEXDATAPATH%(index, date))
                break
            except Exception, e:
                if _checker == 1:
                    logging.warning(str(e))
                if _checker >= 3:
                    if not os.path.isfile(IndexPath):
                        logging.warning('Data for %s is missing on %s when reading data'%(index, date))
                    else:
                        logging.warning('Other Critical Error When Processing Data of %s on %s'%(index, date))

"""
Modification 4:
    pull volume and volume rolling for sz000001
"""
stock = 'SZ000001'
for date in CONFIG.TRADINGDAYS:
    ProcessedDataPath = CONFIG.PROCESSEDDATAPATH%(stock, date)
    _checker = 0
    while _checker <= 2:
        _checker += 1
        try: 
            # Save Processed Daily Intraday 3sec Data
            df = pd.read_csv(ProcessedDataPath, index_col = 'time')
            df = df[['volume', 'volumeRolling']]
            df.to_csv('/Users/Hui/Desktop/Volume_SZ000001/%s'%date)
            break
        except Exception, e:
            if _checker == 1:
                logging.warning(str(e))
            if _checker >= 3:
                if (not os.path.isfile(ProcessedDataPath)):
                    logging.warning('Data for %s is missing on %s when reading data'%(stock, date))
                else:
                    logging.warning('Other Critical Error When Reading Data of %s on %s'%(stock, date))
                    

"""
Modification 5:
    selecting the proper subset of columns for SZ000001
"""
stock = 'SZ000001'
for date in CONFIG.TRADINGDAYS:
    ProcessedDataPath = CONFIG.PROCESSEDDATAPATH%(stock, date)
    _checker = 0
    while _checker <= 2:
        _checker += 1
        try: 
            # Save Processed Daily Intraday 3sec Data
            df = pd.read_csv(ProcessedDataPath, index_col = 'time')
            df.index = TimeWrapper3(df.index)
            df = df[['pendingBuyRatio', 'price', 'volume', 'amount', 'amountRolling', 
                     'volumeRolling', 'buyRatio', 'A_buyRatio', 'B_buyRatio', 'sidedAmount', 
                     'sidedAmountRolling', 'volume', 'volumeRolling']]
            df.to_csv(CONFIG.PROCESSEDDATAPATH%(stock, date), index_label = 'time')
            break
        except Exception, e:
            if _checker == 1:
                logging.warning(str(e))
            if _checker >= 3:
                if (not os.path.isfile(ProcessedDataPath)):
                    logging.warning('Data for %s is missing on %s when reading data'%(stock, date))
                else:
                    logging.warning('Other Critical Error When Reading Data of %s on %s'%(stock, date))
       
