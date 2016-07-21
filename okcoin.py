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
        
    def Tick(self):
        """
        This combines data from the candlestick and 
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
        self.cursor.execute("""\
        INSERT INTO btc \
        (time, date, tradeTime, tradeDate, product, exchange, last, high, low, buy, sell, vol) \
        VALUES \
        (NOW(), CURDATE(), '{0}', '{1}', '{2}', '{3}', {4}, {5}, {6}, {7}, {8}, {9});\
        """.format(self.CurrentTick['date'], self.CurrentTick['date'][:10], self.product, self.exchange, self.CurrentTick['last'], self.CurrentTick['high'], self.CurrentTick['low'], self.CurrentTick['buy'], self.CurrentTick['sell'], self.CurrentTick['vol']))

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
    threading.Timer(10.0, DataHandler, args=(btcobject,)).start()
    print('time is %s'%time.time())
    print(btcobject.product)    
#    
    btcobject.Tick()
    btcobject.SaveCurrentTickToMySQL()

    #CurrentTick = btcspot.GetTick()
    #CurrentOrderBook = btcspot.GetDepth()

btcspot = OKCoinSpot(
                    Config.okcoin_btcspot['product'], 
                    Config.okcoin_btcspot['exchange'], 
                    Config.okcoin_btcspot['url'], 
                    Config.okcoin_btcspot['symbol']
                    )
                    
#btcspot.ResetTable()
#btcspot.ResetAutoIncrement()
                    
ltcspot = OKCoinSpot(
                    Config.okcoin_ltcspot['product'], 
                    Config.okcoin_ltcspot['exchange'], 
                    Config.okcoin_ltcspot['url'], 
                    Config.okcoin_ltcspot['symbol']
                    )
                    

threading.Thread(target = DataHandler, args=(btcspot, )).start()

p = requests.get('https://www.okcoin.com/api/v1/kline.do?symbol=btc_usd&type=5min')
json_data = json.loads(p.text.decode('utf-8'))
json_data['asks'] = zip(*json_data['asks'])
json_data['bids'] = zip(*json_data['bids'])
