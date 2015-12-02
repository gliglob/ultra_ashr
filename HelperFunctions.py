##############
### HELPER ###
##############


import datetime, time, os
import pandas as pd
import numpy as np
from Static import STATIC

def CodeWrapper(series):
    """
    Take pandas.series as input
    Cast the int type code to the 6 digit letter as stock code
    """
    series = series.map(lambda x: unicode('0'*(6-len(str(x))) + str(x)))
    return series

def TimeWrapper1(series):
    """
    Cast the string '09:30:00' type time to datetime.time
    """
    series = series.map(lambda x: datetime.time(int(x[0:2]), int(x[3:5]), int(x[6:8])))
    return series
    
def TimeWrapper2(series):
    """
    Cast the string '1/3/2012' type date to datetime.date
    """
    series = series.map(lambda x: datetime.date(*time.strptime(x, '%Y-%m-%d')[:3]))
    return series

def TimeWrapper3(series):
    """
    Cast the string '2015-01-05 09:25:02' type date to datetime.datetime
    """
    series = series.map(lambda x: datetime.datetime(*time.strptime(x, '%Y-%m-%d %H:%M:%S')[:6]))
    return series

def TimeWrapper4(series):
    """
    Cast the string '92503' type time to datetime.time(9, 25, 3)
    """
    series = series.map(lambda x: datetime.time(*time.strptime(str(int(x)), '%H%M%S')[3:6]))
    return series    

def TimeWrapper5(series):
    """
    Cast the string '7/31/2015 9:25' type time to datetime.datetime
    """
    series = series.map(lambda x: datetime.datetime(*time.strptime(x, '%m/%d/%Y %H:%M')[:5]))
    return series    
    
def TimeMapToDatetime(Time, day):
    return datetime.datetime.combine(day, Time)

def DropOutliers(df, column):
    """
    Detect the outliers for column that are 3 std devs away
    Input:
        /df/: the target data frame
        /column/: the target column within the data frame
    NOTE: apply the function to intraday data only as jumps are likely for overnight
    """
    df = df[np.abs(df[column] - df[column].mean()) <= 5 * df[column].std()]
    return df
    
def DropWeekend(df):
    """
    Excluding the weekends
    """
    df = df[df['time'].apply(lambda x: x.isoweekday() in range(1,6))]
    return df

def DropHoliday(df):
    """
    Excluding the holidays
    """
    df = df[df['time'].apply(lambda x: x.date() not in STATIC.HOLIDAYLIST)]
    return df
    
def RestrictTradingHour(df, RestrictingLst, TimeFormat = False):
    """
    Takes a list of times, in multiples of two.
    Input: 
            /TimeFormat/  True when type of df['time'] is datetime.time
                          False when type of df['time'] is datetime.datetime
                          
    Example: [datetime.time(9, 30, 0), datetime.time(11, 30, 0), datetime.time(13, 0, 0), datetime.time(15, 0, 0)]
            representing 9:30 -- 11:30, 13:00 -- 15:00            
    """
    
    df_new = pd.DataFrame()
    for i in range(0, len(RestrictingLst), 2):
        if TimeFormat:
            subset = df[df['time'].apply(lambda x: x >= RestrictingLst[i] and x <= RestrictingLst[i+1])]
        else:
            subset = df[df['time'].apply(lambda x: x.time() >= RestrictingLst[i] and x.time() <= RestrictingLst[i+1])]
        df_new = subset if i == 0 else df_new.append(subset)

    return df_new

def DropNaData(df, ColToDrop = None):
    """
    Drop the NA and 0 value in the columns that specified
    ColToDrop is a list parameter
    """
    if not ColToDrop: 
        ColToDrop = df.columns
    # Drop NA
    df = df.dropna(subset = ColToDrop, axis = 0)
    for col in ColToDrop:
        df = df[df[col] != 0]
    return df

def DropColumn(df, ColToDrop):
    """
    Drop the columns that specified
    ColToDrop is a list parameter
    """
    # Drop NA
    df = df.drop(ColToDrop, axis = 1)
    return df


def WriteExcel(writer, sheet, df, index = False, header = True):
    # Example: writer = pd.ExcelWriter('./ASHR/DATA/test.xlsx')
    df.to_excel(writer, sheet, index = index, header = header)
    writer.save()

