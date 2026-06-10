import click
from sympy import pprint, simplify, factorial
from itertools import product

from maxel.matrix import matrix_from_func, EMatrixType


@click.command()
@click.argument("n", type=int)
def main(n):

    def func_expr(i, j):
        num = f"factorial(i)"
        den = f"(factorial(j)*factorial(i-j))"
        expr_str = f"{num}/{den}"
        return expr_str

    matrix = matrix_from_func(func_expr, EMatrixType.LOWER, n)
    pprint(matrix)

    print("LOG MATRIX")
    log_matrix = matrix.log()
    pprint(log_matrix)


if __name__ == "__main__":
    main()
