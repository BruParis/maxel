import click
from sympy import pprint, simplify, factorial, factor, pretty, RisingFactorial
from itertools import product

from maxel.matrix import matrix_from_str, matrix_from_func, EMatrixType, symbols


@click.command()
@click.argument("n", type=int)
def main(n):

    I_m = matrix_from_str("1", EMatrixType.DIAGONAL, n)
    pprint(I_m)

    def func_expr(i, j):

        poly_mu = f"RisingFactorial(mu+{j+1},{i-j})/factorial(i-j)"
        poly_mu_nu = f"RisingFactorial(mu+nu+{i+1},{j})/factorial(j)"

        expr_str = f"{poly_mu}*{poly_mu_nu}"
        return expr_str

    jacobi_matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    jacobi_matrix = jacobi_matrix.applyfunc(factor)
    pprint(jacobi_matrix)

    def func_expr(i, j):
        poly_str = f"RisingFactorial(mu+nu+{i+1},{j})/factorial({j})"
        return poly_str

    diag = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag = diag.applyfunc(factor)
    pprint(diag)

    print("*" * 80)
    print("DIVIDE mu-nu-DIAGONAL ON LEFT")
    print("*" * 80)
    aux_matrix = diag.inv() * jacobi_matrix
    aux_matrix = aux_matrix.applyfunc(factor)
    pprint(aux_matrix)

    print("INV MATRIX")
    pprint(aux_matrix.inv().applyfunc(factor))

    sub_triangular_matrix = aux_matrix - I_m
    sub_triangular_matrix = sub_triangular_matrix.applyfunc(factor)

    I_minus_matrix = I_m - sub_triangular_matrix
    I_plus_matrix = I_m + sub_triangular_matrix
    print("I MINUS MATRIX")
    pprint(I_minus_matrix.applyfunc(factor))
    print("I PLUS MATRIX inverse")
    pprint(I_plus_matrix.inv().applyfunc(factor))
    cayley_matrix = I_minus_matrix * I_plus_matrix.inv()
    cayley_matrix = cayley_matrix.applyfunc(factor)
    print("CAYLEY MATRIX")
    pprint(cayley_matrix)


if __name__ == "__main__":
    main()
