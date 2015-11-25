class ScalarFilterBase(object):

    def __init__(self, *args, **kwargs):
        """
        kwargs keys:
            name
            weight

        ctor example:
            sfb = ScalarFilterBase(name = 'awesome-filter', weight = 1.0)

        """

        # all filters have a name, name set only by ctor
        self._name   = kwargs.get('name', None)

        # all filters have
        self._weight = kwargs.get('weight', 1.0)


    def setWeight(self, weight):
        self._weight = weight

    def setWeightFromDict(self, weight_dict):
        has_weight   = weight_dict.has_key(self._name)
        self._weight = weight_dict.get(self._name, self._weight)

        return has_weight

    def getName(self):
        return self._name

    def getWeight(self):
        return self._weight

    def report(self, logger):
        pass
