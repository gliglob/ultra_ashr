def PolyEmaConstruction(name, data, M1, filter_instance = None, order = 3):

    """
    Apply the poly ema filter
    Input: 
    /name/: name of the filter
    /data/: data to be filtered
    /M1/:   M1 of the differencer filter
    /filter_instance/: default is None, Otherwise is a previously computed Slope curvature instance, usually loaded from local
    /order/: order of the filter
    Output:
    /Filter/: the filter instance, that can be pickled and reused
    /Integrated/: filtered integrated differencer value, length = len(data)
    """

    # apply the differencer and double differencer filter 
    # construct filters
    from signal_processing.filters.polyema.scalar_polyema import ScalarPolyEma
    if not filter_instance:
        Filter = ScalarPolyEma(name = name, weight = 1.0, order = order)
        Filter.make(M1)
        Filter.relevel(data[0])
    else:
        Filter = filter_instance
    # apply filters
    Filtered = [0.0 for x in range(len(data))]
    for i in range(len(data)):
        Filter.update(data[i])
        Filtered[i] = Filter.value()
    return Filtered, Filter
