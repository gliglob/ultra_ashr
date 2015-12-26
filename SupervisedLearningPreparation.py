"""
Supervised Leaerning Preparation
"""

from sklearn.cross_validation import train_test_split
from sklearn.decomposition import RandomizedPCA
import pandas as pd
import numpy as np
from Config import CONFIG


stock = 'SZ000001'
df = pd.read_csv('C:/Users/zklnu66/Desktop/DailyData_%s.csv'%stock, index_col = 0)
df.index.name = 'Time'
BacktestFeatures = ['EndOfDayPendingBuyRatio', 'BuyRatio', 'A_buyRatio', 'B_buyRatio', 'PriceSlope1', 'PriceCurvature1', 'PriceSlope2', 'PriceCurvature2', 
        'PriceSlope3', 'PriceCurvature3', 'PendingBuySlope1', 'PendingBuyCurvature1', 'PendingBuySlope2', 'PendingBuyCurvature2', 
        'PendingBuySlope3', 'PendingBuyCurvature3', 'AmountSlope1', 'AmountCurvature1', 'AmountSlope2', 'AmountCurvature2', 
        'AmountSlope3', 'AmountCurvature3', 'IndustrySpreadSlope1', 'IndustrySpreadCurvature1', 'IndustryeSpreadSlope2', 
        'IndustrySpreadCurvature2', 'IndustrySpreadSlope3', 'IndustrySpreadCurvature3', 'SidedAmount1', 'SidedAmount2', 'SidedAmount3']

TargetFeature = 'Return2'
TradingHorizon = 1
TestSize = 0.2
RandomState = None

Dependent = df[BacktestFeatures][:-TradingHorizon].as_matrix()
Target = df[TargetFeature].shift(-TradingHorizon)[:-TradingHorizon].as_matrix()

X_train, X_test, Y_train, Y_test = train_test_split(Dependent, Target, test_size = TestSize, random_state = RandomState)


# Randomized PCA
n_components = 3
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

#### Pairwise correlation
for feature in BacktestFeatures:
    pair_df = df[[feature, TargetFeature]]
    # pearson    
    pair_df.corr()

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

"""
Compute correlation between X and Y
"""

def RobustPairwiseCorrelation(pair_df):
    import numpy as np
    import statistics.robust_estimation as robust_estimation
    
    P                 = pair_df.as_matrix()
    nu_v              = robust_estimation.multi_uvtfit(P)
    nu_select         = robust_estimation.shape_selection(nu_v)
    mu, Sigma, _      = robust_estimation.robust_st_est(nu_select, P)
            
    # get robust corelation coefficient
    robust_Cov        = nu_select / (nu_select - 2) * Sigma
    s                 = robust_Cov.diagonal()
    S                 = np.sqrt(np.outer(s, s))
    robust_Corr       = robust_Cov / S
    robust_rho        = robust_Corr[0][1]
    return robust_rho
