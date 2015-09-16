import numpy as np
from scipy.stats import norm, t, gaussian_kde
from qz.analytics.statistics.robust_estimation import uvtfit

# pdf / cdf
def GeneratePDF(Data, method = 'Robust_Student_t', lower_threshold = 0.15, upper_threshold = 0.85):
    
    '''Generate the pdf estimate of the data
    Input: /Data/   data to estimate pdf on
           /method/ Method of estimation.
                    Available methods: 'Robust_Student_t'; 'KDE'; 'Normal'
           /lower_threshold/ in percentage
           /upper_threshold/ in percentage
    Output: /pdf/   fitted pdf
            /cdf/   fitted cdf
    '''
    x = np.linspace(min(Data), max(Data), 100)
    if method == 'Robust_Student_t':
        nu, mu, sigma = uvtfit(Data)
        pdf = t.pdf(x, nu, mu, sigma)
        cdf = t.cdf(x, nu, mu, sigma)
        lower = t.ppf(lower_threshold, nu, mu, sigma)
        upper = t.ppf(upper_threshold, nu, mu, sigma)
        
    elif method == 'Normal':
        mu, sigma = norm.fit(Data)
        pdf = norm.pdf(x, mu, sigma)
        cdf = norm.cdf(x, mu, sigma)
        lower = norm.ppf(lower_threshold, mu, sigma)
        upper = norm.ppf(upper_threshold, mu, sigma)
        
    elif method == 'KDE':
        kernal = gaussian_kde(Data)
        pdf = kernal.evaluate(x)
        cdf = np.array([kernal.integrate_box(x[0], x[i+1]) for i in range(len(x)-1)])
        lower = np.percentile(cdf, lower_threshold*100)
        upper = np.percentile(cdf, upper_threshold*100)
        
    return x, pdf, cdf, lower, upper
