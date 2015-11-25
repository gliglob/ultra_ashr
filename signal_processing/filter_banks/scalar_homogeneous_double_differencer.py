from   signal_processing.filter_banks.scalar_homogeneous_differencer import ScalarHomogeneousDifferencer
from   signal_processing.filters.base.scalar_filter_base import ScalarFilterBase


class ScalarHomogeneousDoubleDifferencer(ScalarFilterBase):

    def __init__(self, *args, **kwargs):
        """
        This double-differencer is a cascade of two differencers:

                |-------------------------------------------|
                |                                           |
                |   ----------------   ----------------     |
            --->|---|   diffr M1   |---|   diffr M1   |-----|---->  double difference
                |   ----------------   ----------------     |
                |                                           |
                |-------------------------------------------|

        This cascade halves the bandwidth of either differencer. When used in conjuction with a
        single differencer, the M1 value here must be 1/2 the M1 value of the single differencer.
        Specifically:

                single differencer: M1 = (tau_+ + tau_-) / 2
                double differencer: M1 = (tau_+ + tau_-) / 4

        With these conditions, the delay of the single- and double-differencer is nearly the same.


        kwarg keys:
            name
            weight
            arm_ratio
            order
        """

        # the differencer has a name
        ScalarFilterBase.__init__(self, *args, **kwargs)

        # instantiate an underlying poly-ema pair
        this_order      = kwargs.get('order', 1)
        name_1st_fltr   = "%s-1st" % kwargs.get('name', 'f')
        name_2nd_fltr   = "%s-2nd" % kwargs.get('name', 'f')

        # a note on weights: the filter output is the cascade of these two filters. The total filter
        # output weight needs to be 1/2

        self._1st_fltr  = ScalarHomogeneousDifferencer(name=name_1st_fltr, order=this_order, weight=1.0)
        self._2nd_fltr  = ScalarHomogeneousDifferencer(name=name_2nd_fltr, order=this_order, weight=0.5)

        #--------------------------------------------------------------------
        # in this pythonic environ need to have more explicit assurance that the filter is made

        self._is_made   = False


    #--------------------------------------------------------------------
    # main interface

    # make the differencer, which makes the two underlying filters
    def make(self, wireframe_M1p_Mpm_avg):

        self._1st_fltr.make(wireframe_M1p_Mpm_avg)
        self._2nd_fltr.make(wireframe_M1p_Mpm_avg)

        self._is_made = True

    def reset(self):

        self._1st_fltr.reset()
        self._2nd_fltr.reset()

    def relevel(self, v):

        # the double-differencer is a cascade
        self._1st_fltr.relevel(v)
        self._2nd_fltr.relevel( self._1st_fltr.value() )

    def update(self, v):

        # the double-differencer is a cascade
        self._1st_fltr.update(v)
        self._2nd_fltr.update( self._1st_fltr.value() )

    def value(self):

        # The double-differencer value is that output of the second diff-r
        return self._2nd_fltr.value()

    def isReady(self):

        return self._is_made and (self._1st_fltr.isReady() and self._2nd_fltr.isReady())

    def isMade(self):

        return self._is_made

    #--------------------------------------------------------------------
    # getters

    def getProperties(self):

        prop = {}
        prop['order']     = self._1st_fltr.getOrder()  # Hack
        prop['arm-ratio'] = self._1st_fltr._arm_ratio  # Hack
        prop['name']      = self._name
        prop['weight']    = self._weight

        return prop
