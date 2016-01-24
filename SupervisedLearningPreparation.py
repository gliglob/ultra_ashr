"""
Supervised Leaerning Preparation
"""

from sklearn.cross_validation import train_test_split
from sklearn.decomposition import RandomizedPCA
import pandas as pd
import numpy as np
from Config import CONFIG
from HelperFunctions import *

stock = 'SZ000001'
#df = pd.read_csv('C:/Users/zklnu66/Desktop/ASHR/DailyData/%s.csv'%stock, index_col = 0)
#df.index.name = 'Time'

df = pd.read_csv('C:/Users/zklnu66/Desktop/ASHR/DailyData/%s.csv'%stock)

df = df[df['IncludedInTraining'] == 'Y']
df = df.set_index('Time')

df['Return2'] = np.exp(-df['Open'] + df.shift(-1)['Open']) - 1
df['Target'] = df['Return2'].shift(-1)

#BacktestFeatures = ['EndOfDayPendingBuyRatio', 'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2',
#    'PriceCurvature2', 'PriceSlope3', 'PriceCurvature3', 'PricePema1', 'PricePema2', 'PricePema3',
#    'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 'PendingBuySlope3',
#    'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2',
#    'AmountSlope3', 'AmountCurvature3', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2',
#    'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3', 'SidedAmount1', 'SidedAmount2',
#    'SidedAmount3', 'RSI1', 'RSI2', 'RSI3', 'WilliamR_1', 'WilliamR_2', 'WilliamR_3',
#    'InverseWilliamR_1', 'InverseWilliamR_2', 'InverseWilliamR_3', 'Disparity1', 'Disparity2', 'Disparity3',
#    'Disparity12', 'Disparity13', 'Disparity23', 'BuyRatio2', 'BuyRatio3', 'A_buyRatio2', 'A_buyRatio3',
#    'B_buyRatio2', 'B_buyRatio3', 'EndOfDayPendingBuyRatio2', 'EndOfDayPendingBuyRatio3']
#    
BacktestFeatures = ['EndOfDayPendingBuyRatio', 'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2',
    'PriceCurvature2', 'PriceSlope3', 'PriceCurvature3', 
    'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 'PendingBuySlope3',
    'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2',
    'AmountSlope3', 'AmountCurvature3', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2',
    'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3',  'IndexSpreadSlope1', 'IndexSpreadCurvature1', 
    'IndexSpreadSlope2', 'IndexSpreadCurvature2', 'IndexSpreadSlope3', 'IndexSpreadCurvature3', 'SidedAmount1', 'SidedAmount2',
    'SidedAmount3', 'RSI1', 'RSI2', 'RSI3', 'Volatility', 'VolatilityIndexSpread', 'VolatilityIndustryIndexSpread', 'BetaIndex', 'BetaIndustryIndex',
    'WilliamR_1', 'WilliamR_2', 'WilliamR_3','InverseWilliamR_1', 'InverseWilliamR_2', 'InverseWilliamR_3', 'Disparity1', 'Disparity2', 'Disparity3',
    'Disparity12', 'Disparity13', 'Disparity23', 'BuyRatio2', 'BuyRatio3', 'A_buyRatio2', 'A_buyRatio3',
    'B_buyRatio2', 'B_buyRatio3', 'EndOfDayPendingBuyRatio2', 'EndOfDayPendingBuyRatio3', 'Volatility2', 'Volatility3', 
    'VolatilityIndexSpread2', 'VolatilityIndexSpread3', 'VolatilityIndustryIndexSpread2', 'VolatilityIndustryIndexSpread3',
    'BetaIndex2', 'BetaIndex3', 'BetaIndustryIndex2', 'BetaIndustryIndex3']
    

"""
Pre processing
Demean: note, we are interested in the theoretical mean
"""
DemeanFeatures = {'RSI1' : 0.5, 'RSI2' : 0.5, 'RSI3' : 0.5, 'WilliamR_1' : 0.5, 'WilliamR_2' : 0.5, 'WilliamR_3' : 0.5,
    'InverseWilliamR_1' : -0.5, 'InverseWilliamR_2' : -0.5, 'InverseWilliamR_3' : -0.5}


MeanDataFrame = pd.DataFrame(columns = ['EstimatedMean'])
for feature in ['Volatility', 'Volatility2', 'Volatility3', 'VolatilityIndexSpread', 'VolatilityIndexSpread2',
                'VolatilityIndexSpread3', 'VolatilityIndustryIndexSpread', 'VolatilityIndustryIndexSpread2', 'VolatilityIndustryIndexSpread3',
                'BetaIndex', 'BetaIndustryIndex', 'BetaIndex2', 'BetaIndex3', 'BetaIndustryIndex2', 'BetaIndustryIndex3']:
    EstimatedMean = np.mean(df[feature])
    MeanDataFrame.loc[feature] = EstimatedMean

MeanDataFrame.to_csv(CONFIG.ESTIMATEDMEANDATAPATH%stock, index_label = 'Feature')
    
    
for feature in DemeanFeatures.keys():
    df[feature] -= DemeanFeatures[feature]




TargetFeature = 'Return2'
TradingHorizon = 1
TestSize = 0.2
RandomState = 42

