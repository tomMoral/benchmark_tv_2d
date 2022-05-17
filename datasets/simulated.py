from benchopt import BaseDataset
from benchopt import safe_import_context

with safe_import_context() as import_ctx:
    import numpy as np
    from scipy.signal import fftconvolve


class Dataset(BaseDataset):

    name = "Simulated"

    # List of parameters to generate the datasets. The benchmark will consider
    # the cross product for each key in the dictionary.
    # cos + bruit ~ N(mu, sigma)
    parameters = {
        'sigma': [0.1],
        'mu': [0],
        'K': [50],
        'type_A': ['identity', 'diagonal', 'triangular', 'random']}

    def __init__(self, mu=0, sigma=0.3, K=10,
                 type_A='identity', random_state=27):
        # Store the parameters of the dataset
        self.mu = mu
        self.sigma = sigma
        self.K = K
        self.type_A = type_A
        self.random_state = random_state

    def set_A(self, rng):
        if self.type_A == 'diagonal':
            A = np.diag(rng.random(self.K))
        elif self.type_A == 'triangular':
            A = np.triu(rng.randn(self.K, self.K))
        elif self.type_A == 'random':
            A = rng.randn(self.K, self.K)
        else:
            A = np.eye(self.K, dtype=float)
        return A

    def get_data(self):
        t = np.arange(self.K)
        rng = np.random.RandomState(47)
        y = np.cos(np.pi*t/self.K*10) + np.zeros((self.K, self.K))
        A = self.set_A(rng)
        y_blurred = fftconvolve(y, A, mode="same") + \
            rng.normal(self.mu, self.sigma, size=(self.K, self.K))
        data = dict(A=A, y=y_blurred)

        return y_blurred .shape[0], data
