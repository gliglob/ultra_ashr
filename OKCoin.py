import json
import requests
import datetime, time
import pandas as pd
from threading import Timer
from itertools import chain
import logging

symbol = 'btc_usd'
BTCTickDataPath = '/Users/hui/Desktop/%s_BTCTickData.csv'
BTCDepthDataPath = '/Users/hui/Desktop/%s_BTCDepthData.csv'

#symbol2 = 'okcoinCNY'
#p = requests.get('http://www.quandl.com/api/v3/datasets/BCHARTS/OKCOINCNY')


class OKCoinSpot(object):
    
    def __init__(self, symbol):
        self._symbol = symbol
        self.CurrentTick = {}
        self.CurrentOrderBook = None
        self.BTCTickData = pd.DataFrame(columns=['date', 'last', 'high', 'low', 'buy', 'sell', 'vol'])
#        self.BTCDepthData = pd.DataFrame(columns=list(chain.from_iterable(('askPrice%s'%i, 'askVol%s'%i, 'bidPrice%s'%i, 'bidVol%s'%i) for i in range(1, 31))))
        self.BTCDepthData = pd.DataFrame(columns=['askPrice%s'%i for i in range(1, 31)] + ['askVol%s'%i for i in range(1, 31)] + ['bidPrice%s'%i for i in range(1, 31)] + ['bidVol%s'%i for i in range(1, 31)])
        self.currentDate = time.time()
        
    def Tick(self):
        # get the most recent trade price
        p = requests.get('https://www.okcoin.com/api/v1/ticker.do?symbol=%s'%self._symbol)
        json_data = json.loads(p.text.decode('utf-8'))
        json_data['date'] = datetime.datetime.fromtimestamp(int(json_data['date'])).strftime('%Y-%m-%d %H:%M:%S')
        self.CurrentDate = json_data['date']
        json_data.update(json_data['ticker'])
        json_data.pop('ticker')
        json_data = pd.DataFrame(json_data.items()).set_index(0)
        self.BTCTickData.loc[len(self.BTCTickData)] = [json_data.loc[i][1] for i in self.BTCTickData.columns]
        self.CurrentTick = json_data
    
    def SaveUpdatedBTCTickData(self, BTCTickDataPath):
        self.BTCTickData.to_csv(BTCTickDataPath%self._symbol, index=False)
    
    def Depth(self):
        # get the most recent order book
        # only save level 30 order book
        p = requests.get('https://www.okcoin.com/api/v1/depth.do?symbol=%s'%self._symbol)
        json_data = json.loads(p.text.decode('utf-8'))
        json_data['asks'] = zip(*json_data['asks'])
        json_data['bids'] = zip(*json_data['bids'])
        df = pd.DataFrame(data={'askPrice':json_data['asks'][0][::-1][:30], 'askVol':json_data['asks'][1][::-1][:30], 'bidPrice':json_data['bids'][0][:30], 'bidVol':json_data['bids'][1][:30]})
        self.BTCDepthData.loc[self.CurrentDate] = list(df['askPrice'].values) + list(df['askVol'].values) + list(df['bidPrice'].values) + list(df['bidVol'].values)
        self.CurrentOrderBook = df
    
    def SaveUpdatedBTCDepthData(self, BTCDepthDataPath):
        self.BTCDepthData.to_csv(BTCDepthDataPath%self._symbol)    
    
    def GetTick(self):
        return self.CurrentTick
    
    def GetDepth(self):
        return self.CurrentOrderBook


btcspot = OKCoinSpot('btc_usd')
t = None

def main():
    t = Timer(10.0, main).start()
    print('time is %s'%time.time())
    
    btcspot.Tick()
    btcspot.SaveUpdatedBTCTickData(BTCTickDataPath)
    
    btcspot.Depth()
    btcspot.SaveUpdatedBTCDepthData(BTCDepthDataPath)

    #CurrentTick = btcspot.GetTick()
    #CurrentOrderBook = btcspot.GetDepth()

main()
