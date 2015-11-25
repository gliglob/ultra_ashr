def IntegratedDifferencerConstruction(name, data, M1, filter_instance = None, order = 3):

    """
    Apply the integrated differencer filter
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
    from signal_processing.filter_banks.scalar_homogeneous_integrated_differencer import ScalarHomogeneousIntegratedDifferencer as IntegratedDifferencer
    if not filter_instance:
        Filter = IntegratedDifferencer(name = name, weight = 1.0, order = order, arm_ratio = 3)
        Filter.make(M1)
        Filter.reset()
    else:
        Filter = filter_instance
    # apply filters
    Integrated = [0.0 for x in range(len(data))]
    for i in range(len(data)):
        Filter.update(data[i])
        Integrated[i] = Filter.value()
    return Integrated, Filter
