"""
Recover the Jacobi polynomial coefficient matrix from OEIS sequence A027614.

Goal
----
The Jacobi polynomials P_n^(mu,nu)(x) form a family parameterized by mu, nu.
Their coefficients assemble into a lower-triangular matrix J (the "Jacobi maxel")
where J[n, k] is the coefficient of x^k in P_n^(mu,nu)(x) (up to normalization).

Rather than computing J directly, we reconstruct it by exponentiating its matrix
logarithm, whose entries are governed by A027614.

Steps
-----
  1. Load A027614: the EGF numerator sequence a_0, a_1, ..., a_{n-1}.
  2. Build the subdiagonal shift matrix L, with L[i, i-1] = mu + i.
  3. Form the EGF sum  G = sum_{k>=1} (-1)^{k+1} * (a_k / k!) * L^k.
     G encodes the matrix logarithm of the normalized Jacobi matrix via A027614.
  4. Apply two diagonal similarity transforms (using Pochhammer symbols in mu+nu)
     to put G into canonical log form.
  5. Apply a further factorial diagonal similarity to normalize row/column scaling.
  6. Exponentiate the result to recover the normalized Jacobi matrix.
  7. Multiply on the left by a Jacobi-specific diagonal factor to get the full
     coefficient matrix J.
"""

import click
from typing import Optional
from sympy import (
    symbols,
    pprint,
    simplify,
    factor,
    together,
    Matrix,
    factorial,
    RisingFactorial,
)
from sympy.parsing.sympy_parser import parse_expr

from maxel.common import A027614_FP
from maxel.sequences import load_sequences, load_and_assign_to
from maxel.matrix import matrix_from_str, matrix_from_func, EMatrixType


# --- Diagonal matrix builders --------------------------------------------------


def make_diag_left(n):
    """Diagonal matrix D_L with D_L[j,j] = (mu+nu+1)_{2j} (even Pochhammer)."""

    def func_expr(i, j):
        return f"RisingFactorial(mu+nu+1,{2*j})"

    return matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)


def make_diag_right(n):
    """Diagonal matrix D_R with D_R[j,j] = (mu+nu+1)_{2j+1} (odd Pochhammer)."""

    def func_expr(i, j):
        return f"RisingFactorial(mu+nu+1,{2*j+1})"

    return matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)


def make_jacobi_diag(n):
    """
    Diagonal prefactor D_J with D_J[i,i] = (mu+nu+i+1)_i / i!
    Left-multiplying by D_J converts the normalized matrix into the full
    Jacobi coefficient matrix.
    """

    def func_expr(i, j):
        return f"RisingFactorial(mu+nu+i+1,j)/factorial({j})"

    diag = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    return diag.applyfunc(factor)


# --- Main ----------------------------------------------------------------------


