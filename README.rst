2-dimensional Total Variation (TV) Benchmark
============================================
|Build Status| |Python 3.6+|

This benchmark is dedicated to solver of TV-2D regularised regression problem:

$$\\boldsymbol{u} \\in \\underset{\\boldsymbol{u} \\in \\mathbb{R}^{n \\times m}}{\\mathrm{argmin}} f(\\boldsymbol{y}, A \\boldsymbol{u}) + g(\\boldsymbol{u})$$


- $\\boldsymbol{y} \\in \\mathbb{R}^{n \\times m}$ is a vector of observations or targets.
- $A \\in \\mathbb{R}^{n \\times n}$ is a design matrix or forward operator.
- $\\lambda > 0$ is a regularization hyperparameter.
- the datafit is $f(\\boldsymbol{y},A\\boldsymbol{u})=\\sum\_{k=1}^{n}\\sum\_{l=1}^{m} l(y\_{k,l}, (A\\boldsymbol{u}))_{k,l}$, where $l$ can either be the quadratic loss $l(y, x) = \\frac{1}{2} \\vert y - x \\vert_2^2$, or the Huber loss $l(y, x) = h\_{\\delta} (y - x)$ defined by


$$
h\_{\\delta}(t) = \\begin{cases} \\frac{1}{2} t^2 & \\mathrm{ if } \\vert t \\vert \\le \\delta \\\\ \\delta \\vert t \\vert - \\frac{1}{2} \\delta^2 & \\mathrm{ otherwise} \\end{cases}
$$


- $D_1 \\in \\mathbb{R}^{(n-1) \\times n}$ and $D_2 \\in \\mathbb{R}^{(m-1) \\times m}$ are finite difference operators, such that the regularised TV-2D term $g(\\boldsymbol{u}) = \\lambda \\| \\boldsymbol{u} \\|\_{TV}$ expressed as follows.


In isotropic cases:


$$
g(\\boldsymbol{u}) = \\lambda \\| \\sqrt{ (D\_1 \\boldsymbol{u})^2 + (\\boldsymbol{u} D\_2^{\\top})^2 } \\|\_{1} = \\lambda \\sum\\limits\_{k = 1}^{n-1} \\sum\\limits\_{l = 1}^{m-1} \\sqrt{\\vert u\_{k+1,l} - u\_{k,l} \\vert^2 + \\vert u\_{k,l+1} - u\_{k,l} \\vert^2}
$$


In anisotropic cases:


$$
g(\\boldsymbol{u}) = \\lambda \\| D_1 \\boldsymbol{u} \\|_{1} + \\| \\boldsymbol{u} D_2^{\\top} \\|\_{1} = \\lambda \\sum\\limits\_{k = 1}^{n-1} \\sum\\limits\_{l = 1}^{m-1} (\\vert u\_{k+1,l} - u\_{k,l} \\vert + \\vert u\_{k,l+1} - u\_{k,l} \\vert)
$$


where n (or `height`) and m (or `width`) are the dimensions of the image.

The type of loss is controlled by the ``data_fit`` attribute of the Objective.

Install
--------

A simple version of this benchmark can be run using the following commands:

.. code-block::

   $ pip install -U benchopt
   $ git clone https://github.com/benchopt/benchmark_tv_2d
   $ cd benchmark_tv_2d
   $ benchopt install --config example_config.yml
   $ benchopt run --config example_config.yml

To run the benchmark on a limited subset of Objectives, Solvers or Datasets, visit https://benchopt.github.io/api.html or use the command ```benchopt run -h``.

.. |Build Status| image:: https://github.com/benchopt/benchmark_tv_2d/workflows/Tests/badge.svg
   :target: https://github.com/benchopt/benchmark_tv_2d/actions
.. |Python 3.6+| image:: https://img.shields.io/badge/python-3.6%2B-blue
   :target: https://www.python.org/downloads/release/python-360/
