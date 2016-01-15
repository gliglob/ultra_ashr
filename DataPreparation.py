"""
Data Preparation
"""

from SetUp import *
from HelperFunctions import *
from DataProcessing import *
from DataCleaning import *
from FeaturePreparation import *
from VwapFeaturePreparation import *
from Config import CONFIG
logging.info('Setting up...')

# Tick Data Example

DailyData = CONFIG.DAILYDATAFRAME.copy()


stock = CONFIG.STOCK[0]
# Make directory for stock to save processed data
if not os.path.exists(CONFIG.PROCESSEDFOLDERPATH%stock):
    os.makedirs(CONFIG.PROCESSEDFOLDERPATH%stock)

#########################
# Read and Process Data #
#########################

logging.warning('Reading and Processing Data Start... For Stock %s From %s To %s...'%(stock, CONFIG.TRADINGDAYS[0], CONFIG.TRADINGDAYS[-1]))

for date in CONFIG.TRADINGDAYS:
    TickDataPath = CONFIG.TICKDATAPATH%(date[:-2], date, stock)
    SecondDataPath = CONFIG.SECONDDATAPATH%(date[:-2], date, stock, date)
    _checker = 0
    while _checker <= 2:
        _checker += 1
        try: 
            STARTTIME = time.time()
            df_tick = pd.read_csv(TickDataPath, header = None, names = ['time', 'price', 'side', 'volume'])
            length1 = len(df_tick)
            df_tick = TickDataCleaning(df_tick)
            if len(df_tick) - length1 > 10:
                logging.warning('Tick Data for %s on %s contains more than 10 NA or outlier values'%(stock, date))
            df_tick = TickDataProcessing(df_tick)
                
            # Second Data Example
            
            df_sec = pd.read_csv(SecondDataPath, header = 0, 
                names = ['exchange', 'ticker', 'time', 'price', 'count', 'amount', 'volume', 'side',
                'buy1', 'buy2', 'buy3', 'buy4', 'buy5',
                'sell1', 'sell2', 'sell3', 'sell4', 'sell5',
                'buy1Volume', 'buy2Volume', 'buy3Volume', 'buy4Volume', 'buy5Volume',
                'sell1Volume', 'sell2Volume', 'sell3Volume', 'sell4Volume', 'sell5Volume'])
            
            length1 = len(df_sec)
            df_sec = SecondDataCleaning(df_sec)
            if len(df_sec) - length1 > 5:
                logging.warning('Second Data for %s on %s contains more than 5 NA and outlier values'%(stock, date))
            df_sec = SecondDataProcessing(df_sec)
            
            
            # Concat Tick and Second Data
            Date = df_sec.index[0].date()
            df_tick.index = df_tick.index.map(lambda x: datetime.datetime.combine(Date, x))
            df = pd.concat([df_sec, df_tick], axis = 1)
            
            df.index.name = 'time'    
            
            # Save Processed Daily Intraday 3sec Data
            df.to_csv(CONFIG.PROCESSEDDATAPATH%(stock, date))

            ENDTIME = time.time()
            logger.info('Stock: %s, Date: %s, Time to Process: %f sec'%(stock, date, ENDTIME-STARTTIME))
            break
        except Exception, e:
            if _checker == 1:
                logging.warning(str(e))
            if _checker >= 3:
                if (not os.path.isfile(TickDataPath)) or (not os.path.isfile(SecondDataPath)):
                    logging.warning('Data for %s is missing on %s when reading data'%(stock, date))
                else:
                    logging.warning('Other Critical Error When Reading and Processing Data of %s on %s'%(stock, date))


#######################
# Feature Preparation #
#######################

logging.warning('Standard Feature Preparation Start... For Stock %s From %s To %s...'%(stock, CONFIG.TRADINGDAYS[0], CONFIG.TRADINGDAYS[-1]))

IndustryIndex = CONFIG.STOCKINDUSTRYINDEXMAP.IndustryCode[stock]
Index = CONFIG.STOCKINDUSTRYINDEXMAP.IndexCode[stock]
logging.info('The corresponding industry index for stock %s is %s'%(stock, IndustryIndex))
logging.info('The corresponding index for stock %s is %s'%(stock, Index))

