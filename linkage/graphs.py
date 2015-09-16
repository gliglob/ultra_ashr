import networkx as nx
import numpy as np
import qz.ui as ui
import matplotlib.pyplot as plt
import qz.lib.matplot
    
def plot_correlation_matrix(C, col_names, col_order=None, ax=None, show=False):
    """ Plot given correlation matrix as a heatmap
        
        Inputs:
            /C/                  (N,N) numpy 2d-array, the original correlation matrix
            /col_names/          (N,1) numpy 1d-array, column names of C
            /col_order/          list of indices representing sorting of C
            /ax/                 matplit axes to plot on
            /show/               show in a qz frame with current matplot figure if True
                        
        Outputs:
            new qz window        bring up a new qz window with current figure if show is True
    """
    # convert inputs in numpy ndarray, copy and/or expand dimension if needed
    C         = np.array(C,         copy=True,  ndmin=2)
    col_names = np.array(col_names, copy=True,  ndmin=1)
    if col_order is not None:
        col_order = np.array(col_order, copy=False, ndmin=1)
    
    # validate inputs
    n = C.shape[1]
    if C.shape[0] != n:
        raise RuntimeError('input C must be a square matrix, got [%d, %d]'%(C.shape[0], C.shape[1]))
    if np.all(C.T != C):
        raise RuntimeError('input C must be Hermitian, i.e. C.T = C')
    if col_names.shape[0] != n:
        raise RuntimeError('num column names, %d, must be same as num columns in C, %d'%(col_names.shape[0], n))
    
    # reorder column if col_order is given
    if col_order is not None:
        C         = C[col_order]
        C         = C.T[col_order]
        col_names = col_names[col_order]
    
    # use current axes if ax is None
    if ax is None:
        ax = plt.gca()
    else:
        # passing axes to pcolor show work but it doesn't. force to plot on give axes for now
        plt.sca(ax)
    
    # pcolor(mesh) assumes plotting starts (x,y) at (0,0) not matrix orienation from (0, y_max)
    # so need reverse them    
    reverse_slice = range(n-1, -1, -1) 
    
    # matplotlib doc says pcolormesh is faster than pcolor on large matrix. 
    # use pcolor here since in qz's scipy version, pcolor accepts edgecolors parameter 
    # while pcolormesh doesn't. both should in newest version.   
    plt.pcolor(C[reverse_slice], edgecolors='k', vmin=-1.0, vmax=1.0) 
    plt.colorbar() 
    
    # tailor plot
    ax.set_xticks(np.arange(n)+0.5)
    ax.set_xticklabels(col_names, rotation=90, fontsize='x-small')
    ax.set_yticks(np.arange(n)+0.5)
    ax.set_yticklabels(col_names[reverse_slice], fontsize='x-small')

    if show:
        # show current figure
        f = ui.Frame( ui.VL( [ qz.lib.matplot.MatPlotWin(plt.gcf()) ] ), size=(800,800) )
        f.show()
        
''' #TODO add dendrogram and MST plotting later
def plot_tumminello_dendrogram(Z_bar, col_name, title='Dendrogram', show=True):
    """ plot linkage matrix Z_Bar from output of tumminello_correlation_filter function
        return ordering of the leaf of default sorting criteria
    """
    fig = qz.lib.matplot.plt.figure()
    # use one of distance_sort or count_sort, = 'aescending' or 'descending'
    ret_dict = dendrogram(Z_bar, count_sort='descending')
    leaf_order = ret_dict['leaves']
    if show:
        xticks = qz.lib.matplot.plt.xticks()
        qz.lib.matplot.plt.xticks(xticks[0], col_name[leaf_order], rotation=90) 
        # since Z_bar has distance as 1-rho, convert y-axis value back to rho
        qz.lib.matplot.plt.yticks(np.arange(1,-0.1,-0.1), np.arange(0,1.1,0.1))
        fig.suptitle(title)
        f = ui.Frame( ui.VL( [ qz.lib.matplot.MatPlotWin(fig) ] ), size=(800,800) )
        f.show()
    return leaf_order
    
def plot_MST(T):
    fig = qz.lib.matplot.plt.figure()
    nx.draw(T)
    f = ui.Frame( ui.VL( [ qz.lib.matplot.MatPlotWin(fig) ] ), size=(800,800) )
    f.show()
'''

def test():
    fig, axes = plt.subplots(1,1,1)
    col_names = np.asarray(['AIG', 'IBM', 'BAC', 'MER', 'AXP', 'MOT', 'OXY', 'TXN', 'RD', 'SLB'])
    C = np.asarray([[ 1.   ,  0.413,  0.518,  0.543,  0.529,  0.341,  0.271,  0.231, 0.412,  0.294],
                    [ 0.413,  1.   ,  0.471,  0.537,  0.617,  0.552,  0.298,  0.475, 0.373,  0.27 ],
                    [ 0.518,  0.471,  1.   ,  0.547,  0.592,  0.4  ,  0.258,  0.349, 0.37 ,  0.276],
                    [ 0.543,  0.537,  0.547,  1.   ,  0.664,  0.422,  0.347,  0.351, 0.414,  0.269],
                    [ 0.529,  0.617,  0.592,  0.664,  1.   ,  0.533,  0.344,  0.462, 0.44 ,  0.318],
                    [ 0.341,  0.552,  0.4  ,  0.422,  0.533,  1.   ,  0.305,  0.582, 0.355,  0.245],
                    [ 0.271,  0.298,  0.258,  0.347,  0.344,  0.305,  1.   ,  0.193, 0.533,  0.591],
                    [ 0.231,  0.475,  0.349,  0.351,  0.462,  0.582,  0.193,  1.   , 0.258,  0.166],
                    [ 0.412,  0.373,  0.37 ,  0.414,  0.44 ,  0.355,  0.533,  0.258, 1.   ,  0.59 ],
                    [ 0.294,  0.27 ,  0.276,  0.269,  0.318,  0.245,  0.591,  0.166, 0.59 ,  1.   ]])
    plot_correlation_matrix(C, col_names, ax=axes, show=True)
    
def main():
    test()
