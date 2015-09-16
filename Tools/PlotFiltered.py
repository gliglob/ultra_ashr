
import pandas as pd
import numpy as np
import qztable
from matplotlib import pyplot as plt
from matplotlib import gridspec
from playground.huiliu.Tools.pdf_estimation import GeneratePDF

def PlotFiltered(data, alpha):
    
    '''Plots the filtered value, its pdf,cdf and its corresponding threshold at level alpha
    Input:  
        /data/ pd.DataFrame object or qztable or a list/numpy.array
        /alpha/ the significance level to plot the threshold level
    Output: 
        Show the plot
    '''
    
    if isinstance(data, pd.DataFrame):

        gs = gridspec.GridSpec(data.shape[1], 3, width_ratios = [4, 1, 1])
        
        for i, col in enumerate(list(data.columns.values)):
            col_data = data[col] / np.std(data[col])
            x, pdf, cdf, lower, upper = GeneratePDF(col_data, method = 'Robust_Student_t', lower_threshold = alpha, upper_threshold = 1 - alpha)
            ax1 = plt.subplot(gs[3*i])
            ax1.plot(range(0, len(data)), col_data)
            ax1.axhline(y = lower, linewidth = 3, color = 'red')
            ax1.axhline(y = upper, linewidth = 3, color = 'red')
            ax1.fill_between(range(0, len(data)), lower, upper, color = 'cyan', alpha = 1)
            ax1.set_xlim(0, len(data))
            ax1.set_title('Plot of ' + col + ' Fitered')
            ax2 = plt.subplot(gs[3*i+1])
            ax2.plot(pdf, x)
            ax2.set_title('PDF')
            ax3 = plt.subplot(gs[3*i+2])
            ax3.plot(cdf, x)
            ax3.set_title('CDF')
            
    elif isinstance(data, qztable.Table):

        gs = gridspec.GridSpec(data.shape[1], 3, width_ratios = [4, 1, 1])
        
        for i, col in enumerate(data.columnNames()):
            col_data = data.toDict()[col] / np.std(data.toDict()[col])
            x, pdf, cdf, lower, upper = GeneratePDF(col_data, method = 'Robust_Student_t', lower_threshold = alpha, upper_threshold = 1 - alpha)
            ax1 = plt.subplot(gs[3*i])
            ax1.plot(range(0, len(data)), col_data)
            ax1.axhline(y = lower, linewidth = 3, color = 'red')
            ax1.axhline(y = upper, linewidth = 3, color = 'red')
            ax1.fill_between(range(0, len(data)), lower, upper, color = 'cyan', alpha = 1)
            ax1.set_title('Plot of ' + col + ' Fitered')
            ax1.set_xlim(0, len(data))
            ax2 = plt.subplot(gs[3*i+1])
            ax2.plot(pdf, x)
            ax2.set_title('PDF')
            ax3 = plt.subplot(gs[3*i+2])
            ax3.plot(cdf, x)
            ax3.set_title('CDF')
            
    else:
        
        try:
            
            data = np.array(data)
            data = data / np.std(data)
            x, pdf, cdf, lower, upper = GeneratePDF(data, method = 'Robust_Student_t', lower_threshold = alpha, upper_threshold = 1 - alpha)
            gs = gridspec.GridSpec(1, 3, width_ratios = [4, 1, 1])
            ax1 = plt.subplot(gs[0])
            ax1.plot(range(0, len(data)), data)
            ax1.axhline(y = lower, linewidth = 3, color = 'red')
            ax1.axhline(y = upper, linewidth = 3, color = 'red')
            ax1.fill_between(range(0, len(data)), lower, upper, color = 'cyan', alpha = 1)
            ax1.set_title('Plot of filtered value')
            ax1.set_xlim(0, len(data))
            ax2 = plt.subplot(gs[1])
            ax2.plot(pdf, x)
            ax2.set_title('PDF')
            ax3 = plt.subplot(gs[2])
            ax3.plot(cdf, x)
            ax3.set_title('CDF')
            
        except:
            
            print "DATA TYPE NOT SUPPORTED"


    plt.show()
