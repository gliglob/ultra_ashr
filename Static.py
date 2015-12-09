import pandas as pd
import datetime, time


class STATIC(object):
    
    # Holidays Schedule
    Holidays = pd.read_csv('./ASHR/DATA/Holidays.csv')
    Holidays['Holidays'] = Holidays['Holidays'].map(lambda x: datetime.date(*time.strptime(x, '%Y-%m-%d')[:3]))
    HOLIDAYLIST = Holidays['Holidays'].tolist()
    TRADINGHOURS = [datetime.time(9, 30, 0), datetime.time(11, 30, 0), datetime.time(13, 0, 0), datetime.time(15, 0, 0)]

    
