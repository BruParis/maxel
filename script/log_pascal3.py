import click
from sympy import pprint, simplify, factorial, factor
from itertools import product

from maxel.matrix import matrix_from_func, matrix_from_str, EMatrixType


@click.command()
@click.argument("n", type=int)
def main(n):

    def func_expr(i, j):
        num = "factorial(i+2*j+2)"
        den = "(factorial(3*j+2)*factorial(i-j))"
        expr_str = f"{num}/{den}"
        return expr_str

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    pprint(matrix)

    print("LOG MATRIX")
    log_matrix = matrix.log()
    pprint(log_matrix)


if __name__ == "__main__":
    main()
