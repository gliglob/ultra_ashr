"""
Modification 1:
    Set all data files under Processed Data folder, 
"""

from Config import CONFIG
from SetUp import *

for stock in CONFIG.STOCK:
    
    
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

