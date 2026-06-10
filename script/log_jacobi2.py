import click
from sympy import pprint, simplify, factorial, factor, pretty, RisingFactorial
from itertools import product

from maxel.matrix import matrix_from_str, matrix_from_func, EMatrixType, symbols


@click.command()
@click.argument("n", type=int)
def main(n):

    def func_expr(i, j):
        poly_mu = f"RisingFactorial(mu+{j+1},{i-j})/factorial(i-j)"
        poly_mu_nu = f"RisingFactorial(mu+nu+{i+1},{j})/factorial(j)"

        expr_str = f"{poly_mu}*{poly_mu_nu}"
        return expr_str

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    matrix = matrix.applyfunc(factor)
    pprint(matrix)

    def func_expr(i, j):
        poly_str = f"RisingFactorial(mu+nu+1,{2*j})"
        return poly_str

    diag_1 = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag_1 = diag_1.applyfunc(factor)
    print("DIAG 1")
    pprint(diag_1)

    def func_expr(i, j):
        poly_str = f"RisingFactorial(mu+nu+1,{i})*factorial(i)"
        return poly_str

    diag_2 = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    diag_2 = diag_2.applyfunc(factor)
    print("DIAG 2")
    pprint(diag_2)

    print("*" * 80)
    print("diag_1.inv() * matrix * diag_2")
    print("*" * 80)
    aux_matrix = diag_1.inv() * matrix * diag_2
    aux_matrix = aux_matrix.applyfunc(factor)
    pprint(aux_matrix)

    print("LOG MATRIX")
    log_matrix = aux_matrix.log()
    log_matrix = log_matrix.applyfunc(factor)
    pprint(log_matrix)
    exit()

    def func_expr(i, j):
        poly = f"RisingFactorial(mu+nu+1,{2*j+1})"

        poly_aux = f"({2*i+1}+mu+nu)"
        expr_str = f"({poly})/({poly_aux})"
        return expr_str

    diag_mu_nu_0 = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)

    def func_expr(i, j):
        poly = f"RisingFactorial(mu+nu+1,{2*j})"

        poly_aux = f"({2*j+1}+mu+nu)"
        expr_str = f"({poly}*{poly_aux})"
        return expr_str

    diag_mu_nu_1 = matrix_from_func(func_expr, EMatrixType.DIAGONAL, n)
    log_matrix = diag_mu_nu_0 * log_matrix * diag_mu_nu_1.inv()
    log_matrix = log_matrix.applyfunc(factor)
    print("LOG MATRIX")
    pprint(log_matrix)

    print("*" * 80)
    print("DIVIDE 1/factorial(j) ON RIGHT")
    print("DIVIDE factorial(i) ON LEFT")
    print("*" * 80)
    diag_fact = matrix_from_str("factorial(i)", EMatrixType.DIAGONAL, n)
    log_matrix = diag_fact.inv() * log_matrix * diag_fact
    log_matrix = log_matrix.applyfunc(factor)
    pprint(log_matrix)


if __name__ == "__main__":
    main()
