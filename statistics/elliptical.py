import numpy as np

def mvtrnd(mu, Sigma, nu, size):
    """ generate multivariate student-t distribution
        with  Z ~ N(zeros, Sigma)
        and   V ~ Chi^2(nu),
        then  T = mu + Z/sqrt(V/nu) ~ St(mu, Sigma, nu)
        
        see, http://en.wikipedia.org/wiki/Multivariate_t-distribution        

        Inputs:
            /mu/       (n, 1) numpy 1d-array, the location parameter
                              where n is the dimension
            /Sigma/    (n, n) numpy 2d-array, the dispersion parameter
            /nu/       scalar, the shape parameter
            /size/     scalar, how many samples to be drawn
        
        Outputs:
            /T/        (size, n) numpy 2d-array, sampled data 
    """
    
    # convert inputs in numpy ndarray, copy and/or expand dimension if needed
    mu    = np.array(mu, copy=False, ndmin=1)
    Sigma = np.array(Sigma, copy=False, ndmin=2)
    
    # extract and check dimensions
    n     = mu.shape[0]
    j,k   = Sigma.shape
    if n != j or n != k:
        raise RuntimeError('Sigma (%d, %d) must be a square matrix with same dimension as mu (%d,1)'\
                            %(j,k,n))
    
    # sample chi-square for each row
    chi_2 = np.tile(np.random.chisquare(nu, size), (j,1)).T
    
    # sample multivariate normal for each row
    Z     = np.random.multivariate_normal(np.zeros(j), Sigma, size)
    
    # construt student-t sample
    T     = mu + Z / np.sqrt(chi_2/nu)
    
    return T

def mahal(Y, X):
    """ computes the Mahalanobis distance (in squared units) of each observation
        in Y from the reference sample in X. For each observation I, the distance
        is defined as d(I) = (Y[I,:]-mu)*inv(SIGMA)*(Y[I,:]-mu).T . Note that we 
        use vectorization and QR decomposition for efficient implementation here.
        This follows the Mathworks implementation of mahal().
        
        Inputs:
            /Y/ (m,n) numpy 2d-array, where m is the number of observtions and 
                                            n is the dimension of the data
            /X/ (j,n) numpy 2d-array, where j is the number of samples, must have j>=n
        
        Outputs:
            /d/ (m,1) numpy 1d-array, squared distance for each observation in y
    """
    
    # convert inputs in numpy ndarray, copy and/or expand dimension if needed
    X   = np.array(X, copy=False, ndmin=2)
    Y   = np.array(Y, copy=False, ndmin=2)
    
    # extract and check dimensions
    rx,cx = X.shape
    ry,cy = Y.shape
    
    if cy != cx:
        raise RuntimeError('Y (%d, %d) and X (%d,%d) must have same number of columns'\
                          %(ry, cy, rx, cx))
    if rx < cx :
        raise RuntimeError('X (%d,%d) must have no less num rows than columns'\
                            %(rx, cx))
    
    # take column means, reshape to (1, cy) 2d array for later slicing
    mu  = X.mean(axis=0).reshape(1, cy) 
    
    # subtract column means to every column
    C   = X - mu[[0]*rx, :]
    
    # intead of matrix inverse, generate R (n,n) from QR decomposition and solve
    R   = np.linalg.qr(C, mode='r') 
    ri  = np.linalg.solve(R.T, (Y-mu[[0]*ry, :]).T)
    
    # column sums
    d   = (ri*ri).sum(axis=0).T*(rx-1) 
    
    return d
