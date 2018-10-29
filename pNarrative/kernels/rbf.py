
def rbf(V1, V2, args):
    import numpy as np
    assert isinstance(args, dict)
    assert all([argument in ["sigma", "el"] for argument in args.keys()])
    sigma = args["sigma"]
    el = args["el"]

    n1 = len(V1)
    n2 = len(V2)
    V1 = np.array(V1)
    V2 = np.array(V2)

    X = np.empty(shape=(n1, n2))

    for i, value1 in enumerate(V1):
        X[i,] = (sigma**2)*np.exp(-0.5*((value1 - V2)/el)**2)

    return X



if __name__ == "__main__":
    import numpy as np
    import time
    x1 = np.random.randint(low=0, high=100, size=3000)
    x2 = np.random.randint(low=0, high=100, size=3000)

    t = time.process_time()
    rbf(V1=x1, V2=x2, sigma=1, el=1)
    elapsed_time = time.process_time() - t
    elapsed_time
