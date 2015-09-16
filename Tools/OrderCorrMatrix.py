import numpy as np
import itertools

# sort the corr matrix

def OrderCorrMatrix(corr_matrix, colnames, leaf_order):
    '''Sort the correlation matrix given a list of order that we want to apply
    Input:  /corr_matrix/, /colnames/, /leaf_order/
    Output: /corr_matrix_ordered/, /colnames_ordered/'''
    
    colnames_ordered = [colnames[i] for i in leaf_order]
    length = len(leaf_order)
    _helper_indices = dict(zip(range(length), leaf_order))
    corr_matrix_ordered = np.ones((length, length))
    for i in itertools.permutations(range(length), r = 2):
        corr_matrix_ordered[i] = corr_matrix[(_helper_indices[i[0]], _helper_indices[i[1]])]
    
    return corr_matrix_ordered, colnames_ordered
