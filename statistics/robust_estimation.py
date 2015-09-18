import qz.analytics.statistics.elliptical as elliptical
import qz.analytics.eigen.utils as utils
import scipy.optimize as sp_opt
import scipy.special as sp_special
import numpy as np
    
def uvtfit(x):
    """ for univariate series x, fit t-distribution's shape parameter 'nu' using MLE.
        if X ~ St(nu, mu, sigma^2), then Z = (X-mu)/sigma ~ St(nu, 0, (nu-2)/nu)
        
        Inputs:
            /x/     (m,1) numpy 1d-array, where m is the number of samples
        
        Outputs:
            /nu/    scalar, shape estimate
            /mu/    scalar, location estimate
            /sigma/ scalar, dispersion estimate            
    """ 
    # convert inputs in numpy ndarray, copy and/or expand dimension if needed
    x    = np.array(x, copy=False, ndmin=1)
    
    # standardize data for stability
    mu   = x.mean()
    stdx = x.std()
    z    = (x - mu) / stdx
    
    def _neg_log_likelihood(nu):
        
        # computes the negative log likelihood function for a scalar t distribution
        cv      = sp_special.gamma(0.5 * (1 + nu)) / (sp_special.gamma(0.5 * nu) * np.sqrt(np.pi * nu))
        sigma_2 = (nu - 2) / nu * np.var(z)
        negL    = - np.mean( np.log(cv) - 0.5 * np.log(sigma_2) - 0.5 * (nu + 1) * np.log(1 + z * z / (nu * sigma_2)) )
        
        return negL
    
    # minimize neg log likelihood function
    # note nu=1 is Cauchy distribution, 
    #      nu=2 variance is infinite, 
    #      nu=100 close to normal distribution
    nu    = sp_opt.optimize.fminbound(_neg_log_likelihood, 2.01, 100)
    
    # estimate sigma
    sigma = np.sqrt((nu - 2) / nu) * stdx
    
    return [nu, mu, sigma]
    
    
def multi_uvtfit(P):
    """ given panel data P with n dimensions, each dimension, use uvfit to estimate
        one-dimentional shape parameter. compute final shape parameter for multivariate 
        case using shape_select_method.

        Inputs:
            /P/          (m, n) numpy 2d-array, sample data with dimension = n
            /method/     selection method for shape prameter, currently supports
                         'min', 'mean', and 'median', default to 'min'
        
        Outputs:
            /nu_v/       (n) nu_est for each column of panel /P/
    """
    
    # convert inputs in numpy ndarray, copy and/or expand dimension if needed
    P = np.array(P, copy=False, ndmin=2)
    
    # extract dimensions
    n = P.shape[1]
    
    # call uvtfit to estimate nu for each dimension
    nu_v = np.zeros(n)
    for i in range(n):
        nu_v[i], _, _ = uvtfit(P[:,i])
        
    return nu_v
    

def robust_st_est(nu, Y, rtol=0.0001, max_iter=1000):
    """ computes mu and sigma given nu from MLE, using convegence technique
    
        Inputs:
            /nu/        scalar, t-distribution shape parameter
            /Y/         (m,n) numpy 2d-array data 
                            where m is the number of observtions and 
                                  n is the dimension 
            /rtol/      relative tolerance in weight vector between iterations
        
        Outputs:
            /mu_est/    scalar, robust sample estimate of location parameter
            /Sigma_est/ scalar, robust sample estimate of dispersion parameter
            /w_new/     scalar, final weights vector     
    """
    # convert inputs in numpy ndarray, copy and/or expand dimension if needed
    Y       = np.array(Y, copy=False, ndmin=2)
    
    # extract dimensions
    m,n   = Y.shape 
    
    # init for convergence iterations
    X       = Y
    w_old   = np.ones((m, 1))
    w_new   = w_old - 0.99
    i_count = 0
    
    while np.linalg.norm( (w_new - w_old) / w_new ) > rtol and i_count < max_iter:
        
        # compute squared Mahalanobis distance
        ma2      = elliptical.mahal(Y, X).reshape((m, 1))
        
        # update weights        
        w_old    = w_new
        w_new    = (n + nu) / (nu + ma2)
        w_sqrt   = np.sqrt(w_new)
        
        # compute weighted location
        mu_est   = np.dot(w_new.T, Y) / w_new.sum()
        
        # compute weighted X panel 
        # note: weighted centered Y panel, add location back in to find new X
        X        = w_sqrt[:, [0]*n] * (Y - mu_est[[0]*m, :]) + mu_est[[0]*m, :]  
        
        # incr
        i_count += 1
        
    # compute covariance matrix, each column is a varaible
    Sigma_est = np.cov(X, rowvar=0) 
    
    return [mu_est.flatten(), Sigma_est, w_new]
    
    
