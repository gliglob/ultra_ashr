"""
Modification 3:
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
