import numpy as np

def ComputeCorrMatrix(data, colnames, correlation_method = 'Robust_t'):
    ''' compute the correlation matrix given the data panel
    Input:  /data/ data panel
            /colnames/ column names of the data panel
            /correlation_method/ method of computing the correlations, robust_t or pearson
    Output: /corr_matrix/ the resulting correlation matrix
    '''
    
    if correlation_method == 'Robust_t':
        import qz.analytics.statistics.robust_estimation as robust_estimation
        length = len(colnames)
        corr_matrix  = np.identity(length)
        
        for i in range(length):
            for j in range(i+1, length):               
                # pairwise robust_estimation 
                pair_names        = [colnames[i], colnames[j]]
                pair_df           = data[pair_names]
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
                corr_matrix[i][j] = robust_rho
                corr_matrix[j][i] = robust_rho
                
    elif correlation_method == 'Pearson':
        corr_matrix = data.corr()
    
    return corr_matrix
