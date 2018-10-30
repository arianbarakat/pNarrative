def constant(V1, V2, args):
    import numpy as np
    assert isinstance(args, dict)
    assert all([argument in ["sigma"] for argument in args.keys()])
    sigma = args["sigma"]

    n1 = len(V1)
    n2 = len(V2)

    X = np.full(shape=(n1, n2), fill_value=sigma**2)

    return X



if __name__ == "__main__":
    import numpy as np
    x1 = np.random.randint(low=0, high=100, size=3000)
    x2 = np.random.randint(low=0, high=100, size=3000)

    consant(V1=x1, V2=x2, sigma=1)
