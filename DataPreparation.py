"""
Data Preparation
"""

from SetUp import *
from HelperFunctions import *
from DataProcessing import *
from DataCleaning import *
from FeaturePreparation import *
logging.info('Setting up...')

# Tick Data Example

TradingDays = GenerateMasterClock(datetime.date(2015, 9, 1), datetime.date(2015, 9, 7), '1d', TradingHours, HolidayList).MasterClock
TradingDays = TradingDays.map(lambda x: x.strftime('%Y%m%d')).tolist()

DailyData = DailyDataFrame.copy()


stock = 'SH600000'
# Make directory for stock to save processed data
if not os.path.exists('./ASHR/DATA/Processed/%s/'%stock):
    os.makedirs('./ASHR/DATA/Processed/%s/'%stock)

#########################
# Read and Process Data #
#########################

logging.warning('Reading and Processing Data Start... For Stock %s From %s To %s...'%(stock, TradingDays[0], TradingDays[-1]))
#date = TradingDays[0]
for date in TradingDays:
    TickDataPath = './ASHR/DATA/Test/Test_Tick/%s/%s/%s.csv'%(date[:-2], date, stock)
    SecondDataPath = './ASHR/DATA/Test/Test_Second/%s/%s/%s_%s.csv'%(date[:-2], date, stock, date)

    try: 
        STARTTIME = time.time()
        df_tick = pd.read_csv(TickDataPath, header = None, names = ['time', 'price', 'side', 'volume']
        length1 = len(df_tick)
        df_tick = TickDataCleaning(df_tick)
        if len(df_tick) - length1 > 100:
            logging.warning('Tick Data for %s on %s contains more than 100 NA values'%(stock, date))
        df_tick = TickDataProcessing(df_tick, IntradayMasterClock)
            
        # Second Data Example
        
        df_sec = pd.read_csv(SecondDataPath, header = 0, 
            names = ['exchange', 'ticker', 'time', 'price', 'count', 'amount', 'volume', 'side',
            'buy1', 'buy2', 'buy3', 'buy4', 'buy5',
            'sell1', 'sell2', 'sell3', 'sell4', 'sell5',
            'buy1Volume', 'buy2Volume', 'buy3Volume', 'buy4Volume', 'buy5Volume',
            'sell1Volume', 'sell2Volume', 'sell3Volume', 'sell4Volume', 'sell5Volume'])
        
        length1 = len(df_sec)
        df_sec = SecondDataCleaning(df_sec)
        if len(df_sec) - length1 > 100:
            logging.warning('Second Data for %s on %s contains more than 100 NA values'%(stock, date))
        df_sec = SecondDataProcessing(df_sec, IntradayMasterClock)
        
        
        # Concat Tick and Second Data
        Date = df_sec.index[0].date()
        df_tick.index = df_tick.index.map(lambda x: datetime.datetime.combine(Date, x))
        df = pd.concat([df_sec, df_tick], axis = 1)
        
        df.index.name = 'time'    
        
        # Save Processed Daily Intraday 3sec Data
        df.to_csv('./ASHR/DATA/Processed/%s/%s.csv'%(stock, date))
        
        ENDTIME = time.time()
        logger.info('Stock: %s, Date: %s, Time to Process: %f sec'%(stock, date, ENDTIME-STARTTIME))
    except Exception:
        if (not os.path.isfile(TickDataPath)) or (not os.path.isfile(SecondDataPath)):
            logging.warning('Data for %s is missing on %s when reading data'%(stock, date))
        else:
            logging.warning('Other Critical Error When Reading and Processing Data of %s on %s'%(stock, date))


#######################
# Feature Preparation #
#######################

logging.warning('Standard Feature Preparation Start... For Stock %s From %s To %s...'%(stock, TradingDays[0], TradingDays[-1]))

for date in TradingDays:
    ProcessedDataPath = './ASHR/DATA/Processed/%s/%s.csv'%(stock, date)
    try:
        STARTTIME = time.time()  
        df = pd.read_csv(ProcessedDataPath, index_col = 'time')
        df.index = TimeWrapper3(df.index)
        # Prepare daily signals
        # TODO Prepare data by session
        DailyData = FeaturePreparation(df, DailyData, HolidayList)
        
        ENDTIME = time.time()
        logger.info('Stock: %s, Date: %s, Time to Prepare Feature: %f sec'%(stock, date, ENDTIME-STARTTIME))
    except Exception:
        if (not os.path.isfile(ProcessedDataPath)):
            logging.warning('Data for %s is misisng on %s when preparing features'%(stock, date))
        else:
            logging.warning('Other Critical Error When Preparing Features for %s on %s'%(stock, date))
            

##########################
# Add Additional Feature #
##########################
FeatureToAdd = 'SpreadToIndustry'
DailyData[FeatureToAdd] = None

for date in TradingDays:
    