for date in CONFIG.TRADINGDAYS:
    ProcessedDataPath = CONFIG.PROCESSEDDATAPATH%(stock, date)
    try:
        STARTTIME = time.time()  
        df = pd.read_csv(ProcessedDataPath, index_col = 'time')
        df.index = TimeWrapper3(df.index)
        # Prepare daily signals
        # TODO Prepare data by session
        
        # backkfill missing data for df
        df = df.fillna(method = 'bfill')
        if df.iloc[-1].isnull().any():
            DailyData.loc[df.index[-1]] = [None] * (len(CONFIG.FEATURES) - 1) + ['N']
            logging.warning('Data is missing in some fields for processed data of %s on %s, set IncludedInTraining to N'%(stock, date))
        else:
            DailyData = FeaturePreparation(df, stock, IndustryIndex, Index, DailyData)
            DailyData.index.name = 'Time'
        
        ENDTIME = time.time()
        logger.info('Stock: %s, Date: %s, Time to Prepare Feature: %f sec'%(stock, date, ENDTIME-STARTTIME))
    except Exception, e:
        logging.warning(str(e))
        if (not os.path.isfile(ProcessedDataPath)):
            logging.warning('Data for %s is missing on %s when preparing features'%(stock, date))
        else:
            logging.warning('Other Critical Error When Preparing Features for %s on %s'%(stock, date))
    
_checker = 0
while _checker <= 2:
    _checker += 1
    try:
        DailyData.to_csv(CONFIG.DAILYDATAPATH%stock)
        break
    except Exception, e:
        if _checker == 1:
            logging.warning(str(e))
        if _checker >= 3:
            logging.warning('Other Critical Error When Saving Data of %s'%stock)

#####################
# VWAP Feature Prep #
#####################

DailyVwapData = CONFIG.DAILYVWAPDATAFRAME.copy()

logging.warning('VWAP Feature Preparation Start... For Stock %s From %s To %s...'%(stock, CONFIG.TRADINGDAYS[0], CONFIG.TRADINGDAYS[-1]))

IndustryIndex = CONFIG.STOCKINDUSTRYINDEXMAP.IndustryCode[stock]
Index = CONFIG.STOCKINDUSTRYINDEXMAP.IndexCode[stock]
logging.info('The corresponding industry index for stock %s is %s'%(stock, IndustryIndex))
logging.info('The corresponding index for stock %s is %s'%(stock, Index))

for date in CONFIG.TRADINGDAYS:
    ProcessedDataPath = CONFIG.PROCESSEDDATAPATH%(stock, date)
    try:
        STARTTIME = time.time()  
        df = pd.read_csv(ProcessedDataPath, index_col = 'time')
        df.index = TimeWrapper3(df.index)
        # Prepare daily signals
        # TODO Prepare data by session
        
        # backkfill missing data for df
        df = df.fillna(method = 'bfill')
        if df.iloc[-1].isnull().any():
            DailyVwapData.loc[df.index[-1]] = [None] * (len(CONFIG.VWAPFEATURES))
            logging.warning('Data is missing in some fields for processed data of %s on %s, set IncludedInTraining to N'%(stock, date))
        else:
            DailyVwapData = VwapFeaturePreparation(df, stock, IndustryIndex, Index, DailyVwapData)
            DailyVwapData.index.name = 'Time'
        
        ENDTIME = time.time()
        logger.info('Stock: %s, Date: %s, Time to Prepare Feature: %f sec'%(stock, date, ENDTIME-STARTTIME))
    except Exception, e:
        logging.warning(str(e))
        if (not os.path.isfile(ProcessedDataPath)):
            logging.warning('Data for %s is missing on %s when preparing features'%(stock, date))
        else:
            logging.warning('Other Critical Error When Preparing Features for %s on %s'%(stock, date))
    
_checker = 0
while _checker <= 2:
    _checker += 1
    try:
        DailyVwapData.to_csv(CONFIG.DAILYVWAPDATAPATH%stock)
        break
    except Exception, e:
        if _checker == 1:
            logging.warning(str(e))
        if _checker >= 3:
            logging.warning('Other Critical Error When Saving Data of %s'%stock)
