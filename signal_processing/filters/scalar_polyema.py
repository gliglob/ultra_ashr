from   qz.analytics.signal_processing.filters.base.scalar_filter_base import ScalarFilterBase
from   qz.analytics.signal_processing.utils.fixed_length_circular_buffer import FixedLengthCircularBuffer
import numpy


class ScalarPolyEma(ScalarFilterBase):

    def __init__(self, *args, **kwargs):

        # base class ctor first
        ScalarFilterBase.__init__(self, *args, **kwargs)

        # all poly emas have an order
        self._order            = kwargs.get('order', 1)
        self._zero_based_order = self._order - 1

        #--------------------------------------------------------------------
        # buffers

        # 1 linear buffer for lags on output y[n]
        self._Ycoef       = [0.0 for x in range(self._order)]

        # 1 circular buffer for lags on output y[n]
        self._yn          = FixedLengthCircularBuffer(self._order)

        # we only have 1 x[n] for polyemas
        self._Xcoef       = 1.0
        self._xn          = 0.0

        #--------------------------------------------------------------------
        # initialization

        self._init        = False
        self._v0          = 0.0

        #--------------------------------------------------------------------
        # filter parameters

        self._inv_gain    = 1.0    # gain adjustment
        self._M1          = 1.0    # location parameter

        #--------------------------------------------------------------------
        # event count to determine when the filter is ready

        self._event_count = 0

        #--------------------------------------------------------------------
        # in this pythonic environ need to have more explicit assurance that the filter is made

        self._is_made     = False


    #--------------------------------------------------------------------
    # main interface

    # a filter must be made, to make a filter the location parameter M1 is required
    def make(self, M1):

        # capture
        self._M1 = M1

        # 1) adjust M1 by order m
        M1_by_m = float(M1) / self._order

        # 2) compute parameter p
        p = M1_by_m / (M1_by_m + 1.0)

        # 3) compute gain adjustment
        self._inv_gain = pow((1.0 - p), self._order)

        # 4) compute Ycoef for recursion
        #    The convolution below expands (1-p z^-1)^order as polynomial coefs to z^-1.
        #    There are (order + 1) terms, the first term is 1. Thus:
        #           1 + phi_1 z^-1 + phi_2 z^-2 + .. + phi_m z^-m

        poly_expansion = reduce( lambda x,y: numpy.convolve(x,y), [[1, -p] for x in range(self._order)] )

        #    Keep only (phi_1, phi_2, .., phi_m) in an m-size linear buffer.
        #    In addition, flip coef sign to reflect that these terms are shifted to the rhs of the finite-diff eq

        self._Ycoef = [ -poly_expansion[i] for i in range(len(poly_expansion)) if i > 0 ]

        # prepare the filter
        self.reset()

        # declare
        self._is_made = True


    def reset(self):
        self._v0          = 0.0
        self._init        = False
        self._xn          = 0.0
        self._event_count = 0
        self._yn.reset()

    def relevel(self, v = 0.0):
        self.reset()
        self._v0          = v
        self._init        = True

    def update(self, v):

        # capture level if filter is uninitialized
        self._update(v)

        # update xn
        self._xn = v - self._v0

        # prepare yn circ buf
        self._yn.toFirst()

        # the recursion is
        #   phi_1 y[n-1] + phi_2 y[n-2] + .. + phi_m y[n-m] + inv_gain x[n]
        #
        # the linear buffer phi -> Ycoef[i] has its index increment
        # the circular buffer yn is called with .prev() to get lag values
        yn =  sum( [ self._Ycoef[i] * self._yn.prev() for i in range(self._order) ] )
        yn += self._inv_gain * self._xn

        # push this update to the yn circ buff
        self._yn.push(yn)

        # lastly, incr the event counter
        self._event_count += 1


    def value(self):

        # must restore the initial offset and apply the filter weight
        return (self._yn.first() + self._v0) * self._weight

    def isReady(self):

        # is-ready might be based on several scales, right now I'll just use M1
        return self._is_made and (self._event_count > self._M1)

    def isMade(self):

        return self._is_made

    #--------------------------------------------------------------------
    # getters

    def getOrder(self):
        return self._order

    def getLocation(self):
        return self._M1

    def getName(self):
        return self._name

    def getWeight(self):
        return self._weight

    def getInvGain(self):
        return self._inv_gain

    def getEventCount(self):
        return self._event_count

    #--------------------------------------------------------------------
    # reports

    def writeRecursion(self, logger):
        pass

    def writeFilterAttributes(self, logger):
        pass

    # local methods
    def _update(self, v):

        if not self._init:
            self._v0   = v
            self._init = True

    def _initialize(self):
        pass

    def _getCoefs(self):

        return [self._Xcoef, self._Ycoef]
