
def rolling_mean(x, wdw):
    import pandas as pd
    assert isinstance(wdw, int)
    assert wdw <= len(x) and wdw > 0

    return list(pd.Series(x).rolling(window=wdw).mean())







if __name__ == "__main__":
    import numpy as np
    vector_x = np.random.randint(low=-10, high=10, size = 10)
    vector_x
    rolling_mean(x = vector_x, wdw= -1)
