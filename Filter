# construct and apply filters (options include differencer, poly ema)
def Filter(name, data, M1, filter_type):
    if  filter_type == 'differencer':
        # apply the differencer filter (poly.ema, in qz-analytics)
        # construct filters
        from qz.analytics.signal_processing.filter_banks.scalar_homogeneous_differencer import ScalarHomogeneousDifferencer as Differencer
        order = 3
        filter = Differencer(name = name, weight = 1.0, order = order)
        filter.make(M1)
        filter.relevel()
        # apply filters
        filtered = [0.0 for x in range(len(data))]
        for i in range(len(data)):
            filter.update(data[i])
            filtered[i] = filter.value()
    elif filter_type == 'pema':
        from qz.analytics.signal_processing.filters.polyema.scalar_polyema import ScalarPolyEma
        order = 3
        filter = ScalarPolyEma(name = name, weight = 1.0, order = order)
        filter.make(M1)
        filter.relevel()
        # apply filters
        filtered = [0.0 for x in range(len(data))]
        for i in range(len(data)):
            filter.update(data[i])
            filtered[i] = filter.value()  
    return filtered