def robust_pairwise_beta_est(P, shape_selection_method='min'):
    """ Compute robust estimtes of coefficient beta of pairwise OLS regression
        
        Input: 
            /P/      (m, 2) numpy 2d-array, sample data with dismension = 2
        
        Output:
            /beta/   scalar, OLS regression coefficient of the columns of P
    """
    # convert inputs in numpy ndarray, copy and/or expand dimension if needed
    P = np.array(P, copy=False, ndmin=2)
    
    # check exaclty two columns
    if P.shape[1] != 2:
        raise RuntimeError('P %s must be a (m,2) 2d array'%str(P.shape))
    
    # multiple uvtfit for nu 
    nu_v        = multi_uvtfit(P)

    # call shape_selection 
    nu_select   = shape_selection(nu_v, shape_selection_method)
    
    # robust dispersion estimate
    _, Sigma, _ = robust_st_est(nu_select, P)
    
    # compute covariance matrix
    Cov         = nu_select / (nu_select - 2) * Sigma
    
    # for pairwise OLS, the regression coefficient beta can be expressed as
    # beta = rho * sigma_y / sigma_x 
    #      = covariance(x,y) / sigma_x^2. 
    # Given covariance matrix Cov, 
    # beta = Cov[0,1] / Cov[1,1] 
    
    beta        = Cov[0,1] / Cov[1,1]
    
    return beta
    

def robust_eigen_est(P):
    """ compute eigen systems using both robust and regular correlation matrix estimations.
        returned systems are sorted and eigen vectors are normalized
        
        Input: 
            /P/               (m, n) numpy 2d-array, sample data with dismension n
        
        Output:
            /robust_evals/    (n, 1) numpy 1d-array, vector of sorted robust eigen values
            /robust_evecs/    (n, n) numpy 2d-array, matrix whose columns are associated eigenvectors
            /regular_evals/   (n, 1) numpy 1d-array, vector of sorted regular eigen values
            /regular_evecs/   (n, n) numpy 2d-array, matrix whose columns are associated eigenvectors
    """
    # compute robust estimation on Sigma
    nu_v         = multi_uvtfit(P)
    nu_select    = shape_selection(nu_v)
    _, Sigma, _  = robust_st_est(nu_select, P)
    
    # compute covariance matrix
    robust_Cov   = nu_select / (nu_select - 2) * Sigma
    
    # convert to correlaton matrix
    s            = robust_Cov.diagonal()
    S            = np.sqrt(np.outer(s, s))
    robust_Corr  = robust_Cov / S
    
    # compute regular correlation matrix
    regular_Corr = np.corrcoef(P, rowvar=0)    

    # compute eigen values and vectors
    robust_evals,  robust_evecs  = np.linalg.eigh(robust_Corr)
    regular_evals, regular_evecs = np.linalg.eigh(regular_Corr)
    
    # sort eigen systems inplace
    utils.sort_eigensystem_for_analysis(robust_evals,  robust_evecs)
    utils.sort_eigensystem_for_analysis(regular_evals, regular_evecs)
    
    return [robust_evals, robust_evecs, regular_evals, regular_evecs]
    

def shape_selection(nu_v, method='min'):
    """ given a vector of shape parameter estimations nu from uvtfit, and 
        selection method, compute a single shape parameter for multivariate case
        
        Inputs:
            /nu_v/       (n,1) numpy 1d-array, vector of univariate t-distribution shape parameter
            /method/     selection method for shape prameter, currently supports
                         'min', 'mean', and 'median', default to 'min'
        
        Outputs:
            /nu_select/  computed nu for given method           
    """
    if method in ['min', 'mean', 'median']:
        
        nu_select = getattr(np, method)(nu_v)
        
        return nu_select
        
    else:
        
        raise RuntimeError('shape selection method %s not supported' % method)