@click.command()
@click.argument("n", type=int)
@click.option("--mu", type=int, default=None)
@click.option("--nu", type=int, default=None)
def main(n: int, mu: Optional[int] = None, nu: Optional[int] = None):
    _, _ = symbols("mu, nu")

    # ------------------------------------------------------------------
    # Step 1: Load A027614 — the EGF numerator coefficients
    # ------------------------------------------------------------------
    # A027614 provides integers a_0, a_1, a_2, ... such that the EGF
    #   sum_{k>=0} a_k * x^k / k!
    # encodes the relationship between the shift operator L and the Jacobi
    # matrix logarithm. We load the first n values and bind them to symbols.

    raw_values = load_sequences(A027614_FP)
    print("=" * 70)
    print("STEP 1 — A027614 EGF coefficients (first n values)")
    print("  a_k : the numerators of the EGF  sum_k a_k * x^k / k!")
    print("=" * 70)
    for k, v in enumerate(raw_values[:n]):
        print(f"  a_{k} = {v}")
    print(f"  ...")

    list_a = symbols(",".join([f"a{i}" for i in range(n)]))
    dict_a = load_and_assign_to(A027614_FP, list_a)

    # ------------------------------------------------------------------
    # Step 2: Build the subdiagonal shift matrix L
    # ------------------------------------------------------------------
    # L is a lower-triangular matrix with a single subdiagonal:
    #   L[i, i-1] = mu + i   (for i >= 1),  all other entries 0.
    # It acts as a "shift-down" operator whose spectral structure reflects
    # the Jacobi recurrence in mu.

    def func_expr(i, j):
        if i != j + 1:
            return "0"
        return "mu+i"

    sub_diag_mu = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    print()
    print("=" * 70)
    print("STEP 2 — Subdiagonal shift matrix L  (L[i, i-1] = mu + i)")
    print("=" * 70)
    pprint(sub_diag_mu)

    # ------------------------------------------------------------------
    # Step 3: Form the series G(x) = sum_{k>=1} (-1)^{k+1} (a_k/k!) x^k
    # ------------------------------------------------------------------
    # G(x) has the form of an EGF (exponential generating function): its
    # coefficients are a_k/k!. After substituting the A027614 values and
    # evaluating at the matrix L, G(L) becomes the matrix logarithm of a
    # normalized Jacobi matrix (up to conjugation).

    # First show G(x) as a scalar series — with symbolic a_k, then with
    # A027614 values — before evaluating at the matrix L.
    x = symbols("x")
    log_series_sym = sum(
        (-1) ** (k + 1) * a_k / factorial(k) * x**k for k, a_k in enumerate(list_a)
    )
    log_series_sym = log_series_sym  # keep as sum to show term structure

    log_series_num = log_series_sym.subs(dict_a)

    print()
    print("=" * 70)
    print("STEP 3 — Series G(x) = sum_{k>=1} (-1)^{k+1} (a_k / k!) x^k  [EGF shape]")
    print("  Scalar series with symbolic a_k (truncated at degree n-1):")
    print("=" * 70)
    pprint(log_series_sym)
    print()
    print("  After substituting A027614 values:")
    pprint(log_series_num)

    print()
    print("  Evaluated at the matrix L  (x -> L), symbolic a_k:")
    egf_matrix_sym = Matrix.zeros(n)
    for k, a_k in enumerate(list_a):
        egf_matrix_sym += ((-1) ** (k + 1) * a_k / factorial(k)) * sub_diag_mu**k
    egf_matrix_sym = egf_matrix_sym.applyfunc(factor)
    pprint(egf_matrix_sym)

    print()
    print("  After substituting A027614 values:")
    egf_matrix = egf_matrix_sym.subs(dict_a).applyfunc(factor)
    pprint(egf_matrix)

    # ------------------------------------------------------------------
    # Step 4: Diagonal similarity with Pochhammer factors
    # ------------------------------------------------------------------
    # Two diagonal matrices built from the Pochhammer symbol (mu+nu+1)_m:
    #
    #   D_L[j, j] = (mu+nu+1)_{2j}   (even-index rising factorials)
    #   D_R[j, j] = (mu+nu+1)_{2j+1} (odd-index rising factorials)
    #
    # The two-sided scaling  D_L^{-1} * G * D_R  removes the Pochhammer weight
    # from the rows and columns of G, exposing the structure of log(J).

    diag_left = make_diag_left(n)
    diag_right = make_diag_right(n)

    print()
    print("=" * 70)
    print("STEP 4 — Pochhammer diagonal scaling (measure correction)")
    print("  D_L[j,j] = (mu+nu+1)_{2j}   (even rising factorials)")
    print("=" * 70)
    pprint(diag_left)
    print()
    print("  D_R[j,j] = (mu+nu+1)_{2j+1}   (odd rising factorials)")
    pprint(diag_right)

    d_t_d = diag_left.inv() * egf_matrix * diag_right
    d_t_d = d_t_d.applyfunc(factor)
    print()
    print("  D_L^{-1} * G * D_R  (Pochhammer-scaled series)")
    pprint(d_t_d)

    # ------------------------------------------------------------------
    # Step 4b: Factorial diagonal similarity  diag(i!) * ... * diag(j!)^{-1}
    # ------------------------------------------------------------------
    # A further conjugation by the factorial diagonal normalizes the
    # row/column scaling so that the resulting matrix has a clean form
    # whose exponential is the Jacobi coefficient matrix.

    diag_factorial = matrix_from_str("factorial(i)", EMatrixType.DIAGONAL, n)
    print()
    print("  Factorial diagonal  diag(i!):")
    pprint(diag_factorial)

    d_t_d = diag_factorial * d_t_d * diag_factorial.inv()
    d_t_d = d_t_d.applyfunc(factor)
    print()
    print("  diag(i!) * [D_L^{-1} G D_R] * diag(j!)^{-1}  (log of Jacobi matrix)")
    pprint(d_t_d)

    # Optional: substitute numeric values of mu and/or nu
    if mu is not None:
        d_t_d = d_t_d.subs({"mu": mu})
        print(f"  → evaluated at mu = {mu}")
    if nu is not None:
        d_t_d = d_t_d.subs({"nu": nu})
        print(f"  → evaluated at nu = {nu}")

    if mu is not None or nu is not None:
        d_t_d = d_t_d.applyfunc(simplify)
        d_t_d = d_t_d.applyfunc(together)
        print("  Log matrix after substitution:")
        pprint(d_t_d)

    # ------------------------------------------------------------------
    # Step 5: Exponentiate to recover the normalized Jacobi matrix
    # ------------------------------------------------------------------
    # Taking the matrix exponential undoes the logarithm:
    #   exp(log(J_normalized)) = J_normalized

    exp_matrix = d_t_d.exp()
    exp_matrix = exp_matrix.applyfunc(factor)
    print()
    print("=" * 70)
    print("STEP 5 — Exponentiate: exp(log matrix) = normalized Jacobi matrix")
    print("=" * 70)
    pprint(exp_matrix)

    # ------------------------------------------------------------------
    # Step 6: Jacobi prefactor diagonal → full Jacobi coefficient matrix
    # ------------------------------------------------------------------
    # The Jacobi diagonal D_J[i,i] = (mu+nu+i+1)_i / i! encodes the
    # leading normalization of P_n^(mu,nu). Left-multiplying recovers J.

    diag_jacobi = make_jacobi_diag(n)
    print()
    print("  Jacobi prefactor diagonal  D_J[i,i] = (mu+nu+i+1)_i / i!:")
    pprint(diag_jacobi)

    jacobi_matrix = diag_jacobi * exp_matrix
    jacobi_matrix = jacobi_matrix.applyfunc(factor)
    if mu is not None:
        jacobi_matrix = jacobi_matrix.subs({"mu": mu})
    if nu is not None:
        jacobi_matrix = jacobi_matrix.subs({"nu": nu})

    print()
    print("=" * 70)
    print("STEP 6 — Jacobi coefficient matrix  J = D_J * exp(log matrix)")
    print("=" * 70)
    pprint(jacobi_matrix)


if __name__ == "__main__":
    main()
