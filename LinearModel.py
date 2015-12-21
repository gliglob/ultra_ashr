"""
Model Training
"""

import pandas as pd

#stock = 'SZ000001'
#df = pd.read_csv('./DailyData_%s.csv'%stock, index_col = 0)
#df.index.name = 'Time'
#BacktestFeatures = ['EndOfDayPendingBuyRatio', 'TotalAmount', 'Open', 'Close', 'High', 'Low', 
#        'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2', 'PriceCurvature2', 
#        'PriceSlope3', 'PriceCurvature3', 'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 
#        'PendingBuySlope3', 'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2', 
#        'AmountSlope3', 'AmountCurvature3', 'IntegratedDiff1', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2', 
#        'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3']
#
#Target = 'Result1'
#TradingHorizon = 1
#
#param_grid = {'alpha' : [0.1, 1, 10]}

def OLS(X_train, Y_train):
    """
    Ordinary Least Squares
    """
    from sklearn import linear_model
    clf = linear_model.LinearRegression(fit_intercept = True, n_jobs = -1)
    clf.fit(X_train, Y_train)
    return clf



def Ridge(X_train, Y_train, param_grid):
    """
    Ridge regression
    """
    from sklearn import linear_model
    from sklearn.grid_search import GridSearchCV
    
    clf = GridSearchCV(linear_model.Ridge(), param_grid)
    clf.fit(X_train, Y_train)
    return clf

def Lasso(X_train, Y_train, param_grid):
    """
    Lasso regression
    """
    from sklearn import linear_model
    from sklearn.grid_search import GridSearchCV
    
    clf = GridSearchCV(linear_model.Lasso(), param_grid)
    clf.fit(X_train, Y_train)
    return clf

