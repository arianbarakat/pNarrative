import numpy as np
import math


class GP():

    def __init__(self, x, y, kernel = None, noise_sigma = 1):
        import numpy as np
        from util import normalization
        assert isinstance(x, (list, np.ndarray, np.generic))
        assert isinstance(y, (list, np.ndarray, np.generic))
        assert len(x) == len(y), "x and y must have the same number of dimensions"

        self.x = np.array(x)
        self.x_normalized = normalization.normalizeNarrativeTime(self.x)
        self.y = np.array(y)
        self.nDim = len(x)

        self.kernel = kernel
        self.noise_sigma = noise_sigma


    def train(self, kernel_parameters):
        import inspect
        import numpy as np
        assert isinstance(kernel_parameters, dict), "Supply kernel parameters in a dictionary"

        self.kernel_parameters = kernel_parameters
        self.K_train = self.kernel(self.x_normalized, self.x_normalized, args = kernel_parameters)
        self.L = np.linalg.cholesky(self.K_train + self.noise_sigma**2*np.identity(n=self.nDim))
        self.alpha = np.linalg.solve(a=self.L, b = np.linalg.solve(a = self.L.T, b = self.y))

    def predict(self, x_new = None):
        import numpy as np
        if x_new == None:
            x_new = list(range(101))


        self.x_new = x_new
        self.K_star = self.kernel(self.x_normalized, V2= x_new, args = self.kernel_parameters)
        self.K_test = self.kernel(x_new, V2= x_new, args = self.kernel_parameters)

        predictive_mean = np.matmul(self.K_star.T, self.alpha)
        v = np.linalg.solve(a = self.L.T, b = self.K_star)
        predictive_covariance = self.K_test - np.matmul(v.T, v)

        self.predictions = {"predictive_mean": predictive_mean,\
                            "predictive_covariance": predictive_covariance,\
                            "predictive_variance": np.diag(predictive_covariance)}
