"""
Supervised Leaerning Preparation
"""

from sklearn.cross_validation import train_test_split
from sklearn.decomposition import RandomizedPCA
import pandas as pd
from Config import CONFIG


stock = 'SZ000002'
df = pd.read_csv('C:/Users/zklnu66/Desktop/DailyData_%s.csv'%stock, index_col = 0)
df.index.name = 'Time'
BacktestFeatures = ['EndOfDayPendingBuyRatio', 'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2', 'PriceCurvature2', 
        'PriceSlope3', 'PriceCurvature3', 'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 
        'PendingBuySlope3', 'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2', 
        'AmountSlope3', 'AmountCurvature3', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2', 
        'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3']

TargetFeature = 'Return2'
TradingHorizon = 1
TestSize = 0.2
RandomState = None

Dependent = df[BacktestFeatures][:-TradingHorizon].as_matrix()
Target = df[TargetFeature].shift(-TradingHorizon)[:-TradingHorizon].as_matrix()

X_train, X_test, Y_train, Y_test = train_test_split(Dependent, Target, test_size = TestSize, random_state = RandomState)

# Randomized PCA
n_components = 10
pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X_train)
X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)


from LinearModel import Ridge
param_grid = {'alpha' : [0.1, 1, 10]}
clf = Ridge(X_train_pca, Y_train, param_grid)



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
