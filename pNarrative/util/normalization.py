def scale(x, limits):
    import numpy as np
    assert isinstance(limits, tuple)
    assert len(limits) == 2
    x = np.array(x)
    x_min = np.min(x)
    x_max = np.max(x)

    a = limits[0]
    b = limits[1]

    return (b-a)*((x - x_min)/(x_max - x_min)) + a


def normalizeNarrativeTime(x):
    return scale(x, limits=(0,100))
