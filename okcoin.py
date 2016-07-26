import json
import requests
import datetime, time
import pandas as pd
import logging
import MySQLdb as sql
#import multiprocessing
import threading

symbol = 'btc_usd'
BTCTickDataPath = '/Users/hui/Desktop/%s_BTCTickData.csv'
BTCDepthDataPath = '/Users/hui/Desktop/%s_BTCDepthData.csv'

#symbol2 = 'okcoinCNY'
#p = requests.get('http://www.quandl.com/api/v3/datasets/BCHARTS/OKCOINCNY')


class OKCoinSpot(object):
    
    def __init__(self, product, exchange, url_tick='', url_candlestick='', url_depth='', symbol=''):
        self._symbol = symbol
        self.product = product
        self.exchange = exchange
        self.url_tick = url_tick
        self.url_candlestick = url_candlestick
        self.url_depth = url_depth
        self.CurrentTick = {}
        self.CurrentOrderBook = None
        self.BTCTickData = pd.DataFrame(columns=['date', 'last', 'high', 'low', 'buy', 'sell', 'vol'])
#        self.BTCDepthData = pd.DataFrame(columns=list(chain.from_iterable(('askPrice%s'%i, 'askVol%s'%i, 'bidPrice%s'%i, 'bidVol%s'%i) for i in range(1, 31))))
        self.BTCDepthData = pd.DataFrame(columns=['askPrice%s'%i for i in range(1, 31)] + ['askVol%s'%i for i in range(1, 31)] + ['bidPrice%s'%i for i in range(1, 31)] + ['bidVol%s'%i for i in range(1, 31)])
        self.currentDate = time.time()
        self.db = sql.connect(host='localhost', user='root', db='bitcoin')
        self.db.autocommit(True)
        self.cursor = self.db.cursor()
        self.mysqlQuery = ''
        
    def Tick(self):
        """
        This combines data from the candlestick and tick data
        /tick data/
        date: current datetime
        buy:  best bid
        sell: best ask
        high: high in rolling 24hours
        low:  low in rolling 24hours
        /candlestick data/
        date1min: most recent 1min datetime
        open1min: open for 1min data
        high1min: high in 1min
        low1min: low in 1min
        close1min: close for 1min data
        vol1min: volume in 1min
        """
        logging.info('Requesting from %s'%self.exchange)
        # get the most recent trade price
        p = requests.get(self.url_tick%self._symbol)
        json_data = json.loads(p.text.decode('utf-8'))
        json_data['date'] = datetime.datetime.fromtimestamp(int(json_data['date'])).strftime('%Y-%m-%d %H:%M:%S')
        self.CurrentDate = json_data['date']
        json_data.update(json_data['ticker'])
        json_data.pop('ticker')
#        json_data = pd.DataFrame(json_data.items()).set_index(0)
#        self.BTCTickData.loc[len(self.BTCTickData)] = [json_data.loc[i][1] for i in self.BTCTickData.columns]
        # get the most recent 1min candle stick        
        p = requests.get(self.url_candlestick%self._symbol)
        json_candlestick = json.loads(p.text.decode('utf-8'))[0]
        json_data['date1min'] = datetime.datetime.fromtimestamp(int(json_candlestick[0])/1000).strftime('%Y-%m-%d %H:%M:%S')
        json_data['open1min'] = json_candlestick[1]
        json_data['high1min'] = json_candlestick[2]
        json_data['low1min']  = json_candlestick[3]
        json_data['close1min'] = json_candlestick[4]
        json_data['vol1min'] =  json_candlestick[5]
        self.CurrentTick = json_data
    
    def SaveUpdatedBTCTickData(self, BTCTickDataPath):
        self.BTCTickData.to_csv(BTCTickDataPath%self._symbol, index=False)
    
    def Depth(self):
        # get the most recent order book
        # only save level 30 order book
        p = requests.get(self.url_depth%self._symbol)
        json_data = json.loads(p.text.decode('utf-8'))
        json_data['asks'] = zip(*json_data['asks'])
        json_data['bids'] = zip(*json_data['bids'])
        df = pd.DataFrame(data={'askPrice':json_data['asks'][0][::-1][:30], 'askVol':json_data['asks'][1][::-1][:30], 'bidPrice':json_data['bids'][0][:30], 'bidVol':json_data['bids'][1][:30]})
