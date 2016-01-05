'''
Id:          "$Id: scalar_homogeneous_integrated_differencer.py,v 1.3 2015/11/19 21:01:06 jay.damask Exp $"
Copyright:   Copyright (c) 2015 Bank of America Merrill Lynch, All Rights Reserved
Description: This filter container holds a scalar_homogeneous_differencer and integrates its
             output value. 
Test:        qz.tests.unittests.analytics.signal_processing.filter_banks.scalar_homogeneous_integrated_differencer
'''

from qz.analytics.signal_processing.filters.base.scalar_filter_base import ScalarFilterBase
from qz.analytics.signal_processing.filter_banks.scalar_homogeneous_differencer import ScalarHomogeneousDifferencer

class ScalarHomogeneousIntegratedDifferencer(ScalarFilterBase):
    
    def __init__(self, *args, **kwargs):
        """
        kwarg keys:
            name
            weight
            arm_ratio
            order
        """
        
        # the integrated differencer has a name
        ScalarFilterBase.__init__(self, *args, **kwargs)
        
        #--------------------------------------------------------------------
        # underlying differencer

        # make differencer name
        kwargs['name']          = "%s.%s" % (kwargs.get('name', 'idiffr'), "diffr")
        
        # instantiate a differencer filter
        self._differencer = ScalarHomogeneousDifferencer(*args, **kwargs)

        #--------------------------------------------------------------------
        # local variables

        # default the gain adj
        self._gain_adj          = 0.0

        # hold the accumulated value
        self._accumulated_value = 0.0
        
        #--------------------------------------------------------------------
        # in this pythonic environ need to have more explicit assurance that the filter is made

        self._is_made           = False

    #--------------------------------------------------------------------
    # main interface

    # make the integrated differencer
    def make(self, wireframe_M1p_M1m_avg):
        """
        Make the integrated differencer.
        inputs:
            /wireframe_M1p_M1m_avg/     the value of (M1_+ + M1_-) / 2, the delay of a differencer
        
        result:
            a filter object that is correctly configured for use.
        """
        
        # make the differencer
        self._differencer.make(wireframe_M1p_M1m_avg)
        
        # recover the difference in pos and neg arm locations
        p = self._differencer.getProperties()
        
        self._gain_adj = 1.0 / (p['M1_neg'] - p['M1_pos'])
        
        # set the made flag
        self._is_made = True
        
    
    def reset(self):
        self._differencer.reset()
        self._accumulated_value = 0
        
    def relevel(self, v):
        self._differencer.relevel(v)
        self._accumulated_value = 0
        
    def update(self, v):
        self._differencer.update(v)
        self._accumulated_value += self._gain_adj * self._differencer.value()
        
    def value(self):
        return self._accumulated_value + self._differencer.initial_value()
        
    def initial_value(self):
        return self._differencer.initial_value()
        
    def isReady(self):
        return self._differencer.isReady()
        
    def isMake(self):
        return self._differencer.isMade()
        
        
    #--------------------------------------------------------------------
    # getters

    def getProperties(self):

        prop = {}
        prop['name']      = self.getName()
        prop['gain_adj']  = self._gain_adj
        
        diffr_props = self._differencer.getProperties()
        
        prop['diffr.name']      = diffr_props['name']
        prop['diffr.order']     = diffr_props['order']
        prop['diffr.weight']    = diffr_props['weight']
        prop['diffr.arm_ratio'] = diffr_props['arm_ratio']

        return prop
