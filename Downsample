import pandas as pd

# Downsample procedure
# type of data can be taken: pd.DataFrame, qztable

def Downsample(data, M1, critical_value, starting_point):
    
    stride = round(2 * M1 * critical_value)
    starting_point = round(stride * starting_point)
    
    if isinstance(data, pd.DataFrame):
        downsample = range(starting_point, data.shape[0], stride)
        data_down = data.ix[downsample]
    else:
        data_down = data[range(starting_point, int(data.nRows()), stride)]
    
    return data_down