#        self.BTCDepthData.loc[self.CurrentDate] = list(df['askPrice'].values) + list(df['askVol'].values) + list(df['bidPrice'].values) + list(df['bidVol'].values)
        self.CurrentOrderBook = df
    
    def SaveUpdatedBTCDepthData(self, BTCDepthDataPath):
        self.BTCDepthData.to_csv(BTCDepthDataPath%self._symbol)    
    
    def GetTick(self):
        return self.CurrentTick
    
    def GetDepth(self):
        return self.CurrentOrderBook
    
    def SaveCurrentTickToMySQL(self):
        self.mysqlQuery = """\
        INSERT INTO btc \
        (time, date, tradeTime, tradeDate, product, exchange, last, high, low, buy, sell, vol, tradeTime1min, close1min, open1min, high1min, low1min, vol1min) \
        VALUES \
        (NOW(), CURDATE(), '{0}', '{1}', '{2}', '{3}', {4}, {5}, {6}, {7}, {8}, {9}, '{10}', {11}, {12}, {13}, {14}, {15});\
        """.format(self.CurrentTick['date'], self.CurrentTick['date'][:10], self.product, self.exchange, self.CurrentTick['last'], self.CurrentTick['high'], self.CurrentTick['low'], self.CurrentTick['buy'], self.CurrentTick['sell'], self.CurrentTick['vol'], self.CurrentTick['date1min'], self.CurrentTick['close1min'], self.CurrentTick['open1min'], self.CurrentTick['high1min'], self.CurrentTick['low1min'], self.CurrentTick['vol1min'])

        self.cursor.execute(self.mysqlQuery)
        
    def ResetAutoIncrement(self):
        self.cursor.execute("""ALTER TABLE btc auto_increment = 1;""")
    
    def ResetTable(self):
        logging.info('WARNING. Clean entire table BTC')
        self.cursor.execute("""DELETE FROM btc WHERE id > 0;""")
    
    def CloseConnection(self):
        self.db.close()
    
class Config(object):
    okcoin_btcspot = {'url_tick' : 'https://www.okcoin.com/api/v1/ticker.do?symbol=%s', 
    'url_candlestick': 'https://www.okcoin.com/api/v1/kline.do?symbol=%s&type=1min&size=1',
    'url_depth': 'https://www.okcoin.com/api/v1/depth.do?symbol=%s',
    'symbol' : 'btc_usd',
    'exchange' : 'OKCoin',
    'product' : 'BTC'}
    okcoin_ltcspot = {'url_tick' : 'https://www.okcoin.com/api/v1/ticker.do?symbol=%s', 
    'url_candlestick': 'https://www.okcoin.com/api/v1/kline.do?symbol=%s&type=1min&size=1',
    'url_depth': 'https://www.okcoin.com/api/v1/depth.do?symbol=%s',
    'symbol' : 'ltc_usd',
    'exchange' : 'OKCoin',
    'product' : 'LTC'}


def DataHandler(btcobject):
    threading.Timer(60.0, DataHandler, args=(btcobject,)).start()
    print('time is %s'%datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
    print('Getting %s Tick'%btcobject.product)
#    
    btcobject.Tick()
    btcobject.SaveCurrentTickToMySQL()

    #CurrentTick = btcspot.GetTick()
    #CurrentOrderBook = btcspot.GetDepth()
                    
btcspot = OKCoinSpot(
                    Config.okcoin_btcspot['product'], 
                    Config.okcoin_btcspot['exchange'], 
                    Config.okcoin_btcspot['url_tick'], 
                    Config.okcoin_btcspot['url_candlestick'],
                    Config.okcoin_btcspot['url_depth'],
                    Config.okcoin_btcspot['symbol']
                    )
                

                
ltcspot = OKCoinSpot(
                    Config.okcoin_ltcspot['product'], 
                    Config.okcoin_ltcspot['exchange'], 
                    Config.okcoin_btcspot['url_tick'], 
                    Config.okcoin_btcspot['url_candlestick'],
                    Config.okcoin_btcspot['url_depth'],
                    Config.okcoin_ltcspot['symbol']
                    )

btcspot.ResetTable()
btcspot.ResetAutoIncrement()

if __name__ == '__main__':
    threading.Thread(target = DataHandler, args=(btcspot, )).start()
    threading.Thread(target = DataHandler, args=(ltcspot, )).start()
    
