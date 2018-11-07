def find_nearest(x, value):
    import numpy as np
    x = np.array(x)

    assert np.max(x) > value, "Chose a smaller value"
    assert np.min(x) < value, "Chose a greater value"

    idx = (np.abs(x - value)).argmin()
    return(idx)
