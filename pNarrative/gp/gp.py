import numpy as np
import math


class GP():

    def __init__(self, x, y, kernel = None, noise_sigma = 1):
        import numpy as np
        from pNarrative.util import normalization
        assert isinstance(x, (list, np.ndarray, np.generic))
        assert isinstance(y, (list, np.ndarray, np.generic))
        assert len(x) == len(y), "x and y must have the same number of dimensions"

        self.x = np.array(x)
        self.x_normalized = normalization.normalizeNarrativeTime(self.x)
        self.y = np.array(y)
        self.nDim = len(x)

        self.kernel = kernel
        self.noise_sigma = noise_sigma


    def train(self, kernel_parameters, filter_zeros = True, use_normalized_x = True):
        import numpy as np
        assert isinstance(kernel_parameters, dict), "Supply kernel parameters in a dictionary"
        assert isinstance(filter_zeros, bool)
        assert isinstance(use_normalized_x, bool)

        if filter_zeros:
            self.idx_to_keep = [idx for idx, value in enumerate(self.y) if value != 0]
        else:
            self.idx_to_keep = [idx for idx, value in enumerate(self.y)]

        if use_normalized_x:
            self.x_train = [self.x_normalized[to_keep] for to_keep in self.idx_to_keep]
            self.y_train = [self.y[to_keep] for to_keep in self.idx_to_keep]
        else:
            self.x_train = [self.x[to_keep] for to_keep in self.idx_to_keep]
            self.y_train = [self.y[to_keep] for to_keep in self.idx_to_keep]


        self.kernel_parameters = kernel_parameters
        self.K_train = self.kernel(self.x_train, self.x_train, args = kernel_parameters)
        self.L = np.linalg.cholesky(self.K_train + self.noise_sigma**2*np.identity(n=len(self.y_train)))
        self.alpha = np.linalg.solve(a=self.L, b = np.linalg.solve(a = self.L.T, b = self.y_train))

    def predict(self, x_new = None):
        import numpy as np
        import math
        if x_new == None:
            x_new = list(range(101))


        self.x_new = x_new
        self.K_star = self.kernel(self.x_train, V2= x_new, args = self.kernel_parameters)
        self.K_test = self.kernel(x_new, V2= x_new, args = self.kernel_parameters)

        predictive_mean = np.matmul(self.K_star.T, self.alpha)
        v = np.linalg.solve(a = self.L.T, b = self.K_star)
        predictive_covariance = self.K_test - np.matmul(v.T, v)

        upper95 = [pred_mean + 1.96*math.sqrt(abs(pred_var)) for pred_mean, pred_var \
                    in zip(predictive_mean,np.diag(predictive_covariance))]

        lower95 = [pred_mean - 1.96*math.sqrt(abs(pred_var)) for pred_mean, pred_var \
                    in zip(predictive_mean,np.diag(predictive_covariance))]

        self.predictions = {"predictive_mean": predictive_mean,\
                            "lower95":lower95,\
                            "upper95":upper95,\
                            "predictive_covariance": predictive_covariance,\
                            "predictive_variance": abs(np.diag(predictive_covariance))}
