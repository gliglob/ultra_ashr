import scipy.cluster.hierarchy as hierarchy 
import scipy.spatial.distance  as distance 
import numpy as np

def tumminello_correlation_filter(C, col_names, linkage_method='average',  distance_mapping='shift'):
    """ Applies an agglometative hierchical clustering filter to correltion matrix C.    
        see tumminells's paper at http://arxiv.org/pdf/0809.4615.pdf. For an N by N input 
        C with 0.5*N(N-1) distinct entries(max), the ouput filtered matrix Q has only 
        N distinct entries (max), and Z is the linkage matrix encoding the hierachical 
        clustering of the correlation network. 
    
        Inputs:
            /C/                  (N,N) numpy 2d-array, the original correlation matrix
            /col_names/          (N,1) numpy 1d-array, column names of C
            /linkage_method/     which method of linkage analysis to run, equal to 'average' or 'single', 
                                 'average' : average linked cluster analysis, 
                                 'single'  : singlely linked cluster analysis.
            /distance_mapping/   which method used to map between correlation and distance, correlation is between [-1, 1], 
                                 distance is between [0, 1], 0 means close and 1 means distant, equal to 'shift' or 'abs', 
                                 'shift'   : f(x) = (1-x)/2
                                 'abs'     : f(x) = 1-|x|                
        
        Outputs:
            /Q/                  (N,N) numpy 2d-array, the filtered correlation matrix 
            Z_bar                the linkage matrix in scipy's linkage format with f(x) as distance, ready for dendrogram plot, see
                                 http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage
            /leaf_sort/          list of indices representing sorting of original correlation matrix C
    """
    # convert inputs in numpy ndarray, copy and/or expand dimension if needed
    C         = np.array(C, copy=False, ndmin=2)
    col_names = np.array(col_names, copy=False, ndmin=1)
    
    # scipy linkage assumes distance measue where large number is distant and 0.0 is self position, we need to convert input C
    if distance_mapping == 'shift':
        C_bar = (1.0-C) / 2.0
    elif distance_mapping == 'abs':
        C_bar = 1.0 - np.abs(C)
    else:
        raise RuntimeError('unknown distance_mapping, %s, shift or abs accepted'%distance_mapping)
        
    # for numerical reasons, diagnoal entries might not be 0.0, fix them
    C_bar[np.diag_indices_from(C_bar)] = 0.0
    
    # convert matrix to linkage function input format
    C_bar_condensed = distance.squareform(C_bar)
    
    # run linkage analysis
    Z_bar = hierarchy.linkage(C_bar_condensed, linkage_method)
        
    # convert disances back to correlation sapce 
    Q = distance.squareform(hierarchy.cophenet(Z_bar))
    if distance_mapping == 'shift':
        Q   = 1.0 - 2.0*Q
    elif distance_mapping == 'abs':
        Q   = 1.0 - Q
        neg = (C < 0.0).astype(np.int)        
        Q   = (np.ones(Q.shape)-2*neg)*Q  

    # for numerical reasons, diagnoal entries might not be 1.0, fix them
    Q[np.diag_indices_from(Q)] = 1.0
    
    # sorting only
    # Note: qz's scipy version (0.10.1) is outdated that's missing ability to specify which ax to plot for hierarchy dendrogram function
    ret_dict = hierarchy.dendrogram(Z_bar, count_sort='descending', no_plot=True)
    leaf_order = ret_dict['leaves']
    
    return [Q, Z_bar, leaf_order]
