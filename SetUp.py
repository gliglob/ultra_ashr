"""
Setting Up Proxy
Importing Modules
Setting Paths
"""

from __future__ import division

####################
# Set Project Path #
####################

import sys, os
os.chdir('C:/Users/zklnu66/Desktop')
sys.path.append(os.path.abspath(os.getcwd() + '/ASHR'))

################
# SET ENCODING #
################

reload(sys)  
#sys.setdefaultencoding('ascii')
sys.setdefaultencoding('utf8')


#############
# SET PROXY #
#############

import urllib2

proxy = urllib2.ProxyHandler({'http': 'proxy.ml.com:8080', 'https': 'proxy.ml.com:8080'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

#############
#  Imports  #
#############

import pandas as pd
import numpy as np
import tushare as ts
import datetime, time
from HelperFunctions import *
from matplotlib import pyplot as plt

##############
# SET LOGGER #
##############
import logging
logger = logging.getLogger()
hdlr = logging.FileHandler('./ASHR/Log/%s_Log.log'%datetime.date.today().strftime('%Y-%m-%d'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Set Up Pandas Displays
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 50)

# AUTO-COMPLETION
#import rlcompleter, readline
#readline.parse_and_bind('tab:complete')

##########
# Static #
##########

TradingHours = [datetime.time(9, 30, 0), datetime.time(11, 30, 0), datetime.time(13, 0, 0), datetime.time(15, 0, 0)]

# Load Holidays Schedule
Holidays = pd.read_csv('./ASHR/DATA/Holidays.csv')
Holidays['Holidays'] = TimeWrapper2(Holidays['Holidays'])
HolidayList = Holidays['Holidays'].tolist()

# Intraday Master Clock
StartDate = datetime.datetime.combine(datetime.date(2015, 10, 9), TradingHours[0])
EndDate = datetime.datetime.combine(datetime.date(2015, 10, 9), TradingHours[-1])
Scale = '3s'
IntradayMasterClock = GenerateMasterClock(StartDate, EndDate, Scale, TradingHours, HolidayList)
IntradayMasterClock['MasterClock'] = IntradayMasterClock['MasterClock'].apply(lambda x: x.time())

# Daily Stock Data for a single Stock
DailyDataFrame = pd.DataFrame(columns = ['EndOfDayPendingBuyRatio', 'TotalAmount', 'Open', 'Close', 'High', 'Low', 
    'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2', 'PriceCurvature2', 
    'PriceSlope3', 'PriceCurvature3', 'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 
    'PendingBuySlope3', 'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2', 
    'AmountSlope3', 'AmountCurvature3', 'IntegratedDiff1'])

