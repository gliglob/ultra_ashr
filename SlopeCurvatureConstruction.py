def SlopeCurvatureConstruction(name, data, M1, filter_instance = None, order = 3):
    """
    Compute the slope (differencer) and curvature (double differencer)
    NOTE: no missing data allowed
    Input: 
    /name/: name of the filter
    /data/: data to be filtered
    /M1/:   M1 of the differencer filter, then M1 of the double differencer is M1/2
    /filter_instance/: Default is None, Otherwise is a previously computed Slope curvature instance, usually loaded from local
    /order/: order of the filter
    Output:
    /Filter/: the filter instance, that can be pickled and reused
    /Slope/: filtered differencer value, length = len(data)
    /Curvature/: filtered double differencer value
    """

    # apply the differencer and double differencer filter 
    # construct filters
    from signal_processing.filter_banks.slope_curvature_filter_bank import SlopeCurvatureFilterBank as SlopeCurvature
    if not filter_instance:
        Filter = SlopeCurvature(name = name, weight = 1.0, order = order)
        Filter.make(M1)
        Filter.reset()
    else:
        Filter = filter_instance
    # apply filters
    Slope = [0.0 for x in range(len(data))]
    Curvature = [0.0 for x in range(len(data))]
    for i in range(len(data)):
        Filter.update(data[i])
        Slope[i] = Filter.value()[0]
        Curvature[i] = Filter.value()[1]
    return Slope, Curvature, Filter