Dependent = df[BacktestFeatures][:-TradingHorizon].as_matrix()
Target = df[TargetFeature].shift(-TradingHorizon)[:-TradingHorizon].as_matrix()

X_train, X_test, Y_train, Y_test = train_test_split(Dependent, Target, test_size = TestSize, random_state = RandomState)


# Randomized PCA
n_components = 10
pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X_train)
X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)

# Ridge
from LinearModel import Ridge
param_grid = {'alpha' : [0.1, 1, 10]}
clf = Ridge(X_train_pca, Y_train, param_grid)

# Lasso
from LinearModel import Lasso
alpha = 0.01
clf = Lasso(alpha = alpha)
clf.fit(X_train_pca, Y_train)
Y_pred_lasso = clf.predict(X_test_pca)
from sklearn.metrics import r2_score
r2_score_lasso = r2_score(Y_test, Y_pred_lasso)

from sklearn.linear_model import LassoLarsCV
clf = LassoLarsCV(cv = 10)
clf.fit(X_train, Y_train)

#### Kernal Ridge vs SVR
from sklearn.svm import SVR
from sklearn.grid_search import GridSearchCV
from sklearn.kernel_ridge import KernelRidge
param_grid_svr = {"C": [1e0, 1e1, 1e2, 1e3, 1e4, 1e5], "gamma": np.logspace(-5, 5, 10)}
param_grid_kr = {"alpha": [1e0, 1e-1, 1e-2, 1e-3], "gamma": np.logspace(-2, 2, 5)}
svr = GridSearchCV(SVR(kernel = 'rbf'), cv = 5, param_grid = param_grid_svr)
kr = GridSearchCV(KernelRidge(kernel = 'rbf'), cv = 5, param_grid = param_grid_kr)
svr.fit(X_train_pca, Y_train)
kr.fit(X_train_pca, Y_train)
y_svr = svr.predict(X_test_pca)
y_kr = kr.predict(X_test_pca)


from sklearn.svm import SVC
cutoff = 0.04
param_grid_svc = {"C": [1e0, 1e1, 1e2, 1e3, 1e4, 1e5], "gamma": np.logspace(-5, 5, 10)}
svc = GridSearchCV(SVC(kernel = 'rbf'), cv = 5, param_grid = param_grid_svr))
Y_train01 = [1 if i > cutoff else 0 for i in Y_train]
Y_test01 = [1 if i > cutoff else 0 for i in Y_test]
svc.fit(X_train, Y_train01)
svc.score(X_test, Y_test01)

"""
Visualize learning curve
"""
from sklearn.learning_curve import learning_curve
train_sizes_svr, train_scores_svr, test_scores_svr = learning_curve(svr, X_train_pca, Y_train, train_sizes = np.linspace(0.1, 1, 10), cv = 10, scoring = 'mean_squared_error')
train_sizes_kr, train_scores_kr, test_scores_kr = learning_curve(kr, X_train_pca, Y_train, train_sizes = np.linspace(0.1, 1, 10), cv = 10, scoring = 'mean_squared_error')

"""
Feature selection
"""
from sklearn.feature_selection import SelectKBest 
from sklearn.feature_selection import f_regression
selection = SelectKBest(f_regression, k = 15)
X_train_selected = selection.fit_transform(X_train, Y_train)
X_test_selected = selection.transform(X_test)
# kept features
[BacktestFeatures[i] for i in selection.get_support(indices = True)]

"""
Save model
"""
if not os.path.exists(CONFIG.MODELPATH%(stock)):
    os.makedirs(CONFIG.MODELPATH%stock)

model_name = 'Regr_'
SaveObject(model, CONFIG.MODELDATAPATH%(stock, model_name + CONFIG.LASTMODELUPDATE))



#### Pairwise correlation
CorrelationList = []
for feature in BacktestFeatures:
    pair_df = pd.DataFrame({'Feature': X_train[:, BacktestFeatures.index(feature)], 'Target': Y_train})
#    # pearson    
#    CorrelationList.append(abs(pair_df.corr().iloc[0][1]))
    # robust
    CorrelationList.append(abs(RobustPairwiseCorrelation(pair_df)))

SortAndZip(BacktestFeatures, CorrelationList, True)

"""
Correlation Analysis
"""

# Correlation Plots
colnames = BacktestFeatures
from tools.compute_corr_matrix import ComputeCorrMatrix
from tools.order_corr_matrix import OrderCorrMatrix

corr_matrix = ComputeCorrMatrix(df[colnames], colnames, 'Robust_t')

import linkage.analysis as linkage_analysis
_, _, leaf_order = linkage_analysis.tumminello_correlation_filter(corr_matrix, colnames, 'single')
    
corr_matrix_ordered, colnames_ordered = OrderCorrMatrix(corr_matrix, colnames, leaf_order)

from matplotlib import pyplot as plt
import linkage.graphs as linkage_graphs
fig, axes = plt.subplots(1, 1)
linkage_graphs.plot_correlation_matrix(corr_matrix_ordered, colnames_ordered, col_order=None, ax=axes)


# auto correlation
# Durbin-Watson statistic

# stationary (unit root)
# ADF test
from statsmodels.tsa.stattools import adfuller
series = df['PriceSlope1']
adfuller(series)
