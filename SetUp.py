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
pd.set_option('display.max_columns', 100)

# AUTO-COMPLETION
#import rlcompleter, readline
#readline.parse_and_bind('tab:complete')

