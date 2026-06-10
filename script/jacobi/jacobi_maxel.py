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
from maxel.sequences import load_and_assign_to
from maxel.matrix import matrix_from_str, matrix_from_func, EMatrixType


def make_diag_left(n):
    def func_expr(i, j):
        poly_str = f"RisingFactorial(mu+nu+1,{2*j})"
        return poly_str

    diag_mu_nu = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)

    return diag_mu_nu


def make_diag_right(n):
    def func_expr(i, j):
        poly_str = f"RisingFactorial(mu+nu+1,{2*j+1})"
        return poly_str

    diag_mu_nu = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)

    return diag_mu_nu


def make_jacobi_diag(n):
    def func_expr(i, j):

        poly_str = f"RisingFactorial(mu+nu+i+1,j)/factorial({j})"
        return poly_str

    diag_mu_nu = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag_mu_nu = diag_mu_nu.applyfunc(factor)

    return diag_mu_nu


@click.command()
@click.argument("n", type=int)
@click.option("--mu", type=int, default=None)
@click.option("--nu", type=int, default=None)
def main(n: int, mu: Optional[int] = None, nu: Optional[int] = None):
    _, _ = symbols("mu, nu")
    list_a = symbols(",".join([f"a{i}" for i in range(n)]))

    dict_a = load_and_assign_to(A027614_FP, list_a)
    print("dict_a", dict_a)

    def func_expr(i, j):

        if i != j + 1:
            return "0"

        return "mu+i"

    sub_diag_mu = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    print("INITIAL MATRIX")
    pprint(sub_diag_mu)

    # exp_ak is sum (ak/k!)*sub_diag_mu**k
    egf_matrix = Matrix.zeros(n)
    for k, a_k in enumerate(list_a):
        egf_matrix += ((-1) ** (k + 1) * a_k / factorial(k)) * sub_diag_mu**k

    egf_matrix = egf_matrix.subs(dict_a)
    egf_matrix = egf_matrix.applyfunc(factor)
    pprint("EXP_ak MATRIX")
    pprint(egf_matrix)

    diag_left = make_diag_left(n)
    diag_right = make_diag_right(n)

    print("DIAG_LEFT")
    pprint(diag_left)
    print("DIAG RIGHT")
    pprint(diag_right)

    d_t_d = diag_left.inv() * egf_matrix * diag_right
    d_t_d = d_t_d.applyfunc(factor)
    print("D_T_D")
    pprint(d_t_d)

    diag_factorial = matrix_from_str("factorial(i)", EMatrixType.DIAGONAL, n)
    d_t_d = diag_factorial * d_t_d * diag_factorial.inv()
    d_t_d = d_t_d.applyfunc(factor)
    print("D_T_D with factorial i!/j!")
    pprint(d_t_d)

    if mu is not None:
        d_t_d = d_t_d.subs({"mu": mu})
        print(f"Evaluated mu={mu}")
    if nu is not None:
        d_t_d = d_t_d.subs({"nu": nu})
        print(f"Evaluated nu={nu}")

    if mu is not None or nu is not None:
        d_t_d = d_t_d.applyfunc(simplify)
        d_t_d = d_t_d.applyfunc(together)
        print("D_T_D evaluated")
        pprint(d_t_d)

    exp_matrix = d_t_d.exp()
    exp_matrix = exp_matrix.applyfunc(factor)
    print("EXP MATRIX")
    pprint(exp_matrix)

    diag_jacobi = make_jacobi_diag(n)
    jacobi_matrix = diag_jacobi * exp_matrix
    jacobi_matrix = jacobi_matrix.applyfunc(factor)
    if mu is not None:
        jacobi_matrix = jacobi_matrix.subs({"mu": mu})
    if nu is not None:
        jacobi_matrix = jacobi_matrix.subs({"nu": nu})

    print("JACOBI MATRIX")
    pprint(jacobi_matrix)


if __name__ == "__main__":
    main()
