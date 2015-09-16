from   collections import deque
from   qz.analytics.signal_processing.filter_banks.scalar_homogeneous_differencer import ScalarHomogeneousDifferencer
from   qz.analytics.signal_processing.filter_banks.scalar_homogeneous_double_differencer import ScalarHomogeneousDoubleDifferencer
from   qz.analytics.signal_processing.filters.base.scalar_filter_base import ScalarFilterBase

class SlopeCurvatureFilterBank(ScalarFilterBase):

    def __init__(self, *args, **kwargs):
        """
        kwarg keys:
            name
            weight
            arm_ratio
            order
        """

        # this filter bank has a name
        ScalarFilterBase.__init__(self, *args, **kwargs)

        """
        This filter bank looks like this:

                |---------------------------------------------|
                |                                             |
                |                --------------               |
                |   ----------- |  diffr M1   |---------------|---->  slope
                | /              --------------               |
        px  --->|-                                            |
                | \                                           |
                |  \          --------------------            |
                |   \---------|  dbl-diffr M1/2  |------------|---->  curvature
                |             --------------------            |
                |                                             |
                |---------------------------------------------|

        """

        # aux
        this_order     = kwargs.get('order', 1)
        name_slope_arm = "%s-slope"  % kwargs.get('name', 'scf')
        name_curv_arm  = "%s-curv"   % kwargs.get('name', 'scf')


        # the slope filter
        self._slope_filter = ScalarHomogeneousDifferencer(name=name_slope_arm, order=this_order, weight=1.0)

        # the curvature filter. This filter is a chain of two half-M1 differencers
        self._curv_filter  = ScalarHomogeneousDoubleDifferencer(name=name_curv_arm, order=this_order, weight=1.0)

        self._meta_data_queue = deque()

        #--------------------------------------------------------------------
        # in this pythonic environ need to have more explicit assurance that the filter is made

        self._is_made = False


    #--------------------------------------------------------------------
    # main interface

    # make the differencer, which makes the two underlying filters
    def make(self, slope_M1):

        # simply make the slope and curvature filters, use M1/2 for the curvature filter.
        self._slope_filter.make(slope_M1)
        self._curv_filter.make(slope_M1/2.0)
        self._meta_data_queue = deque(maxlen=slope_M1)

        # set
        self._is_made = True

    def reset(self):
        self._slope_filter.reset()
        self._curv_filter.reset()

    def relevel(self, v):
        self._slope_filter.relevel(v)
        self._curv_filter.relevel(v)

    def update(self, v, meta_data=None):
        self._slope_filter.update(v)
        self._curv_filter.update(v)
        if meta_data:
            self._meta_data_queue.append(meta_data)

    def value(self):

        # return a tuple (slope, curvature)
        return [self._slope_filter.value(), self._curv_filter.value()]

    def getMetaDataQueue(self):
        return self._meta_data_queue

    def isReady(self):

        return self._slope_filter.isReady() and self._curv_filter.isReady()

    def isMade(self):

        return self._is_made

    #--------------------------------------------------------------------
    # getters

    def getProperties(self):

        prop = {}
        prop['order']     = self._slope_filter.getOrder()
        prop['name']      = self._name
        prop['weight']    = self._weight

        return prop

    def getArms(self):

        return {'slope': self._slope_filter, 'curve': self._curv_filter}
