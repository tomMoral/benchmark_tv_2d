from benchopt import BaseObjective
from benchopt import safe_import_context

with safe_import_context() as import_ctx:
    import numpy as np
    import torch
    import deepinv as dinv
    from benchmark_utils.shared import huber
    from benchmark_utils.matrix_op import grad


class Objective(BaseObjective):
    min_benchopt_version = "1.5"
    name = "TV2D"

    parameters = {'reg': [0.02],
                  'delta': [0.9],
                  'isotropy': ["anisotropic", "isotropic"],
                  'data_fit': ["lsq", "huber"]}

    def linop(self, x2, size=False):
        if not size:
            size = x2.shape
        x = torch.from_numpy(x2)
        if torch.cuda.is_available():
            device = dinv.utils.get_freer_gpu()
        else:
            device = 'cpu'
        operator = dinv.physics.Inpainting(
            tensor_size=size,
            mask=0.5,
            device=device
        )
        return operator(x).numpy().squeeze(0)

    def set_data(self, A, y):
        self.A = A
        self.y = y
        self.reg = self.reg

    def evaluate_result(self, u):
        if self.A != 0:
            R = self.y - self.A @ u  # residuals
        else:
            R = self.y - self.linop(u)

        if self.data_fit == "lsq":
            loss = .5 * np.linalg.norm(R) ** 2
        else:
            loss = huber(R, self.delta)

        if self.isotropy == "isotropic":
            penalty = self.isotropic_tv_value(u)
        else:
            penalty = self.anisotropic_tv_value(u)

        return loss + self.reg * penalty

    def get_one_result(self):
        return np.zeros(self.y.shape)

    def get_objective(self):
        return dict(A=self.A,
                    reg=self.reg,
                    delta=self.delta,
                    data_fit=self.data_fit,
                    y=self.y,
                    isotropy=self.isotropy)

    def isotropic_tv_value(self, u):
        gh, gv = grad(u)
        return (np.sqrt(gh ** 2 + gv ** 2)).sum()

    def anisotropic_tv_value(self, u):
        gh, gv = grad(u)
        return (np.abs(gh) + np.abs(gv)).sum()