def ReadExcel(file, sheetname):
    # Example: file = pd.ExcelFile('./ASHR/DATA/test.xlsx')
    # read the sheet from the excel file
    df = file.parse(sheetname)
    return df

def AddBusinessDay(Date, NumOfDaysToAdd):
    """
    Add any number of business days given a date
    Input:
        /Date/: Reference business datetime.datetime object or datetime.date object
        /NumOfDaysToAdd/: Number of days to add
    Output:
        /Date/: The resulting date with added days. Returning same data type as the Date input.
    """
    CurrentDate = datetime.datetime.combine(Date, datetime.time(0)) if type(Date) == datetime.date else Date
    while NumOfDaysToAdd != 0:
        if NumOfDaysToAdd > 0:
            CurrentDate += datetime.timedelta(days=1)
            if (CurrentDate.date() not in STATIC.HOLIDAYLIST) and (CurrentDate.date().isoweekday() in range(1, 6)):
                NumOfDaysToAdd -= 1
        else:
            CurrentDate -= datetime.timedelta(days=1)
            if (CurrentDate.date() not in STATIC.HOLIDAYLIST) and (CurrentDate.date().isoweekday() in range(1, 6)):
                NumOfDaysToAdd += 1
    CurrentDate = CurrentDate.date() if type(Date) == datetime.date else CurrentDate
    return CurrentDate

def GenerateMasterClock(StartDate, EndDate, Scale):
    """
    Gnerate the master wall clock
    Restricting to trading hours, non holidays only
    Input:
        /StartDate/: datetime.date type if Scale = day; daetime.datetime type if Scale = 's','m','h'
        /EndDate/: datetime.date type if Scale = day; daetime.datetime type if Scale = 's','m','h'
        /Scale/: Time scale. Possible values: '1d', '2s', '3m', '4h', etc.
    """
    def ScaleMapping(Scale):
        if Scale[-1] == 's':
            return datetime.timedelta(seconds = int(Scale[:-1]))
        elif Scale[-1] == 'm':
            return datetime.timedelta(minutes = int(Scale[:-1]))
        elif Scale[-1] == 'h':
            return datetime.timedelta(hours = int(Scale[:-1]))


    def CheckTradingHours(date):
        for i in range(0, len(STATIC.TRADINGHOURS), 2):
            if (date.time() >= STATIC.TRADINGHOURS[i]) and (date.time() <= STATIC.TRADINGHOURS[i+1]):
                return True
        return False
            
    df = pd.DataFrame(columns = ['MasterClock'])
    ind = 0
    
    if Scale[-1] == 'd':
        date = StartDate
        while (date <= EndDate):
            if (date not in STATIC.HOLIDAYLIST) and (date.isoweekday() in range(1, 6)):
                df.loc[ind] = [date]
                ind += 1
            date += datetime.timedelta(days = int(Scale[:-1]))
                
    elif Scale[-1] == 's' or Scale[-1] == 'm' or Scale[-1] == 'h':
        date = StartDate
        while (date <= EndDate):
            if (date.date() not in STATIC.HOLIDAYLIST) and (CheckTradingHours(date)) and (date.date().isoweekday() in range(1, 6)):
                df.loc[ind] = [date]
                ind += 1
            date += ScaleMapping(Scale)

    return df



def AddDateToIntradayMasterClock(Date, IntradayMasterClock):
    """
    Add Date to the IntradayMasterClock such as each row is datetime.datetime type
    """
    return IntradayMasterClock['MasterClock'].apply(lambda x: datetime.datetime.combine(Date, x)).to_frame()

def SaveObject(Object, Path):
    """
    Pickle the object (for instance, filter) to local machine for later use
    Input:
        /Object/ The object to be saved
        /Path/   Path of the object to be saved. Example: 'C:/Users/zklnu66/Desktop/data.pkl'
    """
    import pickle
    with open(Path, 'wb') as output:
        pickle.dump(Object, output, pickle.HIGHEST_PROTOCOL)

def LoadObject(Path):
    """
    Load the pickled the object (for instance, filter) to local machine for later use
    Input:
        /Path/   Path of the object to be loaded. Example: 'C:/Users/zklnu66/Desktop/data.pkl'
    """
    import pickle
    with open(Path, 'rb') as input:
        Object = pickle.load(input)
    return Object
    
