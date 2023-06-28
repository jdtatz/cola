from linops import jax_fns
from linops import torch_fns
from linops.linear_algebra import kron
from linops.linear_algebra import lazify
from linops.linalg.sqrt import sqrt
from linops.ops import Diagonal
from linops.ops import SelfAdjoint
from linops.utils_test import parametrize, relative_error
from linops.utils_test import generate_spectrum, generate_pd_from_diag
from jax.config import config

config.update('jax_platform_name', 'cpu')
_tol = 1e-6


@parametrize([torch_fns, jax_fns])
def test_diagonal(xnp):
    dtype = xnp.float32
    diag = xnp.array([0.1, 0.2, 3., 4.], dtype=dtype)
    C = xnp.diag(diag**0.5)
    B = sqrt(Diagonal(diag=diag))

    rel_error = relative_error(C, B.to_dense())
    assert rel_error < _tol


@parametrize([torch_fns, jax_fns])
def test_kronecker(xnp):
    dtype = xnp.float32
    diag = xnp.array([9., 4., 9., 4.], dtype=dtype)
    diag1 = Diagonal(xnp.array([3., 3.], dtype=dtype))
    diag2 = Diagonal(xnp.array([3., 4. / 3.], dtype=dtype))
    soln = xnp.diag(diag**0.5)
    K = kron(diag1, diag2)
    approx = sqrt(K)

    rel_error = relative_error(soln, approx.to_dense())
    assert rel_error < _tol


@parametrize([torch_fns, jax_fns])
def test_general(xnp):
    dtype = xnp.float32
    diag = generate_spectrum(coeff=0.75, scale=1.0, size=15)
    A = xnp.array(generate_pd_from_diag(diag, dtype=diag.dtype, seed=21), dtype=dtype)
    A = SelfAdjoint(lazify(A))
    soln = xnp.array(generate_pd_from_diag(diag ** 0.5, dtype=diag.dtype, seed=21), dtype=dtype)
    approx = sqrt(A).to_dense()

    rel_error = relative_error(soln, approx)
    assert rel_error < _tol
