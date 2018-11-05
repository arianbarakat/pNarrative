def scale(x, limits, custom_max = None, custom_min = None):
    import numpy as np
    assert isinstance(limits, tuple)
    assert len(limits) == 2
    x = np.array(x)

    if custom_min == None:
        x_min = np.nanmin(x)
    else:
        x_min = custom_min
    if custom_max == None:
        x_max = np.nanmax(x)
    else:
        x_max = custom_max


    a = limits[0]
    b = limits[1]

    return (b-a)*((x - x_min)/(x_max - x_min)) + a


def normalizeNarrativeTime(x):
    return scale(x, limits=(0,100))
