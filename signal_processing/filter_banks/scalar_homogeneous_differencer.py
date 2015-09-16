from qz.analytics.signal_processing.filters.base.scalar_filter_base import ScalarFilterBase
from qz.analytics.signal_processing.filters.polyema.scalar_polyema import ScalarPolyEma

class ScalarHomogeneousDifferencer(ScalarFilterBase):

    def __init__(self, *args, **kwargs):
        """
        kwarg keys:
            name
            weight
            arm_ratio
            order
        """

        # the differencer has a name
        ScalarFilterBase.__init__(self, *args, **kwargs)

        # /r/ is the ratio of long- to short-arm M1 (location) values. Typically r = 3.
        self._arm_ratio = kwargs.get('arm_ratio', 3)

        # instantiate an underlying poly-ema pair
        this_order      = kwargs.get('order', 1)
        name_pos_arm    = "%s-pos" % kwargs.get('name', 'f')
        name_neg_arm    = "%s-neg" % kwargs.get('name', 'f')

        self._pos_arm   = ScalarPolyEma(name=name_pos_arm, order=this_order, weight=1.0)
        self._neg_arm   = ScalarPolyEma(name=name_neg_arm, order=this_order, weight=-1.0)

        #--------------------------------------------------------------------
        # in this pythonic environ need to have more explicit assurance that the filter is made

        self._is_made   = False


    #--------------------------------------------------------------------
    # main interface

    # make the differencer, which makes the two underlying filters
    def make(self, wireframe_M1p_Mpm_avg):
        """
        The continuous-time analogue of wireframe_M1p_Mpm_avg is

                wireframe_M1p_Mpm_avg = (M1_+ + M1_-) / 2

        The arm ratio is defined by

                          r = M1_- / M1_+

        Therefore

              M1_- = r / (1 + r) * 2 * wireframe_M1p_Mpm_avg
              M1_+ = 1 / (1 + r) * 2 * wireframe_M1p_Mpm_avg

        """

        # make the pos and neg arms
        r      = self._arm_ratio
        M1_pos = 1.0 / (1.0 + r) * 2.0 * wireframe_M1p_Mpm_avg
        M1_neg = r / (1.0 + r) * 2.0 * wireframe_M1p_Mpm_avg

        self._pos_arm.make(M1_pos)
        self._neg_arm.make(M1_neg)


    def reset(self):
        self._pos_arm.reset()
        self._neg_arm.reset()

    def relevel(self, v):
        self._pos_arm.relevel(v)
        self._neg_arm.relevel(v)

    def update(self, v):
        self._pos_arm.update(v)
        self._neg_arm.update(v)

    def value(self):

        # generic return, sum of components. Internally, the pos and neg arms are
        # weighted by +/- 1.0, respectively.
        return (self._pos_arm.value() + self._neg_arm.value()) * self._weight

    def isReady(self):

        return self._is_made and (self._pos_arm.isReady() and self._neg_arm.isReady())

    def isMade(self):

        return self._is_made


    #--------------------------------------------------------------------
    # getters

    def getProperties(self):

        prop = {}
        prop['order']     = self._pos_arm.getOrder()
        prop['name']      = self.getName()
        prop['weight']    = self._weight
        prop['arm_ratio'] = self._arm_ratio

        return prop

    def getOrder(self):

        return self._pos_arm.getOrder()

    def getArms(self):

        return {'pos': self._pos_arm, 'neg': self._neg_arm}
